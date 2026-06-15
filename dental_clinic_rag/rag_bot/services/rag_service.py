"""Simple RAG service with TF-IDF."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rag_bot.models import DocumentChunk
from .gemini_service import GeminiService


class RAGService:
    """Simple RAG with TF-IDF retrieval."""
    
    def __init__(self):
        self.gemini = GeminiService()
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.chunks = []
        self.matrix = None
        self._load()
    
    def _load(self):
        """Load chunks and build TF-IDF matrix."""
        docs = DocumentChunk.objects.select_related('document').all()
        if not docs.exists():
            return
        
        self.chunks = []
        texts = []
        for chunk in docs:
            self.chunks.append({
                'text': chunk.chunk_text,
                'title': chunk.document.title,
                'num': chunk.chunk_number
            })
            texts.append(chunk.chunk_text)
        
        if texts:
            self.matrix = self.vectorizer.fit_transform(texts)
    
    def search(self, query, top_k=5):
        """Find relevant chunks."""
        if not self.matrix is None and len(self.chunks) == 0:
            return []
        
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()
        top_idx = scores.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_idx:
            if scores[idx] > 0.1:
                results.append({
                    'text': self.chunks[idx]['text'],
                    'title': self.chunks[idx]['title'],
                    'num': self.chunks[idx]['num'],
                    'score': float(scores[idx])
                })
        return results
    
    def generate_response(self, query):
        """Generate RAG response."""
        chunks = self.search(query)
        
        context = ""
        if chunks:
            context = "\n\n".join([f"[{c['title']}]\n{c['text']}" for c in chunks])
        
        response = self.gemini.generate_response(query, context)
        
        sources = [{'document': c['title'], 'chunk': c['num']} for c in chunks]
        
        return {
            'response': response,
            'sources': sources,
            'has_context': len(chunks) > 0
        }
