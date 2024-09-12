from .models import DocumentNote, Document, CommissionAdvanceRequest,InvoiceItem,Invoice
from rest_framework import serializers

class DocumentNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentNote
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class CommissionAdvanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionAdvanceRequest
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'