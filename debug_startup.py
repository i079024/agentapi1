#!/usr/bin/env python3
"""
Debug script to diagnose startup issues for Agent API Testing Platform
Run this to check dependencies and basic functionality
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 7:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.7+ required")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required_packages = {
        'fastapi': '0.68.0',
        'uvicorn': '0.15.0',
        'python-dotenv': '1.0.0',
        'typing-extensions': '3.7.4'
    }
    
    missing_packages = []
    
    for package, min_version in required_packages.items():
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package} is installed")
        except ImportError:
            print(f"   ❌ {package} is missing")
            missing_packages.append(package)
    
    return missing_packages

def check_port_availability():
    """Check if port 8000 is available"""
    print("\n🔍 Checking port 8000 availability...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("   ⚠️  Port 8000 is already in use")
            print("   💡 Try: lsof -i :8000 to see what's using it")
            return False
        else:
            print("   ✅ Port 8000 is available")
            return True
    except Exception as e:
        print(f"   ❌ Error checking port: {e}")
        return False

def check_main_files():
    """Check if main application files exist"""
    print("\n🔍 Checking application files...")
    import os
    
    files_to_check = [
        'main_minimal.py',
        'main_minimal_clean.py',
        'frontend_simple.html',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"   ✅ {file} exists")
        else:
            print(f"   ❌ {file} is missing")
            all_exist = False
    
    return all_exist

def test_basic_import():
    """Test basic import of the main application"""
    print("\n🔍 Testing application import...")
    try:
        from main_minimal import app
        print("   ✅ Successfully imported main_minimal")
        print(f"   📡 App title: {app.title}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to import main_minimal: {e}")
        return False

def install_missing_packages(missing_packages):
    """Install missing packages"""
    if not missing_packages:
        return True
    
    print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
    try:
        for package in missing_packages:
            if package == 'fastapi':
                cmd = [sys.executable, '-m', 'pip', 'install', 'fastapi==0.68.0']
            elif package == 'uvicorn':
                cmd = [sys.executable, '-m', 'pip', 'install', 'uvicorn==0.15.0']
            elif package == 'python-dotenv':
                cmd = [sys.executable, '-m', 'pip', 'install', 'python-dotenv==1.0.0']
            elif package == 'typing-extensions':
                cmd = [sys.executable, '-m', 'pip', 'install', 'typing-extensions>=3.7.4']
            else:
                cmd = [sys.executable, '-m', 'pip', 'install', package]
            
            print(f"   Installing {package}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {package} installed successfully")
            else:
                print(f"   ❌ Failed to install {package}: {result.stderr}")
                return False
        
        return True
    except Exception as e:
        print(f"   ❌ Installation failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🚀 Agent API Testing Platform - Diagnostic Tool")
    print("=" * 50)
    
    # Run all checks
    python_ok = check_python_version()
    missing_deps = check_dependencies()
    port_ok = check_port_availability()
    files_ok = check_main_files()
    
    # Install missing dependencies if needed
    if missing_deps:
        print(f"\n⚠️  Found {len(missing_deps)} missing dependencies")
        install_ok = install_missing_packages(missing_deps)
        if install_ok:
            print("\n🔍 Re-checking dependencies after installation...")
            missing_deps = check_dependencies()
    
    # Test import after potential installation
    import_ok = test_basic_import()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY:")
    print(f"   Python Version: {'✅' if python_ok else '❌'}")
    print(f"   Dependencies: {'✅' if not missing_deps else '❌'}")
    print(f"   Port 8000: {'✅' if port_ok else '⚠️'}")
    print(f"   App Files: {'✅' if files_ok else '❌'}")
    print(f"   App Import: {'✅' if import_ok else '❌'}")
    
    if python_ok and not missing_deps and files_ok and import_ok:
        print("\n🎉 All checks passed! Try running the server:")
        print("   python main_minimal_clean.py")
        if not port_ok:
            print("   (or use: uvicorn main_minimal_clean:app --port 8001)")
    else:
        print("\n❌ Some issues found. Please fix the above problems and try again.")
        
        if not python_ok:
            print("   💡 Install Python 3.7+ from https://python.org")
        if missing_deps:
            print("   💡 Run: pip install fastapi uvicorn python-dotenv typing-extensions")
        if not files_ok:
            print("   💡 Ensure you're in the correct directory with all project files")
        if not import_ok:
            print("   💡 Check main_minimal.py for syntax errors")

if __name__ == "__main__":
    main()