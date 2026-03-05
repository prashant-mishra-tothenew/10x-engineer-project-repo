// src/components/layout/Header.jsx

import ThemeToggle from '../shared/ThemeToggle';
import styles from './Header.module.css';

function Header({ onMenuToggle }) {
  return (
    <header className={styles.header}>
      <nav className={styles.nav} aria-label="Main navigation">
        <div className={styles.container}>
          <h1 className={styles.title}>PromptLab</h1>

          <div className={styles.actions}>
            <ThemeToggle />
            <button
              className={styles.menuButton}
              onClick={onMenuToggle}
              aria-label="Toggle navigation menu"
              aria-expanded="false"
            >
              <span className={styles.hamburger}>☰</span>
            </button>
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;
