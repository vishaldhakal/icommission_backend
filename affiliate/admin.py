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

@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
   list_display = ('name', 'email', 'phone', 'created_at', 'message')
   search_fields = ('created_at','affiliate')
   list_filter = ('created_at','affiliate')
   


