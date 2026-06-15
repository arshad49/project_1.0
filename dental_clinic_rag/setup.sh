#!/bin/bash

echo "🦷 Dental Clinic RAG Bot - Setup"
echo "================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

echo "✅ Python: $(python3 --version)"

# Create venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install deps
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Create .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Edit .env and add your GEMINI_API_KEY"
fi

# Create dirs
mkdir -p media/pdfs staticfiles

# Migrate
echo "🗄️  Running migrations..."
python manage.py migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next:"
echo "1. Edit .env and add GEMINI_API_KEY"
echo "2. python manage.py runserver"
echo "3. Visit: http://localhost:8000"
