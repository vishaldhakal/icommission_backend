from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'user', 'name', 'broker_of_record', 'deal_admin_email', 'emergency_phone', 
                  'upload_id', 'purchase_sale_agreement', 'mls_listing', 'submitted_at', 'status']
        read_only_fields = ['id', 'user', 'submitted_at']