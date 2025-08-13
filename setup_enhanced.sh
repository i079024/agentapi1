#!/bin/bash

echo "🔧 Setting up Enhanced API Testing Platform"
echo "==========================================="

# Install required dependencies
echo "📦 Installing Python dependencies..."
pip install fastapi uvicorn requests python-multipart

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "🚀 Starting Enhanced Backend with Test Execution..."
echo ""
echo "📡 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🎨 Frontend: Open frontend_simple.html"
echo ""
echo "✨ New Features:"
echo "  ✅ Test Execution (/execute-test/{id})"
echo "  ✅ Test Update (/tests/{id} PUT)"
echo "  ✅ Test Export (/export/tests)"
echo "  ✅ Enhanced Postman Import"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Kill existing processes
pkill -f "uvicorn.*main" 2>/dev/null || true
pkill -f "python.*main" 2>/dev/null || true
sleep 2

# Start the enhanced backend
python main_enhanced_import.py