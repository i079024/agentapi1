#!/bin/bash

# Quick Run Script - Uses the correct clean file
echo "🚀 Agent API Testing Platform - Quick Run"
echo "Using main_minimal_clean.py (syntax error free!)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install --quiet fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0

echo ""
echo "✅ Starting the clean backend server..."
echo "📡 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs" 
echo "🎨 Frontend: Open frontend_simple.html in your browser"
echo ""

# Start the clean server
python main_minimal_clean.py