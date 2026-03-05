// frontend/src/components/shared/Button.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './Button.module.css';

const Button = ({ variant, children, onClick, disabled, loading, type }) => {
  const classNames = `${styles.button} ${styles[variant]}`;

  return (
    <button
      type={type}
      className={classNames}
      onClick={onClick}
      disabled={disabled || loading}
      style={{ minWidth: '44px', minHeight: '44px' }} // Ensures minimum touch target
    >
      {loading ? <span className={styles.loader}></span> : children}
    </button>
  );
};

Button.propTypes = {
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  loading: PropTypes.bool,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
};

Button.defaultProps = {
  variant: 'primary',
  disabled: false,
  loading: false,
  type: 'button',
};

export default Button;
