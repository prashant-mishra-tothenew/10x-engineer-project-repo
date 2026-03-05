// src/api/client.js

import axios from 'axios';
import { API_BASE_URL } from '../config';

// Create an axios instance with default configurations
const apiClient = axios.create({
  baseURL: API_BASE_URL,  // Base URL from the config file
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,  // Request timeout set to 10 seconds
});

// Add a response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    const enhancedError = {
      message: 'An unexpected error occurred',
      status: error.response?.status,
      type: 'network',
      retryable: true,
    };

    if (error.response) {
      // Request was made and server responded with a status code
      const { status, data } = error.response;

      // Updated the way to determine the error message
      enhancedError.message = (data?.detail?.trim() !== '' && data?.detail) || error.message || 'An unexpected error occurred';
      // Categorize errors based on status codes
      if (status >= 500) {
        enhancedError.type = 'server';
      } else if (status === 404) {
        enhancedError.type = 'not_found';
        enhancedError.retryable = false;
      } else if (status === 400) {
        enhancedError.type = 'validation';
        enhancedError.retryable = false;
      } else {
        enhancedError.type = 'client';
        enhancedError.retryable = false;
      }
    } else if (error.request) {
      // Request was made but no response - backend is likely not running
      enhancedError.type = 'network';
      enhancedError.message = 'Unable to connect to the backend server. Please make sure the backend is running on http://localhost:8000';
      enhancedError.retryable = true;
    } else {
      // Something else happened in making the request
      enhancedError.message = error.message;
    }

    console.error(enhancedError);  // Log the enhanced error for visibility
    return Promise.reject(enhancedError);
  }
);

export default apiClient;
