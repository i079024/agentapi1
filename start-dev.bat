@echo off
REM Agent API Testing Platform - Development Startup Script for Windows

echo 🚀 Starting Agent API Testing Platform...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    pause
    exit /b 1
)

REM Check if Node.js is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js and npm are required but not installed.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check environment configuration
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from template...
    copy config.env.example .env
    echo ⚠️  Please edit .env file with your API keys before running the application.
)

REM Install frontend dependencies if not already installed
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    npm install
    if errorlevel 1 (
        echo ⚠️  npm install failed. Trying with --legacy-peer-deps...
        npm install --legacy-peer-deps
        if errorlevel 1 (
            echo ⚠️  Still failing. Cleaning cache and retrying...
            npm cache clean --force
            rmdir /s /q node_modules 2>nul
            del package-lock.json 2>nul
            npm install --legacy-peer-deps
        )
    )
    cd ..
)

echo 🔧 Starting Backend Server...
start "Backend" cmd /k "python main.py"

timeout /t 3 /nobreak >nul

echo 🎨 Starting Frontend Development Server...
cd frontend
start "Frontend" cmd /k "npm start"
cd ..

echo ✅ Services started successfully!
echo 📡 Backend API: http://localhost:8000
echo 📡 API Documentation: http://localhost:8000/docs  
echo 🎨 Frontend: http://localhost:3000
echo 💡 Close the command windows to stop services

pause