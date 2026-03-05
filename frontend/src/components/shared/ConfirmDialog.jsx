// frontend/src/components/shared/ConfirmDialog.jsx

import React from 'react';
import PropTypes from 'prop-types';
import Modal from './Modal';
import styles from './ConfirmDialog.module.css';

const ConfirmDialog = ({ isOpen, onClose, onConfirm, title, message, loading, confirmText, cancelText, variant }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title}>
      <div className={styles.content}>
        <p className={styles.message}>{message}</p>
        <div className={styles.actions}>
          <button
            onClick={onClose}
            disabled={loading}
            style={{
              backgroundColor: '#e5e7eb',
              color: '#1f2937 !important',
              border: '1px solid #d1d5db',
              padding: '10px 24px',
              borderRadius: '6px',
              fontSize: '15px !important',
              fontWeight: '500',
              cursor: loading ? 'not-allowed' : 'pointer',
              minWidth: '100px',
              opacity: loading ? 0.6 : 1,
              fontFamily: 'inherit',
              display: 'inline-block',
              textAlign: 'center',
              lineHeight: 'normal',
            }}
          >
            No
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            style={{
              backgroundColor: '#dc2626',
              color: '#ffffff !important',
              border: 'none',
              padding: '10px 24px',
              borderRadius: '6px',
              fontSize: '15px !important',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              minWidth: '100px',
              opacity: loading ? 0.6 : 1,
              fontFamily: 'inherit',
              display: 'inline-block',
              textAlign: 'center',
              lineHeight: 'normal',
            }}
          >
            Yes
          </button>
        </div>
      </div>
    </Modal>
  );
};

ConfirmDialog.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onConfirm: PropTypes.func.isRequired,
  title: PropTypes.string,
  message: PropTypes.string.isRequired,
  loading: PropTypes.bool,
  confirmText: PropTypes.string,
  cancelText: PropTypes.string,
  variant: PropTypes.oneOf(['danger', 'primary', 'warning']),
};

ConfirmDialog.defaultProps = {
  loading: false,
  title: 'Confirm Action',
  confirmText: 'Yes',
  cancelText: 'No',
  variant: 'danger',
};

export default ConfirmDialog;
