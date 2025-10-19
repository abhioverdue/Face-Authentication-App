# Face Recognition Access Control System

A face recognition system with guided photo capture, admin panel, and emotion detection built with Python, DeepFace, and Streamlit.
---

## Features

**Core Functionality**
- Face recognition using Facenet512 model (98%+ accuracy)
- Guided 3-angle photo capture (front, left, right)
- PIN-protected admin panel (default: 1234)
- Real-time user authentication
- Emotion detection with 7 emotion categories
- Complete access logging with CSV export
- Multi-page application with sidebar navigation

**Security**
- bcrypt-hashed PIN authentication
- Session management with 30-minute timeout
- Role-based access control
- Full audit trail logging

---

## Project Structure

```
face-auth-system/
├── app.py                      # Main launcher
├── pages/
│   ├── Admin_App.py          # Admin panel
│   └── User_App.py     # User authentication
├── utils/
│   ├── authentication.py       # PIN authentication
│   ├── database_manager.py     # User & log management
│   ├── face_recognition.py     # Recognition engine
│   ├── face_verification.py    # 1:1 verification
│   └── emotion_detector.py     # Emotion analysis
├── database/
│   ├── friends/                # User face images
│   ├── embeddings.pkl          # Face embeddings cache
│   ├── user_info.json          # User metadata
│   └── access_logs.json        # Access logs
├── config.py                   # Configuration
└── requirements.txt            # Dependencies
```

---

## Installation

**Prerequisites**
- Python 3.10 or 3.11 (3.12+ not fully supported)
- Webcam
- 4GB+ RAM

**Setup**
```bash
# Clone/download and navigate to project
cd face-auth-system

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access at `http://localhost:8501`

---

## Usage

### Admin Panel

**Initial Login**
- Navigate to Admin Panel in sidebar
- Enter default PIN: `1234`

**Register Users**
1. Click "Register User"
2. Enter user details (name required)
3. Choose capture method:
   - **Guided Camera**: Capture 3 angles (front, left, right)
   - **File Upload**: Upload 3-7 photos
4. Click "Register User"

**Manage Users**
- View registered users
- Review access history
- Delete users
- Change admin PIN in Settings → Security

### User Access Panel

1. Navigate to User Access in sidebar
2. Capture photo using camera
3. Click "Authenticate"
4. View result: Access Granted/Denied with confidence score and emotion

---

## Photo Capture Guidelines

**Best Practices**
- Clear, well-lit face centered in frame
- Face fills 30-40% of image
- Natural lighting (avoid backlighting)
- Look directly at camera
- No sunglasses or masks

**Guided Capture**
- Front: Look straight ahead
- Left: Turn head 20-30° left
- Right: Turn head 20-30° right

---

## Configuration

Key settings in `config.py`:

```python
# Recognition
FACE_RECOGNITION_MODEL = "Facenet512"
FACE_DETECTION_BACKEND = "opencv"
RECOGNITION_THRESHOLD = 0.50  # Lower = stricter (0.40-0.60)
DISTANCE_METRIC = "cosine"

# Photos
MIN_PHOTOS_PER_PERSON = 3
MAX_PHOTOS_PER_PERSON = 7

# Security
DEFAULT_ADMIN_PIN = "1234"  # Change immediately
SESSION_TIMEOUT_MINUTES = 30

# Emotion Detection
SUSPICION_THRESHOLD = 0.5
```

---

## Technical Specifications

**Models**
- Face Recognition: Facenet512 (128-dimensional embeddings)
- Face Detection: OpenCV Haar Cascades / RetinaFace
- Emotion Detection: DeepFace emotion model

**Performance**
- Recognition Speed: 1-2 seconds
- Memory Usage: ~500MB base + 50MB per 100 users
- Accuracy: 90-95% with quality photos

---

## Troubleshooting

**User Not Recognized**
- Add more photos (4-5 recommended)
- Improve lighting during capture
- Lower `RECOGNITION_THRESHOLD` in config

**No Face Detected**
- Improve lighting
- Move closer to camera
- Try different `FACE_DETECTION_BACKEND`

**TensorFlow Errors**
```bash
pip uninstall tensorflow deepface -y
pip install tensorflow==2.16.1 deepface==0.0.92
```

**Forgotten Admin PIN**
- Delete `.streamlit/` cache folder
- Restart app (resets to 1234)

---

## Database Schema

**User Info** (`database/user_info.json`)
```json
{
  "John Doe": {
    "full_name": "John Doe",
    "employee_id": "EMP001",
    "department": "Engineering",
    "photo_count": 4,
    "registered_date": "2025-10-19 20:30:15",
    "last_seen": "2025-10-19 21:15:42",
    "total_access_count": 5
  }
}
```

**Access Logs** (`database/access_logs.json`)
```json
[
  {
    "timestamp": "2025-10-19 21:15:42",
    "user_name": "John Doe",
    "confidence": 92.5,
    "emotion": "happy",
    "suspicious": false,
    "status": "granted"
  }
]
```

---

## Security Best Practices

1. Change default PIN immediately after first login
2. Keep `database/` folder secure (don't commit to public repos)
3. Review access logs regularly
4. Update dependencies periodically
5. Set up regular database backups

---

## Requirements

```
streamlit==1.30.0
opencv-python==4.8.1.78
deepface==0.0.92
tensorflow==2.16.1
numpy==1.26.4
pandas==2.1.4
Pillow==10.1.0
mtcnn==0.1.1
bcrypt==4.1.2
PyYAML==6.0.1
```

---

## Deployment

**Local Network**
```bash
streamlit run app.py 
```
Access from other devices: `http://localhost:8501`

**Cloud (Streamlit Cloud)**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy from repository

---

## Known Issues

- TensorFlow warnings on startup (can be ignored)
- Camera lag on first capture (model loading)
- False positives in low light conditions
- Emotion detection accuracy ~70-80%

---

## License

MIT License

---

**Version 2.0 | Built with DeepFace, TensorFlow, and Streamlit**
