"""
SOULFRIEND Admin Components - Enhanced Authentication
Hệ thống xác thực admin nâng cao với bảo mật tốt hơn
"""

import streamlit as st
import hashlib
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import secrets
import logging

# Setup logging for admin activities
admin_logger = logging.getLogger('admin_auth')
admin_logger.setLevel(logging.INFO)

class AdminAuth:
    """Enhanced Admin Authentication System"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 3
        self.lockout_duration = 900  # 15 minutes
        self.admin_config_file = "/workspaces/Mentalhealth/data/admin_config.json"
        self.init_admin_config()
    
    def init_admin_config(self):
        """Initialize admin configuration"""
        if not os.path.exists(self.admin_config_file):
            os.makedirs(os.path.dirname(self.admin_config_file), exist_ok=True)
            
            default_config = {
                "admin_users": {
                    "admin": {
                        "password_hash": self.hash_password("SoulFriend2025!"),
                        "role": "super_admin",
                        "created": datetime.now().isoformat(),
                        "last_login": None,
                        "failed_attempts": 0,
                        "locked_until": None,
                        "permissions": ["all"]
                    },
                    "doctor": {
                        "password_hash": self.hash_password("Doctor2025!"),
                        "role": "medical_admin", 
                        "created": datetime.now().isoformat(),
                        "last_login": None,
                        "failed_attempts": 0,
                        "locked_until": None,
                        "permissions": ["view_users", "view_reports", "manage_assessments"]
                    },
                    "analyst": {
                        "password_hash": self.hash_password("Analyst2025!"),
                        "role": "data_analyst",
                        "created": datetime.now().isoformat(), 
                        "last_login": None,
                        "failed_attempts": 0,
                        "locked_until": None,
                        "permissions": ["view_reports", "view_analytics", "export_data"]
                    }
                },
                "security_settings": {
                    "session_timeout": 3600,
                    "max_login_attempts": 3,
                    "lockout_duration": 900,
                    "require_2fa": False,
                    "password_expiry_days": 90
                },
                "audit_log": []
            }
            
            with open(self.admin_config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    def load_admin_config(self) -> Dict:
        """Load admin configuration"""
        try:
            with open(self.admin_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            admin_logger.error(f"Failed to load admin config: {e}")
            return {}
    
    def save_admin_config(self, config: Dict):
        """Save admin configuration"""
        try:
            with open(self.admin_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            admin_logger.error(f"Failed to save admin config: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = "SoulFriend2025"
        hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hash_bytes.hex()
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def is_account_locked(self, username: str) -> bool:
        """Check if account is locked"""
        config = self.load_admin_config()
        user_data = config.get("admin_users", {}).get(username, {})
        
        locked_until = user_data.get("locked_until")
        if locked_until:
            unlock_time = datetime.fromisoformat(locked_until)
            if datetime.now() < unlock_time:
                return True
            else:
                # Unlock account
                user_data["locked_until"] = None
                user_data["failed_attempts"] = 0
                self.save_admin_config(config)
        
        return False
    
    def verify_credentials(self, username: str, password: str) -> Tuple[bool, str, Dict]:
        """Verify admin credentials"""
        config = self.load_admin_config()
        
        # Check if account exists
        if username not in config.get("admin_users", {}):
            self.log_audit_event("login_failed", username, "Invalid username")
            return False, "Tên đăng nhập không tồn tại", {}
        
        user_data = config["admin_users"][username]
        
        # Check if account is locked
        if self.is_account_locked(username):
            locked_until = user_data.get("locked_until")
            unlock_time = datetime.fromisoformat(locked_until)
            remaining = unlock_time - datetime.now()
            minutes = int(remaining.total_seconds() / 60)
            self.log_audit_event("login_blocked", username, f"Account locked for {minutes} minutes")
            return False, f"Tài khoản bị khóa. Thử lại sau {minutes} phút", {}
        
        # Verify password
        if user_data["password_hash"] == self.hash_password(password):
            # Reset failed attempts
            user_data["failed_attempts"] = 0
            user_data["last_login"] = datetime.now().isoformat()
            self.save_admin_config(config)
            
            self.log_audit_event("login_success", username, "Successful login")
            return True, "Đăng nhập thành công", user_data
        else:
            # Increment failed attempts
            user_data["failed_attempts"] += 1
            
            if user_data["failed_attempts"] >= self.max_login_attempts:
                # Lock account
                lock_until = datetime.now() + timedelta(seconds=self.lockout_duration)
                user_data["locked_until"] = lock_until.isoformat()
                self.log_audit_event("account_locked", username, f"Account locked after {self.max_login_attempts} failed attempts")
                message = f"Tài khoản bị khóa sau {self.max_login_attempts} lần đăng nhập sai"
            else:
                remaining = self.max_login_attempts - user_data["failed_attempts"]
                message = f"Mật khẩu sai. Còn {remaining} lần thử"
                self.log_audit_event("login_failed", username, f"Wrong password, {user_data['failed_attempts']} attempts")
            
            self.save_admin_config(config)
            return False, message, {}
    
    def log_audit_event(self, event_type: str, username: str, details: str):
        """Log audit events"""
        config = self.load_admin_config()
        
        audit_event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "username": username,
            "details": details,
            "ip_address": "localhost",  # In production, get real IP
            "user_agent": "Streamlit"
        }
        
        config.setdefault("audit_log", []).append(audit_event)
        
        # Keep only last 1000 events
        if len(config["audit_log"]) > 1000:
            config["audit_log"] = config["audit_log"][-1000:]
        
        self.save_admin_config(config)
        admin_logger.info(f"Audit: {event_type} - {username} - {details}")
    
    def check_session_validity(self) -> bool:
        """Check if current admin session is valid"""
        if 'admin_authenticated' not in st.session_state:
            return False
        
        if 'admin_session_start' not in st.session_state:
            return False
        
        session_start = st.session_state.admin_session_start
        current_time = time.time()
        
        if current_time - session_start > self.session_timeout:
            self.logout()
            return False
        
        return st.session_state.admin_authenticated
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Admin login"""
        success, message, user_data = self.verify_credentials(username, password)
        
        if success:
            # Set session state
            st.session_state.admin_authenticated = True
            st.session_state.admin_username = username
            st.session_state.admin_role = user_data.get("role", "admin")
            st.session_state.admin_permissions = user_data.get("permissions", [])
            st.session_state.admin_session_start = time.time()
            st.session_state.admin_session_token = self.generate_session_token()
            
            return True, message
        else:
            return False, message
    
    def logout(self):
        """Admin logout"""
        if 'admin_username' in st.session_state:
            self.log_audit_event("logout", st.session_state.admin_username, "User logout")
        
        # Clear admin session
        admin_keys = [key for key in st.session_state.keys() if key.startswith('admin_')]
        for key in admin_keys:
            del st.session_state[key]
    
    def has_permission(self, permission: str) -> bool:
        """Check if current admin has specific permission"""
        if not self.check_session_validity():
            return False
        
        permissions = st.session_state.get('admin_permissions', [])
        return 'all' in permissions or permission in permissions
    
    def render_login_form(self) -> bool:
        """Render admin login form"""
        st.markdown("### 🔐 SOULFRIEND Admin Login")
        st.markdown("---")
        
        with st.form("admin_login_form"):
            st.markdown("#### Thông tin đăng nhập")
            
            username = st.text_input(
                "👤 Tên đăng nhập", 
                placeholder="Nhập tên đăng nhập admin"
            )
            
            password = st.text_input(
                "🔑 Mật khẩu", 
                type="password",
                placeholder="Nhập mật khẩu"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("🚀 Đăng nhập", type="primary")
            with col2:
                st.form_submit_button("🔄 Làm mới")
            
            if login_button and username and password:
                success, message = self.login(username, password)
                
                if success:
                    st.success(f"✅ {message}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        # Help section
        with st.expander("ℹ️ Thông tin đăng nhập"):
            st.markdown("""
            **Tài khoản mặc định:**
            - **Super Admin**: admin / SoulFriend2025!
            - **Medical Admin**: doctor / Doctor2025!
            - **Data Analyst**: analyst / Analyst2025!
            
            **Chính sách bảo mật:**
            - Tối đa 3 lần đăng nhập sai
            - Khóa tài khoản 15 phút nếu vượt quá
            - Phiên làm việc tự động hết hạn sau 1 giờ
            """)
        
        return False
    
    def render_session_info(self):
        """Render current session information"""
        if self.check_session_validity():
            with st.sidebar:
                st.markdown("### 👤 Admin Session")
                st.success(f"**User:** {st.session_state.admin_username}")
                st.info(f"**Role:** {st.session_state.admin_role}")
                
                # Session timer
                session_start = st.session_state.admin_session_start
                elapsed = time.time() - session_start
                remaining = self.session_timeout - elapsed
                
                if remaining > 0:
                    hours = int(remaining // 3600)
                    minutes = int((remaining % 3600) // 60)
                    st.warning(f"**Session:** {hours:02d}:{minutes:02d} remaining")
                
                if st.button("🚪 Đăng xuất", key="admin_logout"):
                    self.logout()
                    st.rerun()

# Global admin auth instance
admin_auth = AdminAuth()

def require_admin_auth(permission: str = None):
    """Decorator để yêu cầu admin authentication"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not admin_auth.check_session_validity():
                admin_auth.render_login_form()
                return None
            
            if permission and not admin_auth.has_permission(permission):
                st.error(f"❌ Bạn không có quyền: {permission}")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
