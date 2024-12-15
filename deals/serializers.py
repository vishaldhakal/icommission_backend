from rest_framework import serializers
from .models import Deal, PortfolioSettings

class DealSerializer(serializers.ModelSerializer):
    term_days = serializers.SerializerMethodField()
    discount_fee = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    advance_ratio = serializers.SerializerMethodField()
    countdown = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = '__all__'

    def get_term_days(self, obj):
        return obj.calculate_term_days()

    def get_discount_fee(self, obj):
        return obj.calculate_discount_fee()

    def get_rate(self, obj):
        return obj.calculate_rate()

    def get_advance_ratio(self, obj):
        return obj.calculate_advance_ratio()

    def get_countdown(self, obj):
        return obj.calculate_countdown()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Ensure computed fields are properly formatted
        data['term_days'] = self.get_term_days(instance)
        data['discount_fee'] = self.get_discount_fee(instance)
        data['rate'] = self.get_rate(instance)
        data['advance_ratio'] = self.get_advance_ratio(instance)
        data['countdown'] = self.get_countdown(instance)
        return data

class PortfolioSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioSettings
        fields = '__all__'

class PortfolioBreakdownSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    ratio = serializers.DecimalField(max_digits=5, decimal_places=2)

class DealAnalyticsSerializer(serializers.Serializer):
    total_purchased_commission = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_purchase_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    average_repayment_term = serializers.IntegerField()
    total_discount_fee = serializers.DecimalField(max_digits=15, decimal_places=2)
    average_apr = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_agent_commission = serializers.DecimalField(max_digits=15, decimal_places=2)
    average_advance_ratio = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_income_realized = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_repayments_received = serializers.IntegerField()
    portfolio_breakdown = serializers.DictField(
        child=PortfolioBreakdownSerializer()
    ) 