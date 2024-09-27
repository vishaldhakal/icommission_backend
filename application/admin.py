from django.contrib import admin
from .models import Application,Document,Note
from unfold.admin import ModelAdmin


admin.site.register(Application,ModelAdmin)
admin.site.register(Document,ModelAdmin)
admin.site.register(Note,ModelAdmin)