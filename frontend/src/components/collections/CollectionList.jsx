import React from 'react';
import PropTypes from 'prop-types';
import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './CollectionList.module.css';

/**
 * CollectionList - Display grid of collection cards
 * Similar to a list view in Laravel or a grid component in Vue
 */
const CollectionList = ({ collections, loading, error, onDelete, onClick, onRetry }) => {
  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={error.message || error}
        onRetry={onRetry}
        retryable={error.retryable !== false}
      />
    );
  }

  // Handle null or undefined collections
  if (!collections || collections.length === 0) {
    return (
      <div className={styles.emptyState}>
        <h3>No collections yet</h3>
        <p>Create your first collection to organize your prompts.</p>
      </div>
    );
  }

  return (
    <div className={styles.grid}>
      {collections.map((collection) => (
        <div
          key={collection.id}
          className={styles.card}
          onClick={() => onClick && onClick(collection.id)}
        >
          <div className={styles.cardHeader}>
            <h3 className={styles.cardTitle}>{collection.name}</h3>
            <div className={styles.cardActions}>
              <button
                className={`${styles.iconButton} ${styles.danger}`}
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(collection.id);
                }}
                aria-label={`Delete ${collection.name}`}
                title="Delete collection"
              >
                🗑️
              </button>
            </div>
          </div>

          {collection.description && (
            <p className={styles.description}>{collection.description}</p>
          )}
        </div>
      ))}
    </div>
  );
};

CollectionList.propTypes = {
  collections: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      description: PropTypes.string,
    })
  ),
  loading: PropTypes.bool,
  error: PropTypes.object,
  onDelete: PropTypes.func.isRequired,
  onClick: PropTypes.func,
  onRetry: PropTypes.func,
};

CollectionList.defaultProps = {
  collections: [],
  loading: false,
  error: null,
  onClick: null,
  onRetry: null,
};

export default CollectionList;
