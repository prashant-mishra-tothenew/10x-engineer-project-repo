// frontend/src/hooks/usePrompts.js

import { useEffect, useState, useCallback } from 'react';
import { getPrompts } from '../api/prompts';

/**
 * Custom hook to fetch prompts and manage associated states.
 *
 * This is similar to using a composable in Vue or a custom hook pattern in React.
 * It encapsulates the data fetching logic and state management.
 *
 * @param {Object} filters - Filters to apply when fetching (e.g., { search: 'query', collection_id: '123' })
 */
const usePrompts = (filters = {}) => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPrompts = useCallback(
    async (customFilters) => {
      setLoading(true);
      setError(null);
      try {
        // Use custom filters if provided, otherwise use the filters from props
        const filtersToUse = customFilters !== undefined ? customFilters : filters;
        const data = await getPrompts(filtersToUse);
        // Backend returns { prompts: [...], total: number }
        setPrompts(data.prompts || data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    },
    [filters]
  );

  // Fetch prompts whenever filters change
  // This is similar to a watcher in Vue or useEffect in React
  useEffect(() => {
    fetchPrompts();
  }, [fetchPrompts]);

  return { prompts, loading, error, refetch: fetchPrompts };
};

export default usePrompts;
