"""
Test Management Service - CRUD operations for API tests
Handles creation, editing, deletion, and organization of API tests
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

class TestManagementService:
    def __init__(self):
        self.tests_file = "saved_tests.json"
        self.tests = self._load_tests()
    
    def _load_tests(self) -> Dict[str, Any]:
        """Load tests from file storage"""
        try:
            if os.path.exists(self.tests_file):
                with open(self.tests_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
    
    def _save_tests(self):
        """Save tests to file storage"""
        try:
            with open(self.tests_file, 'w') as f:
                json.dump(self.tests, f, indent=2, default=str)
        except Exception as e:
            print(f"Failed to save tests: {e}")
    
    def create_test(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new API test"""
        test_id = str(uuid.uuid4())
        
        # Validate required fields
        required_fields = ['name', 'method', 'url']
        for field in required_fields:
            if field not in test_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Create test with metadata
        test = {
            "id": test_id,
            "name": test_data["name"],
            "description": test_data.get("description", ""),
            "method": test_data["method"].upper(),
            "url": test_data["url"],
            "headers": test_data.get("headers", {}),
            "body": test_data.get("body"),
            "assertions": test_data.get("assertions", []),
            "tags": test_data.get("tags", []),
            "timeout": test_data.get("timeout", 30),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "created_by": test_data.get("created_by", "user"),
            "version": 1,
            "enabled": test_data.get("enabled", True)
        }
        
        self.tests[test_id] = test
        self._save_tests()
        
        return test
    
    def get_test(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific test by ID"""
        return self.tests.get(test_id)
    
    def get_all_tests(self, 
                     tags: Optional[List[str]] = None,
                     enabled_only: bool = False) -> List[Dict[str, Any]]:
        """Get all tests with optional filtering"""
        tests_list = list(self.tests.values())
        
        # Filter by tags
        if tags:
            tests_list = [t for t in tests_list if any(tag in t.get("tags", []) for tag in tags)]
        
        # Filter by enabled status
        if enabled_only:
            tests_list = [t for t in tests_list if t.get("enabled", True)]
        
        # Sort by creation date (newest first)
        tests_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return tests_list
    
    def update_test(self, test_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing test"""
        if test_id not in self.tests:
            return None
        
        test = self.tests[test_id].copy()
        
        # Update allowed fields
        updatable_fields = [
            'name', 'description', 'method', 'url', 'headers', 
            'body', 'assertions', 'tags', 'timeout', 'enabled'
        ]
        
        for field in updatable_fields:
            if field in update_data:
                test[field] = update_data[field]
        
        # Update metadata
        test["updated_at"] = datetime.now().isoformat()
        test["version"] = test.get("version", 1) + 1
        
        self.tests[test_id] = test
        self._save_tests()
        
        return test
    
    def delete_test(self, test_id: str) -> bool:
        """Delete a test"""
        if test_id in self.tests:
            del self.tests[test_id]
            self._save_tests()
            return True
        return False
    
    def duplicate_test(self, test_id: str, new_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a duplicate of an existing test"""
        original_test = self.get_test(test_id)
        if not original_test:
            return None
        
        # Create new test data
        test_data = original_test.copy()
        test_data["name"] = new_name or f"{original_test['name']} (Copy)"
        
        # Remove metadata fields
        for field in ['id', 'created_at', 'updated_at', 'version']:
            test_data.pop(field, None)
        
        return self.create_test(test_data)
    
    def get_tests_by_url_pattern(self, url_pattern: str) -> List[Dict[str, Any]]:
        """Find tests that match a URL pattern"""
        matching_tests = []
        for test in self.tests.values():
            if url_pattern.lower() in test.get("url", "").lower():
                matching_tests.append(test)
        return matching_tests
    
    def get_test_statistics(self) -> Dict[str, Any]:
        """Get statistics about saved tests"""
        all_tests = list(self.tests.values())
        
        if not all_tests:
            return {
                "total_tests": 0,
                "enabled_tests": 0,
                "disabled_tests": 0,
                "methods": {},
                "tags": {},
                "last_created": None
            }
        
        # Method distribution
        methods = {}
        for test in all_tests:
            method = test.get("method", "UNKNOWN")
            methods[method] = methods.get(method, 0) + 1
        
        # Tag usage
        tags = {}
        for test in all_tests:
            for tag in test.get("tags", []):
                tags[tag] = tags.get(tag, 0) + 1
        
        # Enabled/disabled counts
        enabled_count = len([t for t in all_tests if t.get("enabled", True)])
        
        # Latest creation date
        latest_test = max(all_tests, key=lambda x: x.get("created_at", ""))
        
        return {
            "total_tests": len(all_tests),
            "enabled_tests": enabled_count,
            "disabled_tests": len(all_tests) - enabled_count,
            "methods": methods,
            "tags": tags,
            "last_created": latest_test.get("created_at"),
            "last_test_name": latest_test.get("name")
        }
    
    def export_tests(self, test_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Export tests as JSON data"""
        if test_ids:
            tests_to_export = {tid: self.tests[tid] for tid in test_ids if tid in self.tests}
        else:
            tests_to_export = self.tests.copy()
        
        export_data = {
            "export_metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0",
                "total_tests": len(tests_to_export),
                "tool": "Agent API Testing Platform"
            },
            "tests": tests_to_export
        }
        
        return export_data
    
    def import_tests(self, import_data: Dict[str, Any], merge_strategy: str = "skip") -> Dict[str, Any]:
        """
        Import tests from JSON data
        merge_strategy: 'skip', 'overwrite', or 'rename'
        """
        if "tests" not in import_data:
            raise ValueError("Invalid import data: missing 'tests' key")
        
        imported_tests = import_data["tests"]
        results = {
            "imported": 0,
            "skipped": 0,
            "renamed": 0,
            "errors": []
        }
        
        for test_id, test_data in imported_tests.items():
            try:
                if test_id in self.tests:
                    if merge_strategy == "skip":
                        results["skipped"] += 1
                        continue
                    elif merge_strategy == "rename":
                        # Create new test with renamed title
                        test_data["name"] = f"{test_data.get('name', 'Imported Test')} (Imported)"
                        new_test = self.create_test(test_data)
                        results["renamed"] += 1
                        continue
                    # else overwrite (fall through)
                
                # Import the test
                test_data["updated_at"] = datetime.now().isoformat()
                self.tests[test_id] = test_data
                results["imported"] += 1
                
            except Exception as e:
                results["errors"].append(f"Test {test_id}: {str(e)}")
        
        if results["imported"] > 0 or results["renamed"] > 0:
            self._save_tests()
        
        return results
