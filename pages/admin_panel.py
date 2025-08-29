"""
SOULFRIEND Admin Panel
Administrative interface for managing mental health assessment system
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.admin_auth import admin_auth, require_admin_auth
from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Admin",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# App header
app_header()

# Admin panel interface with enhanced authentication
def main():
    """Main admin panel function"""
    st.markdown("# 🔧 SOULFRIEND Admin Panel V2.0")
    st.markdown("#### Hệ thống quản trị nâng cao")
    st.markdown("---")
    
    # Check authentication
    if not admin_auth.check_session_validity():
        admin_auth.render_login_form()
        return
    
    # Render session info
    admin_auth.render_session_info()
    
    # Main admin interface
    admin_dashboard()

@require_admin_auth()
def admin_dashboard():
    """Main admin dashboard - requires authentication"""
    st.success(f"🎉 Chào mừng {st.session_state.admin_username}!")
    st.info(f"🛡️ Role: {st.session_state.admin_role}")
    
    # Admin tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "👥 User Management", 
        "📋 System Monitor",
        "🔐 Security",
        "⚙️ Settings"
    ])
    
    with tab1:
        render_admin_dashboard()
    
    with tab2:
        render_user_management()
    
    with tab3:
        render_system_monitor()
    
    with tab4:
        render_security_panel()
    
    with tab5:
        render_admin_settings()

def render_admin_dashboard():
    """Render main admin dashboard"""
    st.markdown("### 📊 System Overview")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Users", "150", "↗️ +12")
    
    with col2:
        st.metric("📝 Assessments Today", "45", "↗️ +8")
    
    with col3:
        st.metric("⚡ System Health", "98%", "↗️ +2%")
    
    with col4:
        st.metric("🔐 Security Score", "95%", "→ 0%")
    
    st.markdown("---")
    
    # Activity overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### � Recent Activity")
        st.info("🔸 User 'anonymous_123' completed PHQ-9 assessment")
        st.info("🔸 User 'anonymous_456' started GAD-7 assessment") 
        st.info("🔸 System backup completed successfully")
        st.info("🔸 2 new user registrations today")
    
    with col2:
        st.markdown("#### ⚠️ System Alerts")
        st.warning("🔸 High memory usage detected (85%)")
        st.success("🔸 All services running normally")
        st.info("🔸 Database optimization scheduled")

def render_user_management():
    """Render user management panel"""
    if not admin_auth.has_permission("view_users"):
        st.error("❌ Bạn không có quyền quản lý người dùng")
        return
    
    st.markdown("### 👥 User Management")
    st.info("🔧 User management features đang được phát triển...")

def render_system_monitor():
    """Render system monitoring panel"""
    st.markdown("### 📋 System Monitor")
    st.info("🔧 System monitoring features đang được phát triển...")

def render_security_panel():
    """Render security management panel"""
    if not admin_auth.has_permission("all"):
        st.error("❌ Bạn không có quyền truy cập bảo mật")
        return
    
    st.markdown("### 🔐 Security Management")
    st.info("🔧 Security management features đang được phát triển...")

def render_admin_settings():
    """Render admin settings panel"""
    if not admin_auth.has_permission("all"):
        st.error("❌ Bạn không có quyền cài đặt hệ thống")
        return
    
    st.markdown("### ⚙️ Admin Settings")
    st.info("🔧 Admin settings đang được phát triển...")

if __name__ == "__main__":
    main()
