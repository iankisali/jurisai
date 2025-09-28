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

function ClientIntake({ onTaskSubmit }) {
  const [formData, setFormData] = useState({
    client_name: '',
    case_description: '',
    case_type: '',
    jurisdiction: '',
    preferred_outcome: '',
    budget_range: '',
    timeline: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const caseTypes = [
    'Criminal Defense',
    'Personal Injury',
    'Family Law',
    'Business Law',
    'Real Estate',
    'Immigration',
    'Intellectual Property',
    'Employment Law'
  ];

  const budgetRanges = [
    'Under $5,000',
    '$5,000 - $10,000',
    '$10,000 - $25,000',
    '$25,000 - $50,000',
    'Over $50,000'
  ];

  const timelines = [
    'Immediate (within 1 week)',
    'Short-term (1-4 weeks)',
    'Medium-term (1-3 months)',
    'Long-term (3+ months)'
  ];

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
      const response = await axios.post(`${API_BASE_URL}/client-intake`, formData);
      setSuccess(`Client intake submitted successfully! Task ID: ${response.data.task_id}`);
      onTaskSubmit(response.data.task_id);
      setFormData({
        client_name: '',
        case_description: '',
        case_type: '',
        jurisdiction: '',
        preferred_outcome: '',
        budget_range: '',
        timeline: ''
      });
    } catch (err) {
      setError('Failed to submit client intake. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        New Client Intake
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Complete the intake form to get personalized legal assistance recommendations.
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Client Name"
              name="client_name"
              value={formData.client_name}
              onChange={handleChange}
              required
              variant="outlined"
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
              required
              variant="outlined"
            >
              {caseTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Case Description"
              name="case_description"
              value={formData.case_description}
              onChange={handleChange}
              required
              variant="outlined"
              placeholder="Provide a detailed description of the legal matter..."
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Jurisdiction"
              name="jurisdiction"
              value={formData.jurisdiction}
              onChange={handleChange}
              variant="outlined"
              placeholder="e.g., California, New York"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Budget Range"
              name="budget_range"
              value={formData.budget_range}
              onChange={handleChange}
              variant="outlined"
            >
              {budgetRanges.map((range) => (
                <MenuItem key={range} value={range}>
                  {range}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={2}
              label="Preferred Outcome"
              name="preferred_outcome"
              value={formData.preferred_outcome}
              onChange={handleChange}
              variant="outlined"
              placeholder="What outcome would you like to achieve?"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Timeline"
              name="timeline"
              value={formData.timeline}
              onChange={handleChange}
              variant="outlined"
            >
              {timelines.map((timeline) => (
                <MenuItem key={timeline} value={timeline}>
                  {timeline}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12}>
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
            {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
            
            <Button
              type="submit"
              variant="contained"
              color="primary"
              size="large"
              disabled={loading || !formData.client_name || !formData.case_description || !formData.case_type}
              startIcon={loading && <CircularProgress size={20} />}
            >
              {loading ? 'Processing...' : 'Submit Intake'}
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
}

export default ClientIntake;


