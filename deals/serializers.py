from rest_framework import serializers
from .models import Deal, PortfolioSettings

class DealSerializer(serializers.ModelSerializer):
    term_days = serializers.IntegerField(read_only=True)
    discount_fee = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    rate = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    advance_ratio = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    countdown = serializers.IntegerField(read_only=True)

    class Meta:
        model = Deal
        fields = '__all__'

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
    average_repayment_term = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_discount_fee = serializers.DecimalField(max_digits=15, decimal_places=2)
    average_apr = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_agent_commission = serializers.DecimalField(max_digits=15, decimal_places=2)
    average_advance_ratio = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_income_realized = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_repayments_received = serializers.IntegerField()
    portfolio_breakdown = serializers.DictField(
        child=PortfolioBreakdownSerializer()
    ) 