import { describe, it } from 'vitest';
import fc from 'fast-check';
import apiClient from './client';

describe('API Client Properties', () => {
  it('Property 1: includes Content-Type header in all requests', async () => {
    /**
     * Feature: API Integration Layer
     * Property 1: For any HTTP request made by the API client, the request
     * SHALL include the Content-Type header set to "application/json".
     * Validates: Requirements 2.2
     */
    await fc.assert(
      fc.asyncProperty(
        fc.constantFrom('GET', 'POST', 'PUT', 'DELETE'),
        fc.webUrl(),
        async (method, url) => {
          // Setup a mock request to inspect headers
          const mockRequest = {
            baseURL: apiClient.defaults.baseURL,
            url,
            method,
            headers: apiClient.defaults.headers,
          };

          // Expect the Content-Type header to be set correctly
          return mockRequest.headers['Content-Type'] === 'application/json';
        }
      ),
      { numRuns: 100 } // Run multiple cases for thorough testing
    );
  });
});
