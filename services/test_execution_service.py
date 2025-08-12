import asyncio
import httpx
import os
from typing import Dict, List, Any, Optional
import time
import json
from urllib.parse import urljoin

class TestExecutionService:
    def __init__(self):
        self.timeout = int(os.getenv("DEFAULT_TIMEOUT", "30"))
        self.max_concurrent = int(os.getenv("MAX_CONCURRENT_TESTS", "5"))
        self.session = None
    
    async def execute_tests(self, tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute a list of API tests and return results"""
        results = []
        
        # Group tests by base URL if possible
        test_groups = self._group_tests_by_base_url(tests)
        
        # Execute tests in batches to respect concurrency limits
        for base_url, test_group in test_groups.items():
            batch_results = await self._execute_test_batch(test_group, base_url)
            results.extend(batch_results)
        
        return results
    
    def _group_tests_by_base_url(self, tests: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group tests by their base URL to optimize execution"""
        # For now, we'll assume all tests are for the same service
        # In a real implementation, you might detect base URLs from endpoints
        return {"default": tests}
    
    async def _execute_test_batch(self, tests: List[Dict[str, Any]], base_url: str) -> List[Dict[str, Any]]:
        """Execute a batch of tests for a specific base URL"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def execute_single_test(test: Dict[str, Any]) -> Dict[str, Any]:
            async with semaphore:
                return await self._execute_single_test(test, base_url)
        
        # Execute tests concurrently
        tasks = [execute_single_test(test) for test in tests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(self._create_error_result(tests[i], str(result)))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _execute_single_test(self, test: Dict[str, Any], base_url: str) -> Dict[str, Any]:
        """Execute a single API test"""
        start_time = time.time()
        
        try:
            # Prepare request details
            method = test.get("method", "GET").upper()
            endpoint = test.get("endpoint", "/")
            headers = test.get("headers", {})
            body = test.get("body")
            expected_status = test.get("expected_status", 200)
            
            # Try to determine the actual API URL
            test_url = await self._determine_test_url(endpoint, test, base_url)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Execute the HTTP request
                response = await self._make_request(client, method, test_url, headers, body)
                
                # Analyze the response
                execution_time = time.time() - start_time
                result = await self._analyze_response(test, response, execution_time)
                
                return result
                
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_error_result(test, str(e), execution_time)
    
    async def _determine_test_url(self, endpoint: str, test: Dict[str, Any], base_url: str) -> str:
        """Determine the actual URL to test"""
        # Try common localhost patterns for development testing
        common_urls = [
            "http://localhost:8000",
            "http://localhost:3000", 
            "http://localhost:5000",
            "http://localhost:8080",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5000"
        ]
        
        # If endpoint starts with http, use it directly
        if endpoint.startswith("http"):
            return endpoint
        
        # Try to find a working local server
        for base in common_urls:
            test_url = urljoin(base, endpoint.lstrip("/"))
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(base + "/health", timeout=2)
                    if response.status_code < 500:  # Server is responding
                        return test_url
            except:
                continue
        
        # Fallback to first common URL
        return urljoin(common_urls[0], endpoint.lstrip("/"))
    
    async def _make_request(self, client: httpx.AsyncClient, method: str, url: str, headers: Dict, body: Any) -> httpx.Response:
        """Make HTTP request with proper error handling"""
        # Prepare headers
        request_headers = {"User-Agent": "AgentAPI-Testing-Platform/1.0"}
        request_headers.update(headers)
        
        # Prepare body
        if body is not None and method in ["POST", "PUT", "PATCH"]:
            if isinstance(body, dict):
                request_headers["Content-Type"] = "application/json"
                body = json.dumps(body)
        
        # Make the request
        response = await client.request(
            method=method,
            url=url,
            headers=request_headers,
            content=body if body else None
        )
        
        return response
    
    async def _analyze_response(self, test: Dict[str, Any], response: httpx.Response, execution_time: float) -> Dict[str, Any]:
        """Analyze the API response and compare with expectations"""
        expected_status = test.get("expected_status", 200)
        
        # Basic response data
        result = {
            "test": test,
            "success": False,
            "execution_time": execution_time,
            "response": {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "url": str(response.url)
            },
            "assertions": [],
            "errors": []
        }
        
        # Get response body
        try:
            response_text = response.text
            result["response"]["body"] = response_text
            
            # Try to parse JSON
            if response.headers.get("content-type", "").startswith("application/json"):
                try:
                    result["response"]["json"] = response.json()
                except:
                    pass
        except Exception as e:
            result["errors"].append(f"Failed to read response body: {str(e)}")
        
        # Check status code
        status_assertion = {
            "name": "status_code",
            "expected": expected_status,
            "actual": response.status_code,
            "passed": response.status_code == expected_status
        }
        result["assertions"].append(status_assertion)
        
        # Check if response is valid JSON for JSON endpoints
        if test.get("headers", {}).get("Content-Type") == "application/json":
            json_assertion = {
                "name": "valid_json_response",
                "expected": True,
                "actual": "json" in result["response"],
                "passed": "json" in result["response"]
            }
            result["assertions"].append(json_assertion)
        
        # Check response time (reasonable threshold)
        time_assertion = {
            "name": "response_time",
            "expected": "< 10 seconds",
            "actual": f"{execution_time:.2f} seconds",
            "passed": execution_time < 10.0
        }
        result["assertions"].append(time_assertion)
        
        # Overall success
        result["success"] = all(assertion["passed"] for assertion in result["assertions"])
        
        return result
    
    def _create_error_result(self, test: Dict[str, Any], error_message: str, execution_time: float = 0) -> Dict[str, Any]:
        """Create error result for failed test execution"""
        return {
            "test": test,
            "success": False,
            "execution_time": execution_time,
            "response": None,
            "assertions": [],
            "errors": [error_message],
            "error_type": "execution_error"
        }