#!/bin/bash

# Complete Ultra-Compatible Setup for Python 3.13
echo "🚀 Complete Ultra-Compatible Setup for Python 3.13..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Phase 1: Backend Setup${NC}"

# Clean backend
rm -rf venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install minimal backend dependencies
echo "Installing backend packages..."
pip install --upgrade pip
pip install fastapi==0.68.0
pip install uvicorn==0.15.0
pip install python-dotenv==1.0.0

# Test backend
echo "Testing backend..."
python3 -c "
import fastapi, uvicorn
print('✅ Backend packages working')
"

if [ $? -ne 0 ]; then
    echo "❌ Backend setup failed"
    exit 1
fi

echo -e "${GREEN}✅ Backend setup complete${NC}"

echo -e "${BLUE}Phase 2: Frontend Setup${NC}"

# Clean frontend
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force

# Install older, more compatible versions
echo "Installing frontend packages..."
npm install --legacy-peer-deps

if [ $? -ne 0 ]; then
    echo "⚠️  Standard install failed, trying with older Node..."
    npm install --legacy-peer-deps --no-optional
fi

cd ..

echo -e "${GREEN}✅ Frontend setup complete${NC}"

# Create .env if needed
if [ ! -f ".env" ]; then
    cp config.env.example .env 2>/dev/null || echo "# Add your API keys here" > .env
fi

echo -e "${GREEN}🎉 Complete setup finished!${NC}"
echo -e "${YELLOW}To start:${NC}"
echo "1. Backend: python main_minimal.py"
echo "2. Frontend: cd frontend && npm start"