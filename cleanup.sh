#!/bin/bash

# Agent API Testing Platform - Cleanup Script
# This script removes temporary files and caches

echo "🧹 Cleaning up Agent API Testing Platform..."

# Remove Python cache files
echo "Removing Python cache files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Remove temporary files
echo "Removing temporary files..."
find . -name "*.tmp" -delete
find . -name "*.log" -delete
find . -name ".DS_Store" -delete

# Remove virtual environment if exists
if [ -d "venv" ]; then
    echo "Removing virtual environment..."
    rm -rf venv
fi

if [ -d "env" ]; then
    echo "Removing virtual environment..."
    rm -rf env
fi

# List remaining files
echo ""
echo "✅ Cleanup complete! Remaining files:"
ls -la

echo ""
echo "🚀 To start the platform:"
echo "1. pip install -r requirements.txt"
echo "2. python main_minimal_clean.py"
echo "3. open frontend_simple.html"