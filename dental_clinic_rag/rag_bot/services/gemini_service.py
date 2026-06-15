"""Simple Gemini AI Service."""
import google.generativeai as genai
from django.conf import settings


class GeminiService:
    """Simple Gemini AI integration."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_response(self, prompt, context=""):
        """Generate response with optional context."""
        if context:
            full_prompt = f"""You are a dental clinic assistant. Use this context to answer:

Context:
{context}

Question: {prompt}

Answer based on the context. If not found, provide general dental information."""
        else:
            full_prompt = f"You are a dental clinic assistant. Answer: {prompt}"
        
        response = self.model.generate_content(full_prompt)
        return response.text
