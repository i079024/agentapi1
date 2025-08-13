#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import json
import traceback
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="Agent API Testing Platform", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
stored_tests = {}

# Data models
class TestAssertion(BaseModel):
    type: str
    expected: str
    description: Optional[str] = ""

class APITest(BaseModel):
    name: str
    method: str
    endpoint: str
    description: Optional[str] = ""
    headers: Optional[Dict[str, str]] = {}
    body: Optional[Any] = None
    assertions: Optional[List[TestAssertion]] = []
    tags: Optional[List[str]] = []
    collection: Optional[str] = "default"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Agent API Testing Platform is running",
        "version": "1.0.0",
        "stored_tests": len(stored_tests)
    }

@app.get("/tests")
async def get_tests():
    """Get all stored tests"""
    return {
        "status": "success",
        "tests": list(stored_tests.values()),
        "total": len(stored_tests)
    }

@app.post("/tests")
async def create_test(test: APITest):
    """Create a new test"""
    test_id = str(uuid.uuid4())
    current_time = datetime.now().isoformat()
    
    test_data = {
        "id": test_id,
        "name": test.name,
        "method": test.method.upper(),
        "endpoint": test.endpoint,
        "description": test.description,
        "headers": test.headers or {},
        "body": test.body,
        "assertions": [assertion.dict() for assertion in test.assertions] if test.assertions else [],
        "tags": test.tags or [],
        "collection": test.collection or "default",
        "created_at": current_time,
        "updated_at": current_time
    }
    
    stored_tests[test_id] = test_data
    
    return {
        "status": "success",
        "message": f"Test '{test.name}' created successfully",
        "test": test_data
    }

def extract_url_from_postman(url_data):
    """Extract URL string from Postman URL object or string"""
    if isinstance(url_data, str):
        return url_data
    elif isinstance(url_data, dict):
        # Try 'raw' field first
        if url_data.get("raw"):
            return url_data["raw"]
        
        # Construct from parts
        protocol = url_data.get("protocol", "https")
        host = url_data.get("host", [])
        if isinstance(host, list):
            host = ".".join(host)
        path = url_data.get("path", [])
        if isinstance(path, list):
            path = "/" + "/".join(path)
        
        return f"{protocol}://{host}{path}"
    return ""

def convert_postman_headers(headers_list):
    """Convert Postman headers list to dict"""
    headers = {}
    if not isinstance(headers_list, list):
        return headers
        
    for header in headers_list:
        if isinstance(header, dict) and not header.get("disabled", False):
            key = header.get("key", "")
            value = header.get("value", "")
            if key and value:
                headers[key] = value
    return headers

def convert_postman_body(body_data):
    """Convert Postman body to our format"""
    if not isinstance(body_data, dict):
        return None
    
    mode = body_data.get("mode", "")
    if mode == "raw":
        raw_data = body_data.get("raw", "")
        try:
            # Try to parse as JSON
            return json.loads(raw_data)
        except:
            return raw_data
    elif mode == "formdata":
        # Convert form data to dict
        form_data = {}
        for item in body_data.get("formdata", []):
            if isinstance(item, dict):
                key = item.get("key")
                value = item.get("value") 
                if key and value:
                    form_data[key] = value
        return form_data
    elif mode == "urlencoded":
        # Convert URL encoded to dict
        url_data = {}
        for item in body_data.get("urlencoded", []):
            if isinstance(item, dict):
                key = item.get("key")
                value = item.get("value")
                if key and value:
                    url_data[key] = value
        return url_data
    
    return None

def convert_postman_collection(collection_data):
    """Convert Postman collection to our test format"""
    tests = []
    
    def process_items(items, folder_name=""):
        for item in items:
            if "item" in item:
                # This is a folder
                folder_name = item.get("name", "")
                process_items(item["item"], folder_name)
            else:
                # This is a request
                if "request" in item:
                    test = {
                        "name": item.get("name", "Unnamed Test"),
                        "request": item["request"],
                        "collection": folder_name or "postman-import"
                    }
                    tests.append(test)
    
    process_items(collection_data.get("item", []))
    return tests

@app.post("/import/tests")
async def import_tests(request: dict):
    """Enhanced import tests from various formats with detailed debugging"""
    try:
        import_data = request.get("tests", {})
        
        print(f"\n=== BACKEND IMPORT DEBUG ===")
        print(f"Received import_data type: {type(import_data)}")
        print(f"Received import_data length: {len(import_data) if isinstance(import_data, (list, dict)) else 'N/A'}")
        
        if not import_data:
            raise HTTPException(status_code=400, detail="No test data provided")
        
        imported_tests = []
        errors = []
        
        # Handle different import formats
        tests_to_import = []
        
        if isinstance(import_data, dict):
            # Check if it's a Postman collection
            if "info" in import_data and "item" in import_data:
                print("Detected Postman collection format")
                tests_to_import = convert_postman_collection(import_data)
            # Check if it's our export format
            elif "tests" in import_data:
                print("Detected export format")
                tests_to_import = import_data["tests"]
            # Single test object
            else:
                print("Treating as single test object")
                tests_to_import = [import_data]
        elif isinstance(import_data, list):
            print(f"Detected array format with {len(import_data)} items")
            tests_to_import = import_data
        else:
            raise HTTPException(status_code=400, detail="Invalid import format")
        
        print(f"Tests to import: {len(tests_to_import)}")
        
        # Process each test with detailed logging
        for i, test_data in enumerate(tests_to_import):
            try:
                print(f"\n--- Processing test {i+1}/{len(tests_to_import)} ---")
                print(f"Test data keys: {list(test_data.keys()) if isinstance(test_data, dict) else 'Not a dict'}")
                
                # Normalize the test data
                normalized_test = {}
                
                # Handle Postman request format
                if "request" in test_data:
                    print("Processing Postman request format")
                    request_data = test_data["request"]
                    normalized_test = {
                        "name": test_data.get("name", f"Test {i+1}"),
                        "method": request_data.get("method", "GET"),
                        "endpoint": extract_url_from_postman(request_data.get("url", "")),
                        "description": request_data.get("description", ""),
                        "headers": convert_postman_headers(request_data.get("header", [])),
                        "body": convert_postman_body(request_data.get("body", {})),
                        "tags": ["postman", "imported"],
                        "collection": test_data.get("collection", "postman-import")
                    }
                else:
                    print("Processing direct test format")
                    # Direct test format with multiple field name support
                    normalized_test = {
                        "name": (test_data.get("name") or test_data.get("title") or f"Test {i+1}"),
                        "method": (test_data.get("method") or test_data.get("http_method") or "GET").upper(),
                        "endpoint": (test_data.get("endpoint") or test_data.get("url") or test_data.get("uri") or ""),
                        "description": (test_data.get("description") or test_data.get("desc") or ""),
                        "headers": test_data.get("headers", {}),
                        "body": test_data.get("body") or test_data.get("data"),
                        "tags": test_data.get("tags", ["imported"]),
                        "collection": test_data.get("collection", "imported-tests")
                    }
                
                print(f"Normalized - Name: {normalized_test['name']}, Method: {normalized_test['method']}, Endpoint: {normalized_test['endpoint']}")
                
                # Validate required fields
                if not normalized_test.get("endpoint"):
                    error_msg = f"Test {i+1} ({normalized_test.get('name', 'Unknown')}): Missing endpoint/URL"
                    print(f"❌ VALIDATION ERROR: {error_msg}")
                    errors.append(error_msg)
                    continue
                
                # Ensure we have a name
                if not normalized_test.get("name"):
                    normalized_test["name"] = f"Imported Test {i+1}"
                
                # Generate test object
                test_id = str(uuid.uuid4())
                current_time = datetime.now().isoformat()
                
                test_object = {
                    "id": test_id,
                    "name": normalized_test["name"],
                    "method": normalized_test["method"],
                    "endpoint": str(normalized_test["endpoint"]).strip(),
                    "description": normalized_test.get("description") or f"Imported test: {normalized_test['method']} {normalized_test['endpoint']}",
                    "headers": normalized_test.get("headers", {}),
                    "body": normalized_test.get("body"),
                    "assertions": [
                        {
                            "type": "status_code",
                            "expected": "200",
                            "description": "Status code should be 200"
                        }
                    ],
                    "tags": normalized_test.get("tags", ["imported"]),
                    "collection": normalized_test.get("collection", "imported-tests"),
                    "created_at": current_time,
                    "updated_at": current_time,
                    "imported_at": current_time
                }
                
                # Store the test
                stored_tests[test_id] = test_object
                imported_tests.append(test_object)
                
                print(f"✅ Successfully imported test {i+1}: {test_object['name']} ({test_object['method']} {test_object['endpoint']})")
                
            except Exception as e:
                error_msg = f"Test {i+1}: Error processing - {str(e)}"
                print(f"❌ PROCESSING ERROR: {error_msg}")
                errors.append(error_msg)
                traceback.print_exc()
        
        print(f"\n=== FINAL IMPORT SUMMARY ===")
        print(f"Total tests received: {len(tests_to_import)}")
        print(f"Successfully imported: {len(imported_tests)}")
        print(f"Errors: {len(errors)}")
        print(f"Stored tests count: {len(stored_tests)}")
        
        if not imported_tests and errors:
            raise HTTPException(status_code=400, detail=f"Import failed: {'; '.join(errors[:3])}")
        
        result = {
            "status": "success",
            "imported_tests": len(imported_tests),
            "total_tests": len(imported_tests),
            "errors": errors,
            "tests": imported_tests[:3],  # Return first 3 for preview
            "message": f"Successfully imported {len(imported_tests)} test(s)"
        }
        
        print(f"Returning result: {result}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ IMPORT EXCEPTION: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@app.get("/tests/{test_id}")
async def get_test(test_id: str):
    """Get a specific test by ID"""
    if test_id not in stored_tests:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return {
        "status": "success",
        "test": stored_tests[test_id]
    }

@app.delete("/tests/{test_id}")
async def delete_test(test_id: str):
    """Delete a test by ID"""
    if test_id not in stored_tests:
        raise HTTPException(status_code=404, detail="Test not found")
    
    deleted_test = stored_tests.pop(test_id)
    
    return {
        "status": "success",
        "message": f"Test '{deleted_test['name']}' deleted successfully"
    }

@app.post("/create-sample-tests")
async def create_sample_tests():
    """Create sample tests for demonstration"""
    sample_tests = [
        {
            "name": "JSONPlaceholder - Get Posts",
            "method": "GET",
            "endpoint": "https://jsonplaceholder.typicode.com/posts",
            "description": "Fetch all posts from JSONPlaceholder",
            "headers": {"Accept": "application/json"},
            "tags": ["sample", "get"]
        },
        {
            "name": "JSONPlaceholder - Get User 1",
            "method": "GET", 
            "endpoint": "https://jsonplaceholder.typicode.com/users/1",
            "description": "Fetch user with ID 1",
            "headers": {"Accept": "application/json"},
            "tags": ["sample", "user"]
        },
        {
            "name": "HTTPBin - Post Test",
            "method": "POST",
            "endpoint": "https://httpbin.org/post",
            "description": "Test POST request with HTTPBin",
            "headers": {"Content-Type": "application/json"},
            "body": {"test": "data", "timestamp": "2024-01-01"},
            "tags": ["sample", "post"]
        }
    ]
    
    created_tests = []
    for test_data in sample_tests:
        test_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        test_object = {
            "id": test_id,
            "name": test_data["name"],
            "method": test_data["method"],
            "endpoint": test_data["endpoint"],
            "description": test_data["description"],
            "headers": test_data.get("headers", {}),
            "body": test_data.get("body"),
            "assertions": [
                {
                    "type": "status_code",
                    "expected": "200",
                    "description": "Status code should be 200"
                }
            ],
            "tags": test_data["tags"],
            "collection": "sample-tests",
            "created_at": current_time,
            "updated_at": current_time
        }
        
        stored_tests[test_id] = test_object
        created_tests.append(test_object)
    
    return {
        "status": "success",
        "message": f"Created {len(created_tests)} sample tests",
        "created_tests": created_tests
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Agent API Testing Platform...")
    print("📡 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)