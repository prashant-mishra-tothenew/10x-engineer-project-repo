import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useCollections from '../hooks/useCollections';
import Button from '../components/shared/Button';
import Modal from '../components/shared/Modal';
import ConfirmDialog from '../components/shared/ConfirmDialog';
import CollectionList from '../components/collections/CollectionList';
import CollectionForm from '../components/collections/CollectionForm';
import { createCollection, deleteCollection } from '../api/collections';
import styles from './CollectionsPage.module.css';

/**
 * CollectionsPage - Main page for managing collections
 * Similar to an index/list page in Laravel or a collections route in Express
 */
const CollectionsPage = () => {
  const navigate = useNavigate();
  const { collections, loading, error, refetch } = useCollections();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [deletingCollectionId, setDeletingCollectionId] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState(null);

  /**
   * Handle create new collection button click
   */
  const handleCreateNew = () => {
    setIsCreateModalOpen(true);
    setFormError(null);
  };

  /**
   * Handle create form submission
   */
  const handleCreateSubmit = async (formData) => {
    setIsSubmitting(true);
    setFormError(null);
    try {
      await createCollection(formData);
      setIsCreateModalOpen(false);
      refetch(); // Refresh the collections list
    } catch (err) {
      console.error('Failed to create collection:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to create collection';
      setFormError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle delete button click
   */
  const handleDelete = (collectionId) => {
    setDeletingCollectionId(collectionId);
    setIsDeleteDialogOpen(true);
  };

  /**
   * Handle delete confirmation
   */
  const handleDeleteConfirm = async () => {
    setIsSubmitting(true);
    try {
      await deleteCollection(deletingCollectionId);
      setIsDeleteDialogOpen(false);
      setDeletingCollectionId(null);
      refetch(); // Refresh the collections list
    } catch (err) {
      console.error('Failed to delete collection:', err);
      // TODO: Show error message to user
      setIsDeleteDialogOpen(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle collection card click - navigate to filtered prompts view
   */
  const handleCollectionClick = (collectionId) => {
    // Navigate to prompts page with collection filter
    navigate(`/prompts?collection=${collectionId}`);
  };

  /**
   * Get the name of the collection being deleted (for confirmation dialog)
   */
  const deletingCollectionName = deletingCollectionId
    ? collections.find(c => c.id === deletingCollectionId)?.name
    : '';

  return (
    <div className={styles.container}>
      {/* Page header with title and create button */}
      <div className={styles.header}>
        <h1>Collections</h1>
        <Button onClick={handleCreateNew} variant="primary">
          Create New Collection
        </Button>
      </div>

      {/* Collection list with loading/error states */}
      <CollectionList
        collections={collections}
        loading={loading}
        error={error}
        onDelete={handleDelete}
        onClick={handleCollectionClick}
        onRetry={refetch}
      />

      {/* Create Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Collection"
      >
        <CollectionForm
          onSubmit={handleCreateSubmit}
          loading={isSubmitting}
          error={formError}
        />
      </Modal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Collection"
        message={`Are you sure you want to delete "${deletingCollectionName}"? This action cannot be undone.`}
        loading={isSubmitting}
      />
    </div>
  );
};

export default CollectionsPage;
