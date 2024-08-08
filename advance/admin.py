from django.contrib import admin
from .models import CommissionAdvanceRequest
from unfold.admin import ModelAdmin

admin.site.register(CommissionAdvanceRequest,ModelAdmin)