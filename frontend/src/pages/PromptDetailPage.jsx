import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import PromptDetail from '../components/prompts/PromptDetail';
import Modal from '../components/shared/Modal';
import PromptForm from '../components/prompts/PromptForm';
import ConfirmDialog from '../components/shared/ConfirmDialog';
import LoadingSpinner from '../components/shared/LoadingSpinner';
import ErrorMessage from '../components/shared/ErrorMessage';
import { getPrompt, updatePrompt, deletePrompt } from '../api/prompts';
import useCollections from '../hooks/useCollections';
import styles from './PromptDetailPage.module.css';

/**
 * PromptDetailPage - Full page view for a single prompt
 * Similar to a "show" route in Laravel or a detail page in Next.js
 */
const PromptDetailPage = () => {
  const { id } = useParams(); // Get prompt ID from URL (like req.params.id in Express)
  const navigate = useNavigate();

  const [prompt, setPrompt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editError, setEditError] = useState(null);

  const { collections } = useCollections();

  // Fetch prompt on mount (like componentDidMount in class components)
  useEffect(() => {
    fetchPrompt();
  }, [id]);

  const fetchPrompt = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getPrompt(id);
      setPrompt(data);
    } catch (err) {
      console.error('Failed to fetch prompt:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load prompt');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditModalOpen(true);
    setEditError(null);
  };

  const handleEditSubmit = async (formData) => {
    setIsSubmitting(true);
    setEditError(null);
    try {
      const updated = await updatePrompt(id, formData);
      setPrompt(updated);
      setIsEditModalOpen(false);
    } catch (err) {
      console.error('Failed to update prompt:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to update prompt';
      setEditError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = () => {
    setIsDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    setIsSubmitting(true);
    try {
      await deletePrompt(id);
      navigate('/prompts'); // Redirect to prompts list after deletion
    } catch (err) {
      console.error('Failed to delete prompt:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to delete prompt');
      setIsDeleteDialogOpen(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBack = () => {
    navigate('/prompts');
  };

  // Find collection name if prompt has a collection
  const collectionName = prompt?.collection_id
    ? collections.find(c => c.id === prompt.collection_id)?.name
    : null;

  if (loading) {
    return (
      <div className={styles.centerContainer}>
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.centerContainer}>
        <ErrorMessage
          message={error}
          onRetry={fetchPrompt}
        />
      </div>
    );
  }

  if (!prompt) {
    return (
      <div className={styles.centerContainer}>
        <h2>Prompt not found</h2>
        <button onClick={handleBack}>Go back to prompts</button>
      </div>
    );
  }

  return (
    <>
      <PromptDetail
        prompt={prompt}
        collectionName={collectionName}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onBack={handleBack}
      />

      {/* Edit Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Edit Prompt"
      >
        <PromptForm
          onSubmit={handleEditSubmit}
          loading={isSubmitting}
          collections={collections}
          initialData={prompt}
          error={editError}
        />
      </Modal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Delete Prompt"
        message={`Are you sure you want to delete "${prompt.title}"? This action cannot be undone.`}
        loading={isSubmitting}
      />
    </>
  );
};

export default PromptDetailPage;
