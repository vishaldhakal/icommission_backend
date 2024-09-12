from django.contrib import admin
from .models import DocumentNote, Document, CommissionAdvanceRequest,InvoiceItem,Invoice
from unfold.admin import ModelAdmin


admin.site.register(DocumentNote, ModelAdmin)
admin.site.register(Document, ModelAdmin)
admin.site.register(CommissionAdvanceRequest, ModelAdmin)
admin.site.register(InvoiceItem, ModelAdmin)
admin.site.register(Invoice, ModelAdmin)