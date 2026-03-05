// frontend/src/api/prompts.js

import apiClient from './client';

// Fetch all prompts with optional filters
export const getPrompts = async (filters = {}) => {
  const response = await apiClient.get('/prompts', { params: { ...filters } });
  return response.data;
};

// Fetch a single prompt by ID
export const getPrompt = async (id) => {
  const response = await apiClient.get(`/prompts/${id}`);
  return response.data;
};

// Create a new prompt
export const createPrompt = async (promptData) => {
  const response = await apiClient.post('/prompts', promptData);
  return response.data;
};

// Update an existing prompt
export const updatePrompt = async (id, promptData) => {
  const response = await apiClient.put(`/prompts/${id}`, promptData);
  return response.data;
};

// Delete a prompt by ID
export const deletePrompt = async (id) => {
  const response = await apiClient.delete(`/prompts/${id}`);
  return response.data;
};
