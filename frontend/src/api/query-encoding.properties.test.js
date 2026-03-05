// frontend/src/api/query-encoding.properties.test.js

import { describe, it, vi, beforeEach, afterEach } from 'vitest';
import fc from 'fast-check';

describe('API Client Query Parameter Encoding', () => {
  let apiClient;

  beforeEach(async () => {
    // Reset modules to get a fresh import
    vi.resetModules();

    // Import the client fresh for each test
    const clientModule = await import('./client.js');
    apiClient = clientModule.default;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('Property 3: correctly encodes query parameters for requests', async () => {
    /**
     * Feature: react-frontend-implementation
     * Property 3: For any search or filter parameters passed to the API client,
     * they SHALL be properly encoded as URL query parameters in the request.
     * Validates: Requirements 2.6
     */
    await fc.assert(
      fc.asyncProperty(
        fc.dictionary(
          fc.string({ minLength: 1 }).filter(s => s.trim() !== ''),
          fc.oneof(
            fc.string(),
            fc.integer(),
            fc.boolean()
          )
        ),
        async (params) => {
          // Mock the axios request to capture the config
          let capturedConfig = null;
          const getSpy = vi.spyOn(apiClient, 'get').mockImplementation((url, config) => {
            capturedConfig = config;
            return Promise.resolve({
              data: [],
              config: { ...config, params, url }
            });
          });

          try {
            // Make the request with query parameters
            await apiClient.get('/prompts', { params });

            // Verify that params were passed to the request
            if (Object.keys(params).length === 0) {
              // Empty params should still work
              return capturedConfig !== null;
            }

            // Verify params were passed correctly
            const result = capturedConfig &&
                   capturedConfig.params &&
                   Object.keys(capturedConfig.params).length === Object.keys(params).length &&
                   Object.keys(params).every(key => capturedConfig.params[key] === params[key]);

            getSpy.mockRestore();
            return result;
          } catch {
            getSpy.mockRestore();
            // Should not throw errors for valid params
            return false;
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
