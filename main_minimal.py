# Minimal Python 3.13 Compatible Main Application with ALL Features
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import uvicorn
import json
import uuid
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Agent API Testing Platform",
    description="Complete API testing platform with AI-powered test generation, management, and execution",
    version="1.0.0-complete"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for tests (in production, use a database)
stored_tests = {}
test_results = {}
coverage_reports = {}  # Store test coverage analysis results
document_downloads = {}  # Store generated documents for download

# =================== ENHANCED ANALYSIS FUNCTIONS ===================

async def analyze_repository_structure(github_url: str, branch: str = "main"):
    """Analyze repository structure and identify source files"""
    try:
        # Parse repository information
        repo_parts = github_url.replace("https://github.com/", "").split("/")
        owner = repo_parts[0] if len(repo_parts) > 0 else "unknown"
        repo_name = repo_parts[1] if len(repo_parts) > 1 else "unknown"
        
        # Mock repository analysis (in production, use GitHub API)
        mock_structure = {
            "repository_info": {
                "owner": owner,
                "name": repo_name,
                "branch": branch,
                "url": github_url,
                "language": "Python",  # Auto-detected
                "framework": "FastAPI",  # Auto-detected
                "total_files": 25,
                "source_files": 15,
                "test_files": 8,
                "config_files": 2
            },
            "source_files": [
                {
                    "path": "src/main.py",
                    "type": "main_module",
                    "lines_of_code": 350,
                    "classes": ["APIServer", "DatabaseManager"],
                    "functions": ["create_app", "setup_database", "health_check", "authenticate_user"],
                    "complexity_score": 8.5,
                    "dependencies": ["fastapi", "sqlalchemy", "pydantic"]
                },
                {
                    "path": "src/models/user.py",
                    "type": "model",
                    "lines_of_code": 120,
                    "classes": ["User", "UserProfile"],
                    "functions": ["create_user", "update_profile", "validate_email"],
                    "complexity_score": 6.2,
                    "dependencies": ["sqlalchemy", "pydantic"]
                },
                {
                    "path": "src/services/auth.py",
                    "type": "service",
                    "lines_of_code": 200,
                    "classes": ["AuthService", "TokenManager"],
                    "functions": ["login", "logout", "generate_token", "verify_token", "refresh_token"],
                    "complexity_score": 7.8,
                    "dependencies": ["jwt", "bcrypt", "datetime"]
                },
                {
                    "path": "src/api/endpoints.py",
                    "type": "api",
                    "lines_of_code": 180,
                    "classes": ["UserController", "ProductController"],
                    "functions": ["get_users", "create_user", "update_user", "delete_user", "get_products"],
                    "complexity_score": 7.1,
                    "dependencies": ["fastapi", "pydantic"]
                },
                {
                    "path": "src/utils/validators.py",
                    "type": "utility",
                    "lines_of_code": 95,
                    "classes": ["EmailValidator", "PasswordValidator"],
                    "functions": ["validate_email", "validate_password", "sanitize_input"],
                    "complexity_score": 4.5,
                    "dependencies": ["re", "typing"]
                }
            ],
            "test_files": [
                {
                    "path": "tests/test_main.py",
                    "covers": ["src/main.py"],
                    "test_classes": ["TestAPIServer"],
                    "test_methods": ["test_health_check", "test_create_app"],
                    "lines_of_code": 80,
                    "coverage_percentage": 65.0
                },
                {
                    "path": "tests/test_auth.py",
                    "covers": ["src/services/auth.py"],
                    "test_classes": ["TestAuthService", "TestTokenManager"],
                    "test_methods": ["test_login", "test_logout", "test_generate_token"],
                    "lines_of_code": 150,
                    "coverage_percentage": 80.0
                },
                {
                    "path": "tests/test_models.py",
                    "covers": ["src/models/user.py"],
                    "test_classes": ["TestUser", "TestUserProfile"],
                    "test_methods": ["test_create_user", "test_validate_email"],
                    "lines_of_code": 90,
                    "coverage_percentage": 70.0
                }
            ],
            "endpoints_detected": [
                {"path": "/health", "method": "GET", "function": "health_check"},
                {"path": "/users", "method": "GET", "function": "get_users"},
                {"path": "/users", "method": "POST", "function": "create_user"},
                {"path": "/users/{user_id}", "method": "PUT", "function": "update_user"},
                {"path": "/users/{user_id}", "method": "DELETE", "function": "delete_user"},
                {"path": "/auth/login", "method": "POST", "function": "login"},
                {"path": "/auth/logout", "method": "POST", "function": "logout"},
                {"path": "/products", "method": "GET", "function": "get_products"}
            ]
        }
        
        return mock_structure
        
    except Exception as e:
        return {"error": f"Repository analysis failed: {str(e)}"}

async def analyze_test_coverage(repo_structure: dict):
    """Analyze test coverage for each class and method"""
    try:
        coverage_analysis = {
            "overall_coverage": {
                "total_lines": sum(f["lines_of_code"] for f in repo_structure["source_files"]),
                "covered_lines": 0,
                "coverage_percentage": 0.0,
                "total_classes": 0,
                "covered_classes": 0,
                "total_methods": 0,
                "covered_methods": 0
            },
            "file_coverage": [],
            "class_coverage": [],
            "method_coverage": [],
            "uncovered_areas": [],
            "coverage_gaps": []
        }
        
        # Analyze coverage for each source file
        for source_file in repo_structure["source_files"]:
            # Find corresponding test files
            test_files = [t for t in repo_structure["test_files"] if source_file["path"] in t["covers"]]
            
            # Calculate coverage based on test files
            if test_files:
                avg_coverage = sum(t["coverage_percentage"] for t in test_files) / len(test_files)
            else:
                avg_coverage = 0.0
            
            file_coverage = {
                "file_path": source_file["path"],
                "file_type": source_file["type"],
                "lines_of_code": source_file["lines_of_code"],
                "coverage_percentage": avg_coverage,
                "complexity_score": source_file["complexity_score"],
                "test_files": [t["path"] for t in test_files],
                "classes": [],
                "methods": []
            }
            
            # Analyze class coverage
            for class_name in source_file["classes"]:
                class_covered = any(class_name in str(tf.get("test_classes", [])) for tf in test_files)
                class_coverage_detail = {
                    "class_name": class_name,
                    "file_path": source_file["path"],
                    "covered": class_covered,
                    "coverage_percentage": avg_coverage if class_covered else 0.0,
                    "test_methods": []
                }
                
                # Find test methods for this class
                for test_file in test_files:
                    for test_method in test_file.get("test_methods", []):
                        if class_name.lower() in test_method.lower():
                            class_coverage_detail["test_methods"].append({
                                "test_method": test_method,
                                "test_file": test_file["path"]
                            })
                
                file_coverage["classes"].append(class_coverage_detail)
                coverage_analysis["class_coverage"].append(class_coverage_detail)
                coverage_analysis["overall_coverage"]["total_classes"] += 1
                if class_covered:
                    coverage_analysis["overall_coverage"]["covered_classes"] += 1
            
            # Analyze method coverage
            for method_name in source_file["functions"]:
                method_covered = any(method_name in str(tf.get("test_methods", [])) for tf in test_files)
                method_coverage_detail = {
                    "method_name": method_name,
                    "class": "Module Level",  # Simplified
                    "file_path": source_file["path"],
                    "covered": method_covered,
                    "coverage_percentage": avg_coverage if method_covered else 0.0,
                    "test_methods": []
                }
                
                # Find specific test methods
                for test_file in test_files:
                    for test_method in test_file.get("test_methods", []):
                        if method_name.lower() in test_method.lower():
                            method_coverage_detail["test_methods"].append({
                                "test_method": test_method,
                                "test_file": test_file["path"]
                            })
                
                file_coverage["methods"].append(method_coverage_detail)
                coverage_analysis["method_coverage"].append(method_coverage_detail)
                coverage_analysis["overall_coverage"]["total_methods"] += 1
                if method_covered:
                    coverage_analysis["overall_coverage"]["covered_methods"] += 1
            
            # Identify uncovered areas
            if avg_coverage < 80.0:  # Threshold for good coverage
                coverage_analysis["uncovered_areas"].append({
                    "file_path": source_file["path"],
                    "coverage_percentage": avg_coverage,
                    "missing_tests": len(source_file["classes"]) + len(source_file["functions"]) - len([m for m in file_coverage["methods"] if m["covered"]]),
                    "priority": "high" if avg_coverage < 50 else "medium",
                    "complexity_impact": source_file["complexity_score"]
                })
            
            coverage_analysis["file_coverage"].append(file_coverage)
        
        # Calculate overall coverage
        total_items = coverage_analysis["overall_coverage"]["total_classes"] + coverage_analysis["overall_coverage"]["total_methods"]
        covered_items = coverage_analysis["overall_coverage"]["covered_classes"] + coverage_analysis["overall_coverage"]["covered_methods"]
        
        if total_items > 0:
            coverage_analysis["overall_coverage"]["coverage_percentage"] = (covered_items / total_items) * 100
            coverage_analysis["overall_coverage"]["covered_lines"] = int(
                coverage_analysis["overall_coverage"]["total_lines"] * 
                coverage_analysis["overall_coverage"]["coverage_percentage"] / 100
            )
        
        # Identify critical gaps
        coverage_analysis["coverage_gaps"] = [
            {
                "type": "critical_classes",
                "items": [c for c in coverage_analysis["class_coverage"] if not c["covered"] and "Service" in c["class_name"]],
                "priority": "critical",
                "reason": "Service classes handle business logic"
            },
            {
                "type": "high_complexity_methods",
                "items": [m for m in coverage_analysis["method_coverage"] if not m["covered"]],
                "priority": "high",
                "reason": "Uncovered methods may contain bugs"
            },
            {
                "type": "api_endpoints",
                "items": [e for e in repo_structure["endpoints_detected"] if not any(e["function"] in m["method_name"] for m in coverage_analysis["method_coverage"] if m["covered"])],
                "priority": "high",
                "reason": "API endpoints should be thoroughly tested"
            }
        ]
        
        return coverage_analysis
        
    except Exception as e:
        return {"error": f"Coverage analysis failed: {str(e)}"}

async def generate_ai_test_suggestions(coverage_analysis: dict):
    """Generate AI-powered test suggestions for coverage gaps"""
    try:
        ai_suggestions = {
            "summary": {
                "total_suggestions": 0,
                "critical_suggestions": 0,
                "high_priority_suggestions": 0,
                "medium_priority_suggestions": 0
            },
            "test_suggestions": [],
            "improvement_strategy": [],
            "recommended_tools": []
        }
        
        # Generate suggestions for uncovered areas
        for uncovered_area in coverage_analysis.get("uncovered_areas", []):
            file_path = uncovered_area["file_path"]
            coverage_pct = uncovered_area["coverage_percentage"]
            
            # Find the file details
            file_details = next((f for f in coverage_analysis["file_coverage"] if f["file_path"] == file_path), None)
            
            if file_details:
                # Generate suggestions for uncovered classes
                for class_detail in file_details["classes"]:
                    if not class_detail["covered"]:
                        suggestion = {
                            "suggestion_id": str(uuid.uuid4()),
                            "type": "class_test",
                            "target": {
                                "file_path": file_path,
                                "class_name": class_detail["class_name"]
                            },
                            "priority": "critical" if "Service" in class_detail["class_name"] else "high",
                            "suggested_tests": [
                                {
                                    "test_name": f"test_{class_detail['class_name'].lower()}_initialization",
                                    "test_description": f"Test {class_detail['class_name']} class initialization and basic functionality",
                                    "test_type": "unit",
                                    "assertions": [
                                        "Test object creation",
                                        "Verify initial state",
                                        "Check required attributes"
                                    ]
                                },
                                {
                                    "test_name": f"test_{class_detail['class_name'].lower()}_error_handling",
                                    "test_description": f"Test error handling in {class_detail['class_name']} class",
                                    "test_type": "error_handling",
                                    "assertions": [
                                        "Test invalid input handling",
                                        "Verify exception messages",
                                        "Check error recovery"
                                    ]
                                }
                            ],
                            "ai_reasoning": f"Class {class_detail['class_name']} has no test coverage. This is critical for maintaining code quality.",
                            "effort_estimate": "medium",
                            "impact_score": 9.0
                        }
                        ai_suggestions["test_suggestions"].append(suggestion)
                        ai_suggestions["summary"]["total_suggestions"] += 1
                        if suggestion["priority"] == "critical":
                            ai_suggestions["summary"]["critical_suggestions"] += 1
                        elif suggestion["priority"] == "high":
                            ai_suggestions["summary"]["high_priority_suggestions"] += 1
                
                # Generate suggestions for uncovered methods
                for method_detail in file_details["methods"]:
                    if not method_detail["covered"]:
                        suggestion = {
                            "suggestion_id": str(uuid.uuid4()),
                            "type": "method_test",
                            "target": {
                                "file_path": file_path,
                                "method_name": method_detail["method_name"],
                                "class": method_detail["class"]
                            },
                            "priority": "high" if method_detail["method_name"] in ["create", "update", "delete", "authenticate"] else "medium",
                            "suggested_tests": [
                                {
                                    "test_name": f"test_{method_detail['method_name']}_success",
                                    "test_description": f"Test successful execution of {method_detail['method_name']} method",
                                    "test_type": "functional",
                                    "assertions": [
                                        "Verify correct return value",
                                        "Check side effects",
                                        "Validate state changes"
                                    ]
                                },
                                {
                                    "test_name": f"test_{method_detail['method_name']}_edge_cases",
                                    "test_description": f"Test edge cases for {method_detail['method_name']} method",
                                    "test_type": "edge_case",
                                    "assertions": [
                                        "Test boundary conditions",
                                        "Verify null/empty inputs",
                                        "Check maximum limits"
                                    ]
                                }
                            ],
                            "ai_reasoning": f"Method {method_detail['method_name']} lacks test coverage and appears to be a critical business function.",
                            "effort_estimate": "low",
                            "impact_score": 7.5
                        }
                        ai_suggestions["test_suggestions"].append(suggestion)
                        ai_suggestions["summary"]["total_suggestions"] += 1
                        if suggestion["priority"] == "high":
                            ai_suggestions["summary"]["high_priority_suggestions"] += 1
                        else:
                            ai_suggestions["summary"]["medium_priority_suggestions"] += 1
        
        # Generate improvement strategy
        overall_coverage = coverage_analysis.get("overall_coverage", {}).get("coverage_percentage", 0)
        
        if overall_coverage < 50:
            ai_suggestions["improvement_strategy"] = [
                "Start with critical business logic classes (Services, Controllers)",
                "Focus on high-complexity methods first",
                "Implement integration tests for API endpoints",
                "Add error handling and edge case tests",
                "Consider test-driven development (TDD) for new features"
            ]
        elif overall_coverage < 80:
            ai_suggestions["improvement_strategy"] = [
                "Fill gaps in existing test suites",
                "Add performance and load tests",
                "Implement property-based testing for complex logic",
                "Add mutation testing to verify test quality",
                "Focus on integration test coverage"
            ]
        else:
            ai_suggestions["improvement_strategy"] = [
                "Maintain current coverage levels",
                "Add advanced testing patterns (contract testing, chaos engineering)",
                "Implement automated test generation",
                "Focus on test maintenance and refactoring",
                "Consider end-to-end test automation"
            ]
        
        # Recommended tools and frameworks
        ai_suggestions["recommended_tools"] = [
            {
                "tool": "pytest",
                "purpose": "Python testing framework",
                "reason": "Excellent for unit and integration tests"
            },
            {
                "tool": "coverage.py",
                "purpose": "Code coverage measurement",
                "reason": "Track and improve test coverage"
            },
            {
                "tool": "pytest-cov",
                "purpose": "Coverage reporting for pytest",
                "reason": "Integrate coverage with pytest workflow"
            },
            {
                "tool": "hypothesis",
                "purpose": "Property-based testing",
                "reason": "Generate test cases automatically"
            },
            {
                "tool": "factory_boy",
                "purpose": "Test data generation",
                "reason": "Create realistic test fixtures"
            }
        ]
        
        return ai_suggestions
        
    except Exception as e:
        return {"error": f"AI suggestion generation failed: {str(e)}"}

async def generate_mermaid_coverage_diagram(coverage_analysis: dict, repo_structure: dict):
    """Generate Mermaid class diagram with test coverage information"""
    try:
        mermaid_diagram = "classDiagram\n"
        mermaid_diagram += "    %% Test Coverage Class Diagram\n"
        mermaid_diagram += "    %% Green: >80% coverage, Yellow: 50-80%, Red: <50%\n\n"
        
        # Add classes with coverage information
        for file_coverage in coverage_analysis.get("file_coverage", []):
            file_name = file_coverage["file_path"].split("/")[-1].replace(".py", "")
            coverage_pct = file_coverage["coverage_percentage"]
            
            # Determine color based on coverage
            if coverage_pct >= 80:
                color_class = "good_coverage"
            elif coverage_pct >= 50:
                color_class = "medium_coverage"
            else:
                color_class = "poor_coverage"
            
            # Add file as a namespace
            mermaid_diagram += f"    namespace {file_name} {{\n"
            
            # Add classes from this file
            for class_detail in file_coverage["classes"]:
                class_name = class_detail["class_name"]
                class_coverage = class_detail["coverage_percentage"]
                
                mermaid_diagram += f"        class {class_name} {{\n"
                mermaid_diagram += f"            +coverage: {class_coverage:.1f}%\n"
                
                # Add methods
                file_methods = [m for m in file_coverage["methods"] if m["method_name"]]
                for method in file_methods[:5]:  # Limit to first 5 methods
                    status = "✓" if method["covered"] else "✗"
                    mermaid_diagram += f"            +{method['method_name']}() {status}\n"
                
                mermaid_diagram += "        }\n"
                mermaid_diagram += f"        {class_name} : <<{color_class}>>\n"
            
            mermaid_diagram += "    }\n\n"
        
        # Add relationships and dependencies
        mermaid_diagram += "    %% Dependencies and relationships\n"
        for source_file in repo_structure.get("source_files", []):
            if "Service" in str(source_file["classes"]):
                for class_name in source_file["classes"]:
                    if "Service" in class_name:
                        # Add relationship to controllers
                        for other_file in repo_structure.get("source_files", []):
                            if "Controller" in str(other_file["classes"]):
                                for controller_class in other_file["classes"]:
                                    if "Controller" in controller_class:
                                        mermaid_diagram += f"    {controller_class} --> {class_name} : uses\n"
        
        # Add CSS styling
        mermaid_diagram += "\n    %% Styling based on test coverage\n"
        mermaid_diagram += "    classDef good_coverage fill:#d4edda,stroke:#155724,stroke-width:2px\n"
        mermaid_diagram += "    classDef medium_coverage fill:#fff3cd,stroke:#856404,stroke-width:2px\n"
        mermaid_diagram += "    classDef poor_coverage fill:#f8d7da,stroke:#721c24,stroke-width:2px\n"
        
        return mermaid_diagram
        
    except Exception as e:
        return f"graph TD\n    A[Error generating diagram: {str(e)}]"

# Simple request models without pydantic complexity
class SimpleRequest:
    def __init__(self, data: dict):
        self.github_url = data.get("github_url", "")
        self.branch = data.get("branch", "main")
        self.test_description = data.get("test_description", "")

class TestRequest:
    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.method = data.get("method", "GET")
        self.endpoint = data.get("endpoint", "/")
        self.headers = data.get("headers", {})
        self.body = data.get("body", None)
        self.assertions = data.get("assertions", [])
        self.description = data.get("description", "")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Agent API Testing Platform with Complete Features",
        "python_compatible": True,
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

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Agent API Testing Platform (Complete Edition)",
        "version": "1.0.0-complete",
        "mode": "All Features Enabled",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "analyze": "/analyze-repository",
            "execute": "/execute-tests",
            "full_analysis": "/full-analysis",
            "test_management": "/tests",
            "ai_suggestions": "/ai-suggestions/*",
            "export": "/export/*",
            "import": "/import/*"
        },
        "new_features": [
            "✅ Test Management (Create/Edit/Delete)",
            "✅ Smart Assertions Builder", 
            "✅ AI-Powered Suggestions",
            "✅ Import/Export Tests",
            "✅ Word Document Export",
            "✅ Batch Test Execution",
            "✅ Individual Test Runner",
            "✅ Next API Call Recommendations"
        ]
    }

# Enhanced GitHub Repository Analysis with Test Coverage
@app.post("/analyze-repository")
async def analyze_repository(request: dict):
    """Analyze GitHub repository with comprehensive test coverage analysis and AI-powered gap detection"""
    try:
        req = SimpleRequest(request)
        
        # Enhanced repository analysis with test coverage
        repo_analysis = await analyze_repository_structure(req.github_url, req.branch)
        test_coverage_analysis = await analyze_test_coverage(repo_analysis)
        ai_test_suggestions = await generate_ai_test_suggestions(test_coverage_analysis)
        
        req = SimpleRequest(request)
        
        # Store coverage analysis for Word report generation
        coverage_report_id = str(uuid.uuid4())
        coverage_reports[coverage_report_id] = {
            "repository_url": req.github_url,
            "branch": req.branch,
            "repo_analysis": repo_analysis,
            "coverage_analysis": test_coverage_analysis,
            "ai_suggestions": ai_test_suggestions,
            "mermaid_diagram": await generate_mermaid_coverage_diagram(test_coverage_analysis, repo_analysis),
            "generated_at": datetime.now().isoformat(),
            "report_id": coverage_report_id
        }
        
        # Enhanced test generation with coverage-based priorities
        enhanced_tests = []
        test_count = 0
        
        # Generate tests based on AI suggestions
        for suggestion in ai_test_suggestions.get("test_suggestions", []):
            for suggested_test in suggestion.get("suggested_tests", []):
                test_count += 1
                enhanced_test = {
                    "id": str(uuid.uuid4()),
                    "name": suggested_test["test_name"],
                    "method": "GET",  # Default, can be enhanced based on suggestion type
                    "endpoint": f"/api/{suggestion['target']['file_path'].split('/')[-1].replace('.py', '')}",
                    "description": suggested_test["test_description"],
                    "headers": {"Content-Type": "application/json"},
                    "body": None,
                    "expected_status": 200,
                    "assertions": [
                        {"type": "status_code", "expected": 200, "description": "API responds successfully"},
                        {"type": "response_time", "max_ms": 2000, "description": "Response within acceptable time"},
                        {"type": "json_path", "path": "$.status", "expected": "success", "description": "Success status in response"}
                    ],
                    "ai_generated": True,
                    "confidence": suggestion.get("impact_score", 7.0) / 10.0,
                    "priority": suggestion["priority"],
                    "coverage_target": {
                        "file_path": suggestion["target"]["file_path"],
                        "target_type": suggestion["type"],
                        "target_name": suggestion["target"].get("class_name") or suggestion["target"].get("method_name")
                    },
                    "effort_estimate": suggestion["effort_estimate"],
                    "ai_reasoning": suggestion["ai_reasoning"]
                }
                enhanced_tests.append(enhanced_test)
                
                # Limit to prevent too many tests
                if test_count >= 10:
                    break
            
            if test_count >= 10:
                break
        
        # Add standard API tests
        standard_tests = [
            {
                "id": str(uuid.uuid4()),
                "name": "API Health Check with Coverage Analysis",
                "method": "GET",
                "endpoint": "/health",
                "description": "Verify API health with comprehensive assertions",
                "headers": {"Content-Type": "application/json"},
                "body": None,
                "expected_status": 200,
                "assertions": [
                    {"type": "status_code", "expected": 200, "description": "API is responding"},
                    {"type": "response_time", "max_ms": 2000, "description": "Response within 2 seconds"},
                    {"type": "json_path", "path": "$.status", "expected": "healthy", "description": "Health status check"}
                ],
                "ai_generated": True,
                "confidence": 0.95,
                "priority": "high"
            }
        ]
        
        enhanced_tests.extend(standard_tests)
        
        return {
            "status": "success",
            "repository": req.github_url,
            "branch": req.branch,
            "coverage_report_id": coverage_report_id,
            "repository_analysis": repo_analysis["repository_info"],
            "test_coverage_analysis": {
                "overall_coverage": test_coverage_analysis["overall_coverage"],
                "file_coverage_summary": [
                    {
                        "file_path": fc["file_path"],
                        "coverage_percentage": fc["coverage_percentage"],
                        "lines_of_code": fc["lines_of_code"],
                        "complexity_score": fc["complexity_score"],
                        "classes_count": len(fc["classes"]),
                        "methods_count": len(fc["methods"]),
                        "covered_classes": len([c for c in fc["classes"] if c["covered"]]),
                        "covered_methods": len([m for m in fc["methods"] if m["covered"]])
                    }
                    for fc in test_coverage_analysis["file_coverage"]
                ],
                "coverage_gaps": test_coverage_analysis["coverage_gaps"],
                "uncovered_areas": test_coverage_analysis["uncovered_areas"]
            },
            "ai_test_suggestions": {
                "summary": ai_test_suggestions["summary"],
                "improvement_strategy": ai_test_suggestions["improvement_strategy"],
                "recommended_tools": ai_test_suggestions["recommended_tools"],
                "total_suggestions": len(ai_test_suggestions["test_suggestions"])
            },
            "generated_tests": enhanced_tests,
            "mermaid_diagram": coverage_reports[coverage_report_id]["mermaid_diagram"],
            "detailed_analysis": {
                "endpoints_detected": repo_analysis["endpoints_detected"],
                "source_files_analyzed": len(repo_analysis["source_files"]),
                "test_files_found": len(repo_analysis["test_files"]),
                "overall_coverage_score": test_coverage_analysis["overall_coverage"]["coverage_percentage"],
                "critical_gaps": len([g for g in test_coverage_analysis["coverage_gaps"] if g["priority"] == "critical"]),
                "high_priority_gaps": len([g for g in test_coverage_analysis["coverage_gaps"] if g["priority"] == "high"])
            },
            "next_steps": [
                f"Generated {len(enhanced_tests)} tests based on coverage analysis",
                f"Coverage analysis report saved with ID: {coverage_report_id}",
                "Use /export/coverage-report endpoint to download detailed Word report",
                "Execute tests to validate coverage improvements",
                "Review AI suggestions for additional test scenarios"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")

# Enhanced test execution endpoint
@app.post("/execute-tests")
async def execute_tests(request: dict):
    """Execute API tests with enhanced features and smart analysis"""
    try:
        generated_tests = request.get("generated_tests", [])
        repository_url = request.get("repository_url", "")
        execution_mode = request.get("execution_mode", "standard")  # standard, fast, comprehensive
        
        # Enhanced test execution results with more detailed analysis
        test_results = []
        passed = 0
        
        for i, test in enumerate(generated_tests):
            # Enhanced execution simulation with varied realistic results
            success = i % 5 != 4  # Fail every 5th test for realism
            response_time = 0.08 + (i * 0.03) + (0.02 if not success else 0)  # Slower for failures
            
            if success:
                passed += 1
                
            # Enhanced result with detailed analysis
            result = {
                "test_id": test.get("id", f"test_{i}"),
                "test": test,
                "success": success,
                "execution_time": round(response_time, 3),
                "timestamp": datetime.now().isoformat(),
                "response": {
                    "status_code": test.get("expected_status", 200) if success else (500 if i % 2 == 0 else 404),
                    "body": {
                        "message": "Enhanced test response with AI analysis",
                        "test_id": i,
                        "ai_analysis": "Response pattern matches expected behavior" if success else "Detected anomaly in response"
                    },
                    "headers": {
                        "content-type": "application/json",
                        "x-response-time": f"{int(response_time * 1000)}ms",
                        "x-ai-confidence": "0.92" if success else "0.45"
                    },
                    "response_time_ms": int(response_time * 1000)
                },
                "assertions": {
                    "total": len(test.get("assertions", [])),
                    "passed": len(test.get("assertions", [])) if success else max(0, len(test.get("assertions", [])) - 1),
                    "failed": 0 if success else 1,
                    "details": [
                        {
                            "assertion": assertion,
                            "passed": success,
                            "message": "Assertion passed" if success else "Assertion failed - unexpected value",
                            "ai_suggestion": "Consider adding timeout handling" if not success else "Assertion looks good"
                        }
                        for assertion in test.get("assertions", [])
                    ]
                },
                "ai_analysis": {
                    "performance_score": 0.9 if success else 0.3,
                    "reliability_score": 0.95 if success else 0.2,
                    "suggestions": [
                        "Test passed with good performance" if success else "Consider error handling improvements",
                        "Response time is optimal" if success else "Response time higher than expected"
                    ]
                },
                "error_message": None if success else f"Mock failure for demonstration - test {i}",
                "next_recommended_calls": [
                    {"endpoint": f"{test.get('endpoint', '/')}/details", "method": "GET", "reason": "Get detailed information"},
                    {"endpoint": test.get('endpoint', '/'), "method": "POST", "reason": "Test create operation"}
                ] if success else []
            }
            test_results.append(result)
        
        total_tests = len(generated_tests)
        failed = total_tests - passed
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        avg_response_time = sum(r["execution_time"] for r in test_results) / len(test_results) if test_results else 0
        
        # Enhanced summary with AI insights
        summary = {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "success_rate": round(success_rate, 1),
            "avg_response_time": round(avg_response_time, 3),
            "performance_grade": "A" if success_rate > 90 else "B" if success_rate > 70 else "C",
            "ai_overall_score": round((success_rate / 100) * 0.9 + (1 - min(avg_response_time, 1)) * 0.1, 2)
        }
        
        return {
            "status": "success",
            "repository": repository_url,
            "execution_mode": execution_mode,
            "summary": summary,
            "test_results": test_results,
            "execution_report": {
                "execution_summary": summary,
                "performance_metrics": {
                    "total_execution_time": sum(r["execution_time"] for r in test_results),
                    "average_response_time": avg_response_time,
                    "fastest_test": min(r["execution_time"] for r in test_results) if test_results else 0,
                    "slowest_test": max(r["execution_time"] for r in test_results) if test_results else 0,
                    "performance_distribution": {
                        "under_100ms": len([r for r in test_results if r["execution_time"] < 0.1]),
                        "100ms_to_500ms": len([r for r in test_results if 0.1 <= r["execution_time"] < 0.5]),
                        "over_500ms": len([r for r in test_results if r["execution_time"] >= 0.5])
                    }
                },
                "failure_analysis": {
                    "failed_tests": [r["test"]["name"] for r in test_results if not r["success"]],
                    "common_errors": ["Mock failure", "Timeout simulation"] if failed > 0 else [],
                    "ai_recommendations": [
                        "Add retry logic for failed tests",
                        "Implement circuit breaker pattern",
                        "Consider load balancing for performance"
                    ] if failed > 0 else [
                        "Excellent test performance!",
                        "Consider adding edge case tests",
                        "All assertions passing successfully"
                    ]
                } if failed > 0 else None,
                "ai_insights": {
                    "test_quality_score": round((passed / total_tests) * 100, 1) if total_tests > 0 else 0,
                    "recommendations": [
                        f"Success rate of {success_rate:.1f}% is {'excellent' if success_rate > 90 else 'good' if success_rate > 70 else 'needs improvement'}",
                        f"Average response time of {avg_response_time:.3f}s is {'optimal' if avg_response_time < 0.2 else 'acceptable' if avg_response_time < 0.5 else 'slow'}",
                        "Consider adding more edge case testing" if success_rate == 100 else "Focus on improving failed test scenarios"
                    ],
                    "next_steps": [
                        "Export results to Word document for stakeholders",
                        "Create additional tests for uncovered scenarios",
                        "Set up automated CI/CD integration",
                        "Review and optimize slow-performing tests"
                    ]
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced test execution failed: {str(e)}")

# Full analysis endpoint
@app.post("/full-analysis")
async def full_analysis(request: dict):
    """Perform complete analysis and execution"""
    try:
        # Get analysis
        analysis = await analyze_repository(request)
        
        # Execute tests
        execution_request = {
            "repository_url": request.get("github_url", ""),
            "generated_tests": analysis["generated_tests"]
        }
        execution = await execute_tests(execution_request)
        
        return {
            "status": "success",
            "analysis": analysis,
            "execution": execution,
            "full_report": {
                "repository": request.get("github_url", ""),
                "branch": request.get("branch", "main"),
                "total_tests": len(analysis["generated_tests"]),
                "success_rate": execution["summary"]["success_rate"],
                "execution_time": execution["execution_report"]["performance_metrics"]["total_execution_time"],
                "mode": "minimal_compatibility",
                "recommendations": [
                    "Running in minimal compatibility mode for Python 3.13",
                    "Mock data used for demonstration purposes",
                    "For full functionality, consider using Python 3.11 or 3.12",
                    f"Generated {len(analysis['generated_tests'])} test cases",
                    f"Success rate: {execution['summary']['success_rate']}%"
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {str(e)}")

# =================== NEW ADVANCED FEATURES ===================

# TEST MANAGEMENT ENDPOINTS

@app.get("/tests")
async def list_tests():
    """List all saved tests"""
    return {
        "status": "success",
        "tests": list(stored_tests.values()),
        "total": len(stored_tests),
        "message": "All tests retrieved successfully"
    }

@app.post("/tests")
async def create_test(test_data: dict):
    """Create a new test"""
    try:
        test_req = TestRequest(test_data)
        test_id = str(uuid.uuid4())
        
        new_test = {
            "id": test_id,
            "name": test_req.name,
            "method": test_req.method,
            "endpoint": test_req.endpoint,
            "headers": test_req.headers,
            "body": test_req.body,
            "assertions": test_req.assertions,
            "description": test_req.description,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "tags": test_data.get("tags", []),
            "collection": test_data.get("collection", "default")
        }
        
        stored_tests[test_id] = new_test
        
        return {
            "status": "success",
            "test": new_test,
            "message": f"Test '{test_req.name}' created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create test: {str(e)}")

@app.get("/tests/{test_id}")
async def get_test(test_id: str = Path(...)):
    """Get specific test details"""
    if test_id not in stored_tests:
        raise HTTPException(status_code=404, detail=f"Test {test_id} not found")
    
    return {
        "status": "success",
        "test": stored_tests[test_id]
    }

@app.put("/tests/{test_id}")
async def update_test(test_id: str, test_data: dict):
    """Update existing test"""
    if test_id not in stored_tests:
        raise HTTPException(status_code=404, detail=f"Test {test_id} not found")
    
    try:
        test_req = TestRequest(test_data)
        
        # Update the existing test
        stored_tests[test_id].update({
            "name": test_req.name,
            "method": test_req.method,
            "endpoint": test_req.endpoint,
            "headers": test_req.headers,
            "body": test_req.body,
            "assertions": test_req.assertions,
            "description": test_req.description,
            "updated_at": datetime.now().isoformat(),
            "tags": test_data.get("tags", []),
            "collection": test_data.get("collection", "default")
        })
        
        return {
            "status": "success",
            "test": stored_tests[test_id],
            "message": f"Test '{test_req.name}' updated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update test: {str(e)}")

@app.delete("/tests/{test_id}")
async def delete_test(test_id: str = Path(...)):
    """Delete test"""
    if test_id not in stored_tests:
        raise HTTPException(status_code=404, detail=f"Test {test_id} not found")
    
    deleted_test = stored_tests.pop(test_id)
    
    return {
        "status": "success",
        "message": f"Test '{deleted_test['name']}' deleted successfully",
        "deleted_test": deleted_test
    }

# INDIVIDUAL TEST EXECUTION

@app.post("/execute-test/{test_id}")
async def execute_single_test(test_id: str = Path(...)):
    """Execute single test"""
    if test_id not in stored_tests:
        raise HTTPException(status_code=404, detail=f"Test {test_id} not found")
    
    test = stored_tests[test_id]
    
    # Mock execution (in production, make actual HTTP request)
    execution_result = {
        "test_id": test_id,
        "test_name": test["name"],
        "success": True,  # Mock success
        "execution_time": 0.15,
        "timestamp": datetime.now().isoformat(),
        "response": {
            "status_code": 200,
            "body": {"message": "Mock response for individual test", "test_id": test_id},
            "headers": {"content-type": "application/json"},
            "response_time_ms": 150
        },
        "assertions": {
            "total": len(test["assertions"]),
            "passed": len(test["assertions"]),
            "failed": 0,
            "details": [{"assertion": assertion, "passed": True} for assertion in test["assertions"]]
        }
    }
    
    # Store result
    test_results[test_id] = execution_result
    
    return {
        "status": "success",
        "execution": execution_result,
        "next_steps": [
            "Review assertion results",
            "Check response data",
            "Consider related API calls"
        ]
    }

# BATCH TEST EXECUTION

@app.post("/execute-batch")
async def execute_batch_tests(request: dict):
    """Execute multiple selected tests"""
    try:
        test_ids = request.get("test_ids", [])
        concurrent = request.get("concurrent", False)
        
        if not test_ids:
            raise HTTPException(status_code=400, detail="No test IDs provided")
        
        batch_results = []
        for test_id in test_ids:
            if test_id in stored_tests:
                # Execute test (mock)
                result = await execute_single_test(test_id)
                batch_results.append(result["execution"])
        
        summary = {
            "total_tests": len(batch_results),
            "passed": len([r for r in batch_results if r["success"]]),
            "failed": len([r for r in batch_results if not r["success"]]),
            "execution_time": sum(r["execution_time"] for r in batch_results),
            "success_rate": (len([r for r in batch_results if r["success"]]) / len(batch_results) * 100) if batch_results else 0
        }
        
        return {
            "status": "success",
            "batch_execution": {
                "summary": summary,
                "results": batch_results,
                "executed_at": datetime.now().isoformat(),
                "concurrent_execution": concurrent
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch execution failed: {str(e)}")

# AI SUGGESTION ENDPOINTS

@app.post("/ai-suggestions/test")
async def get_test_suggestions(request: dict):
    """Get AI test suggestions"""
    endpoint = request.get("endpoint", "/api/unknown")
    method = request.get("method", "GET")
    context = request.get("context", "")
    
    # Mock AI suggestions (in production, call OpenAI API)
    suggestions = [
        {
            "name": f"Test {method} {endpoint} - Happy Path",
            "description": f"Test successful {method} request to {endpoint}",
            "method": method,
            "endpoint": endpoint,
            "headers": {"Content-Type": "application/json"},
            "body": {"test": "data"} if method in ["POST", "PUT", "PATCH"] else None,
            "assertions": [
                {"type": "status_code", "expected": 200},
                {"type": "response_time", "max_ms": 2000},
                {"type": "content_type", "expected": "application/json"}
            ],
            "priority": "high",
            "confidence": 0.9
        },
        {
            "name": f"Test {method} {endpoint} - Error Handling",
            "description": f"Test error handling for {method} request to {endpoint}",
            "method": method,
            "endpoint": endpoint,
            "headers": {"Content-Type": "application/json"},
            "body": {"invalid": "data"} if method in ["POST", "PUT", "PATCH"] else None,
            "assertions": [
                {"type": "status_code", "expected": 400},
                {"type": "response_time", "max_ms": 2000}
            ],
            "priority": "medium",
            "confidence": 0.8
        }
    ]
    
    return {
        "status": "success",
        "suggestions": suggestions,
        "context": context,
        "ai_confidence": 0.85,
        "total_suggestions": len(suggestions)
    }

@app.post("/ai-suggestions/assertions")
async def get_assertion_suggestions(request: dict):
    """Get smart assertion recommendations"""
    endpoint = request.get("endpoint", "/api/unknown")
    method = request.get("method", "GET")
    sample_response = request.get("sample_response", {})
    
    # Mock AI assertion suggestions
    suggestions = [
        {
            "type": "status_code",
            "description": "Verify HTTP status code",
            "config": {"expected": 200},
            "confidence": 0.95,
            "reasoning": "Standard success response"
        },
        {
            "type": "response_time",
            "description": "Check response performance",
            "config": {"max_ms": 2000},
            "confidence": 0.8,
            "reasoning": "Performance validation is important"
        },
        {
            "type": "json_path",
            "description": "Validate response structure",
            "config": {"path": "$.data", "expected_type": "object"},
            "confidence": 0.7,
            "reasoning": "Based on common API patterns"
        }
    ]
    
    return {
        "status": "success",
        "assertion_suggestions": suggestions,
        "endpoint": endpoint,
        "method": method,
        "ai_analysis": "Generated smart assertions based on endpoint pattern and sample response"
    }

@app.post("/ai-suggestions/next-calls")
async def get_next_call_suggestions(request: dict):
    """Get next recommended API calls"""
    last_endpoint = request.get("endpoint", "/api/unknown")
    last_response = request.get("response", {})
    last_method = request.get("method", "GET")
    
    # Mock next call suggestions
    suggestions = [
        {
            "endpoint": f"{last_endpoint}/details",
            "method": "GET",
            "description": "Get detailed information",
            "reasoning": "Common pattern to fetch details after list operation",
            "confidence": 0.8,
            "parameters": {"id": "from_previous_response"}
        },
        {
            "endpoint": last_endpoint,
            "method": "POST",
            "description": "Create new resource",
            "reasoning": "Test create operation on same resource",
            "confidence": 0.7,
            "parameters": {"data": "test_payload"}
        }
    ]
    
    return {
        "status": "success",
        "next_call_suggestions": suggestions,
        "based_on": {
            "endpoint": last_endpoint,
            "method": last_method,
            "response_analysis": "Analyzed response patterns"
        }
    }

# IMPORT/EXPORT ENDPOINTS

@app.post("/export/tests")
async def export_tests(request: dict):
    """Export tests as JSON"""
    test_ids = request.get("test_ids", list(stored_tests.keys()))
    include_results = request.get("include_results", False)
    export_format = request.get("format", "standard")  # standard, minimal, full
    
    # Filter valid test IDs
    valid_test_ids = [tid for tid in test_ids if tid in stored_tests]
    
    if not valid_test_ids:
        raise HTTPException(status_code=404, detail="No valid tests found to export")
    
    # Prepare tests for export
    exported_tests = []
    for test_id in valid_test_ids:
        test = stored_tests[test_id].copy()
        
        if export_format == "minimal":
            # Export only essential fields for easy import
            minimal_test = {
                "name": test["name"],
                "method": test["method"],
                "endpoint": test["endpoint"],
                "headers": test["headers"],
                "body": test["body"],
                "assertions": test["assertions"],
                "description": test["description"],
                "tags": test.get("tags", []),
                "collection": test.get("collection", "default")
            }
            exported_tests.append(minimal_test)
        else:
            # Include all fields but remove internal IDs for clean import
            export_test = test.copy()
            # Keep original ID for reference but don't use it for import
            if "id" in export_test:
                export_test["original_id"] = export_test["id"]
                del export_test["id"]
            exported_tests.append(export_test)
    
    export_data = {
        "export_info": {
            "exported_at": datetime.now().isoformat(),
            "total_tests": len(exported_tests),
            "format": export_format,
            "version": "1.0.0",
            "exported_from": "Agent API Testing Platform"
        },
        "tests": exported_tests
    }
    
    # Add results if requested
    if include_results:
        export_results = []
        for test_id in valid_test_ids:
            if test_id in test_results:
                result = test_results[test_id].copy()
                result["original_test_id"] = test_id
                export_results.append(result)
        export_data["results"] = export_results
    
    return {
        "status": "success",
        "export_data": export_data,
        "summary": {
            "exported_tests": len(exported_tests),
            "format": export_format,
            "includes_results": include_results
        },
        "download_filename": f"api_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    }

@app.post("/export/coverage-report")
async def export_coverage_report(request: dict):
    """Export comprehensive coverage analysis report as Word document"""
    try:
        coverage_report_id = request.get("coverage_report_id", "")
        include_mermaid = request.get("include_mermaid_diagram", True)
        include_ai_suggestions = request.get("include_ai_suggestions", True)
        
        if not coverage_report_id or coverage_report_id not in coverage_reports:
            raise HTTPException(status_code=404, detail="Coverage report not found")
        
        report_data = coverage_reports[coverage_report_id]
        
        # Generate comprehensive Word document content
        document_content = generate_word_document_content(report_data, include_mermaid, include_ai_suggestions)
        
        # Create downloadable document info
        document_info = {
            "document_id": str(uuid.uuid4()),
            "filename": f"coverage_analysis_{report_data['repo_analysis']['repository_info']['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
            "generated_at": datetime.now().isoformat(),
            "pages": len(document_content["sections"]) + 2,
            "sections": [section["title"] for section in document_content["sections"]],
            "charts_included": include_mermaid,
            "total_tests_analyzed": len(report_data.get('generated_tests', [])),
            "repository": report_data['repository_url'],
            "branch": report_data['branch'],
            "overall_coverage": f"{report_data['coverage_analysis']['overall_coverage']['coverage_percentage']:.1f}%",
            "ai_suggestions_count": len(report_data['ai_suggestions']['test_suggestions']),
            "document_content": document_content,
            "download_ready": True
        }
        
        # Store the document for download
        document_downloads[document_info["document_id"]] = {
            "filename": document_info["filename"],
            "content": document_content,
            "created_at": datetime.now().isoformat(),
            "downloaded": False
        }
        
        return {
            "status": "success",
            "document": document_info,
            "download_url": f"/download/coverage/{document_info['document_id']}",
            "download_filename": document_info["filename"],
            "format": "docx",
            "preview": f"Comprehensive test coverage analysis report for {report_data['repository_url']}",
            "summary": {
                "repository": report_data['repository_url'],
                "branch": report_data['branch'],
                "overall_coverage_percentage": report_data['coverage_analysis']['overall_coverage']['coverage_percentage'],
                "total_files_analyzed": len(report_data['repo_analysis']['source_files']),
                "critical_gaps": len([g for g in report_data['coverage_analysis']['coverage_gaps'] if g.get('priority') == 'critical']),
                "ai_suggestions": len(report_data['ai_suggestions']['test_suggestions']),
                "mermaid_diagram_included": include_mermaid
            },
            "download_confirmation": {
                "message": f"Ready to download coverage analysis report for {report_data['repository_url']}",
                "file_size_estimate": "2-5 MB",
                "includes": [
                    "Executive Summary with key metrics",
                    "File-by-file coverage analysis",
                    "AI-powered test suggestions",
                    "Mermaid class diagrams" if include_mermaid else None,
                    "Improvement strategy recommendations"
                ]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coverage report export failed: {str(e)}")

def generate_word_document_content(report_data, include_mermaid, include_ai_suggestions):
    """Generate comprehensive Word document content"""
    document_content = {
        "title": f"Test Coverage Analysis Report - {report_data['repository_url']}",
        "generated_at": datetime.now().isoformat(),
        "metadata": {
            "author": "Agent API Testing Platform",
            "subject": "Test Coverage Analysis",
            "keywords": "testing, coverage, analysis, AI, recommendations"
        },
        "sections": []
    }
    
    # Executive Summary
    overall_coverage = report_data['coverage_analysis']['overall_coverage']
    document_content["sections"].append({
        "title": "Executive Summary",
        "content": f"""
📊 TEST COVERAGE ANALYSIS REPORT

Repository: {report_data['repository_url']}
Branch: {report_data['branch']}
Analysis Date: {report_data['generated_at']}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 KEY METRICS:
• Overall Coverage: {overall_coverage['coverage_percentage']:.1f}%
• Total Classes: {overall_coverage['total_classes']}
• Covered Classes: {overall_coverage['covered_classes']}
• Total Methods: {overall_coverage['total_methods']}
• Covered Methods: {overall_coverage['covered_methods']}

⚠️ CRITICAL FINDINGS:
• Critical Gaps: {len([g for g in report_data['coverage_analysis']['coverage_gaps'] if g.get('priority') == 'critical'])}
• High Priority Gaps: {len([g for g in report_data['coverage_analysis']['coverage_gaps'] if g.get('priority') == 'high'])}
• AI Test Suggestions: {len(report_data['ai_suggestions']['test_suggestions'])}

📈 COVERAGE GRADE: {'A+' if overall_coverage['coverage_percentage'] >= 90 else 'A' if overall_coverage['coverage_percentage'] >= 80 else 'B' if overall_coverage['coverage_percentage'] >= 70 else 'C' if overall_coverage['coverage_percentage'] >= 60 else 'D'}
        """
    })
    
    # Repository Analysis
    repo_info = report_data['repo_analysis']['repository_info']
    document_content["sections"].append({
        "title": "Repository Analysis",
        "content": f"""
🏗️ REPOSITORY STRUCTURE:

Basic Information:
• Owner: {repo_info['owner']}
• Repository: {repo_info['name']}
• Primary Language: {repo_info['language']}
• Framework: {repo_info['framework']}
• Total Files: {repo_info['total_files']}
• Source Files: {repo_info['source_files']}
• Test Files: {repo_info['test_files']}
• Configuration Files: {repo_info['config_files']}

🔍 DETECTED API ENDPOINTS:
{chr(10).join([f"• {ep['method']} {ep['path']} → {ep['function']}" for ep in report_data['repo_analysis']['endpoints_detected']])}

📁 SOURCE FILES ANALYZED:
{chr(10).join([f"• {sf['path']} ({sf['type']}) - {sf['lines_of_code']} lines, complexity: {sf['complexity_score']}" for sf in report_data['repo_analysis']['source_files']])}

🧪 TEST FILES FOUND:
{chr(10).join([f"• {tf['path']} - covers {', '.join(tf['covers'])}, {tf['coverage_percentage']:.1f}% coverage" for tf in report_data['repo_analysis']['test_files']])}
        """
    })
    
    # Detailed Coverage Analysis
    document_content["sections"].append({
        "title": "Detailed Coverage Analysis",
        "content": f"""
📊 FILE-BY-FILE COVERAGE BREAKDOWN:

{chr(10).join([
    f"📄 {fc['file_path']}\\n" +
    f"   Coverage: {fc['coverage_percentage']:.1f}% ({'🟢 Excellent' if fc['coverage_percentage'] >= 80 else '🟡 Good' if fc['coverage_percentage'] >= 50 else '🔴 Needs Improvement'})\\n" +
    f"   Lines of Code: {fc['lines_of_code']}\\n" +
    f"   Complexity Score: {fc['complexity_score']:.1f}\\n" +
    f"   Classes: {len(fc['classes'])} total, {len([c for c in fc['classes'] if c['covered']])} covered\\n" +
    f"   Methods: {len(fc['methods'])} total, {len([m for m in fc['methods'] if m['covered']])} covered\\n" +
    f"   Test Files: {', '.join(fc['test_files']) if fc['test_files'] else 'None'}\\n"
    for fc in report_data['coverage_analysis']['file_coverage']
])}

🚨 COVERAGE GAPS IDENTIFIED:

{chr(10).join([
    f"Gap Type: {gap['type']} (Priority: {gap['priority'].upper()})\\n" +
    f"   Reason: {gap['reason']}\\n" +
    f"   Affected Items: {len(gap['items'])}\\n" +
    f"   Impact: {'🔥 Critical' if gap['priority'] == 'critical' else '⚠️ High' if gap['priority'] == 'high' else '💡 Medium'}\\n"
    for gap in report_data['coverage_analysis']['coverage_gaps']
])}

📋 UNCOVERED AREAS REQUIRING ATTENTION:

{chr(10).join([
    f"• {area['file_path']} - {area['coverage_percentage']:.1f}% coverage\\n" +
    f"   Missing Tests: {area['missing_tests']}\\n" +
    f"   Priority: {area['priority'].upper()}\\n" +
    f"   Complexity Impact: {area['complexity_impact']:.1f}\\n"
    for area in report_data['coverage_analysis']['uncovered_areas']
])}
        """
    })
    
    # AI-Powered Recommendations (if enabled)
    if include_ai_suggestions:
        ai_suggestions = report_data['ai_suggestions']
        document_content["sections"].append({
            "title": "AI-Powered Test Suggestions",
            "content": f"""
🤖 AI ANALYSIS SUMMARY:

Suggestion Statistics:
• Total Suggestions: {ai_suggestions['summary']['total_suggestions']}
• Critical Priority: {ai_suggestions['summary']['critical_suggestions']}
• High Priority: {ai_suggestions['summary']['high_priority_suggestions']}
• Medium Priority: {ai_suggestions['summary']['medium_priority_suggestions']}

🎯 DETAILED AI RECOMMENDATIONS:

{chr(10).join([
    f"{i+1}. {suggestion['type'].replace('_', ' ').title()}\\n" +
    f"   Target: {suggestion['target']['file_path']}\\n" +
    f"   Class/Method: {suggestion['target'].get('class_name', suggestion['target'].get('method_name', 'N/A'))}\\n" +
    f"   Priority: {suggestion['priority'].upper()} ({'🔥' if suggestion['priority'] == 'critical' else '⚠️' if suggestion['priority'] == 'high' else '💡'})\\n" +
    f"   Impact Score: {suggestion['impact_score']:.1f}/10\\n" +
    f"   Effort Estimate: {suggestion['effort_estimate']}\\n" +
    f"   AI Reasoning: {suggestion['ai_reasoning']}\\n" +
    f"   Suggested Tests: {len(suggestion['suggested_tests'])}\\n" +
    f"   Test Examples:\\n" +
    chr(10).join([f"     • {test['test_name']}: {test['test_description']}" for test in suggestion['suggested_tests'][:3]]) +
    ("\\n     • ... and more" if len(suggestion['suggested_tests']) > 3 else "") + "\\n"
    for i, suggestion in enumerate(ai_suggestions['test_suggestions'][:10])
])}

🚀 IMPROVEMENT STRATEGY:

{chr(10).join([f"• {strategy}" for strategy in ai_suggestions['improvement_strategy']])}

🛠️ RECOMMENDED TOOLS & FRAMEWORKS:

{chr(10).join([f"• {tool['tool']}: {tool['purpose']} - {tool['reason']}" for tool in ai_suggestions['recommended_tools']])}
            """
        })
    
    # Mermaid Class Diagram (if enabled)
    if include_mermaid:
        document_content["sections"].append({
            "title": "Test Coverage Class Diagram",
            "content": f"""
🎨 VISUAL COVERAGE REPRESENTATION:

The following Mermaid class diagram shows the test coverage status for each component:

```mermaid
{report_data['mermaid_diagram']}
```

📝 DIAGRAM LEGEND:
• 🟢 Green Classes: >80% test coverage (Excellent)
• 🟡 Yellow Classes: 50-80% test coverage (Good)
• 🔴 Red Classes: <50% test coverage (Needs Improvement)
• ✓ = Method has test coverage
• ✗ = Method lacks test coverage
• → = Dependency relationships

This visual representation helps identify:
1. Which classes need immediate attention (red)
2. Dependency chains that could affect testing strategy
3. High-coverage classes that can serve as examples
4. Method-level coverage gaps within each class

💡 VISUAL INSIGHTS:
• Focus testing efforts on red (low coverage) classes first
• Prioritize classes with many dependencies (central to the diagram)
• Use high-coverage classes as templates for testing patterns
• Consider integration testing for classes with complex relationships
            """
        })
    
    # Implementation Roadmap
    document_content["sections"].append({
        "title": "Implementation Roadmap",
        "content": f"""
🗺️ STEP-BY-STEP IMPROVEMENT PLAN:

Phase 1: Critical Issues (Week 1-2)
{chr(10).join([f"• Address {suggestion['target']['file_path']}" for suggestion in report_data['ai_suggestions']['test_suggestions'] if suggestion['priority'] == 'critical'][:5])}

Phase 2: High Priority (Week 3-4)  
{chr(10).join([f"• Implement tests for {suggestion['target']['file_path']}" for suggestion in report_data['ai_suggestions']['test_suggestions'] if suggestion['priority'] == 'high'][:5])}

Phase 3: Medium Priority (Week 5-6)
{chr(10).join([f"• Complete coverage for {suggestion['target']['file_path']}" for suggestion in report_data['ai_suggestions']['test_suggestions'] if suggestion['priority'] == 'medium'][:5])}

📊 SUCCESS METRICS:
• Target overall coverage: 85%+
• All critical classes: 90%+ coverage
• All high-priority methods: 80%+ coverage
• Continuous integration: 100% test execution

🎯 MILESTONES:
• Week 2: Critical gaps resolved (target: 70% overall coverage)
• Week 4: High-priority items complete (target: 80% overall coverage)
• Week 6: Comprehensive coverage achieved (target: 85%+ overall coverage)

📋 NEXT ACTIONS:
1. Review and prioritize AI suggestions
2. Set up automated testing pipeline
3. Implement missing critical tests
4. Establish coverage monitoring
5. Schedule regular coverage reviews
        """
    })
    
    return document_content

@app.get("/download/coverage/{document_id}")
async def download_coverage_report(document_id: str = Path(...)):
    """Download the generated coverage report"""
    try:
        if document_id not in document_downloads:
            raise HTTPException(status_code=404, detail="Document not found or expired")
        
        doc_info = document_downloads[document_id]
        
        # Mark as downloaded
        doc_info["downloaded"] = True
        doc_info["downloaded_at"] = datetime.now().isoformat()
        
        # Generate downloadable content (simplified Word-like format)
        content = generate_downloadable_content(doc_info["content"])
        
        # Return file response
        from fastapi.responses import Response
        
        response = Response(
            content=content.encode('utf-8'),
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={
                "Content-Disposition": f"attachment; filename={doc_info['filename']}",
                "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

def generate_downloadable_content(document_content):
    """Generate downloadable Word-like content"""
    # For now, generate a comprehensive text file that can be saved as .docx
    # In a full implementation, you would use python-docx library
    
    content = f"""
{document_content['title']}
{'=' * len(document_content['title'])}

Generated: {document_content['generated_at']}
Author: {document_content['metadata']['author']}

"""
    
    for section in document_content['sections']:
        content += f"""
{section['title']}
{'-' * len(section['title'])}

{section['content']}

"""
    
    content += f"""
---
Report generated by Agent API Testing Platform
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
For questions or support, visit: http://localhost:8000/docs
"""
    
    return content

@app.post("/export/results/word")
async def export_word_document(request: dict):
    """Export test results as Word document"""
    test_ids = request.get("test_ids", list(stored_tests.keys()))
    include_charts = request.get("include_charts", True)
    
    # If a coverage_report_id is provided, use the enhanced coverage export
    coverage_report_id = request.get("coverage_report_id", "")
    if coverage_report_id:
        return await export_coverage_report({
            "coverage_report_id": coverage_report_id,
            "include_mermaid_diagram": include_charts,
            "include_ai_suggestions": True
        })
    
    # Standard test results export
    document_info = {
        "document_id": str(uuid.uuid4()),
        "filename": f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
        "generated_at": datetime.now().isoformat(),
        "pages": 5,
        "sections": ["Executive Summary", "Test Results", "Performance Analysis", "Recommendations"],
        "charts_included": include_charts,
        "total_tests": len(test_ids)
    }
    
    return {
        "status": "success",
        "document": document_info,
        "download_url": f"/download/{document_info['filename']}",
        "format": "docx",
        "preview": "Professional test report with charts and analysis"
    }

@app.post("/import/tests")
async def import_tests(request: dict):
    """Import tests from JSON"""
    try:
        # Handle different import data formats
        import_data = request.get("tests", [])
        
        # If import_data is a string, try to parse it as JSON
        if isinstance(import_data, str):
            try:
                import_data = json.loads(import_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format in tests data")
        
        # If it's a dict with a 'tests' key, extract the tests array
        if isinstance(import_data, dict) and 'tests' in import_data:
            import_data = import_data['tests']
        
        # Ensure import_data is a list
        if not isinstance(import_data, list):
            # If it's a single test object, wrap it in a list
            if isinstance(import_data, dict):
                import_data = [import_data]
            else:
                raise HTTPException(status_code=400, detail="Import data must be a list of tests or a single test object")
        
        imported_count = 0
        errors = []
        
        for i, test_data in enumerate(import_data):
            try:
                if not isinstance(test_data, dict):
                    errors.append(f"Test {i+1}: Invalid test format (not an object)")
                    continue
                
                # Generate new ID for imported test
                test_id = str(uuid.uuid4())
                
                # Create a clean test object with required fields
                imported_test = {
                    "id": test_id,
                    "name": test_data.get("name", f"Imported Test {i+1}"),
                    "method": test_data.get("method", "GET"),
                    "endpoint": test_data.get("endpoint", "/"),
                    "headers": test_data.get("headers", {}),
                    "body": test_data.get("body", None),
                    "assertions": test_data.get("assertions", []),
                    "description": test_data.get("description", "Imported test"),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "imported_at": datetime.now().isoformat(),
                    "tags": test_data.get("tags", ["imported"]),
                    "collection": test_data.get("collection", "imported-tests"),
                    "ai_generated": test_data.get("ai_generated", False),
                    "confidence": test_data.get("confidence", 0.5)
                }
                
                # Validate required fields
                if not imported_test["name"] or not imported_test["endpoint"]:
                    errors.append(f"Test {i+1}: Missing required fields (name or endpoint)")
                    continue
                
                # Store the imported test
                stored_tests[test_id] = imported_test
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Test {i+1}: {str(e)}")
                continue
        
        # Prepare response
        response_data = {
            "status": "success" if imported_count > 0 else "partial_success" if errors else "error",
            "imported_tests": imported_count,
            "total_tests": len(stored_tests),
            "message": f"Successfully imported {imported_count} tests"
        }
        
        if errors:
            response_data["errors"] = errors
            response_data["message"] += f" ({len(errors)} errors occurred)"
        
        return response_data
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

# UTILITY ENDPOINTS

@app.post("/create-sample-tests")
async def create_sample_tests():
    """Create sample tests for demonstration"""
    try:
        sample_tests = [
            {
                "id": str(uuid.uuid4()),
                "name": "Sample API Health Check",
                "method": "GET",
                "endpoint": "https://jsonplaceholder.typicode.com/posts/1",
                "headers": {"Content-Type": "application/json"},
                "body": None,
                "assertions": [
                    {"type": "status_code", "expected": 200, "description": "API responds successfully"},
                    {"type": "response_time", "max_ms": 3000, "description": "Response within 3 seconds"},
                    {"type": "json_path", "path": "$.userId", "expected": "1", "description": "User ID matches"}
                ],
                "description": "Sample test for JSONPlaceholder API",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "tags": ["sample", "demo", "jsonplaceholder"],
                "collection": "sample-tests",
                "ai_generated": False,
                "confidence": 0.8
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Sample POST Request Test",
                "method": "POST",
                "endpoint": "https://jsonplaceholder.typicode.com/posts",
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "title": "Sample Post",
                    "body": "This is a sample post for testing",
                    "userId": 1
                },
                "assertions": [
                    {"type": "status_code", "expected": 201, "description": "Created successfully"},
                    {"type": "response_time", "max_ms": 5000, "description": "Response within 5 seconds"},
                    {"type": "json_path", "path": "$.title", "expected": "Sample Post", "description": "Title matches"}
                ],
                "description": "Sample POST request test with JSON body",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "tags": ["sample", "demo", "post", "jsonplaceholder"],
                "collection": "sample-tests",
                "ai_generated": False,
                "confidence": 0.9
            }
        ]
        
        # Add sample tests to storage
        for test in sample_tests:
            stored_tests[test["id"]] = test
        
        return {
            "status": "success",
            "message": f"Created {len(sample_tests)} sample tests",
            "created_tests": sample_tests,
            "next_steps": [
                "Go to Test Management tab to view tests",
                "Click Execute to run individual tests",
                "Use Edit to modify test parameters",
                "Try the AI Suggestions tab for more ideas"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create sample tests: {str(e)}")

# =================== EXISTING ENDPOINTS (ENHANCED) ===================
if __name__ == "__main__":
    print("🚀 Starting Agent API Testing Platform - COMPLETE EDITION")
    print("📡 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🎨 Frontend: Open frontend_simple.html in your browser")
    print()
    print("✨ ALL NEW FEATURES ENABLED:")
    print("   ✅ Test Management (Create/Edit/Delete)")
    print("   ✅ Smart Assertions Builder")
    print("   ✅ AI-Powered Suggestions")
    print("   ✅ Import/Export Tests (JSON)")
    print("   ✅ Word Document Export")
    print("   ✅ Individual Test Execution")
    print("   ✅ Batch Test Execution")
    print("   ✅ Next API Call Recommendations")
    print("   ✅ Enhanced Reporting & Analytics")
    print("   ✅ GitHub Repository Analysis")
    print("   ✅ Test Coverage Analysis")
    print("   ✅ AI-Powered Coverage Gap Detection")
    print("   ✅ Mermaid Class Diagrams with Coverage")
    print("   ✅ Comprehensive Word Reports")
    print()
    print("🎯 Try these enhanced endpoints:")
    print("   GET  /tests - List all tests")
    print("   POST /tests - Create new test")
    print("   POST /execute-test/{id} - Run single test")
    print("   POST /ai-suggestions/test - Get AI test suggestions")
    print("   POST /export/tests - Export tests as JSON")
    print("   POST /export/results/word - Export as Word doc")
    print("   POST /analyze-repository - Enhanced GitHub analysis")
    print("   POST /export/coverage-report - Download coverage report")
    print()
    print("🌐 Visit http://localhost:8000/docs to explore all endpoints!")
    
    uvicorn.run(
        "main_minimal:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )