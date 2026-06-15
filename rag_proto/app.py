from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ollama
import os

app = Flask(__name__)

# Store context and vectorizer globally (simple approach for prototype)
context_data = ""
vectorizer = None
tfidf_matrix = None
chunks = []


def split_text_into_chunks(text, chunk_size=200):
    """Split text into smaller chunks for better search"""
    words = text.split()
    chunks_list = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # +1 for space
        current_chunk.append(word)

        if current_length >= chunk_size:
            chunks_list.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    # Add remaining words
    if current_chunk:
        chunks_list.append(" ".join(current_chunk))

    return chunks_list


def setup_vectorizer(text):
    """Create vectorizer and transform text into numerical format"""
    global vectorizer, tfidf_matrix, chunks

    if not text.strip():
        return False

    # Split text into chunks
    chunks = split_text_into_chunks(text)

    if len(chunks) == 0:
        return False

    # Create vectorizer and transform chunks
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(chunks)

    return True


def find_relevant_chunks(query, top_k=3):
    """Find the most relevant chunks for a query"""
    global vectorizer, tfidf_matrix, chunks

    if vectorizer is None or tfidf_matrix is None:
        return []

    # Transform query using same vectorizer
    query_vec = vectorizer.transform([query])

    # Calculate similarity between query and all chunks
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # Get indices of top_k most similar chunks
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    # Return the relevant chunks
    relevant = []
    for idx in top_indices:
        if similarities[idx] > 0:  # Only include chunks with some similarity
            relevant.append(chunks[idx])

    return relevant


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_context', methods=['POST'])
def add_context():
    global context_data
    data = request.json
    context_data = data.get('context', '')

    # Setup vectorizer with new context
    success = setup_vectorizer(context_data)

    if success:
        return jsonify({
            'status': 'success',
            'message': f'Context added! Split into {len(chunks)} chunks.'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No valid context provided.'
        })


@app.route('/upload_file', methods=['POST'])
def upload_file():
    global context_data

    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})

    # Read text from file
    text = file.read().decode('utf-8')
    context_data = text

    # Setup vectorizer with file content
    success = setup_vectorizer(context_data)

    if success:
        return jsonify({
            'status': 'success',
            'message': f'File uploaded! Split into {len(chunks)} chunks.'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'File is empty or invalid.'
        })


def generate_answer(question, context):
    """Use Ollama LLM to generate a natural answer based on context"""
    try:
        prompt = f"""Based on the following context, please answer the question. If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Answer:"""
        
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        return response['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}. Make sure Ollama is running (run 'ollama serve' in terminal)."


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    query = data.get('question', '')

    if not context_data:
        return jsonify({
            'answer': 'Please add some context first by pasting text or uploading a file.'
        })

    # Find relevant chunks
    relevant_chunks = find_relevant_chunks(query)

    if not relevant_chunks:
        return jsonify({
            'answer': 'I could not find relevant information in the provided context.'
        })

    # Combine relevant chunks for context
    context = "\n\n".join(relevant_chunks[:3])  # Use top 3 chunks
    
    # Generate answer using LLM
    answer = generate_answer(query, context)

    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)