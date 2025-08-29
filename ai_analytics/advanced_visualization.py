"""
🎨 Advanced Data Visualization Module
Interactive charts và dashboards cho SOULFRIEND Analytics
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class AdvancedVisualization:
    """
    Advanced visualization engine cho mental health analytics
    """
    
    def __init__(self):
        self.color_palette = {
            'low_risk': '#2E8B57',      # Sea Green
            'moderate_risk': '#FFD700',  # Gold
            'high_risk': '#FF6347',      # Tomato
            'very_high_risk': '#DC143C', # Crimson
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#17becf'
        }
    
    def create_risk_distribution_chart(self, cluster_analysis: Dict) -> go.Figure:
        """
        Tạo biểu đồ phân bố risk clusters
        """
        if not cluster_analysis or 'cluster_analysis' not in cluster_analysis:
            return self._create_empty_chart("No cluster data available")
        
        clusters = cluster_analysis['cluster_analysis']
        
        # Prepare data
        cluster_names = []
        sizes = []
        colors = []
        
        for cluster_id, data in clusters.items():
            risk_level = data.get('risk_level', 'unknown')
            cluster_names.append(f"{risk_level.replace('_', ' ').title()}<br>({data['size']} users)")
            sizes.append(data['percentage'])
            colors.append(self.color_palette.get(risk_level, '#gray'))
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=cluster_names,
            values=sizes,
            marker_colors=colors,
            hole=0.4,
            textinfo='label+percent',
            textfont_size=12,
            showlegend=True
        )])
        
        fig.update_layout(
            title={
                'text': "🎯 Risk Level Distribution",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50'}
            },
            font_family="Arial",
            width=500,
            height=400
        )
        
        return fig
    
    def create_trends_timeline(self, trends_data: Dict) -> go.Figure:
        """
        Tạo timeline chart cho trends analysis
        """
        if not trends_data or 'daily_assessment_counts' not in trends_data:
            return self._create_empty_chart("No trends data available")
        
        daily_counts = trends_data['daily_assessment_counts']
        
        # Convert to lists for plotting
        dates = list(daily_counts.keys())
        counts = list(daily_counts.values())
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=counts,
            mode='lines+markers',
            name='Daily Assessments',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=6, color=self.color_palette['primary']),
            hovertemplate='<b>Date:</b> %{x}<br><b>Assessments:</b> %{y}<extra></extra>'
        ))
        
        # Add trend line
        if len(counts) > 1:
            z = np.polyfit(range(len(counts)), counts, 1)
            trend_line = np.poly1d(z)(range(len(counts)))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=trend_line,
                mode='lines',
                name='Trend',
                line=dict(color=self.color_palette['secondary'], width=2, dash='dash'),
                hovertemplate='<b>Trend:</b> %{y:.1f}<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': "📈 Assessment Activity Trends",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50'}
            },
            xaxis_title="Date",
            yaxis_title="Number of Assessments",
            font_family="Arial",
            hovermode='x unified',
            width=700,
            height=400
        )
        
        return fig
    
    def create_hourly_heatmap(self, trends_data: Dict) -> go.Figure:
        """
        Tạo heatmap cho hourly patterns
        """
        if not trends_data or 'hourly_distribution' not in trends_data:
            return self._create_empty_chart("No hourly data available")
        
        hourly_dist = trends_data['hourly_distribution']
        
        # Prepare data for heatmap
        hours = list(range(24))
        values = [hourly_dist.get(hour, 0) for hour in hours]
        
        # Create matrix for heatmap (3 rows x 8 cols)
        matrix = np.array(values).reshape(3, 8)
        hour_labels = [f"{h:02d}:00" for h in hours]
        hour_matrix = np.array(hour_labels).reshape(3, 8)
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            text=hour_matrix,
            texttemplate="%{text}<br>%{z}",
            textfont={"size": 10},
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Assessments")
        ))
        
        fig.update_layout(
            title={
                'text': "🕐 Hourly Activity Heatmap",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50'}
            },
            width=600,
            height=300,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False)
        )
        
        return fig
    
    def create_risk_scores_radar(self, avg_scores: Dict) -> go.Figure:
        """
        Tạo radar chart cho risk scores comparison
        """
        if not avg_scores:
            return self._create_empty_chart("No scores data available")
        
        # Filter và normalize scores
        score_names = []
        score_values = []
        
        for key, value in avg_scores.items():
            if isinstance(value, (int, float)) and not np.isnan(value):
                # Normalize different scales to 0-100
                if 'phq9' in key.lower():
                    normalized = min((value / 27) * 100, 100)  # PHQ-9 max = 27
                elif 'gad7' in key.lower():
                    normalized = min((value / 21) * 100, 100)  # GAD-7 max = 21
                elif 'dass21' in key.lower():
                    normalized = min((value / 42) * 100, 100)  # DASS-21 subscale max = 42
                else:
                    normalized = min(value, 100)
                
                score_names.append(key.replace('_', ' ').title())
                score_values.append(normalized)
        
        if not score_names:
            return self._create_empty_chart("No valid scores for radar chart")
        
        # Add first point at end to close the radar
        score_names.append(score_names[0])
        score_values.append(score_values[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=score_values,
            theta=score_names,
            fill='toself',
            name='Average Scores',
            line_color=self.color_palette['primary'],
            fillcolor=f"rgba(31, 119, 180, 0.3)"
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title={
                'text': "🎯 Risk Scores Profile",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50'}
            },
            width=500,
            height=500
        )
        
        return fig
    
    def create_interactive_dashboard(self, ml_insights_report: Dict):
        """
        Tạo interactive dashboard tổng hợp
        """
        st.markdown("## 🧠 AI-Powered Mental Health Analytics")
        
        if 'error' in ml_insights_report:
            st.error(f"❌ Error loading insights: {ml_insights_report['error']}")
            return
        
        # Summary metrics
        data_summary = ml_insights_report.get('data_summary', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📊 Total Assessments",
                data_summary.get('total_assessments', 0),
                help="Total number of assessments analyzed"
            )
        
        with col2:
            st.metric(
                "👥 Unique Sessions",
                data_summary.get('unique_sessions', 0),
                help="Number of unique user sessions"
            )
        
        with col3:
            st.metric(
                "📅 Analysis Period",
                f"{data_summary.get('analysis_period_days', 0)} days",
                help="Number of days of data analyzed"
            )
        
        with col4:
            ml_status = ml_insights_report.get('ml_status', {})
            ml_available = ml_status.get('ml_available', False)
            st.metric(
                "🤖 ML Status",
                "Active" if ml_available else "Inactive",
                help="Machine Learning capabilities status"
            )
        
        # Risk Analysis Section
        risk_analysis = ml_insights_report.get('risk_analysis', {})
        if 'cluster_analysis' in risk_analysis:
            st.markdown("### 🎯 Risk Level Distribution")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                risk_chart = self.create_risk_distribution_chart(risk_analysis)
                st.plotly_chart(risk_chart, use_container_width=True)
            
            with col2:
                st.markdown("#### 📋 Cluster Analysis Details")
                for cluster_id, data in risk_analysis['cluster_analysis'].items():
                    risk_level = data.get('risk_level', 'unknown')
                    color = self.color_palette.get(risk_level, 'gray')
                    
                    st.markdown(f"""
                    <div style="padding: 10px; border-left: 4px solid {color}; margin: 5px 0;">
                    <b>{risk_level.replace('_', ' ').title()}</b><br>
                    👥 {data['size']} users ({data['percentage']:.1f}%)<br>
                    📊 Avg scores: {len(data.get('avg_scores', {}))} metrics
                    </div>
                    """, unsafe_allow_html=True)
        
        # Trends Analysis Section
        trends_analysis = ml_insights_report.get('trends_analysis', {})
        if trends_analysis and 'daily_assessment_counts' in trends_analysis:
            st.markdown("### 📈 Activity Trends & Patterns")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                trends_chart = self.create_trends_timeline(trends_analysis)
                st.plotly_chart(trends_chart, use_container_width=True)
            
            with col2:
                hourly_heatmap = self.create_hourly_heatmap(trends_analysis)
                st.plotly_chart(hourly_heatmap, use_container_width=True)
            
            # Activity insights
            st.markdown("#### 🔍 Activity Insights")
            insights_col1, insights_col2 = st.columns(2)
            
            with insights_col1:
                peak_hour = trends_analysis.get('peak_hour', 'N/A')
                st.info(f"⏰ **Peak Hour:** {peak_hour}:00")
                
                peak_day = trends_analysis.get('peak_day', 'N/A')
                st.info(f"📅 **Most Active Day:** {peak_day}")
            
            with insights_col2:
                weekly_dist = trends_analysis.get('weekly_distribution', {})
                if weekly_dist:
                    total_weekly = sum(weekly_dist.values())
                    weekend_count = weekly_dist.get('Saturday', 0) + weekly_dist.get('Sunday', 0)
                    weekend_percent = (weekend_count / total_weekly * 100) if total_weekly > 0 else 0
                    st.info(f"📊 **Weekend Activity:** {weekend_percent:.1f}%")
        
        # Summary Insights
        summary_insights = ml_insights_report.get('summary_insights', [])
        if summary_insights:
            st.markdown("### 💡 Key Insights")
            for insight in summary_insights:
                st.success(insight)
        
        # ML Model Status
        ml_status = ml_insights_report.get('ml_status', {})
        if ml_status:
            with st.expander("🤖 Machine Learning Status"):
                st.json(ml_status)
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Helper to create empty chart with message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            plot_bgcolor='white'
        )
        return fig

# Export for use in other modules
def create_visualization_engine():
    """Factory function for visualization engine"""
    return AdvancedVisualization()
