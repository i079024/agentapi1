#!/bin/bash

echo "🚀 Starting Agent API Testing Platform..."
echo "📡 Starting backend server..."
echo "📚 API Documentation will be available at: http://localhost:8000/docs"
echo "🎨 Open frontend_simple.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "📦 Installing required dependencies..."
    pip install fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0 typing-extensions
}

# Check if port 8000 is available
echo "🌐 Checking port availability..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 is in use, trying port 8001..."
    echo "🚀 Starting server on port 8001..."
    uvicorn main_minimal:app --host 0.0.0.0 --port 8001
else
    echo "✅ Port 8000 is available"
    echo "🚀 Starting server on port 8000..."
    # Start the server using uvicorn directly (more reliable than python main_minimal_clean.py)
    uvicorn main_minimal:app --host 0.0.0.0 --port 8000
fi