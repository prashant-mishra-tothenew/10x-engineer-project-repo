// frontend/src/components/shared/ErrorMessage.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './ErrorMessage.module.css';

const ErrorMessage = ({ message, onRetry, retryable }) => {
  return (
    <div className={styles.error} role="alert">
      <span className={styles.icon} aria-hidden="true">⚠️</span>
      <span>{message}</span>
      {retryable && <button onClick={onRetry} className={styles.retryButton}>Retry</button>}
    </div>
  );
};

ErrorMessage.propTypes = {
  message: PropTypes.string.isRequired,
  onRetry: PropTypes.func,
  retryable: PropTypes.bool,
};

ErrorMessage.defaultProps = {
  retryable: false,
  onRetry: () => {},
};

export default ErrorMessage;
