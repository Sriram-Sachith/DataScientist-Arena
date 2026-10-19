import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import { Dashboard } from './components/Dashboard';
import { DatasetUpload } from './components/DatasetUpload';
import { DataExplorer } from './components/DataExplorer';
import { AnalysisConfig } from './components/AnalysisConfig';
import { AILab } from './components/AILab';
import { RunMonitor } from './components/RunMonitor';
import { VerificationCenter } from './components/VerificationCenter';
import { Results } from './components/Results';
import { Login } from './pages/Login';
import { AppProvider } from './context/AppContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import './styles/globals.css';

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin text-4xl mb-4">⏳</div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

function AppContent() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      {!isAuthenticated ? (
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      ) : (
        <MainLayout>
          <Routes>
            <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/dataset-upload" element={<ProtectedRoute><DatasetUpload /></ProtectedRoute>} />
            <Route path="/data-explorer" element={<ProtectedRoute><DataExplorer /></ProtectedRoute>} />
            <Route path="/data-explorer/:id" element={<ProtectedRoute><DataExplorer /></ProtectedRoute>} />
            <Route path="/analysis-config" element={<ProtectedRoute><AnalysisConfig /></ProtectedRoute>} />
            <Route path="/ai-lab" element={<ProtectedRoute><AILab /></ProtectedRoute>} />
            <Route path="/run-monitor" element={<ProtectedRoute><RunMonitor /></ProtectedRoute>} />
            <Route path="/verification-center" element={<ProtectedRoute><VerificationCenter /></ProtectedRoute>} />
            <Route path="/results" element={<ProtectedRoute><Results /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </MainLayout>
      )}
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </AuthProvider>
  );
}

export default App;
