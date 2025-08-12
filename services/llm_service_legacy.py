# Updated LLM Service for Python 3.13 compatibility with older OpenAI API
import os
import json
import logging
from typing import List, Dict, Any, Optional
import openai

# Configure OpenAI API key for older openai package
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMServiceLegacy:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Check if API key is configured
        if not openai.api_key:
            self.logger.warning("OpenAI API key not configured. LLM features will be limited.")
    
    async def generate_tests_from_analysis(self, analysis_data: Dict[str, Any], test_description: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate API tests using OpenAI GPT based on repository analysis"""
        
        if not openai.api_key:
            return self._generate_fallback_tests(analysis_data)
        
        try:
            # Create prompt for test generation
            prompt = self._create_test_generation_prompt(analysis_data, test_description)
            
            # Call OpenAI API using legacy format
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7,
                stop=None
            )
            
            # Parse and structure the response
            generated_content = response.choices[0].text.strip()
            tests = self._parse_generated_tests(generated_content)
            
            # Add metadata to tests
            for test in tests:
                test.update({
                    "generated_by": "openai_gpt",
                    "model": "gpt-3.5-turbo-instruct",
                    "analysis_based": True
                })
            
            self.logger.info(f"Generated {len(tests)} tests using OpenAI")
            return tests
            
        except Exception as e:
            self.logger.error(f"OpenAI test generation failed: {str(e)}")
            return self._generate_fallback_tests(analysis_data)
    
    def _create_test_generation_prompt(self, analysis_data: Dict[str, Any], test_description: Optional[str] = None) -> str:
        """Create a prompt for the LLM to generate API tests"""
        
        repository_info = analysis_data.get('repository_analysis', {})
        code_analysis = analysis_data.get('code_analysis', {})
        detected_endpoints = code_analysis.get('detected_endpoints', [])
        
        prompt = f"""
Generate comprehensive API tests for a {repository_info.get('language', 'web')} application using the {repository_info.get('framework', 'unknown')} framework.

Repository Information:
- Framework: {repository_info.get('framework', 'Unknown')}
- Language: {repository_info.get('language', 'Unknown')}
- Main Files: {', '.join(repository_info.get('main_files', [])[:5])}

Detected API Endpoints:
{self._format_endpoints_for_prompt(detected_endpoints)}

{f"Additional Requirements: {test_description}" if test_description else ""}

Generate API tests in JSON format with the following structure for each test:
{{
  "name": "descriptive test name",
  "method": "GET|POST|PUT|DELETE",
  "endpoint": "/api/path",
  "description": "what this test validates",
  "headers": {{"Content-Type": "application/json"}},
  "body": {{}} or null,
  "expected_status": 200,
  "assertions": [
    {{"type": "status_code", "expected": 200}},
    {{"type": "response_time", "max_ms": 5000}},
    {{"type": "content_type", "expected": "application/json"}}
  ]
}}

Focus on:
1. CRUD operations for main entities
2. Authentication endpoints if detected
3. Error handling scenarios
4. Input validation tests
5. Performance checks

Generate 5-10 comprehensive tests. Return only valid JSON array of test objects.
"""
        return prompt
    
    def _format_endpoints_for_prompt(self, endpoints: List[str]) -> str:
        """Format detected endpoints for the prompt"""
        if not endpoints:
            return "No endpoints detected - generate generic REST API tests"
        
        formatted = []
        for endpoint in endpoints[:10]:  # Limit to avoid token limits
            formatted.append(f"- {endpoint}")
        
        return "\n".join(formatted)
    
    def _parse_generated_tests(self, generated_content: str) -> List[Dict[str, Any]]:
        """Parse the generated content and extract test definitions"""
        try:
            # Try to parse as JSON first
            tests = json.loads(generated_content)
            if isinstance(tests, list):
                return tests
            elif isinstance(tests, dict):
                return [tests]
        except json.JSONDecodeError:
            pass
        
        # If JSON parsing fails, try to extract JSON from text
        import re
        json_pattern = r'\[.*?\]'
        matches = re.findall(json_pattern, generated_content, re.DOTALL)
        
        for match in matches:
            try:
                tests = json.loads(match)
                if isinstance(tests, list):
                    return tests
            except json.JSONDecodeError:
                continue
        
        # If all parsing fails, return fallback tests
        self.logger.warning("Failed to parse generated tests, using fallback")
        return []
    
    def _generate_fallback_tests(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic fallback tests when LLM is not available"""
        code_analysis = analysis_data.get('code_analysis', {})
        detected_endpoints = code_analysis.get('detected_endpoints', [])
        
        tests = []
        
        # Basic health check test
        tests.append({
            "name": "Health Check",
            "method": "GET",
            "endpoint": "/health",
            "description": "Check if API is responding",
            "headers": {"Content-Type": "application/json"},
            "body": None,
            "expected_status": 200,
            "assertions": [
                {"type": "status_code", "expected": 200},
                {"type": "response_time", "max_ms": 5000}
            ],
            "generated_by": "fallback_pattern",
            "analysis_based": True
        })
        
        # Generate tests for detected endpoints
        for endpoint in detected_endpoints[:5]:
            method = "GET"  # Default to GET for safety
            
            # Try to infer method from endpoint pattern
            if any(word in endpoint.lower() for word in ['create', 'post', 'add']):
                method = "POST"
            elif any(word in endpoint.lower() for word in ['update', 'put', 'edit']):
                method = "PUT"
            elif any(word in endpoint.lower() for word in ['delete', 'remove']):
                method = "DELETE"
            
            test = {
                "name": f"Test {endpoint}",
                "method": method,
                "endpoint": endpoint,
                "description": f"Test {method} request to {endpoint}",
                "headers": {"Content-Type": "application/json"},
                "body": None if method == "GET" else {},
                "expected_status": 200,
                "assertions": [
                    {"type": "status_code", "expected": 200},
                    {"type": "response_time", "max_ms": 5000}
                ],
                "generated_by": "fallback_pattern",
                "analysis_based": True
            }
            tests.append(test)
        
        # Add some common REST endpoints if none detected
        if not detected_endpoints:
            common_endpoints = [
                {"endpoint": "/api/users", "method": "GET", "name": "List Users"},
                {"endpoint": "/api/users", "method": "POST", "name": "Create User"},
                {"endpoint": "/api/users/1", "method": "GET", "name": "Get User"},
                {"endpoint": "/api/users/1", "method": "PUT", "name": "Update User"},
                {"endpoint": "/api/users/1", "method": "DELETE", "name": "Delete User"}
            ]
            
            for common in common_endpoints:
                test = {
                    "name": common["name"],
                    "method": common["method"],
                    "endpoint": common["endpoint"],
                    "description": f"Test {common['method']} request to {common['endpoint']}",
                    "headers": {"Content-Type": "application/json"},
                    "body": None if common["method"] == "GET" else {"test": "data"},
                    "expected_status": 200,
                    "assertions": [
                        {"type": "status_code", "expected": 200},
                        {"type": "response_time", "max_ms": 5000}
                    ],
                    "generated_by": "fallback_pattern",
                    "analysis_based": False
                }
                tests.append(test)
        
        return tests
    
    def get_test_generation_summary(self, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of the test generation process"""
        total_tests = len(tests)
        test_types = {}
        generated_by = {}
        
        for test in tests:
            method = test.get('method', 'Unknown')
            test_types[method] = test_types.get(method, 0) + 1
            
            generator = test.get('generated_by', 'Unknown')
            generated_by[generator] = generated_by.get(generator, 0) + 1
        
        return {
            "total_tests_generated": total_tests,
            "test_types_breakdown": test_types,
            "generation_methods": generated_by,
            "llm_available": bool(openai.api_key),
            "coverage_areas": [
                "CRUD operations",
                "Error handling", 
                "Performance validation",
                "Authentication (if detected)"
            ]
        }