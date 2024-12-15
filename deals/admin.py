from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Deal, PortfolioSettings

@admin.register(Deal)
class DealAdmin(ModelAdmin):
    list_display = ('file', 'date', 'name', 'company', 'type', 
                   'purchased_commission_amount', 'status')
    list_filter = ('status', 'type', 'category')
    search_fields = ('file', 'name', 'company', 'transaction_address')
    readonly_fields = ('calculate_term_days', 'calculate_discount_fee', 
                      'calculate_rate', 'calculate_advance_ratio', 
                      'calculate_countdown')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('file', 'date', 'category', 'status')
        }),
        ('Deal Details', {
            'fields': ('transaction_address', 'name', 'company', 'type')
        }),
        ('Financial Information', {
            'fields': ('purchased_commission_amount', 'purchase_price', 
                      'closing_date', 'agent_commission')
        }),
        ('Calculated Fields', {
            'fields': ('calculate_term_days', 'calculate_discount_fee', 
                      'calculate_rate', 'calculate_advance_ratio', 
                      'calculate_countdown')
        }),
        ('Additional Information', {
            'fields': ('internal_notes',)
        }),
    )

    def calculate_term_days(self, obj):
        return obj.calculate_term_days()
    calculate_term_days.short_description = 'Term Days'

    def calculate_discount_fee(self, obj):
        return obj.calculate_discount_fee()
    calculate_discount_fee.short_description = 'Discount Fee'

    def calculate_rate(self, obj):
        return obj.calculate_rate()
    calculate_rate.short_description = 'Rate'

    def calculate_advance_ratio(self, obj):
        return obj.calculate_advance_ratio()
    calculate_advance_ratio.short_description = 'Advance Ratio'

    def calculate_countdown(self, obj):
        return obj.calculate_countdown()
    calculate_countdown.short_description = 'Countdown'

@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(ModelAdmin):
    list_display = ('exposure_basis', 'updated_at')
