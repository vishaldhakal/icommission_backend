from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
import random
import string
from .models import Application, Document, Note, ApplicationComment
from .serializers import ApplicationSerializer, DocumentSerializer, NoteSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationCommentSerializer

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