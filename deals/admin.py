from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Deal, PortfolioSettings

@admin.register(Deal)
class DealAdmin(ModelAdmin):
    list_display = ('file', 'date', 'name', 'company', 'type', 
                   'purchased_commission_amount', 'status')
    list_filter = ('status', 'type', 'category')
    search_fields = ('file', 'name', 'company', 'transaction_address')
    readonly_fields = ('term_days', 'discount_fee', 'rate', 
                      'advance_ratio', 'countdown')
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
            'fields': ('term_days', 'discount_fee', 'rate', 
                      'advance_ratio', 'countdown')
        }),
        ('Additional Information', {
            'fields': ('internal_notes',)
        }),
    )

@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(ModelAdmin):
    list_display = ('exposure_basis', 'updated_at')
