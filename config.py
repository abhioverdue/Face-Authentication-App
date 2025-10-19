import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database", "friends")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "database", "embeddings.pkl")
USER_INFO_PATH = os.path.join(BASE_DIR, "database", "user_info.json")
ACCESS_LOGS_PATH = os.path.join(BASE_DIR, "database", "access_logs.json")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Model Configuration
FACE_DETECTION_BACKEND = "opencv"
FACE_RECOGNITION_MODEL = "Facenet512"
EMOTION_MODEL = "deepface"
DISTANCE_METRIC = "cosine"

# Thresholds
RECOGNITION_THRESHOLD = 0.50
VERIFICATION_THRESHOLD = 0.50
CONFIDENCE_THRESHOLD = 0.70

# Emotion-based Suspicion
SUSPICION_EMOTIONS = {
    "angry": 0.3,
    "fear": 0.25,
    "sad": 0.2,
    "disgust": 0.15
}
SUSPICION_THRESHOLD = 0.5

# Registration Settings
MIN_PHOTOS_PER_PERSON = 3
MAX_PHOTOS_PER_PERSON = 7
RECOMMENDED_PHOTOS = 4

# Admin Settings
DEFAULT_ADMIN_PIN = "1234"
SESSION_TIMEOUT_MINUTES = 30

# UI Configuration
APP_TITLE = "🔐 Face Recognition System"
PRIMARY_COLOR = "#007AFF"
SUCCESS_COLOR = "#34C759"
ERROR_COLOR = "#FF3B30"
WARNING_COLOR = "#FF9500"
ADMIN_COLOR = "#5856D6"

# Create directories
for directory in [DATABASE_DIR, TEMP_DIR, ASSETS_DIR]:
    os.makedirs(directory, exist_ok=True)
