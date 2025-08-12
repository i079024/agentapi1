#!/bin/bash

echo "🚀 Quick Start - Agent API Testing Platform"
echo "============================================="

# Navigate to project directory
cd /Users/i079024/ariba/agenticapi_pers/agentapi3

# Check dependencies
echo "📦 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "📦 Installing dependencies..."
    pip install fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0
}

# Kill any existing processes
echo "🔧 Cleaning up existing processes..."
pkill -f "uvicorn.*main_minimal" 2>/dev/null || true
pkill -f "python.*main_minimal" 2>/dev/null || true

# Wait a moment for cleanup
sleep 2

# Check which ports are available
echo "🌐 Checking available ports..."
PORT=8000
if lsof -i :8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 in use, trying 8001..."
    PORT=8001
    if lsof -i :8001 > /dev/null 2>&1; then
        echo "⚠️  Port 8001 in use, trying 8002..."
        PORT=8002
    fi
fi

echo "🚀 Starting backend on port $PORT..."
echo ""
echo "📡 Backend will be available at: http://localhost:$PORT"
echo "📚 API Documentation: http://localhost:$PORT/docs"
echo "🎨 Frontend: Open frontend_simple.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
if [ "$PORT" = "8000" ]; then
    python main_minimal_clean.py
else
    uvicorn main_minimal:app --host 0.0.0.0 --port $PORT
fi