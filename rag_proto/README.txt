RAG BOT - SIMPLE PROTOTYPE
===========================

What is this?
This is a very simple chatbot that can answer questions based on information you give it.
Think of it like a student who reads some notes, then answers questions using only those notes.

How it works:
1. You give the bot some text (context) by uploading a file or pasting text
2. The bot remembers this information 
3. When you ask a question, the bot finds the relevant part of your text
4. An AI (Llama 3.2) reads the relevant parts and generates a natural answer

IMPORTANT - SETUP OLLAMA FIRST:
This bot uses Ollama (free AI) to generate answers. You need to:

OPTION 1 - Download from website (Easiest):
1. Visit: https://ollama.com
2. Click "Download" for Mac
3. Install and open Ollama
4. It will start automatically!

OPTION 2 - Use Homebrew (if installed):
1. Run: brew install ollama
2. Start it: ollama serve

The model (llama3.2) will download automatically when you first ask a question.
This might take a few minutes on first use (about 2GB download).

Files in this project:
- app.py: The main program that runs the chatbot
- templates/index.html: The web page where you interact with the bot
- requirements.txt: List of tools needed to run the program

How to use:
1. Install requirements: pip install -r requirements.txt
2. Check Ollama setup: bash setup.sh (this will guide you)
3. Run the program: python3 app.py
4. Open your browser and go to: http://localhost:5000
5. Paste some text or upload a file with information
6. Ask questions about that information!

Example:
- Paste: "The capital of France is Paris. The Eiffel Tower is in Paris."
- Ask: "What is the capital of France?"
- Bot answers: "The capital of France is Paris." (generated naturally by AI)

This is a learning prototype - simple and easy to understand!