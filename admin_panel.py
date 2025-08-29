"""
SOULFRIEND Admin Panel
Administrative interface for managing mental health assessment system
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.admin import admin_panel
from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Admin",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    load_css()
except:
    pass  # Continue without custom CSS if it fails

# Header
app_header()

# Admin Panel
admin_panel()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    🔧 <strong>SOULFRIEND Admin Panel</strong> | Phiên bản 2.0 | © 2025
</div>
""", unsafe_allow_html=True)
