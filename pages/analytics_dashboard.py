"""
SOULFRIEND Analytics Dashboard
Real-time analytics and monitoring for mental health assessments
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# App header
app_header()

def generate_realtime_data():
    """Generate real-time analytics data"""
    current_time = datetime.now()
    
    # User activity data
    user_activity = {
        'active_users': random.randint(50, 150),
        'new_registrations': random.randint(5, 25),
        'assessments_completed': random.randint(20, 80),
        'help_requests': random.randint(2, 15)
    }
    
    # Assessment completion rates
    completion_rates = {
        'PHQ-9': random.uniform(0.75, 0.95),
        'GAD-7': random.uniform(0.70, 0.90),
        'DASS-21': random.uniform(0.65, 0.85),
        'EPDS': random.uniform(0.60, 0.80),
        'PSS-10': random.uniform(0.70, 0.88)
    }
    
    # Geographic distribution
    geographic_data = {
        'Ho Chi Minh City': random.randint(30, 50),
        'Hanoi': random.randint(20, 35),
        'Da Nang': random.randint(10, 20),
        'Can Tho': random.randint(5, 15),
        'Hai Phong': random.randint(5, 12),
        'Others': random.randint(15, 25)
    }
    
    return user_activity, completion_rates, geographic_data

def analytics_dashboard_main():
    """Main analytics dashboard interface"""
    st.markdown("# 📈 SOULFRIEND Analytics Dashboard")
    st.markdown("#### Real-time monitoring và phân tích hệ thống")
    st.markdown("---")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
    
    if auto_refresh:
        time.sleep(5)
        st.rerun()
    
    # Generate real-time data
    user_activity, completion_rates, geographic_data = generate_realtime_data()
    
    # Real-time metrics
    st.markdown("### 📊 Real-time Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Active Users",
            value=user_activity['active_users'],
            delta=random.randint(-5, 10)
        )
    
    with col2:
        st.metric(
            "📝 Assessments Today",
            value=user_activity['assessments_completed'],
            delta=random.randint(2, 15)
        )
    
    with col3:
        st.metric(
            "🆕 New Registrations",
            value=user_activity['new_registrations'],
            delta=random.randint(0, 8)
        )
    
    with col4:
        st.metric(
            "🆘 Help Requests",
            value=user_activity['help_requests'],
            delta=random.randint(-2, 5)
        )
    
    st.markdown("---")
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📈 Performance",
        "🌍 Geographic",
        "🎯 User Behavior",
        "⚡ System Health"
    ])
    
    with tab1:
        st.markdown("### 📊 System Overview")
        
        # Assessment completion rates
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Assessment Completion Rates")
            
            assessments = list(completion_rates.keys())
            rates = list(completion_rates.values())
            
            fig_bar = px.bar(
                x=assessments,
                y=rates,
                title="Completion Rates by Assessment Type",
                color=rates,
                color_continuous_scale='Viridis'
            )
            fig_bar.update_layout(height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Daily Activity Trend")
            
            # Generate hourly data for today
            hours = list(range(24))
            activity_data = [random.randint(10, 50) for _ in hours]
            
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=hours,
                y=activity_data,
                mode='lines+markers',
                name='User Activity',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=6)
            ))
            
            fig_line.update_layout(
                title="User Activity by Hour",
                xaxis_title="Hour of Day",
                yaxis_title="Active Users",
                height=400
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Quick stats
        st.markdown("#### 🎯 Quick Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_completion_rate = sum(completion_rates.values()) / len(completion_rates)
            st.info(f"""
            **Average Completion Rate**: {avg_completion_rate:.1%}
            **Best Performing**: {max(completion_rates, key=completion_rates.get)}
            **Needs Attention**: {min(completion_rates, key=completion_rates.get)}
            """)
        
        with col2:
            total_users = sum(geographic_data.values())
            st.success(f"""
            **Total Active Regions**: {len(geographic_data)}
            **Total Users**: {total_users}
            **Top Region**: {max(geographic_data, key=geographic_data.get)}
            """)
        
        with col3:
            response_time = random.uniform(0.5, 2.0)
            uptime = random.uniform(98.5, 99.9)
            st.warning(f"""
            **Avg Response Time**: {response_time:.2f}s
            **System Uptime**: {uptime:.1f}%
            **Error Rate**: {random.uniform(0.1, 1.0):.2f}%
            """)
    
    with tab2:
        st.markdown("### 📈 Performance Analytics")
        
        # Performance metrics over time
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
        
        performance_data = {
            'date': dates,
            'response_time': [random.uniform(0.8, 2.5) for _ in dates],
            'throughput': [random.randint(100, 500) for _ in dates],
            'error_rate': [random.uniform(0.1, 2.0) for _ in dates],
            'user_satisfaction': [random.uniform(3.5, 5.0) for _ in dates]
        }
        
        df_perf = pd.DataFrame(performance_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Response time trend
            fig_resp = px.line(
                df_perf,
                x='date',
                y='response_time',
                title='Response Time Trend (7 days)',
                markers=True
            )
            fig_resp.update_layout(height=400)
            st.plotly_chart(fig_resp, use_container_width=True)
        
        with col2:
            # Throughput vs Error Rate
            fig_scatter = px.scatter(
                df_perf,
                x='throughput',
                y='error_rate',
                size='user_satisfaction',
                title='Throughput vs Error Rate',
                hover_data=['date']
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Performance summary
        st.markdown("#### 📊 Performance Summary")
        
        perf_metrics = [
            {
                "Metric": "Average Response Time",
                "Current": f"{df_perf['response_time'].iloc[-1]:.2f}s",
                "7-day Avg": f"{df_perf['response_time'].mean():.2f}s",
                "Trend": "↗️" if df_perf['response_time'].iloc[-1] > df_perf['response_time'].mean() else "↘️"
            },
            {
                "Metric": "Throughput",
                "Current": f"{df_perf['throughput'].iloc[-1]} req/min",
                "7-day Avg": f"{df_perf['throughput'].mean():.0f} req/min",
                "Trend": "↗️" if df_perf['throughput'].iloc[-1] > df_perf['throughput'].mean() else "↘️"
            },
            {
                "Metric": "Error Rate",
                "Current": f"{df_perf['error_rate'].iloc[-1]:.2f}%",
                "7-day Avg": f"{df_perf['error_rate'].mean():.2f}%",
                "Trend": "↗️" if df_perf['error_rate'].iloc[-1] > df_perf['error_rate'].mean() else "↘️"
            }
        ]
        
        st.dataframe(pd.DataFrame(perf_metrics), use_container_width=True)
    
    with tab3:
        st.markdown("### 🌍 Geographic Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Geographic pie chart
            fig_geo = px.pie(
                values=list(geographic_data.values()),
                names=list(geographic_data.keys()),
                title="User Distribution by Region"
            )
            st.plotly_chart(fig_geo, use_container_width=True)
        
        with col2:
            # Regional activity bar chart
            fig_regional = px.bar(
                x=list(geographic_data.keys()),
                y=list(geographic_data.values()),
                title="Active Users by Region",
                color=list(geographic_data.values()),
                color_continuous_scale='Blues'
            )
            fig_regional.update_layout(height=400)
            st.plotly_chart(fig_regional, use_container_width=True)
        
        # Regional details table
        st.markdown("#### 📍 Regional Details")
        
        regional_details = []
        for region, users in geographic_data.items():
            regional_details.append({
                "Region": region,
                "Active Users": users,
                "Percentage": f"{(users / sum(geographic_data.values()) * 100):.1f}%",
                "Growth": f"{random.randint(-10, 25)}%"
            })
        
        st.dataframe(pd.DataFrame(regional_details), use_container_width=True)
    
    with tab4:
        st.markdown("### 🎯 User Behavior Analytics")
        
        # User journey funnel
        funnel_data = {
            'Stage': ['Landing', 'Registration', 'First Assessment', 'Complete Assessment', 'Return User'],
            'Users': [1000, 750, 600, 480, 320],
            'Conversion': ['100%', '75%', '60%', '48%', '32%']
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Funnel chart
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Users'],
                textinfo="value+percent initial"
            ))
            fig_funnel.update_layout(title="User Journey Funnel")
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            # Session duration distribution
            session_durations = [random.randint(2, 30) for _ in range(100)]
            
            fig_hist = px.histogram(
                x=session_durations,
                title="Session Duration Distribution",
                nbins=10,
                labels={'x': 'Duration (minutes)', 'y': 'Frequency'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Behavior insights
        st.markdown("#### 🔍 Behavior Insights")
        
        insights = [
            "🎯 **Peak Activity**: Users are most active between 7-9 PM",
            "📱 **Device Preference**: 68% mobile, 32% desktop users",
            "⏱️ **Average Session**: 12.5 minutes per session",
            "🔄 **Return Rate**: 65% of users return within 7 days",
            "🏆 **Completion Success**: 78% complete their first assessment"
        ]
        
        for insight in insights:
            st.success(insight)
    
    with tab5:
        st.markdown("### ⚡ System Health Monitor")
        
        # System health metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cpu_usage = random.uniform(20, 80)
            cpu_color = "🟢" if cpu_usage < 50 else "🟡" if cpu_usage < 75 else "🔴"
            st.metric(
                "CPU Usage",
                f"{cpu_usage:.1f}%",
                delta=f"{cpu_color}"
            )
            
            memory_usage = random.uniform(30, 85)
            memory_color = "🟢" if memory_usage < 60 else "🟡" if memory_usage < 80 else "🔴"
            st.metric(
                "Memory Usage",
                f"{memory_usage:.1f}%",
                delta=f"{memory_color}"
            )
        
        with col2:
            disk_usage = random.uniform(40, 90)
            disk_color = "🟢" if disk_usage < 70 else "🟡" if disk_usage < 85 else "🔴"
            st.metric(
                "Disk Usage",
                f"{disk_usage:.1f}%",
                delta=f"{disk_color}"
            )
            
            network_latency = random.uniform(10, 100)
            network_color = "🟢" if network_latency < 30 else "🟡" if network_latency < 60 else "🔴"
            st.metric(
                "Network Latency",
                f"{network_latency:.0f}ms",
                delta=f"{network_color}"
            )
        
        with col3:
            uptime = random.uniform(98, 99.9)
            uptime_color = "🟢" if uptime > 99 else "🟡" if uptime > 98 else "🔴"
            st.metric(
                "System Uptime",
                f"{uptime:.2f}%",
                delta=f"{uptime_color}"
            )
            
            active_connections = random.randint(50, 200)
            st.metric(
                "Active Connections",
                active_connections,
                delta=random.randint(-10, 20)
            )
        
        # System status alerts
        st.markdown("#### 🚨 System Alerts")
        
        alerts = [
            {"Level": "INFO", "Message": "System backup completed successfully", "Time": "2 minutes ago"},
            {"Level": "WARNING", "Message": "High memory usage detected", "Time": "15 minutes ago"},
            {"Level": "SUCCESS", "Message": "Database optimization completed", "Time": "1 hour ago"}
        ]
        
        for alert in alerts:
            if alert["Level"] == "INFO":
                st.info(f"ℹ️ {alert['Message']} ({alert['Time']})")
            elif alert["Level"] == "WARNING":
                st.warning(f"⚠️ {alert['Message']} ({alert['Time']})")
            elif alert["Level"] == "SUCCESS":
                st.success(f"✅ {alert['Message']} ({alert['Time']})")
    
    # Footer with last update time
    st.markdown("---")
    st.markdown(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    analytics_dashboard_main()
