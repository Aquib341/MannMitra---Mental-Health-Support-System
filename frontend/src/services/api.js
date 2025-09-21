// frontend/src/services/api.js
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiService = {
  // Auth endpoints
  async register(userData) {
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      return await response.json();
    } catch (error) {
      return { error: 'Network error' };
    }
  },

  async login(credentials) {
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      return await response.json();
    } catch (error) {
      return { error: 'Network error' };
    }
  },

  // Chat endpoints
  async sendMessage(messageData) {
    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(messageData)
      });
      return await response.json();
    } catch (error) {
      return { error: 'Network error' };
    }
  }
};