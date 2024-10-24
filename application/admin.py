from django.contrib import admin
from .models import Application, Document, Note, ApplicationComment, ChangeRequest
from unfold.admin import ModelAdmin


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ('user', 'status', 'transaction_type', 'submitted_at', 'updated_at')
    list_filter = ('status', 'transaction_type')
    search_fields = ('user__username', 'transaction_address')

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
