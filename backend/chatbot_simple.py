import random
import time

class ChatAssistant:
    def __init__(self):
        self.responses = {
            "hello": ["Hello! How can I help you today?", "Hi there! What's on your mind?", "Hello! How are you feeling?"],
            "sad": ["I'm sorry you're feeling sad. Would you like to talk about it?", "It's okay to feel sad sometimes. I'm here to listen.", "Let's try to find something that might cheer you up!"],
            "happy": ["That's wonderful to hear! 😊", "I'm glad you're feeling happy!", "Great! Let's keep this positive energy going!"],
            "anxious": ["Take a deep breath. I'm here with you.", "Anxiety can be tough. Would you like to try some breathing exercises?", "Let's break this down together. What's specifically worrying you?"],
            "stress": ["Stress can be overwhelming. Remember to take breaks.", "Let's think about what might help reduce your stress.", "Have you tried any relaxation techniques?"],
            "default": ["I'm here to listen. Tell me more.", "That's interesting. Could you elaborate?", "How does that make you feel?"]
        }
    
    def get_response(self, message):
        """Simple response system without external APIs"""
        message = message.lower()
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Check for keywords
        if any(word in message for word in ["hello", "hi", "hey"]):
            return random.choice(self.responses["hello"])
        elif any(word in message for word in ["sad", "depressed", "unhappy"]):
            return random.choice(self.responses["sad"])
        elif any(word in message for word in ["happy", "good", "great", "awesome"]):
            return random.choice(self.responses["happy"])
        elif any(word in message for word in ["anxious", "nervous", "worried"]):
            return random.choice(self.responses["anxious"])
        elif any(word in message for word in ["stress", "stressed", "overwhelmed"]):
            return random.choice(self.responses["stress"])
        else:
            return random.choice(self.responses["default"])