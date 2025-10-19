import streamlit as st
import bcrypt
from datetime import datetime, timedelta
import config

class AdminAuthenticator:
    def __init__(self):
        self.session_timeout = config.SESSION_TIMEOUT_MINUTES
        
    def hash_pin(self, pin: str) -> str:
        return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()
    
    def verify_pin(self, pin: str, hashed_pin: str) -> bool:
        try:
            return bcrypt.checkpw(pin.encode(), hashed_pin.encode())
        except:
            return False
    
    def login(self, pin: str) -> bool:
        stored_pin_hash = self.get_stored_pin_hash()
        if self.verify_pin(pin, stored_pin_hash):
            st.session_state.admin_authenticated = True
            st.session_state.admin_login_time = datetime.now()
            return True
        return False
    
    def get_stored_pin_hash(self) -> str:
        if 'stored_pin_hash' not in st.session_state:
            st.session_state.stored_pin_hash = self.hash_pin(config.DEFAULT_ADMIN_PIN)
        return st.session_state.stored_pin_hash
    
    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        stored_hash = self.get_stored_pin_hash()
        if self.verify_pin(old_pin, stored_hash):
            st.session_state.stored_pin_hash = self.hash_pin(new_pin)
            return True
        return False
    
    def is_authenticated(self) -> bool:
        if not st.session_state.get('admin_authenticated', False):
            return False
        login_time = st.session_state.get('admin_login_time')
        if login_time:
            elapsed = datetime.now() - login_time
            if elapsed > timedelta(minutes=self.session_timeout):
                self.logout()
                return False
        return True
    
    def logout(self):
        st.session_state.admin_authenticated = False
        st.session_state.admin_login_time = None
    
    def render_login_form(self) -> bool:
        st.markdown("### 🔐 Admin Authentication")
        st.info("💡 Default PIN: **1234** (Change after first login)")
        
        with st.form("admin_login"):
            pin = st.text_input("Enter Admin PIN", type="password", max_chars=6, placeholder="Enter 4-6 digit PIN")
            submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
            
            if submit:
                if pin:
                    if self.login(pin):
                        st.success("✅ Authentication successful!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid PIN")
                        return False
                else:
                    st.warning("⚠️ Please enter PIN")
                    return False
        return False
