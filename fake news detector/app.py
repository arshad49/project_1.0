from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyB11IkIBm-Eg_B9y6UuoOH7hSY7oGsNYv0")
def analyze_news(text):
    try:
        prompt = f"""
        You are an expert in detecting fake news.
        Read the following news headline or text and explain in a few sentences:
        - Is it True, Fake, or Misleading?
        - Why you think so

        News text: {text}
        """
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            return "No response from AI."
    except Exception as e:
        print("❌ Error in analyze_news:", e)
        return f"Error analyzing news: {e}"

# Serve main page
@app.route('/')
def home():
    return send_file('index.html')

# Serve CSS & JS
@app.route('/<path:filename>')
def static_files(filename):
    return send_file(filename)

# API route
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    print("📩 Received:", data)

    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    result = analyze_news(text)
    print("✅ Result:", result)

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
