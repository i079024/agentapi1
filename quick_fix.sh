#!/bin/bash
# Quick fix script for Agent API Testing Platform startup issues

echo "🔧 Agent API Testing Platform - Quick Fix"
echo "========================================="

# Step 1: Check current directory
echo "📁 Current directory: $(pwd)"
echo "📋 Files present:"
ls -la *.py *.html 2>/dev/null || echo "   ⚠️  Some files may be missing"

# Step 2: Install dependencies
echo ""
echo "📦 Installing/updating dependencies..."
pip install --upgrade fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0 typing-extensions

# Step 3: Check for port conflicts
echo ""
echo "🌐 Checking port 8000..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "   ⚠️  Port 8000 is in use"
    echo "   💡 We'll use port 8001 instead"
    PORT=8001
else
    echo "   ✅ Port 8000 is available"
    PORT=8000
fi

# Step 4: Try to start the server
echo ""
echo "🚀 Starting server on port $PORT..."
echo "   Press Ctrl+C to stop"
echo ""

# Try multiple start methods
if command -v uvicorn > /dev/null 2>&1; then
    echo "Method 1: Using uvicorn directly..."
    uvicorn main_minimal:app --host 0.0.0.0 --port $PORT
else
    echo "Method 2: Using python directly..."
    python main_minimal_clean.py
fi