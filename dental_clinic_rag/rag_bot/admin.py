from django.contrib import admin
from .models import PDFDocument, DocumentChunk, Conversation, ChatMessage


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'filename', 'uploaded_at', 'is_processed']
    list_filter = ['is_processed', 'uploaded_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at']


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['document', 'chunk_number', 'created_at']
    list_filter = ['document', 'created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'timestamp', 'content_preview']
    list_filter = ['role', 'timestamp']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
