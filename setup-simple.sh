#!/bin/bash

# Simplified Setup - Backend Only with HTML Frontend
echo "🚀 Simplified Setup - Backend + HTML Frontend"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Setting up Python 3.13 compatible backend...${NC}"

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
try:
    import fastapi, uvicorn
    print('✅ Backend packages working')
except Exception as e:
    print(f'❌ Backend failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Backend setup failed${NC}"
    exit 1
fi

# Create .env if needed
if [ ! -f ".env" ]; then
    cp config.env.example .env 2>/dev/null || echo "# Add your API keys here" > .env
fi

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}To start:${NC}"
echo "1. Backend: python main_minimal_clean.py"
echo "2. Frontend: open frontend_simple.html in your browser"
echo ""
echo -e "${BLUE}URLs:${NC}"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo "- Frontend: file://$(pwd)/frontend_simple.html"