// frontend/src/hooks/useCollections.js

import { useEffect, useState, useCallback } from 'react';
import { getCollections } from '../api/collections';

/**
 * Custom hook to fetch collections and manage associated states.
 */
const useCollections = () => {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCollections = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCollections();
      // Backend returns { collections: [...], total: number }
      setCollections(data.collections || data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCollections();
  }, [fetchCollections]);

  return { collections, loading, error, refetch: fetchCollections };
};

export default useCollections;
