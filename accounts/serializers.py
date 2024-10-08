from .models import CustomUser
from rest_framework import serializers

class UserSmallestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role','current_brokerage_name']

class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'license_number', 'current_brokerage_name', 'brokerage_phone', 'broker_of_record_name', 'broker_of_record_email', 'emergency_contact_name', 'emergency_contact_phone', 'driver_license','deal_administrator_name', 'deal_administrator_email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number', 'license_number', 'current_brokerage_name', 'brokerage_phone', 'broker_of_record_name', 'broker_of_record_email', 'emergency_contact_name', 'emergency_contact_phone', 'driver_license']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'license_number',
                  'current_brokerage_name', 'brokerage_phone', 'broker_of_record_name',
                  'broker_of_record_email', 'deal_administrator_name', 'deal_administrator_email',
                  'emergency_contact_name', 'emergency_contact_phone', 'driver_license']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
