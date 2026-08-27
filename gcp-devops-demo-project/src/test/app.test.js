const request = require('supertest');
const app = require('../app');

describe('GCP DevOps Demo Web Application Tests', () => {

  test('GET /health returns 200 OK and status Healthy', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('Healthy');
    expect(res.body).toHaveProperty('timestamp');
  });

  test('GET /api/info returns node version and service metadata', async () => {
    const res = await request(res.statusCode === 200 ? app : app).get('/api/info');
    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('serviceName');
    expect(res.body).toHaveProperty('revisionName');
    expect(res.body).toHaveProperty('nodeVersion');
  });

  test('GET /unknown-path falls back to HTML wrapper', async () => {
    const res = await request(app).get('/unknown-path');
    expect(res.statusCode).toBe(200);
    expect(res.text).toContain('<!DOCTYPE html>');
  });

});
