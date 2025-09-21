# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import base64
import cv2
import numpy as np
from datetime import datetime, timedelta
import uuid
import io
import os
import tempfile

# Import modules
from emotion_detection_simple import EmotionDetector
from chatbot import ChatAssistant
from mood_analysis import MoodAnalyzer
from music_recommendation import MusicRecommender
from anonymous_chat import ChatManager
from emergency import EmergencySystem
from database import DatabaseManager
from voice_processing import VoiceProcessor
from auth import AuthManager

app = FastAPI(title="MannMitra API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
emotion_detector = EmotionDetector()
chat_assistant = ChatAssistant()
mood_analyzer = MoodAnalyzer()
music_recommender = MusicRecommender()
chat_manager = ChatManager()
emergency_system = EmergencySystem()
voice_processor = VoiceProcessor()
db = DatabaseManager()
auth_manager = AuthManager()

# Mount static files for serving frontend
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
app.mount("/assets", StaticFiles(directory="frontend/build/assets"), name="assets")

# Serve React frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/build/index.html")

# Authentication endpoints
@app.post("/auth/register")
async def register_user(user_data: dict):
    try:
        user = auth_manager.register_user(
            user_data.get("email"),
            user_data.get("password"),
            user_data.get("name", ""),
            user_data.get("photo_url", "")
        )
        return JSONResponse(content={"user": user, "message": "User registered successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
async def login_user(credentials: dict):
    try:
        user = auth_manager.login_user(
            credentials.get("email"),
            credentials.get("password")
        )
        return JSONResponse(content={"user": user, "message": "Login successful"})
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/auth/logout")
async def logout_user(user_data: dict):
    try:
        auth_manager.logout_user(user_data.get("user_id"))
        return JSONResponse(content={"message": "Logout successful"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# WebSocket for real-time emotion detection
@app.websocket("/ws/emotion")
async def websocket_emotion(websocket: WebSocket):
    await websocket.accept()
    user_id = "anonymous"
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            
            if 'user_id' in data:
                user_id = data['user_id']
            
            if 'image' in data:
                # Process image for emotion detection
                image_data = data['image'].split(',')[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Detect emotion
                emotion, confidence = emotion_detector.detect_emotion(frame)
                
                # Store emotion data
                db.store_emotion_data(user_id, emotion, confidence)
                
                # Send back emotion data
                await websocket.send_json({
                    "emotion": emotion,
                    "confidence": float(confidence),
                    "timestamp": datetime.now().isoformat()
                })
                
                # Check for crisis situation
                if emotion in ['sad', 'angry', 'fear'] and confidence > 0.7:
                    crisis_level = emergency_system.assess_crisis(user_id, emotion, confidence)
                    if crisis_level > 0.8:
                        await websocket.send_json({
                            "alert": "crisis_detected",
                            "message": "We've detected you might need help. Would you like to talk to someone?",
                            "level": crisis_level
                        })
    except WebSocketDisconnect:
        print("Client disconnected from emotion detection")
    except Exception as e:
        print(f"Error in emotion detection: {e}")

# Chat endpoints
@app.post("/chat")
async def chat_endpoint(message: dict):
    user_id = message.get("user_id", "anonymous")
    user_message = message.get("message", "")
    voice_data = message.get("voice", None)
    
    # Process voice if provided
    if voice_data:
        user_message = voice_processor.speech_to_text(voice_data)
    
    # Get AI response
    response = chat_assistant.get_response(user_message, user_id)
    
    # Analyze mood from text
    mood = mood_analyzer.analyze_text(user_message)
    
    # Store conversation
    db.store_conversation(user_id, user_message, response, mood)
    
    # Convert to speech if requested
    speech_data = None
    if message.get("voice_response", False):
        speech_data = voice_processor.text_to_speech(response)
    
    return JSONResponse(content={
        "response": response,
        "mood": mood,
        "speech_data": speech_data,
        "user_message": user_message
    })

# Music recommendation endpoint
@app.get("/music/{mood}")
async def get_music(mood: str, user_id: str = None):
    playlists = music_recommender.get_playlists(mood, user_id)
    return JSONResponse(content={"playlists": playlists})

# Anonymous chat endpoints
@app.post("/chat/join")
async def join_chat_room(user_id: str):
    room_id = chat_manager.join_chat(user_id)
    return JSONResponse(content={"room_id": room_id})

@app.websocket("/ws/chat/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await websocket.accept()
    user_id = "anonymous"
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_id = message_data.get("user_id", user_id)
            message_text = message_data.get("message", "")
            
            # Store message in database
            db.store_anonymous_message(room_id, user_id, message_text)
            
            # Broadcast to all users in room
            await chat_manager.broadcast_message(room_id, {
                "user_id": user_id,
                "message": message_text,
                "timestamp": datetime.now().isoformat(),
                "type": "message"
            })
    except WebSocketDisconnect:
        chat_manager.leave_chat(room_id, user_id)
    except Exception as e:
        print(f"Error in chat: {e}")

# Emergency contact endpoint
@app.post("/emergency/contacts")
async def add_emergency_contact(contact: dict):
    user_id = contact.get("user_id")
    contact_info = contact.get("contact_info")
    success = db.add_emergency_contact(user_id, contact_info)
    if success:
        return JSONResponse(content={"status": "contact_added"})
    else:
        raise HTTPException(status_code=400, detail="Failed to add emergency contact")

@app.get("/emergency/contacts/{user_id}")
async def get_emergency_contacts(user_id: str):
    contacts = db.get_emergency_contacts(user_id)
    return JSONResponse(content={"contacts": contacts})

@app.post("/emergency/alert")
async def send_emergency_alert(alert: dict):
    user_id = alert.get("user_id")
    message = alert.get("message", "I need help")
    emergency_system.send_alert(user_id, message)
    return JSONResponse(content={"status": "alert_sent"})

# Mood tracking endpoints
@app.get("/mood/history/{user_id}")
async def get_mood_history(user_id: str, days: int = 30):
    history = db.get_mood_history(user_id, days)
    analysis = mood_analyzer.analyze_trends(history)
    return JSONResponse(content={"history": history, "analysis": analysis})

# Voice processing endpoints
@app.post("/voice/process")
async def process_voice(voice_data: dict):
    user_id = voice_data.get("user_id", "anonymous")
    audio_data = voice_data.get("audio")
    
    text = voice_processor.speech_to_text(audio_data)
    mood = mood_analyzer.analyze_text(text)
    
    return JSONResponse(content={"text": text, "mood": mood})

@app.post("/voice/synthesize")
async def synthesize_voice(text: str = Form(...)):
    audio_data = voice_processor.text_to_speech(text)
    if audio_data:
        return StreamingResponse(io.BytesIO(base64.b64decode(audio_data)), media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=400, detail="Failed to synthesize speech")

# Meditation and exercises endpoints
@app.get("/meditation/{type}")
async def get_meditation_guide(type: str):
    guides = {
        "breathing": {
            "title": "Deep Breathing Exercise",
            "description": "A simple breathing exercise to reduce stress and anxiety",
            "steps": [
                "Find a comfortable seated position",
                "Close your eyes and take a deep breath in for 4 seconds",
                "Hold your breath for 4 seconds",
                "Exhale slowly for 6 seconds",
                "Repeat for 5-10 cycles"
            ],
            "duration": 300  # 5 minutes
        },
        "mindfulness": {
            "title": "5-Minute Mindfulness Meditation",
            "description": "A short mindfulness practice to center yourself",
            "steps": [
                "Sit comfortably with your eyes closed",
                "Focus on your breath without trying to change it",
                "Notice thoughts as they arise without judgment",
                "Gently return focus to your breath",
                "Expand awareness to sounds and sensations around you"
            ],
            "duration": 300
        }
    }
    
    guide = guides.get(type, guides["breathing"])
    return JSONResponse(content=guide)

@app.get("/exercises")
async def get_all_exercises():
    exercises = [
        {
            "id": "breathing",
            "name": "Deep Breathing",
            "description": "Calm your nervous system with controlled breathing",
            "duration": 5,
            "category": "relaxation"
        },
        {
            "id": "mindfulness",
            "name": "Mindfulness Meditation",
            "description": "Practice being present in the moment",
            "duration": 10,
            "category": "meditation"
        },
        {
            "id": "progressive",
            "name": "Progressive Muscle Relaxation",
            "description": "Release tension throughout your body",
            "duration": 15,
            "category": "relaxation"
        }
    ]
    return JSONResponse(content={"exercises": exercises})

# Therapist matching endpoint
@app.get("/therapists/{user_id}")
async def get_therapist_recommendations(user_id: str):
    # This would typically integrate with a therapist database API
    # For now, return mock data
    therapists = [
        {
            "id": "1",
            "name": "Dr. Sarah Johnson",
            "specialty": "Cognitive Behavioral Therapy",
            "experience": "8 years",
            "languages": ["English", "Spanish"],
            "availability": ["Mon", "Wed", "Fri"],
            "rating": 4.8,
            "photo": "/assets/therapists/therapist1.jpg"
        },
        {
            "id": "2",
            "name": "Dr. Michael Chen",
            "specialty": "Mindfulness-Based Stress Reduction",
            "experience": "12 years",
            "languages": ["English", "Mandarin"],
            "availability": ["Tue", "Thu", "Sat"],
            "rating": 4.9,
            "photo": "/assets/therapists/therapist2.jpg"
        }
    ]
    
    # In a real implementation, we would match based on user preferences and needs
    user_profile = db.get_user_profile(user_id)
    
    return JSONResponse(content={"therapists": therapists})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)