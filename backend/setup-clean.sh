#!/bin/bash
# Clean installation script for EC2

echo "🧹 Setting up clean Python environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Remove any problematic packages
pip uninstall pathlib2 -y 2>/dev/null || true

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Clean installation complete!"
echo ""
echo "To activate the environment:"
echo "source venv/bin/activate"
