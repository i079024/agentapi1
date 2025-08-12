"""
AI Suggestion Service - AI-powered test and assertion recommendations
Provides intelligent suggestions for test scenarios, assertions, and next API calls
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class AISuggestionService:
    def __init__(self):
        self.endpoint_patterns = {
            'user_management': {
                'patterns': ['/users', '/user', '/accounts', '/account', '/profile'],
                'common_tests': [
                    {'name': 'Create User', 'method': 'POST', 'path': '/users'},
                    {'name': 'Get User', 'method': 'GET', 'path': '/users/{id}'},
                    {'name': 'Update User', 'method': 'PUT', 'path': '/users/{id}'},
                    {'name': 'Delete User', 'method': 'DELETE', 'path': '/users/{id}'},
                    {'name': 'List Users', 'method': 'GET', 'path': '/users'}
                ]
            },
            'authentication': {
                'patterns': ['/auth', '/login', '/logout', '/token', '/signin'],
                'common_tests': [
                    {'name': 'Login', 'method': 'POST', 'path': '/auth/login'},
                    {'name': 'Logout', 'method': 'POST', 'path': '/auth/logout'},
                    {'name': 'Token Refresh', 'method': 'POST', 'path': '/auth/refresh'},
                    {'name': 'Get Profile', 'method': 'GET', 'path': '/auth/profile'}
                ]
            },
            'api_operations': {
                'patterns': ['/api', '/v1', '/v2'],
                'common_tests': [
                    {'name': 'API Health Check', 'method': 'GET', 'path': '/health'},
                    {'name': 'API Status', 'method': 'GET', 'path': '/status'},
                    {'name': 'API Info', 'method': 'GET', 'path': '/info'}
                ]
            }
        }
        
        self.response_patterns = {
            'success_responses': [200, 201, 202, 204],
            'error_responses': [400, 401, 403, 404, 422, 500],
            'common_headers': [
                'content-type', 'authorization', 'x-api-key', 
                'accept', 'user-agent', 'cache-control'
            ]
        }
    
    def suggest_tests_for_endpoint(self, endpoint_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test suggestions for a specific endpoint"""
        endpoint_path = endpoint_info.get('path', '').lower()
        method = endpoint_info.get('method', 'GET').upper()
        
        suggestions = []
        
        # Determine endpoint category
        category = self._categorize_endpoint(endpoint_path)
        
        # Generate basic test scenarios
        suggestions.extend(self._generate_basic_test_scenarios(endpoint_info, category))
        
        # Add method-specific tests
        suggestions.extend(self._generate_method_specific_tests(endpoint_info))
        
        # Add security tests
        suggestions.extend(self._generate_security_tests(endpoint_info))
        
        # Add error handling tests
        suggestions.extend(self._generate_error_tests(endpoint_info))
        
        return suggestions
    
    def suggest_assertions_for_response(self, response_data: Dict[str, Any], 
                                       request_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate assertion suggestions based on response data"""
        suggestions = []
        
        # Basic status code assertion
        status_code = response_data.get('status_code', 200)
        suggestions.append({
            'type': 'status_code',
            'expected': status_code,
            'description': f'Validate HTTP status code is {status_code}',
            'confidence': 'high',
            'category': 'basic'
        })
        
        # Response time assertion
        response_time = response_data.get('response_time_ms', 0)
        if response_time > 0:
            suggested_timeout = max(1000, int(response_time * 3))  # 3x actual time
            suggestions.append({
                'type': 'response_time',
                'max_ms': suggested_timeout,
                'description': f'Validate response time is under {suggested_timeout}ms',
                'confidence': 'medium',
                'category': 'performance'
            })
        
        # Content type assertion
        headers = response_data.get('headers', {})
        content_type = self._get_header_value(headers, 'content-type')
        if content_type:
            clean_content_type = content_type.split(';')[0].strip()
            suggestions.append({
                'type': 'content_type',
                'expected': clean_content_type,
                'description': f'Validate content type is {clean_content_type}',
                'confidence': 'high',
                'category': 'basic'
            })
        
        # JSON structure assertions
        body = response_data.get('body', {})
        if isinstance(body, dict):
            suggestions.extend(self._suggest_json_assertions(body))
        elif isinstance(body, list):
            suggestions.extend(self._suggest_array_assertions(body))
        
        # Header assertions
        suggestions.extend(self._suggest_header_assertions(headers))
        
        return suggestions
    
    def suggest_next_api_calls(self, current_response: Dict[str, Any], 
                              current_request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest logical next API calls based on current response"""
        suggestions = []
        
        current_method = current_request.get('method', 'GET').upper()
        current_path = current_request.get('url', '')
        response_body = current_response.get('body', {})
        status_code = current_response.get('status_code', 200)
        
        # If current call was successful, suggest related operations
        if 200 <= status_code < 300:
            suggestions.extend(self._suggest_successful_follow_ups(
                current_method, current_path, response_body
            ))
        
        # Suggest resource-based operations
        suggestions.extend(self._suggest_resource_operations(current_path, response_body))
        
        # Suggest authentication flow continuations
        if 'auth' in current_path.lower() or 'login' in current_path.lower():
            suggestions.extend(self._suggest_auth_flow_continuations(response_body))
        
        # Suggest CRUD completions
        suggestions.extend(self._suggest_crud_completions(current_method, current_path))
        
        return suggestions
    
    def suggest_test_improvements(self, test: Dict[str, Any], 
                                 execution_results: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Suggest improvements for existing tests"""
        suggestions = []
        
        # Check for missing assertions
        assertions = test.get('assertions', [])
        if len(assertions) < 3:
            suggestions.append({
                'type': 'add_assertions',
                'priority': 'medium',
                'description': 'Consider adding more assertions for comprehensive validation',
                'suggestion': 'Add response time, content type, and JSON schema assertions'
            })
        
        # Check for missing headers
        headers = test.get('headers', {})
        if not headers.get('Content-Type') and test.get('method') in ['POST', 'PUT', 'PATCH']:
            suggestions.append({
                'type': 'add_headers',
                'priority': 'high',
                'description': 'Add Content-Type header for request body',
                'suggestion': 'Add "Content-Type": "application/json" header'
            })
        
        # Suggest timeout optimization
        if execution_results:
            actual_time = execution_results.get('execution_time', 0) * 1000
            current_timeout = test.get('timeout', 30000)
            if actual_time > 0 and current_timeout > actual_time * 5:
                suggestions.append({
                    'type': 'optimize_timeout',
                    'priority': 'low',
                    'description': f'Consider reducing timeout from {current_timeout}ms to {int(actual_time * 3)}ms',
                    'suggestion': f'Set timeout to {int(actual_time * 3)}ms based on actual response time'
                })
        
        # Suggest error handling tests
        if not any('error' in str(assertion).lower() for assertion in assertions):
            suggestions.append({
                'type': 'add_error_handling',
                'priority': 'medium',
                'description': 'Add negative test cases for error handling',
                'suggestion': 'Create tests for 400, 401, 404, and 500 status codes'
            })
        
        return suggestions
    
    def _categorize_endpoint(self, path: str) -> str:
        """Categorize endpoint based on path patterns"""
        for category, info in self.endpoint_patterns.items():
            for pattern in info['patterns']:
                if pattern in path:
                    return category
        return 'general'
    
    def _generate_basic_test_scenarios(self, endpoint_info: Dict[str, Any], category: str) -> List[Dict[str, Any]]:
        """Generate basic test scenarios for an endpoint"""
        scenarios = []
        path = endpoint_info.get('path', '')
        method = endpoint_info.get('method', 'GET')
        
        # Happy path test
        scenarios.append({
            'name': f'Test {method} {path} - Happy Path',
            'method': method,
            'url': path,
            'description': f'Verify successful {method} request to {path}',
            'assertions': [
                {'type': 'status_code', 'expected': 200},
                {'type': 'response_time', 'max_ms': 5000}
            ],
            'confidence': 'high',
            'category': 'basic'
        })
        
        return scenarios
    
    def _generate_method_specific_tests(self, endpoint_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate method-specific test scenarios"""
        scenarios = []
        method = endpoint_info.get('method', 'GET').upper()
        path = endpoint_info.get('path', '')
        
        if method == 'POST':
            scenarios.append({
                'name': f'Test {method} {path} - Valid Creation',
                'method': method,
                'url': path,
                'description': 'Test successful resource creation',
                'body': {'name': 'Test Resource', 'description': 'Test description'},
                'assertions': [
                    {'type': 'status_code', 'expected': 201},
                    {'type': 'json_path', 'path': 'id', 'description': 'Verify ID is returned'}
                ],
                'confidence': 'high',
                'category': 'creation'
            })
        
        elif method == 'PUT':
            scenarios.append({
                'name': f'Test {method} {path} - Full Update',
                'method': method,
                'url': path,
                'description': 'Test complete resource update',
                'body': {'name': 'Updated Resource', 'description': 'Updated description'},
                'assertions': [
                    {'type': 'status_code', 'expected': 200},
                    {'type': 'json_path', 'path': 'name', 'expected': 'Updated Resource'}
                ],
                'confidence': 'medium',
                'category': 'update'
            })
        
        elif method == 'DELETE':
            scenarios.append({
                'name': f'Test {method} {path} - Successful Deletion',
                'method': method,
                'url': path,
                'description': 'Test resource deletion',
                'assertions': [
                    {'type': 'status_code', 'expected': 204}
                ],
                'confidence': 'medium',
                'category': 'deletion'
            })
        
        return scenarios
    
    def _generate_security_tests(self, endpoint_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate security-focused test scenarios"""
        scenarios = []
        path = endpoint_info.get('path', '')
        method = endpoint_info.get('method', 'GET')
        
        # Authentication test
        scenarios.append({
            'name': f'Test {method} {path} - No Authentication',
            'method': method,
            'url': path,
            'description': 'Test endpoint without authentication',
            'headers': {},  # No auth headers
            'assertions': [
                {'type': 'status_code', 'expected': 401}
            ],
            'confidence': 'medium',
            'category': 'security'
        })
        
        # Invalid token test
        scenarios.append({
            'name': f'Test {method} {path} - Invalid Token',
            'method': method,
            'url': path,
            'description': 'Test endpoint with invalid authentication',
            'headers': {'Authorization': 'Bearer invalid_token'},
            'assertions': [
                {'type': 'status_code', 'expected': 401}
            ],
            'confidence': 'medium',
            'category': 'security'
        })
        
        return scenarios
    
    def _generate_error_tests(self, endpoint_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate error handling test scenarios"""
        scenarios = []
        path = endpoint_info.get('path', '')
        method = endpoint_info.get('method', 'GET')
        
        # Invalid input test (for POST/PUT methods)
        if method in ['POST', 'PUT', 'PATCH']:
            scenarios.append({
                'name': f'Test {method} {path} - Invalid Input',
                'method': method,
                'url': path,
                'description': 'Test endpoint with invalid input data',
                'body': {'invalid_field': 'invalid_value'},
                'assertions': [
                    {'type': 'status_code', 'expected': 400}
                ],
                'confidence': 'medium',
                'category': 'error_handling'
            })
        
        # Resource not found test (for GET/PUT/DELETE with ID)
        if '{id}' in path or path.endswith('/1') or path.endswith('/123'):
            scenarios.append({
                'name': f'Test {method} {path} - Resource Not Found',
                'method': method,
                'url': path.replace('{id}', '999999'),
                'description': 'Test endpoint with non-existent resource',
                'assertions': [
                    {'type': 'status_code', 'expected': 404}
                ],
                'confidence': 'high',
                'category': 'error_handling'
            })
        
        return scenarios
    
    def _suggest_json_assertions(self, json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest assertions for JSON response data"""
        suggestions = []
        
        # Check for common important fields
        important_fields = ['id', 'uuid', 'status', 'success', 'error', 'message']
        
        for field in important_fields:
            if field in json_data:
                suggestions.append({
                    'type': 'json_path',
                    'path': field,
                    'expected': json_data[field],
                    'description': f'Validate {field} field value',
                    'confidence': 'medium',
                    'category': 'data_validation'
                })
        
        # Suggest schema validation for complex objects
        if len(json_data) > 3:
            suggestions.append({
                'type': 'json_schema',
                'schema': self._generate_simple_schema(json_data),
                'description': 'Validate response structure matches expected schema',
                'confidence': 'low',
                'category': 'structure_validation'
            })
        
        return suggestions
    
    def _suggest_array_assertions(self, array_data: List[Any]) -> List[Dict[str, Any]]:
        """Suggest assertions for array response data"""
        suggestions = []
        
        # Array length assertion
        suggestions.append({
            'type': 'array_length',
            'path': '',
            'expected': len(array_data),
            'description': f'Validate array contains {len(array_data)} items',
            'confidence': 'low',
            'category': 'data_validation'
        })
        
        # If array has objects, suggest validating first item structure
        if array_data and isinstance(array_data[0], dict):
            suggestions.append({
                'type': 'json_path',
                'path': '0',
                'description': 'Validate first array item exists',
                'confidence': 'medium',
                'category': 'structure_validation'
            })
        
        return suggestions
    
    def _suggest_header_assertions(self, headers: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest assertions for response headers"""
        suggestions = []
        
        # Security headers
        security_headers = ['x-frame-options', 'x-content-type-options', 'x-xss-protection']
        for header in security_headers:
            if header in headers or header.title() in headers:
                suggestions.append({
                    'type': 'header',
                    'header': header,
                    'expected': headers.get(header, headers.get(header.title(), '')),
                    'description': f'Validate security header {header}',
                    'confidence': 'low',
                    'category': 'security'
                })
        
        return suggestions
    
    def _suggest_successful_follow_ups(self, method: str, path: str, response_body: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest follow-up calls after successful operation"""
        suggestions = []
        
        # If response contains an ID, suggest GET request
        if isinstance(response_body, dict) and ('id' in response_body or 'uuid' in response_body):
            resource_id = response_body.get('id') or response_body.get('uuid')
            suggestions.append({
                'name': f'Get Created Resource',
                'method': 'GET',
                'url': f"{path}/{resource_id}",
                'description': f'Retrieve the resource that was just created/modified',
                'confidence': 'high',
                'category': 'follow_up'
            })
        
        # If this was a POST (creation), suggest listing the collection
        if method == 'POST':
            collection_path = path.rstrip('/').rstrip('s') + 's'  # Simple pluralization
            suggestions.append({
                'name': 'List Collection',
                'method': 'GET',
                'url': collection_path,
                'description': 'List the collection to verify the new resource',
                'confidence': 'medium',
                'category': 'follow_up'
            })
        
        return suggestions
    
    def _suggest_resource_operations(self, path: str, response_body: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest resource-based operations"""
        suggestions = []
        
        # Extract resource type from path
        path_parts = path.strip('/').split('/')
        if path_parts:
            resource_type = path_parts[-1] if not path_parts[-1].isdigit() else path_parts[-2]
            
            # Suggest CRUD operations for the resource
            base_path = f"/{resource_type}"
            
            crud_ops = [
                {'name': f'Create {resource_type.title()}', 'method': 'POST', 'path': base_path},
                {'name': f'List {resource_type.title()}s', 'method': 'GET', 'path': f"{base_path}s"},
                {'name': f'Update {resource_type.title()}', 'method': 'PUT', 'path': f"{base_path}/1"},
                {'name': f'Delete {resource_type.title()}', 'method': 'DELETE', 'path': f"{base_path}/1"}
            ]
            
            for op in crud_ops:
                suggestions.append({
                    'name': op['name'],
                    'method': op['method'],
                    'url': op['path'],
                    'description': f"{op['name']} operation",
                    'confidence': 'medium',
                    'category': 'crud'
                })
        
        return suggestions
    
    def _suggest_auth_flow_continuations(self, response_body: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest authentication flow continuations"""
        suggestions = []
        
        # If login was successful and token returned, suggest protected operations
        if isinstance(response_body, dict) and ('token' in response_body or 'access_token' in response_body):
            token = response_body.get('token') or response_body.get('access_token')
            
            suggestions.extend([
                {
                    'name': 'Get User Profile',
                    'method': 'GET',
                    'url': '/profile',
                    'headers': {'Authorization': f'Bearer {token}'},
                    'description': 'Access protected user profile endpoint',
                    'confidence': 'high',
                    'category': 'authenticated'
                },
                {
                    'name': 'Refresh Token',
                    'method': 'POST',
                    'url': '/auth/refresh',
                    'headers': {'Authorization': f'Bearer {token}'},
                    'description': 'Refresh the authentication token',
                    'confidence': 'medium',
                    'category': 'authenticated'
                }
            ])
        
        return suggestions
    
    def _suggest_crud_completions(self, method: str, path: str) -> List[Dict[str, Any]]:
        """Suggest completing CRUD operations"""
        suggestions = []
        
        # Extract base resource path
        if '/' in path:
            parts = path.strip('/').split('/')
            if parts[-1].isdigit():  # Path ends with ID
                base_path = '/' + '/'.join(parts[:-1])
                resource_id = parts[-1]
            else:
                base_path = path
                resource_id = '1'
        else:
            base_path = path
            resource_id = '1'
        
        # Suggest missing CRUD operations
        crud_suggestions = []
        
        if method != 'GET':
            crud_suggestions.append({
                'name': 'Read Resource',
                'method': 'GET',
                'url': f"{base_path}/{resource_id}",
                'description': 'Retrieve the resource'
            })
        
        if method != 'POST':
            crud_suggestions.append({
                'name': 'Create Resource',
                'method': 'POST',
                'url': base_path,
                'description': 'Create a new resource'
            })
        
        if method != 'PUT':
            crud_suggestions.append({
                'name': 'Update Resource',
                'method': 'PUT',
                'url': f"{base_path}/{resource_id}",
                'description': 'Update the resource'
            })
        
        if method != 'DELETE':
            crud_suggestions.append({
                'name': 'Delete Resource',
                'method': 'DELETE',
                'url': f"{base_path}/{resource_id}",
                'description': 'Delete the resource'
            })
        
        for suggestion in crud_suggestions:
            suggestion.update({
                'confidence': 'medium',
                'category': 'crud_completion'
            })
            suggestions.append(suggestion)
        
        return suggestions[:2]  # Limit to 2 suggestions to avoid overwhelming
    
    def _get_header_value(self, headers: Dict[str, Any], header_name: str) -> Optional[str]:
        """Get header value with case-insensitive lookup"""
        for key, value in headers.items():
            if key.lower() == header_name.lower():
                return value
        return None
    
    def _generate_simple_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a simple JSON schema for data"""
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for key, value in data.items():
            if isinstance(value, str):
                schema["properties"][key] = {"type": "string"}
            elif isinstance(value, int):
                schema["properties"][key] = {"type": "number"}
            elif isinstance(value, bool):
                schema["properties"][key] = {"type": "boolean"}
            elif isinstance(value, list):
                schema["properties"][key] = {"type": "array"}
            elif isinstance(value, dict):
                schema["properties"][key] = {"type": "object"}
            
            # Mark non-null values as required
            if value is not None:
                schema["required"].append(key)
        
        return schema
