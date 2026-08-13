const express = require('express');
const path = require('path');
const app = express();

// Cloud Run default PORT is 8080
const PORT = process.env.PORT || 8080;

app.use(express.static(path.join(__dirname, 'views')));

// Health check endpoint for Google Cloud Load Balancer / target probes
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'Healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// JSON metadata API
app.get('/api/info', (req, res) => {
  res.json({
    serviceName: process.env.K_SERVICE || 'Local-Dev-Demo',
    revisionName: process.env.K_REVISION || 'v1.0.0-local',
    nodeVersion: process.version,
    platform: process.platform,
    environment: process.env.NODE_ENV || 'development',
    serverTime: new Date().toLocaleTimeString(),
    welcomeMessage: process.env.CUSTOM_WELCOME_MESSAGE || 'Welcome to the GCP DevOps Demo App running on Cloud Run!'
  });
});

// Fallback routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

module.exports = app;
