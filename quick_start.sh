#!/bin/bash

echo "🚀 Quick Start - Agent API Testing Platform"
echo "==========================================="

# Function to check if backend is running
check_backend() {
    echo "🔍 Checking backend status..."
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is already running on port 8000"
        return 0
    else
        echo "❌ Backend is not running"
        return 1
    fi
}

# Function to start backend
start_backend() {
    echo "🚀 Starting backend server..."
    
    # Kill any existing processes
    pkill -f "uvicorn.*main" 2>/dev/null || true
    pkill -f "python.*main" 2>/dev/null || true
    sleep 2
    
    # Check if main_enhanced_import.py exists
    if [ ! -f "main_enhanced_import.py" ]; then
        echo "❌ Error: main_enhanced_import.py not found"
        echo "   Make sure you're in the correct directory"
        exit 1
    fi
    
    # Start the backend in background
    echo "   Starting python main_enhanced_import.py..."
    python3 main_enhanced_import.py &
    BACKEND_PID=$!
    
    # Wait for backend to start
    echo "   Waiting for backend to start..."
    for i in {1..10}; do
        sleep 1
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Backend started successfully (PID: $BACKEND_PID)"
            return 0
        fi
        echo "   Attempt $i/10..."
    done
    
    echo "❌ Backend failed to start within 10 seconds"
    return 1
}

# Main execution
echo ""

# Run diagnostic check
if [ -f "check_backend.py" ]; then
    echo "🔍 Running diagnostics..."
    python check_backend.py
    echo ""
fi

# Check if backend is already running
if check_backend; then
    echo ""
    echo "🎯 Backend is ready!"
else
    echo ""
    echo "🔧 Starting backend..."
    if start_backend; then
        echo ""
        echo "🎯 Backend started successfully!"
    else
        echo ""
        echo "❌ Failed to start backend"
        echo "   Try manually: python main_enhanced_import.py"
        exit 1
    fi
fi

echo ""
echo "🌐 Platform Access:"
echo "   📡 Backend API: http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/docs" 
echo "   🎨 Frontend: Open frontend_simple.html in browser"
echo ""
echo "✨ Features Available:"
echo "   • Enhanced Postman Collection Import"
echo "   • Batch Test Execution"
echo "   • AI-Powered Word Reports"
echo "   • Performance & Security Analysis"
echo ""
echo "Frontend should now show: Backend Status: ✅ running"
echo ""
echo "Press Enter to continue or Ctrl+C to exit..."
read -r

# Keep the script running so backend stays up
echo "🏃 Backend is running in background..."
echo "   PID: $BACKEND_PID"
echo "   To stop: kill $BACKEND_PID"
echo ""
echo "Press Ctrl+C to stop the backend and exit"

# Wait for user interrupt
trap 'echo ""; echo "🛑 Stopping backend..."; kill $BACKEND_PID 2>/dev/null; echo "✅ Backend stopped"; exit 0' INT

# Keep script alive
while true; do
    sleep 1
done