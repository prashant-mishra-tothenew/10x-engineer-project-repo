// frontend/src/components/prompts/PromptList.jsx

import React from 'react';
import PropTypes from 'prop-types';
import PromptCard from './PromptCard';
import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './PromptList.module.css';

/**
 * PromptList component displays a grid of prompt cards with loading and error states.
 *
 * This is similar to a list component in React/Vue - it handles the display logic
 * for multiple items, including empty states and error handling.
 */
const PromptList = ({ prompts, loading, error, onEdit, onDelete, onClick, onRetry }) => {
  // Show loading spinner during initial fetch (when no prompts are loaded yet)
  if (loading && prompts.length === 0) {
    return (
      <div className={styles.loadingContainer}>
        <LoadingSpinner size="large" />
        <p>Loading prompts...</p>
      </div>
    );
  }

  // Show error message if fetch failed
  if (error) {
    return (
      <div className={styles.errorContainer}>
        <ErrorMessage
          message={error.message || 'Failed to load prompts'}
          onRetry={onRetry}
          retryable={true}
        />
      </div>
    );
  }

  // Show empty state when no prompts exist
  if (prompts.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p>No prompts found. Create your first prompt to get started!</p>
      </div>
    );
  }

  // Render grid of prompt cards
  // The grid is responsive: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
  return (
    <div className={styles.grid}>
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          onEdit={onEdit}
          onDelete={onDelete}
          onClick={onClick}
        />
      ))}
    </div>
  );
};

PromptList.propTypes = {
  prompts: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      content: PropTypes.string.isRequired,
      created_at: PropTypes.string.isRequired,
      updated_at: PropTypes.string.isRequired,
      collection_id: PropTypes.string,
      collectionName: PropTypes.string,
    })
  ).isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.object,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onClick: PropTypes.func.isRequired,
  onRetry: PropTypes.func,
};

PromptList.defaultProps = {
  error: null,
  onRetry: () => {},
};

export default PromptList;
