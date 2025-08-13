#!/bin/bash

echo "🔧 Fixing Frontend Connection Issue"
echo "=================================="

# Kill any existing backend processes
echo "🛑 Stopping existing backend processes..."
pkill -f "uvicorn.*main" 2>/dev/null || true
pkill -f "python.*main" 2>/dev/null || true
sleep 3

# Check if port 8000 is free
echo "🔍 Checking if port 8000 is available..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Port 8000 is still in use. Killing processes..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start backend with explicit CORS logging
echo "🚀 Starting backend with enhanced CORS support..."
echo "   This will fix the 'Backend Status: Checking...' issue"
echo ""

# Start the backend
python main_enhanced_import.py &
BACKEND_PID=$!

echo "   Backend PID: $BACKEND_PID"
echo "   Waiting for startup..."

# Wait for backend to be ready
for i in {1..15}; do
    sleep 1
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    echo "   Startup check $i/15..."
done

# Verify connection
echo ""
echo "🧪 Testing connection..."
curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null && echo "" || echo "❌ Connection test failed"

echo ""
echo "🌐 Access URLs:"
echo "   📡 Backend API: http://localhost:8000"
echo "   📚 API Documentation: http://localhost:8000/docs"
echo "   🔧 Connection Test: Open test_connection.html"
echo "   🎨 Main Frontend: Open frontend_simple.html"
echo ""
echo "✅ Frontend should now show: Backend Status: ✅ Connected"
echo ""
echo "Press Ctrl+C to stop backend, or press Enter to continue..."
read -r

echo "Backend is running in background (PID: $BACKEND_PID)"
echo "To stop manually: kill $BACKEND_PID"