const express = require('express');
const path = require('path');
const app = express();

const PORT = process.env.PORT || 3000;

// Serve static views
app.use(express.static(path.join(__dirname, 'views')));

// Health check endpoint for Azure probe configurations
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'Healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// JSON API endpoint for runtime details
app.get('/api/info', (req, res) => {
  res.json({
    appName: process.env.WEBSITE_SITE_NAME || 'Local-Dev-Demo',
    nodeVersion: process.version,
    platform: process.platform,
    environment: process.env.NODE_ENV || 'development',
    serverTime: new Date().toLocaleTimeString(),
    customMessage: process.env.CUSTOM_WELCOME_MESSAGE || 'Welcome to the Azure DevOps Demo App!'
  });
});

// Fallback to index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// Only start listening if not running in test mode
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

module.exports = app;
