import React from 'react';
import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './layouts/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Companies from './pages/Companies';
import CompanyDetails from './pages/CompanyDetails';
import Interviews from './pages/Interviews';
import InterviewDetails from './pages/InterviewDetails';
import SubmitInterview from './pages/SubmitInterview';
import Profile from './pages/Profile';
import AIInsights from './pages/AIInsights';
import Analytics from './pages/Analytics';
import Roadmap from './pages/Roadmap';

const FullPageState = ({ message }) => (
  <div className="flex min-h-screen items-center justify-center px-6 text-center text-sm text-slate-300">
    <div className="surface max-w-md p-8">{message}</div>
  </div>
);

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <FullPageState message="Loading StudentSphere workspace..." />;
  }

  return user ? children : <Navigate to="/login" />;
};

const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <FullPageState message="Restoring your StudentSphere session..." />;
  }

  return user ? <Navigate to="/dashboard" /> : children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route
            path="/login"
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            }
          />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="companies" element={<Companies />} />
            <Route path="companies/:id" element={<CompanyDetails />} />
            <Route path="interviews" element={<Interviews />} />
            <Route path="interviews/:id" element={<InterviewDetails />} />
            <Route path="submit-interview" element={<SubmitInterview />} />
            <Route path="profile" element={<Profile />} />
            <Route path="ai-insights" element={<AIInsights />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="roadmap" element={<Roadmap />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
