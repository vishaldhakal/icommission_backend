from .models import CommissionAdvanceRequest
from rest_framework import serializers

class CommissionAdvanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionAdvanceRequest
        fields = '__all__'