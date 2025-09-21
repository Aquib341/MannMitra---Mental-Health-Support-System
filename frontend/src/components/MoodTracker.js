// src/components/MoodTracker.js
import React, { useState } from 'react';
import './MoodTracker.css';

function MoodTracker() {
  const [moodData] = useState([
    { day: 'Mon', mood: 'happy' },
    { day: 'Tue', mood: 'neutral' },
    { day: 'Wed', mood: 'sad' },
    { day: 'Thu', mood: 'happy' },
    { day: 'Fri', mood: 'angry' },
    { day: 'Sat', mood: 'happy' },
    { day: 'Sun', mood: 'neutral' }
  ]);

  const getMoodColor = (mood) => {
    const colors = {
      happy: '#4caf50',
      sad: '#2196f3',
      angry: '#f44336',
      neutral: '#ffeb3b',
      surprise: '#9c27b0'
    };
    return colors[mood] || '#666';
  };

  return (
    <div className="mood-tracker-container">
      <h2>Mood Tracker</h2>
      <p>Your emotional journey this week</p>
      
      <div className="mood-chart">
        <div className="chart-title">Weekly Mood Summary</div>
        <div className="chart-bars">
          {moodData.map((entry, index) => (
            <div key={index} className="chart-bar-container">
              <div className="chart-bar">
                <div 
                  className="bar-fill"
                  style={{
                    height: '60px',
                    backgroundColor: getMoodColor(entry.mood)
                  }}
                >
                  <span className="mood-emoji">
                    {entry.mood === 'happy' ? '😊' : 
                     entry.mood === 'sad' ? '😢' : 
                     entry.mood === 'angry' ? '😠' : 
                     entry.mood === 'surprise' ? '😲' : '😐'}
                  </span>
                </div>
              </div>
              <div className="bar-label">{entry.day}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="mood-history">
        <h3>Recent Mood Entries</h3>
        <div className="mood-list">
          {moodData.map((entry, index) => (
            <div key={index} className="mood-item">
              <span className="mood-emoji">
                {entry.mood === 'happy' ? '😊' : 
                 entry.mood === 'sad' ? '😢' : 
                 entry.mood === 'angry' ? '😠' : 
                 entry.mood === 'surprise' ? '😲' : '😐'}
              </span>
              <span className="mood-text">{entry.mood}</span>
              <span className="mood-day">{entry.day}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default MoodTracker;