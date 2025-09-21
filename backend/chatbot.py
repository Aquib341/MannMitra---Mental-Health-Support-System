# backend/chatbot.py
import google.generativeai as genai
from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
import os
from dotenv import load_dotenv

load_dotenv()

class ChatAssistant:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Initialize Vertex AI
        try:
            vertexai.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION"))
            self.vertex_chat_model = ChatModel.from_pretrained("chat-bison@001")
            self.use_vertex = True
        except Exception as e:
            print(f"Vertex AI initialization failed: {e}. Using Gemini only.")
            self.use_vertex = False
        
        # Define mental health context
        self.context = """
        You are MannMitra, a mental health assistant. Your role is to:
        1. Provide empathetic and supportive responses
        2. Offer practical coping strategies
        3. Identify potential crisis situations
        4. Suggest professional resources when needed
        5. Never provide medical diagnosis
        
        Always respond in a caring, non-judgmental manner.
        Keep responses concise but compassionate.
        """
        
        # Start chat session if using Vertex AI
        if self.use_vertex:
            self.chat = self.vertex_chat_model.start_chat(
                context=self.context,
                examples=[
                    InputOutputTextPair(
                        input_text="I'm feeling really sad today",
                        output_text="I'm sorry you're feeling this way. It's okay to feel sad sometimes. Would you like to talk about what's bothering you?"
                    ),
                    InputOutputTextPair(
                        input_text="I'm so stressed with work",
                        output_text="Work stress can be overwhelming. Have you tried any relaxation techniques like deep breathing or taking short breaks?"
                    ),
                    InputOutputTextPair(
                        input_text="I don't think anyone cares about me",
                        output_text="Your feelings are valid, and I want you to know that I care. Would you like to explore these feelings more? If you're in crisis, we can connect you with someone to talk to immediately."
                    )
                ]
            )
    
    def get_response(self, message, user_id):
        try:
            # Try Vertex AI first if available
            if self.use_vertex:
                response = self.chat.send_message(message, temperature=0.8)
                response_text = response.text
            else:
                # Fallback to Gemini
                prompt = f"{self.context}\n\nUser: {message}\nMannMitra:"
                response = self.gemini_model.generate_content(prompt)
                response_text = response.text
            
            # For crisis detection
            if self.detect_crisis(message):
                crisis_response = self.gemini_model.generate_content(
                    f"User message: {message}. This seems like a potential crisis. Generate a compassionate response that validates their feelings and offers immediate support options."
                )
                return crisis_response.text
            
            return response_text
        except Exception as e:
            print(f"Chat error: {e}")
            return "I'm here to listen. How are you feeling today?"
    
    def detect_crisis(self, message):
        # Use Gemini to detect crisis language
        prompt = f"""
        Analyze this message for signs of mental health crisis: "{message}"
        
        Respond with:
        - "CRISIS" if the message indicates immediate self-harm or severe crisis
        - "CONCERN" if the message indicates depression or potential risk
        - "OK" if the message does not indicate crisis
        
        Response:
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return "CRISIS" in response.text
        except:
            return False