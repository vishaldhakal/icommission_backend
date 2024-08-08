from django.contrib import admin
from .models import CustomUser
from unfold.admin import ModelAdmin

admin.site.register(CustomUser,ModelAdmin)
