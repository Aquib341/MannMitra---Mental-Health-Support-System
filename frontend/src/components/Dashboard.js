// frontend/src/components/Dashboard.js
import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  };

  const features = [
    {
      title: 'Chat with AI',
      description: 'Talk to our empathetic AI assistant',
      path: '/chat',
      icon: '💬'
    },
    {
      title: 'Mood Detection',
      description: 'Detect your emotions using your webcam',
      path: '/emotion',
      icon: '😊'
    },
    {
      title: 'Music Therapy',
      description: 'Get music recommendations based on your mood',
      path: '/music',
      icon: '🎵'
    },
    {
      title: 'Community Chat',
      description: 'Join anonymous support groups',
      path: '/community',
      icon: '👥'
    },
    {
      title: 'Mood Tracker',
      description: 'Track your emotional journey over time',
      path: '/mood',
      icon: '📊'
    },
    {
      title: 'Emergency Contacts',
      description: 'Manage your emergency support network',
      path: '/emergency',
      icon: '🆘'
    }
  ];

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Welcome to MannMitra, {currentUser?.displayName || 'User'}!</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>

      <div className="dashboard-content">
        <div className="features-grid">
          {features.map((feature, index) => (
            <div 
              key={index} 
              className="feature-card"
              onClick={() => navigate(feature.path)}
            >
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="quick-stats">
          <h2>Your Mental Health Journey</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>7</h3>
              <p>Days tracked</p>
            </div>
            <div className="stat-card">
              <h3>24</h3>
              <p>Chat sessions</p>
            </div>
            <div className="stat-card">
              <h3>85%</h3>
              <p>Positive days</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;