#!/bin/bash

# YouTube Audio Downloader Backend Setup Script

echo "🚀 Setting up YouTube Audio Downloader Backend..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""
echo "To start the backend server:"
echo "1. cd backend"
echo "2. source venv/bin/activate"
echo "3. python app.py"
echo ""
echo "The backend will be available at: http://localhost:5000"
