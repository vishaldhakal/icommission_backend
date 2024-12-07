from django.contrib import admin
from .models import Application, Document, Note, ApplicationComment, ChangeRequest
from unfold.admin import ModelAdmin
from django.db.models import Q


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ('user', 'status', 'transaction_type', 'submitted_at', 'updated_at')
    list_filter = ('status', 'transaction_type')
    search_fields = ('user__username', 'transaction_address')
    autocomplete_fields = ['user']

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(
                Q(user__first_name__icontains=search_term) |
                Q(user__last_name__icontains=search_term) |
                Q(user__email__icontains=search_term)
            )
        return queryset, may_have_duplicates

    def get_form(self, request, obj=None, **kwargs):
        self.request = request
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        self.request = request
        super().save_model(request, obj, form, change)

@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ('application', 'document_type', 'status', 'uploaded_at')
    list_filter = ('document_type', 'status')
    search_fields = ('application__user__username',)

@admin.register(Note)
class NoteAdmin(ModelAdmin):
    list_display = ('document', 'note_type', 'created_at')
    list_filter = ('note_type',)
    search_fields = ('content',)

@admin.register(ApplicationComment)
class ApplicationCommentAdmin(ModelAdmin):
    list_display = ('application', 'comment_type', 'created_at')
    list_filter = ('comment_type',)
    search_fields = ('comment',)

@admin.register(ChangeRequest)
class ChangeRequestAdmin(ModelAdmin):
    list_display = ('content_object', 'status', 'created_by', 'created_at', 'approved_by', 'approved_at')
    list_filter = ('status',)
    search_fields = ('created_by__username', 'approved_by__username')
