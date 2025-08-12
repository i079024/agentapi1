import React from 'react';
import { Box, Typography } from '@mui/material';

// Simple JSON display component to avoid external dependencies
const JsonDisplay = ({ data }) => {
  if (!data) return <Typography variant="body2">No data available</Typography>;
  
  return (
    <Box sx={{ fontFamily: 'monospace', fontSize: '0.875rem' }}>
      <pre style={{ 
        backgroundColor: '#f5f5f5', 
        padding: '16px', 
        borderRadius: '4px',
        overflow: 'auto',
        margin: 0,
        whiteSpace: 'pre-wrap'
      }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </Box>
  );
};

export default JsonDisplay;