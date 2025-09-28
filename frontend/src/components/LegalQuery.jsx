import React, { useState } from 'react';
import {
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  MenuItem,
  Typography,
  Box
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

function LegalQuery({ onTaskSubmit }) {
  const [formData, setFormData] = useState({
    query: '',
    case_type: 'general',
    jurisdiction: '',
    urgency: 'normal',
    additional_context: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const caseTypes = [
    'general', 'criminal', 'civil', 'corporate', 
    'family', 'intellectual_property', 'immigration'
  ];

  const urgencyLevels = ['low', 'normal', 'high', 'urgent'];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post(`${API_BASE_URL}/legal-query`, formData);
      setSuccess(`Query submitted successfully! Task ID: ${response.data.task_id}`);
      onTaskSubmit(response.data.task_id);
      setFormData({
        query: '',
        case_type: 'general',
        jurisdiction: '',
        urgency: 'normal',
        additional_context: ''
      });
    } catch (err) {
      setError('Failed to submit query. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Submit Legal Query
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Get AI-powered legal insights and recommendations for your query.
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Legal Query"
              name="query"
              value={formData.query}
              onChange={handleChange}
              required
              variant="outlined"
              placeholder="Describe your legal question or issue..."
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Case Type"
              name="case_type"
              value={formData.case_type}
              onChange={handleChange}
              variant="outlined"
            >
              {caseTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type.replace('_', ' ').toUpperCase()}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Jurisdiction"
              name="jurisdiction"
              value={formData.jurisdiction}
              onChange={handleChange}
              variant="outlined"
              placeholder="e.g., California, USA"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Urgency"
              name="urgency"
              value={formData.urgency}
              onChange={handleChange}
              variant="outlined"
            >
              {urgencyLevels.map((level) => (
                <MenuItem key={level} value={level}>
                  {level.toUpperCase()}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Additional Context"
              name="additional_context"
              value={formData.additional_context}
              onChange={handleChange}
              variant="outlined"
              placeholder="Any additional information that might be relevant..."
            />
          </Grid>

          <Grid item xs={12}>
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
            {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
            
            <Button
              type="submit"
              variant="contained"
              color="primary"
              size="large"
              disabled={loading || !formData.query}
              startIcon={loading && <CircularProgress size={20} />}
            >
              {loading ? 'Processing...' : 'Submit Query'}
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
}

export default LegalQuery;


