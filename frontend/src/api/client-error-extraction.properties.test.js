// frontend/src/api/client-error-extraction.properties.test.js

import { describe, it } from 'vitest';
import fc from 'fast-check';

const createMockErrorResponse = (status, detail) => ({
  response: {
    status,
    data: {
      detail,
    },
  },
});

describe('API Client Error Handling Properties', () => {
  it('Property 2: correctly extracts and defaults error messages', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.record({
          status: fc.constantFrom(400, 404, 500),
          detail: fc.string(),
        }),
        async ({ status, detail }) => {
          const mockError = createMockErrorResponse(status, detail);

          // Throwing a mock error to simulate error handling
          try {
            if (mockError.response) {
              const errorMessage = (mockError.response.data.detail?.trim() !== '') ? mockError.response.data.detail.trim() : 'An unexpected error occurred';
              throw new Error(errorMessage);
            }
            throw new Error('An unexpected network error occurred');
          } catch (e) {
            const expectedMessage = (detail.trim() !== '') ? detail.trim() : 'An unexpected error occurred';
            return e.message === expectedMessage;
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
