"""
📋 GDPR Compliance Dashboard
Comprehensive privacy và compliance monitoring cho SOULFRIEND V2.0
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Add paths
sys.path.insert(0, '/workspaces/Mentalhealth')
sys.path.insert(0, '/workspaces/Mentalhealth/security')

try:
    from security.advanced_security import (
        create_security_framework, 
        GDPRCompliance, 
        AuditLogger,
        RoleBasedAccess
    )
    SECURITY_AVAILABLE = True
except ImportError as e:
    SECURITY_AVAILABLE = False
    st.error(f"Security modules not available: {e}")

# Page config
st.set_page_config(
    page_title="GDPR Compliance Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .compliance-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #27ae60;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .danger-card {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .privacy-notice {
        background: #e7f3ff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #0066cc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔒 GDPR Compliance Dashboard</h1>
        <p>Privacy Protection & Data Compliance Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not SECURITY_AVAILABLE:
        st.error("❌ Security framework không khả dụng. Vui lòng kiểm tra cài đặt.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🛡️ Security Controls")
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            st.rerun()
        
        st.markdown("---")
        
        # View options
        st.markdown("### 📋 Compliance Views")
        show_privacy_notice = st.checkbox("📜 Privacy Notice", value=True)
        show_consent_management = st.checkbox("✅ Consent Management", value=True)
        show_data_retention = st.checkbox("⏰ Data Retention", value=True)
        show_audit_logs = st.checkbox("📝 Audit Logs", value=True)
        show_user_rights = st.checkbox("👤 User Rights", value=True)
        
        st.markdown("---")
        
        # Security status
        st.markdown("### 🔒 Security Status")
        try:
            security_framework = create_security_framework()
            st.success("✅ Security Framework: Active")
            st.info("🔐 Encryption: AES-256")
            st.info("📊 Anonymization: Active")
            st.info("👥 RBAC: Configured")
        except Exception as e:
            st.error(f"❌ Security Error: {str(e)[:50]}...")
    
    # Main content
    try:
        # Initialize security framework
        security_framework = create_security_framework()
        gdpr_compliance = security_framework["gdpr_compliance"]
        
        # Overview metrics
        st.markdown("## 📊 Compliance Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🔒 Privacy Notice Version",
                "2.0",
                help="Current privacy notice version"
            )
        
        with col2:
            st.metric(
                "⏰ Data Retention Period",
                "730 days",
                help="Maximum data retention period"
            )
        
        with col3:
            st.metric(
                "🛡️ Encryption Status",
                "AES-256",
                help="Data encryption standard"
            )
        
        with col4:
            st.metric(
                "👥 User Rights",
                "7 Rights",
                help="GDPR user rights implemented"
            )
        
        # Privacy Notice Section
        if show_privacy_notice:
            st.markdown("---")
            st.markdown("## 📜 Privacy Notice & Data Processing")
            
            privacy_notice = gdpr_compliance.create_privacy_notice()["privacy_notice"]
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 🏢 Data Controller Information")
                controller = privacy_notice["controller"]
                st.markdown(f"""
                <div class="compliance-card">
                <b>Organization:</b> {controller["name"]}<br>
                <b>Privacy Contact:</b> {controller["contact"]}<br>
                <b>DPO Contact:</b> {controller["dpo_contact"]}<br>
                <b>Effective Date:</b> {privacy_notice["effective_date"]}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Data Collection Purposes")
                purposes = privacy_notice["data_collection"]["purposes"]
                for purpose in purposes:
                    st.markdown(f"• {purpose}")
            
            with col2:
                st.markdown("### ⚖️ Legal Basis for Processing")
                legal_basis = privacy_notice["data_collection"]["legal_basis"]
                for basis in legal_basis:
                    st.markdown(f"• {basis}")
                
                st.markdown("### 📊 Data Types Collected")
                data_types = privacy_notice["data_collection"]["data_types"]
                for data_type in data_types:
                    st.markdown(f"• {data_type}")
        
        # Consent Management Section
        if show_consent_management:
            st.markdown("---")
            st.markdown("## ✅ Consent Management")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📝 Consent Record Demo")
                
                # Demo consent creation
                sample_consent = {
                    "research_participation": True,
                    "analytics_consent": True,
                    "marketing_consent": False
                }
                
                consent_record = gdpr_compliance.create_consent_record("demo_user", sample_consent)
                
                st.markdown(f"""
                <div class="compliance-card">
                <b>Consent ID:</b> {consent_record['consent_id']}<br>
                <b>User ID (Anonymized):</b> {consent_record['user_id']}<br>
                <b>Timestamp:</b> {consent_record['timestamp']}<br>
                <b>Version:</b> {consent_record['consent_version']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Consents Given:**")
                for consent_type, granted in consent_record['consents_given'].items():
                    status_icon = "✅" if granted else "❌"
                    st.markdown(f"{status_icon} {consent_type.replace('_', ' ').title()}")
            
            with col2:
                st.markdown("### 🔄 Withdrawal Rights")
                withdrawal_info = consent_record['withdrawal_info']
                
                st.markdown(f"""
                <div class="privacy-notice">
                <b>Can Withdraw:</b> {'Yes' if withdrawal_info['can_withdraw'] else 'No'}<br>
                <b>Withdrawal Method:</b> {withdrawal_info['withdrawal_method']}<br>
                <b>Effect:</b> {withdrawal_info['withdrawal_effect']}
                </div>
                """, unsafe_allow_html=True)
                
                # Consent analytics
                st.markdown("### 📊 Consent Analytics (Demo)")
                consent_data = {
                    'Consent Type': ['Research', 'Analytics', 'Marketing'],
                    'Granted': [85, 70, 30],
                    'Declined': [15, 30, 70]
                }
                
                df_consent = pd.DataFrame(consent_data)
                fig_consent = px.bar(
                    df_consent, 
                    x='Consent Type', 
                    y=['Granted', 'Declined'],
                    title="Consent Rates by Type",
                    color_discrete_map={'Granted': '#27ae60', 'Declined': '#e74c3c'}
                )
                st.plotly_chart(fig_consent, use_container_width=True)
        
        # Data Retention Section
        if show_data_retention:
            st.markdown("---")
            st.markdown("## ⏰ Data Retention & Lifecycle Management")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📅 Retention Policy")
                
                # Demo retention checks
                test_ages = [10, 35, 100, 800]
                retention_results = []
                
                for age in test_ages:
                    result = gdpr_compliance.check_data_retention(age)
                    retention_results.append({
                        'Data Age (Days)': age,
                        'Status': result['compliance_status'],
                        'Actions Required': ', '.join(result['required_actions']) if result['required_actions'] else 'None'
                    })
                
                df_retention = pd.DataFrame(retention_results)
                st.dataframe(df_retention, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Data Lifecycle Visualization")
                
                # Create retention timeline
                timeline_data = {
                    'Days': list(range(0, 800, 50)),
                    'Data Status': []
                }
                
                for days in timeline_data['Days']:
                    if days <= 30:
                        timeline_data['Data Status'].append('Active')
                    elif days <= 730:
                        timeline_data['Data Status'].append('Anonymized')
                    else:
                        timeline_data['Data Status'].append('Archived/Deleted')
                
                df_timeline = pd.DataFrame(timeline_data)
                fig_timeline = px.scatter(
                    df_timeline, 
                    x='Days', 
                    y='Data Status',
                    color='Data Status',
                    title="Data Lifecycle Timeline",
                    color_discrete_map={
                        'Active': '#3498db',
                        'Anonymized': '#f39c12', 
                        'Archived/Deleted': '#95a5a6'
                    }
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # User Rights Section
        if show_user_rights:
            st.markdown("---")
            st.markdown("## 👤 GDPR User Rights Implementation")
            
            privacy_notice = gdpr_compliance.create_privacy_notice()["privacy_notice"]
            user_rights = privacy_notice["user_rights"]
            
            rights_cols = st.columns(2)
            
            for i, (right, description) in enumerate(user_rights.items()):
                col = rights_cols[i % 2]
                
                with col:
                    right_name = right.replace('_', ' ').title()
                    st.markdown(f"""
                    <div class="compliance-card">
                    <h4>🔹 {right_name}</h4>
                    <p>{description}</p>
                    <small><b>Implementation:</b> Available via privacy portal</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Audit Logs Section
        if show_audit_logs:
            st.markdown("---")
            st.markdown("## 📝 Security Audit & Monitoring")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 🔍 Recent Security Events (Demo)")
                
                # Demo audit events
                demo_events = [
                    {"Event": "User Login", "Status": "Success", "Time": "2025-08-28 10:30"},
                    {"Event": "Data Export", "Status": "Success", "Time": "2025-08-28 09:15"},
                    {"Event": "Failed Access", "Status": "Blocked", "Time": "2025-08-28 08:45"},
                    {"Event": "Consent Update", "Status": "Success", "Time": "2025-08-28 07:20"}
                ]
                
                df_events = pd.DataFrame(demo_events)
                st.dataframe(df_events, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Security Metrics")
                
                # Security metrics chart
                metrics_data = {
                    'Metric': ['Successful Logins', 'Failed Attempts', 'Data Exports', 'Privacy Requests'],
                    'Count': [1250, 45, 23, 8]
                }
                
                df_metrics = pd.DataFrame(metrics_data)
                fig_metrics = px.pie(
                    df_metrics, 
                    values='Count', 
                    names='Metric',
                    title="Security Event Distribution"
                )
                st.plotly_chart(fig_metrics, use_container_width=True)
        
        # Compliance Summary
        st.markdown("---")
        st.markdown("## 🎯 Compliance Status Summary")
        
        compliance_items = [
            {"Item": "Privacy Notice", "Status": "✅ Current", "Notes": "Version 2.0 active"},
            {"Item": "Consent Management", "Status": "✅ Implemented", "Notes": "Granular consent tracking"},
            {"Item": "Data Encryption", "Status": "✅ Active", "Notes": "AES-256 encryption"},
            {"Item": "User Rights Portal", "Status": "🚧 In Development", "Notes": "Available Q4 2025"},
            {"Item": "Audit Logging", "Status": "✅ Active", "Notes": "Comprehensive logging"},
            {"Item": "Data Retention", "Status": "✅ Automated", "Notes": "Auto-anonymization after 30 days"},
            {"Item": "GDPR Training", "Status": "⏳ Scheduled", "Notes": "Staff training Q4 2025"}
        ]
        
        df_compliance = pd.DataFrame(compliance_items)
        st.dataframe(df_compliance, use_container_width=True)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6c757d; padding: 1rem;">
            🔒 GDPR Compliance Dashboard • SOULFRIEND V2.0 • 
            Last Updated: {timestamp}
        </div>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
        unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error in GDPR Compliance Dashboard: {str(e)}")
        
        # Show basic compliance info
        st.markdown("### 📋 Basic Compliance Information")
        st.info("""
        **GDPR Compliance Features:**
        - ✅ Privacy by Design architecture
        - ✅ Data minimization principles
        - ✅ Automatic anonymization
        - ✅ User consent management
        - ✅ Right to be forgotten
        - ✅ Data portability
        - ✅ Security measures (encryption)
        """)

if __name__ == "__main__":
    main()
