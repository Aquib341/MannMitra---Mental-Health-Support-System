// src/components/EmotionDetector.js
import React, { useState } from 'react';
import './EmotionDetector.css';

function EmotionDetector() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [emotion, setEmotion] = useState('');
  const [confidence, setConfidence] = useState(0);

  const startDetection = () => {
    setIsDetecting(true);
    // Simulate emotion detection for now
    const emotions = ['happy', 'sad', 'neutral', 'angry', 'surprise'];
    const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
    const randomConfidence = (Math.random() * 0.5 + 0.5).toFixed(2); // 0.5 to 1.0
    
    setTimeout(() => {
      setEmotion(randomEmotion);
      setConfidence(randomConfidence);
    }, 2000);
  };

  const stopDetection = () => {
    setIsDetecting(false);
    setEmotion('');
    setConfidence(0);
  };

  return (
    <div className="emotion-detector-container">
      <div className="detector-header">
        <h2>Mood Detection</h2>
        <p>Let me understand how you're feeling through facial expressions</p>
      </div>

      <div className="detection-area">
        <div className="video-container">
          <div className="video-placeholder">
            {isDetecting ? '🎥 Camera Active' : '📷 Camera Off'}
          </div>
        </div>

        <div className="controls">
          <button
            onClick={isDetecting ? stopDetection : startDetection}
            className={`detect-btn ${isDetecting ? 'stop' : 'start'}`}
          >
            {isDetecting ? 'Stop Detection' : 'Start Detection'}
          </button>
        </div>

        {(emotion || confidence > 0) && (
          <div className="results">
            <h3>Detection Results</h3>
            <div className="result-card">
              <span className="emotion">{emotion}</span>
              <span className="confidence">
                Confidence: {(confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default EmotionDetector;