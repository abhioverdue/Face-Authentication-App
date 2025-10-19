import streamlit as st

st.set_page_config(
    page_title="Face Recognition System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1614850523011-8f49ffc73908?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ymx1ZSUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D&fm=jpg&q=60&w=3000');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%);
        z-index: -1;
    }
    
    h1, h2, h3, p { 
        color: white !important; 
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 20, 25, 0.95) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white; font-size: 48px; text-shadow: 0 4px 8px rgba(0,0,0,0.3);'>🔐 Face Recognition Access Control</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 50px;'>Welcome to the System</h3>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.1); padding: 40px; border-radius: 20px; 
         backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
         border: 1px solid rgba(255, 255, 255, 0.2);'>
        <h2 style='text-align: center; color: white; margin-bottom: 30px; font-size: 32px;'>📋 Navigation</h2>
        <p style='font-size: 18px; color: white; text-align: center; line-height: 1.8;'>
            👈 <strong>Use the sidebar</strong> to navigate between:
            <br><br>
            👨‍💼 <strong>Admin Panel</strong> - Register users (PIN: 1234)
            <br>
            👤 <strong>User Access</strong> - Face recognition login
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style='text-align: center; color: white; padding: 30px;'>
    <h3 style='font-size: 28px; margin-bottom: 20px;'>📝 Quick Guide</h3>
    <p style='font-size: 18px; line-height: 1.8;'><strong>Admin Panel:</strong> Register users with PIN (Default: 1234)</p>
    <p style='font-size: 18px; line-height: 1.8;'><strong>User Access:</strong> Face recognition authentication</p>
    <br>
    <p style='font-size: 16px;'>🚀 First time? Go to <strong>Admin Panel</strong> in sidebar to register users!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7); font-size: 14px;'>Powered by DeepFace • TensorFlow • OpenCV</p>", unsafe_allow_html=True)

