# backend/voice_processing.py
import base64
import tempfile
import os
from google.cloud import speech_v1 as speech
from google.cloud import texttospeech_v1 as texttospeech
from dotenv import load_dotenv

load_dotenv()

class VoiceProcessor:
    def __init__(self):
        # Initialize speech clients
        try:
            self.speech_client = speech.SpeechClient()
            self.tts_client = texttospeech.TextToSpeechClient()
            self.speech_available = True
        except Exception as e:
            print(f"Speech API initialization failed: {e}")
            self.speech_available = False
    
    def speech_to_text(self, audio_data):
        if not self.speech_available:
            return "Voice processing is not available at the moment."
        
        try:
            # Decode base64 audio
            audio_content = base64.b64decode(audio_data)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_content)
                tmp_file_name = tmp_file.name
            
            # Configure recognition
            with open(tmp_file_name, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='en-US',
            )
            
            # Perform speech-to-text
            response = self.speech_client.recognize(config=config, audio=audio)
            
            # Clean up
            os.unlink(tmp_file_name)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
            return "Sorry, I couldn't understand that."
        except Exception as e:
            print(f"Speech to text error: {e}")
            return "Sorry, I couldn't process your audio."
    
    def text_to_speech(self, text):
        if not self.speech_available:
            return None
        
        try:
            # Set up text-to-speech request
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code='en-US',
                name='en-US-Wavenet-D',  # Compassionate female voice
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.9,  # Slightly slower for compassion
                pitch=0.0  # Neutral pitch
            )
            
            # Perform text-to-speech
            response = self.tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            # Encode to base64 for sending over HTTP
            return base64.b64encode(response.audio_content).decode('utf-8')
        except Exception as e:
            print(f"Text to speech error: {e}")
            return None