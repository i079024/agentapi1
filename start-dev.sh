#!/bin/bash

# Agent API Testing Platform - Development Startup Script

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

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install -r requirements.txt

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