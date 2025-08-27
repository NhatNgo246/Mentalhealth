"""
Mental Health Support App - 2025 Demo Page
Showcase of modern UI/UX features and interactions
"""

import streamlit as st
import time
from components.modern_ui import *

st.set_page_config(
    page_title="Mental Health 2025 Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1 style="
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin: 0;
    ">🚀 Mental Health 2025 Demo</h1>
    <p style="font-size: 1.2rem; color: var(--text-secondary); margin-top: 1rem;">
        Trải nghiệm những tính năng UI/UX tiên tiến nhất năm 2025
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎨 Glassmorphism", 
    "🌊 Neumorphism", 
    "📊 Modern Charts", 
    "🎤 Voice UI", 
    "💬 AI Chat"
])

with tab1:
    st.markdown("### 🎨 Glassmorphism Design Trend 2025")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_glassmorphism_card(
            "🧠 Đánh giá tâm lý",
            """
            <p>Sử dụng thang đo DASS-21 chuẩn quốc tế</p>
            <p>✅ Độ chính xác cao</p>
            <p>⚡ Kết quả tức thì</p>
            <p>📱 Responsive design</p>
            """,
            "🎯"
        )
    
    with col2:
        create_glassmorphism_card(
            "🤖 AI Assistant",
            """
            <p>Trợ lý AI thông minh 24/7</p>
            <p>🌟 GPT-4 powered</p>
            <p>💡 Tư vấn cá nhân hóa</p>
            <p>🔒 Bảo mật tuyệt đối</p>
            """,
            "🤖",
            "linear-gradient(135deg, rgba(168, 237, 234, 0.1), rgba(254, 214, 227, 0.1))"
        )

with tab2:
    st.markdown("### 🌊 Neumorphism Interactive Elements")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Bắt đầu đánh giá", key="neuro1"):
            st.success("Neumorphism button clicked!")
    
    with col2:
        if st.button("📊 Xem kết quả", key="neuro2"):
            st.info("Loading results...")
    
    with col3:
        if st.button("💬 Chat với AI", key="neuro3"):
            st.warning("Opening AI chat...")
    
    # Progress rings
    st.markdown("#### 📈 Circular Progress Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_progress_ring(25, 100, 6)
        st.markdown("<p style='text-align: center; margin-top: -1rem;'>Stress Level</p>", unsafe_allow_html=True)
    
    with col2:
        create_progress_ring(65, 100, 6)
        st.markdown("<p style='text-align: center; margin-top: -1rem;'>Anxiety</p>", unsafe_allow_html=True)
    
    with col3:
        create_progress_ring(40, 100, 6)
        st.markdown("<p style='text-align: center; margin-top: -1rem;'>Depression</p>", unsafe_allow_html=True)
    
    with col4:
        create_progress_ring(85, 100, 6)
        st.markdown("<p style='text-align: center; margin-top: -1rem;'>Overall</p>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 📊 Modern Data Visualization")
    
    # Animated counters
    col1, col2, col3 = st.columns(3)
    
    if st.button("🎬 Run Animation Demo"):
        with col1:
            create_animated_counter(1247, "Người dùng hôm nay", "👥")
        
        with col2:
            create_animated_counter(89, "Phần trăm hài lòng", "😊")
        
        with col3:
            create_animated_counter(24, "Giờ hỗ trợ/ngày", "🕐")
    
    # Wellness dashboard
    st.markdown("#### 🎯 Personal Wellness Dashboard")
    create_wellness_dashboard()

with tab4:
    st.markdown("### 🎤 Voice-Enabled Interface")
    create_voice_interaction_ui()
    
    st.markdown("#### 🌈 Interactive Mood Selector")
    create_mood_selector_2025()

with tab5:
    st.markdown("### 💬 AI Chat Interface Preview")
    create_ai_chat_preview()
    
    # Add some interactive elements
    st.markdown("#### 🎮 Interactive Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="interactive" style="
            background: white;
            padding: 2rem;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            margin: 1rem 0;
            cursor: pointer;
        ">
            <h4>🎯 Smart Assessment</h4>
            <p>AI-powered mental health evaluation with real-time feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="interactive" style="
            background: white;
            padding: 2rem;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            margin: 1rem 0;
            cursor: pointer;
        ">
            <h4>📱 Mobile First</h4>
            <p>Optimized for all devices with responsive design patterns</p>
        </div>
        """, unsafe_allow_html=True)

# Floating action menu
create_floating_action_menu()

# Footer
st.markdown("""
<div style="
    margin-top: 4rem;
    padding: 2rem;
    text-align: center;
    background: var(--primary-gradient);
    border-radius: var(--radius-lg);
    color: white;
">
    <h3 style="margin: 0 0 1rem 0;">🌟 Mental Health Support 2025</h3>
    <p style="margin: 0; opacity: 0.9;">
        Công nghệ tiên tiến nhất cho sức khỏe tâm thần
    </p>
</div>
""", unsafe_allow_html=True)
