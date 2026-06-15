"""
Views for the RAG bot - Handle chat, PDF upload, and document management.
"""
import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rag_bot.models import PDFDocument, Conversation, ChatMessage
from rag_bot.services.pdf_processor import PDFProcessor
from rag_bot.services.rag_service import RAGService


def index(request):
    """Main chat interface view."""
    # Create or get session
    if 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())
    
    session_id = request.session['session_id']
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(session_id=session_id)
    
    # Get chat history
    messages = ChatMessage.objects.filter(conversation=conversation).order_by('timestamp')
    
    # Get uploaded documents
    documents = PDFDocument.objects.all().order_by('-uploaded_at')
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'documents': documents,
    }
    
    return render(request, 'rag_bot/chat.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    """Handle chat message and generate RAG response."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Get or create session
            if 'session_id' not in request.session:
                request.session['session_id'] = str(uuid.uuid4())
            
            session_id = request.session['session_id']
            conversation, created = Conversation.objects.get_or_create(session_id=session_id)
            
            # Save user message
            ChatMessage.objects.create(
                conversation=conversation,
                role='user',
                content=user_message
            )
            
            # Generate RAG response
            rag_service = RAGService()
            result = rag_service.generate_response(user_message, session_id)
            
            # Save assistant response
            ChatMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=result['response'],
                source_chunks=json.dumps(result['sources']) if result['sources'] else None
            )
            
            return JsonResponse({
                'response': result['response'],
                'sources': result['sources'],
                'has_context': result['has_context']
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def upload_pdf(request):
    """Handle PDF file upload."""
    try:
        if 'pdf_file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        pdf_file = request.FILES['pdf_file']
        title = request.POST.get('title', pdf_file.name)
        description = request.POST.get('description', '')
        
        # Validate file type
        if not pdf_file.name.endswith('.pdf'):
            return JsonResponse({'error': 'Only PDF files are allowed'}, status=400)
        
        # Save document
        document = PDFDocument.objects.create(
            title=title,
            pdf_file=pdf_file,
            description=description
        )
        
        # Process PDF
        try:
            num_chunks = PDFProcessor.process_pdf(document.id)
            return JsonResponse({
                'success': True,
                'message': f'PDF uploaded and processed successfully. Created {num_chunks} chunks.',
                'document_id': document.id,
                'num_chunks': num_chunks
            })
        except Exception as e:
            return JsonResponse({
                'error': f'File uploaded but processing failed: {str(e)}',
                'document_id': document.id
            }, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def process_document(request, document_id):
    """Re-process a PDF document."""
    try:
        document = get_object_or_404(PDFDocument, id=document_id)
        num_chunks = PDFProcessor.process_pdf(document.id)
        
        return JsonResponse({
            'success': True,
            'message': f'Document re-processed successfully. Created {num_chunks} chunks.',
            'num_chunks': num_chunks
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def delete_document(request, document_id):
    """Delete a PDF document and its chunks."""
    try:
        document = get_object_or_404(PDFDocument, id=document_id)
        document.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Document deleted successfully.'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_documents(request):
    """Get list of uploaded documents."""
    documents = PDFDocument.objects.all().order_by('-uploaded_at')
    
    docs_data = []
    for doc in documents:
        docs_data.append({
            'id': doc.id,
            'title': doc.title,
            'filename': doc.filename(),
            'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M'),
            'is_processed': doc.is_processed,
            'description': doc.description,
            'chunk_count': doc.chunks.count()
        })
    
    return JsonResponse({'documents': docs_data})


def clear_chat(request):
    """Clear chat history for current session."""
    if 'session_id' in request.session:
        session_id = request.session['session_id']
        try:
            conversation = Conversation.objects.get(session_id=session_id)
            conversation.messages.all().delete()
        except Conversation.DoesNotExist:
            pass
    
    return JsonResponse({'success': True, 'message': 'Chat history cleared.'})
