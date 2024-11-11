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

User = get_user_model()

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
        data = request.data
        user = request.user
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        documents = data.pop('documents', [])
        document_types = data.pop('document_types', [])
        application = Application.objects.get(pk=serializer.data['id'])
        for index, document in enumerate(documents):
            Document.objects.create(application=application, file=document, document_type=document_types[index])
            
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ApplicationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Check if status has changed
        status_changed = False
        if 'status' in serializer.validated_data:
            old_status = instance.status
            new_status = serializer.validated_data['status']
            if old_status != new_status:
                status_changed = True
                instance.status = new_status
                instance.save(update_fields=['status'])
        
        # Handle other fields through ChangeRequest
        changes = {}
        for field, value in serializer.validated_data.items():
            if field == 'status':
                continue
                
            old_value = getattr(instance, field)
            
            # Handle date fields
            if hasattr(old_value, 'isoformat') or old_value is None:
                if old_value != value:
                    changes[field] = value.isoformat()
            # Handle Decimal fields
            elif isinstance(old_value, Decimal):
                if old_value.compare(Decimal(str(value))) != 0:
                    changes[field] = str(value)
            # Handle other fields
            elif old_value != value:
                changes[field] = value if not isinstance(value, Decimal) else str(value)
        
        if changes:
            ChangeRequest.objects.create(
                content_object=instance,
                changes=changes,
                created_by=request.user
            )
            if status_changed:
                return Response({
                    "message": "Status updated and change request created successfully."
                }, status=status.HTTP_202_ACCEPTED)
            return Response({
                "message": "Change request created successfully."
            }, status=status.HTTP_202_ACCEPTED)
        
        if status_changed:
            return Response({
                "message": "Status updated successfully."
            }, status=status.HTTP_200_OK)
            
        return Response({
            "message": "No changes detected."
        }, status=status.HTTP_200_OK)

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

class ChangeRequestListCreate(generics.ListCreateAPIView):
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            # For admin, show requests made by users (non-admin)
            return ChangeRequest.objects.filter(status='Pending', created_by__role='Agent')
        else:
            # For non-admin users, show requests made by admin
            return ChangeRequest.objects.filter(status='Pending', created_by__role='Admin')

class ChangeRequestApprove(generics.UpdateAPIView):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        change_request = self.get_object()
        content_object = change_request.content_object

        if isinstance(content_object, Application):
            content_object.approve_changes(change_request)
        elif isinstance(content_object, Document):
            content_object.approve_changes(change_request)

        return Response({"message": "Changes approved successfully."}, status=status.HTTP_200_OK)

class ChangeRequestReject(generics.UpdateAPIView):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        change_request = self.get_object()
        content_object = change_request.content_object

        if isinstance(content_object, Application):
            content_object.reject_changes(change_request)
        elif isinstance(content_object, Document):
            content_object.reject_changes(change_request)

        return Response({"message": "Changes rejected successfully."}, status=status.HTTP_200_OK)

class ApplicationChangeRequestList(generics.ListAPIView):
    serializer_class = ChangeRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        application_id = self.kwargs['application_id']
        user = self.request.user
        base_queryset = ChangeRequest.objects.filter(
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application_id,
            status='Pending'
        )

        """ if user.role == 'Admin':
            # For admin, show requests made by users (non-admin)
            return base_queryset.filter(created_by__role='Agent')
        else:
            # For non-admin users, show requests made by admin
            return base_queryset.filter(created_by__role='Admin') """

        return base_queryset