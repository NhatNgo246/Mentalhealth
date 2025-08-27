"""
Mental Health 2025 - Modern Experience Page
Next-generation user interface and interactions
"""

import streamlit as st
import time
from components.modern_ui import *
from components.ui import load_css

st.set_page_config(
    page_title="Mental Health 2025",
    page_icon="🚀",
    layout="wide"
)

# Load modern CSS
load_css()

# Main container with modern layout
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 2rem;
    margin: -2rem -2rem 2rem -2rem;
    text-align: center;
    color: white;
">
    <div style="font-size: 4rem; margin-bottom: 1rem; animation: floating 3s ease-in-out infinite;">🚀</div>
    <h1 style="
        font-size: 3.5rem;
        margin: 0 0 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: slideInUp 1s ease;
    ">Mental Health 2025</h1>
    <p style="
        font-size: 1.3rem;
        margin: 0;
        opacity: 0.95;
        animation: slideInUp 1s ease 0.2s both;
    ">
        Trải nghiệm đánh giá tâm lý với công nghệ tiên tiến nhất
    </p>
</div>
""", unsafe_allow_html=True)

# Feature showcase
st.markdown("## 🌟 Tính năng nổi bật 2025")

col1, col2, col3 = st.columns(3)

with col1:
    create_glassmorphism_card(
        "🎯 AI-Powered Assessment",
        """
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin: 1rem 0;">🧠</div>
            <p>Đánh giá tâm lý thông minh với AI</p>
            <p>✅ Độ chính xác 95%</p>
            <p>⚡ Kết quả trong 2 phút</p>
        </div>
        """,
        "🎯"
    )

with col2:
    create_glassmorphism_card(
        "💬 Smart Chatbot",
        """
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin: 1rem 0;">🤖</div>
            <p>Tư vấn AI 24/7 thông minh</p>
            <p>🌟 GPT-4 Turbo powered</p>
            <p>💡 Phản hồi cá nhân hóa</p>
        </div>
        """,
        "💬",
        "linear-gradient(135deg, rgba(168, 237, 234, 0.1), rgba(254, 214, 227, 0.1))"
    )

with col3:
    create_glassmorphism_card(
        "📊 Real-time Analytics",
        """
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin: 1rem 0;">📈</div>
            <p>Dashboard theo dõi realtime</p>
            <p>📱 Responsive design</p>
            <p>🎯 Insights cá nhân</p>
        </div>
        """,
        "📊",
        "linear-gradient(135deg, rgba(255, 236, 210, 0.1), rgba(252, 182, 159, 0.1))"
    )

# Interactive demo section
st.markdown("## 🎮 Trải nghiệm tương tác")

# Mood selector
create_mood_selector_2025()

# Progress indicators
st.markdown("### 📈 Theo dõi tiến triển")
col1, col2, col3, col4 = st.columns(4)

with col1:
    create_progress_ring(78, 120, 8)
    st.markdown("<p style='text-align: center; margin-top: -1rem; font-weight: 600;'>Tâm trạng</p>", unsafe_allow_html=True)

with col2:
    create_progress_ring(65, 120, 8)
    st.markdown("<p style='text-align: center; margin-top: -1rem; font-weight: 600;'>Stress</p>", unsafe_allow_html=True)

with col3:
    create_progress_ring(82, 120, 8)
    st.markdown("<p style='text-align: center; margin-top: -1rem; font-weight: 600;'>Giấc ngủ</p>", unsafe_allow_html=True)

with col4:
    create_progress_ring(71, 120, 8)
    st.markdown("<p style='text-align: center; margin-top: -1rem; font-weight: 600;'>Tổng thể</p>", unsafe_allow_html=True)

# Voice interface
create_voice_interaction_ui()

# AI Chat preview
st.markdown("## 💬 Preview AI Assistant")
create_ai_chat_preview()

# Action buttons
st.markdown("## 🚀 Bắt đầu ngay")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎯 Đánh giá tâm lý", use_container_width=True, type="primary"):
        st.switch_page("app.py")

with col2:
    if st.button("💬 Chat với AI", use_container_width=True):
        st.switch_page("pages/5_Chatbot.py")

with col3:
    if st.button("📊 Xem tài nguyên", use_container_width=True):
        st.switch_page("pages/3_Resources.py")

# Floating action menu
create_floating_action_menu()

# Modern footer
st.markdown("""
<div style="
    margin-top: 4rem;
    padding: 3rem 2rem;
    background: var(--primary-gradient);
    border-radius: var(--radius-xl);
    color: white;
    text-align: center;
">
    <div style="font-size: 2rem; margin-bottom: 1rem;">🌟</div>
    <h2 style="margin: 0 0 1rem 0;">Mental Health Support 2025</h2>
    <p style="margin: 0 0 1.5rem 0; opacity: 0.9; font-size: 1.1rem;">
        Công nghệ AI tiên tiến cho sức khỏe tâm thần
    </p>
    <div style="
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
    ">
        <div style="text-align: center;">
            <div style="font-size: 1.5rem;">🔒</div>
            <small>Bảo mật</small>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.5rem;">⚡</div>
            <small>Nhanh chóng</small>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.5rem;">🎯</div>
            <small>Chính xác</small>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.5rem;">💡</div>
            <small>Thông minh</small>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
