import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Paper,
  Typography,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  GitHub,
  Psychology,
  PlayArrow,
  Assessment,
  AutoAwesome,
  Speed,
  Security,
  Integration
} from '@mui/icons-material';

function HomePage() {
  const navigate = useNavigate();

  const features = [
    {
      icon: <GitHub />,
      title: 'GitHub Integration',
      description: 'Automatically analyze any public GitHub repository to understand its API structure and endpoints.'
    },
    {
      icon: <Psychology />,
      title: 'AI-Powered Test Generation',
      description: 'Use GPT-4 to generate comprehensive test scenarios based on your repository analysis.'
    },
    {
      icon: <PlayArrow />,
      title: 'Automated Execution',
      description: 'Execute all generated tests automatically with intelligent endpoint detection and validation.'
    },
    {
      icon: <Assessment />,
      title: 'Detailed Reporting',
      description: 'Get comprehensive reports with performance metrics, failure analysis, and recommendations.'
    }
  ];

  const benefits = [
    'Natural language test definition',
    'Automatic test generation from code analysis',
    'Intelligent test execution with multiple assertions',
    'Performance and security testing built-in',
    'CI/CD pipeline integration ready',
    'Extensible architecture for custom agents'
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Paper 
        elevation={3} 
        sx={{ 
          p: 6, 
          mb: 4, 
          background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
          color: 'white',
          textAlign: 'center'
        }}
      >
        <Typography variant="h1" gutterBottom>
          Agent API Testing Platform
        </Typography>
        <Typography variant="h5" sx={{ mb: 3, opacity: 0.9 }}>
          Intelligent API testing with LLM-powered test generation
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, maxWidth: 800, mx: 'auto' }}>
          Analyze GitHub repositories, generate comprehensive API tests using AI, 
          and execute them automatically with detailed reporting and performance analysis.
        </Typography>
        <Button
          variant="contained"
          size="large"
          sx={{ 
            mt: 2, 
            px: 4, 
            py: 1.5,
            backgroundColor: 'white',
            color: 'primary.main',
            '&:hover': {
              backgroundColor: 'grey.100'
            }
          }}
          onClick={() => navigate('/testing')}
          startIcon={<AutoAwesome />}
        >
          Start Testing Now
        </Button>
      </Paper>

      {/* Features Section */}
      <Typography variant="h2" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
        Platform Features
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: 'primary.main', mr: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6">
                    {feature.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Benefits Section */}
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <Speed sx={{ mr: 2, color: 'primary.main' }} />
              Key Benefits
            </Typography>
            <List>
              {benefits.map((benefit, index) => (
                <ListItem key={index} sx={{ py: 0.5 }}>
                  <ListItemIcon>
                    <AutoAwesome color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={benefit} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <Security sx={{ mr: 2, color: 'primary.main' }} />
              How It Works
            </Typography>
            <List>
              <ListItem sx={{ py: 1 }}>
                <ListItemIcon>
                  <Typography variant="h6" color="primary">1</Typography>
                </ListItemIcon>
                <ListItemText 
                  primary="Repository Analysis" 
                  secondary="Fetch and analyze GitHub repository code structure and endpoints"
                />
              </ListItem>
              <ListItem sx={{ py: 1 }}>
                <ListItemIcon>
                  <Typography variant="h6" color="primary">2</Typography>
                </ListItemIcon>
                <ListItemText 
                  primary="AI Test Generation" 
                  secondary="Generate comprehensive test scenarios using GPT-4 based on code analysis"
                />
              </ListItem>
              <ListItem sx={{ py: 1 }}>
                <ListItemIcon>
                  <Typography variant="h6" color="primary">3</Typography>
                </ListItemIcon>
                <ListItemText 
                  primary="Automated Execution" 
                  secondary="Execute tests against live APIs with intelligent validation and reporting"
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Call to Action */}
      <Box sx={{ textAlign: 'center', mt: 6 }}>
        <Paper sx={{ p: 4, backgroundColor: 'grey.50' }}>
          <Typography variant="h4" gutterBottom>
            Ready to Test Your APIs?
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: 'text.secondary' }}>
            Get started with intelligent API testing in minutes
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/testing')}
            startIcon={<Integration />}
            sx={{ mr: 2 }}
          >
            Start Analysis
          </Button>
          <Button
            variant="outlined"
            size="large"
            href="https://github.com/user/agentapi"
            target="_blank"
            startIcon={<GitHub />}
          >
            View on GitHub
          </Button>
        </Paper>
      </Box>
    </Box>
  );
}

export default HomePage;