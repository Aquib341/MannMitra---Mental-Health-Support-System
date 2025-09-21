# backend/auth.py
import firebase_admin
from firebase_admin import auth, credentials
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AuthManager:
    def __init__(self):
        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:
            firebase_config = os.getenv("FIREBASE_SERVICE_ACCOUNT")
            if firebase_config:
                cred_dict = json.loads(firebase_config)
                cred = credentials.Certificate(cred_dict)
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
    
    def register_user(self, email, password, name, photo_url):
        try:
            # Create user in Firebase Auth
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name,
                photo_url=photo_url
            )
            
            # Create custom token for the user
            custom_token = auth.create_custom_token(user.uid)
            
            return {
                "uid": user.uid,
                "email": user.email,
                "name": name,
                "photo_url": photo_url,
                "custom_token": custom_token
            }
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")
    
    def login_user(self, email, password):
        # In a real implementation, this would verify credentials
        # For Firebase, you'd typically use the client SDK for authentication
        # This is a simplified version
        try:
            # Get user by email
            user = auth.get_user_by_email(email)
            
            # In a real app, you would verify the password against Firebase Auth
            # This is a placeholder implementation
            
            # Create custom token
            custom_token = auth.create_custom_token(user.uid)
            
            return {
                "uid": user.uid,
                "email": user.email,
                "name": user.display_name,
                "photo_url": user.photo_url,
                "custom_token": custom_token
            }
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")
    
    def logout_user(self, user_id):
        # Firebase handles logout on the client side
        # This method would typically invalidate tokens on the server
        return True
    
    def verify_token(self, token):
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except:
            return None