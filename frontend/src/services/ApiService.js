import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 60000, // 60 seconds for long-running operations
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`Response received:`, response.status);
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        
        // Handle different error types
        if (error.response) {
          // Server responded with error status
          const message = error.response.data?.detail || 
                         error.response.data?.message || 
                         `Server error: ${error.response.status}`;
          throw new Error(message);
        } else if (error.request) {
          // Request was made but no response
          throw new Error('Unable to connect to the server. Please ensure the backend is running.');
        } else {
          // Something else happened
          throw new Error(error.message || 'An unexpected error occurred');
        }
      }
    );
  }

  /**
   * Analyze a GitHub repository and generate tests
   */
  async analyzeRepository(data) {
    try {
      const response = await this.client.post('/analyze-repository', {
        github_url: data.githubUrl,
        branch: data.branch || 'main',
        test_description: data.testDescription || null
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Execute generated tests
   */
  async executeTests(data) {
    try {
      const response = await this.client.post('/execute-tests', {
        repository_url: data.repository_url,
        generated_tests: data.generated_tests
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Perform full analysis (analyze + execute)
   */
  async fullAnalysis(data) {
    try {
      const response = await this.client.post('/full-analysis', {
        github_url: data.githubUrl,
        branch: data.branch || 'main',
        test_description: data.testDescription || null
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Check API health
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get API status and information
   */
  async getApiInfo() {
    try {
      const response = await this.client.get('/');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Validate GitHub URL format
   */
  static validateGitHubUrl(url) {
    const githubPattern = /^https:\/\/github\.com\/[^\/]+\/[^\/]+/;
    return githubPattern.test(url);
  }

  /**
   * Extract repository info from GitHub URL
   */
  static parseGitHubUrl(url) {
    const match = url.match(/github\.com\/([^\/]+)\/([^\/]+)/);
    if (match) {
      return {
        owner: match[1],
        repo: match[2].replace('.git', '')
      };
    }
    return null;
  }
}

export default new ApiService();