#!/bin/bash

# Agent API Testing Platform - Development Startup Script with Error Handling

echo "🚀 Starting Agent API Testing Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version
get_python_version() {
    python3 --version 2>&1 | sed 's/.* \([0-9]\.[0-9]*\).*/\1/'
}

# Function to fix pydantic installation issues
fix_pydantic_issues() {
    local py_version=$(get_python_version)
    echo -e "${YELLOW}🔧 Attempting to fix pydantic build issues (Python ${py_version})...${NC}"
    
    # Check if this is Python 3.13
    if [[ $py_version == "3.13"* ]]; then
        echo -e "${BLUE}Python 3.13 detected - using compatibility mode...${NC}"
        pip install -r requirements-py313.txt
        return $?
    fi
    
    # Try installing with pre-compiled wheels for other versions
    echo -e "${BLUE}Installing with pre-compiled wheels...${NC}"
    pip install --only-binary=pydantic-core pydantic==2.4.2
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Pre-compiled wheels failed. Trying alternative approach...${NC}"
        
        # Try installing build dependencies
        if command_exists brew; then
            echo -e "${BLUE}Installing build dependencies via Homebrew...${NC}"
            brew install rust
        fi
        
        # Try alternative requirements
        echo -e "${BLUE}Trying alternative requirements...${NC}"
        pip install -r requirements-alt.txt
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to install dependencies. Trying minimal setup...${NC}"
            pip install fastapi==0.88.0 uvicorn==0.20.0 pydantic==1.9.2 httpx==0.24.1 python-dotenv==1.0.0 openai==0.28.1 requests==2.31.0
        fi
    fi
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ Node.js and npm are required but not installed.${NC}"
    exit 1
fi

# Check Python version and warn about compatibility
PY_VERSION=$(get_python_version)
echo -e "${GREEN}✅ Found Python ${PY_VERSION}${NC}"

if [[ $PY_VERSION == "3.13"* ]]; then
    echo -e "${YELLOW}⚠️  Python 3.13 detected. Using compatibility mode...${NC}"
    echo -e "${YELLOW}💡 For best experience, consider using Python 3.11 or 3.12${NC}"
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies with error handling
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install --upgrade pip setuptools wheel

# Check if Python 3.13 and use compatible requirements directly
PY_VERSION=$(get_python_version)
if [[ $PY_VERSION == "3.13"* ]]; then
    echo -e "${YELLOW}Using Python 3.13 compatible requirements...${NC}"
    pip install -r requirements-py313.txt
else
    # Try standard installation first
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Standard installation failed. Attempting fixes...${NC}"
        fix_pydantic_issues
    fi
fi

# Check environment configuration
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp config.env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file with your API keys before running the application.${NC}"
fi

# Install frontend dependencies if not already installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  npm install failed. Trying with --legacy-peer-deps...${NC}"
        npm install --legacy-peer-deps
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}⚠️  Still failing. Cleaning cache and retrying...${NC}"
            npm cache clean --force
            rm -rf node_modules package-lock.json
            npm install --legacy-peer-deps
        fi
    fi
    cd ..
fi

# Function to start backend
start_backend() {
    echo -e "${GREEN}🔧 Starting Backend Server (FastAPI)...${NC}"
    python main.py &
    BACKEND_PID=$!
    echo "Backend PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo -e "${GREEN}🎨 Starting Frontend Development Server (React)...${NC}"
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "Frontend PID: $FRONTEND_PID"
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down services...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Backend stopped${NC}"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Frontend stopped${NC}"
    fi
    deactivate 2>/dev/null
    echo -e "${GREEN}✅ Services stopped successfully${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Test backend dependencies
echo -e "${BLUE}Testing backend dependencies...${NC}"
python -c "import fastapi, uvicorn, pydantic, httpx, openai; print('✅ All backend dependencies imported successfully')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Backend dependency test failed. Please check the installation.${NC}"
    echo -e "${YELLOW}💡 Try running: pip install -r requirements-alt.txt${NC}"
    exit 1
fi

# Start services
echo -e "${GREEN}🚀 Starting services...${NC}"
start_backend
sleep 3  # Give backend time to start
start_frontend

echo -e "${GREEN}✅ Services started successfully!${NC}"
echo -e "${BLUE}📡 Backend API: http://localhost:8000${NC}"
echo -e "${BLUE}📡 API Documentation: http://localhost:8000/docs${NC}"
echo -e "${BLUE}🎨 Frontend: http://localhost:3000${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop all services${NC}"

# Wait for processes
wait