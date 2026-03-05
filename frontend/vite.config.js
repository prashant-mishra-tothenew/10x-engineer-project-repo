// vite.config.js

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,  // Development server port
    proxy: {
      '/api': 'http://localhost:8000',  // Proxy API requests to backend during development
    },
  },
  test: {
    environment: 'jsdom',  // Use jsdom for DOM testing
    globals: true,  // Enable global test APIs (describe, it, expect)
  },
});
