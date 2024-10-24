from rest_framework import serializers
from .models import Application, Document, Note, ApplicationComment, ChangeRequest
from accounts.serializers import UserSmallestSerializer, UserSmallSerializer
from decimal import Decimal

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'note_type', 'content', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'document_type', 'file', 'uploaded_at', 'notes', 'status']

class ChangeRequestSerializer(serializers.ModelSerializer):
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = ChangeRequest
        fields = ['id', 'changes', 'created_by', 'created_at', 'status', 'approved_by', 'approved_at', 'content_type_name']

    def get_content_type_name(self, obj):
        return obj.content_type.model

class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    user = UserSmallSerializer(read_only=True)
    pending_changes = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'status', 'submitted_at', 'updated_at', 'transaction_type',
            'transaction_address', 'deal_commission_amount', 'purchase_commission_amount',
            'advance_payout_amount', 'discount_fee_amount', 'advance_date', 'closing_date',
            'documents', 'pending_changes', 'transaction_count', 'commission_amount_requested'
        ]

    def get_pending_changes(self, obj):
        pending_changes = obj.get_pending_changes()
        return ChangeRequestSerializer(pending_changes, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        decimal_fields = ['deal_commission_amount', 'purchase_commission_amount', 'advance_payout_amount', 'discount_fee_amount', 'commission_amount_requested']
        for field in decimal_fields:
            if representation[field] is not None:
                representation[field] = str(representation[field])
        return representation

class ApplicationListSerializer(serializers.ModelSerializer):
    user = UserSmallestSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'closing_date', 'status', 'submitted_at', 'updated_at',
            'transaction_type', 'transaction_address', 'deal_commission_amount',
            'purchase_commission_amount', 'advance_payout_amount', 'advance_date', 
            'transaction_count', 'discount_fee_amount', 'commission_amount_requested'
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
