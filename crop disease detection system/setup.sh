#!/bin/bash

# Crop Disease Detection System - Setup Script
# This script helps you set up and run the system quickly

echo "============================================================"
echo "CROP DISEASE DETECTION SYSTEM - SETUP"
echo "============================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "✓ Found: $python_version"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt
echo ""

# Verify installation
echo "Verifying installation..."
python -c "import tensorflow; import fastapi; import cv2; print('✓ All core dependencies installed successfully')"
echo ""

# Create directories
echo "Creating necessary directories..."
mkdir -p models
mkdir -p data/train
mkdir -p data/test
echo "✓ Directories created"
echo ""

# Show next steps
echo "============================================================"
echo "SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. If you have training data, place it in: data/train/"
echo "   Each disease class should have its own subdirectory"
echo ""
echo "2. Train the model (optional):"
echo "   python train.py"
echo ""
echo "3. Start the system:"
echo "   python main.py serve          # Start API server"
echo "   OR"
echo "   python main.py frontend       # Open web interface"
echo "   OR"
echo "   python main.py predict -i image.jpg  # Command line prediction"
echo ""
echo "4. View documentation:"
echo "   README.md - Full documentation"
echo "   QUICKSTART.md - Quick start guide"
echo "   ARCHITECTURE.md - System architecture"
echo ""
echo "============================================================"
echo "Need help? Check the README.md file for detailed instructions."
echo "============================================================"
