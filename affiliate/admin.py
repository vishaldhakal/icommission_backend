from django.contrib import admin
from .models import Affiliate, Submission
from unfold.admin import ModelAdmin

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'affiliate_link')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at', 'affiliate_link')

    def affiliate_link(self, obj):
        return obj.create_link()
    
    affiliate_link.short_description = 'Affiliate Link'

class SubmissionAdmin(ModelAdmin):
      list_display = ('name', 'email', 'phone', 'created_at','message')
      search_fields = ('name', 'email', 'phone')

admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(Submission, SubmissionAdmin)

