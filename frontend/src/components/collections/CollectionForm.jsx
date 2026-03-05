import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Button from '../shared/Button';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './CollectionForm.module.css';

/**
 * CollectionForm - Form for creating/editing collections
 * Similar to form components in Laravel Blade or Vue forms
 */
const CollectionForm = ({ onSubmit, loading, initialData, error }) => {
  const [formState, setFormState] = useState({
    name: initialData?.name || '',
    description: initialData?.description || '',
  });

  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formState.name.trim()) {
      newErrors.name = 'Collection name is required.';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
    // Clear error for this field when user types
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: null });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formState);
    }
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      {error && (
        <div className={styles.errorContainer}>
          <ErrorMessage message={error} />
        </div>
      )}

      <div className={styles.field}>
        <label htmlFor="name">
          Collection Name <span className={styles.required}>*</span>
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formState.name}
          onChange={handleChange}
          placeholder="e.g., Marketing Prompts"
          disabled={loading}
        />
        {errors.name && <span className={styles.error}>{errors.name}</span>}
      </div>

      <div className={styles.field}>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formState.description}
          onChange={handleChange}
          placeholder="Optional description for this collection"
          rows="3"
          disabled={loading}
        />
      </div>

      <div className={styles.actions}>
        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? 'Saving...' : initialData ? 'Update Collection' : 'Create Collection'}
        </Button>
      </div>
    </form>
  );
};

CollectionForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  initialData: PropTypes.shape({
    name: PropTypes.string,
    description: PropTypes.string,
  }),
  error: PropTypes.string,
};

CollectionForm.defaultProps = {
  loading: false,
  initialData: null,
  error: null,
};

export default CollectionForm;
