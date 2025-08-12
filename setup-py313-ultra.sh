#!/bin/bash

# Python 3.13 Ultra-Compatible Setup
echo "🔧 Python 3.13 Ultra-Compatible Setup..."

# Clean everything
echo "Cleaning previous installations..."
rm -rf venv
rm -rf frontend/node_modules

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install minimal compatible versions
echo "Installing ultra-compatible packages..."
pip install --upgrade pip setuptools wheel

# Install packages one by one with older versions
pip install fastapi==0.88.0
pip install "uvicorn[standard]==0.20.0"
pip install pydantic==1.9.2
pip install httpx==0.24.1
pip install python-dotenv==1.0.0
pip install "openai==0.28.1"
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install markdown==3.5.1

# Install git dependency separately (might not be needed)
pip install gitpython || echo "GitPython failed - continuing without it"

# Test backend
echo "Testing backend imports..."
python -c "
try:
    import fastapi
    import uvicorn  
    import pydantic
    import httpx
    import requests
    print('✅ Core packages imported successfully')
    
    # Test OpenAI import
    try:
        import openai
        print('✅ OpenAI imported successfully')
    except Exception as e:
        print(f'⚠️  OpenAI import issue: {e}')
        
except Exception as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Backend setup complete!"
else
    echo "❌ Backend setup failed"
    exit 1
fi

# Setup frontend
echo "Setting up frontend..."
cd frontend

# Clean npm cache and install
npm cache clean --force
npm install --legacy-peer-deps

if [ $? -eq 0 ]; then
    echo "✅ Frontend setup complete!"
    cd ..
else
    echo "❌ Frontend setup failed"
    cd ..
    exit 1
fi

# Create .env if not exists
if [ ! -f ".env" ]; then
    cp config.env.example .env
    echo "⚠️  Created .env file - please add your API keys"
fi

echo "🎉 Setup complete! You can now run:"
echo "  Backend: python main.py"
echo "  Frontend: cd frontend && npm start"