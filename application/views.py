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
    ApplicationCommentSerializer, ChangeRequestSerializer, AdminApplicationCreateSerializer
)
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from django.db import models
from django.db.models import Sum, Count, Case, When, F, DecimalField
from django.db.models.functions import Coalesce
from datetime import datetime
from django.db.models.functions import ExtractDay
from django.db.models import Avg

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
        total=Coalesce(Sum('purchase_commission_amount'), Decimal('0'))
    )['total']
    
    total_advance = applications.aggregate(
        total=Coalesce(Sum('advance_payout_amount'), Decimal('0'))
    )['total']
    
    total_discount_fee = applications.aggregate(
        total=Coalesce(Sum('discount_fee_amount'), Decimal('0'))
    )['total']
    
    # Calculate average APR and term days in Python
    valid_applications = [
        app for app in applications 
        if app.closing_date and app.advance_date and app.purchase_commission_amount 
        and app.discount_fee_amount and app.purchase_commission_amount != 0
    ]

    total_days = Decimal('0')
    apr_values = []
    
    for app in valid_applications:
        days_between = Decimal(str((app.closing_date - app.advance_date).days))
        total_days += days_between
        
        if days_between > 0:
            apr = (
                (app.discount_fee_amount / app.purchase_commission_amount) 
                / days_between 
                * Decimal('365') 
                * Decimal('100')
            )
            apr_values.append(apr)

    # Calculate averages
    avg_term_days = total_days / Decimal(str(len(valid_applications))) if valid_applications else Decimal('0')
    avg_apr = sum(apr_values) / Decimal(str(len(apr_values))) if apr_values else Decimal('0')
    
    # Calculate total agent commission
    total_agent_commission = applications.aggregate(
        total=Coalesce(Sum('deal_commission_amount'), Decimal('0'))
    )['total']
    
    # Calculate average advance ratio
    valid_ratio_apps = [
        app for app in applications 
        if app.deal_commission_amount and app.deal_commission_amount != 0
    ]
    
    total_ratio = Decimal('0')
    if valid_ratio_apps:
        ratios = [
            (app.purchase_commission_amount * Decimal('100') / app.deal_commission_amount)
            for app in valid_ratio_apps
        ]
        total_ratio = sum(ratios) / Decimal(str(len(ratios)))
    
    # Calculate total income realized (from closed deals)
    total_income = applications.filter(status='Closed').aggregate(
        total=Coalesce(Sum('discount_fee_amount'), Decimal('0'))
    )['total']
    
    # Calculate total repayments received
    total_repayments = applications.filter(status='Closed').count()
    
    # Calculate portfolio snapshot
    portfolio_snapshot = {}
    for transaction_type, _ in Application.TRANSACTION_TYPES:
        type_apps = applications.filter(transaction_type=transaction_type)
        portfolio_snapshot[transaction_type] = {
            'count': type_apps.count(),
            'amount': type_apps.aggregate(
                total=Coalesce(Sum('purchase_commission_amount'), Decimal('0'))
            )['total']
        }
    
    # Calculate percentages for portfolio snapshot
    total_amount = sum(item['amount'] for item in portfolio_snapshot.values())
    for key in portfolio_snapshot:
        if total_amount > 0:
            portfolio_snapshot[key]['percentage'] = (
                portfolio_snapshot[key]['amount'] * Decimal('100') / total_amount
            )
        else:
            portfolio_snapshot[key]['percentage'] = Decimal('0')
        # Convert to float for JSON serialization
        portfolio_snapshot[key]['amount'] = float(portfolio_snapshot[key]['amount'])
        portfolio_snapshot[key]['percentage'] = float(portfolio_snapshot[key]['percentage'])

    return Response({
        'key_metrics': {
            'total_purchased_commission_amount': float(total_commission),
            'total_purchase_price': float(total_advance),
            'average_repayment_term': float(avg_term_days),
            'total_discount_fee': float(total_discount_fee),
            'average_apr': float(avg_apr),
            'total_agent_commission': float(total_agent_commission),
            'average_advance_ratio': float(total_ratio),
            'total_income_realized': float(total_income),
            'total_repayments_received': total_repayments
        },
        'portfolio_snapshot': portfolio_snapshot
    })

@api_view(['GET'])
def get_application_analytics(request):
    applications = Application.objects.all()
    closed_applications = applications.filter(status='Closed')
    
    # Calculate metrics in Python instead of database
    def calculate_term_days(app):
        if app.closing_date and app.advance_date:
            return (app.closing_date - app.advance_date).days
        return 0

    def calculate_discount_fee(app):
        if app.purchase_commission_amount and app.advance_payout_amount:
            return float(app.purchase_commission_amount - app.advance_payout_amount)
        return 0

    def calculate_rate(app):
        term_days = calculate_term_days(app)
        discount_fee = calculate_discount_fee(app)
        if term_days > 0 and app.purchase_commission_amount and float(app.purchase_commission_amount) > 0:
            return float((discount_fee / float(app.purchase_commission_amount) / term_days * 365) * 100)
        return 0

    # Calculate aggregates
    total_apps = len(applications)
    if total_apps > 0:
        total_term_days = sum(calculate_term_days(app) for app in applications)
        avg_term_days = total_term_days / total_apps
        
        total_discount_fee = sum(calculate_discount_fee(app) for app in applications)
        total_rates = sum(calculate_rate(app) for app in applications)
        avg_rate = total_rates / total_apps
    else:
        avg_term_days = 0
        total_discount_fee = 0
        avg_rate = 0

    analytics_data = {
        'total_purchase_commission': float(applications.aggregate(
            total=Sum('purchase_commission_amount')
        )['total'] or 0),
        'total_advance_payout': float(applications.aggregate(
            total=Sum('advance_payout_amount')
        )['total'] or 0),
        'average_term_days': round(float(avg_term_days), 2),
        'total_discount_fee': float(total_discount_fee),
        'average_rate': round(float(avg_rate), 2),
        'total_commission_requested': float(applications.aggregate(
            total=Sum('commission_amount_requested')
        )['total'] or 0),
        'total_closed_applications': closed_applications.count(),
        'transaction_type_breakdown': get_transaction_type_breakdown(applications)
    }
    
    return Response(analytics_data)

def get_transaction_type_breakdown(applications):
    breakdown = {}
    total_amount = float(applications.aggregate(
        total=Sum('purchase_commission_amount')
    )['total'] or 0)

    for transaction_type in Application.TRANSACTION_TYPES:
        type_apps = applications.filter(transaction_type=transaction_type[0])
        type_amount = float(type_apps.aggregate(
            total=Sum('purchase_commission_amount')
        )['total'] or 0)
        
        ratio = (type_amount / total_amount * 100) if total_amount > 0 else 0
        
        breakdown[transaction_type[0]] = {
            'amount': type_amount,
            'ratio': round(ratio, 2)
        }
    
    return breakdown

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class ApplicationListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.user.role == 'Admin' and self.request.method == 'POST':
            return AdminApplicationCreateSerializer
        elif self.request.method == 'POST':
            return ApplicationCreateSerializer
        return ApplicationListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.all() if user.role == 'Admin' else Application.objects.filter(user=user)

        # Filter by closing date
        closing_date_from = self.request.query_params.get('closing_date_from')
        closing_date_to = self.request.query_params.get('closing_date_to')

        if closing_date_from:
            queryset = queryset.filter(closing_date__gte=closing_date_from)
        if closing_date_to:
            queryset = queryset.filter(closing_date__lte=closing_date_to)

        return queryset.order_by('-submitted_at')

    def perform_create(self, serializer):
        data = self.request.data.copy()
        if self.request.user.role != 'Admin':
            # For non-admin users, force their own user ID
            data['user'] = self.request.user.id
        serializer.save()

    def create(self, request, *args, **kwargs):
        # Create a mutable copy of the request data
        data = request.data.copy()
        
        # If not admin, force the user ID to be the current user
        if request.user.role != 'Admin':
            data['user'] = request.user.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()  # Save and get the application instance
        headers = self.get_success_headers(serializer.data)
        
        # Handle documents if they exist
        documents = request.FILES.getlist('documents', [])
        document_types = request.POST.getlist('document_types', [])
        
        for index, document in enumerate(documents):
            if index < len(document_types):
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