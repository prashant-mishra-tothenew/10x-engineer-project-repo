// frontend/src/api/collections.js

import apiClient from './client';

// Fetch all collections
export const getCollections = async () => {
  const response = await apiClient.get('/collections');
  return response.data;
};

// Fetch a single collection by ID
export const getCollection = async (id) => {
  const response = await apiClient.get(`/collections/${id}`);
  return response.data;
};

// Create a new collection
export const createCollection = async (collectionData) => {
  const response = await apiClient.post('/collections', collectionData);
  return response.data;
};

// Update an existing collection
export const updateCollection = async (id, collectionData) => {
  const response = await apiClient.put(`/collections/${id}`, collectionData);
  return response.data;
};

// Delete a collection by ID
export const deleteCollection = async (id) => {
  const response = await apiClient.delete(`/collections/${id}`);
  return response.data;
};
