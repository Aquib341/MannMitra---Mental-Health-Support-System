# backend/music_recommendation.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class MusicRecommender:
    def __init__(self):
        # Initialize Spotify client
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if client_id and client_secret:
            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            self.spotify_available = True
        else:
            self.spotify_available = False
            print("Spotify credentials not found. Using mock recommendations.")
        
        # Mood to genre mapping
        self.mood_genres = {
            'happy': ['pop', 'dance', 'electronic', 'happy'],
            'sad': ['sad', 'acoustic', 'piano', 'singer-songwriter'],
            'anxious': ['ambient', 'classical', 'meditation', 'chill'],
            'stressed': ['ambient', 'jazz', 'lo-fi', 'meditation'],
            'angry': ['rock', 'metal', 'punk', 'workout'],
            'neutral': ['indie', 'alternative', 'pop', 'chill'],
            'crisis': ['calm', 'meditation', 'ambient', 'classical']
        }
    
    def get_playlists(self, mood, user_id=None):
        """Get playlists based on mood"""
        if not self.spotify_available:
            return self.get_default_playlists(mood)
        
        genres = self.mood_genres.get(mood, ['pop'])
        
        try:
            # Search for playlists based on mood and genres
            playlists = []
            
            for genre in genres:
                results = self.sp.search(q=f'mood:{mood} {genre}', type='playlist', limit=5)
                for item in results['playlists']['items']:
                    playlists.append({
                        'name': item['name'],
                        'description': item['description'],
                        'image': item['images'][0]['url'] if item['images'] else None,
                        'url': item['external_urls']['spotify'],
                        'tracks': item['tracks']['total']
                    })
            
            # If no mood-specific playlists found, search by genre
            if not playlists:
                for genre in genres:
                    results = self.sp.search(q=genre, type='playlist', limit=5)
                    for item in results['playlists']['items']:
                        playlists.append({
                            'name': item['name'],
                            'description': item['description'],
                            'image': item['images'][0]['url'] if item['images'] else None,
                            'url': item['external_urls']['spotify'],
                            'tracks': item['tracks']['total']
                        })
            
            return playlists[:10]  # Return top 10 playlists
        
        except Exception as e:
            print(f"Spotify API error: {e}")
            # Return default playlists
            return self.get_default_playlists(mood)
    
    def get_default_playlists(self, mood):
        """Fallback playlists if API fails"""
        defaults = {
            'happy': [
                {
                    'name': 'Happy Hits!',
                    'description': 'Feel-good music to boost your mood',
                    'image': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC',
                    'tracks': 50
                }
            ],
            'sad': [
                {
                    'name': 'Sad Songs',
                    'description': 'Songs for when you need to feel understood',
                    'image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3YSRoSdA634',
                    'tracks': 50
                }
            ],
            'anxious': [
                {
                    'name': 'Calm Mind',
                    'description': 'Peaceful music to ease anxiety',
                    'image': 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=300',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX4UmVJ9sdNEs',
                    'tracks': 50
                }
            ],
            'stressed': [
                {
                    'name': 'Stress Relief',
                    'description': 'Music to help you relax and decompress',
                    'image': 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=300',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj',
                    'tracks': 50
                }
            ],
            'angry': [
                {
                    'name': 'Anger Management',
                    'description': 'Channel your anger through powerful music',
                    'image': 'https://images.unsplash.com/photo-1494232410401-ad00d5433cfa?w=300',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX5IDTimEWoTd',
                    'tracks': 50
                }
            ],
            'crisis': [
                {
                    'name': 'Crisis Support',
                    'description': 'Calming music for difficult moments',
                    'image': 'https://images.unsplash.com/photo-1511735111819-9a3f7709049c?w=300',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR',
                    'tracks': 50
                }
            ]
        }
        
        return defaults.get(mood, defaults['neutral'])