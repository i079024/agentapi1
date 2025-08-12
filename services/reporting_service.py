from typing import Dict, List, Any
from datetime import datetime
import json

class ReportingService:
    def __init__(self):
        pass
    
    def create_analysis_report(self, repo_data: Dict[str, Any], test_prompts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a detailed analysis report of the repository and generated tests"""
        
        repository = repo_data.get("repository", {})
        structure = repo_data.get("structure", {})
        endpoints = repo_data.get("api_endpoints", [])
        files = repo_data.get("files", {})
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "repository_analysis": {
                "name": repository.get("name", "Unknown"),
                "description": repository.get("description", "No description available"),
                "language": repository.get("language", "Unknown"),
                "framework": structure.get("framework", "Unknown"),
                "project_type": structure.get("type", "Unknown"),
                "url": repository.get("url", ""),
                "branch": repo_data.get("branch", "main")
            },
            "code_analysis": {
                "files_analyzed": len(files),
                "key_files": list(files.keys()),
                "detected_endpoints": len(endpoints),
                "endpoint_details": endpoints
            },
            "test_generation": {
                "total_tests_generated": len(test_prompts),
                "test_categories": self._categorize_tests(test_prompts),
                "generation_method": self._determine_generation_method(test_prompts),
                "test_coverage": self._analyze_test_coverage(test_prompts, endpoints)
            },
            "recommendations": self._generate_recommendations(repo_data, test_prompts)
        }
        
        return report
    
    def create_execution_report(self, execution_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a detailed execution report of test results"""
        
        total_tests = len(execution_results)
        passed_tests = [r for r in execution_results if r.get("success", False)]
        failed_tests = [r for r in execution_results if not r.get("success", False)]
        
        # Calculate statistics
        avg_response_time = 0
        if execution_results:
            total_time = sum(r.get("execution_time", 0) for r in execution_results)
            avg_response_time = total_time / len(execution_results)
        
        # Analyze failure patterns
        failure_analysis = self._analyze_failures(failed_tests)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "execution_summary": {
                "total_tests": total_tests,
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "success_rate": (len(passed_tests) / total_tests * 100) if total_tests > 0 else 0,
                "average_response_time": avg_response_time
            },
            "test_results": {
                "passed_tests": self._summarize_test_results(passed_tests),
                "failed_tests": self._summarize_test_results(failed_tests)
            },
            "failure_analysis": failure_analysis,
            "performance_metrics": self._analyze_performance(execution_results),
            "recommendations": self._generate_execution_recommendations(execution_results)
        }
        
        return report
    
    def create_full_report(self, analysis_response: Dict[str, Any], execution_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive report combining analysis and execution results"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "report_type": "comprehensive_api_testing_report",
            "repository": analysis_response.get("repository", "Unknown"),
            "branch": analysis_response.get("branch", "Unknown"),
            "summary": {
                "repository_analyzed": True,
                "tests_generated": len(analysis_response.get("generated_tests", [])),
                "tests_executed": execution_response.get("summary", {}).get("total_tests", 0),
                "overall_success_rate": execution_response.get("summary", {}).get("passed", 0) / max(execution_response.get("summary", {}).get("total_tests", 1), 1) * 100
            },
            "analysis_phase": analysis_response.get("analysis_report", {}),
            "execution_phase": execution_response.get("execution_report", {}),
            "overall_recommendations": self._generate_overall_recommendations(analysis_response, execution_response),
            "next_steps": self._suggest_next_steps(analysis_response, execution_response)
        }
        
        return report
    
    def _categorize_tests(self, tests: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize tests by type"""
        categories = {}
        for test in tests:
            category = test.get("category", "general")
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _determine_generation_method(self, tests: List[Dict[str, Any]]) -> str:
        """Determine how tests were generated"""
        if not tests:
            return "none"
        
        methods = set(test.get("generated_by", "unknown") for test in tests)
        if "llm" in methods:
            return "llm_assisted"
        elif "fallback" in methods:
            return "pattern_based"
        else:
            return "unknown"
    
    def _analyze_test_coverage(self, tests: List[Dict[str, Any]], endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze test coverage against detected endpoints"""
        tested_endpoints = set()
        for test in tests:
            endpoint = test.get("endpoint", "")
            method = test.get("method", "GET")
            tested_endpoints.add(f"{method} {endpoint}")
        
        detected_endpoints = set()
        for endpoint in endpoints:
            method = endpoint.get("method", "GET")
            path = endpoint.get("path", "")
            detected_endpoints.add(f"{method} {path}")
        
        coverage = {
            "detected_endpoints": len(detected_endpoints),
            "tested_endpoints": len(tested_endpoints),
            "coverage_percentage": 0,
            "untested_endpoints": list(detected_endpoints - tested_endpoints),
            "additional_tests": list(tested_endpoints - detected_endpoints)
        }
        
        if detected_endpoints:
            covered = len(detected_endpoints & tested_endpoints)
            coverage["coverage_percentage"] = (covered / len(detected_endpoints)) * 100
        
        return coverage
    
    def _generate_recommendations(self, repo_data: Dict[str, Any], tests: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        endpoints = repo_data.get("api_endpoints", [])
        structure = repo_data.get("structure", {})
        
        if not endpoints:
            recommendations.append("No API endpoints detected. Consider adding endpoint detection for your specific framework.")
        
        if len(tests) < 5:
            recommendations.append("Limited test coverage. Consider adding more comprehensive test scenarios.")
        
        if structure.get("framework") == "unknown":
            recommendations.append("Framework not detected. Manual test configuration may be required.")
        
        # Check for authentication patterns
        auth_tests = [t for t in tests if "auth" in t.get("category", "").lower()]
        if not auth_tests:
            recommendations.append("No authentication tests generated. Consider adding security testing.")
        
        return recommendations
    
    def _analyze_failures(self, failed_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in test failures"""
        if not failed_tests:
            return {"total_failures": 0, "patterns": []}
        
        # Group failures by type
        failure_types = {}
        status_codes = {}
        
        for test in failed_tests:
            errors = test.get("errors", [])
            if errors:
                error_type = "execution_error"
                failure_types[error_type] = failure_types.get(error_type, 0) + 1
            
            response = test.get("response")
            if response:
                status = response.get("status_code", 0)
                status_codes[status] = status_codes.get(status, 0) + 1
        
        patterns = []
        if 404 in status_codes:
            patterns.append(f"{status_codes[404]} tests failed with 404 - endpoints may not exist")
        if 500 in status_codes:
            patterns.append(f"{status_codes[500]} tests failed with 500 - server errors detected")
        if "execution_error" in failure_types:
            patterns.append(f"{failure_types['execution_error']} tests failed to execute - connectivity issues")
        
        return {
            "total_failures": len(failed_tests),
            "failure_types": failure_types,
            "status_codes": status_codes,
            "patterns": patterns
        }
    
    def _summarize_test_results(self, test_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create summary of test results"""
        summaries = []
        for result in test_results:
            test = result.get("test", {})
            summary = {
                "name": test.get("name", "Unknown Test"),
                "method": test.get("method", "GET"),
                "endpoint": test.get("endpoint", "/"),
                "success": result.get("success", False),
                "execution_time": result.get("execution_time", 0),
                "status_code": result.get("response", {}).get("status_code") if result.get("response") else None
            }
            summaries.append(summary)
        return summaries
    
    def _analyze_performance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance metrics from test results"""
        if not results:
            return {}
        
        times = [r.get("execution_time", 0) for r in results]
        times.sort()
        
        return {
            "min_response_time": min(times),
            "max_response_time": max(times),
            "avg_response_time": sum(times) / len(times),
            "median_response_time": times[len(times) // 2],
            "slow_tests": [r for r in results if r.get("execution_time", 0) > 5.0]
        }
    
    def _generate_execution_recommendations(self, results: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on execution results"""
        recommendations = []
        
        failed_results = [r for r in results if not r.get("success", False)]
        slow_results = [r for r in results if r.get("execution_time", 0) > 5.0]
        
        if failed_results:
            failure_rate = len(failed_results) / len(results) * 100
            recommendations.append(f"High failure rate ({failure_rate:.1f}%). Review API availability and endpoint configurations.")
        
        if slow_results:
            recommendations.append(f"{len(slow_results)} tests had slow response times (>5s). Consider performance optimization.")
        
        # Check for 404 errors
        not_found_tests = [r for r in results if r.get("response", {}).get("status_code") == 404]
        if not_found_tests:
            recommendations.append(f"{len(not_found_tests)} endpoints returned 404. Verify endpoint paths and server status.")
        
        return recommendations
    
    def _generate_overall_recommendations(self, analysis: Dict[str, Any], execution: Dict[str, Any]) -> List[str]:
        """Generate overall recommendations for the complete testing process"""
        recommendations = []
        
        # Combine recommendations from both phases
        analysis_recs = analysis.get("analysis_report", {}).get("recommendations", [])
        execution_recs = execution.get("execution_report", {}).get("recommendations", [])
        
        recommendations.extend(analysis_recs)
        recommendations.extend(execution_recs)
        
        # Add overall recommendations
        success_rate = execution.get("summary", {}).get("passed", 0) / max(execution.get("summary", {}).get("total_tests", 1), 1) * 100
        
        if success_rate < 50:
            recommendations.append("Low overall success rate. Consider reviewing API server status and endpoint configurations.")
        elif success_rate > 90:
            recommendations.append("High success rate! Consider expanding test coverage and adding edge cases.")
        
        return recommendations
    
    def _suggest_next_steps(self, analysis: Dict[str, Any], execution: Dict[str, Any]) -> List[str]:
        """Suggest next steps for improving the testing process"""
        steps = []
        
        # Based on test coverage
        coverage = analysis.get("analysis_report", {}).get("test_generation", {}).get("test_coverage", {})
        if coverage.get("coverage_percentage", 0) < 80:
            steps.append("Improve test coverage by adding tests for undetected endpoints")
        
        # Based on execution results
        failed_count = execution.get("summary", {}).get("failed", 0)
        if failed_count > 0:
            steps.append("Investigate and fix failing tests")
            steps.append("Verify API server is running and accessible")
        
        steps.extend([
            "Set up continuous integration for automated testing",
            "Add authentication and authorization tests",
            "Implement load testing for performance validation",
            "Create custom test scenarios for business logic"
        ])
        
        return steps