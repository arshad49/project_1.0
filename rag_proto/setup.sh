#!/bin/bash

echo "🤖 RAG Bot - Ollama Setup Checker"
echo "=================================="
echo ""

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed!"
    echo ""
    
    # Check if Ollama is running
    if curl -s http://localhost:11434 &> /dev/null; then
        echo "✅ Ollama is running!"
        echo ""
        
        # Check if llama3.2 model is downloaded
        if ollama list | grep -q "llama3.2"; then
            echo "✅ Llama3.2 model is ready!"
            echo ""
            echo "🎉 Everything is set up! You can now:"
            echo "   Run: python3 app.py"
            echo "   Then open: http://localhost:5000"
        else
            echo "⚠️  Llama3.2 model not found."
            echo ""
            echo "Downloading Llama3.2 model (about 2GB, takes a few minutes)..."
            echo "This only happens once!"
            ollama pull llama3.2
            echo ""
            echo "✅ Model downloaded! You can now:"
            echo "   Run: python3 app.py"
        fi
    else
        echo "❌ Ollama is installed but not running."
        echo ""
        echo "Please start Ollama:"
        echo "   1. Open the Ollama app from Applications"
        echo "   OR"
        echo "   2. Run: ollama serve"
        echo ""
        echo "Then run this script again."
    fi
else
    echo "❌ Ollama is not installed."
    echo ""
    echo "To install Ollama (FREE):"
    echo ""
    echo "OPTION 1 - Website (Easiest):"
    echo "   1. Visit: https://ollama.com"
    echo "   2. Click Download for Mac"
    echo "   3. Install and open it"
    echo ""
    echo "OPTION 2 - Homebrew:"
    echo "   Run: brew install ollama"
    echo ""
    echo "After installing, run this script again."
fi
