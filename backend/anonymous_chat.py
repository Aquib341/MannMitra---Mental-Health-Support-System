# backend/anonymous_chat.py
import asyncio
from collections import defaultdict
from typing import Dict, List
import uuid

class ChatManager:
    def __init__(self):
        self.active_rooms: Dict[str, List] = defaultdict(list)
        self.user_rooms: Dict[str, str] = {}
    
    def join_chat(self, user_id: str):
        """Join a chat room - either existing or new"""
        # Check if user is already in a room
        if user_id in self.user_rooms:
            return self.user_rooms[user_id]
        
        # Find a suitable room or create new one
        room_id = None
        for rid, users in self.active_rooms.items():
            if len(users) < 5:  # Room size limit
                room_id = rid
                break
        
        if not room_id:
            room_id = str(uuid.uuid4())
        
        # Add user to room
        self.active_rooms[room_id].append(user_id)
        self.user_rooms[user_id] = room_id
        
        return room_id
    
    def leave_chat(self, room_id: str, user_id: str):
        """Remove user from chat room"""
        if room_id in self.active_rooms and user_id in self.active_rooms[room_id]:
            self.active_rooms[room_id].remove(user_id)
        
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]
        
        # Clean up empty rooms
        if room_id in self.active_rooms and not self.active_rooms[room_id]:
            del self.active_rooms[room_id]
    
    async def broadcast_message(self, room_id: str, message_data: dict, sender_websocket):
        """Broadcast message to all users in room"""
        if room_id not in self.active_rooms:
            return
        
        # Prepare message for broadcasting
        broadcast_message = {
            "type": "message",
            "user_id": "anonymous",  # Anonymize user ID
            "message": message_data.get("message", ""),
            "timestamp": message_data.get("timestamp", "")
        }
        
        # In a real implementation, you would store connections
        # and broadcast to all users in the room
        # This is a simplified version
        
        # For now, just echo back to sender
        await sender_websocket.send_json(broadcast_message)