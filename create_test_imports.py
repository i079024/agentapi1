#!/usr/bin/env python3

# Test import functionality separately
import json

def test_import_parsing():
    """Test different import formats to debug the issue"""
    
    # Test case 1: Simple test array
    test_data_1 = [
        {
            "name": "Get Users",
            "method": "GET", 
            "endpoint": "https://jsonplaceholder.typicode.com/users",
            "headers": {"Content-Type": "application/json"},
            "description": "Fetch all users"
        },
        {
            "name": "Create User",
            "method": "POST",
            "endpoint": "https://jsonplaceholder.typicode.com/users", 
            "headers": {"Content-Type": "application/json"},
            "body": {"name": "John", "email": "john@example.com"},
            "description": "Create new user"
        }
    ]
    
    # Test case 2: Export format
    test_data_2 = {
        "export_info": {
            "exported_at": "2024-01-01T00:00:00",
            "total_tests": 2
        },
        "tests": [
            {
                "name": "API Health Check",
                "method": "GET",
                "endpoint": "https://api.example.com/health",
                "headers": {},
                "description": "Check API health"
            },
            {
                "name": "Login Test", 
                "method": "POST",
                "endpoint": "https://api.example.com/login",
                "headers": {"Content-Type": "application/json"},
                "body": {"username": "test", "password": "test123"},
                "description": "Test user login"
            }
        ]
    }
    
    # Test case 3: Postman collection format
    test_data_3 = {
        "info": {
            "name": "Test Collection",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "Get Posts",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Accept",
                            "value": "application/json"
                        }
                    ],
                    "url": {
                        "raw": "https://jsonplaceholder.typicode.com/posts",
                        "protocol": "https",
                        "host": ["jsonplaceholder", "typicode", "com"],
                        "path": ["posts"]
                    }
                }
            },
            {
                "name": "Create Post",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": "{\"title\": \"Test Post\", \"body\": \"Test content\", \"userId\": 1}"
                    },
                    "url": {
                        "raw": "https://jsonplaceholder.typicode.com/posts",
                        "protocol": "https", 
                        "host": ["jsonplaceholder", "typicode", "com"],
                        "path": ["posts"]
                    }
                }
            }
        ]
    }
    
    print("=== Import Test Cases ===")
    print(f"Test 1 (Simple Array): {len(test_data_1)} tests")
    print(f"Test 2 (Export Format): {len(test_data_2['tests'])} tests")
    print(f"Test 3 (Postman Collection): {len(test_data_3['item'])} items")
    
    # Save test files
    with open('/Users/i079024/ariba/agenticapi_pers/agentapi3/test_import_1.json', 'w') as f:
        json.dump(test_data_1, f, indent=2)
    
    with open('/Users/i079024/ariba/agenticapi_pers/agentapi3/test_import_2.json', 'w') as f:
        json.dump(test_data_2, f, indent=2)
        
    with open('/Users/i079024/ariba/agenticapi_pers/agentapi3/test_import_3.json', 'w') as f:
        json.dump(test_data_3, f, indent=2)
    
    print("\n✅ Created test import files:")
    print("  - test_import_1.json (Simple Array)")
    print("  - test_import_2.json (Export Format)")  
    print("  - test_import_3.json (Postman Collection)")
    print("\nTry importing these files to test different formats!")

if __name__ == "__main__":
    test_import_parsing()