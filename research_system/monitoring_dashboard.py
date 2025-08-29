"""
Real-time Research System Monitoring Dashboard
Dashboard Giám sát Hệ thống Nghiên cứu Thời gian Thực

Provides real-time monitoring and alerting for the research data collection system.
Cung cấp giám sát thời gian thực và cảnh báo cho hệ thống thu thập dữ liệu nghiên cứu.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import requests
from pathlib import Path
import logging
from typing import Dict, List, Any
import os

# Add research system to path
import sys
sys.path.append('/workspaces/Mentalhealth')
from research_system.analytics import ResearchAnalytics

class ResearchMonitoring:
    """Real-time monitoring for research system"""
    
    def __init__(self):
        self.analytics = ResearchAnalytics()
        self.api_base_url = "http://localhost:8502"
        
    def get_api_health(self) -> Dict[str, Any]:
        """Check research API health status"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=2)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "last_checked": datetime.now().isoformat()
            }
        except requests.RequestException:
            return {
                "status": "offline",
                "response_time_ms": None,
                "last_checked": datetime.now().isoformat()
            }
    
    def get_api_stats(self) -> Dict[str, Any]:
        """Get current API statistics"""
        try:
            response = requests.get(f"{self.api_base_url}/stats", timeout=2)
            if response.status_code == 200:
                return response.json()
            return {"error": "Could not fetch stats"}
        except requests.RequestException:
            return {"error": "API not available"}
    
    def get_recent_events(self, minutes: int = 60) -> pd.DataFrame:
        """Get recent events from the last N minutes"""
        df = self.analytics.load_collected_data(days_back=1)
        if df.empty:
            return df
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_df = df[df['timestamp'] >= cutoff_time]
        return recent_df.sort_values('timestamp', ascending=False)

def render_system_status():
    """Render system status section"""
    st.header("🔧 System Status")
    
    monitor = ResearchMonitoring()
    health = monitor.get_api_health()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_color = {"healthy": "🟢", "unhealthy": "🟡", "offline": "🔴"}
        st.metric(
            "API Status", 
            f"{status_color.get(health['status'], '⚪')} {health['status'].upper()}"
        )
    
    with col2:
        if health['response_time_ms']:
            st.metric("Response Time", f"{health['response_time_ms']:.1f} ms")
        else:
            st.metric("Response Time", "N/A")
    
    with col3:
        last_check = datetime.fromisoformat(health['last_checked'])
        st.metric("Last Check", last_check.strftime("%H:%M:%S"))
    
    # API Statistics
    stats = monitor.get_api_stats()
    if "error" not in stats:
        st.subheader("📊 API Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Events", stats.get('total_events', 0))
        with col2:
            st.metric("Today's Events", stats.get('events_today', 0))
        with col3:
            st.metric("Active Sessions", stats.get('active_sessions', 0))
        with col4:
            st.metric("Uptime", stats.get('uptime', 'Unknown'))

def render_real_time_events():
    """Render real-time events section"""
    st.header("⚡ Real-time Events")
    
    monitor = ResearchMonitoring()
    
    # Time range selector
    time_range = st.selectbox(
        "Time Range",
        [15, 30, 60, 120, 240],
        index=2,
        format_func=lambda x: f"Last {x} minutes"
    )
    
    # Get recent events
    recent_df = monitor.get_recent_events(minutes=time_range)
    
    if recent_df.empty:
        st.info(f"No events in the last {time_range} minutes")
        return
    
    # Events timeline
    fig = px.scatter(
        recent_df,
        x='timestamp',
        y='event_type',
        color='event_type',
        title=f"Events in Last {time_range} Minutes",
        hover_data=['session_id'] if 'session_id' in recent_df.columns else None
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent events table
    st.subheader("📋 Recent Events Detail")
    
    # Format the dataframe for display
    display_df = recent_df.copy()
    if 'timestamp' in display_df.columns:
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%H:%M:%S')
    
    # Show only relevant columns
    columns_to_show = ['timestamp', 'event_type', 'session_id']
    columns_to_show = [col for col in columns_to_show if col in display_df.columns]
    
    st.dataframe(
        display_df[columns_to_show].head(20),
        use_container_width=True
    )

def render_analytics_dashboard():
    """Render analytics dashboard"""
    st.header("📈 Analytics Dashboard")
    
    monitor = ResearchMonitoring()
    
    # Load data for analytics
    days_back = st.slider("Analysis Period (days)", 1, 30, 7)
    df = monitor.analytics.load_collected_data(days_back=days_back)
    
    if df.empty:
        st.warning(f"No data available for the last {days_back} days")
        return
    
    # Generate analytics
    usage_stats = monitor.analytics.generate_usage_statistics(df)
    behavior_patterns = monitor.analytics.analyze_user_behavior_patterns(df)
    
    # Overview metrics
    st.subheader("📊 Overview")
    overview = usage_stats.get('overview', {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", overview.get('total_events', 0))
    with col2:
        st.metric("Unique Sessions", overview.get('unique_sessions', 0))
    with col3:
        st.metric("Collection Days", overview.get('data_collection_days', 0))
    with col4:
        completion_rate = usage_stats.get('completion_rates', {}).get('completion_rate', 0)
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Event distribution chart
    if 'event_distribution' in usage_stats:
        st.subheader("📊 Event Distribution")
        event_dist = usage_stats['event_distribution']
        
        fig = px.pie(
            values=list(event_dist.values()),
            names=list(event_dist.keys()),
            title="Event Types Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Daily usage pattern
    if 'daily_usage' in usage_stats:
        st.subheader("📅 Daily Usage Pattern")
        daily_data = usage_stats['daily_usage']
        
        dates = list(daily_data.keys())
        counts = list(daily_data.values())
        
        fig = px.line(
            x=dates,
            y=counts,
            title="Daily Event Counts",
            labels={'x': 'Date', 'y': 'Event Count'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Hourly patterns
    if 'hourly_patterns' in usage_stats:
        st.subheader("🕐 Hourly Usage Patterns")
        hourly_data = usage_stats['hourly_patterns']
        
        fig = px.bar(
            x=list(hourly_data.keys()),
            y=list(hourly_data.values()),
            title="Events by Hour of Day",
            labels={'x': 'Hour', 'y': 'Event Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Session analysis
    if 'session_analysis' in usage_stats:
        st.subheader("👥 Session Analysis")
        session_data = usage_stats['session_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg Events/Session", f"{session_data.get('avg_events_per_session', 0):.1f}")
            st.metric("Max Events/Session", session_data.get('max_events_per_session', 0))
        with col2:
            st.metric("Min Events/Session", session_data.get('min_events_per_session', 0))
            st.metric("Total Sessions", session_data.get('total_sessions', 0))

def render_privacy_compliance():
    """Render privacy compliance section"""
    st.header("🔐 Privacy Compliance")
    
    monitor = ResearchMonitoring()
    df = monitor.analytics.load_collected_data(days_back=30)
    
    privacy_report = monitor.analytics.generate_privacy_compliance_report(df)
    
    # Overall status
    status = privacy_report.get('privacy_status', 'UNKNOWN')
    status_colors = {
        'COMPLIANT': '🟢',
        'NEEDS_REVIEW': '🟡',
        'ACTION_REQUIRED': '🔴'
    }
    
    st.metric(
        "Privacy Status",
        f"{status_colors.get(status, '⚪')} {status}"
    )
    
    # Detailed checks
    st.subheader("🔍 Compliance Checks")
    
    checks = privacy_report.get('checks_performed', [])
    for check in checks:
        with st.expander(f"{check['check_name']} - {check['status']}"):
            status_icon = {"PASS": "✅", "WARNING": "⚠️", "ACTION_REQUIRED": "🚨"}
            st.write(f"{status_icon.get(check['status'], '❓')} {check['details']}")
    
    # Data retention info
    if not df.empty and 'timestamp' in df.columns:
        st.subheader("📅 Data Retention")
        
        oldest_data = df['timestamp'].min()
        newest_data = df['timestamp'].max()
        data_span = (newest_data - oldest_data).days
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oldest Data", f"{(datetime.now() - oldest_data.to_pydatetime()).days} days ago")
        with col2:
            st.metric("Newest Data", f"{(datetime.now() - newest_data.to_pydatetime()).days} days ago")
        with col3:
            st.metric("Data Span", f"{data_span} days")

def main():
    """Main dashboard application"""
    st.set_page_config(
        page_title="Research System Monitor",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔬 Research System Monitoring Dashboard")
    st.markdown("Real-time monitoring and analytics for SOULFRIEND research data collection")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose Page",
        ["System Status", "Real-time Events", "Analytics", "Privacy Compliance"]
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
    
    if auto_refresh:
        time.sleep(30)
        st.experimental_rerun()
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.experimental_rerun()
    
    # Render selected page
    if page == "System Status":
        render_system_status()
    elif page == "Real-time Events":
        render_real_time_events()
    elif page == "Analytics":
        render_analytics_dashboard()
    elif page == "Privacy Compliance":
        render_privacy_compliance()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Research System Monitor v1.0**")
    st.sidebar.markdown(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
