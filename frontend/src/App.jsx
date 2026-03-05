import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import PromptsPage from './pages/PromptsPage';
import PromptDetailPage from './pages/PromptDetailPage';
import CollectionsPage from './pages/CollectionsPage';
import './App.css';

function NotFoundPage() {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/prompts" replace />} />
          <Route path="/prompts" element={<PromptsPage />} />
          <Route path="/prompts/:id" element={<PromptDetailPage />} />
          <Route path="/collections" element={<CollectionsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
