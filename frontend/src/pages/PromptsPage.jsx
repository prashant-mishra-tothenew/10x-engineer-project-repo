// frontend/src/pages/PromptsPage.jsx

import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import usePrompts from '../hooks/usePrompts';
import useCollections from '../hooks/useCollections';
import useDebounce from '../hooks/useDebounce';
import SearchBar from '../components/shared/SearchBar';
import Button from '../components/shared/Button';
import Modal from '../components/shared/Modal';
import PromptList from '../components/prompts/PromptList';
import PromptForm from '../components/prompts/PromptForm';
import { deletePrompt, updatePrompt, getPrompt, createPrompt } from '../api/prompts';
import styles from './PromptsPage.module.css';

/**
 * PromptsPage - Main page for displaying and managing prompts
 *
 * This is the main "view" or "page" component (similar to a route component in Vue Router
 * or a page component in Next.js). It orchestrates the data fetching, search functionality,
 * and user interactions.
 */
const PromptsPage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [createError, setCreateError] = useState(null);
  const [editError, setEditError] = useState(null);

  // Debounce the search query to avoid excessive API calls
  // This is like using lodash.debounce in JavaScript - it waits 300ms after
  // the user stops typing before actually triggering the search
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  // Memoize the filters object to prevent unnecessary re-renders
  // This is like useMemo in React or computed in Vue - it only creates a new
  // object when debouncedSearchQuery actually changes
  const filters = useMemo(() => {
    // Only include search in filters if it's not empty
    return debouncedSearchQuery ? { search: debouncedSearchQuery } : {};
  }, [debouncedSearchQuery]);

  // Fetch prompts with debounced search filter
  // The usePrompts hook handles the API call and state management
  const { prompts, loading, error, refetch } = usePrompts(filters);

  // Fetch collections for the form dropdown
  const { collections } = useCollections();

  /**
   * Handle search input changes
   * We just update the local state here - the useDebounce hook will
   * debounce it, and usePrompts will automatically refetch when the
   * debounced value changes
   */
  const handleSearchChange = (query) => {
    setSearchQuery(query);
  };

  /**
   * Navigate to prompt detail page when card is clicked
   */
  const handlePromptClick = (promptId) => {
    navigate(`/prompts/${promptId}`);
  };

  /**
   * Handle edit button click - open modal with prompt data
   */
  const handleEdit = async (promptId) => {
    try {
      // Fetch the full prompt data
      const promptData = await getPrompt(promptId);
      setEditingPrompt(promptData);
      setIsEditModalOpen(true);
    } catch (err) {
      console.error('Failed to fetch prompt:', err);
      // TODO: Show error message to user
    }
  };

  /**
   * Handle edit form submission
   */
  const handleEditSubmit = async (formData) => {
    setIsSubmitting(true);
    setEditError(null); // Clear any previous errors
    try {
      await updatePrompt(editingPrompt.id, formData);
      // Close modal and refresh the list
      setIsEditModalOpen(false);
      setEditingPrompt(null);
      refetch(filters);
    } catch (err) {
      console.error('Failed to update prompt:', err);
      // Display error message without closing the form
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to update prompt. Please try again.';
      setEditError(errorMessage);
      // Don't close the modal - let user see the error and retry
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle modal close
   */
  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
    setEditingPrompt(null);
    setEditError(null); // Clear error when closing modal
  };

  /**
   * Handle delete button click
   * This makes an API call to delete the prompt, then refreshes the list
   */
  const handleDelete = async (promptId) => {
    // TODO: Add confirmation dialog before deleting
    try {
      await deletePrompt(promptId);
      // Refresh the prompt list after successful deletion
      refetch(filters);
    } catch (err) {
      console.error('Failed to delete prompt:', err);
      // TODO: Show error message to user
    }
  };

  /**
   * Handle create new prompt button click
   */
  const handleCreateNew = () => {
    setIsCreateModalOpen(true);
    setCreateError(null);
  };

  /**
   * Handle create form submission
   */
  const handleCreateSubmit = async (formData) => {
    setIsSubmitting(true);
    setCreateError(null);
    try {
      await createPrompt(formData);
      // Close modal and refresh the list
      setIsCreateModalOpen(false);
      refetch(filters);
    } catch (err) {
      console.error('Failed to create prompt:', err);
      // Display error message without closing the form
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to create prompt. Please try again.';
      setCreateError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.container}>
      {/* Page header with title and create button */}
      <div className={styles.header}>
        <h1>All Prompts</h1>
        <Button onClick={handleCreateNew} variant="primary">
          Create New Prompt
        </Button>
      </div>

      {/* Search bar */}
      <div className={styles.searchSection}>
        <SearchBar
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search prompts..."
        />
      </div>

      {/* Prompt list with loading/error states */}
      <PromptList
        prompts={prompts}
        loading={loading}
        error={error}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onClick={handlePromptClick}
        onRetry={() => refetch(filters)}
      />

      {/* Create Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Prompt"
      >
        <PromptForm
          onSubmit={handleCreateSubmit}
          loading={isSubmitting}
          collections={collections}
          error={createError}
        />
      </Modal>

      {/* Edit Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={handleCloseEditModal}
        title="Edit Prompt"
      >
        <PromptForm
          onSubmit={handleEditSubmit}
          loading={isSubmitting}
          collections={collections}
          initialData={editingPrompt}
          error={editError}
        />
      </Modal>
    </div>
  );
};

export default PromptsPage;
