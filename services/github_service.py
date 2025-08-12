import os
import re
import httpx
import aiofiles
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import json
import base64

class GitHubService:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AgentAPI-Testing-Platform/1.0"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def parse_github_url(self, github_url: str) -> Dict[str, str]:
        """Parse GitHub URL to extract owner and repository name"""
        # Handle different GitHub URL formats
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+)/",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, github_url)
            if match:
                return {
                    "owner": match.group(1),
                    "repo": match.group(2)
                }
        
        raise ValueError(f"Invalid GitHub URL format: {github_url}")
    
    async def fetch_repository_code(self, github_url: str, branch: str = "main") -> Dict[str, Any]:
        """Fetch repository code and metadata from GitHub"""
        try:
            repo_info = self.parse_github_url(github_url)
            owner, repo = repo_info["owner"], repo_info["repo"]
            
            async with httpx.AsyncClient() as client:
                # Get repository information
                repo_response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}",
                    headers=self.headers
                )
                repo_response.raise_for_status()
                repo_data = repo_response.json()
                
                # Get repository contents
                contents_response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contents",
                    headers=self.headers,
                    params={"ref": branch}
                )
                contents_response.raise_for_status()
                contents_data = contents_response.json()
                
                # Fetch key files (README, API docs, code files)
                key_files = await self._fetch_key_files(client, owner, repo, branch, contents_data)
                
                return {
                    "repository": {
                        "name": repo_data["name"],
                        "full_name": repo_data["full_name"],
                        "description": repo_data.get("description", ""),
                        "language": repo_data.get("language", ""),
                        "topics": repo_data.get("topics", []),
                        "url": repo_data["html_url"],
                        "clone_url": repo_data["clone_url"]
                    },
                    "branch": branch,
                    "files": key_files,
                    "structure": self._analyze_project_structure(contents_data),
                    "api_endpoints": self._detect_api_endpoints(key_files)
                }
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Repository not found: {github_url}")
            elif e.response.status_code == 403:
                raise ValueError("GitHub API rate limit exceeded or insufficient permissions")
            else:
                raise ValueError(f"GitHub API error: {e.response.status_code}")
        except Exception as e:
            raise ValueError(f"Failed to fetch repository: {str(e)}")
    
    async def _fetch_key_files(self, client: httpx.AsyncClient, owner: str, repo: str, branch: str, contents: List[Dict]) -> Dict[str, str]:
        """Fetch content of key files that might contain API information"""
        key_files = {}
        
        # Priority files to fetch
        priority_files = [
            "README.md", "readme.md", "README.txt",
            "API.md", "api.md", "ENDPOINTS.md",
            "package.json", "requirements.txt", "Pipfile",
            "app.py", "main.py", "server.py", "index.js", "app.js"
        ]
        
        # Look for key files in root directory
        for item in contents:
            if item["type"] == "file" and item["name"] in priority_files:
                try:
                    file_response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}/contents/{item['path']}",
                        headers=self.headers,
                        params={"ref": branch}
                    )
                    if file_response.status_code == 200:
                        file_data = file_response.json()
                        content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                        key_files[item["name"]] = content
                except:
                    continue
        
        # Look for additional API-related files
        api_patterns = [
            r".*routes?\.py$", r".*api\.py$", r".*endpoints?\.py$",
            r".*controller.*\.py$", r".*handler.*\.py$",
            r".*routes?\.js$", r".*api\.js$", r".*controller.*\.js$"
        ]
        
        for item in contents:
            if item["type"] == "file":
                for pattern in api_patterns:
                    if re.match(pattern, item["name"], re.IGNORECASE):
                        try:
                            file_response = await client.get(
                                f"{self.base_url}/repos/{owner}/{repo}/contents/{item['path']}",
                                headers=self.headers,
                                params={"ref": branch}
                            )
                            if file_response.status_code == 200:
                                file_data = file_response.json()
                                content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                                key_files[item["name"]] = content
                        except:
                            continue
                        break
        
        return key_files
    
    def _analyze_project_structure(self, contents: List[Dict]) -> Dict[str, Any]:
        """Analyze project structure to understand the type and framework"""
        structure = {
            "type": "unknown",
            "framework": "unknown",
            "files": [],
            "directories": []
        }
        
        files = [item["name"] for item in contents if item["type"] == "file"]
        dirs = [item["name"] for item in contents if item["type"] == "dir"]
        
        structure["files"] = files
        structure["directories"] = dirs
        
        # Detect project type and framework
        if "package.json" in files:
            structure["type"] = "javascript"
            if "express" in str(files).lower():
                structure["framework"] = "express"
            elif "next" in str(files).lower():
                structure["framework"] = "nextjs"
            else:
                structure["framework"] = "nodejs"
        elif "requirements.txt" in files or "Pipfile" in files or any(f.endswith(".py") for f in files):
            structure["type"] = "python"
            if any("flask" in f.lower() for f in files):
                structure["framework"] = "flask"
            elif any("django" in f.lower() for f in files):
                structure["framework"] = "django"
            elif any("fastapi" in f.lower() for f in files):
                structure["framework"] = "fastapi"
            else:
                structure["framework"] = "python"
        
        return structure
    
    def _detect_api_endpoints(self, files: Dict[str, str]) -> List[Dict[str, Any]]:
        """Detect potential API endpoints from file contents"""
        endpoints = []
        
        # Common patterns for different frameworks
        patterns = {
            "flask": [
                r"@app\.route\(['\"]([^'\"]+)['\"].*methods=\[([^\]]+)\]",
                r"@app\.route\(['\"]([^'\"]+)['\"]"
            ],
            "fastapi": [
                r"@app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]",
                r"@router\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]"
            ],
            "express": [
                r"app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]",
                r"router\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]"
            ]
        }
        
        for filename, content in files.items():
            for framework, pattern_list in patterns.items():
                for pattern in pattern_list:
                    matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            if len(match) == 2:
                                method, path = match
                                endpoints.append({
                                    "method": method.upper(),
                                    "path": path,
                                    "file": filename,
                                    "framework": framework
                                })
                            elif len(match) == 1:
                                endpoints.append({
                                    "method": "GET",
                                    "path": match[0],
                                    "file": filename,
                                    "framework": framework
                                })
        
        return endpoints