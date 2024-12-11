from rest_framework import serializers
from .models import Application, Document, Note, ApplicationComment, ChangeRequest, ContentType
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
    created_by_name = serializers.SerializerMethodField()
    change_time = serializers.SerializerMethodField()
    changes_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ChangeRequest
        fields = ['id', 'changes', 'changes_formatted', 'created_by', 'created_by_name', 'created_at', 'content_type_name', 'change_time']

    def get_content_type_name(self, obj):
        return obj.content_type.model

    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    def get_change_time(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_changes_formatted(self, obj):
        formatted = {}
        for field, value in obj.changes.items():
            if field in ['deal_commission_amount', 'purchase_commission_amount', 
                        'advance_payout_amount', 'discount_fee_amount']:
                formatted[field] = str(value)
            elif field in ['closing_date', 'advance_date'] and value:
                formatted[field] = value
            else:
                formatted[field] = value
        return formatted

class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    user = UserSmallSerializer(read_only=True)
    change_history = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'status', 'submitted_at', 'updated_at', 'transaction_type',
            'transaction_address', 'deal_commission_amount', 'purchase_commission_amount',
            'advance_payout_amount', 'discount_fee_amount', 'advance_date', 'closing_date',
            'documents', 'change_history', 'transaction_count', 'commission_amount_requested'
        ]

    def get_change_history(self, obj):
        changes = ChangeRequest.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        ).order_by('-created_at')
        return ChangeRequestSerializer(changes, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Handle decimal fields
        decimal_fields = ['deal_commission_amount', 'purchase_commission_amount', 
                         'advance_payout_amount', 'discount_fee_amount', 
                         'commission_amount_requested']
        for field in decimal_fields:
            if representation.get(field) is not None:
                representation[field] = str(representation[field])
        
        # Handle date fields
        date_fields = ['advance_date', 'closing_date']
        for field in date_fields:
            value = getattr(instance, field)
            if value is not None:
                representation[field] = value.isoformat()
            else:
                representation[field] = None
                
        return representation

class ApplicationListSerializer(serializers.ModelSerializer):
    user = UserSmallestSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user','closing_date', 'status', 'submitted_at', 'updated_at',
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
