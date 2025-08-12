import React from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  LinearProgress,
  Divider
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Error,
  Speed,
  Assessment,
  GitHub,
  Download,
  Refresh
} from '@mui/icons-material';
import JsonDisplay from './JsonDisplay';

function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const { 
    analysisResult, 
    executionResult, 
    fullReport,
    repositoryUrl 
  } = location.state || {};

  if (!analysisResult && !executionResult) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h4" gutterBottom>
          No Results Available
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Please run an analysis first to see results here.
        </Typography>
        <Button
          variant="contained"
          onClick={() => navigate('/testing')}
          startIcon={<Refresh />}
        >
          Start New Analysis
        </Button>
      </Box>
    );
  }

  const summary = executionResult?.summary || {};
  const successRate = summary.total_tests ? (summary.passed / summary.total_tests * 100) : 0;

  return (
    <Box>
      <Typography variant="h2" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
        Test Results
      </Typography>

      {/* Repository Header */}
      {repositoryUrl && (
        <Paper sx={{ p: 3, mb: 4, backgroundColor: 'primary.main', color: 'white' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <GitHub sx={{ mr: 2 }} />
              <Box>
                <Typography variant="h6">
                  Repository Analysis Results
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  {repositoryUrl}
                </Typography>
              </Box>
            </Box>
            <Button
              variant="outlined"
              sx={{ color: 'white', borderColor: 'white' }}
              startIcon={<Download />}
            >
              Export Report
            </Button>
          </Box>
        </Paper>
      )}

      <Grid container spacing={4}>
        {/* Summary Cards */}
        <Grid item xs={12}>
          <Grid container spacing={3}>
            {/* Tests Summary */}
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="primary">
                    {summary.total_tests || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Tests
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Success Rate */}
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color={successRate >= 80 ? 'success.main' : successRate >= 50 ? 'warning.main' : 'error.main'}>
                    {successRate.toFixed(1)}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Success Rate
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Passed Tests */}
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="success.main">
                    {summary.passed || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Passed
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Failed Tests */}
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="error.main">
                    {summary.failed || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Failed
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>

        {/* Success Rate Progress */}
        {summary.total_tests > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Test Execution Progress
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Box sx={{ width: '100%', mr: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={successRate} 
                    sx={{ height: 10, borderRadius: 5 }}
                    color={successRate >= 80 ? 'success' : successRate >= 50 ? 'warning' : 'error'}
                  />
                </Box>
                <Box sx={{ minWidth: 35 }}>
                  <Typography variant="body2" color="text.secondary">
                    {successRate.toFixed(1)}%
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {summary.passed} of {summary.total_tests} tests passed
              </Typography>
            </Paper>
          </Grid>
        )}

        {/* Analysis Report */}
        {analysisResult?.analysis_report && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <Assessment sx={{ mr: 2 }} />
                Analysis Report
              </Typography>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography>Repository Analysis</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <JsonDisplay 
                    data={analysisResult.analysis_report.repository_analysis || {}}
                  />
                </AccordionDetails>
              </Accordion>

              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography>Code Analysis</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <JsonDisplay 
                    data={analysisResult.analysis_report.code_analysis || {}}
                  />
                </AccordionDetails>
              </Accordion>

              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography>Test Generation</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <JsonDisplay 
                    data={analysisResult.analysis_report.test_generation || {}}
                  />
                </AccordionDetails>
              </Accordion>
            </Paper>
          </Grid>
        )}

        {/* Execution Report */}
        {executionResult?.execution_report && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <Speed sx={{ mr: 2 }} />
                Execution Report
              </Typography>

              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography>Execution Summary</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <JsonDisplay 
                    data={executionResult.execution_report.execution_summary || {}}
                  />
                </AccordionDetails>
              </Accordion>

              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography>Performance Metrics</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <JsonDisplay 
                    data={executionResult.execution_report.performance_metrics || {}}
                  />
                </AccordionDetails>
              </Accordion>

              {executionResult.execution_report.failure_analysis && (
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography>Failure Analysis</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <JsonDisplay 
                      data={executionResult.execution_report.failure_analysis}
                    />
                  </AccordionDetails>
                </Accordion>
              )}
            </Paper>
          </Grid>
        )}

        {/* Test Results Table */}
        {executionResult?.test_results && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Individual Test Results
              </Typography>
              
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Test Name</TableCell>
                      <TableCell>Method</TableCell>
                      <TableCell>Endpoint</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Response Time</TableCell>
                      <TableCell>Status Code</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {executionResult.test_results.slice(0, 20).map((result, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          {result.test?.name || `Test ${index + 1}`}
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={result.test?.method || 'GET'} 
                            size="small"
                            color="primary"
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell sx={{ fontFamily: 'monospace' }}>
                          {result.test?.endpoint || '/'}
                        </TableCell>
                        <TableCell>
                          {result.success ? (
                            <Chip 
                              icon={<CheckCircle />} 
                              label="Passed" 
                              color="success" 
                              size="small"
                            />
                          ) : (
                            <Chip 
                              icon={<Error />} 
                              label="Failed" 
                              color="error" 
                              size="small"
                            />
                          )}
                        </TableCell>
                        <TableCell>
                          {result.execution_time ? `${(result.execution_time * 1000).toFixed(0)}ms` : 'N/A'}
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={result.response?.status_code || 'N/A'}
                            size="small"
                            color={
                              result.response?.status_code >= 200 && result.response?.status_code < 300 
                                ? 'success' 
                                : result.response?.status_code >= 400 
                                ? 'error' 
                                : 'default'
                            }
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              
              {executionResult.test_results.length > 20 && (
                <Alert severity="info" sx={{ mt: 2 }}>
                  Showing first 20 results. Total: {executionResult.test_results.length} tests
                </Alert>
              )}
            </Paper>
          </Grid>
        )}

        {/* Recommendations */}
        {(analysisResult?.analysis_report?.recommendations || executionResult?.execution_report?.recommendations) && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Recommendations
              </Typography>
              
              {analysisResult?.analysis_report?.recommendations && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Analysis Recommendations
                  </Typography>
                  {analysisResult.analysis_report.recommendations.map((rec, index) => (
                    <Alert severity="info" key={index} sx={{ mb: 1 }}>
                      {rec}
                    </Alert>
                  ))}
                </Box>
              )}
              
              {executionResult?.execution_report?.recommendations && (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Execution Recommendations
                  </Typography>
                  {executionResult.execution_report.recommendations.map((rec, index) => (
                    <Alert severity="warning" key={index} sx={{ mb: 1 }}>
                      {rec}
                    </Alert>
                  ))}
                </Box>
              )}
            </Paper>
          </Grid>
        )}
      </Grid>

      {/* Actions */}
      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Button
          variant="outlined"
          onClick={() => navigate('/testing')}
          startIcon={<Refresh />}
          sx={{ mr: 2 }}
        >
          New Analysis
        </Button>
        <Button
          variant="contained"
          href={repositoryUrl}
          target="_blank"
          startIcon={<GitHub />}
        >
          View Repository
        </Button>
      </Box>
    </Box>
  );
}

export default ResultsPage;