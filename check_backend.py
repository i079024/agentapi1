#!/usr/bin/env python3

"""
Backend Status Checker
Diagnoses backend connection issues
"""

import requests
import sys
import time

def check_backend_status():
    """Check if backend is running and responsive"""
    backend_url = "http://localhost:8000"
    
    print("🔍 Backend Status Checker")
    print("=" * 30)
    
    # Check basic connectivity
    try:
        print(f"📡 Checking connectivity to {backend_url}...")
        response = requests.get(f"{backend_url}/health", timeout=5)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Backend is ONLINE and healthy!")
            print(f"   Version: {health_data.get('version', 'Unknown')}")
            print(f"   Message: {health_data.get('message', 'N/A')}")
            print(f"   Tests stored: {health_data.get('stored_tests', 0)}")
            
            # Check additional endpoints
            endpoints_to_check = [
                "/tests",
                "/status", 
                "/docs"
            ]
            
            print("\n🔗 Checking additional endpoints:")
            for endpoint in endpoints_to_check:
                try:
                    resp = requests.get(f"{backend_url}{endpoint}", timeout=3)
                    status = "✅ OK" if resp.status_code < 400 else f"❌ {resp.status_code}"
                    print(f"   {endpoint}: {status}")
                except Exception as e:
                    print(f"   {endpoint}: ❌ Error - {str(e)}")
            
            return True
            
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend is OFFLINE - Connection refused")
        print("\n🔧 To start the backend:")
        print("   1. Open terminal in project directory")
        print("   2. Run: python main_enhanced_import.py")
        print("   3. Wait for 'Uvicorn running on http://0.0.0.0:8000'")
        print("   4. Try this checker again")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Backend is not responding (timeout)")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking Python dependencies:")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "requests",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Main diagnostic function"""
    print("🚀 Agent API Testing Platform - Backend Diagnostics")
    print("=" * 60)
    
    # Check dependencies first
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    # Check backend status
    backend_ok = check_backend_status()
    
    if backend_ok:
        print("\n🎉 All systems operational!")
        print("   Frontend should show: Backend Status: ✅ running")
    else:
        print("\n🔧 Backend needs to be started")
        print("   Frontend will show: Backend Status: ❌ Offline")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()