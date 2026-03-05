// frontend/src/components/prompts/PromptForm.jsx

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './PromptForm.module.css';

const PromptForm = ({ onSubmit, loading, collections, initialData, error }) => {
  const [formState, setFormState] = useState({
    title: initialData?.title || '',
    content: initialData?.content || '',
    description: initialData?.description || '',
    collection_id: initialData?.collection_id || '',
  });

  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formState.title.trim()) newErrors.title = 'Title is required.';
    if (!formState.content.trim()) newErrors.content = 'Content is required.';
    // Add more validations as needed
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formState);
    }
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      {/* Display API error if present */}
      {error && (
        <div className={styles.errorContainer}>
          <ErrorMessage message={error} />
        </div>
      )}

      <div className={styles.field}>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formState.title}
          onChange={handleChange}
        />
        {errors.title && <span className={styles.error}>{errors.title}</span>}
      </div>
      <div className={styles.field}>
        <label htmlFor="content">Content</label>
        <textarea
          id="content"
          name="content"
          value={formState.content}
          onChange={handleChange}
        />
        {errors.content && <span className={styles.error}>{errors.content}</span>}
      </div>
      <div className={styles.field}>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formState.description}
          onChange={handleChange}
        />
      </div>
      <div className={styles.field}>
        <label htmlFor="collection">Collection</label>
        <select
          id="collection"
          name="collection_id"
          value={formState.collection_id}
          onChange={handleChange}
        >
          <option value="">Select a collection</option>
          {collections.map((collection) => (
            <option key={collection.id} value={collection.id}>
              {collection.name}
            </option>
          ))}
        </select>
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Loading...' : (initialData ? 'Update Prompt' : 'Create Prompt')}
      </button>
    </form>
  );
};

PromptForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  collections: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
    })
  ),
  initialData: PropTypes.shape({
    title: PropTypes.string,
    content: PropTypes.string,
    description: PropTypes.string,
    collection_id: PropTypes.string,
  }),
  error: PropTypes.string,
};

PromptForm.defaultProps = {
  loading: false,
  collections: [],
  initialData: null,
  error: null,
};

export default PromptForm;
