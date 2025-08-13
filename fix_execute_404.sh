#!/bin/bash

echo "🔧 Fixing 404 Error for /execute-test/ endpoint"
echo "=============================================="

# Kill existing processes  
pkill -f "uvicorn.*main" 2>/dev/null || true
pkill -f "python.*main" 2>/dev/null || true
sleep 2

echo "✅ Added Missing Endpoints:"
echo "  - POST /execute-test/{test_id}"
echo "  - PUT /tests/{test_id}" 
echo "  - POST /export/tests"
echo ""

echo "🚀 Starting Backend with Execute Test Support..."
echo ""
echo "📡 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🎨 Frontend: Open frontend_simple.html"
echo ""
echo "🧪 Test the Execute button:"
echo "  1. Import some tests"
echo "  2. Click 'Execute' button on any test"
echo "  3. Should see execution results (simulated)"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start backend with execute support
python main_minimal_clean.py