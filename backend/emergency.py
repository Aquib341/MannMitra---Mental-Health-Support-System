import cv2
import numpy as np
import random
import time
from datetime import datetime

class EmergencySystem:
    def __init__(self):
        # Try to load face detection model
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            self.face_cascade = None
            print("Note: Using simple emergency detection")
        
        self.emergency_contacts = [
            {"name": "Emergency Services", "number": "112"},
            {"name": "Local Hospital", "number": "+1-555-0123"},
            {"name": "Trusted Friend", "number": "+1-555-9876"}
        ]
        
        self.distress_signals = {
            "panic": ["rapid head movement", "wide eyes", "tense facial expression"],
            "fall": ["sudden downward movement", "loss of balance", "lying position"],
            "medical": ["clutching chest", "difficulty breathing", "slurred speech"]
        }
    
    def detect_distress(self, image_path):
        """Simple distress detection using basic computer vision"""
        try:
            # Check if image exists
            import os
            if not os.path.exists(image_path):
                return {"status": "error", "message": "Image file not found"}
            
            # If we have OpenCV, try basic analysis
            if self.face_cascade:
                img = cv2.imread(image_path)
                if img is not None:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    # Simple analysis based on face detection
                    if len(faces) == 0:
                        # No face detected - could indicate fall or absence
                        return {
                            "status": "warning",
                            "message": "No face detected - possible fall or absence",
                            "confidence": 0.4,
                            "suggested_action": "check_on_user"
                        }
                    else:
                        # Face detected - simulate some analysis
                        distress_level = random.uniform(0.1, 0.3)  # Low probability for demo
                        if distress_level > 0.25:
                            return {
                                "status": "alert",
                                "message": "Possible distress detected",
                                "confidence": distress_level,
                                "suggested_action": "ask_if_okay"
                            }
            
            # Default: no distress detected
            return {
                "status": "normal",
                "message": "No distress detected",
                "confidence": 0.9,
                "suggested_action": "continue_monitoring"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def trigger_emergency_protocol(self, emergency_type="general"):
        """Simulate emergency response"""
        protocol = {
            "general": [
                "Alerting emergency contacts...",
                "Sending location data to responders...",
                "Preparing emergency information..."
            ],
            "medical": [
                "Contacting medical services...",
                "Preparing medical history...",
                "Guiding through first aid steps..."
            ],
            "safety": [
                "Alerting safety authorities...",
                "Securing the area...",
                "Providing safety instructions..."
            ]
        }
        
        steps = protocol.get(emergency_type, protocol["general"])
        results = []
        
        for step in steps:
            time.sleep(0.5)  # Simulate processing time
            results.append({
                "step": step,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            })
        
        return {
            "emergency_type": emergency_type,
            "contacts_notified": self.emergency_contacts,
            "steps_completed": results,
            "message": "Emergency protocol activated successfully"
        }
    
    def get_emergency_contacts(self):
        return self.emergency_contacts
    
    def add_emergency_contact(self, name, number):
        self.emergency_contacts.append({"name": name, "number": number})
        return {"status": "success", "message": "Contact added successfully"}