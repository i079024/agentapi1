from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn

from services.github_service import GitHubService
from services.llm_service import LLMService
from services.test_execution_service import TestExecutionService
from services.reporting_service import ReportingService

app = FastAPI(
    title="Agent API Testing Platform",
    description="An intelligent API testing platform that generates and executes tests from GitHub repositories",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GitHubService()
llm_service = LLMService()
test_execution_service = TestExecutionService()
reporting_service = ReportingService()

# Request models
class RepositoryAnalysisRequest(BaseModel):
    github_url: str
    branch: Optional[str] = "main"
    test_description: Optional[str] = None

class TestExecutionRequest(BaseModel):
    repository_url: str
    generated_tests: List[Dict[str, Any]]

@app.get("/")
async def root():
    return {
        "message": "Welcome to Agent API Testing Platform",
        "version": "1.0.0",
        "features": [
            "GitHub Repository Analysis",
            "LLM-Powered Test Generation", 
            "Intelligent API Test Execution",
            "Detailed Reporting"
        ]
    }

@app.post("/analyze-repository")
async def analyze_repository(request: RepositoryAnalysisRequest):
    """
    Analyze a GitHub repository and generate API tests using LLM
    """
    try:
        # Step 1: Fetch repository code
        repo_data = await github_service.fetch_repository_code(
            request.github_url, 
            request.branch
        )
        
        # Step 2: Generate test prompts using LLM
        test_prompts = await llm_service.generate_test_prompts(
            repo_data, 
            request.test_description
        )
        
        # Step 3: Generate detailed report
        analysis_report = reporting_service.create_analysis_report(
            repo_data, 
            test_prompts
        )
        
        return {
            "status": "success",
            "repository": request.github_url,
            "branch": request.branch,
            "analysis_report": analysis_report,
            "generated_tests": test_prompts,
            "next_steps": "Execute tests using /execute-tests endpoint"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/execute-tests")
async def execute_tests(request: TestExecutionRequest):
    """
    Execute the generated API tests and return results
    """
    try:
        # Execute all generated tests
        execution_results = await test_execution_service.execute_tests(
            request.generated_tests
        )
        
        # Generate execution report
        execution_report = reporting_service.create_execution_report(
            execution_results
        )
        
        return {
            "status": "success",
            "repository": request.repository_url,
            "execution_report": execution_report,
            "test_results": execution_results,
            "summary": {
                "total_tests": len(execution_results),
                "passed": len([r for r in execution_results if r.get("success", False)]),
                "failed": len([r for r in execution_results if not r.get("success", False)])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

@app.post("/full-analysis")
async def full_analysis(request: RepositoryAnalysisRequest):
    """
    Complete end-to-end analysis: repository fetch -> test generation -> test execution
    """
    try:
        # Step 1: Analyze repository and generate tests
        analysis_response = await analyze_repository(request)
        
        # Step 2: Execute the generated tests
        execution_request = TestExecutionRequest(
            repository_url=request.github_url,
            generated_tests=analysis_response["generated_tests"]
        )
        execution_response = await execute_tests(execution_request)
        
        # Step 3: Create comprehensive report
        full_report = reporting_service.create_full_report(
            analysis_response,
            execution_response
        )
        
        return {
            "status": "success",
            "repository": request.github_url,
            "branch": request.branch,
            "full_report": full_report,
            "analysis": analysis_response,
            "execution": execution_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agentapi"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)