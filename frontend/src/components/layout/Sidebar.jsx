// src/components/layout/Sidebar.jsx

import { NavLink } from 'react-router-dom';
import styles from './Sidebar.module.css';

function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Backdrop for mobile */}
      {isOpen && (
        <div
          className={styles.backdrop}
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}
        aria-label="Sidebar navigation"
      >
        <nav className={styles.nav}>
          <ul className={styles.navList}>
            <li>
              <NavLink
                to="/prompts"
                className={({ isActive }) =>
                  `${styles.navLink} ${isActive ? styles.active : ''}`
                }
                onClick={onClose}
              >
                <span className={styles.icon}>📝</span>
                <span>All Prompts</span>
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/collections"
                className={({ isActive }) =>
                  `${styles.navLink} ${isActive ? styles.active : ''}`
                }
                onClick={onClose}
              >
                <span className={styles.icon}>📁</span>
                <span>Collections</span>
              </NavLink>
            </li>
          </ul>
        </nav>
      </aside>
    </>
  );
}

export default Sidebar;
