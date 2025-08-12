#!/bin/bash

# Quick Start Script for Python 3.13
echo "🚀 Quick Start for Agent API Testing Platform"

# Clean npm cache issues
echo "Cleaning npm cache..."
npm cache clean --force 2>/dev/null || echo "npm cache clean skipped"
rm -rf ~/.npm/_cacache 2>/dev/null || echo "npm cache directory clean skipped"

# Backend setup
echo "🔧 Setting up backend..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install fastapi==0.68.0
pip install uvicorn==0.15.0
pip install python-dotenv==1.0.0

# Create .env
if [ ! -f ".env" ]; then
    echo "GITHUB_TOKEN=optional" > .env
    echo "OPENAI_API_KEY=optional" >> .env
fi

echo "✅ Backend ready!"
echo ""
echo "🚀 Starting backend server..."
python main_minimal_clean.py &
BACKEND_PID=$!

echo "Backend started with PID: $BACKEND_PID"
echo ""
echo "🌐 Opening frontend..."

# Try to open the HTML frontend
if command -v open >/dev/null 2>&1; then
    # macOS
    open frontend_simple.html
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open frontend_simple.html
elif command -v start >/dev/null 2>&1; then
    # Windows
    start frontend_simple.html
else
    echo "Manual: Open frontend_simple.html in your browser"
fi

echo ""
echo "📡 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the backend server"

# Wait for interrupt
trap "echo 'Stopping backend...'; kill $BACKEND_PID 2>/dev/null; exit 0" INT
wait $BACKEND_PID