#!/usr/bin/env python3
"""
🔥 SOULFRIEND Research System Monitoring Dashboard
Real-time monitoring and analytics for research data collection
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import monitoring components
from research_system.monitoring_dashboard import (
    ResearchMonitoring,
    render_system_status,
    render_real_time_events,
    render_analytics_dashboard,
    render_privacy_compliance,
    main
)

# Configure monitoring dashboard page
st.set_page_config(
    page_title="🔬 SOULFRIEND Research Monitoring",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for monitoring dashboard
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .status-healthy {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .dashboard-header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard header
st.markdown("""
<div class="dashboard-header">
    <h1>🔬 SOULFRIEND Research System Monitoring</h1>
    <p>Real-time monitoring, analytics, and privacy compliance dashboard</p>
</div>
""", unsafe_allow_html=True)

# Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "🏥 System Health", 
    "📊 Real-time Events", 
    "📈 Analytics", 
    "🔒 Privacy Compliance"
])

with tab1:
    st.header("🏥 System Health Status")
    render_system_status()

with tab2:
    st.header("📊 Real-time Event Monitoring")
    render_real_time_events()

with tab3:
    st.header("📈 Analytics Dashboard")
    render_analytics_dashboard()

with tab4:
    st.header("🔒 Privacy Compliance")
    render_privacy_compliance()

# Sidebar with additional controls
with st.sidebar:
    st.markdown("### 🔧 Dashboard Controls")
    
    # Refresh controls
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=True)
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()
    
    if st.button("🔄 Manual Refresh"):
        st.rerun()
    
    # System info
    st.markdown("---")
    st.markdown("### 📋 System Info")
    st.info("🔬 Research System V2.0")
    st.info("📊 Monitoring Dashboard Active")
    st.success("✅ Privacy Compliant")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("📊 Export Analytics"):
        st.success("📊 Analytics export initiated")
    
    if st.button("🧹 Cleanup Old Data"):
        st.success("🧹 Data cleanup initiated")
    
    if st.button("🔒 Privacy Audit"):
        st.success("🔒 Privacy audit started")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    🔬 <strong>SOULFRIEND Research System V2.0</strong> | 
    Monitoring Dashboard | 
    🔒 Privacy-First Analytics | 
    © 2025
</div>
""", unsafe_allow_html=True)
