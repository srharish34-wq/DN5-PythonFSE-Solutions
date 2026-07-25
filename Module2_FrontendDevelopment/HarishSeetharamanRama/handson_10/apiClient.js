

import axios from 'axios';

// ── TASK 1: Centralised Axios Instance ────────────────────
const apiClient = axios.create({
  baseURL : 'https://jsonplaceholder.typicode.com',
  timeout : 5000,
  headers : {
    'Content-Type': 'application/json',
  }
});

// Request interceptor — attach auth token to every request
apiClient.interceptors.request.use(config => {
  const token = 'mock-jwt-token-2024';  // replace with real token in production
  config.headers['Authorization'] = `Bearer ${token}`;
  console.log(`[API] Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
  return config;
}, error => Promise.reject(error));

// Response interceptor:
// (a) return response.data directly — callers get data, not Axios wrapper
// (b) standardise error format
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    const statusCode = error.response?.status || 0;
    const message    = error.response?.data?.message || error.message || 'Unknown error';
    console.error(`[API] Error ${statusCode}: ${message}`);
    // Throw standardised error — components never see HTTP status codes
    throw new Error(`${message} (status: ${statusCode})`);
  }
);

export default apiClient;



console.log('Hands-On 10: See comments for full implementation of API Layer + Redux + Error Boundary');
