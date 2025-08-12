#!/bin/bash

# Minimal Python 3.13 Setup - No Complex Dependencies
echo "🔧 Minimal Python 3.13 Setup..."

# Clean everything
rm -rf venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install only the most basic packages
echo "Installing minimal packages..."
pip install --upgrade pip

# Install packages individually with error handling
echo "Installing FastAPI..."
pip install fastapi==0.68.0 || { echo "FastAPI failed"; exit 1; }

echo "Installing Uvicorn..."
pip install uvicorn==0.15.0 || { echo "Uvicorn failed"; exit 1; }

echo "Installing basic dependencies..."
pip install python-dotenv==1.0.0 || echo "dotenv failed - continuing"
pip install requests==2.31.0 || echo "requests failed - continuing"

# Test minimal imports
echo "Testing minimal imports..."
python3 -c "
import sys
print(f'Python version: {sys.version}')

try:
    import fastapi
    print('✅ FastAPI imported')
except Exception as e:
    print(f'❌ FastAPI failed: {e}')
    exit(1)

try:
    import uvicorn
    print('✅ Uvicorn imported')
except Exception as e:
    print(f'❌ Uvicorn failed: {e}')
    exit(1)
    
print('✅ Minimal setup successful')
"

echo "✅ Minimal backend setup complete!"
echo "Run: python main_minimal.py"