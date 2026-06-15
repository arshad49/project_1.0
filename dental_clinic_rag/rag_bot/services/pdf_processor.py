"""Simple PDF processor."""
import PyPDF2
from rag_bot.models import PDFDocument, DocumentChunk


class PDFProcessor:
    """Simple PDF text extraction and chunking."""
    
    @staticmethod
    def process_pdf(document_id, chunk_size=1000, overlap=200):
        """Extract text from PDF and save chunks."""
        document = PDFDocument.objects.get(id=document_id)
        
        # Extract text
        text = ""
        with open(document.pdf_file.path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        if not text.strip():
            raise Exception("No text found in PDF")
        
        # Chunk text
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - overlap
        
        # Save chunks
        DocumentChunk.objects.filter(document=document).delete()
        for i, chunk_text in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document,
                chunk_text=chunk_text,
                chunk_number=i + 1
            )
        
        document.is_processed = True
        document.save()
        
        return len(chunks)
