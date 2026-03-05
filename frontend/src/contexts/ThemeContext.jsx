import React, { createContext, useContext, useState, useEffect } from 'react';

/**
 * ThemeContext - Manages dark/light theme across the app
 * Similar to Context API in React or Vuex in Vue
 * Like a global state management system (Redux, Zustand)
 */
const ThemeContext = createContext();

/**
 * Custom hook to use theme context
 * Similar to useSelector in Redux or useContext pattern
 */
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

/**
 * ThemeProvider - Wraps the app to provide theme context
 * Similar to Provider in Redux or Context Provider in React
 */
export const ThemeProvider = ({ children }) => {
  // Safety check: ensure we're in a browser environment
  if (typeof window === 'undefined') {
    // Server-side rendering or test environment - provide minimal context
    const value = {
      theme: 'light',
      toggleTheme: () => {},
      setThemeMode: () => {},
      isDark: false,
    };
    return (
      <ThemeContext.Provider value={value}>
        {children}
      </ThemeContext.Provider>
    );
  }

  // Get initial theme from localStorage or system preference
  const getInitialTheme = () => {
    // Check if we're in a browser environment
    if (typeof window === 'undefined') {
      return 'light';
    }

    // Check localStorage first (user preference)
    try {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        return savedTheme;
      }
    } catch (error) {
      // localStorage might not be available (e.g., in some test environments)
      console.warn('localStorage not available:', error);
    }

    // Check system preference (like macOS dark mode)
    // Similar to window.matchMedia in JavaScript
    try {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
    } catch (error) {
      console.warn('matchMedia not available:', error);
    }

    return 'light';
  };

  const [theme, setTheme] = useState(getInitialTheme);

  // Apply theme to document root when it changes
  useEffect(() => {
    // Check if we're in a browser environment
    if (typeof document === 'undefined') {
      return;
    }

    // Add theme class to <html> element
    // This is like adding a class to document.documentElement in vanilla JS
    document.documentElement.setAttribute('data-theme', theme);

    // Save to localStorage for persistence
    // Like sessionStorage in PHP or localStorage in JavaScript
    try {
      localStorage.setItem('theme', theme);
    } catch (error) {
      console.warn('Could not save theme to localStorage:', error);
    }
  }, [theme]);

  // Listen for system theme changes
  useEffect(() => {
    // Check if matchMedia is supported
    if (typeof window === 'undefined' || !window.matchMedia) {
      return;
    }

    try {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

      // Check if mediaQuery is valid
      if (!mediaQuery) {
        return;
      }

      const handleChange = (e) => {
        // Only update if user hasn't set a preference
        try {
          if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
          }
        } catch (error) {
          console.warn('Error in theme change handler:', error);
        }
      };

      // Add event listener (like addEventListener in vanilla JS)
      // Some browsers use addListener instead of addEventListener
      try {
        if (mediaQuery.addEventListener) {
          mediaQuery.addEventListener('change', handleChange);
        } else if (mediaQuery.addListener) {
          mediaQuery.addListener(handleChange);
        }
      } catch (error) {
        console.warn('Could not add theme change listener:', error);
      }

      // Cleanup function (like componentWillUnmount in class components)
      return () => {
        try {
          if (mediaQuery.removeEventListener) {
            mediaQuery.removeEventListener('change', handleChange);
          } else if (mediaQuery.removeListener) {
            mediaQuery.removeListener(handleChange);
          }
        } catch (error) {
          console.warn('Could not remove theme change listener:', error);
        }
      };
    } catch (error) {
      console.warn('Error setting up theme change listener:', error);
      return undefined;
    }
  }, []);

  /**
   * Toggle between light and dark themes
   */
  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  /**
   * Set specific theme
   */
  const setThemeMode = (mode) => {
    if (mode === 'light' || mode === 'dark') {
      setTheme(mode);
    }
  };

  const value = {
    theme,
    toggleTheme,
    setThemeMode,
    isDark: theme === 'dark',
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};
