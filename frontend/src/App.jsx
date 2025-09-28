import React, { useState } from 'react';
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Tab,
  Tabs,
  Paper,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';
import LegalQuery from './components/LegalQuery';
import DocumentAnalysis from './components/DocumentAnalysis';
import ClientIntake from './components/ClientIntake';
import TaskStatus from './components/TaskStatus';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [currentTaskId, setCurrentTaskId] = useState(null);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleTaskSubmit = (taskId) => {
    setCurrentTaskId(taskId);
    // Optionally switch to status tab
    setTabValue(3);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              JurisAI - Legal Intelligence Platform
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Paper elevation={3}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                aria-label="JurisAI features"
                variant="fullWidth"
              >
                <Tab label="Legal Query" />
                <Tab label="Document Analysis" />
                <Tab label="Client Intake" />
                <Tab label="Task Status" />
              </Tabs>
            </Box>

            <TabPanel value={tabValue} index={0}>
              <LegalQuery onTaskSubmit={handleTaskSubmit} />
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <DocumentAnalysis onTaskSubmit={handleTaskSubmit} />
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <ClientIntake onTaskSubmit={handleTaskSubmit} />
            </TabPanel>

            <TabPanel value={tabValue} index={3}>
              <TaskStatus taskId={currentTaskId} />
            </TabPanel>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;


