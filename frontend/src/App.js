// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import EmotionDetector from './components/EmotionDetector';
import MusicPlayer from './components/MusicPlayer';
import AnonymousChat from './components/AnonymousChat';
import MoodTracker from './components/MoodTracker';
import EmergencyContacts from './components/EmergencyContacts';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/chat" element={<ProtectedRoute><ChatInterface /></ProtectedRoute>} />
            <Route path="/emotion" element={<ProtectedRoute><EmotionDetector /></ProtectedRoute>} />
            <Route path="/music" element={<ProtectedRoute><MusicPlayer /></ProtectedRoute>} />
            <Route path="/community" element={<ProtectedRoute><AnonymousChat /></ProtectedRoute>} />
            <Route path="/mood" element={<ProtectedRoute><MoodTracker /></ProtectedRoute>} />
            <Route path="/emergency" element={<ProtectedRoute><EmergencyContacts /></ProtectedRoute>} />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

// Protected route component
function ProtectedRoute({ children }) {
  const { currentUser } = useAuth();
  return currentUser ? children : <Navigate to="/login" />;
}

export default App;