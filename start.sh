#!/bin/bash

# Agent API Testing Platform - Start Script
# Quick start script for the platform

echo "🚀 Starting Agent API Testing Platform..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "📡 Starting backend server..."
echo "📚 API Documentation will be available at: http://localhost:8000/docs"
echo "🎨 Open frontend_simple.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 main_minimal_clean.py