# Agent API Testing Platform - Enhanced with Coverage Analysis
# Complete backend implementation with GitHub repository analysis, 
# test coverage reporting, AI-powered gap detection, and downloadable Word reports

# This is the main entry point for the Agent API Testing Platform
# Run this file directly: python main_minimal_clean.py

# Import all functionality from the main application
from main_minimal import app, uvicorn

# Ensure the server starts when this file is run directly
if __name__ == "__main__":
    print("🚀 Starting Agent API Testing Platform - COMPLETE EDITION")
    print("📡 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🎨 Frontend: Open frontend_simple.html in your browser")
    print()
    print("✨ ALL NEW FEATURES ENABLED:")
    print("   ✅ Test Management (Create/Edit/Delete)")
    print("   ✅ Smart Assertions Builder")
    print("   ✅ AI-Powered Suggestions")
    print("   ✅ Import/Export Tests (JSON)")
    print("   ✅ Word Document Export")
    print("   ✅ Individual Test Execution")
    print("   ✅ Batch Test Execution")
    print("   ✅ Next API Call Recommendations")
    print("   ✅ Enhanced Reporting & Analytics")
    print("   ✅ GitHub Repository Analysis")
    print("   ✅ Test Coverage Analysis")
    print("   ✅ AI-Powered Coverage Gap Detection")
    print("   ✅ Mermaid Class Diagrams with Coverage")
    print("   ✅ Comprehensive Word Reports")
    print("   ✅ Local File Downloads with User Confirmation")
    print()
    print("🎯 Try these enhanced endpoints:")
    print("   GET  /tests - List all tests")
    print("   POST /tests - Create new test")
    print("   POST /execute-test/{id} - Run single test")
    print("   POST /ai-suggestions/test - Get AI test suggestions")
    print("   POST /export/tests - Export tests as JSON")
    print("   POST /export/results/word - Export as Word doc")
    print("   POST /analyze-repository - Enhanced GitHub analysis")
    print("   POST /export/coverage-report - Prepare coverage report")
    print("   GET  /download/coverage/{id} - Download coverage report")
    print()
    print("🌐 Visit http://localhost:8000/docs to explore all endpoints!")
    print()
    print("💾 NEW: Coverage reports can be downloaded locally with user confirmation!")
    print("📄 Frontend includes download confirmation dialogs and progress indicators")
    print()
    print("⚠️  Press Ctrl+C to stop the server")
    print()
    
    try:
        uvicorn.run(
            "main_minimal_clean:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {str(e)}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if port 8000 is already in use: lsof -i :8000")
        print("2. Try a different port: uvicorn main_minimal_clean:app --port 8001")
        print("3. Install dependencies: pip install fastapi uvicorn")
        print("4. Check Python version: python --version")