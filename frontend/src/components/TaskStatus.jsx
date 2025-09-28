import { Grid } from '@mui/material';
import React, { useState, useEffect } from 'react';
import {
  TextField,
  Button,
  Alert,
  CircularProgress,
  Typography,
  Box,
  Paper,
  Chip
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

function TaskStatus({ taskId: propTaskId }) {
  const [taskId, setTaskId] = useState(propTaskId || '');
  const [taskData, setTaskData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (propTaskId) {
      setTaskId(propTaskId);
      checkStatus(propTaskId);
    }
  }, [propTaskId]);

  const checkStatus = async (id) => {
    if (!id) return;

    setLoading(true);
    setError('');

    try {
      const response = await axios.get(`${API_BASE_URL}/task-status/${id}`);
      setTaskData(response.data);
    } catch (err) {
      setError('Failed to fetch task status. Please check the Task ID.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    checkStatus(taskId);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Task Status
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Check the status of your submitted tasks.
      </Typography>

      <form onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <TextField
            fullWidth
            label="Task ID"
            value={taskId}
            onChange={(e) => setTaskId(e.target.value)}
            variant="outlined"
            placeholder="Enter task ID to check status"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading || !taskId}
            sx={{ minWidth: 120 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Check Status'}
          </Button>
        </Box>
      </form>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {taskData && (
        <Paper elevation={2} sx={{ p: 3 }}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Task Information
            </Typography>
            <Chip
              label={taskData.status.toUpperCase()}
              color={getStatusColor(taskData.status)}
              sx={{ mb: 2 }}
            />
          </Box>

          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                Task ID
              </Typography>
              <Typography variant="body1" gutterBottom>
                {taskData.task_id}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                Created At
              </Typography>
              <Typography variant="body1" gutterBottom>
                {new Date(taskData.created_at).toLocaleString()}
              </Typography>
            </Grid>

            {taskData.completed_at && (
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Completed At
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {new Date(taskData.completed_at).toLocaleString()}
                </Typography>
              </Grid>
            )}
          </Grid>

          {taskData.result && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Result
              </Typography>
              <Paper elevation={1} sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
                <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
                  {taskData.result.output}
                </Typography>
              </Paper>
            </Box>
          )}

          {taskData.error && (
            <Box sx={{ mt: 3 }}>
              <Alert severity="error">
                {taskData.error}
              </Alert>
            </Box>
          )}
        </Paper>
      )}
    </Box>
  );
}

export default TaskStatus;


