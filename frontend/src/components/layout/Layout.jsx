// src/components/layout/Layout.jsx

import { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import styles from './Layout.module.css';

function Layout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleMenuToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  return (
    <div className={styles.app}>
      <Header onMenuToggle={handleMenuToggle} />

      <div className={styles.appBody}>
        <Sidebar isOpen={isSidebarOpen} onClose={handleSidebarClose} />

        <main className={styles.content}>
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
