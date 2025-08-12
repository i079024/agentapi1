"""
Assertion Service - Smart assertion validation and AI-powered suggestions
Handles response validation, assertion building, and intelligent recommendations
"""

import json
import re
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

class AssertionService:
    def __init__(self):
        self.assertion_types = {
            "status_code": self._validate_status_code,
            "response_time": self._validate_response_time,
            "json_path": self._validate_json_path,
            "json_schema": self._validate_json_schema,
            "header": self._validate_header,
            "content_type": self._validate_content_type,
            "body_contains": self._validate_body_contains,
            "body_not_contains": self._validate_body_not_contains,
            "regex_match": self._validate_regex_match,
            "array_length": self._validate_array_length,
            "value_equals": self._validate_value_equals,
            "value_greater_than": self._validate_value_greater_than,
            "value_less_than": self._validate_value_less_than,
            "value_in_range": self._validate_value_in_range,
            "custom_javascript": self._validate_custom_javascript
        }
    
    def validate_assertions(self, response_data: Dict[str, Any], assertions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate all assertions against response data"""
        results = {
            "total_assertions": len(assertions),
            "passed": 0,
            "failed": 0,
            "details": [],
            "overall_success": True
        }
        
        for assertion in assertions:
            assertion_result = self._validate_single_assertion(response_data, assertion)
            results["details"].append(assertion_result)
            
            if assertion_result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["overall_success"] = False
        
        return results
    
    def _validate_single_assertion(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single assertion"""
        assertion_type = assertion.get("type")
        
        if assertion_type not in self.assertion_types:
            return {
                "assertion": assertion,
                "passed": False,
                "error": f"Unknown assertion type: {assertion_type}",
                "details": None
            }
        
        try:
            validator = self.assertion_types[assertion_type]
            result = validator(response_data, assertion)
            
            return {
                "assertion": assertion,
                "passed": result["passed"],
                "details": result.get("details"),
                "error": result.get("error"),
                "actual_value": result.get("actual_value"),
                "expected_value": result.get("expected_value")
            }
            
        except Exception as e:
            return {
                "assertion": assertion,
                "passed": False,
                "error": f"Assertion validation error: {str(e)}",
                "details": None
            }
    
    def _validate_status_code(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate HTTP status code"""
        expected = assertion.get("expected", 200)
        actual = response_data.get("status_code", 0)
        
        return {
            "passed": actual == expected,
            "expected_value": expected,
            "actual_value": actual,
            "details": f"Status code: expected {expected}, got {actual}"
        }
    
    def _validate_response_time(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate response time"""
        max_time = assertion.get("max_ms", 5000)
        actual_time = response_data.get("response_time_ms", 0) * 1000  # Convert to ms
        
        return {
            "passed": actual_time <= max_time,
            "expected_value": f"<= {max_time}ms",
            "actual_value": f"{actual_time}ms",
            "details": f"Response time: {actual_time}ms (limit: {max_time}ms)"
        }
    
    def _validate_json_path(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate value at JSON path"""
        path = assertion.get("path", "")
        expected = assertion.get("expected")
        
        try:
            actual = self._get_json_path_value(response_data.get("body", {}), path)
            passed = actual == expected
            
            return {
                "passed": passed,
                "expected_value": expected,
                "actual_value": actual,
                "details": f"JSON path '{path}': expected {expected}, got {actual}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"JSON path error: {str(e)}",
                "details": f"Failed to evaluate path: {path}"
            }
    
    def _validate_json_schema(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JSON schema (simplified validation)"""
        schema = assertion.get("schema", {})
        body = response_data.get("body", {})
        
        try:
            # Simple schema validation (could be enhanced with jsonschema library)
            errors = self._validate_simple_schema(body, schema)
            
            return {
                "passed": len(errors) == 0,
                "details": f"Schema validation: {len(errors)} errors found",
                "error": "; ".join(errors) if errors else None
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Schema validation error: {str(e)}"
            }
    
    def _validate_header(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate response header"""
        header_name = assertion.get("header", "")
        expected = assertion.get("expected", "")
        headers = response_data.get("headers", {})
        
        # Case-insensitive header lookup
        actual = None
        for key, value in headers.items():
            if key.lower() == header_name.lower():
                actual = value
                break
        
        return {
            "passed": actual == expected,
            "expected_value": expected,
            "actual_value": actual,
            "details": f"Header '{header_name}': expected '{expected}', got '{actual}'"
        }
    
    def _validate_content_type(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content type"""
        expected = assertion.get("expected", "application/json")
        headers = response_data.get("headers", {})
        actual = headers.get("content-type", headers.get("Content-Type", ""))
        
        # Check if expected content type is in actual (allows for charset, etc.)
        passed = expected.lower() in actual.lower()
        
        return {
            "passed": passed,
            "expected_value": expected,
            "actual_value": actual,
            "details": f"Content type: expected '{expected}', got '{actual}'"
        }
    
    def _validate_body_contains(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate body contains text"""
        expected_text = assertion.get("text", "")
        body = str(response_data.get("body", ""))
        
        passed = expected_text in body
        
        return {
            "passed": passed,
            "expected_value": f"contains '{expected_text}'",
            "actual_value": f"body length: {len(body)}",
            "details": f"Body contains '{expected_text}': {passed}"
        }
    
    def _validate_body_not_contains(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate body does not contain text"""
        forbidden_text = assertion.get("text", "")
        body = str(response_data.get("body", ""))
        
        passed = forbidden_text not in body
        
        return {
            "passed": passed,
            "expected_value": f"does not contain '{forbidden_text}'",
            "actual_value": f"body length: {len(body)}",
            "details": f"Body does not contain '{forbidden_text}': {passed}"
        }
    
    def _validate_regex_match(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate regex pattern match"""
        pattern = assertion.get("pattern", "")
        target = assertion.get("target", "body")  # body, headers, or status
        
        if target == "body":
            text = str(response_data.get("body", ""))
        elif target == "headers":
            text = str(response_data.get("headers", {}))
        else:
            text = str(response_data.get(target, ""))
        
        try:
            match = re.search(pattern, text)
            passed = match is not None
            
            return {
                "passed": passed,
                "expected_value": f"matches pattern '{pattern}'",
                "actual_value": f"found match: {match.group() if match else 'none'}",
                "details": f"Regex '{pattern}' match in {target}: {passed}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Regex error: {str(e)}"
            }
    
    def _validate_array_length(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate array length"""
        path = assertion.get("path", "")
        expected_length = assertion.get("expected", 0)
        
        try:
            array_value = self._get_json_path_value(response_data.get("body", {}), path)
            
            if not isinstance(array_value, list):
                return {
                    "passed": False,
                    "error": f"Value at path '{path}' is not an array"
                }
            
            actual_length = len(array_value)
            passed = actual_length == expected_length
            
            return {
                "passed": passed,
                "expected_value": expected_length,
                "actual_value": actual_length,
                "details": f"Array length at '{path}': expected {expected_length}, got {actual_length}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Array length validation error: {str(e)}"
            }
    
    def _validate_value_equals(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate exact value equality"""
        path = assertion.get("path", "")
        expected = assertion.get("expected")
        
        try:
            actual = self._get_json_path_value(response_data.get("body", {}), path)
            passed = actual == expected
            
            return {
                "passed": passed,
                "expected_value": expected,
                "actual_value": actual,
                "details": f"Value at '{path}': expected {expected}, got {actual}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Value comparison error: {str(e)}"
            }
    
    def _validate_value_greater_than(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate value is greater than threshold"""
        path = assertion.get("path", "")
        threshold = assertion.get("threshold", 0)
        
        try:
            actual = self._get_json_path_value(response_data.get("body", {}), path)
            
            if not isinstance(actual, (int, float)):
                return {
                    "passed": False,
                    "error": f"Value at path '{path}' is not numeric"
                }
            
            passed = actual > threshold
            
            return {
                "passed": passed,
                "expected_value": f"> {threshold}",
                "actual_value": actual,
                "details": f"Value at '{path}': {actual} > {threshold} = {passed}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Numeric comparison error: {str(e)}"
            }
    
    def _validate_value_less_than(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate value is less than threshold"""
        path = assertion.get("path", "")
        threshold = assertion.get("threshold", 0)
        
        try:
            actual = self._get_json_path_value(response_data.get("body", {}), path)
            
            if not isinstance(actual, (int, float)):
                return {
                    "passed": False,
                    "error": f"Value at path '{path}' is not numeric"
                }
            
            passed = actual < threshold
            
            return {
                "passed": passed,
                "expected_value": f"< {threshold}",
                "actual_value": actual,
                "details": f"Value at '{path}': {actual} < {threshold} = {passed}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Numeric comparison error: {str(e)}"
            }
    
    def _validate_value_in_range(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate value is within range"""
        path = assertion.get("path", "")
        min_val = assertion.get("min", 0)
        max_val = assertion.get("max", 100)
        
        try:
            actual = self._get_json_path_value(response_data.get("body", {}), path)
            
            if not isinstance(actual, (int, float)):
                return {
                    "passed": False,
                    "error": f"Value at path '{path}' is not numeric"
                }
            
            passed = min_val <= actual <= max_val
            
            return {
                "passed": passed,
                "expected_value": f"between {min_val} and {max_val}",
                "actual_value": actual,
                "details": f"Value at '{path}': {actual} in range [{min_val}, {max_val}] = {passed}"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": f"Range validation error: {str(e)}"
            }
    
    def _validate_custom_javascript(self, response_data: Dict[str, Any], assertion: Dict[str, Any]) -> Dict[str, Any]:
        """Validate using custom JavaScript expression (mock implementation)"""
        expression = assertion.get("expression", "")
        
        # Mock implementation - in a real system, you'd use a JS engine
        return {
            "passed": True,  # Mock result
            "details": f"Custom JS validation: {expression} (mock result)",
            "note": "Custom JavaScript validation not fully implemented in demo"
        }
    
    def _get_json_path_value(self, data: Any, path: str) -> Any:
        """Get value from JSON data using dot notation path"""
        if not path:
            return data
        
        current = data
        parts = path.split(".")
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                index = int(part)
                current = current[index] if 0 <= index < len(current) else None
            else:
                raise ValueError(f"Cannot access path '{path}' in data")
        
        return current
    
    def _validate_simple_schema(self, data: Any, schema: Dict[str, Any]) -> List[str]:
        """Simple JSON schema validation"""
        errors = []
        
        schema_type = schema.get("type")
        if schema_type:
            if schema_type == "object" and not isinstance(data, dict):
                errors.append(f"Expected object, got {type(data).__name__}")
            elif schema_type == "array" and not isinstance(data, list):
                errors.append(f"Expected array, got {type(data).__name__}")
            elif schema_type == "string" and not isinstance(data, str):
                errors.append(f"Expected string, got {type(data).__name__}")
            elif schema_type == "number" and not isinstance(data, (int, float)):
                errors.append(f"Expected number, got {type(data).__name__}")
        
        # Validate required properties for objects
        if schema.get("type") == "object" and isinstance(data, dict):
            required = schema.get("required", [])
            for prop in required:
                if prop not in data:
                    errors.append(f"Missing required property: {prop}")
        
        return errors
    
    def suggest_assertions(self, response_data: Dict[str, Any], endpoint_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate intelligent assertion suggestions based on response data"""
        suggestions = []
        
        # Always suggest status code assertion
        suggestions.append({
            "type": "status_code",
            "expected": response_data.get("status_code", 200),
            "description": "Validate HTTP status code",
            "confidence": "high"
        })
        
        # Response time assertion
        response_time = response_data.get("response_time_ms", 0) * 1000
        if response_time > 0:
            # Suggest reasonable timeout (2x actual response time, min 1000ms)
            suggested_timeout = max(1000, int(response_time * 2))
            suggestions.append({
                "type": "response_time",
                "max_ms": suggested_timeout,
                "description": f"Validate response time is under {suggested_timeout}ms",
                "confidence": "medium"
            })
        
        # Content type assertion
        headers = response_data.get("headers", {})
        content_type = headers.get("content-type", headers.get("Content-Type", ""))
        if content_type:
            suggestions.append({
                "type": "content_type",
                "expected": content_type.split(";")[0],  # Remove charset
                "description": "Validate response content type",
                "confidence": "high"
            })
        
        # JSON structure assertions
        body = response_data.get("body", {})
        if isinstance(body, dict):
            # Suggest assertions for important fields
            for key, value in body.items():
                if key in ["id", "uuid", "status", "success", "error"]:
                    suggestions.append({
                        "type": "json_path",
                        "path": key,
                        "expected": value,
                        "description": f"Validate {key} field value",
                        "confidence": "medium"
                    })
        
        elif isinstance(body, list):
            # Array length assertion
            suggestions.append({
                "type": "array_length",
                "path": "",
                "expected": len(body),
                "description": f"Validate array contains {len(body)} items",
                "confidence": "low"
            })
        
        return suggestions
