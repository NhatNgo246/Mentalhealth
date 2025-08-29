"""
SOULFRIEND AI Intelligence Platform
Advanced AI-driven mental health assessment and recommendations
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ai_insights import ai_insights_dashboard
from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    load_css()
except:
    pass

# Header
app_header()

# AI Platform
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 15px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">
        🤖 SOULFRIEND AI Intelligence
    </h1>
    <p style="color: white; text-align: center; margin: 10px 0 0 0; font-size: 1.2em;">
        Trí tuệ nhân tạo hỗ trợ sức khỏe tâm thần
    </p>
</div>
""", unsafe_allow_html=True)

# AI Dashboard
ai_insights_dashboard()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.caption("🤖 SOULFRIEND AI Platform - Powered by Machine Learning")

with col2:
    if st.button("📊 Dashboard", key="dashboard_access"):
        st.switch_page("analytics_dashboard.py")

with col3:
    if st.button("🏠 Trang chính", key="main_access"):
        st.switch_page("SOULFRIEND.py")
