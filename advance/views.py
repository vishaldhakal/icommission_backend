from rest_framework import generics
from .models import DocumentNote, Document, CommissionAdvanceRequest, InvoiceItem, Invoice
from .serializers import DocumentNoteSerializer, DocumentSerializer, CommissionAdvanceRequestSerializer, InvoiceItemSerializer, InvoiceSerializer

class DocumentNoteListCreate(generics.ListCreateAPIView):
    queryset = DocumentNote.objects.all()
    serializer_class = DocumentNoteSerializer

class DocumentNoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentNote.objects.all()
    serializer_class = DocumentNoteSerializer

class DocumentListCreate(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class CommissionAdvanceRequestListCreate(generics.ListCreateAPIView):
    queryset = CommissionAdvanceRequest.objects.all()
    serializer_class = CommissionAdvanceRequestSerializer

class CommissionAdvanceRequestRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommissionAdvanceRequest.objects.all()
    serializer_class = CommissionAdvanceRequestSerializer

class InvoiceItemListCreate(generics.ListCreateAPIView):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

class InvoiceItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

class InvoiceListCreate(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer