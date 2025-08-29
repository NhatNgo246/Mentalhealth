"""
SOULFRIEND Advanced Reports
Comprehensive reporting and analytics for mental health assessments
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Advanced Reports",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# App header
app_header()

def generate_sample_data():
    """Generate sample assessment data for demonstration"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    data = []
    for date in dates:
        data.append({
            'date': date,
            'phq9_score': random.randint(5, 25),
            'gad7_score': random.randint(3, 20),
            'dass21_depression': random.randint(0, 42),
            'dass21_anxiety': random.randint(0, 42),
            'dass21_stress': random.randint(0, 42),
            'epds_score': random.randint(0, 25),
            'pss10_score': random.randint(0, 40),
            'user_id': f"user_{random.randint(1, 100)}"
        })
    
    return pd.DataFrame(data)

def advanced_reports_main():
    """Main advanced reports interface"""
    st.markdown("# 📊 SOULFRIEND Advanced Reports")
    st.markdown("#### Báo cáo chuyên sâu và phân tích dữ liệu sức khỏe tâm lý")
    st.markdown("---")
    
    # Generate sample data
    df = generate_sample_data()
    
    # Tabs for different report types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Trend Analysis",
        "📊 Statistical Overview", 
        "👥 Population Analysis",
        "🔍 Detailed Insights",
        "📝 Custom Reports"
    ])
    
    with tab1:
        st.markdown("### 📈 Phân tích xu hướng theo thời gian")
        
        # Time series chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df['phq9_score'].rolling(window=7).mean(),
            mode='lines+markers',
            name='PHQ-9 (7-day avg)',
            line=dict(color='#FF6B6B', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df['gad7_score'].rolling(window=7).mean(),
            mode='lines+markers',
            name='GAD-7 (7-day avg)',
            line=dict(color='#4ECDC4', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df['pss10_score'].rolling(window=7).mean(),
            mode='lines+markers',
            name='PSS-10 (7-day avg)',
            line=dict(color='#45B7D1', width=3)
        ))
        
        fig.update_layout(
            title="Mental Health Score Trends (30 days)",
            xaxis_title="Date",
            yaxis_title="Average Score",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_phq9 = df['phq9_score'].mean()
            trend_phq9 = "↗️" if df['phq9_score'].iloc[-1] > df['phq9_score'].iloc[0] else "↘️"
            st.metric(
                "PHQ-9 Average", 
                f"{avg_phq9:.1f}", 
                f"{trend_phq9} {abs(df['phq9_score'].iloc[-1] - df['phq9_score'].iloc[0]):.1f}"
            )
        
        with col2:
            avg_gad7 = df['gad7_score'].mean()
            trend_gad7 = "↗️" if df['gad7_score'].iloc[-1] > df['gad7_score'].iloc[0] else "↘️"
            st.metric(
                "GAD-7 Average", 
                f"{avg_gad7:.1f}", 
                f"{trend_gad7} {abs(df['gad7_score'].iloc[-1] - df['gad7_score'].iloc[0]):.1f}"
            )
        
        with col3:
            avg_pss10 = df['pss10_score'].mean()
            trend_pss10 = "↗️" if df['pss10_score'].iloc[-1] > df['pss10_score'].iloc[0] else "↘️"
            st.metric(
                "PSS-10 Average", 
                f"{avg_pss10:.1f}", 
                f"{trend_pss10} {abs(df['pss10_score'].iloc[-1] - df['pss10_score'].iloc[0]):.1f}"
            )
    
    with tab2:
        st.markdown("### 📊 Tổng quan thống kê")
        
        # Distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            # PHQ-9 distribution
            fig_hist = px.histogram(
                df, 
                x='phq9_score', 
                title="PHQ-9 Score Distribution",
                color_discrete_sequence=['#FF6B6B']
            )
            fig_hist.update_layout(height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # GAD-7 distribution
            fig_hist2 = px.histogram(
                df, 
                x='gad7_score', 
                title="GAD-7 Score Distribution",
                color_discrete_sequence=['#4ECDC4']
            )
            fig_hist2.update_layout(height=400)
            st.plotly_chart(fig_hist2, use_container_width=True)
        
        # Correlation matrix
        st.markdown("#### 🔗 Correlation Analysis")
        
        corr_data = df[['phq9_score', 'gad7_score', 'dass21_depression', 'dass21_anxiety', 'dass21_stress', 'pss10_score']].corr()
        
        fig_corr = px.imshow(
            corr_data,
            title="Correlation Matrix between Assessment Scores",
            color_continuous_scale='RdYlBu_r',
            aspect='auto'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab3:
        st.markdown("### 👥 Phân tích dân số")
        
        # Risk level distribution
        def get_risk_level(score, scale='phq9'):
            if scale == 'phq9':
                if score <= 4: return "Minimal"
                elif score <= 9: return "Mild"
                elif score <= 14: return "Moderate"
                elif score <= 19: return "Moderately Severe"
                else: return "Severe"
            elif scale == 'gad7':
                if score <= 4: return "Minimal"
                elif score <= 9: return "Mild"
                elif score <= 14: return "Moderate"
                else: return "Severe"
        
        df['phq9_risk'] = df['phq9_score'].apply(lambda x: get_risk_level(x, 'phq9'))
        df['gad7_risk'] = df['gad7_score'].apply(lambda x: get_risk_level(x, 'gad7'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # PHQ-9 risk distribution
            phq9_risk_counts = df['phq9_risk'].value_counts()
            fig_pie1 = px.pie(
                values=phq9_risk_counts.values,
                names=phq9_risk_counts.index,
                title="PHQ-9 Risk Level Distribution"
            )
            st.plotly_chart(fig_pie1, use_container_width=True)
        
        with col2:
            # GAD-7 risk distribution
            gad7_risk_counts = df['gad7_risk'].value_counts()
            fig_pie2 = px.pie(
                values=gad7_risk_counts.values,
                names=gad7_risk_counts.index,
                title="GAD-7 Risk Level Distribution"
            )
            st.plotly_chart(fig_pie2, use_container_width=True)
        
        # Summary statistics
        st.markdown("#### 📋 Summary Statistics")
        
        summary_stats = df[['phq9_score', 'gad7_score', 'dass21_depression', 'dass21_anxiety', 'dass21_stress']].describe()
        st.dataframe(summary_stats, use_container_width=True)
    
    with tab4:
        st.markdown("### 🔍 Chi tiết insights")
        
        # Advanced insights
        st.markdown("#### 🎯 Key Findings")
        
        insights = [
            f"🔸 **Highest Risk Period**: {df.loc[df['phq9_score'].idxmax(), 'date'].strftime('%Y-%m-%d')} (PHQ-9: {df['phq9_score'].max()})",
            f"🔸 **Best Mental Health Day**: {df.loc[df['phq9_score'].idxmin(), 'date'].strftime('%Y-%m-%d')} (PHQ-9: {df['phq9_score'].min()})",
            f"🔸 **Average Assessment Frequency**: {len(df) / 30:.1f} assessments per day",
            f"🔸 **Improvement Rate**: {((df['phq9_score'].iloc[:15].mean() - df['phq9_score'].iloc[-15:].mean()) / df['phq9_score'].iloc[:15].mean() * 100):.1f}% change in recent 15 days"
        ]
        
        for insight in insights:
            st.success(insight)
        
        # Predictive indicators
        st.markdown("#### 🔮 Predictive Indicators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Risk Factors:**")
            st.warning("⚠️ Consistent high stress scores (PSS-10 > 20)")
            st.warning("⚠️ Increasing anxiety trend")
            st.warning("⚠️ Sleep quality correlation with depression")
        
        with col2:
            st.markdown("**Protective Factors:**")
            st.success("✅ Regular assessment completion")
            st.success("✅ Declining overall severity trend")
            st.success("✅ Engagement with support resources")
    
    with tab5:
        st.markdown("### 📝 Custom Reports")
        
        st.markdown("#### 🛠️ Report Generator")
        
        # Custom report options
        col1, col2 = st.columns(2)
        
        with col1:
            date_range = st.date_input(
                "Select Date Range",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
            
            selected_assessments = st.multiselect(
                "Select Assessments",
                ["PHQ-9", "GAD-7", "DASS-21", "EPDS", "PSS-10"],
                default=["PHQ-9", "GAD-7"]
            )
        
        with col2:
            report_type = st.selectbox(
                "Report Type",
                ["Summary Report", "Detailed Analysis", "Trend Report", "Risk Assessment"]
            )
            
            export_format = st.selectbox(
                "Export Format",
                ["PDF", "Excel", "CSV", "JSON"]
            )
        
        if st.button("📋 Generate Custom Report", type="primary"):
            with st.spinner("🔄 Generating custom report..."):
                st.success("✅ Custom report generated successfully!")
                
                # Mock report preview
                st.markdown("#### 📄 Report Preview")
                st.info(f"""
                **Report Type**: {report_type}
                **Date Range**: {date_range[0] if len(date_range) > 0 else 'N/A'} to {date_range[1] if len(date_range) > 1 else 'N/A'}
                **Assessments**: {', '.join(selected_assessments)}
                **Export Format**: {export_format}
                
                📊 This report contains comprehensive analysis of selected mental health assessments within the specified timeframe.
                """)
                
                if st.button("📥 Download Report"):
                    st.success(f"✅ Report downloaded as {export_format} format!")

if __name__ == "__main__":
    advanced_reports_main()
