# backend/emotion_detection.py
import cv2
import numpy as np
from deepface import DeepFace
import mediapipe as mp

class EmotionDetector:
    def __init__(self):
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
    
    def detect_emotion(self, frame):
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get face landmarks for additional analysis
            landmarks_result = self.face_mesh.process(rgb_frame)
            
            # Analyze emotion with DeepFace
            analysis = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)
            
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            emotion = analysis['dominant_emotion']
            confidence = analysis['emotion'][emotion]
            
            # Enhance with facial landmarks if available
            if landmarks_result.multi_face_landmarks:
                confidence = self.enhance_with_landmarks(landmarks_result, emotion, confidence)
            
            return emotion, confidence
        except Exception as e:
            print(f"Emotion detection error: {e}")
            return "neutral", 0.5
    
    def enhance_with_landmarks(self, landmarks_result, emotion, confidence):
        # Analyze facial landmarks to refine emotion detection
        try:
            face_landmarks = landmarks_result.multi_face_landmarks[0]
            
            # Calculate eye openness
            left_eye_landmarks = [33, 160, 158, 133, 153, 144]
            right_eye_landmarks = [362, 385, 387, 263, 373, 380]
            
            # Calculate mouth openness
            mouth_landmarks = [61, 84, 17, 314, 405, 320, 375, 291]
            
            # If eyes are very open, increase surprise confidence
            # If eyes are squinted, increase happy confidence
            # This would need proper implementation
            
            return min(confidence * 1.1, 1.0)  # Slight confidence boost
        except:
            return confidence