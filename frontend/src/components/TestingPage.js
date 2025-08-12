import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import {
  GitHub,
  Psychology,
  PlayArrow,
  Send,
  Refresh
} from '@mui/icons-material';
import ApiService from '../services/ApiService';

function TestingPage() {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Form state
  const [formData, setFormData] = useState({
    githubUrl: '',
    branch: 'main',
    testDescription: ''
  });
  
  // Results state
  const [analysisResult, setAnalysisResult] = useState(null);
  const [executionResult, setExecutionResult] = useState(null);

  const steps = ['Repository Input', 'Analysis & Generation', 'Test Execution'];

  const handleInputChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value
    });
  };

  const validateGitHubUrl = (url) => {
    const githubPattern = /^https:\/\/github\.com\/[^\/]+\/[^\/]+/;
    return githubPattern.test(url);
  };

  const handleAnalyzeRepository = async () => {
    if (!formData.githubUrl.trim()) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    if (!validateGitHubUrl(formData.githubUrl)) {
      setError('Please enter a valid GitHub repository URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await ApiService.analyzeRepository(formData);
      setAnalysisResult(result);
      setActiveStep(1);
    } catch (err) {
      setError(err.message || 'Failed to analyze repository');
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteTests = async () => {
    if (!analysisResult || !analysisResult.generated_tests) {
      setError('No tests available to execute');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await ApiService.executeTests({
        repository_url: formData.githubUrl,
        generated_tests: analysisResult.generated_tests
      });
      setExecutionResult(result);
      setActiveStep(2);
      
      // Navigate to results page with data
      navigate('/results', { 
        state: { 
          analysisResult, 
          executionResult: result,
          repositoryUrl: formData.githubUrl 
        }
      });
    } catch (err) {
      setError(err.message || 'Failed to execute tests');
    } finally {
      setLoading(false);
    }
  };

  const handleFullAnalysis = async () => {
    if (!formData.githubUrl.trim()) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    if (!validateGitHubUrl(formData.githubUrl)) {
      setError('Please enter a valid GitHub repository URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await ApiService.fullAnalysis(formData);
      setAnalysisResult(result.analysis);
      setExecutionResult(result.execution);
      setActiveStep(2);
      
      // Navigate to results page with full data
      navigate('/results', { 
        state: { 
          analysisResult: result.analysis, 
          executionResult: result.execution,
          fullReport: result.full_report,
          repositoryUrl: formData.githubUrl 
        }
      });
    } catch (err) {
      setError(err.message || 'Failed to perform full analysis');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      githubUrl: '',
      branch: 'main',
      testDescription: ''
    });
    setAnalysisResult(null);
    setExecutionResult(null);
    setActiveStep(0);
    setError('');
  };

  return (
    <Box>
      <Typography variant="h2" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
        API Testing Workflow
      </Typography>

      {/* Progress Stepper */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Grid container spacing={4}>
        {/* Input Form */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <GitHub sx={{ mr: 2 }} />
              Repository Configuration
            </Typography>
            
            <Box component="form" sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="GitHub Repository URL"
                placeholder="https://github.com/username/repository"
                value={formData.githubUrl}
                onChange={handleInputChange('githubUrl')}
                margin="normal"
                required
                helperText="Enter the URL of a public GitHub repository"
              />
              
              <FormControl fullWidth margin="normal">
                <InputLabel>Branch</InputLabel>
                <Select
                  value={formData.branch}
                  label="Branch"
                  onChange={handleInputChange('branch')}
                >
                  <MenuItem value="main">main</MenuItem>
                  <MenuItem value="master">master</MenuItem>
                  <MenuItem value="develop">develop</MenuItem>
                  <MenuItem value="dev">dev</MenuItem>
                </Select>
              </FormControl>
              
              <TextField
                fullWidth
                label="Test Description (Optional)"
                placeholder="Describe specific testing requirements..."
                value={formData.testDescription}
                onChange={handleInputChange('testDescription')}
                margin="normal"
                multiline
                rows={3}
                helperText="Optional: Describe specific testing scenarios you want to include"
              />
            </Box>

            <Divider sx={{ my: 3 }} />

            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                startIcon={<Psychology />}
                onClick={handleAnalyzeRepository}
                disabled={loading || !formData.githubUrl.trim()}
                sx={{ flex: 1, minWidth: 150 }}
              >
                {loading && activeStep === 0 ? (
                  <CircularProgress size={20} />
                ) : (
                  'Analyze Repository'
                )}
              </Button>
              
              <Button
                variant="contained"
                color="secondary"
                startIcon={<Send />}
                onClick={handleFullAnalysis}
                disabled={loading || !formData.githubUrl.trim()}
                sx={{ flex: 1, minWidth: 150 }}
              >
                {loading ? (
                  <CircularProgress size={20} />
                ) : (
                  'Full Analysis'
                )}
              </Button>
              
              <Button
                variant="outlined"
                startIcon={<Refresh />}
                onClick={resetForm}
                disabled={loading}
              >
                Reset
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Analysis Results */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Analysis Results
            </Typography>
            
            {analysisResult ? (
              <Card sx={{ mt: 2 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Repository: {analysisResult.repository}
                  </Typography>
                  
                  {analysisResult.analysis_report && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Framework: {analysisResult.analysis_report.repository_analysis?.framework || 'Unknown'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Language: {analysisResult.analysis_report.repository_analysis?.language || 'Unknown'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Tests Generated: {analysisResult.generated_tests?.length || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Endpoints Detected: {analysisResult.analysis_report.code_analysis?.detected_endpoints || 0}
                      </Typography>
                    </Box>
                  )}

                  {analysisResult.generated_tests && analysisResult.generated_tests.length > 0 && (
                    <Box sx={{ mt: 3 }}>
                      <Button
                        variant="contained"
                        startIcon={<PlayArrow />}
                        onClick={handleExecuteTests}
                        disabled={loading}
                        fullWidth
                      >
                        {loading && activeStep === 1 ? (
                          <CircularProgress size={20} />
                        ) : (
                          `Execute ${analysisResult.generated_tests.length} Tests`
                        )}
                      </Button>
                    </Box>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4, color: 'text.secondary' }}>
                <GitHub sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
                <Typography variant="body1">
                  Enter a GitHub repository URL to start analysis
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Quick Examples */}
      <Paper sx={{ p: 3, mt: 4, backgroundColor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          Example Repositories
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Try these sample repositories to see the platform in action:
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {[
            'https://github.com/pallets/flask',
            'https://github.com/tiangolo/fastapi',
            'https://github.com/expressjs/express'
          ].map((url) => (
            <Button
              key={url}
              variant="outlined"
              size="small"
              onClick={() => setFormData({ ...formData, githubUrl: url })}
              disabled={loading}
            >
              {url.split('/').pop()}
            </Button>
          ))}
        </Box>
      </Paper>
    </Box>
  );
}

export default TestingPage;