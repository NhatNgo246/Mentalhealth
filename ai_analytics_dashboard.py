"""
🚀 AI Analytics Dashboard
Advanced ML-powered analytics dashboard cho SOULFRIEND V2.0
"""

import streamlit as st
import sys
import os

# Add paths
sys.path.insert(0, '/workspaces/Mentalhealth')
sys.path.insert(0, '/workspaces/Mentalhealth/ai_analytics')

from ai_analytics.ml_insights import MentalHealthMLInsights
from ai_analytics.advanced_visualization import AdvancedVisualization
import json
from datetime import datetime
import pandas as pd

# Page config
st.set_page_config(
    page_title="SOULFRIEND AI Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 SOULFRIEND AI Analytics Dashboard</h1>
        <p>Advanced Machine Learning insights cho Mental Health Research</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔧 Analytics Controls")
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            st.rerun()
        
        st.markdown("---")
        
        # Analysis options
        st.markdown("### 📊 Analysis Options")
        show_risk_analysis = st.checkbox("🎯 Risk Pattern Analysis", value=True)
        show_trends = st.checkbox("📈 Trends Analysis", value=True)
        show_predictions = st.checkbox("🔮 Predictions", value=True)
        show_raw_data = st.checkbox("📄 Raw Data View", value=False)
        
        st.markdown("---")
        
        # ML Model status
        st.markdown("### 🤖 ML Status")
        try:
            ml_insights = MentalHealthMLInsights()
            st.success("✅ ML Engine: Active")
            st.info(f"📊 Models: {len(ml_insights.models)}")
        except Exception as e:
            st.error(f"❌ ML Engine Error: {str(e)[:50]}...")
    
    # Main content
    try:
        # Initialize ML insights
        with st.spinner("🔄 Loading ML insights..."):
            ml_insights = MentalHealthMLInsights()
            insights_report = ml_insights.generate_insights_report()
        
        # Check for errors
        if 'error' in insights_report:
            st.error(f"❌ Error generating insights: {insights_report['error']}")
            
            # Show sample data instead
            st.markdown("### 📝 Sample Analytics Demo")
            st.info("Since no real data is available, here's a demo of what the AI analytics would show:")
            
            # Demo data
            demo_report = create_demo_data()
            viz_engine = AdvancedVisualization()
            viz_engine.create_interactive_dashboard(demo_report)
            
            return
        
        # Success - show real insights
        st.success(f"✅ Successfully analyzed {insights_report.get('data_summary', {}).get('total_assessments', 0)} assessments")
        
        # Create visualization dashboard
        viz_engine = AdvancedVisualization()
        viz_engine.create_interactive_dashboard(insights_report)
        
        # Additional analysis sections
        if show_predictions:
            st.markdown("---")
            st.markdown("## 🔮 Predictive Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Risk Prediction Demo")
                
                # Input for prediction
                phq9_score = st.slider("PHQ-9 Score", 0, 27, 10)
                gad7_score = st.slider("GAD-7 Score", 0, 21, 8)
                
                if st.button("🎯 Predict Risk Level"):
                    prediction = ml_insights.predict_risk_category({
                        'phq9_total_score': phq9_score,
                        'gad7_total_score': gad7_score
                    })
                    
                    if 'error' not in prediction:
                        risk_level = prediction.get('predicted_risk_level', 'unknown')
                        confidence = prediction.get('confidence', 0)
                        
                        # Display prediction
                        if risk_level == 'low_risk':
                            st.success(f"✅ Predicted Risk: {risk_level.replace('_', ' ').title()} (Confidence: {confidence:.1%})")
                        elif risk_level == 'moderate_risk':
                            st.warning(f"⚠️ Predicted Risk: {risk_level.replace('_', ' ').title()} (Confidence: {confidence:.1%})")
                        else:
                            st.error(f"🚨 Predicted Risk: {risk_level.replace('_', ' ').title()} (Confidence: {confidence:.1%})")
                        
                        # Show recommendations
                        recommendations = prediction.get('recommendations', [])
                        if recommendations:
                            st.markdown("#### 💡 Recommendations:")
                            for rec in recommendations:
                                st.markdown(f"• {rec}")
                    else:
                        st.error(f"Error in prediction: {prediction['error']}")
            
            with col2:
                st.markdown("### 📈 Trend Predictions")
                st.info("🚧 Advanced trend predictions will be available with more historical data")
                
                # Placeholder for future trend predictions
                st.markdown("""
                **Coming Soon:**
                - 📊 Weekly assessment volume predictions
                - 🎯 Risk level trend forecasting  
                - 👥 User engagement predictions
                - 🔄 Seasonal pattern analysis
                """)
        
        if show_raw_data:
            st.markdown("---")
            st.markdown("## 📄 Raw Insights Data")
            
            with st.expander("🔍 View Raw JSON Data"):
                st.json(insights_report)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6c757d; padding: 1rem;">
            🧠 SOULFRIEND AI Analytics • Powered by Machine Learning • 
            Generated at {timestamp}
        </div>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
        unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error in AI Analytics Dashboard: {str(e)}")
        
        # Fallback to demo
        st.markdown("### 🎭 Demo Mode")
        st.info("Showing demo analytics data...")
        
        demo_report = create_demo_data()
        viz_engine = AdvancedVisualization()
        viz_engine.create_interactive_dashboard(demo_report)

def create_demo_data():
    """Create demo data for visualization when no real data is available"""
    return {
        'generated_at': datetime.now().isoformat(),
        'data_summary': {
            'total_assessments': 150,
            'analysis_period_days': 30,
            'unique_sessions': 95
        },
        'risk_analysis': {
            'cluster_analysis': {
                'cluster_0': {
                    'size': 45,
                    'percentage': 30.0,
                    'avg_scores': {'phq9_total_score': 5.2, 'gad7_total_score': 4.1},
                    'risk_level': 'low_risk'
                },
                'cluster_1': {
                    'size': 60,
                    'percentage': 40.0,
                    'avg_scores': {'phq9_total_score': 11.5, 'gad7_total_score': 9.8},
                    'risk_level': 'moderate_risk'
                },
                'cluster_2': {
                    'size': 35,
                    'percentage': 23.3,
                    'avg_scores': {'phq9_total_score': 18.2, 'gad7_total_score': 15.4},
                    'risk_level': 'high_risk'
                },
                'cluster_3': {
                    'size': 10,
                    'percentage': 6.7,
                    'avg_scores': {'phq9_total_score': 23.1, 'gad7_total_score': 19.2},
                    'risk_level': 'very_high_risk'
                }
            },
            'total_assessments': 150,
            'risk_features_used': ['phq9_total_score', 'gad7_total_score'],
            'model_stored': True
        },
        'trends_analysis': {
            'daily_assessment_counts': {
                '2025-08-20': 8, '2025-08-21': 12, '2025-08-22': 15, '2025-08-23': 9,
                '2025-08-24': 6, '2025-08-25': 11, '2025-08-26': 14, '2025-08-27': 18,
                '2025-08-28': 10
            },
            'peak_hour': 14,
            'peak_day': 'Wednesday',
            'hourly_distribution': {
                8: 2, 9: 5, 10: 8, 11: 12, 12: 15, 13: 18, 14: 22, 15: 20,
                16: 16, 17: 14, 18: 10, 19: 8, 20: 6, 21: 4, 22: 2
            },
            'weekly_distribution': {
                'Monday': 25, 'Tuesday': 22, 'Wednesday': 28, 'Thursday': 24,
                'Friday': 20, 'Saturday': 15, 'Sunday': 16
            },
            'analysis_period_days': 30
        },
        'summary_insights': [
            "🚨 30.0% người dùng thuộc nhóm nguy cơ cao hoặc rất cao",
            "⏰ Giờ cao điểm đánh giá: 14:00",
            "📅 Ngày trong tuần phổ biến nhất: Wednesday"
        ],
        'ml_status': {
            'ml_available': True,
            'models_trained': ['risk_clustering'],
            'scalers_available': ['risk_features']
        }
    }

if __name__ == "__main__":
    main()
