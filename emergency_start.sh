#!/bin/bash
# Emergency start script for Agent API Testing Platform

echo "🚀 Emergency Start - Agent API Testing Platform"
echo "================================================"

# Navigate to project directory
cd /Users/i079024/ariba/agenticapi_pers/agentapi3

# Check current directory
echo "📁 Current directory: $(pwd)"

# Install dependencies
echo "📦 Installing dependencies..."
pip install fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0

# Kill any existing process on port 8000
echo "🔧 Checking for existing processes..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "⚠️  Killing existing process on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Try multiple start methods
echo "🚀 Attempting to start server..."

# Method 1: Direct uvicorn with main_minimal
echo "Method 1: Direct uvicorn..."
uvicorn main_minimal:app --host 0.0.0.0 --port 8000 --log-level info

# If that fails, try port 8001
if [ $? -ne 0 ]; then
    echo "Method 2: Trying port 8001..."
    uvicorn main_minimal:app --host 0.0.0.0 --port 8001 --log-level info
fi