#!/bin/bash

echo "🚀 Setting up Complete API Testing Platform with AI Reports"
echo "=========================================================="

# Install all required dependencies
echo "📦 Installing Python dependencies..."
pip install fastapi uvicorn requests python-multipart python-docx

echo ""
echo "✅ Dependencies installed!"
echo ""

# Kill existing processes
echo "🔧 Cleaning up existing processes..."
pkill -f "uvicorn.*main" 2>/dev/null || true
pkill -f "python.*main" 2>/dev/null || true
sleep 2

echo ""
echo "🎯 Features Available:"
echo "  ✅ Enhanced Postman Collection Import"
echo "  ✅ Individual Test Execution" 
echo "  ✅ Batch Test Execution (All Tests)"
echo "  ✅ Collection-based Execution"
echo "  ✅ AI-Powered Word Report Generation"
echo "  ✅ Next API Call Suggestions"
echo "  ✅ Performance & Security Recommendations"
echo ""
echo "📡 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🎨 Frontend: Open frontend_simple.html"
echo ""
echo "🧪 Workflow:"
echo "  1. Import Postman Collection"
echo "  2. Execute All Tests or Execute Collection"
echo "  3. Generate AI Report with recommendations"
echo "  4. Download Word document with insights"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the enhanced backend
python main_enhanced_import.py