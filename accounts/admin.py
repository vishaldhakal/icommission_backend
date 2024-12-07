from django.contrib import admin
from django.contrib.auth import get_user_model
from unfold.admin import ModelAdmin

User = get_user_model()

@admin.register(User)
class UserAdmin(ModelAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_display = ['username', 'email', 'first_name', 'last_name']
