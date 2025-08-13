#!/bin/bash

echo "🚀 Testing Enhanced Import Functionality"
echo "======================================="

# Kill any existing processes
echo "🔧 Cleaning up existing processes..."
pkill -f "uvicorn.*main" 2>/dev/null || true
pkill -f "python.*main" 2>/dev/null || true

# Wait for cleanup
sleep 2

echo "📦 Creating test import files..."
python create_test_imports.py

echo "🚀 Starting enhanced backend..."
echo "Port: 8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: Open frontend_simple.html"
echo ""
echo "🧪 Test import with the following files:"
echo "  - test_import_1.json (Simple Array - 2 tests)"
echo "  - test_import_2.json (Export Format - 2 tests)"  
echo "  - test_import_3.json (Postman Collection - 2 tests)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the enhanced backend
python main_enhanced.py

echo "🚀 Testing Enhanced Import for Postman Collections"
echo "================================================="

# Kill existing processes
pkill -f "uvicorn.*main" 2>/dev/null || true
pkill -f "python.*main" 2>/dev/null || true
sleep 2

echo "🎯 Starting Enhanced Backend..."
echo ""
echo "✅ Fixed Issues:"
echo "  - Proper Postman collection parsing" 
echo "  - Correct test naming (no more 'Imported Test 1' repetition)"
echo "  - Endpoint extraction from Postman URL objects"
echo "  - Better error handling and debugging"
echo ""
echo "📡 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🎨 Frontend: Open frontend_simple.html"
echo ""
echo "🧪 To test:"
echo "  1. Export a Postman collection as JSON"
echo "  2. Use 'Import Tests' in frontend"
echo "  3. Check that all tests show proper names and endpoints"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start enhanced backend
python main_enhanced_import.py