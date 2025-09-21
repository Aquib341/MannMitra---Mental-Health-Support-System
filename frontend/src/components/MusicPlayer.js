// frontend/src/components/MusicPlayer.js
import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './MusicPlayer.css';
const MusicPlayer = ({ user }) => {
  const [playlists, setPlaylists] = useState([]);
  const [currentMood, setCurrentMood] = useState('neutral');
  const [isLoading, setIsLoading] = useState(false);

  const moods = [
    'happy', 'sad', 'neutral', 'angry', 'anxious', 'stressed'
  ];

  const fetchMusic = async (mood) => {
    setIsLoading(true);
    try {
      const response = await apiService.getMusicRecommendations(mood, user?.uid);
      setPlaylists(response.playlists);
      setCurrentMood(mood);
    } catch (error) {
      console.error('Error fetching music:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMusic('neutral');
  }, []);

  return (
    <div className="music-player">
      <h2>Music Therapy</h2>
      
      <div className="mood-selector">
        <h3>Select your mood:</h3>
        <div className="mood-buttons">
          {moods.map(mood => (
            <button
              key={mood}
              onClick={() => fetchMusic(mood)}
              className={currentMood === mood ? 'active' : ''}
              disabled={isLoading}
            >
              {mood.charAt(0).toUpperCase() + mood.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {isLoading ? (
        <div className="loading">Loading playlists...</div>
      ) : (
        <div className="playlists">
          <h3>Playlists for {currentMood} mood</h3>
          <div className="playlist-grid">
            {playlists.map((playlist, index) => (
              <div key={index} className="playlist-card">
                {playlist.image && (
                  <img src={playlist.image} alt={playlist.name} className="playlist-image" />
                )}
                <div className="playlist-info">
                  <h4>{playlist.name}</h4>
                  <p>{playlist.description}</p>
                  <p>{playlist.tracks} tracks</p>
                  <a 
                    href={playlist.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="spotify-link"
                  >
                    Open in Spotify
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MusicPlayer;