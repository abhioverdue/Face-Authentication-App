import streamlit as st
from PIL import Image
import os
import config
from utils.authentication import AdminAuthenticator
from utils.database_manager import DatabaseManager
import pandas as pd

st.set_page_config(page_title="Admin Panel", page_icon="👨‍💼", layout="wide")

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

auth = AdminAuthenticator()
db_manager = DatabaseManager()

if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'photo_step' not in st.session_state:
    st.session_state.photo_step = 0
if 'captured_photos' not in st.session_state:
    st.session_state.captured_photos = []

if not auth.is_authenticated():
    st.title("👨‍💼 Admin Control Panel")
    st.markdown("### Secure Access Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth.render_login_form()
    st.stop()

col1, col2 = st.columns([3, 1])
with col1:
    st.title("👨‍💼 Admin Control Panel")
    st.markdown("### Face Recognition System Management")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        auth.logout()
        st.rerun()

st.markdown("---")

with st.sidebar:
    st.markdown("## 📋 Admin Menu")
    mode = st.radio("", ["📊 Dashboard", "➕ Register User", "👥 Manage Users", "📜 Access Logs", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    stats = db_manager.get_statistics()
    st.metric("👥 Users", stats['total_users'])
    st.metric("✅ Access", stats['total_accesses'])
    st.metric("❌ Denials", stats['total_denials'])

if "Dashboard" in mode:
    st.header("📊 System Dashboard")
    stats = db_manager.get_statistics()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Registered Users", stats['total_users'])
    col2.metric("✅ Successful Access", stats['total_accesses'])
    col3.metric("❌ Denied Access", stats['total_denials'])
    col4.metric("⚠️ Suspicious", stats['suspicious_count'])
    st.markdown("---")
    st.markdown("### 📜 Recent Activity (Last 20)")
    logs = db_manager.get_access_logs(limit=20)
    if logs:
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No logs yet")

elif "Register User" in mode:
    st.header("➕ Register New User")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📝 User Information")
        full_name = st.text_input("Full Name *", placeholder="John Doe")
        employee_id = st.text_input("Employee ID", placeholder="EMP001")
        department = st.text_input("Department", placeholder="Engineering")
        notes = st.text_area("Notes", placeholder="Additional info...")
        st.markdown("### 📸 Upload Photos")
        upload_method = st.radio("Method:", ["📁 File Upload", "📷 Guided Camera"])
        uploaded_images = []
        if upload_method == "📁 File Upload":
            uploaded_images = st.file_uploader(f"Select {config.MIN_PHOTOS_PER_PERSON}-{config.MAX_PHOTOS_PER_PERSON} photos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        else:
            st.markdown("---")
            photo_instructions = [
                {"title": "📸 Photo 1: Face Forward", "instruction": "Look straight at the camera", "emoji": "😐"},
                {"title": "📸 Photo 2: Turn Left", "instruction": "Turn your head slightly to the LEFT", "emoji": "↖️"},
                {"title": "📸 Photo 3: Turn Right", "instruction": "Turn your head slightly to the RIGHT", "emoji": "↗️"},
            ]
            current_step = st.session_state.photo_step
            st.progress(current_step / 3, text=f"Progress: {current_step}/3 photos captured")
            if current_step < 3:
                instruction = photo_instructions[current_step]
                st.markdown(f"""
                <div style='background: rgba(10, 102, 194, 0.15); padding: 20px; border-radius: 12px; border-left: 4px solid #0A66C2; margin: 16px 0;'>
                    <h3 style='margin: 0 0 8px 0; color: white;'>{instruction['title']}</h3>
                    <p style='font-size: 18px; margin: 0; color: white;'>{instruction['emoji']} <strong>{instruction['instruction']}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                camera_img = st.camera_input(f"📷 Capture Photo {current_step + 1}/3", key=f"cam_{current_step}")
                if camera_img:
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("✅ Use This Photo", use_container_width=True, type="primary"):
                            st.session_state.captured_photos.append(camera_img)
                            st.session_state.photo_step += 1
                            st.success(f"✓ Photo {current_step + 1} captured!")
                            st.rerun()
                    with col_btn2:
                        if st.button("🔄 Retake", use_container_width=True):
                            st.info("Take another photo")
                            st.rerun()
            else:
                st.success("🎉 All 3 photos captured successfully!")
                if st.button("🗑️ Start Over", use_container_width=True):
                    st.session_state.photo_step = 0
                    st.session_state.captured_photos = []
                    st.rerun()
                uploaded_images = st.session_state.captured_photos
    with col2:
        st.markdown("### 👁️ Preview")
        if upload_method == "📷 Guided Camera":
            if st.session_state.captured_photos:
                st.success(f"✅ {len(st.session_state.captured_photos)}/3 photos captured")
                photo_labels = ["📸 Front", "📸 Left", "📸 Right"]
                cols = st.columns(3)
                for idx, img in enumerate(st.session_state.captured_photos):
                    with cols[idx]:
                        st.image(img, use_column_width=True, caption=photo_labels[idx])
            else:
                st.info("👆 Follow the instructions to capture photos")
        elif uploaded_images:
            st.success(f"✅ {len(uploaded_images)} photos uploaded")
            cols = st.columns(3)
            for idx, img in enumerate(uploaded_images[:6]):
                with cols[idx % 3]:
                    st.image(img, use_column_width=True, caption=f"Photo {idx+1}")
        else:
            st.info("📤 Upload photos to see preview")
        st.markdown("---")
        if upload_method == "📁 File Upload":
            can_register = full_name and len(uploaded_images) >= config.MIN_PHOTOS_PER_PERSON and len(uploaded_images) <= config.MAX_PHOTOS_PER_PERSON
        else:
            can_register = full_name and len(st.session_state.captured_photos) == 3
            uploaded_images = st.session_state.captured_photos
        if st.button("✅ Register User", type="primary", disabled=not can_register, use_container_width=True):
            with st.spinner(f"🔄 Registering {full_name}..."):
                temp_paths = []
                for i, img in enumerate(uploaded_images):
                    temp_path = os.path.join(config.TEMP_DIR, f"reg_{full_name}_{i}.jpg")
                    Image.open(img).save(temp_path)
                    temp_paths.append(temp_path)
                success = db_manager.register_new_user(full_name, temp_paths, employee_id, department, notes)
                if success:
                    st.success(f"🎉 {full_name} registered successfully!")
                    st.balloons()
                    st.session_state.photo_step = 0
                    st.session_state.captured_photos = []
                    st.cache_resource.clear()
                else:
                    st.error("❌ Registration failed. Please try again.")

elif "Manage Users" in mode:
    st.header("👥 Manage Users")
    users = db_manager.get_registered_users()
    if not users:
        st.info("No users yet")
    else:
        search = st.text_input("🔍 Search", placeholder="Name or ID...")
        if search:
            users = [u for u in users if search.lower() in u.lower()]
        st.markdown(f"### {len(users)} User(s)")
        for user in users:
            with st.expander(f"👤 {user}"):
                info = db_manager.get_user_info(user)
                img_count = db_manager.get_user_image_count(user)
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Name:** {user}")
                    if info:
                        st.write(f"**Employee ID:** {info.get('employee_id', 'N/A')}")
                        st.write(f"**Department:** {info.get('department', 'N/A')}")
                        st.write(f"**Photos:** {img_count}")
                        st.write(f"**Registered:** {info.get('registered_date', 'N/A')[:10]}")
                        st.write(f"**Last Seen:** {info.get('last_seen', 'Never')[:16] if info.get('last_seen') else 'Never'}")
                        st.write(f"**Access Count:** {info.get('total_access_count', 0)}")
                with col2:
                    user_dir = os.path.join(config.DATABASE_DIR, user)
                    if os.path.exists(user_dir):
                        photos = [f for f in os.listdir(user_dir) if f.endswith(('.jpg', '.png'))]
                        if photos:
                            st.image(os.path.join(user_dir, photos[0]), use_column_width=True)
                st.markdown("---")
                if st.button(f"🗑️ Delete", key=f"del_{user}"):
                    if st.checkbox(f"⚠️ Confirm delete {user}", key=f"conf_{user}"):
                        if db_manager.delete_user(user):
                            st.success("Deleted!")
                            st.cache_resource.clear()
                            st.rerun()

elif "Access Logs" in mode:
    st.header("📜 Access Logs")
    limit = st.slider("Logs to show", 10, 200, 50)
    logs = db_manager.get_access_logs(limit=limit)
    if logs:
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "access_logs.csv", "text/csv", use_container_width=True)
    else:
        st.info("No logs")

elif "Settings" in mode:
    st.header("⚙️ Settings")
    tab1, tab2, tab3 = st.tabs(["🔐 Security", "🎛️ Recognition", "📊 System"])
    with tab1:
        st.markdown("### Change Admin PIN")
        with st.form("change_pin"):
            old_pin = st.text_input("Current PIN", type="password")
            new_pin = st.text_input("New PIN", type="password")
            confirm_pin = st.text_input("Confirm PIN", type="password")
            if st.form_submit_button("🔄 Change"):
                if new_pin != confirm_pin:
                    st.error("PINs don't match")
                elif len(new_pin) < 4:
                    st.error("Min 4 digits")
                elif auth.change_pin(old_pin, new_pin):
                    st.success("✅ PIN changed!")
                else:
                    st.error("❌ Wrong current PIN")
    with tab2:
        st.markdown("### Recognition Settings")
        st.info("Current config from config.py")
        col1, col2 = st.columns(2)
        col1.write(f"**Model:** {config.FACE_RECOGNITION_MODEL}")
        col1.write(f"**Backend:** {config.FACE_DETECTION_BACKEND}")
        col2.write(f"**Threshold:** {config.RECOGNITION_THRESHOLD}")
        col2.write(f"**Min Photos:** {config.MIN_PHOTOS_PER_PERSON}")
    with tab3:
        st.markdown("### System Info")
        stats = db_manager.get_statistics()
        st.json(stats)

st.markdown("---")
st.markdown("<p style='text-align: center; color: white;'>👨‍💼 Admin Panel v2.0 | Powered by DeepFace</p>", unsafe_allow_html=True)

