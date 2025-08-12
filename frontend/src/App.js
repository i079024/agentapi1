import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';
import ApiIcon from '@mui/icons-material/Api';
import HomePage from './components/HomePage';
import TestingPage from './components/TestingPage';
import ResultsPage from './components/ResultsPage';

function App() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" elevation={2}>
        <Toolbar>
          <ApiIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Agent API Testing Platform
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/testing" element={<TestingPage />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App;