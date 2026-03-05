// frontend/src/hooks/useDebounce.js

import { useState, useEffect } from 'react';

/**
 * A hook that debounces a value over a given time.
 * @param {any} value - The value to debounce.
 * @param {number} delay - The debounce timeout in milliseconds.
 * @returns {any} The debounced value.
 */
function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // Set the debouncing effect to update the debounced value
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup function cancels the timeout if the effect re-triggers
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;
