from django.contrib import admin
from .models import Affiliate, Submission
from unfold.admin import ModelAdmin

class AffiliateAdmin(ModelAdmin):
      list_display = ('name', 'email', 'created_at', 'id')
      search_fields = ('name', 'email')

class SubmissionAdmin(ModelAdmin):
      list_display = ('name', 'email', 'phone', 'created_at','message')
      search_fields = ('name', 'email', 'phone')

admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(Submission, SubmissionAdmin)

