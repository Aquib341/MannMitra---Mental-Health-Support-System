// frontend/src/firebase.js
// Check what's available in the firebase package
import { initializeApp } from 'firebase/app';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "mock-api-key",
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "mock-auth-domain",
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "mock-project-id",
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "mock-storage-bucket",
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "mock-sender-id",
  appId: process.env.REACT_APP_FIREBASE_APP_ID || "mock-app-id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export default app;