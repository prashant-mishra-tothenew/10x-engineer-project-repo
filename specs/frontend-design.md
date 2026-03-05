# Design Document: React Frontend Implementation

## Overview

This design document specifies the architecture and implementation details for the React-based frontend of PromptLab, an AI prompt engineering platform. The frontend provides a modern, responsive user interface for managing prompt templates and collections, connecting to the existing FastAPI backend via RESTful APIs.

The application follows a component-based architecture using React 18+ with functional components and hooks. It emphasizes user experience through responsive design, accessibility compliance, and clear feedback mechanisms for loading and error states.

### Key Design Principles

1. **Component Reusability**: Build small, focused components that can be composed together
2. **Separation of Concerns**: Keep API logic, business logic, and UI rendering separate
3. **User Feedback**: Provide clear loading states, error messages, and success confirmations
4. **Accessibility First**: Ensure WCAG AA compliance from the start, not as an afterthought
5. **Mobile-First Responsive**: Design for mobile screens first, then enhance for larger displays
6. **Developer Experience**: Use modern tooling (Vite) for fast development and optimized builds

### Technology Stack

- **React 18+**: UI library with hooks and functional components
- **Vite**: Build tool for fast development and optimized production builds
- **React Router v6**: Client-side routing and navigation
- **Axios**: HTTP client for API communication
- **CSS Modules** or **Tailwind CSS**: Styling approach (CSS Modules recommended for better encapsulation)
- **ESLint**: Code quality and consistency

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Application                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Presentation Layer                     │    │
│  │  (Components, Pages, Layout)                       │    │
│  └────────────────┬───────────────────────────────────┘    │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐    │
│  │           Application Layer                         │    │
│  │  (Hooks, Context, State Management)                │    │
│  └────────────────┬───────────────────────────────────┘    │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐    │
│  │              API Layer                              │    │
│  │  (HTTP Client, API Functions)                      │    │
│  └────────────────┬───────────────────────────────────┘    │
└───────────────────┼──────────────────────────────────────────┘
                    │
                    │ HTTP/JSON
                    │
┌───────────────────▼──────────────────────────────────────────┐
│              FastAPI Backend                                  │
│              (localhost:8000)                                 │
└───────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
frontend/
├── public/                    # Static assets
│   └── favicon.ico
├── src/
│   ├── api/                   # API integration layer
│   │   ├── client.js          # Axios configuration
│   │   ├── prompts.js         # Prompt API functions
│   │   ├── collections.js     # Collection API functions
│   │   └── tags.js            # Tag API functions
│   ├── components/            # Reusable UI components
│   │   ├── layout/
│   │   │   ├── Layout.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── prompts/
│   │   │   ├── PromptList.jsx
│   │   │   ├── PromptCard.jsx
│   │   │   ├── PromptForm.jsx
│   │   │   └── PromptDetail.jsx
│   │   ├── collections/
│   │   │   ├── CollectionList.jsx
│   │   │   └── CollectionForm.jsx
│   │   └── shared/
│   │       ├── Button.jsx
│   │       ├── Modal.jsx
│   │       ├── SearchBar.jsx
│   │       ├── LoadingSpinner.jsx
│   │       ├── ErrorMessage.jsx
│   │       └── ConfirmDialog.jsx
│   ├── hooks/                 # Custom React hooks
│   │   ├── usePrompts.js      # Prompt data fetching
│   │   ├── useCollections.js  # Collection data fetching
│   │   ├── useDebounce.js     # Debounced values
│   │   └── useAsync.js        # Async operation state
│   ├── pages/                 # Page components (routes)
│   │   ├── PromptsPage.jsx
│   │   ├── PromptDetailPage.jsx
│   │   └── CollectionsPage.jsx
│   ├── styles/                # Global styles and CSS modules
│   │   ├── global.css
│   │   └── variables.css
│   ├── utils/                 # Utility functions
│   │   ├── formatDate.js
│   │   └── extractVariables.js
│   ├── App.jsx                # Root component with routing
│   ├── main.jsx               # Application entry point
│   └── config.js              # Configuration (API URL, etc.)
├── .eslintrc.cjs              # ESLint configuration
├── index.html                 # HTML template
├── package.json               # Dependencies and scripts
└── vite.config.js             # Vite configuration
```

## Components and Interfaces

### Component Hierarchy

```
App
├── Layout
│   ├── Header
│   └── Sidebar
└── Routes
    ├── PromptsPage
    │   ├── SearchBar
    │   ├── Button (Create New)
    │   ├── PromptList
    │   │   └── PromptCard (multiple)
    │   ├── Modal
    │   │   └── PromptForm
    │   └── ConfirmDialog
    ├── PromptDetailPage
    │   ├── PromptDetail
    │   ├── Button (Edit, Delete, Back)
    │   ├── Modal
    │   │   └── PromptForm
    │   └── ConfirmDialog
    └── CollectionsPage
        ├── Button (Create New)
        ├── CollectionList
        ├── Modal
        │   └── CollectionForm
        └── ConfirmDialog
```

### Core Components

#### Layout Components

**Layout.jsx**
```javascript
// Wrapper component providing consistent structure
// Props: children
// Renders: Header + Sidebar + main content area
// Responsive: Collapses sidebar on mobile
```

**Header.jsx**
```javascript
// Top navigation bar
// Props: none
// Displays: App title, hamburger menu (mobile)
// Accessibility: nav element, proper ARIA labels
```

**Sidebar.jsx**
```javascript
// Navigation sidebar
// Props: isOpen (mobile), onClose
// Displays: Navigation links (All Prompts, Collections)
// Highlights: Active route
// Responsive: Overlay on mobile, fixed on desktop
```

#### Prompt Components

**PromptList.jsx**
```javascript
// Container for prompt cards
// Props: prompts[], loading, error, onEdit, onDelete
// Displays: Grid of PromptCard components
// States: Loading spinner, error message, empty state
// Responsive: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
```

**PromptCard.jsx**
```javascript
// Individual prompt display card
// Props: prompt, onEdit, onDelete, onClick
// Displays: Title, content preview (truncated), collection badge, timestamps
// Actions: Edit button, delete button, click to view detail
// Accessibility: article element, button labels
```

**PromptForm.jsx**
```javascript
// Form for creating/editing prompts
// Props: initialData, onSubmit, onCancel, collections[]
// Fields: title (required), content (required), description, collection_id
// Validation: Client-side validation before submit
// States: Submitting (disabled buttons, loading indicator)
// Accessibility: Labels, error messages, focus management
```

**PromptDetail.jsx**
```javascript
// Full prompt view
// Props: prompt, onEdit, onDelete
// Displays: Full title, content with highlighted variables, metadata
// Features: Variable highlighting ({{variable}} pattern)
// Actions: Edit, delete, back buttons
```

#### Collection Components

**CollectionList.jsx**
```javascript
// List of collections
// Props: collections[], loading, error, onEdit, onDelete, onSelect
// Displays: Collection cards with name, description, prompt count
// Actions: Edit, delete, click to filter prompts
```

**CollectionForm.jsx**
```javascript
// Form for creating/editing collections
// Props: initialData, onSubmit, onCancel
// Fields: name (required), description
// Validation: Client-side validation
// States: Submitting state
```

#### Shared Components

**Button.jsx**
```javascript
// Reusable button component
// Props: children, onClick, variant (primary/secondary/danger),
//        disabled, loading, type (button/submit)
// Variants: Different colors for different actions
// States: Loading spinner when loading=true
// Accessibility: Proper button element, disabled state
```

**Modal.jsx**
```javascript
// Modal dialog overlay
// Props: isOpen, onClose, title, children
// Features: Backdrop click to close, ESC key to close
// Accessibility: Focus trap, ARIA role="dialog", focus management
// Animation: Fade in/out
```

**SearchBar.jsx**
```javascript
// Search input with debouncing
// Props: value, onChange, placeholder, debounceMs (default 300)
// Features: Debounced input to avoid excessive API calls
// Accessibility: Label, clear button
```

**LoadingSpinner.jsx**
```javascript
// Loading indicator
// Props: size (small/medium/large), message
// Displays: Spinning animation, optional message
// Accessibility: role="status", aria-live="polite"
```

**ErrorMessage.jsx**
```javascript
// Error display component
// Props: message, onRetry, onDismiss
// Displays: Error icon, message, retry button
// Variants: Different styles for different error types
// Accessibility: role="alert", aria-live="assertive"
```

**ConfirmDialog.jsx**
```javascript
// Confirmation dialog for destructive actions
// Props: isOpen, title, message, onConfirm, onCancel, loading
// Displays: Warning icon, message, confirm/cancel buttons
// States: Loading state during confirmation
// Accessibility: Focus management, ESC to cancel
```

### Component Props and State

#### PromptCard Example

```javascript
// Props Interface (TypeScript-style documentation)
interface PromptCardProps {
  prompt: {
    id: string;
    title: string;
    content: string;
    description?: string;
    collection_id?: string;
    created_at: string;
    updated_at: string;
  };
  collectionName?: string;
  onEdit: (promptId: string) => void;
  onDelete: (promptId: string) => void;
  onClick: (promptId: string) => void;
}

// Internal State: None (stateless component)
```

#### PromptForm Example

```javascript
// Props Interface
interface PromptFormProps {
  initialData?: {
    id?: string;
    title: string;
    content: string;
    description?: string;
    collection_id?: string;
  };
  collections: Array<{id: string; name: string}>;
  onSubmit: (data: PromptData) => Promise<void>;
  onCancel: () => void;
}

// Internal State
{
  title: string;
  content: string;
  description: string;
  collection_id: string;
  errors: {
    title?: string;
    content?: string;
  };
  isSubmitting: boolean;
}
```

## Data Models

### Frontend Data Models

These models mirror the backend Pydantic models but are plain JavaScript objects.

#### Prompt Model

```javascript
{
  id: string;              // UUID
  title: string;           // 1-200 characters
  content: string;         // 1+ characters
  description: string | null;  // 0-500 characters
  collection_id: string | null;  // UUID or null
  tags: string[];          // Array of tag names
  created_at: string;      // ISO 8601 datetime
  updated_at: string;      // ISO 8601 datetime
}
```

#### Collection Model

```javascript
{
  id: string;              // UUID
  name: string;            // 1-100 characters
  description: string | null;  // 0-500 characters
  created_at: string;      // ISO 8601 datetime
}
```

#### Tag Model

```javascript
{
  tag_id: string;          // UUID
  name: string;            // 1-50 characters
  created_at: string;      // ISO 8601 datetime
}
```

### API Response Models

#### PromptList Response

```javascript
{
  prompts: Prompt[];
  total: number;
}
```

#### CollectionList Response

```javascript
{
  collections: Collection[];
  total: number;
}
```

#### Error Response

```javascript
{
  detail: string;  // Error message from backend
}
```

### Form Data Models

#### PromptFormData

```javascript
{
  title: string;
  content: string;
  description: string;
  collection_id: string | null;
  tags: string[];
}
```

#### CollectionFormData

```javascript
{
  name: string;
  description: string;
}
```

## API Integration Layer

### API Client Configuration

**src/api/client.js**

```javascript
import axios from 'axios';
import { API_BASE_URL } from '../config';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,  // http://localhost:8000
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,  // 10 second timeout
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Extract error message from response
    const message = error.response?.data?.detail
      || error.message
      || 'An unexpected error occurred';

    // Create enhanced error object
    const enhancedError = new Error(message);
    enhancedError.status = error.response?.status;
    enhancedError.originalError = error;

    return Promise.reject(enhancedError);
  }
);

export default apiClient;
```

### Prompt API Functions

**src/api/prompts.js**

```javascript
import apiClient from './client';

// Get all prompts with optional filters
export const getPrompts = async (filters = {}) => {
  const params = {};
  if (filters.collection_id) params.collection_id = filters.collection_id;
  if (filters.search) params.search = filters.search;
  if (filters.tags) params.tags = filters.tags.join(',');

  const response = await apiClient.get('/prompts', { params });
  return response.data;
};

// Get single prompt by ID
export const getPrompt = async (id) => {
  const response = await apiClient.get(`/prompts/${id}`);
  return response.data;
};

// Create new prompt
export const createPrompt = async (data) => {
  const response = await apiClient.post('/prompts', data);
  return response.data;
};

// Update prompt (full update)
export const updatePrompt = async (id, data) => {
  const response = await apiClient.put(`/prompts/${id}`, data);
  return response.data;
};

// Partially update prompt
export const patchPrompt = async (id, data) => {
  const response = await apiClient.patch(`/prompts/${id}`, data);
  return response.data;
};

// Delete prompt
export const deletePrompt = async (id) => {
  await apiClient.delete(`/prompts/${id}`);
};

// Update prompt tags only
export const updatePromptTags = async (id, tags) => {
  const response = await apiClient.put(`/prompts/${id}/tags`, { tags });
  return response.data;
};
```

### Collection API Functions

**src/api/collections.js**

```javascript
import apiClient from './client';

// Get all collections
export const getCollections = async () => {
  const response = await apiClient.get('/collections');
  return response.data;
};

// Get single collection by ID
export const getCollection = async (id) => {
  const response = await apiClient.get(`/collections/${id}`);
  return response.data;
};

// Create new collection
export const createCollection = async (data) => {
  const response = await apiClient.post('/collections', data);
  return response.data;
};

// Delete collection
export const deleteCollection = async (id) => {
  await apiClient.delete(`/collections/${id}`);
};
```

### Tag API Functions

**src/api/tags.js**

```javascript
import apiClient from './client';

// Get all tags
export const getTags = async () => {
  const response = await apiClient.get('/tags');
  return response.data;
};

// Get single tag by ID
export const getTag = async (id) => {
  const response = await apiClient.get(`/tags/${id}`);
  return response.data;
};

// Create new tag (or get existing)
export const createTag = async (name) => {
  const response = await apiClient.post('/tags', { name });
  return response.data;
};
```

## State Management

### Approach: Local State + Custom Hooks

The application uses React's built-in state management (useState, useReducer) combined with custom hooks for data fetching. This approach is sufficient for the application's complexity and avoids the overhead of external state management libraries like Redux.

### Custom Hooks

#### usePrompts Hook

```javascript
// src/hooks/usePrompts.js
import { useState, useEffect } from 'react';
import { getPrompts } from '../api/prompts';

export const usePrompts = (filters = {}) => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPrompts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getPrompts(filters);
      setPrompts(data.prompts);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, [JSON.stringify(filters)]);  // Re-fetch when filters change

  return { prompts, loading, error, refetch: fetchPrompts };
};
```

#### useCollections Hook

```javascript
// src/hooks/useCollections.js
import { useState, useEffect } from 'react';
import { getCollections } from '../api/collections';

export const useCollections = () => {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCollections = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCollections();
      setCollections(data.collections);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCollections();
  }, []);

  return { collections, loading, error, refetch: fetchCollections };
};
```

#### useDebounce Hook

```javascript
// src/hooks/useDebounce.js
import { useState, useEffect } from 'react';

export const useDebounce = (value, delay = 300) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
```

#### useAsync Hook

```javascript
// src/hooks/useAsync.js
import { useState, useCallback } from 'react';

export const useAsync = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (asyncFunction) => {
    try {
      setLoading(true);
      setError(null);
      const result = await asyncFunction();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
  }, []);

  return { loading, error, execute, reset };
};
```

### Data Flow Pattern

```
User Action (e.g., click "Create Prompt")
    ↓
Component Event Handler
    ↓
Call API Function (e.g., createPrompt)
    ↓
API Client sends HTTP request
    ↓
Backend processes request
    ↓
API Client receives response
    ↓
Update Local State (via hook or setState)
    ↓
React Re-renders Component
    ↓
UI Updates
```

## Routing Structure

### Route Configuration

**src/App.jsx**

```javascript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import PromptsPage from './pages/PromptsPage';
import PromptDetailPage from './pages/PromptDetailPage';
import CollectionsPage from './pages/CollectionsPage';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/prompts" replace />} />
          <Route path="/prompts" element={<PromptsPage />} />
          <Route path="/prompts/:id" element={<PromptDetailPage />} />
          <Route path="/collections" element={<CollectionsPage />} />
          <Route path="*" element={<div>404 - Page Not Found</div>} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
```

### Route Descriptions

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | Navigate | Redirects to `/prompts` |
| `/prompts` | PromptsPage | List all prompts with search and filters |
| `/prompts/:id` | PromptDetailPage | View single prompt details |
| `/collections` | CollectionsPage | Manage collections |
| `*` | 404 | Catch-all for undefined routes |

### Navigation Flow

```
┌─────────────┐
│   /prompts  │ ←──────────────┐
│ (List View) │                │
└──────┬──────┘                │
       │                       │
       │ Click Card            │ Back Button
       │                       │
       ▼                       │
┌──────────────┐               │
│ /prompts/:id │ ──────────────┘
│ (Detail View)│
└──────────────┘

┌──────────────┐
│ /collections │
│ (Collections)│
└──────────────┘
```


## Styling Approach

### CSS Modules (Recommended)

CSS Modules provide scoped styling that prevents class name conflicts and makes components more maintainable. Each component has its own CSS file.

**Example: PromptCard.module.css**

```css
.card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: box-shadow 0.2s;
  cursor: pointer;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card:focus-within {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.content {
  color: #4a4a4a;
  margin-bottom: 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.metadata {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #6a6a6a;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
```

**Usage in Component:**

```javascript
import styles from './PromptCard.module.css';

function PromptCard({ prompt }) {
  return (
    <article className={styles.card}>
      <h3 className={styles.title}>{prompt.title}</h3>
      <p className={styles.content}>{prompt.content}</p>
      <div className={styles.metadata}>
        <span>{formatDate(prompt.created_at)}</span>
      </div>
    </article>
  );
}
```

### Design System Variables

**src/styles/variables.css**

```css
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-primary-hover: #0052a3;
  --color-secondary: #6c757d;
  --color-danger: #dc3545;
  --color-danger-hover: #c82333;
  --color-success: #28a745;
  --color-warning: #ffc107;

  /* Neutrals */
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #4a4a4a;
  --color-text-muted: #6a6a6a;
  --color-border: #e0e0e0;
  --color-background: #f5f5f5;
  --color-surface: #ffffff;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 2rem;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.15);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;

  /* Z-index */
  --z-dropdown: 1000;
  --z-modal: 1050;
  --z-tooltip: 1100;
}
```

### Responsive Breakpoints

```css
/* Mobile First Approach */

/* Mobile: Default (< 768px) */
/* No media query needed */

/* Tablet: 768px and up */
@media (min-width: 768px) {
  /* Styles for tablet */
}

/* Desktop: 1024px and up */
@media (min-width: 1024px) {
  /* Styles for desktop */
}

/* Large Desktop: 1440px and up */
@media (min-width: 1440px) {
  /* Styles for large screens */
}
```

### Global Styles

**src/styles/global.css**

```css
@import './variables.css';

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  line-height: 1.5;
  color: var(--color-text-primary);
  background-color: var(--color-background);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Focus visible for keyboard navigation */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove focus outline for mouse users */
*:focus:not(:focus-visible) {
  outline: none;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  line-height: 1.2;
}

/* Links */
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--color-primary-hover);
}

/* Buttons */
button {
  font-family: inherit;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Form elements */
input, textarea, select {
  font-family: inherit;
  font-size: inherit;
}

/* Scrollbar styling (webkit browsers) */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-background);
}

::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-muted);
}
```

## Error Handling Patterns

### Error Types and Handling

#### Network Errors

```javascript
// When backend is unreachable
{
  type: 'network',
  message: 'Unable to connect to server. Please check your connection.',
  retryable: true
}
```

#### Validation Errors (400)

```javascript
// When request data is invalid
{
  type: 'validation',
  message: 'Collection not found',
  retryable: false
}
```

#### Not Found Errors (404)

```javascript
// When resource doesn't exist
{
  type: 'not_found',
  message: 'Prompt not found',
  retryable: false
}
```

#### Server Errors (500)

```javascript
// When backend has internal error
{
  type: 'server',
  message: 'An unexpected error occurred. Please try again.',
  retryable: true
}
```

### Error Display Strategy

**Page-Level Errors**: Display at top of page with retry button

```javascript
{error && (
  <ErrorMessage
    message={error}
    onRetry={refetch}
    onDismiss={() => setError(null)}
  />
)}
```

**Form-Level Errors**: Display above form with context

```javascript
{submitError && (
  <div className={styles.formError}>
    <ErrorMessage message={submitError} />
  </div>
)}
```

**Inline Field Errors**: Display below input field

```javascript
<input
  className={errors.title ? styles.inputError : styles.input}
  {...props}
/>
{errors.title && (
  <span className={styles.fieldError}>{errors.title}</span>
)}
```

### Error Recovery

**Automatic Retry**: For network errors, provide retry button

```javascript
const handleRetry = async () => {
  setError(null);
  await refetch();
};
```

**Graceful Degradation**: Show cached data when available

```javascript
if (error && prompts.length > 0) {
  // Show stale data with warning
  return (
    <>
      <ErrorMessage message="Unable to refresh. Showing cached data." />
      <PromptList prompts={prompts} />
    </>
  );
}
```

**User Feedback**: Always inform user of what went wrong and what they can do

```javascript
const getErrorMessage = (error) => {
  if (error.status === 404) {
    return 'This prompt no longer exists.';
  }
  if (error.status === 400) {
    return error.message; // Backend validation message
  }
  if (error.message.includes('timeout')) {
    return 'Request timed out. Please try again.';
  }
  return 'Something went wrong. Please try again.';
};
```

## Loading State Patterns

### Loading State Types

#### Initial Load

Full page loading spinner while fetching initial data

```javascript
if (loading && prompts.length === 0) {
  return (
    <div className={styles.loadingContainer}>
      <LoadingSpinner size="large" message="Loading prompts..." />
    </div>
  );
}
```

#### Refresh/Refetch

Subtle loading indicator while refreshing data

```javascript
<div className={styles.header}>
  <h1>Prompts</h1>
  {loading && <LoadingSpinner size="small" />}
</div>
```

#### Form Submission

Disabled button with loading indicator

```javascript
<Button
  type="submit"
  disabled={isSubmitting}
  loading={isSubmitting}
>
  {isSubmitting ? 'Creating...' : 'Create Prompt'}
</Button>
```

#### Inline Action

Loading state on specific action button

```javascript
<Button
  variant="danger"
  onClick={handleDelete}
  loading={deleting}
  disabled={deleting}
>
  {deleting ? 'Deleting...' : 'Delete'}
</Button>
```

#### Skeleton UI (Optional Enhancement)

Show placeholder content while loading

```javascript
if (loading) {
  return (
    <div className={styles.grid}>
      {[1, 2, 3, 4, 5, 6].map(i => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
```

### Loading State Best Practices

1. **Prevent Duplicate Submissions**: Disable buttons during loading
2. **Provide Feedback**: Show what's happening ("Creating...", "Deleting...")
3. **Maintain Layout**: Don't shift content when showing loading indicators
4. **Timeout Handling**: Show error after reasonable timeout (10 seconds)
5. **Optimistic Updates**: Update UI immediately, rollback on error (advanced)

## Responsive Design Strategy

### Mobile-First Approach

Start with mobile layout, then enhance for larger screens using min-width media queries.

### Layout Adaptations

#### Header

**Mobile (< 768px)**
- Hamburger menu icon
- Compact title
- Full-width

**Desktop (≥ 1024px)**
- Full navigation visible
- Logo + title
- Fixed height

#### Sidebar

**Mobile (< 768px)**
- Hidden by default
- Overlay when opened (hamburger menu)
- Full-screen overlay with close button
- Slide-in animation

**Tablet (768px - 1023px)**
- Collapsible sidebar
- Icon + text navigation

**Desktop (≥ 1024px)**
- Fixed sidebar (always visible)
- Full navigation with icons and text
- 250px width

#### Prompt Grid

**Mobile (< 768px)**
- 1 column
- Full-width cards
- Vertical stacking

**Tablet (768px - 1023px)**
- 2 columns
- Grid gap: 1rem

**Desktop (≥ 1024px)**
- 3 columns
- Grid gap: 1.5rem

**Large Desktop (≥ 1440px)**
- 4 columns
- Grid gap: 1.5rem

### Touch Targets

All interactive elements must meet minimum touch target size:

- **Minimum**: 44px × 44px (WCAG AAA)
- **Recommended**: 48px × 48px

```css
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 0.75rem 1.5rem;
}

.iconButton {
  width: 44px;
  height: 44px;
  padding: 0.5rem;
}
```

### Responsive Typography

```css
/* Mobile */
.title {
  font-size: 1.5rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .title {
    font-size: 2rem;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .title {
    font-size: 2.5rem;
  }
}
```

### Responsive Images and Icons

Use SVG icons for scalability and clarity at all sizes.

```javascript
// Icon component with size prop
<Icon name="edit" size={isMobile ? 20 : 24} />
```

## Accessibility Implementation

### Semantic HTML

Use proper HTML elements for their intended purpose:

```javascript
// Good: Semantic structure
<nav>
  <ul>
    <li><a href="/prompts">Prompts</a></li>
  </ul>
</nav>

<main>
  <article>
    <h2>Prompt Title</h2>
    <p>Content...</p>
  </article>
</main>

// Bad: Divs for everything
<div>
  <div onClick={navigate}>Prompts</div>
</div>
```

### ARIA Labels and Roles

#### Icon-Only Buttons

```javascript
<button
  aria-label="Edit prompt"
  onClick={handleEdit}
>
  <EditIcon />
</button>
```

#### Modal Dialogs

```javascript
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Create New Prompt</h2>
  {/* Modal content */}
</div>
```

#### Loading States

```javascript
<div role="status" aria-live="polite">
  <LoadingSpinner />
  <span className="sr-only">Loading prompts...</span>
</div>
```

#### Error Messages

```javascript
<div role="alert" aria-live="assertive">
  {error}
</div>
```

### Keyboard Navigation

#### Focus Management

```javascript
// Focus first input when modal opens
useEffect(() => {
  if (isOpen) {
    inputRef.current?.focus();
  }
}, [isOpen]);

// Return focus when modal closes
const handleClose = () => {
  onClose();
  triggerButtonRef.current?.focus();
};
```

#### Keyboard Shortcuts

```javascript
// ESC to close modal
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      handleClose();
    }
  };

  if (isOpen) {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }
}, [isOpen]);
```

#### Tab Order

Ensure logical tab order through DOM structure, not CSS positioning.

```javascript
// Good: DOM order matches visual order
<form>
  <input name="title" />
  <textarea name="content" />
  <button type="submit">Submit</button>
</form>
```

### Focus Indicators

```css
/* Visible focus indicator */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* High contrast focus for buttons */
button:focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Color Contrast

Ensure WCAG AA compliance (4.5:1 for normal text, 3:1 for large text):

```css
/* Good: High contrast */
.text {
  color: #1a1a1a;  /* Dark text */
  background: #ffffff;  /* White background */
  /* Contrast ratio: 16.1:1 */
}

/* Good: Sufficient contrast for large text */
.heading {
  color: #4a4a4a;  /* Medium gray */
  background: #ffffff;
  font-size: 1.5rem;
  /* Contrast ratio: 9.7:1 */
}
```

### Screen Reader Support

#### Skip Links

```javascript
// Allow keyboard users to skip navigation
<a href="#main-content" className="skip-link">
  Skip to main content
</a>

<main id="main-content">
  {/* Page content */}
</main>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: white;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

#### Visually Hidden Text

```css
/* Screen reader only text */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

#### Live Regions

```javascript
// Announce dynamic content changes
<div aria-live="polite" aria-atomic="true">
  {prompts.length} prompts found
</div>
```

### Form Accessibility

```javascript
<form>
  <div className={styles.field}>
    <label htmlFor="title">
      Title <span aria-label="required">*</span>
    </label>
    <input
      id="title"
      type="text"
      required
      aria-required="true"
      aria-invalid={errors.title ? 'true' : 'false'}
      aria-describedby={errors.title ? 'title-error' : undefined}
    />
    {errors.title && (
      <span id="title-error" className={styles.error} role="alert">
        {errors.title}
      </span>
    )}
  </div>
</form>
```

## Build Configuration

### Vite Configuration

**vite.config.js**

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,  // Open browser on start
    proxy: {
      // Proxy API requests to backend during development
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,  // Generate source maps for debugging
    rollupOptions: {
      output: {
        manualChunks: {
          // Split vendor code for better caching
          vendor: ['react', 'react-dom', 'react-router-dom'],
          api: ['axios'],
        },
      },
    },
  },
  css: {
    modules: {
      localsConvention: 'camelCase',  // Allow camelCase in JS
    },
  },
});
```

### Environment Variables

**.env.development**

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=PromptLab
```

**.env.production**

```
VITE_API_BASE_URL=https://api.promptlab.com
VITE_APP_NAME=PromptLab
```

**src/config.js**

```javascript
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'PromptLab';
export const IS_DEV = import.meta.env.DEV;
export const IS_PROD = import.meta.env.PROD;
```

### ESLint Configuration

**.eslintrc.cjs**

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  settings: { react: { version: '18.2' } },
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'react/prop-types': 'off',  // Using TypeScript or JSDoc instead
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
  },
};
```

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  }
}
```

### Dependencies

**package.json**

```json
{
  "name": "promptlab-frontend",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "vite": "^5.0.8"
  }
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified several areas of redundancy:

**Redundancy Analysis:**

1. **Form Validation Properties (5.3, 5.4, 6.3, 6.4)**: The validation requirements for title and content are identical for both create and edit forms. These can be combined into universal form validation properties.

2. **Error Display Properties (4.6, 5.7, 6.7, 7.6, 13.1)**: Multiple requirements state that errors should be displayed. These can be consolidated into a single property about error handling.

3. **Loading State Properties (4.5, 5.8, 6.8, 7.7, 12.1, 12.2, 12.3)**: Multiple requirements about showing loading indicators can be combined into properties about loading state management.

4. **Button Existence Properties (6.1, 7.1, 9.6)**: Requirements about buttons existing on cards can be combined into a property about action availability.

5. **Success Handling (5.6, 6.6, 7.5)**: Similar patterns for handling successful operations can be consolidated.

**Consolidated Properties:**

After reflection, I've identified the following unique, non-redundant properties that provide comprehensive validation coverage:

### Property 1: API Client Headers

*For any* HTTP request made by the API client, the request SHALL include the Content-Type header set to "application/json".

**Validates: Requirements 2.2**

### Property 2: Error Message Extraction

*For any* error response from the backend, the API client SHALL extract the error message from the response detail field and propagate it to the caller.

**Validates: Requirements 2.3**

### Property 3: Query Parameter Encoding

*For any* search or filter parameters passed to the API client, they SHALL be properly encoded as URL query parameters in the request.

**Validates: Requirements 2.6**

### Property 4: Layout Consistency

*For any* page route in the application, both the header and sidebar components SHALL be rendered as part of the layout.

**Validates: Requirements 3.1, 3.2**

### Property 5: Client-Side Routing

*For any* navigation link click, the application SHALL update the route without triggering a full page reload.

**Validates: Requirements 3.4**

### Property 6: Active Route Highlighting

*For any* current route, the corresponding navigation item SHALL have an active state indicator.

**Validates: Requirements 3.5**

### Property 7: Prompt Card Content

*For any* prompt displayed in a list, the prompt card SHALL include the title, content preview, and timestamps (created_at and updated_at).

**Validates: Requirements 4.2, 4.4**

### Property 8: Collection Name Display

*For any* prompt that has a non-null collection_id, the prompt card SHALL display the associated collection name.

**Validates: Requirements 4.3**

### Property 9: Error State Display

*For any* failed data fetch operation, an error message SHALL be displayed to the user.

**Validates: Requirements 4.6, 5.7, 6.7, 7.6, 13.1**

### Property 10: Form Validation - Required Fields

*For any* prompt form submission (create or edit), if the title or content field is empty or contains only whitespace, the form SHALL prevent submission and display a validation error.

**Validates: Requirements 5.3, 5.4, 6.3, 6.4**

### Property 11: Edit Form Pre-population

*For any* prompt being edited, when the edit form opens, all form fields SHALL be pre-populated with the prompt's current data (title, content, description, collection_id).

**Validates: Requirements 6.2**

### Property 12: Action Button Availability

*For any* prompt card or detail view, edit and delete action buttons SHALL be available to the user.

**Validates: Requirements 6.1, 7.1, 8.4**

### Property 13: Delete Confirmation Required

*For any* delete action initiated by the user, a confirmation dialog SHALL be displayed before the delete request is sent to the backend.

**Validates: Requirements 7.2, 7.3**

### Property 14: Prompt Detail Navigation

*For any* prompt card clicked in the list view, the application SHALL navigate to the detail view for that specific prompt.

**Validates: Requirements 8.1**

### Property 15: Prompt Detail Completeness

*For any* prompt displayed in the detail view, all prompt fields SHALL be shown: title, full content, description, collection name (if assigned), created_at, and updated_at.

**Validates: Requirements 8.2**

### Property 16: Variable Placeholder Highlighting

*For any* prompt content containing the pattern `{{variableName}}`, those variable placeholders SHALL be visually distinguished from regular text.

**Validates: Requirements 8.3**

### Property 17: Collection Display Completeness

*For any* collection displayed in the collections list, the collection card SHALL show the name, description, and count of prompts in that collection.

**Validates: Requirements 9.2, 9.6**

### Property 18: Collection Filtering

*For any* collection selected as a filter, the prompts list SHALL display only prompts where collection_id matches the selected collection's ID.

**Validates: Requirements 10.1**

### Property 19: Search Query Transmission

*For any* non-empty search input value (after debouncing), a request SHALL be sent to the backend with the search query as a parameter.

**Validates: Requirements 11.2**

### Property 20: Search Debouncing

*For any* sequence of search input changes, API requests SHALL only be triggered after the input has been stable for at least 300ms.

**Validates: Requirements 11.3**

### Property 21: Loading State During Data Fetch

*For any* asynchronous data fetch operation in progress, a loading indicator SHALL be displayed to the user.

**Validates: Requirements 12.1, 4.5, 8.6**

### Property 22: Form Submission Loading State

*For any* form submission in progress, the submit button SHALL be disabled and display a loading indicator.

**Validates: Requirements 12.2, 5.8, 6.8**

### Property 23: Delete Operation Loading State

*For any* delete operation in progress, the delete button SHALL display a loading indicator.

**Validates: Requirements 12.3, 7.7**

### Property 24: Duplicate Submission Prevention

*For any* form or action with a request in progress, subsequent submission attempts SHALL be prevented until the current request completes.

**Validates: Requirements 12.4**

### Property 25: Loading State Cleanup

*For any* asynchronous operation that completes (success or failure), the loading indicator SHALL be removed.

**Validates: Requirements 12.5**

### Property 26: Error Type Differentiation

*For any* error encountered, the error handling SHALL distinguish between network errors, validation errors (400), not found errors (404), and server errors (500), displaying appropriate messages for each type.

**Validates: Requirements 13.2**

### Property 27: Retry Button for Retryable Errors

*For any* error that is retryable (network errors, server errors), a retry button SHALL be provided to the user.

**Validates: Requirements 13.4**

### Property 28: Error Clearing on Action

*For any* displayed error message, the error SHALL be cleared when the user retries the operation or navigates to a different view.

**Validates: Requirements 13.5**

### Property 29: Inline Validation Errors

*For any* form field validation error, the error message SHALL be displayed adjacent to the invalid field.

**Validates: Requirements 13.6**

### Property 30: Semantic HTML Usage

*For any* component rendered, appropriate semantic HTML elements SHALL be used (nav for navigation, main for main content, article for prompts, button for actions).

**Validates: Requirements 15.1**

### Property 31: Icon Button Accessibility

*For any* button that contains only an icon without visible text, an aria-label attribute SHALL be present describing the button's action.

**Validates: Requirements 15.2**

### Property 32: Keyboard Navigation Support

*For any* interactive element (buttons, links, form inputs), the element SHALL be keyboard accessible (focusable and operable via keyboard).

**Validates: Requirements 15.3**

### Property 33: Image Alt Text

*For any* image element rendered, an alt attribute SHALL be present with descriptive text.

**Validates: Requirements 15.6**

### Property 34: Dynamic Content Announcements

*For any* dynamic content change (loading complete, error occurred, items added/removed), appropriate ARIA live regions SHALL be used to announce changes to screen readers.

**Validates: Requirements 15.7**

### Property 35: JSON Response Parsing

*For any* successful HTTP response from the backend, the response body SHALL be parsed as JSON and the resulting data structure SHALL match the expected model.

**Validates: Requirements 16.4**

### Property 36: HTTP Status Code Handling

*For any* HTTP response received, the application SHALL handle the status code appropriately: 200/201 as success, 204 as success with no content, 400 as validation error, 404 as not found, 500 as server error.

**Validates: Requirements 16.6**

## Error Handling

### Error Categories

The application handles four main categories of errors:

1. **Network Errors**: Connection failures, timeouts, DNS resolution failures
2. **Client Errors (4xx)**: Validation errors (400), not found (404), unauthorized (401)
3. **Server Errors (5xx)**: Internal server errors (500), service unavailable (503)
4. **Application Errors**: JavaScript errors, state management issues, unexpected conditions

### Error Handling Strategy

#### API Layer Error Handling

All errors from the backend are intercepted and normalized in the API client:

```javascript
// Error interceptor in apiClient
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const enhancedError = {
      message: error.response?.data?.detail || error.message,
      status: error.response?.status,
      type: categorizeError(error),
      retryable: isRetryable(error),
    };
    return Promise.reject(enhancedError);
  }
);

function categorizeError(error) {
  if (!error.response) return 'network';
  if (error.response.status >= 500) return 'server';
  if (error.response.status === 404) return 'not_found';
  if (error.response.status === 400) return 'validation';
  return 'client';
}

function isRetryable(error) {
  return !error.response || error.response.status >= 500;
}
```

#### Component-Level Error Handling

Components use the error information to provide appropriate feedback:

```javascript
// In a component
const { prompts, loading, error, refetch } = usePrompts();

if (error) {
  return (
    <ErrorMessage
      message={error.message}
      type={error.type}
      onRetry={error.retryable ? refetch : undefined}
    />
  );
}
```

### Error Recovery Mechanisms

1. **Automatic Retry**: For network and server errors, provide retry button
2. **Graceful Degradation**: Show cached data when available during errors
3. **User Guidance**: Provide clear instructions on how to resolve errors
4. **Error Boundaries**: React error boundaries catch rendering errors

### Error Logging

In production, errors should be logged to a monitoring service:

```javascript
// Error logging utility
export const logError = (error, context) => {
  if (IS_PROD) {
    // Send to monitoring service (e.g., Sentry)
    console.error('Error:', error, 'Context:', context);
  } else {
    // Detailed logging in development
    console.error('Error:', error);
    console.error('Context:', context);
    console.trace();
  }
};
```

## Testing Strategy

### Dual Testing Approach

The frontend will employ both unit testing and property-based testing to ensure comprehensive coverage:

**Unit Tests**: Focus on specific examples, edge cases, and integration points
- Component rendering with specific props
- User interaction flows (click, type, submit)
- Edge cases (empty states, error states, loading states)
- Integration between components

**Property-Based Tests**: Verify universal properties across all inputs
- Form validation with generated inputs
- API client behavior with various responses
- Component rendering with random data
- Error handling with different error types

### Testing Tools

**Unit Testing**:
- **Vitest**: Fast unit test runner (Vite-native alternative to Jest)
- **React Testing Library**: Component testing with user-centric queries
- **MSW (Mock Service Worker)**: API mocking for integration tests

**Property-Based Testing**:
- **fast-check**: Property-based testing library for JavaScript
- Minimum 100 iterations per property test
- Each test tagged with reference to design property

### Test Organization

```
frontend/
├── src/
│   ├── components/
│   │   ├── Button.jsx
│   │   ├── Button.test.jsx          # Unit tests
│   │   └── Button.properties.test.jsx  # Property tests
│   ├── api/
│   │   ├── client.js
│   │   ├── client.test.js
│   │   └── client.properties.test.js
│   └── hooks/
│       ├── useDebounce.js
│       ├── useDebounce.test.js
│       └── useDebounce.properties.test.js
```

### Unit Test Examples

**Component Rendering Test**:
```javascript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PromptCard from './PromptCard';

describe('PromptCard', () => {
  it('displays prompt title, content, and timestamps', () => {
    const prompt = {
      id: '123',
      title: 'Test Prompt',
      content: 'Test content',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
    };

    render(<PromptCard prompt={prompt} />);

    expect(screen.getByText('Test Prompt')).toBeInTheDocument();
    expect(screen.getByText(/Test content/)).toBeInTheDocument();
  });
});
```

**User Interaction Test**:
```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import PromptForm from './PromptForm';

describe('PromptForm', () => {
  it('shows validation error when title is empty', async () => {
    const onSubmit = vi.fn();
    render(<PromptForm onSubmit={onSubmit} />);

    const submitButton = screen.getByRole('button', { name: /create/i });
    await userEvent.click(submitButton);

    expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });
});
```

### Property-Based Test Examples

**Form Validation Property**:
```javascript
import { describe, it } from 'vitest';
import fc from 'fast-check';
import { validatePromptForm } from './validation';

describe('PromptForm Properties', () => {
  it('Property 10: rejects forms with empty or whitespace-only title', () => {
    /**
     * Feature: react-frontend-implementation
     * Property 10: For any prompt form submission, if the title or content
     * field is empty or contains only whitespace, the form SHALL prevent
     * submission and display a validation error.
     */
    fc.assert(
      fc.property(
        fc.string().filter(s => s.trim() === ''), // Whitespace-only strings
        fc.string().filter(s => s.trim().length > 0), // Valid content
        (title, content) => {
          const result = validatePromptForm({ title, content });
          return result.errors.title !== undefined;
        }
      ),
      { numRuns: 100 }
    );
  });

  it('Property 10: rejects forms with empty or whitespace-only content', () => {
    /**
     * Feature: react-frontend-implementation
     * Property 10: For any prompt form submission, if the title or content
     * field is empty or contains only whitespace, the form SHALL prevent
     * submission and display a validation error.
     */
    fc.assert(
      fc.property(
        fc.string().filter(s => s.trim().length > 0), // Valid title
        fc.string().filter(s => s.trim() === ''), // Whitespace-only strings
        (title, content) => {
          const result = validatePromptForm({ title, content });
          return result.errors.content !== undefined;
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

**API Client Property**:
```javascript
import { describe, it } from 'vitest';
import fc from 'fast-check';
import apiClient from './client';

describe('API Client Properties', () => {
  it('Property 1: includes Content-Type header in all requests', () => {
    /**
     * Feature: react-frontend-implementation
     * Property 1: For any HTTP request made by the API client, the request
     * SHALL include the Content-Type header set to "application/json".
     */
    fc.assert(
      fc.property(
        fc.constantFrom('GET', 'POST', 'PUT', 'DELETE'),
        fc.webPath(),
        (method, path) => {
          const request = apiClient.defaults;
          return request.headers['Content-Type'] === 'application/json';
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

**Debounce Property**:
```javascript
import { describe, it } from 'vitest';
import fc from 'fast-check';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce Properties', () => {
  it('Property 20: delays value updates by at least 300ms', async () => {
    /**
     * Feature: react-frontend-implementation
     * Property 20: For any sequence of search input changes, API requests
     * SHALL only be triggered after the input has been stable for at least 300ms.
     */
    fc.assert(
      fc.asyncProperty(
        fc.array(fc.string(), { minLength: 2, maxLength: 10 }),
        async (values) => {
          const { result, rerender } = renderHook(
            ({ value }) => useDebounce(value, 300),
            { initialProps: { value: values[0] } }
          );

          // Rapidly change values
          for (let i = 1; i < values.length; i++) {
            rerender({ value: values[i] });
          }

          // Immediately after changes, debounced value should still be initial
          const immediateValue = result.current;

          // After 300ms, should have latest value
          await waitFor(() => {
            expect(result.current).toBe(values[values.length - 1]);
          }, { timeout: 400 });

          return immediateValue === values[0];
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### Test Coverage Goals

- **Unit Test Coverage**: Minimum 80% code coverage
- **Property Test Coverage**: All 36 correctness properties implemented
- **Integration Test Coverage**: All critical user flows (create, edit, delete prompts)
- **Accessibility Testing**: Automated accessibility checks using jest-axe

### Continuous Integration

Tests should run automatically on:
- Every commit (pre-commit hook)
- Every pull request (CI pipeline)
- Before deployment (pre-deployment check)

```json
// package.json scripts
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:properties": "vitest run --grep 'Property'",
    "test:ui": "vitest --ui"
  }
}
```

### Testing Best Practices

1. **Test User Behavior, Not Implementation**: Use React Testing Library's user-centric queries
2. **Mock External Dependencies**: Use MSW for API mocking, avoid mocking internal modules
3. **Test Accessibility**: Include accessibility checks in component tests
4. **Property Test Generators**: Create reusable generators for common data types (prompts, collections)
5. **Descriptive Test Names**: Use "should" or "when/then" format for clarity
6. **Arrange-Act-Assert**: Structure tests clearly with setup, action, and verification phases
