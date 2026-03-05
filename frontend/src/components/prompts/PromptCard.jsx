// frontend/src/components/prompts/PromptCard.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './PromptCard.module.css';

const PromptCard = ({ prompt, onEdit, onDelete, onClick }) => {
  // Handle both camelCase and snake_case from backend
  const {
    title,
    content,
    created_at,
    updated_at,
    collectionName
  } = prompt;

  // Truncate content for preview (max 100 characters)
  const contentPreview = content.length > 100
    ? content.slice(0, 100) + '...'
    : content;

  return (
    <div className={styles.card} onClick={() => onClick(prompt.id)}>
      <div className={styles.header}>
        <h3>{title}</h3>
        {collectionName && <span className={styles.collectionBadge}>{collectionName}</span>}
      </div>
      <p className={styles.content}>{contentPreview}</p>
      <div className={styles.timestamps}>
        <span>Created: {new Date(created_at).toLocaleDateString()}</span>
        <span>Updated: {new Date(updated_at).toLocaleDateString()}</span>
      </div>
      <div className={styles.actions}>
        <button aria-label="Edit Prompt" onClick={(e) => { e.stopPropagation(); onEdit(prompt.id); }}>Edit</button>
        <button aria-label="Delete Prompt" onClick={(e) => { e.stopPropagation(); onDelete(prompt.id); }}>Delete</button>
      </div>
    </div>
  );
};

PromptCard.propTypes = {
  prompt: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    created_at: PropTypes.string.isRequired,
    updated_at: PropTypes.string.isRequired,
    collection_id: PropTypes.string,
    collectionName: PropTypes.string,
  }).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default PromptCard;
