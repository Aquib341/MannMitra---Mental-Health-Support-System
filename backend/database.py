# backend/database.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # Initialize Firebase
        if not firebase_admin._apps:
            firebase_config = os.getenv("FIREBASE_SERVICE_ACCOUNT")
            if firebase_config:
                cred_dict = json.loads(firebase_config)
                cred = credentials.Certificate(cred_dict)
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    def store_emotion_data(self, user_id, emotion, confidence):
        """Store emotion detection data"""
        try:
            doc_ref = self.db.collection('users').document(user_id).collection('mood_data').document()
            doc_ref.set({
                'emotion': emotion,
                'confidence': confidence,
                'timestamp': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error storing emotion data: {e}")
            return False
    
    def store_conversation(self, user_id, user_message, ai_response, mood=None):
        """Store conversation history"""
        try:
            doc_ref = self.db.collection('users').document(user_id).collection('conversations').document()
            doc_ref.set({
                'user_message': user_message,
                'ai_response': ai_response,
                'mood': mood,
                'timestamp': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error storing conversation: {e}")
            return False
    
    def store_anonymous_message(self, room_id, user_id, message):
        """Store anonymous chat message"""
        try:
            doc_ref = self.db.collection('chat_rooms').document(room_id).collection('messages').document()
            doc_ref.set({
                'user_id': user_id,
                'message': message,
                'timestamp': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error storing anonymous message: {e}")
            return False
    
    def get_mood_history(self, user_id, days=30):
        """Get mood history for a user"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            docs = self.db.collection('users').document(user_id).collection('mood_data') \
                .where('timestamp', '>=', start_date) \
                .order_by('timestamp') \
                .stream()
            
            mood_data = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                mood_data.append(data)
            
            return mood_data
        except Exception as e:
            print(f"Error getting mood history: {e}")
            return []
    
    def add_emergency_contact(self, user_id, contact_info):
        """Add emergency contact for a user"""
        try:
            doc_ref = self.db.collection('users').document(user_id).collection('emergency_contacts').document()
            doc_ref.set({
                'name': contact_info.get('name'),
                'phone': contact_info.get('phone'),
                'email': contact_info.get('email'),
                'relationship': contact_info.get('relationship'),
                'added_date': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error adding emergency contact: {e}")
            return False
    
    def get_emergency_contacts(self, user_id):
        """Get emergency contacts for a user"""
        try:
            docs = self.db.collection('users').document(user_id).collection('emergency_contacts').stream()
            
            contacts = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                contacts.append(data)
            
            return contacts
        except Exception as e:
            print(f"Error getting emergency contacts: {e}")
            return []
    
    def get_user_profile(self, user_id):
        """Get user profile"""
        try:
            doc = self.db.collection('users').document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def update_user_profile(self, user_id, profile_data):
        """Update user profile"""
        try:
            self.db.collection('users').document(user_id).set(profile_data, merge=True)
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def get_chat_rooms(self):
        """Get all chat rooms"""
        try:
            docs = self.db.collection('chat_rooms').stream()
            
            rooms = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                rooms.append(data)
            
            return rooms
        except Exception as e:
            print(f"Error getting chat rooms: {e}")
            return []
    
    def get_chat_messages(self, room_id, limit=50):
        """Get messages from a chat room"""
        try:
            docs = self.db.collection('chat_rooms').document(room_id).collection('messages') \
                .order_by('timestamp', direction=firestore.Query.DESCENDING) \
                .limit(limit) \
                .stream()
            
            messages = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                messages.append(data)
            
            return messages[::-1]  # Reverse to show oldest first
        except Exception as e:
            print(f"Error getting chat messages: {e}")
            return []