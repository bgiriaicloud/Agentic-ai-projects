const express = require('express');
const path = require('path');
const app = express();

// Standard port for container workloads (AWS App Runner defaults to 8080 or user-configured)
const PORT = process.env.PORT || 8080;

app.use(express.static(path.join(__dirname, 'views')));

// Health probe endpoint for AWS ALB target group verification
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
    serviceName: process.env.AWS_APP__RUNNER_SERVICE_NAME || 'Local-AWS-Demo',
    revisionName: process.env.AWS_APP_RUNNER_REVISION || 'v1.0.0-local',
    nodeVersion: process.version,
    platform: process.platform,
    environment: process.env.NODE_ENV || 'development',
    serverTime: new Date().toLocaleTimeString(),
    welcomeMessage: process.env.CUSTOM_WELCOME_MESSAGE || 'Welcome to the AWS DevOps Demo App running on App Runner!'
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
