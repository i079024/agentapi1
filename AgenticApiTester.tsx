import React, { useState, useRef } from 'react';
import { Play, Plus, Trash2, Download, Upload, CheckCircle, XCircle, AlertTriangle, Zap, Settings, Eye, Code, BarChart3, Brain, FileText, Lightbulb, ArrowRight, Copy, Save } from 'lucide-react';

const AgenticAPITester = () => {
  const [tests, setTests] = useState([
    {
      id: 1,
      name: 'User Authentication',
      method: 'POST',
      url: 'https://api.example.com/auth/login',
      headers: { 'Content-Type': 'application/json' },
      body: '{"username": "test@example.com", "password": "password123"}',
      expectedStatus: 200,
      assertions: [
        { type: 'status', operator: 'equals', value: '200' },
        { type: 'header', key: 'Content-Type', operator: 'contains', value: 'application/json' },
        { type: 'body', path: 'token', operator: 'exists', value: '' },
        { type: 'body', path: 'user.email', operator: 'equals', value: 'test@example.com' }
      ],
      result: null,
      aiGenerated: false
    }
  ]);
  
  const [selectedTest, setSelectedTest] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState({});
  const [agentMode, setAgentMode] = useState(false);
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [aiPrompts, setAiPrompts] = useState([]);
  const [nextApiSuggestions, setNextApiSuggestions] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState('');
  const [activeTab, setActiveTab] = useState('config');
  const [learnedPatterns, setLearnedPatterns] = useState([]);
  const fileInputRef = useRef(null);

  const methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];
  const assertionTypes = ['status', 'header', 'body', 'response_time', 'json_schema', 'regex'];
  const operators = {
    status: ['equals', 'not_equals', 'greater_than', 'less_than', 'in_range'],
    header: ['exists', 'not_exists', 'equals', 'contains', 'not_contains', 'matches_regex'],
    body: ['exists', 'not_exists', 'equals', 'contains', 'not_contains', 'greater_than', 'less_than', 'matches_regex', 'has_length', 'is_array', 'is_object'],
    response_time: ['less_than', 'greater_than', 'between'],
    json_schema: ['validates_against', 'has_property', 'property_type'],
    regex: ['matches', 'not_matches']
  };

  const detailedPrompts = [
    {
      category: 'Authentication & Security',
      prompts: [
        {
          title: 'JWT Token Validation',
          description: 'Verify JWT token structure and expiration',
          assertion: 'body.token should match JWT pattern and not be expired',
          example: 'token matches /^[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_=]+\\.?[A-Za-z0-9-_.+/=]*$/'
        },
        {
          title: 'Authorization Headers',
          description: 'Ensure proper authorization headers are required',
          assertion: 'Verify 401 status when Authorization header missing',
          example: 'status equals 401 when header "Authorization" not_exists'
        },
        {
          title: 'CORS Headers',
          description: 'Validate Cross-Origin Resource Sharing headers',
          assertion: 'Response includes proper CORS headers',
          example: 'header "Access-Control-Allow-Origin" exists'
        }
      ]
    },
    {
      category: 'Data Validation',
      prompts: [
        {
          title: 'Email Format Validation',
          description: 'Verify email addresses follow proper format',
          assertion: 'Email field contains valid email pattern',
          example: 'body.user.email matches /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/'
        },
        {
          title: 'Required Fields Check',
          description: 'Ensure all mandatory fields are present',
          assertion: 'Response contains all required fields',
          example: 'body.user.id exists AND body.user.name exists'
        },
        {
          title: 'Data Type Validation',
          description: 'Verify correct data types in response',
          assertion: 'Fields have expected data types',
          example: 'body.user.age property_type "number"'
        }
      ]
    },
    {
      category: 'Performance & Reliability',
      prompts: [
        {
          title: 'Response Time SLA',
          description: 'Verify API meets performance requirements',
          assertion: 'Response time within acceptable limits',
          example: 'response_time less_than 2000'
        },
        {
          title: 'Pagination Validation',
          description: 'Check pagination metadata is correct',
          assertion: 'Pagination fields are consistent',
          example: 'body.pagination.total greater_than body.pagination.per_page'
        },
        {
          title: 'Rate Limiting Headers',
          description: 'Verify rate limiting information',
          assertion: 'Rate limit headers provide usage info',
          example: 'header "X-RateLimit-Remaining" exists'
        }
      ]
    },
    {
      category: 'Business Logic',
      prompts: [
        {
          title: 'State Transitions',
          description: 'Verify object state changes correctly',
          assertion: 'Status changes follow business rules',
          example: 'body.order.status in ["pending", "processing", "completed"]'
        },
        {
          title: 'Calculation Accuracy',
          description: 'Verify mathematical calculations',
          assertion: 'Calculated fields are accurate',
          example: 'body.order.total equals sum of body.order.items[].price'
        },
        {
          title: 'Referential Integrity',
          description: 'Check relationships between entities',
          assertion: 'Foreign key references are valid',
          example: 'body.order.user_id equals body.user.id'
        }
      ]
    }
  ];

  const generateNextApiCalls = (currentTest, result) => {
    const suggestions = [];
    
    if (currentTest.url.includes('/auth/login') && result?.data?.token) {
      suggestions.push({
        name: 'Get User Profile',
        method: 'GET',
        url: currentTest.url.replace('/auth/login', '/users/profile'),
        headers: { 'Authorization': `Bearer ${result.data.token}` },
        description: 'Fetch authenticated user profile using the obtained token'
      });
      
      suggestions.push({
        name: 'Refresh Token',
        method: 'POST',
        url: currentTest.url.replace('/login', '/refresh'),
        headers: { 'Authorization': `Bearer ${result.data.token}` },
        description: 'Test token refresh functionality'
      });
    }
    
    if (currentTest.method === 'POST' && currentTest.url.includes('/users') && result?.data?.id) {
      suggestions.push({
        name: 'Get Created User',
        method: 'GET',
        url: `${currentTest.url}/${result.data.id}`,
        description: 'Verify the created user can be retrieved'
      });
      
      suggestions.push({
        name: 'Update Created User',
        method: 'PUT',
        url: `${currentTest.url}/${result.data.id}`,
        body: JSON.stringify({ name: 'Updated Name' }),
        description: 'Test updating the newly created user'
      });
    }
    
    if (currentTest.method === 'GET' && currentTest.url.includes('/users/') && result?.passed) {
      const userId = currentTest.url.split('/users/')[1];
      suggestions.push({
        name: 'Delete User',
        method: 'DELETE',
        url: currentTest.url,
        description: 'Test user deletion'
      });
      
      suggestions.push({
        name: 'Get User Orders',
        method: 'GET',
        url: currentTest.url.replace('/users/', '/users/') + '/orders',
        description: 'Fetch orders for this user'
      });
    }
    
    return suggestions;
  };

  const learnFromPatterns = (test, result) => {
    if (!result?.passed) return;
    
    const pattern = {
      url_pattern: test.url.replace(/\/\d+/g, '/:id'),
      method: test.method,
      successful_assertions: test.assertions.filter((_, idx) => 
        result.assertions?.[idx]?.passed
      ),
      response_structure: Object.keys(result.data || {}),
      timestamp: new Date().toISOString()
    };
    
    setLearnedPatterns(prev => {
      const existing = prev.find(p => 
        p.url_pattern === pattern.url_pattern && p.method === pattern.method
      );
      if (existing) {
        return prev.map(p => 
          p.url_pattern === pattern.url_pattern && p.method === pattern.method 
            ? { ...p, ...pattern, confidence: (p.confidence || 0) + 1 }
            : p
        );
      }
      return [...prev, { ...pattern, confidence: 1 }];
    });
  };

  const generateSmartAssertions = (test) => {
    const suggestions = [];
    
    // Pattern-based suggestions
    learnedPatterns.forEach(pattern => {
      if (test.url.includes(pattern.url_pattern.replace('/:id', '')) && 
          test.method === pattern.method) {
        pattern.successful_assertions.forEach(assertion => {
          suggestions.push({
            ...assertion,
            confidence: pattern.confidence,
            reason: `Based on ${pattern.confidence} similar successful tests`
          });
        });
      }
    });
    
    // Rule-based suggestions
    if (test.method === 'POST') {
      suggestions.push({
        type: 'status',
        operator: 'equals',
        value: '201',
        reason: 'POST requests typically return 201 for successful creation'
      });
    }
    
    if (test.url.includes('/auth') || test.url.includes('/login')) {
      suggestions.push({
        type: 'body',
        path: 'token',
        operator: 'exists',
        value: '',
        reason: 'Authentication endpoints usually return tokens'
      });
    }
    
    if (test.url.includes('/users')) {
      suggestions.push({
        type: 'body',
        path: 'user.email',
        operator: 'matches_regex',
        value: '^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$',
        reason: 'User endpoints should validate email format'
      });
    }
    
    return suggestions;
  };

  const exportToWord = () => {
    const currentTest = tests[selectedTest];
    const result = testResults[selectedTest];
    
    // Create Word document content
    const wordContent = `
API Test Report
===============

Test Name: ${currentTest.name}
Method: ${currentTest.method}
URL: ${currentTest.url}
Date: ${new Date().toLocaleString()}

Test Configuration:
------------------
${currentTest.body ? `Request Body:\n${currentTest.body}\n` : ''}
Headers: ${JSON.stringify(currentTest.headers, null, 2)}

Assertions:
-----------
${currentTest.assertions.map((assertion, idx) => {
  const assertionResult = result?.assertions?.[idx];
  return `${idx + 1}. ${assertion.type} ${assertion.operator} ${assertion.value}
     ${assertion.key ? `Key: ${assertion.key}` : ''}
     ${assertion.path ? `Path: ${assertion.path}` : ''}
     Result: ${assertionResult ? (assertionResult.passed ? 'PASSED' : 'FAILED') : 'NOT RUN'}
     ${assertionResult && !assertionResult.passed ? `Expected: ${assertion.value}, Got: ${assertionResult.actualValue}` : ''}`;
}).join('\n\n')}

Test Results:
------------
${result ? `
Status: ${result.passed ? 'PASSED' : 'FAILED'}
Response Status: ${result.status}
Response Time: ${Math.round(result.responseTime)}ms
Timestamp: ${result.timestamp}

Response Data:
${JSON.stringify(result.data, null, 2)}

AI Recommendations:
------------------
${nextApiSuggestions.map(suggestion => `
- ${suggestion.name} (${suggestion.method})
  URL: ${suggestion.url}
  Description: ${suggestion.description}
`).join('')}

Generated Prompts:
-----------------
${aiPrompts.map(prompt => `
Category: ${prompt.category}
Title: ${prompt.title}
Description: ${prompt.description}
Assertion: ${prompt.assertion}
Example: ${prompt.example}
`).join('\n')}
` : 'Test not executed yet.'}
    `;

    // Create blob and download
    const blob = new Blob([wordContent], { type: 'application/msword' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${currentTest.name.replace(/\s+/g, '_')}_test_report.doc`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const updateTest = (index, field, value) => {
    const newTests = [...tests];
    newTests[index] = { ...newTests[index], [field]: value };
    setTests(newTests);
  };

  const addTest = () => {
    const newTest = {
      id: Date.now(),
      name: `New Test ${tests.length + 1}`,
      method: 'GET',
      url: '',
      headers: { 'Content-Type': 'application/json' },
      body: '',
      expectedStatus: 200,
      assertions: [
        { type: 'status', operator: 'equals', value: '200' }
      ],
      result: null,
      aiGenerated: false
    };
    setTests([...tests, newTest]);
    setSelectedTest(tests.length);
  };

  const deleteTest = (index) => {
    const newTests = tests.filter((_, i) => i !== index);
    setTests(newTests);
    if (selectedTest >= newTests.length) {
      setSelectedTest(Math.max(0, newTests.length - 1));
    }
  };

  const addAssertion = (testIndex, suggestion = null) => {
    const newTests = [...tests];
    const newAssertion = suggestion || {
      type: 'status',
      operator: 'equals',
      value: '',
      key: ''
    };
    newTests[testIndex].assertions.push(newAssertion);
    setTests(newTests);
  };

  const updateAssertion = (testIndex, assertionIndex, field, value) => {
    const newTests = [...tests];
    newTests[testIndex].assertions[assertionIndex][field] = value;
    setTests(newTests);
  };

  const removeAssertion = (testIndex, assertionIndex) => {
    const newTests = [...tests];
    newTests[testIndex].assertions.splice(assertionIndex, 1);
    setTests(newTests);
  };

  const generateAITests = async (baseUrl) => {
    setAgentMode(true);
    
    // Generate AI test suggestions
    const aiTests = [
      {
        name: 'Health Check',
        method: 'GET',
        url: `${baseUrl}/health`,
        assertions: [
          { type: 'status', operator: 'equals', value: '200' },
          { type: 'response_time', operator: 'less_than', value: '1000' }
        ]
      },
      {
        name: 'Get User Profile',
        method: 'GET',
        url: `${baseUrl}/users/profile`,
        headers: { 'Authorization': 'Bearer {{token}}' },
        assertions: [
          { type: 'status', operator: 'equals', value: '200' },
          { type: 'body', path: 'user.id', operator: 'exists', value: '' },
          { type: 'body', path: 'user.email', operator: 'matches_regex', value: '^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$' }
        ]
      },
      {
        name: 'Create New User',
        method: 'POST',
        url: `${baseUrl}/users`,
        body: JSON.stringify({
          name: "Test User",
          email: "newuser@example.com",
          password: "securepass123"
        }, null, 2),
        assertions: [
          { type: 'status', operator: 'equals', value: '201' },
          { type: 'body', path: 'user.id', operator: 'exists', value: '' },
          { type: 'header', key: 'Location', operator: 'exists', value: '' }
        ]
      }
    ];

    setAiSuggestions(aiTests);
    
    // Generate detailed prompts
    setAiPrompts(detailedPrompts.flatMap(category => 
      category.prompts.map(prompt => ({
        ...prompt,
        category: category.category
      }))
    ));
  };

  const applyAISuggestion = (suggestion) => {
    const newTest = {
      id: Date.now(),
      ...suggestion,
      headers: suggestion.headers || { 'Content-Type': 'application/json' },
      body: suggestion.body || '',
      expectedStatus: suggestion.assertions.find(a => a.type === 'status')?.value || 200,
      result: null,
      aiGenerated: true
    };
    setTests([...tests, newTest]);
  };

  const runTest = async (testIndex) => {
    const test = tests[testIndex];
    setIsRunning(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, Math.random() * 2000 + 500));
      
      // Mock response data
      const mockResponse = {
        status: test.expectedStatus,
        statusText: 'OK',
        headers: {
          'content-type': 'application/json',
          'x-response-time': '245ms',
          'x-ratelimit-remaining': '99'
        },
        data: test.method === 'POST' && test.url.includes('auth') ? 
          { 
            token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...', 
            user: { 
              id: 1, 
              email: 'test@example.com',
              name: 'Test User'
            } 
          } :
          test.method === 'POST' && test.url.includes('users') ?
          {
            user: {
              id: Math.floor(Math.random() * 1000),
              name: 'Test User',
              email: 'newuser@example.com',
              created_at: new Date().toISOString()
            }
          } :
          { 
            success: true, 
            message: 'Operation completed', 
            timestamp: new Date().toISOString(),
            data: { count: 5, items: [] }
          },
        responseTime: Math.random() * 1000 + 100
      };

      // Evaluate assertions
      const assertionResults = test.assertions.map(assertion => {
        let passed = false;
        let actualValue = '';

        switch (assertion.type) {
          case 'status':
            actualValue = mockResponse.status.toString();
            passed = evaluateAssertion(actualValue, assertion.operator, assertion.value);
            break;
          case 'header':
            actualValue = mockResponse.headers[assertion.key?.toLowerCase()] || '';
            passed = evaluateAssertion(actualValue, assertion.operator, assertion.value);
            break;
          case 'body':
            actualValue = getNestedValue(mockResponse.data, assertion.path);
            passed = evaluateAssertion(actualValue, assertion.operator, assertion.value);
            break;
          case 'response_time':
            actualValue = mockResponse.responseTime.toString();
            passed = evaluateAssertion(actualValue, assertion.operator, assertion.value);
            break;
          case 'json_schema':
            actualValue = typeof getNestedValue(mockResponse.data, assertion.path);
            passed = evaluateAssertion(actualValue, assertion.operator, assertion.value);
            break;
          case 'regex':
            actualValue = getNestedValue(mockResponse.data, assertion.path)?.toString() || '';
            passed = evaluateAssertion(actualValue, assertion.operator, assertion.value);
            break;
        }

        return {
          ...assertion,
          passed,
          actualValue
        };
      });

      const testResult = {
        ...mockResponse,
        assertions: assertionResults,
        passed: assertionResults.every(a => a.passed),
        timestamp: new Date().toISOString()
      };

      setTestResults(prev => ({
        ...prev,
        [testIndex]: testResult
      }));

      // Learn from patterns and generate next API calls
      learnFromPatterns(test, testResult);
      const nextSuggestions = generateNextApiCalls(test, testResult);
      setNextApiSuggestions(nextSuggestions);

    } catch (error) {
      setTestResults(prev => ({
        ...prev,
        [testIndex]: {
          error: error.message,
          passed: false,
          timestamp: new Date().toISOString()
        }
      }));
    } finally {
      setIsRunning(false);
    }
  };

  const evaluateAssertion = (actual, operator, expected) => {
    const actualStr = actual?.toString() || '';
    const expectedStr = expected?.toString() || '';
    
    switch (operator) {
      case 'equals':
        return actualStr === expectedStr;
      case 'not_equals':
        return actualStr !== expectedStr;
      case 'contains':
        return actualStr.includes(expectedStr);
      case 'not_contains':
        return !actualStr.includes(expectedStr);
      case 'exists':
        return actual !== undefined && actual !== null && actual !== '';
      case 'not_exists':
        return actual === undefined || actual === null || actual === '';
      case 'greater_than':
        return parseFloat(actual) > parseFloat(expected);
      case 'less_than':
        return parseFloat(actual) < parseFloat(expected);
      case 'matches_regex':
      case 'matches':
        try {
          const regex = new RegExp(expectedStr);
          return regex.test(actualStr);
        } catch {
          return false;
        }
      case 'not_matches':
        try {
          const regex = new RegExp(expectedStr);
          return !regex.test(actualStr);
        } catch {
          return false;
        }
      case 'has_length':
        return (actual?.length || 0) === parseInt(expected);
      case 'is_array':
        return Array.isArray(actual);
      case 'is_object':
        return typeof actual === 'object' && !Array.isArray(actual);
      case 'in_range':
        const [min, max] = expectedStr.split(',').map(v => parseFloat(v.trim()));
        const val = parseFloat(actual);
        return val >= min && val <= max;
      case 'between':
        const [minTime, maxTime] = expectedStr.split(',').map(v => parseFloat(v.trim()));
        const time = parseFloat(actual);
        return time >= minTime && time <= maxTime;
      case 'validates_against':
        // Simplified schema validation
        return true; // Would implement JSON schema validation
      case 'has_property':
        return actual && actual.hasOwnProperty(expectedStr);
      case 'property_type':
        return typeof actual === expectedStr;
      default:
        return false;
    }
  };

  const getNestedValue = (obj, path) => {
    if (!path) return obj;
    return path.split('.').reduce((current, key) => current?.[key], obj);
  };

  const runAllTests = async () => {
    setIsRunning(true);
    for (let i = 0; i < tests.length; i++) {
      await runTest(i);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    setIsRunning(false);
  };

  const exportTests = () => {
    const dataStr = JSON.stringify(tests, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'api-tests.json';
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const importTests = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedTests = JSON.parse(e.target.result);
          setTests(importedTests);
        } catch (error) {
          alert('Error importing tests: Invalid JSON format');
        }
      };
      reader.readAsText(file);
    }
  };

  const getTestStatusIcon = (testIndex) => {
    const result = testResults[testIndex];
    if (!result) return null;
    
    if (result.error) return <XCircle className="w-4 h-4 text-red-500" />;
    return result.passed ? 
      <CheckCircle className="w-4 h-4 text-green-500" /> : 
      <XCircle className="w-4 h-4 text-red-500" />;
  };

  const currentTest = tests[selectedTest] || tests[0];
  const currentResult = testResults[selectedTest];
  const smartAssertions = currentTest ? generateSmartAssertions(currentTest) : [];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-1/4 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-800 mb-4">🤖 Agentic API Tester</h1>
          <div className="flex gap-2 mb-4">
            <button
              onClick={addTest}
              className="flex items-center gap-1 px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
            >
              <Plus className="w-4 h-4" /> Add Test
            </button>
            <button
              onClick={runAllTests}
              disabled={isRunning}
              className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700 disabled:opacity-50"
            >
              <Play className="w-4 h-4" /> Run All
            </button>
          </div>
          <div className="flex gap-2">
            <button
              onClick={exportTests}
              className="flex items-center gap-1 px-2 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700"
            >
              <Download className="w-3 h-3" /> Export JSON
            </button>
            <button
              onClick={exportToWord}
              className="flex items-center gap-1 px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              <FileText className="w-3 h-3" /> Export Word
            </button>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center gap-1 px-2 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700"
            >
              <Upload className="w-3 h-3" /> Import
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".json"
              onChange={importTests}
              className="hidden"
            />
          </div>
        </div>

        {/* AI Agent Mode */}
        <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-purple-50 to-blue-50">
          <div className="flex items-center gap-2 mb-2">
            <Brain className="w-4 h-4 text-purple-600" />
            <span className="text-sm font-medium text-purple-800">AI Test Generator</span>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Enter API base URL..."
              className="flex-1 px-2 py-1 text-xs border border-gray-300 rounded"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  generateAITests(e.target.value);
                }
              }}
            />
            <button
              onClick={() => generateAITests('https://api.example.com')}
              className="px-2 py-1 text-xs bg-purple-600 text-white rounded hover:bg-purple-700"
            >
              Generate
            </button>
          </div>
          {aiSuggestions.length > 0 && (
            <div className="mt-2 max-h-32 overflow-y-auto">
              {aiSuggestions.map((suggestion, idx) => (
                <div key={idx} className="flex items-center justify-between p-2 bg-white rounded border border-purple-200 mb-1">
                  <span className="text-xs text-gray-700">{suggestion.name}</span>
                  <button
                    onClick={() => applyAISuggestion(suggestion)}
                    className="px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded hover:bg-purple-200"
                  >
                    Add
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Test List */}
        <div className="flex-1 overflow-y-auto">
          {tests.map((test, index) => (
            <div
              key={test.id}
              className={`p-3 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${
                selectedTest === index ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
              }`}
              onClick={() => setSelectedTest(index)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {getTestStatusIcon(index)}
                  <span className="font-medium text-sm">{test.name}</span>
                  {test.aiGenerated && (
                    <span className="px-1 py-0.5 text-xs bg-purple-100 text-purple-600 rounded">AI</span>
                  )}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteTest(index);
                  }}
                  className="text-red-500 hover:text-red-700"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                <span className={`px-2 py-0.5 rounded ${
                  test.method === 'GET' ? 'bg-blue-100 text-blue-700' :
                  test.method === 'POST' ? 'bg-green-100 text-green-700' :
                  test.method === 'PUT' ? 'bg-yellow-100 text-yellow-700' :
                  test.method === 'DELETE' ? 'bg-red-100 text-red-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {test.method}
                </span>
                <span className="ml-2 truncate">{test.url}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Tab Navigation */}
        <div className="bg-white border-b border-gray-200">
          <div className="flex">
            {['config', 'assertions', 'ai-prompts', 'next-calls', 'results'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-3 text-sm font-medium border-b-2 ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab === 'config' && <Settings className="w-4 h-4 inline mr-2" />}
                {tab === 'assertions' && <CheckCircle className="w-4 h-4 inline mr-2" />}
                {tab === 'ai-prompts' && <Brain className="w-4 h-4 inline mr-2" />}
                {tab === 'next-calls' && <ArrowRight className="w-4 h-4 inline mr-2" />}
                {tab === 'results' && <BarChart3 className="w-4 h-4 inline mr-2" />}
                {tab.charAt(0).toUpperCase() + tab.slice(1).replace('-', ' ')}
              </button>
            ))}
          </div>
        </div>

        {currentTest && (
          <>
            {/* Test Configuration Tab */}
            {activeTab === 'config' && (
              <div className="bg-white border-b border-gray-200 p-4">
                <div className="flex items-center justify-between mb-4">
                  <input
                    type="text"
                    value={currentTest.name}
                    onChange={(e) => updateTest(selectedTest, 'name', e.target.value)}
                    className="text-lg font-semibold bg-transparent border-none outline-none"
                  />
                  <button
                    onClick={() => runTest(selectedTest)}
                    disabled={isRunning}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Play className="w-4 h-4" />
                    {isRunning ? 'Running...' : 'Run Test'}
                  </button>
                </div>

                <div className="grid grid-cols-1 gap-4">
                  <div className="flex gap-4">
                    <select
                      value={currentTest.method}
                      onChange={(e) => updateTest(selectedTest, 'method', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded"
                    >
                      {methods.map(method => (
                        <option key={method} value={method}>{method}</option>
                      ))}
                    </select>
                    <input
                      type="text"
                      placeholder="Enter API URL..."
                      value={currentTest.url}
                      onChange={(e) => updateTest(selectedTest, 'url', e.target.value)}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded"
                    />
                  </div>

                  {(currentTest.method === 'POST' || currentTest.method === 'PUT' || currentTest.method === 'PATCH') && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Request Body</label>
                      <textarea
                        value={currentTest.body}
                        onChange={(e) => updateTest(selectedTest, 'body', e.target.value)}
                        placeholder="Enter JSON body..."
                        className="w-full h-32 px-3 py-2 border border-gray-300 rounded font-mono text-sm"
                      />
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Assertions Tab */}
            {activeTab === 'assertions' && (
              <div className="bg-white border-b border-gray-200 p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-medium">Smart Assertions</h3>
                  <button
                    onClick={() => addAssertion(selectedTest)}
                    className="flex items-center gap-1 px-2 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                  >
                    <Plus className="w-4 h-4" /> Add Assertion
                  </button>
                </div>

                {/* Smart Suggestions */}
                {smartAssertions.length > 0 && (
                  <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
                    <h4 className="text-sm font-medium text-blue-800 mb-2 flex items-center gap-1">
                      <Lightbulb className="w-4 h-4" />
                      AI Suggested Assertions
                    </h4>
                    <div className="space-y-2">
                      {smartAssertions.slice(0, 3).map((suggestion, idx) => (
                        <div key={idx} className="flex items-center justify-between p-2 bg-white rounded border">
                          <div className="text-sm">
                            <span className="font-medium">{suggestion.type}</span>
                            {suggestion.path && <span className="text-gray-600"> → {suggestion.path}</span>}
                            <span className="text-gray-600"> {suggestion.operator} {suggestion.value}</span>
                            <div className="text-xs text-blue-600">{suggestion.reason}</div>
                          </div>
                          <button
                            onClick={() => addAssertion(selectedTest, suggestion)}
                            className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                          >
                            Add
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {currentTest.assertions.map((assertion, assertionIndex) => {
                    const result = currentResult?.assertions?.[assertionIndex];
                    return (
                      <div key={assertionIndex} className={`flex items-center gap-2 p-3 border rounded ${
                        result ? (result.passed ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50') : 'border-gray-200'
                      }`}>
                        {result && (
                          result.passed ? 
                            <CheckCircle className="w-4 h-4 text-green-500" /> : 
                            <XCircle className="w-4 h-4 text-red-500" />
                        )}
                        
                        <select
                          value={assertion.type}
                          onChange={(e) => updateAssertion(selectedTest, assertionIndex, 'type', e.target.value)}
                          className="px-2 py-1 border border-gray-300 rounded text-sm"
                        >
                          {assertionTypes.map(type => (
                            <option key={type} value={type}>{type.replace('_', ' ')}</option>
                          ))}
                        </select>

                        {(assertion.type === 'header' || assertion.type === 'body') && (
                          <input
                            type="text"
                            placeholder={assertion.type === 'header' ? 'Header key' : 'JSON path (e.g., user.id)'}
                            value={assertion.key || assertion.path || ''}
                            onChange={(e) => updateAssertion(selectedTest, assertionIndex, assertion.type === 'header' ? 'key' : 'path', e.target.value)}
                            className="px-2 py-1 border border-gray-300 rounded text-sm"
                          />
                        )}

                        <select
                          value={assertion.operator}
                          onChange={(e) => updateAssertion(selectedTest, assertionIndex, 'operator', e.target.value)}
                          className="px-2 py-1 border border-gray-300 rounded text-sm"
                        >
                          {operators[assertion.type]?.map(op => (
                            <option key={op} value={op}>{op.replace('_', ' ')}</option>
                          ))}
                        </select>

                        {!['exists', 'not_exists', 'is_array', 'is_object'].includes(assertion.operator) && (
                          <input
                            type="text"
                            placeholder="Expected value"
                            value={assertion.value}
                            onChange={(e) => updateAssertion(selectedTest, assertionIndex, 'value', e.target.value)}
                            className="px-2 py-1 border border-gray-300 rounded text-sm"
                          />
                        )}

                        {result && !result.passed && (
                          <span className="text-xs text-red-600">
                            Expected: {assertion.value}, Got: {result.actualValue}
                          </span>
                        )}

                        <button
                          onClick={() => removeAssertion(selectedTest, assertionIndex)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* AI Prompts Tab */}
            {activeTab === 'ai-prompts' && (
              <div className="flex-1 bg-white p-4 overflow-y-auto">
                <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
                  <Brain className="w-5 h-5 text-purple-600" />
                  Detailed AI Testing Prompts
                </h3>
                <div className="space-y-4">
                  {detailedPrompts.map((category, categoryIdx) => (
                    <div key={categoryIdx} className="border border-gray-200 rounded-lg">
                      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                        <h4 className="font-semibold text-gray-800">{category.category}</h4>
                      </div>
                      <div className="p-4 space-y-3">
                        {category.prompts.map((prompt, promptIdx) => (
                          <div key={promptIdx} className="p-3 bg-blue-50 border border-blue-200 rounded">
                            <h5 className="font-medium text-blue-800 mb-2">{prompt.title}</h5>
                            <p className="text-sm text-gray-700 mb-2">{prompt.description}</p>
                            <div className="text-xs text-gray-600 mb-1">
                              <strong>Assertion:</strong> {prompt.assertion}
                            </div>
                            <div className="text-xs text-gray-600 mb-3">
                              <strong>Example:</strong> <code className="bg-gray-100 px-1 rounded">{prompt.example}</code>
                            </div>
                            <button
                              onClick={() => {
                                setSelectedPrompt(prompt.example);
                                navigator.clipboard.writeText(prompt.example);
                              }}
                              className="flex items-center gap-1 px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                            >
                              <Copy className="w-3 h-3" />
                              Copy Example
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Next API Calls Tab */}
            {activeTab === 'next-calls' && (
              <div className="flex-1 bg-white p-4 overflow-y-auto">
                <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
                  <ArrowRight className="w-5 h-5 text-green-600" />
                  Next Recommended API Calls
                </h3>
                {nextApiSuggestions.length > 0 ? (
                  <div className="space-y-3">
                    {nextApiSuggestions.map((suggestion, idx) => (
                      <div key={idx} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium text-gray-800">{suggestion.name}</h4>
                          <span className={`px-2 py-1 rounded text-xs ${
                            suggestion.method === 'GET' ? 'bg-blue-100 text-blue-700' :
                            suggestion.method === 'POST' ? 'bg-green-100 text-green-700' :
                            suggestion.method === 'PUT' ? 'bg-yellow-100 text-yellow-700' :
                            suggestion.method === 'DELETE' ? 'bg-red-100 text-red-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {suggestion.method}
                          </span>
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          <code className="bg-gray-100 px-1 rounded">{suggestion.url}</code>
                        </div>
                        <p className="text-sm text-gray-700 mb-3">{suggestion.description}</p>
                        <div className="flex gap-2">
                          <button
                            onClick={() => {
                              const newTest = {
                                id: Date.now(),
                                name: suggestion.name,
                                method: suggestion.method,
                                url: suggestion.url,
                                headers: suggestion.headers || { 'Content-Type': 'application/json' },
                                body: suggestion.body || '',
                                expectedStatus: 200,
                                assertions: [
                                  { type: 'status', operator: 'equals', value: '200' }
                                ],
                                result: null,
                                aiGenerated: true
                              };
                              setTests([...tests, newTest]);
                              setSelectedTest(tests.length);
                              setActiveTab('config');
                            }}
                            className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                          >
                            <Plus className="w-3 h-3" />
                            Add Test
                          </button>
                          <button
                            onClick={() => {
                              const testCode = `${suggestion.method} ${suggestion.url}`;
                              navigator.clipboard.writeText(testCode);
                            }}
                            className="flex items-center gap-1 px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700"
                          >
                            <Copy className="w-3 h-3" />
                            Copy
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    <ArrowRight className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                    <p>Run a test to get AI-powered next API call suggestions</p>
                  </div>
                )}
              </div>
            )}

            {/* Test Results Tab */}
            {activeTab === 'results' && currentResult && (
              <div className="flex-1 bg-white p-4 overflow-y-auto">
                <h3 className="text-lg font-medium mb-3 flex items-center gap-2">
                  Test Results
                  {currentResult.passed ? 
                    <CheckCircle className="w-5 h-5 text-green-500" /> : 
                    <XCircle className="w-5 h-5 text-red-500" />
                  }
                </h3>

                {currentResult.error ? (
                  <div className="p-4 bg-red-50 border border-red-200 rounded">
                    <p className="text-red-700">Error: {currentResult.error}</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                      <div className="p-3 bg-gray-50 rounded">
                        <div className="text-sm text-gray-600">Status</div>
                        <div className="text-lg font-semibold">{currentResult.status}</div>
                      </div>
                      <div className="p-3 bg-gray-50 rounded">
                        <div className="text-sm text-gray-600">Response Time</div>
                        <div className="text-lg font-semibold">{Math.round(currentResult.responseTime)}ms</div>
                      </div>
                      <div className="p-3 bg-gray-50 rounded">
                        <div className="text-sm text-gray-600">Assertions</div>
                        <div className="text-lg font-semibold">
                          {currentResult.assertions?.filter(a => a.passed).length || 0} / {currentResult.assertions?.length || 0}
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2">Response Data</h4>
                      <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
                        {JSON.stringify(currentResult.data, null, 2)}
                      </pre>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2">Response Headers</h4>
                      <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
                        {JSON.stringify(currentResult.headers, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Default content when no result */}
            {activeTab === 'results' && !currentResult && (
              <div className="flex-1 bg-white p-4 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <BarChart3 className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>Run the test to see results here</p>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default AgenticAPITester;