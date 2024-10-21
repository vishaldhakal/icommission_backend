from rest_framework import serializers
from .models import Application, Document, Note, ApplicationComment
from accounts.serializers import UserSmallestSerializer, UserSmallSerializer

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'note_type', 'content', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'document_type', 'file', 'uploaded_at', 'notes', 'status']

class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    user = UserSmallSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'status', 'submitted_at', 'updated_at', 'transaction_type',
            'transaction_address', 'deal_commission_amount', 'purchase_commission_amount',
            'advance_payout_amount', 'discount_fee_amount', 'advance_date', 'closing_date',
            'documents'
        ]

class ApplicationListSerializer(serializers.ModelSerializer):
    user = UserSmallestSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'closing_date', 'status', 'submitted_at', 'updated_at',
            'transaction_type', 'transaction_address', 'deal_commission_amount',
            'purchase_commission_amount', 'advance_payout_amount','advance_date', 'transaction_count','discount_fee_amount'
        ]

class ApplicationCreateSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'

class ApplicationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationComment
        fields = ['id', 'comment', 'comment_type', 'created_at']