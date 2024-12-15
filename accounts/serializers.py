from .models import CustomUser, Brokerage
from rest_framework import serializers

class BrokerageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brokerage
        fields = '__all__'

class UserSmallestSerializer(serializers.ModelSerializer):
    brokerage_details = BrokerageSerializer(source='brokerage', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'brokerage_details']

class UserSmallSerializer(serializers.ModelSerializer):
    brokerage_details = BrokerageSerializer(source='brokerage', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'phone_number', 
                 'license_number', 'brokerage_details', 'emergency_contact_name', 
                 'emergency_contact_phone', 'driver_license', 't4a', 'institution_id', 
                 'transit_number', 'account_number']

class UserSerializer(serializers.ModelSerializer):
    brokerage_details = BrokerageSerializer(source='brokerage', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 
                 'role', 'phone_number', 'license_number', 'brokerage', 'brokerage_details',
                 'emergency_contact_name', 'emergency_contact_phone', 'driver_license',
                 't4a', 'void_cheque_or_direct_doposite_form', 'annual_commission_statement', 
                 'deposit_cheque_or_receipt', 'institution_id', 'transit_number', 'account_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    brokerage_details = BrokerageSerializer(source='brokerage', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'phone_number', 'license_number',
                  'emergency_contact_name', 'emergency_contact_phone', 'driver_license',
                  't4a', 'void_cheque_or_direct_doposite_form', 'annual_commission_statement',
                  'deposit_cheque_or_receipt', 'institution_id', 'transit_number', 'account_number',
                  'brokerage_details']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
