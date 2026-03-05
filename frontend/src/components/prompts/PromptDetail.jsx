import React from 'react';
import PropTypes from 'prop-types';
import Button from '../shared/Button';
import styles from './PromptDetail.module.css';

/**
 * PromptDetail - Display full prompt details
 * Similar to a "show" view in Laravel or a detail component in Vue
 */
const PromptDetail = ({ prompt, onEdit, onDelete, onBack, collectionName }) => {
  // Highlight variable placeholders like {{variable}}
  const highlightVariables = (text) => {
    if (!text) return text;

    // Split by {{variable}} pattern and wrap matches in spans
    const parts = text.split(/(\{\{[^}]+\}\})/g);
    return parts.map((part, index) => {
      if (part.match(/\{\{[^}]+\}\}/)) {
        return (
          <span key={index} className={styles.variable}>
            {part}
          </span>
        );
      }
      return part;
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Button onClick={onBack} variant="secondary">
          ← Back
        </Button>
        <div className={styles.actions}>
          <Button onClick={onEdit} variant="primary">
            Edit
          </Button>
          <Button onClick={onDelete} variant="danger">
            Delete
          </Button>
        </div>
      </div>

      <div className={styles.content}>
        <h1 className={styles.title}>{prompt.title}</h1>

        {collectionName && (
          <div className={styles.badge}>{collectionName}</div>
        )}

        {prompt.description && (
          <p className={styles.description}>{prompt.description}</p>
        )}

        <div className={styles.promptContent}>
          <h3>Content:</h3>
          <pre className={styles.contentText}>
            {highlightVariables(prompt.content)}
          </pre>
        </div>

        <div className={styles.metadata}>
          <div className={styles.metadataItem}>
            <strong>Created:</strong> {formatDate(prompt.created_at)}
          </div>
          <div className={styles.metadataItem}>
            <strong>Updated:</strong> {formatDate(prompt.updated_at)}
          </div>
          <div className={styles.metadataItem}>
            <strong>ID:</strong> {prompt.id}
          </div>
        </div>
      </div>
    </div>
  );
};

PromptDetail.propTypes = {
  prompt: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    description: PropTypes.string,
    collection_id: PropTypes.string,
    created_at: PropTypes.string.isRequired,
    updated_at: PropTypes.string.isRequired,
  }).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onBack: PropTypes.func.isRequired,
  collectionName: PropTypes.string,
};

export default PromptDetail;
