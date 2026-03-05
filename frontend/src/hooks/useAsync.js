// frontend/src/hooks/useAsync.js

import { useCallback, useState } from 'react';

/**
 * Custom hook to manage loading and error states for async operations.
 */
const useAsync = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Executes the passed asynchronous function and manages loading and error states.
   * @param {Function} asyncFunction - The async function to execute.
   * @param  {...any} args - Arguments to pass to the async function.
   * @returns - The result of the async function.
   */
  const execute = useCallback(async (asyncFunction, ...args) => {
    setLoading(true);
    setError(null);
    try {
      const result = await asyncFunction(...args);
      return result;
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Resets loading and error states.
   */
  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
  }, []);

  return { loading, error, execute, reset };
};

export default useAsync;
