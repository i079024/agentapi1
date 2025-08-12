# UI Connection Troubleshooting Guide

## 🔧 **UI Stuck at "Backend Status: Checking" - SOLUTIONS**

### **Quick Fixes:**

**1. Start Backend First:**
```bash
# Make sure backend is running
python main_minimal_clean.py

# You should see:
# 🚀 Starting Agent API Testing Platform - COMPLETE EDITION
# 📡 Backend API: http://localhost:8000
```

**2. Check Backend URL:**
- Backend should be at: http://localhost:8000
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

**3. Test Backend Manually:**
```bash
# Test in terminal
curl http://localhost:8000/health

# Should return JSON with status: "healthy"
```

**4. Browser Console Check:**
```bash
# Open browser console (F12)
# Look for errors like:
# - CORS errors
# - Network errors
# - Connection refused
```

### **Common Issues & Solutions:**

**Issue 1: Port 8000 in use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Or use different port in main_minimal_clean.py:
uvicorn.run("main_minimal_clean:app", port=8001)
```

**Issue 2: CORS Errors**
- Already fixed in main_minimal_clean.py
- CORS middleware allows all origins

**Issue 3: Firewall/Network**
```bash
# Check if localhost works
ping localhost

# Try IP instead of localhost
# Edit frontend_simple.html:
# const API_BASE = 'http://127.0.0.1:8000';
```

**Issue 4: File Path Issues**
```bash
# Make sure you're in correct directory
cd /Users/i079024/ariba/agenticapi_pers/agentapi3

# Files should exist:
ls -la main_minimal_clean.py
ls -la frontend_simple.html
```

### **Complete Restart Process:**

**Step 1: Stop Everything**
```bash
# Kill any python processes
pkill -f python
# Or Ctrl+C in terminal where backend is running
```

**Step 2: Start Backend**
```bash
cd /Users/i079024/ariba/agenticapi_pers/agentapi3
python main_minimal_clean.py

# Wait for:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Step 3: Test Backend**
```bash
# In new terminal
curl http://localhost:8000/health
```

**Step 4: Open Frontend**
```bash
open frontend_simple.html
# OR double-click the file
```

### **If Still Stuck:**

**Check browser console (F12) for errors and report:**
- Network errors
- CORS errors  
- JavaScript errors
- Connection timeouts

The enhanced frontend now has:
- ✅ Connection timeout (10 seconds)
- ✅ Automatic retry every 30 seconds
- ✅ Detailed error messages
- ✅ Manual retry button
- ✅ Console logging for debugging