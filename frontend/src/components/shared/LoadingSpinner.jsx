// frontend/src/components/shared/LoadingSpinner.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './LoadingSpinner.module.css';

const LoadingSpinner = ({ size }) => {
  const sizeClass = styles[size] || styles.medium; // Default to medium size

  return (
    <div className={`${styles.spinner} ${sizeClass}`} role="status" aria-live="polite">
      <span className="sr-only">Loading...</span>
    </div>
  );
};

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['small', 'medium', 'large']),
};

LoadingSpinner.defaultProps = {
  size: 'medium',
};

export default LoadingSpinner;
