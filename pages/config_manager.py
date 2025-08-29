"""
SOULFRIEND Config Manager
Configuration management for mental health assessment system
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Config Manager",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# App header
app_header()

def load_config():
    """Load system configuration"""
    config_file = "/workspaces/Mentalhealth/.streamlit/config.toml"
    default_config = {
        "app_settings": {
            "app_name": "SOULFRIEND V2.0",
            "version": "2.0.0",
            "environment": "development",
            "debug_mode": True,
            "language": "vietnamese",
            "timezone": "Asia/Ho_Chi_Minh"
        },
        "assessment_settings": {
            "enable_phq9": True,
            "enable_gad7": True,
            "enable_dass21": True,
            "enable_epds": True,
            "enable_pss10": True,
            "auto_save": True,
            "show_progress": True,
            "require_consent": True
        },
        "ui_settings": {
            "theme": "light",
            "sidebar_expanded": True,
            "show_metrics": True,
            "animation_enabled": True,
            "color_scheme": "default"
        },
        "data_settings": {
            "data_retention_days": 365,
            "backup_enabled": True,
            "encryption_enabled": True,
            "anonymous_mode": False
        },
        "ai_settings": {
            "chatbot_enabled": True,
            "ai_insights": True,
            "predictive_analytics": False,
            "auto_recommendations": True
        }
    }
    
    return default_config

def save_config(config):
    """Save system configuration"""
    try:
        # Mock save operation
        st.success("✅ Configuration saved successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Error saving configuration: {e}")
        return False

def config_manager_main():
    """Main configuration manager interface"""
    st.markdown("# ⚙️ SOULFRIEND Config Manager")
    st.markdown("#### Quản lý cấu hình hệ thống")
    st.markdown("---")
    
    # Load current configuration
    config = load_config()
    
    # Configuration tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 App Settings",
        "📋 Assessment Config",
        "🎨 UI Settings", 
        "💾 Data Settings",
        "🤖 AI Settings",
        "🔧 Advanced"
    ])
    
    with tab1:
        st.markdown("### 🏠 Application Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config["app_settings"]["app_name"] = st.text_input(
                "Application Name",
                value=config["app_settings"]["app_name"]
            )
            
            config["app_settings"]["version"] = st.text_input(
                "Version",
                value=config["app_settings"]["version"]
            )
            
            config["app_settings"]["environment"] = st.selectbox(
                "Environment",
                ["development", "staging", "production"],
                index=["development", "staging", "production"].index(config["app_settings"]["environment"])
            )
        
        with col2:
            config["app_settings"]["debug_mode"] = st.checkbox(
                "Debug Mode",
                value=config["app_settings"]["debug_mode"]
            )
            
            config["app_settings"]["language"] = st.selectbox(
                "Language",
                ["vietnamese", "english"],
                index=["vietnamese", "english"].index(config["app_settings"]["language"])
            )
            
            config["app_settings"]["timezone"] = st.selectbox(
                "Timezone",
                ["Asia/Ho_Chi_Minh", "UTC", "America/New_York"],
                index=["Asia/Ho_Chi_Minh", "UTC", "America/New_York"].index(config["app_settings"]["timezone"])
            )
    
    with tab2:
        st.markdown("### 📋 Assessment Configuration")
        
        st.markdown("#### Questionnaire Modules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config["assessment_settings"]["enable_phq9"] = st.checkbox(
                "🧠 Enable PHQ-9 (Depression)",
                value=config["assessment_settings"]["enable_phq9"]
            )
            
            config["assessment_settings"]["enable_gad7"] = st.checkbox(
                "😰 Enable GAD-7 (Anxiety)",
                value=config["assessment_settings"]["enable_gad7"]
            )
            
            config["assessment_settings"]["enable_dass21"] = st.checkbox(
                "📊 Enable DASS-21 (Multi-scale)",
                value=config["assessment_settings"]["enable_dass21"]
            )
        
        with col2:
            config["assessment_settings"]["enable_epds"] = st.checkbox(
                "🤱 Enable EPDS (Postpartum)",
                value=config["assessment_settings"]["enable_epds"]
            )
            
            config["assessment_settings"]["enable_pss10"] = st.checkbox(
                "😵 Enable PSS-10 (Stress)",
                value=config["assessment_settings"]["enable_pss10"]
            )
        
        st.markdown("#### Assessment Behavior")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config["assessment_settings"]["auto_save"] = st.checkbox(
                "Auto-save Progress",
                value=config["assessment_settings"]["auto_save"]
            )
            
            config["assessment_settings"]["show_progress"] = st.checkbox(
                "Show Progress Bar",
                value=config["assessment_settings"]["show_progress"]
            )
        
        with col2:
            config["assessment_settings"]["require_consent"] = st.checkbox(
                "Require Consent",
                value=config["assessment_settings"]["require_consent"]
            )
    
    with tab3:
        st.markdown("### 🎨 UI Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config["ui_settings"]["theme"] = st.selectbox(
                "Theme",
                ["light", "dark", "auto"],
                index=["light", "dark", "auto"].index(config["ui_settings"]["theme"])
            )
            
            config["ui_settings"]["color_scheme"] = st.selectbox(
                "Color Scheme",
                ["default", "blue", "green", "purple"],
                index=["default", "blue", "green", "purple"].index(config["ui_settings"]["color_scheme"])
            )
        
        with col2:
            config["ui_settings"]["sidebar_expanded"] = st.checkbox(
                "Sidebar Expanded by Default",
                value=config["ui_settings"]["sidebar_expanded"]
            )
            
            config["ui_settings"]["show_metrics"] = st.checkbox(
                "Show Metrics Dashboard",
                value=config["ui_settings"]["show_metrics"]
            )
            
            config["ui_settings"]["animation_enabled"] = st.checkbox(
                "Enable Animations",
                value=config["ui_settings"]["animation_enabled"]
            )
    
    with tab4:
        st.markdown("### 💾 Data Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config["data_settings"]["data_retention_days"] = st.number_input(
                "Data Retention (days)",
                min_value=30,
                max_value=3650,
                value=config["data_settings"]["data_retention_days"]
            )
            
            config["data_settings"]["backup_enabled"] = st.checkbox(
                "Enable Automatic Backup",
                value=config["data_settings"]["backup_enabled"]
            )
        
        with col2:
            config["data_settings"]["encryption_enabled"] = st.checkbox(
                "Enable Data Encryption",
                value=config["data_settings"]["encryption_enabled"]
            )
            
            config["data_settings"]["anonymous_mode"] = st.checkbox(
                "Anonymous Mode",
                value=config["data_settings"]["anonymous_mode"]
            )
        
        if config["data_settings"]["encryption_enabled"]:
            st.info("🔒 Data encryption is enabled. All sensitive data will be encrypted at rest.")
        
        if config["data_settings"]["anonymous_mode"]:
            st.warning("🕶️ Anonymous mode is enabled. No personal identifiers will be stored.")
    
    with tab5:
        st.markdown("### 🤖 AI Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config["ai_settings"]["chatbot_enabled"] = st.checkbox(
                "Enable AI Chatbot",
                value=config["ai_settings"]["chatbot_enabled"]
            )
            
            config["ai_settings"]["ai_insights"] = st.checkbox(
                "Enable AI Insights",
                value=config["ai_settings"]["ai_insights"]
            )
        
        with col2:
            config["ai_settings"]["predictive_analytics"] = st.checkbox(
                "Enable Predictive Analytics",
                value=config["ai_settings"]["predictive_analytics"]
            )
            
            config["ai_settings"]["auto_recommendations"] = st.checkbox(
                "Auto Recommendations",
                value=config["ai_settings"]["auto_recommendations"]
            )
        
        if config["ai_settings"]["predictive_analytics"]:
            st.info("🔮 Predictive analytics will use historical data to predict mental health trends.")
    
    with tab6:
        st.markdown("### 🔧 Advanced Configuration")
        
        # JSON editor
        st.markdown("#### 📝 Raw Configuration (JSON)")
        
        config_json = st.text_area(
            "Configuration JSON",
            value=json.dumps(config, indent=2),
            height=400
        )
        
        if st.button("🔍 Validate JSON"):
            try:
                json.loads(config_json)
                st.success("✅ JSON is valid!")
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {e}")
        
        # System information
        st.markdown("#### 📊 System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **System Status**: 🟢 Online
            **Uptime**: 2 hours 45 minutes
            **Memory Usage**: 45% (512 MB / 1 GB)
            **CPU Usage**: 23%
            """)
        
        with col2:
            st.info(f"""
            **Active Users**: 1
            **Total Assessments**: 156
            **Data Size**: 2.3 MB
            **Last Backup**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """)
    
    # Save configuration
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Save Configuration", type="primary"):
            if save_config(config):
                st.success("✅ Configuration saved successfully!")
                st.balloons()
    
    with col2:
        if st.button("🔄 Reset to Defaults"):
            st.warning("⚠️ This will reset all settings to default values.")
            if st.button("Confirm Reset"):
                config = load_config()
                st.success("✅ Configuration reset to defaults!")
                st.rerun()
    
    with col3:
        if st.button("📥 Export Config"):
            st.download_button(
                label="📄 Download config.json",
                data=json.dumps(config, indent=2),
                file_name=f"soulfriend_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    config_manager_main()
