const request = require('supertest');
const app = require('../app');

describe('Azure DevOps Demo Web Application Tests', () => {
  
  test('GET /health returns 200 OK and valid health schema', async () => {
    const response = await request(app).get('/health');
    expect(response.statusCode).toBe(200);
    expect(response.body.status).toBe('Healthy');
    expect(response.body).toHaveProperty('timestamp');
    expect(response.body).toHaveProperty('uptime');
  });

  test('GET /api/info returns status details and default application name', async () => {
    const response = await request(app).get('/api/info');
    expect(response.statusCode).toBe(200);
    expect(response.body).toHaveProperty('appName');
    expect(response.body).toHaveProperty('nodeVersion');
    expect(response.body).toHaveProperty('platform');
    expect(response.body).toHaveProperty('customMessage');
  });

  test('GET /random-page falls back to index.html', async () => {
    const response = await request(app).get('/random-page');
    expect(response.statusCode).toBe(200);
    expect(response.text).toContain('<!DOCTYPE html>');
  });

});
