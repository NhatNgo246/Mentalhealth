"""
SOULFRIEND AI Platform
Advanced AI-powered mental health analysis and recommendations
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND AI Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# App header
app_header()

# AI Platform interface
def ai_platform_main():
    """Main AI Platform interface"""
    st.markdown("# 🤖 SOULFRIEND AI Platform")
    st.markdown("---")
    
    # AI Features tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 AI Analysis", 
        "💡 Smart Insights", 
        "🎯 Personalized Plans",
        "📊 Predictive Analytics"
    ])
    
    with tab1:
        st.markdown("### 🧠 AI-Powered Mental Health Analysis")
        st.info("🔧 AI Analysis engine đang được phát triển...")
        
        # Mock AI analysis interface
        if st.button("🚀 Run AI Analysis"):
            with st.spinner("🤖 AI đang phân tích..."):
                st.success("✅ AI Analysis completed!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Risk Level", "Low", "↓ 15%")
                    st.metric("Improvement Score", "8.5/10", "↑ 12%")
                
                with col2:
                    st.metric("Support Priority", "Medium", "→ 0%")
                    st.metric("Recovery Timeline", "6-8 weeks", "↓ 2 weeks")
    
    with tab2:
        st.markdown("### 💡 Smart Insights & Recommendations")
        st.info("🔧 Smart Insights engine đang được phát triển...")
        
        # Mock insights
        st.markdown("#### 🎯 Personalized Insights")
        insights = [
            "🌅 Buổi sáng là thời điểm tâm trạng tốt nhất của bạn",
            "🏃‍♂️ Hoạt động thể chất giúp cải thiện tâm trạng 23%",
            "😴 Chất lượng giấc ngủ có tương quan mạnh với điểm số anxiety",
            "🧘‍♀️ Meditation 10 phút/ngày có thể giảm stress 18%"
        ]
        
        for insight in insights:
            st.success(insight)
    
    with tab3:
        st.markdown("### 🎯 Personalized Treatment Plans")
        st.info("🔧 Treatment Plan generator đang được phát triển...")
        
        # Mock treatment plan
        if st.button("📋 Generate Treatment Plan"):
            st.markdown("#### 📝 Your Personalized Plan")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Week 1-2: Foundation**")
                st.markdown("- 🧘‍♀️ Daily mindfulness (5 min)")
                st.markdown("- 📱 Mood tracking")
                st.markdown("- 🏃‍♂️ Light exercise (15 min)")
                
            with col2:
                st.markdown("**Week 3-4: Building**")
                st.markdown("- 🧘‍♀️ Extended meditation (10 min)")
                st.markdown("- 📚 CBT exercises")
                st.markdown("- 👥 Social connection activities")
    
    with tab4:
        st.markdown("### 📊 Predictive Analytics")
        st.info("🔧 Predictive Analytics đang được phát triển...")
        
        # Mock analytics
        st.markdown("#### 📈 Trend Analysis")
        st.line_chart({
            'Mood Score': [6.2, 6.5, 7.1, 6.8, 7.3, 7.6, 8.1],
            'Anxiety Level': [4.5, 4.2, 3.8, 4.1, 3.5, 3.2, 2.9],
            'Sleep Quality': [5.8, 6.1, 6.4, 6.2, 6.7, 7.0, 7.3]
        })

if __name__ == "__main__":
    ai_platform_main()
