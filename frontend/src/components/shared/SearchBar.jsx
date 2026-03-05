// frontend/src/components/shared/SearchBar.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './SearchBar.module.css';

/**
 * SearchBar component with search icon and clear button
 * Note: Debouncing should be handled by the parent component using useDebounce hook
 */
const SearchBar = ({ value, onChange, placeholder }) => {
  const handleClear = () => {
    onChange('');
  };

  return (
    <div className={styles.searchContainer}>
      <div className={styles.searchWrapper}>
        <span className={styles.searchIcon}>🔍</span>
        <input
          id="search-input"
          type="text"
          className={styles.searchInput}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder || "Search prompts..."}
          aria-label="Search"
        />
        {value && (
          <button
            className={styles.clearButton}
            onClick={handleClear}
            aria-label="Clear search"
            type="button"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
};

SearchBar.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string,
};

export default SearchBar;
