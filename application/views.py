from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
import random
import string
from .models import Application, Document, Note, ApplicationComment, ChangeRequest
from .serializers import (
    ApplicationSerializer, DocumentSerializer, NoteSerializer, 
    ApplicationCreateSerializer, ApplicationListSerializer, 
    ApplicationCommentSerializer, ChangeRequestSerializer
)
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from django.db import models
from django.db.models import Sum, Count, Case, When, F, DecimalField
from django.db.models.functions import Coalesce
from datetime import datetime
from django.db.models.functions import ExtractDay

User = get_user_model()


@api_view(['GET'])
def get_document_types(request):
    return Response([choice[0] for choice in Document.DOCUMENT_TYPES])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_analytics(request):
    # Get all applications
    applications = Application.objects.all()
    
    # Calculate key metrics
    total_commission = applications.aggregate(
        total=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
    )['total']
    
    total_advance = applications.aggregate(
        total=Coalesce(Sum('advance_payout_amount'), Decimal('0'))
    )['total']
    
    total_discount_fee = applications.aggregate(
        total=Coalesce(Sum('discount_fee_amount'), Decimal('0'))
    )['total']
    
    # Calculate average APR
    applications_with_dates = applications.exclude(
        closing_date=None
    ).exclude(
        advance_date=None
    ).exclude(
        purchase_commission_amount=None
    ).exclude(
        discount_fee_amount=None
    ).exclude(
        purchase_commission_amount=0
    )

    apr_values = []
    for app in applications_with_dates:
        try:
            # Calculate days between closing and advance date
            days_between = (app.closing_date - app.advance_date).days
            if days_between > 0:  # Only calculate if days is positive
                # Calculate APR for this application
                apr = (
                    (app.discount_fee_amount / app.purchase_commission_amount) 
                    / days_between 
                    * 365 
                    * 100  # Convert to percentage
                )
                apr_values.append(apr)
        except (ZeroDivisionError, AttributeError):
            continue

    # Calculate average APR
    avg_apr = (
        sum(apr_values) / len(apr_values) 
        if apr_values 
        else 0
    )
    
    # Calculate total agent commission
    total_agent_commission = applications.aggregate(
        total=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
    )['total']
    
    # Calculate average advance ratio
    applications_with_ratio = applications.exclude(
        deal_commission_amount=None
    ).exclude(deal_commission_amount=0)
    
    total_ratio = applications_with_ratio.aggregate(
        ratio=Coalesce(
            Sum(F('purchase_commission_amount') * 100.0 / F('deal_commission_amount'), 
                output_field=DecimalField()) / Count('id'),
            Decimal('0')
        )
    )['ratio']
    
    # Calculate total income realized (from closed deals)
    total_income = applications.filter(status='Closed').aggregate(
        total=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
    )['total']
    
    # Calculate total repayments received
    total_repayments = applications.filter(status='Closed').count()
    
    # Calculate portfolio snapshot
    portfolio_snapshot = {
        'Pre-construction': applications.filter(transaction_type='Pre-construction').aggregate(
            count=Count('id'),
            amount=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
        ),
        'Commercial': applications.filter(transaction_type='Commercial').aggregate(
            count=Count('id'),
            amount=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
        ),
        'Resale': applications.filter(transaction_type='Resale').aggregate(
            count=Count('id'),
            amount=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
        ),
        'Line of Credit': applications.filter(transaction_type='Lease').aggregate(
            count=Count('id'),
            amount=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
        ),
    }
    
    # Calculate percentages for portfolio snapshot
    total_amount = sum(item['amount'] for item in portfolio_snapshot.values())
    for key in portfolio_snapshot:
        if total_amount > 0:
            portfolio_snapshot[key]['percentage'] = (portfolio_snapshot[key]['amount'] / total_amount) * 100
        else:
            portfolio_snapshot[key]['percentage'] = 0

    return Response({
        'key_metrics': {
            'total_purchased_commission_amount': float(total_commission),
            'total_purchase_price': float(total_advance),
            'average_repayment_term': 120,  # This could be calculated based on your business logic
            'total_discount_fee': float(total_discount_fee),
            'average_apr': float(avg_apr),
            'total_agent_commission': float(total_agent_commission),
            'average_advance_ratio': float(total_ratio),
            'total_income_realized': float(total_income),
            'total_repayments_received': total_repayments
        },
        'portfolio_snapshot': portfolio_snapshot
    })

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ApplicationListCreate(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.all() if user.role == 'Admin' else Application.objects.filter(user=user) if user.role == 'Agent' else Application.objects.none()

        # Filter by closing date
        closing_date_from = self.request.query_params.get('closing_date_from')
        closing_date_to = self.request.query_params.get('closing_date_to')

        if closing_date_from:
            queryset = queryset.filter(closing_date__gte=closing_date_from)
        if closing_date_to:
            queryset = queryset.filter(closing_date__lte=closing_date_to)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ApplicationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ApplicationListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        # Create a mutable copy of the request data
        data = request.data.copy()
        user = request.user
        data['user'] = user.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Handle documents
        documents = data.pop('documents', [])
        document_types = data.pop('document_types', [])
        application = Application.objects.get(pk=serializer.data['id'])
        
        for index, document in enumerate(documents):
            Document.objects.create(
                application=application, 
                file=document, 
                document_type=document_types[index]
            )
            
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ApplicationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Create a mutable copy of the request data
        data = request.data.copy()
        
        # Store the request in thread local storage
        from threading import current_thread
        current_thread().request = request
        
        try:
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        finally:
            # Clean up thread local storage
            if hasattr(current_thread(), 'request'):
                delattr(current_thread(), 'request')

class DocumentListCreate(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(application_id=self.kwargs['application_id'])

    def perform_create(self, serializer):
        application = Application.objects.get(pk=self.kwargs['application_id'])
        serializer.save(application=application)

class DocumentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(document_id=self.kwargs['document_id'])

    def perform_create(self, serializer):
        document = Document.objects.get(pk=self.kwargs['document_id'])
        serializer.save(document=document)

class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class ApplicationCommentListCreate(generics.ListCreateAPIView):
    serializer_class = ApplicationCommentSerializer

    def get_queryset(self):
        return ApplicationComment.objects.filter(application_id=self.kwargs['application_id'])
    
    def perform_create(self, serializer):
        application = Application.objects.get(pk=self.kwargs['application_id'])
        serializer.save(application=application)

class ApplicationCommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationComment.objects.all()
    serializer_class = ApplicationCommentSerializer

class ApplicationChangeHistoryList(generics.ListAPIView):
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        application_id = self.kwargs['application_id']
        return ChangeRequest.objects.filter(
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application_id
        ).select_related('created_by').order_by('-created_at')