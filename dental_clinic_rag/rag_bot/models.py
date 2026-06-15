from django.db import models
import os


class PDFDocument(models.Model):
    """Model to store uploaded PDF documents for the dental clinic RAG bot."""
    
    title = models.CharField(max_length=255, help_text="Document title")
    pdf_file = models.FileField(upload_to='pdfs/', help_text="Upload PDF file")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, help_text="Whether PDF has been processed and chunked")
    description = models.TextField(blank=True, help_text="Optional description of the document")
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.pdf_file.name)


class DocumentChunk(models.Model):
    """Model to store chunks of text extracted from PDFs for RAG retrieval."""
    
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='chunks')
    chunk_text = models.TextField(help_text="Text content of this chunk")
    chunk_number = models.IntegerField(help_text="Order of this chunk in the document")
    embedding = models.BinaryField(null=True, blank=True, help_text="Vector embedding of the chunk")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['document', 'chunk_number']
        indexes = [
            models.Index(fields=['document', 'chunk_number']),
        ]
    
    def __str__(self):
        return f"Chunk {self.chunk_number} of {self.document.title}"


class Conversation(models.Model):
    """Model to store chat conversations."""
    
    session_id = models.CharField(max_length=255, db_index=True, help_text="User session identifier")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.session_id}"


class ChatMessage(models.Model):
    """Model to store individual chat messages."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField(help_text="Message content")
    timestamp = models.DateTimeField(auto_now_add=True)
    source_chunks = models.TextField(blank=True, null=True, help_text="JSON of source chunks used for this response")
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
