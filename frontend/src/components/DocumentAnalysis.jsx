import React, { useState } from 'react';
import {
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  Typography,
  Box,
  Paper
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

function DocumentAnalysis({ onTaskSubmit }) {
  const [documentText, setDocumentText] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze-document`, {
        document_text: documentText,
        analysis_type: 'comprehensive'
      });
      setSuccess(`Document submitted for analysis! Task ID: ${response.data.task_id}`);
      onTaskSubmit(response.data.task_id);
      setDocumentText('');
    } catch (err) {
      setError('Failed to submit document. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload-document`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuccess(`File uploaded successfully! Task ID: ${response.data.task_id}`);
      onTaskSubmit(response.data.task_id);
      setFile(null);
    } catch (err) {
      setError('Failed to upload file. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Document Analysis
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Analyze legal documents for key insights, risks, and recommendations.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Option 1: Paste Document Text
            </Typography>
            <form onSubmit={handleTextSubmit}>
              <TextField
                fullWidth
                multiline
                rows={8}
                label="Document Text"
                value={documentText}
                onChange={(e) => setDocumentText(e.target.value)}
                variant="outlined"
                placeholder="Paste your legal document text here..."
                sx={{ mb: 2 }}
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading || !documentText}
                startIcon={loading && <CircularProgress size={20} />}
              >
                Analyze Text
              </Button>
            </form>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Option 2: Upload Document File
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Button
                variant="outlined"
                component="label"
                startIcon={<CloudUploadIcon />}
              >
                Choose File
                <input
                  type="file"
                  hidden
                  accept=".txt,.pdf,.doc,.docx"
                  onChange={(e) => setFile(e.target.files[0])}
                />
              </Button>
              {file && (
                <Typography variant="body2">
                  Selected: {file.name}
                </Typography>
              )}
            </Box>
            <Button
              variant="contained"
              color="primary"
              onClick={handleFileUpload}
              disabled={loading || !file}
              startIcon={loading && <CircularProgress size={20} />}
              sx={{ mt: 2 }}
            >
              Upload & Analyze
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          {error && <Alert severity="error">{error}</Alert>}
          {success && <Alert severity="success">{success}</Alert>}
        </Grid>
      </Grid>
    </Box>
  );
}

export default DocumentAnalysis;


