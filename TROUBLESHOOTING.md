# Troubleshooting Guide for Installation Issues

## Python Version Compatibility Issues

### Python 3.13 Compatibility Problems

**The Issue:** Python 3.13 is very new and has compatibility issues with pydantic-core that cause Rust compilation errors.

**Quick Solution:**
```bash
chmod +x start-py313.sh
./start-py313.sh
```

**Manual Solution:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install compatible versions for Python 3.13
pip install -r requirements-py313.txt
```

**Recommended Python Versions:**
- ✅ **Python 3.11** (Best compatibility)
- ✅ **Python 3.12** (Good compatibility) 
- ⚠️ **Python 3.13** (Limited compatibility, use requirements-py313.txt)
- ❌ **Python 3.14+** (Not yet supported)

### Python Version Switching

If you have multiple Python versions, switch to a compatible one:

**Using pyenv (Recommended):**
```bash
# Install pyenv if not already installed
curl https://pyenv.run | bash

# Install and use Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9

# Verify version
python --version

# Then run normal installation
pip install -r requirements.txt
```

**Using Homebrew (macOS):**
```bash
# Install Python 3.11
brew install python@3.11

# Use specific version
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
```

## Common Backend Issues

### pydantic-core Build Errors (Non-Python 3.13)

**Option 1: Use the Fixed Startup Script**
```bash
chmod +x start-dev-fixed.sh
./start-dev-fixed.sh
```

**Option 2: Manual Installation with Compatible Versions**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install with pre-compiled wheels only
pip install --only-binary=pydantic-core pydantic==2.4.2

# Install alternative requirements
pip install -r requirements-alt.txt
```

**Option 3: Install Build Dependencies (if you have Homebrew)**
```bash
# Install Rust compiler
brew install rust

# Then try standard installation
pip install -r requirements.txt
```

**Option 4: Use Older Compatible Versions**
```bash
pip install fastapi==0.103.0 uvicorn==0.24.0 pydantic==1.10.13 httpx==0.25.2 python-dotenv==1.0.0 openai==1.3.7 requests==2.31.0
```

## Common Frontend Issues

### npm Dependency Conflicts

If you encounter `ERESOLVE` errors with React dependencies:

**Option 1: Use Legacy Peer Deps (Recommended)**
```bash
cd frontend
npm install --legacy-peer-deps
```

**Option 2: Force Resolution**
```bash
cd frontend
npm install --force
```

**Option 3: Clean Installation**
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**Option 4: Use Yarn Instead**
```bash
cd frontend
npm install -g yarn
yarn install
```

### React 18 Compatibility Issues

Some packages may not be fully compatible with React 18. The updated package.json uses React 18 compatible alternatives:
- Replaced `react-json-view` with `@uiw/react-json-view`
- Updated all Material-UI packages to latest versions

## Complete Clean Setup

If you continue to have issues, try a complete clean setup:

```bash
# Remove all generated files
rm -rf venv frontend/node_modules frontend/package-lock.json

# Use the enhanced startup script
chmod +x start-dev-fixed.sh
./start-dev-fixed.sh
```

### If All Else Fails: Docker Alternative

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements-alt.txt .
RUN pip install -r requirements-alt.txt

COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

Run with Docker:
```bash
docker build -t agentapi .
docker run -p 8000:8000 agentapi
```

### Verification

Test your installation:
```bash
python -c "import fastapi, pydantic, uvicorn; print('✅ Installation successful')"
```