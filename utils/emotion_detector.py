from deepface import DeepFace
import config
from typing import Dict, Tuple

class EmotionDetector:
    def __init__(self):
        self.detector_backend = config.FACE_DETECTION_BACKEND
        self.suspicion_emotions = config.SUSPICION_EMOTIONS
        self.suspicion_threshold = config.SUSPICION_THRESHOLD
    
    def analyze_emotion(self, img_path: str) -> Tuple[Dict, float, bool]:
        try:
            analysis = DeepFace.analyze(
                img_path=img_path,
                actions=['emotion'],
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            emotions = analysis.get('emotion', {})
            dominant_emotion = analysis.get('dominant_emotion', 'neutral')
            
            suspicion_score = 0.0
            for emotion, weight in self.suspicion_emotions.items():
                if emotion in emotions:
                    suspicion_score += emotions[emotion] * weight / 100
            
            is_suspicious = suspicion_score >= self.suspicion_threshold
            
            return {
                'emotions': emotions,
                'dominant_emotion': dominant_emotion,
                'suspicion_score': suspicion_score,
                'is_suspicious': is_suspicious
            }, suspicion_score, is_suspicious
        except Exception as e:
            print(f"Emotion analysis error: {e}")
            return {
                'emotions': {},
                'dominant_emotion': 'unknown',
                'suspicion_score': 0.0,
                'is_suspicious': False
            }, 0.0, False
    
    def get_emotion_emoji(self, emotion: str) -> str:
        emoji_map = {
            'happy': '😊', 'sad': '😢', 'angry': '😠',
            'fear': '😨', 'surprise': '😮', 'disgust': '🤢',
            'neutral': '😐'
        }
        return emoji_map.get(emotion.lower(), '😐')
