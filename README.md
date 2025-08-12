# Agent API Testing Platform

> A comprehensive, AI-powered API testing platform that enables developers to generate, manage, and execute API tests with intelligent suggestions and automation capabilities.

## 📋 **Table of Contents**

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Frontend Components](#frontend-components)
- [Dependencies](#dependencies)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## 🎯 **Overview**

The Agent API Testing Platform is a modern, full-stack application designed to streamline API testing workflows. It combines traditional test management capabilities with AI-powered insights, making it easier for developers and QA teams to create comprehensive test suites.

### **Key Capabilities:**
- **AI-Driven Test Generation** - Automatically generate tests from GitHub repositories
- **Smart Test Management** - Full CRUD operations with intelligent suggestions
- **Postman Integration** - Import and convert Postman collections seamlessly
- **Professional Reporting** - Export detailed test reports in multiple formats
- **Real-time Execution** - Execute tests individually or in batches with live results

## 🏗️ **Architecture**

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React-like HTML/JS Frontend]
        B[Tab-based Navigation]
        C[Real-time Status Updates]
        D[File Import/Export]
    end
    
    subgraph "Backend Layer"
        E[FastAPI Server]
        F[RESTful API Endpoints]
        G[CORS Middleware]
        H[Request Validation]
    end
    
    subgraph "Core Services"
        I[Test Management Service]
        J[AI Suggestion Engine]
        K[Import/Export Service]
        L[Execution Engine]
    end
    
    subgraph "Data Layer"
        M[In-Memory Storage]
        N[Test Results Cache]
        O[Configuration Store]
    end
    
    subgraph "External Integrations"
        P[GitHub API]
        Q[Postman Collections]
        R[Word Document Export]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> M
    
    J --> P
    K --> Q
    L --> R
```

### **Component Architecture:**

```mermaid
classDiagram
    class AgentAPITestingPlatform {
        +FastAPI app
        +CORSMiddleware middleware
        +InMemoryStorage storage
        +initialize()
        +start_server()
    }
    
    class TestManagementService {
        +Dict stored_tests
        +create_test(test_data)
        +get_test(test_id)
        +update_test(test_id, data)
        +delete_test(test_id)
        +list_tests()
    }
    
    class AIService {
        +get_test_suggestions(endpoint, method)
        +get_assertion_suggestions(endpoint, method)
        +get_next_call_suggestions(endpoint, response)
        +analyze_repository(github_url, branch)
    }
    
    class ImportExportService {
        +import_tests(test_data)
        +export_tests(test_ids, format)
        +convert_postman_collection(collection_data)
        +export_word_document(test_ids)
    }
    
    class ExecutionService {
        +execute_single_test(test_id)
        +execute_batch_tests(test_ids)
        +validate_assertions(response, assertions)
        +generate_execution_report(results)
    }
    
    class TestModel {
        +String id
        +String name
        +String method
        +String endpoint
        +Dict headers
        +Object body
        +List assertions
        +String description
        +DateTime created_at
        +DateTime updated_at
        +List tags
        +String collection
        +Boolean ai_generated
        +Float confidence
        +String source
    }
    
    class FrontendController {
        +TabManager tab_manager
        +APIClient api_client
        +UIComponents components
        +manage_tests()
        +handle_imports()
        +display_results()
    }
    
    AgentAPITestingPlatform --> TestManagementService
    AgentAPITestingPlatform --> AIService
    AgentAPITestingPlatform --> ImportExportService
    AgentAPITestingPlatform --> ExecutionService
    
    TestManagementService --> TestModel
    AIService --> TestModel
    ImportExportService --> TestModel
    ExecutionService --> TestModel
    
    FrontendController --> AgentAPITestingPlatform
```

## ✨ **Features**

### **Core Testing Features:**
- 🧪 **Complete Test Lifecycle Management** - Create, edit, delete, and duplicate tests
- 🔄 **Batch Test Execution** - Run multiple tests simultaneously with parallel processing
- 📊 **Real-time Results** - Live execution status and detailed reporting
- 🎯 **Smart Assertions** - Multiple assertion types (status code, response time, JSON path, headers)

### **AI-Powered Capabilities:**
- 🤖 **Intelligent Test Generation** - AI suggests tests based on endpoint patterns
- 🧠 **Smart Assertion Recommendations** - Context-aware assertion suggestions
- 🔮 **Next API Call Predictions** - Suggests logical follow-up endpoint calls
- 📈 **Confidence Scoring** - AI confidence ratings for suggestions

### **Integration Features:**
- 📂 **Postman Collection Import** - Full v2.1 support with automatic conversion
- 🌐 **GitHub Repository Analysis** - Analyze repos to generate API tests
- � **Professional Reporting** - Export to Word documents with charts and analysis
- 💾 **JSON Import/Export** - Standard format for test sharing and backup

### **User Experience:**
- 🎨 **Modern Tab-based Interface** - Intuitive navigation between features
- 🔧 **In-line Test Editing** - Edit tests directly in the management interface
- ⚡ **Real-time Backend Status** - Live connection monitoring with auto-retry
- � **Responsive Design** - Works on desktop and mobile devices

## � **Project Structure**

```
agent-api-testing-platform/
├── 📄 main_minimal_clean.py          # Main FastAPI backend server
├── 🌐 frontend_simple.html           # Complete frontend interface
├── 📋 requirements.txt               # Python dependencies
├── 📝 README.md                      # Project documentation
├── 🔧 UI_TROUBLESHOOTING.md          # Troubleshooting guide
├── 🧹 cleanup.sh                     # Cleanup script for temp files
├── 🚀 start.sh                       # Quick start script
└── ⚙️ setup.sh                       # Setup and initialization script
```

### **File Descriptions:**

| File | Description | Size | Purpose |
|------|-------------|------|---------|
| `main_minimal_clean.py` | FastAPI backend server with all endpoints | ~700 lines | Core application server |
| `frontend_simple.html` | Complete HTML/CSS/JS frontend | ~600 lines | User interface |
| `requirements.txt` | Python package dependencies | 4 packages | Dependency management |
| `UI_TROUBLESHOOTING.md` | Connection troubleshooting guide | ~100 lines | User support |
| `cleanup.sh` | Cleanup script for temporary files | ~30 lines | Maintenance |
| `start.sh` | Quick start script | ~25 lines | Convenience |

## 🛠 **Installation**

### **Prerequisites:**
- **Python 3.7+** (Tested with Python 3.13)
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Internet Connection** (for AI features and GitHub analysis)

### **Step 1: Clone/Download Project**
```bash
# If using git
git clone <repository-url>
cd agent-api-testing-platform

# Or extract from ZIP
unzip agent-api-testing-platform.zip
cd agent-api-testing-platform
```

### **Step 2: Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Or install manually
pip install fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0 typing-extensions>=3.7.4
```

### **Step 3: Make Scripts Executable (Linux/Mac)**
```bash
chmod +x cleanup.sh
chmod +x start.sh
chmod +x setup.sh
```

## 🚀 **Running the Project**

### **Method 1: Quick Start (Recommended)**
```bash
# One-command start
./start.sh
```

### **Method 2: Manual Start**
```bash
# Start backend server
python main_minimal_clean.py

# In another terminal or browser, open frontend
open frontend_simple.html
# Or double-click the HTML file
```

### **Method 3: Development Mode**
```bash
# Start with auto-reload for development
uvicorn main_minimal_clean:app --reload --host 0.0.0.0 --port 8000
```

### **Expected Output:**
```
🚀 Starting Agent API Testing Platform - COMPLETE EDITION
📡 Backend API: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
🎨 Frontend: Open frontend_simple.html in your browser

✨ ALL NEW FEATURES ENABLED:
   ✅ Test Management (Create/Edit/Delete)
   ✅ Smart Assertions Builder
   ✅ AI-Powered Suggestions
   ✅ Import/Export Tests (JSON)
   ✅ Word Document Export
   ✅ Individual Test Execution
   ✅ Batch Test Execution
   ✅ Next API Call Recommendations
   ✅ Enhanced Reporting & Analytics

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 📚 **API Documentation**

### **Health & Status Endpoints**

#### `GET /health`
**Description:** Health check endpoint to verify server status  
**Parameters:** None  
**Response:**
```json
{
  "status": "healthy",
  "message": "Agent API Testing Platform with Complete Features",
  "python_compatible": true,
  "features": [
    "GitHub Repository Analysis",
    "AI Test Generation",
    "Test Management (CRUD)",
    "Smart Assertions",
    "Import/Export",
    "Word Document Export",
    "AI Suggestions",
    "Batch Execution"
  ]
}
```

#### `GET /`
**Description:** Root endpoint with platform information  
**Parameters:** None  
**Response:** Platform overview with available endpoints and features

### **Test Management Endpoints**

#### `GET /tests`
**Description:** Retrieve all stored tests  
**Parameters:** None  
**Response:**
```json
{
  "status": "success",
  "tests": [
    {
      "id": "uuid-string",
      "name": "Test Name",
      "method": "GET",
      "endpoint": "https://api.example.com/users",
      "headers": {"Content-Type": "application/json"},
      "body": null,
      "assertions": [
        {"type": "status_code", "expected": 200},
        {"type": "response_time", "max_ms": 2000}
      ],
      "description": "Test description",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00",
      "tags": ["api", "test"],
      "collection": "default",
      "ai_generated": false,
      "confidence": 0.5,
      "source": "manual"
    }
  ],
  "total": 1,
  "message": "All tests retrieved successfully"
}
```

#### `POST /tests`
**Description:** Create a new test  
**Parameters:**
```json
{
  "name": "string (required)",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "endpoint": "string (required)",
  "headers": {"key": "value"},
  "body": "object|null",
  "assertions": [
    {"type": "status_code", "expected": 200}
  ],
  "description": "string",
  "tags": ["string"],
  "collection": "string"
}
```
**Response:** Created test object with generated ID and timestamps

#### `GET /tests/{test_id}`
**Description:** Retrieve a specific test by ID  
**Parameters:**
- `test_id` (path): UUID of the test  
**Response:** Single test object or 404 error

#### `PUT /tests/{test_id}`
**Description:** Update an existing test  
**Parameters:**
- `test_id` (path): UUID of the test
- Body: Same as POST /tests (all fields optional)  
**Response:** Updated test object

#### `DELETE /tests/{test_id}`
**Description:** Delete a test by ID  
**Parameters:**
- `test_id` (path): UUID of the test  
**Response:**
```json
{
  "status": "success",
  "message": "Test 'Test Name' deleted successfully",
  "deleted_test": {...}
}
```

### **Test Execution Endpoints**

#### `POST /execute-test/{test_id}`
**Description:** Execute a single test  
**Parameters:**
- `test_id` (path): UUID of the test  
**Response:**
```json
{
  "status": "success",
  "execution": {
    "test_id": "uuid",
    "test_name": "Test Name",
    "success": true,
    "execution_time": 0.15,
    "timestamp": "2024-01-01T12:00:00",
    "response": {
      "status_code": 200,
      "body": {"message": "Response data"},
      "headers": {"content-type": "application/json"}
    }
  }
}
```

#### `POST /execute-batch`
**Description:** Execute multiple tests in batch  
**Parameters:**
```json
{
  "test_ids": ["uuid1", "uuid2"],
  "concurrent": false
}
```
**Response:**
```json
{
  "status": "success",
  "batch_execution": {
    "summary": {
      "total_tests": 2,
      "passed": 2,
      "failed": 0,
      "execution_time": 0.3,
      "success_rate": 100.0
    },
    "results": [...],
    "executed_at": "2024-01-01T12:00:00",
    "concurrent_execution": false
  }
}
```

#### `POST /execute-tests`
**Description:** Execute generated tests from analysis  
**Parameters:**
```json
{
  "generated_tests": [...]
}
```
**Response:** Execution summary with test results

### **AI Suggestion Endpoints**

#### `POST /ai-suggestions/test`
**Description:** Get AI-generated test suggestions  
**Parameters:**
```json
{
  "endpoint": "/api/users",
  "method": "GET",
  "context": "User management API"
}
```
**Response:**
```json
{
  "status": "success",
  "suggestions": [
    {
      "name": "Test GET /api/users - Happy Path",
      "description": "Test successful GET request to /api/users",
      "method": "GET",
      "endpoint": "/api/users",
      "headers": {"Content-Type": "application/json"},
      "body": null,
      "assertions": [...],
      "priority": "high",
      "confidence": 0.9
    }
  ],
  "context": "User management API",
  "ai_confidence": 0.85,
  "total_suggestions": 1
}
```

#### `POST /ai-suggestions/assertions`
**Description:** Get AI-suggested assertions for an endpoint  
**Parameters:**
```json
{
  "endpoint": "/api/users",
  "method": "GET"
}
```
**Response:**
```json
{
  "status": "success",
  "assertion_suggestions": [
    {
      "type": "status_code",
      "description": "Verify HTTP status code",
      "config": {"expected": 200},
      "confidence": 0.95,
      "reasoning": "Standard success response"
    }
  ],
  "endpoint": "/api/users",
  "method": "GET"
}
```

#### `POST /ai-suggestions/next-calls`
**Description:** Get suggestions for next API calls  
**Parameters:**
```json
{
  "endpoint": "/api/users",
  "method": "GET",
  "response": {...}
}
```
**Response:**
```json
{
  "status": "success",
  "next_call_suggestions": [
    {
      "endpoint": "/api/users/details",
      "method": "GET",
      "description": "Get detailed information",
      "reasoning": "Common pattern to fetch details after list operation",
      "confidence": 0.8,
      "parameters": {"id": "from_previous_response"}
    }
  ],
  "based_on": {
    "endpoint": "/api/users",
    "method": "GET",
    "response_analysis": "Analyzed response patterns"
  }
}
```

### **Import/Export Endpoints**

#### `POST /import/tests`
**Description:** Import tests from JSON or Postman collections  
**Parameters:**
```json
{
  "tests": "array|object|postman_collection"
}
```
**Supported Formats:**
- JSON array of test objects
- Single test object
- Postman Collection v2.1
- Export file with nested structure

**Response:**
```json
{
  "status": "success",
  "imported_tests": 5,
  "total_tests": 10,
  "message": "Successfully imported 5 test(s)",
  "errors": ["Optional array of error messages"]
}
```

#### `POST /export/tests`
**Description:** Export tests as JSON  
**Parameters:**
```json
{
  "test_ids": ["uuid1", "uuid2"],
  "format": "standard"
}
```
**Response:**
```json
{
  "status": "success",
  "export_data": {
    "export_info": {
      "exported_at": "2024-01-01T12:00:00",
      "total_tests": 2,
      "format": "standard"
    },
    "tests": [...]
  },
  "download_filename": "api_tests_20240101_120000.json"
}
```

#### `POST /export/results/word`
**Description:** Export test results as Word document  
**Parameters:**
```json
{
  "test_ids": ["uuid1", "uuid2"],
  "include_charts": true
}
```
**Response:**
```json
{
  "status": "success",
  "document": {
    "document_id": "uuid",
    "filename": "test_results_20240101_120000.docx",
    "generated_at": "2024-01-01T12:00:00",
    "pages": 5,
    "sections": ["Executive Summary", "Test Results", "Performance Analysis", "Recommendations"],
    "charts_included": true,
    "total_tests": 2
  },
  "download_url": "/download/filename.docx",
  "format": "docx",
  "preview": "Professional test report with charts and analysis"
}
```

### **Repository Analysis Endpoints**

#### `POST /analyze-repository`
**Description:** Analyze GitHub repository to generate tests  
**Parameters:**
```json
{
  "github_url": "https://github.com/user/repo",
  "branch": "main",
  "test_description": "Optional description"
}
```
**Response:**
```json
{
  "status": "success",
  "repository": "https://github.com/user/repo",
  "branch": "main",
  "generated_tests": [...],
  "next_steps": "Use /tests endpoints to manage tests"
}
```

#### `POST /full-analysis`
**Description:** Complete repository analysis with execution  
**Parameters:** Same as `/analyze-repository`  
**Response:**
```json
{
  "status": "success",
  "repository": "repo_url",
  "analysis": {...},
  "execution": {
    "summary": {
      "total_tests": 5,
      "passed": 5,
      "failed": 0,
      "success_rate": 100
    }
  }
}
```

### **Utility Endpoints**

#### `POST /create-sample-tests`
**Description:** Create sample tests for demonstration  
**Parameters:** None  
**Response:**
```json
{
  "status": "success",
  "message": "Created 1 sample tests",
  "created_tests": [...]
}
```

## 🎨 **Frontend Components**

### **Architecture Overview:**
The frontend is built as a Single Page Application (SPA) using vanilla HTML5, CSS3, and modern JavaScript ES6+. It provides a comprehensive interface for all platform features through a tabbed navigation system.

### **Component Structure:**

```mermaid
graph TD
    subgraph "Frontend Application"
        A[Main Application Container]
        B[Header Component]
        C[Status Indicator]
        D[Tab Navigation Controller]
        
        subgraph "Tab Components"
            E[Auto-Generate Tab]
            F[Manual Create Tab]
            G[Test Management Tab]
            H[AI Suggestions Tab]
        end
        
        subgraph "Shared Components"
            I[Test Form Builder]
            J[Assertion Manager]
            K[File Import/Export]
            L[Test List Display]
            M[Edit Modal]
            N[Execution Results]
        end
        
        subgraph "Services"
            O[API Client Service]
            P[State Management]
            Q[UI Utils]
            R[Validation Service]
        end
    end
    
    A --> B
    A --> C
    A --> D
    D --> E
    D --> F
    D --> G
    D --> H
    
    E --> I
    F --> I
    G --> L
    H --> J
    
    I --> J
    L --> M
    G --> K
    M --> N
    
    E --> O
    F --> O
    G --> O
    H --> O
    
    O --> P
    P --> Q
    Q --> R
```

### **Key Frontend Features:**

#### **1. Tab-based Navigation System**
- **Auto-Generate Tab** - Repository analysis and automatic test generation
- **Manual Create Tab** - Custom test creation with form validation
- **Test Management Tab** - CRUD operations for test management
- **AI Suggestions Tab** - AI-powered recommendations and insights

#### **2. Smart Form Components**
- **Dynamic Assertion Builder** - Add/remove assertions with type selection
- **JSON Validators** - Real-time validation for headers and body
- **Method Selectors** - HTTP method dropdown with context awareness
- **Endpoint Input** - URL validation with protocol detection

#### **3. Real-time Features**
- **Backend Status Monitor** - Live connection status with auto-retry
- **Progress Indicators** - Loading states for async operations
- **Toast Notifications** - Success/error messages with auto-dismiss
- **Live Test Results** - Real-time execution feedback

#### **4. File Handling Components**
- **Import Dialog** - Multi-format file upload with preview
- **Export Generator** - JSON/Word document generation
- **Postman Converter** - Collection format detection and conversion
- **Drag & Drop Support** - File upload with visual feedback

#### **5. Test Management Interface**
```javascript
// Core frontend components and their responsibilities
const FrontendComponents = {
    TabManager: {
        showTab: 'Switch between application tabs',
        initializeTabs: 'Set up tab navigation and default state'
    },
    
    TestManager: {
        loadTests: 'Fetch and display all tests',
        displayTestsList: 'Render test list with actions',
        editTest: 'In-line test editing with form',
        deleteTest: 'Test deletion with confirmation',
        duplicateTest: 'Create copy of existing test'
    },
    
    FormHandlers: {
        handleManualTestSave: 'Process manual test creation',
        collectAssertions: 'Gather assertion data from form',
        parseJSON: 'Validate and parse JSON inputs',
        addAssertion: 'Dynamically add assertion fields',
        removeAssertion: 'Remove assertion from form'
    },
    
    ImportExport: {
        showImportDialog: 'File selection and upload',
        importTests: 'Process imported test data',
        exportTests: 'Generate and download test exports',
        exportWordReport: 'Create professional reports'
    },
    
    AIIntegration: {
        getTestSuggestions: 'AI test recommendations',
        getAIAssertions: 'Smart assertion suggestions',
        getNextCallSuggestions: 'API flow predictions'
    },
    
    ExecutionEngine: {
        executeTest: 'Single test execution',
        executeBatch: 'Multiple test execution',
        displayResults: 'Show execution outcomes'
    }
};
```

### **CSS Architecture:**
- **Modern CSS Grid/Flexbox** - Responsive layouts
- **CSS Variables** - Consistent theming and colors
- **Animations & Transitions** - Smooth user interactions
- **Mobile-First Design** - Responsive across devices

### **JavaScript Architecture:**
- **ES6+ Features** - Modern JavaScript with async/await
- **Modular Functions** - Organized code structure
- **Event-Driven** - Reactive UI updates
- **Error Handling** - Comprehensive error management

## 📦 **Dependencies**

### **Backend Dependencies (Python):**

| Package | Version | Purpose | Features Used |
|---------|---------|---------|---------------|
| `fastapi` | 0.68.0 | Web framework | REST APIs, automatic docs, validation |
| `uvicorn` | 0.15.0 | ASGI server | Production server, auto-reload |
| `python-dotenv` | 1.0.0 | Environment variables | Configuration management |
| `typing-extensions` | ≥3.7.4 | Type hints | Enhanced type checking |

#### **FastAPI Features Utilized:**
- **Automatic API Documentation** - Swagger UI at `/docs`
- **Request/Response Validation** - Pydantic models
- **Path Parameters** - Dynamic URL routing
- **Query Parameters** - Optional filters and parameters
- **Request Bodies** - JSON payload validation
- **HTTP Exception Handling** - Proper error responses
- **CORS Middleware** - Cross-origin resource sharing
- **Dependency Injection** - Service layer architecture

#### **Uvicorn Configuration:**
```python
uvicorn.run(
    "main_minimal_clean:app",
    host="0.0.0.0",          # Allow external connections
    port=8000,               # Standard development port
    log_level="info",        # Detailed logging
    reload=False             # Production mode (set True for dev)
)
```

### **Frontend Dependencies (Web Standards):**

| Technology | Version | Purpose | Features Used |
|------------|---------|---------|---------------|
| HTML5 | Latest | Structure | Semantic elements, forms, file API |
| CSS3 | Latest | Styling | Grid, flexbox, animations, variables |
| JavaScript | ES6+ | Functionality | Modules, async/await, fetch API |
| Web APIs | Latest | Browser features | File API, Storage API, Fetch API |

#### **Browser Compatibility:**
- **Chrome** 60+ ✅
- **Firefox** 55+ ✅  
- **Safari** 12+ ✅
- **Edge** 79+ ✅

### **External Integrations:**

| Service | Purpose | Implementation |
|---------|---------|----------------|
| GitHub API | Repository analysis | REST API calls for repo metadata |
| Postman Collections | Test import | JSON parsing and conversion |
| Word Documents | Report export | Mock implementation (extensible) |

### **Development Dependencies:**
```bash
# Optional development tools
pip install --dev pytest          # Testing framework
pip install --dev black           # Code formatting
pip install --dev flake8          # Linting
pip install --dev mypy            # Type checking
```

### **Installation Commands:**

#### **Minimal Installation:**
```bash
pip install fastapi==0.68.0 uvicorn==0.15.0 python-dotenv==1.0.0 typing-extensions>=3.7.4
```

#### **From Requirements File:**
```bash
pip install -r requirements.txt
```

#### **Development Environment:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Optional: Install development tools
pip install pytest black flake8 mypy
```

### **System Requirements:**

#### **Minimum Requirements:**
- **Python:** 3.7+
- **RAM:** 512MB available
- **Storage:** 100MB free space
- **Network:** Internet connection for AI features

#### **Recommended Requirements:**
- **Python:** 3.9+
- **RAM:** 1GB available
- **Storage:** 500MB free space
- **Browser:** Latest version of Chrome/Firefox/Safari

## 💻 **Usage Examples**

### **1. Basic Test Creation:**
```javascript
// Create a simple GET test
const testData = {
    name: "Get Users List",
    method: "GET",
    endpoint: "https://jsonplaceholder.typicode.com/users",
    headers: {"Content-Type": "application/json"},
    assertions: [
        {"type": "status_code", "expected": 200},
        {"type": "response_time", "max_ms": 2000}
    ],
    description: "Retrieve list of all users",
    tags: ["users", "api", "get"],
    collection: "user-management"
};

// Send to backend
const response = await fetch('http://localhost:8000/tests', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(testData)
});
```

### **2. Batch Test Execution:**
```javascript
// Execute multiple tests
const batchRequest = {
    test_ids: ["test-1", "test-2", "test-3"],
    concurrent: true
};

const result = await fetch('http://localhost:8000/execute-batch', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(batchRequest)
});

const execution = await result.json();
console.log(`Success Rate: ${execution.batch_execution.summary.success_rate}%`);
```

### **3. Postman Collection Import:**
```javascript
// Import Postman collection
const postmanCollection = {
    "info": {"name": "My API Collection"},
    "item": [
        {
            "name": "Get Users",
            "request": {
                "method": "GET",
                "url": "https://api.example.com/users"
            }
        }
    ]
};

await fetch('http://localhost:8000/import/tests', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({tests: postmanCollection})
});
```

### **4. AI Test Generation:**
```javascript
// Get AI suggestions for an endpoint
const suggestions = await fetch('http://localhost:8000/ai-suggestions/test', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        endpoint: "/api/products",
        method: "POST",
        context: "E-commerce product management"
    })
});

const aiTests = await suggestions.json();
console.log(`Generated ${aiTests.total_suggestions} test suggestions`);
```

### **5. Repository Analysis:**
```javascript
// Analyze GitHub repository
const analysis = await fetch('http://localhost:8000/analyze-repository', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        github_url: "https://github.com/user/api-project",
        branch: "main",
        test_description: "REST API endpoints analysis"
    })
});

const result = await analysis.json();
console.log(`Generated ${result.generated_tests.length} tests from repository`);
```

## 🔧 **Troubleshooting**

### **Common Issues & Solutions:**

#### **1. Backend Connection Issues**
**Problem:** Frontend shows "❌ Disconnected"
```bash
# Solution 1: Check if backend is running
python main_minimal_clean.py

# Solution 2: Check port availability
lsof -i :8000

# Solution 3: Try different port
uvicorn main_minimal_clean:app --port 8001
```

#### **2. Import/Export Issues**
**Problem:** File import fails
```javascript
// Check file format
const validFormats = [
    'JSON array of tests',
    'Single test object', 
    'Postman Collection v2.1',
    'Platform export file'
];

// Validate JSON structure
try {
    const data = JSON.parse(fileContent);
    console.log('Valid JSON format');
} catch (error) {
    console.error('Invalid JSON:', error.message);
}
```

#### **3. CORS Errors**
**Problem:** Browser blocks requests
```bash
# Backend solution: CORS is pre-configured
# Frontend solution: Check browser console
# Try: Disable browser security (development only)
# Chrome: --disable-web-security --user-data-dir=/tmp/chrome_dev
```

#### **4. AI Features Not Working**
**Problem:** AI suggestions return errors
```bash
# Check internet connection
curl -I https://api.github.com

# Verify endpoint accessibility
curl http://localhost:8000/health

# Test AI endpoint directly
curl -X POST http://localhost:8000/ai-suggestions/test \
  -H "Content-Type: application/json" \
  -d '{"endpoint":"/test","method":"GET"}'
```

### **Debug Mode:**
```javascript
// Enable frontend debugging
const DEBUG = true;
const API_BASE = DEBUG ? 'http://localhost:8000' : 'https://your-domain.com';

// Backend debug mode
# Set environment variable
export DEBUG=True
python main_minimal_clean.py
```

### **Performance Optimization:**
```bash
# Backend optimization
pip install --upgrade fastapi uvicorn

# Frontend optimization
# Use browser dev tools to monitor:
# - Network requests
# - Memory usage  
# - JavaScript performance
```

### **Getting Help:**
1. **Check logs** - Backend terminal output
2. **Browser console** - Frontend error messages (F12)
3. **API documentation** - http://localhost:8000/docs
4. **Troubleshooting guide** - UI_TROUBLESHOOTING.md
5. **Test endpoints** - Use curl or Postman to test API

---