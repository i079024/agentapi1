#!/bin/bash

# Quick Python 3.13 Setup Script

echo "🔧 Python 3.13 Quick Setup..."

# Create fresh virtual environment
echo "Creating fresh virtual environment..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install Python 3.13 compatible packages
echo "Installing Python 3.13 compatible packages..."
pip install fastapi==0.88.0
pip install uvicorn==0.20.0
pip install pydantic==1.9.2
pip install httpx==0.24.1
pip install python-dotenv==1.0.0
pip install openai==0.28.1
pip install requests==2.31.0
pip install gitpython==3.1.40
pip install beautifulsoup4==4.12.2
pip install markdown==3.5.1

# Test imports
echo "Testing imports..."
python -c "import fastapi, uvicorn, pydantic, httpx, openai; print('✅ All packages imported successfully')"

if [ $? -eq 0 ]; then
    echo "✅ Python 3.13 setup complete!"
    echo "Now run: python main.py"
else
    echo "❌ Setup failed. Check errors above."
fi