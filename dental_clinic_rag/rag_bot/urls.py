"""
URL configuration for rag_bot app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_message, name='chat_message'),
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
    path('documents/', views.get_documents, name='get_documents'),
    path('documents/<int:document_id>/process/', views.process_document, name='process_document'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('clear-chat/', views.clear_chat, name='clear_chat'),
]
