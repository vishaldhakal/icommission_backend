from django.contrib import admin
from .models import Partner
from unfold.admin import ModelAdmin

admin.site.register(Partner,ModelAdmin)