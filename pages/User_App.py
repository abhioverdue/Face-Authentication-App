import streamlit as st
from PIL import Image
import os
import config
from utils.face_recognition import FaceRecognizer
from utils.emotion_detector import EmotionDetector
from utils.database_manager import DatabaseManager

st.set_page_config(page_title="User Access", page_icon="👤", layout="wide")


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* BACKGROUND IMAGE */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1614850523011-8f49ffc73908?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ymx1ZSUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D&fm=jpg&q=60&w=3000');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif !important;
    } </style>
""", unsafe_allow_html=True)
@st.cache_resource
def get_recognizer():
    return FaceRecognizer()

@st.cache_resource
def get_emotion_detector():
    return EmotionDetector()

recognizer = get_recognizer()
emotion_detector = get_emotion_detector()
db_manager = DatabaseManager()

# Header
st.title("🔐 Face Recognition Access Control")
st.markdown("<h3 style='text-align: center; color: white;'>Present Your Face for Authentication</h3>", unsafe_allow_html=True)
st.markdown("---")

# Check users
users = db_manager.get_registered_users()
if not users:
    st.error("❌ No users registered. Contact administrator.")
    st.stop()

# Main
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 📸 Capture Your Face")
    camera_photo = st.camera_input("Look at camera", label_visibility="collapsed")
    
    if camera_photo:
        st.image(camera_photo, caption="Captured", use_column_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔍 AUTHENTICATE", type="primary", use_container_width=True):
            with st.spinner("🔄 Analyzing..."):
                temp_path = os.path.join(config.TEMP_DIR, "user_access.jpg")
                Image.open(camera_photo).save(temp_path)
                
                has_face = recognizer.quick_face_check(temp_path)
                
                if not has_face:
                    st.error("❌ No face detected")
                else:
                    person_name, confidence, all_matches = recognizer.recognize_face(temp_path)
                    emotion_result, suspicion_score, is_suspicious = emotion_detector.analyze_emotion(temp_path)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # ACCESS GRANTED
                    if person_name:
                        st.markdown(f"""
                        <div class='access-granted'>
                            ✅ ACCESS GRANTED<br>
                            <div style='font-size: 48px; margin-top: 20px;'>{person_name}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("🎯 Confidence", f"{confidence*100:.1f}%")
                        
                        dominant = emotion_result['dominant_emotion']
                        emoji = emotion_detector.get_emotion_emoji(dominant)
                        col_b.metric("😊 Emotion", f"{emoji} {dominant.title()}")
                        
                        user_info = db_manager.get_user_info(person_name)
                        dept = user_info.get('department', 'N/A') if user_info else 'N/A'
                        col_c.metric("🏢 Department", dept)
                        
                        db_manager.log_access(person_name, confidence, dominant, is_suspicious)
                        
                        if is_suspicious:
                            st.warning(f"⚠️ Unusual behavior ({suspicion_score*100:.1f}%)")
                        
                        st.balloons()
                    
                    # ACCESS DENIED
                    else:
                        st.markdown("""
                        <div class='access-denied'>
                            ❌ ACCESS DENIED<br>
                            <div style='font-size: 24px; margin-top: 20px;'>Unknown Person</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.error("Not authorized. Contact admin to register.")
                        db_manager.log_access_denied(0.0)
                        
                        with st.expander("🔍 Debug: Matches"):
                            for name, distance in sorted(all_matches.items(), key=lambda x: x[1])[:3]:
                                st.write(f"{name}: {(1-distance)*100:.1f}%")

# Sidebar
with st.sidebar:
    st.markdown("## ℹ️ How to Use")
    st.info("""
    1. Look at camera
    2. Capture photo
    3. Click AUTHENTICATE
    4. Wait for result
    """)
    st.markdown("---")
    st.metric("👥 Registered", len(users))
    st.markdown("---")
    st.success("🟢 System Online")

st.markdown("---")
st.markdown("<p style='text-align: center; color: white;'>👤 User Access v2.0</p>", unsafe_allow_html=True)
