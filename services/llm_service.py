import os
import openai
from typing import Dict, List, Any, Optional
import json
import re

class LLMService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    async def generate_test_prompts(self, repo_data: Dict[str, Any], user_description: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate API test prompts using LLM based on repository analysis"""
        
        # Prepare context for LLM
        context = self._prepare_repository_context(repo_data)
        
        # Create the prompt for LLM
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_user_prompt(context, user_description)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse the LLM response
            llm_response = response.choices[0].message.content
            if llm_response:
                test_prompts = self._parse_llm_response(llm_response, repo_data)
            else:
                test_prompts = self._generate_fallback_tests(repo_data)
            
            return test_prompts
            
        except Exception as e:
            # Fallback to pattern-based generation if LLM fails
            return self._generate_fallback_tests(repo_data)
    
    def _prepare_repository_context(self, repo_data: Dict[str, Any]) -> str:
        """Prepare repository context for LLM"""
        context_parts = []
        
        # Repository metadata
        repo_info = repo_data.get("repository", {})
        context_parts.append(f"Repository: {repo_info.get('name', 'Unknown')}")
        context_parts.append(f"Description: {repo_info.get('description', 'No description')}")
        context_parts.append(f"Language: {repo_info.get('language', 'Unknown')}")
        
        # Project structure
        structure = repo_data.get("structure", {})
        context_parts.append(f"Project Type: {structure.get('type', 'unknown')}")
        context_parts.append(f"Framework: {structure.get('framework', 'unknown')}")
        
        # Detected endpoints
        endpoints = repo_data.get("api_endpoints", [])
        if endpoints:
            context_parts.append("Detected API Endpoints:")
            for endpoint in endpoints[:10]:  # Limit to first 10
                context_parts.append(f"  {endpoint.get('method', 'GET')} {endpoint.get('path', '/')}")
        
        # Key file contents (truncated)
        files = repo_data.get("files", {})
        for filename, content in files.items():
            if content and len(content) > 0:
                truncated_content = content[:1000] + "..." if len(content) > 1000 else content
                context_parts.append(f"\n--- {filename} ---")
                context_parts.append(truncated_content)
        
        return "\n".join(context_parts)
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for LLM"""
        return """You are an expert API testing assistant. Your task is to analyze a GitHub repository and generate comprehensive API test scenarios.

Based on the repository information provided, generate a list of API tests that should be performed. Each test should include:

1. Test name and description
2. HTTP method (GET, POST, PUT, DELETE, etc.)
3. Endpoint URL/path
4. Required headers (if any)
5. Request body/payload (if applicable)
6. Expected response status code
7. Expected response structure/validation
8. Test category (authentication, CRUD operations, edge cases, etc.)

Focus on:
- Testing all discovered endpoints
- Common API testing scenarios (CRUD operations, authentication, validation)
- Edge cases and error handling
- Different data types and formats
- Security considerations

Return your response as a JSON array of test objects. Each test object should have the structure:
{
  "name": "Test name",
  "description": "Detailed test description",
  "method": "HTTP method",
  "endpoint": "/api/path",
  "headers": {"key": "value"},
  "body": {"key": "value"} or null,
  "expected_status": 200,
  "expected_response": {"structure": "description"},
  "category": "test category",
  "priority": "high|medium|low"
}"""
    
    def _create_user_prompt(self, context: str, user_description: Optional[str]) -> str:
        """Create user prompt with repository context"""
        prompt = f"""Analyze this repository and generate comprehensive API tests:

{context}

"""
        
        if user_description:
            prompt += f"Additional testing requirements: {user_description}\n\n"
        
        prompt += """Please generate a comprehensive set of API tests for this repository. Include tests for:
1. All detected endpoints
2. Authentication/authorization (if applicable)
3. CRUD operations
4. Input validation and error handling
5. Edge cases and boundary conditions

Return the tests as a valid JSON array."""
        
        return prompt
    
    def _parse_llm_response(self, response: str, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse LLM response and extract test definitions"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                tests = json.loads(json_str)
                
                # Validate and enhance test definitions
                validated_tests = []
                for test in tests:
                    if self._validate_test_definition(test):
                        enhanced_test = self._enhance_test_definition(test, repo_data)
                        validated_tests.append(enhanced_test)
                
                return validated_tests
            else:
                raise ValueError("No valid JSON found in LLM response")
                
        except Exception as e:
            print(f"Failed to parse LLM response: {e}")
            return self._generate_fallback_tests(repo_data)
    
    def _validate_test_definition(self, test: Dict[str, Any]) -> bool:
        """Validate that test definition has required fields"""
        required_fields = ["name", "method", "endpoint"]
        return all(field in test for field in required_fields)
    
    def _enhance_test_definition(self, test: Dict[str, Any], repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance test definition with additional metadata"""
        enhanced = test.copy()
        
        # Set defaults
        enhanced.setdefault("description", f"Test {test['name']}")
        enhanced.setdefault("headers", {})
        enhanced.setdefault("body", None)
        enhanced.setdefault("expected_status", 200)
        enhanced.setdefault("expected_response", {})
        enhanced.setdefault("category", "general")
        enhanced.setdefault("priority", "medium")
        
        # Add repository context
        enhanced["repository"] = repo_data.get("repository", {}).get("name", "unknown")
        enhanced["generated_by"] = "llm"
        
        return enhanced
    
    def _generate_fallback_tests(self, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic tests based on detected endpoints when LLM fails"""
        tests = []
        endpoints = repo_data.get("api_endpoints", [])
        
        for i, endpoint in enumerate(endpoints):
            test = {
                "name": f"Test {endpoint.get('method', 'GET')} {endpoint.get('path', '/')}",
                "description": f"Basic test for {endpoint.get('method', 'GET')} endpoint {endpoint.get('path', '/')}",
                "method": endpoint.get("method", "GET"),
                "endpoint": endpoint.get("path", "/"),
                "headers": {"Content-Type": "application/json"},
                "body": None,
                "expected_status": 200,
                "expected_response": {"type": "json"},
                "category": "endpoint_test",
                "priority": "medium",
                "repository": repo_data.get("repository", {}).get("name", "unknown"),
                "generated_by": "fallback"
            }
            
            # Add request body for POST/PUT methods
            if endpoint.get("method", "GET").upper() in ["POST", "PUT", "PATCH"]:
                test["body"] = {"data": "test_data"}
            
            tests.append(test)
        
        # Add some common API tests if no endpoints detected
        if not tests:
            common_tests = [
                {
                    "name": "Health Check",
                    "description": "Test basic application health/status endpoint",
                    "method": "GET",
                    "endpoint": "/health",
                    "headers": {},
                    "body": None,
                    "expected_status": 200,
                    "expected_response": {"status": "ok"},
                    "category": "health",
                    "priority": "high",
                    "repository": repo_data.get("repository", {}).get("name", "unknown"),
                    "generated_by": "fallback"
                },
                {
                    "name": "Root Endpoint",
                    "description": "Test root endpoint response",
                    "method": "GET",
                    "endpoint": "/",
                    "headers": {},
                    "body": None,
                    "expected_status": 200,
                    "expected_response": {"type": "any"},
                    "category": "basic",
                    "priority": "medium",
                    "repository": repo_data.get("repository", {}).get("name", "unknown"),
                    "generated_by": "fallback"
                }
            ]
            tests.extend(common_tests)
        
        return tests