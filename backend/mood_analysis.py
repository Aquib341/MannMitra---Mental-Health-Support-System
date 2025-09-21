# backend/mood_analysis.py
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class MoodAnalyzer:
    def __init__(self):
        # Initialize Vertex AI
        aiplatform.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION"))
        self.text_model = TextGenerationModel.from_pretrained("text-bison@001")
    
    def analyze_text(self, text):
        """Analyze mood from text input"""
        prompt = f"""
        Analyze the following text for emotional content and determine the primary mood:
        "{text}"
        
        Respond with ONLY one of these moods: happy, sad, angry, anxious, stressed, neutral, or crisis.
        
        If the text indicates self-harm or immediate danger, respond with "crisis".
        
        Mood:
        """
        
        try:
            response = self.text_model.predict(prompt, temperature=0.2)
            mood = response.text.strip().lower()
            
            # Validate response
            valid_moods = ['happy', 'sad', 'angry', 'anxious', 'stressed', 'neutral', 'crisis']
            if mood not in valid_moods:
                return "neutral"
            
            return mood
        except Exception as e:
            print(f"Mood analysis error: {e}")
            return "neutral"
    
    def analyze_trends(self, mood_data):
        """Analyze mood trends over time"""
        if not mood_data or len(mood_data) < 5:
            return {"insights": ["Not enough data yet. Keep using the app to get personalized insights."]}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(mood_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        
        # Map moods to scores for trend analysis
        mood_scores = {
            'happy': 3, 
            'neutral': 2, 
            'anxious': 1, 
            'stressed': 1, 
            'sad': 0, 
            'angry': 0, 
            'crisis': -1
        }
        
        df['mood_score'] = df['mood'].map(mood_scores)
        
        # Calculate daily averages
        daily_avg = df['mood_score'].resample('D').mean()
        
        insights = []
        
        # Weekly trends
        if len(daily_avg) > 7:
            recent_week = daily_avg[-7:].mean()
            previous_week = daily_avg[-14:-7].mean() if len(daily_avg) > 14 else daily_avg[:7].mean()
            
            if recent_week > previous_week + 0.5:
                insights.append("Your mood has improved over the last week. Keep up the positive habits!")
            elif recent_week < previous_week - 0.5:
                insights.append("I've noticed your mood has been lower recently. Would you like to talk about it?")
        
        # Time-of-day patterns
        df['hour'] = df.index.hour
        morning_avg = df[df['hour'] < 12]['mood_score'].mean()
        afternoon_avg = df[(df['hour'] >= 12) & (df['hour'] < 17)]['mood_score'].mean()
        evening_avg = df[df['hour'] >= 17]['mood_score'].mean()
        
        if morning_avg < afternoon_avg and morning_avg < evening_avg:
            insights.append("You tend to feel better as the day goes on. Consider starting your day with a positive routine.")
        elif evening_avg < morning_avg and evening_avg < afternoon_avg:
            insights.append("Your energy seems highest in the mornings. Try scheduling important tasks earlier in the day.")
        
        if not insights:
            insights.append("Your mood patterns are fairly consistent. Regular check-ins help maintain mental wellbeing.")
        
        # Generate weekly summary using AI
        summary = self.generate_weekly_summary(df)
        insights.append(summary)
        
        return {"insights": insights}
    
    def generate_weekly_summary(self, df):
        """Generate a weekly mood summary using AI"""
        mood_counts = df['mood'].value_counts().to_dict()
        
        prompt = f"""
        Based on the following mood distribution from the past week: {mood_counts}
        Generate a compassionate, encouraging weekly summary for a mental health app user.
        Keep it brief (2-3 sentences) and focus on positive reinforcement.
        """
        
        try:
            response = self.text_model.predict(prompt, temperature=0.7)
            return response.text
        except:
            return "Thanks for checking in with your emotions this week. Regular self-reflection is an important part of mental wellbeing."