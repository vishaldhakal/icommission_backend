from django.contrib import admin
from .models import CommissionAdvanceRequest
from unfold.admin import ModelAdmin
@admin.register(CommissionAdvanceRequest)
class CommissionAdvanceRequestAdmin(ModelAdmin):
   fieldsets = (
      ("Advance Request Information", {"fields": (("user", "advance_type", "transaction_address"), ("transaction_closing_date", "deposit_amount","amount_requested"), "purchase_and_sale_agreement", "waivers_of_conditions", "trade_record_sheet", "deposit_cheque_or_receipt", "copy_of_sold_mls_listing")}),
   )
   list_display = ("user", "advance_type", "transaction_address", "transaction_closing_date", "deposit_amount", "amount_requested")
   list_filter = ("advance_type", "transaction_closing_date","user")
   search_fields = ("advance_type", "transaction_closing_date","user")