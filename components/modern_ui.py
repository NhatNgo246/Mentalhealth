"""
Modern UI Components 2025
Advanced user experience patterns and interactions
"""

import streamlit as st
import time
from datetime import datetime

def create_glassmorphism_card(title, content, icon="🔮", gradient="linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05))"):
    """2025 Glassmorphism design trend"""
    st.markdown(f"""
    <div style="
        background: {gradient};
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-right: 1rem;">{icon}</div>
            <h3 style="margin: 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h3>
        </div>
        <div style="color: #333; line-height: 1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_neumorphism_button(text, key, icon="🚀", primary=True):
    """2025 Neumorphism button design"""
    bg_color = "#667eea" if primary else "#f0f0f0"
    text_color = "white" if primary else "#333"
    
    return st.markdown(f"""
    <div style="
        background: {bg_color};
        color: {text_color};
        padding: 1rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 
            20px 20px 60px #bebebe,
            -20px -20px 60px #ffffff;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    " onclick="document.querySelector('[data-testid=\\"{key}\\"]').click();">
        <span>{icon}</span>
        <span>{text}</span>
    </div>
    """, unsafe_allow_html=True)

def create_floating_action_menu():
    """2025 Floating Action Button with micro-interactions"""
    st.markdown("""
    <div style="
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 1000;
    ">
        <div style="
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            cursor: pointer;
            transition: transform 0.3s ease;
            animation: pulse 2s infinite;
        " onmouseover="this.style.transform='scale(1.1)'" 
           onmouseout="this.style.transform='scale(1)'">
            <span style="font-size: 1.5rem; color: white;">💬</span>
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4); }
        50% { box-shadow: 0 4px 30px rgba(102, 126, 234, 0.8); }
        100% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4); }
    }
    </style>
    """, unsafe_allow_html=True)

def create_progress_ring(percentage, size=120, stroke_width=8):
    """2025 Circular progress indicator with animations"""
    radius = (size - stroke_width) / 2
    circumference = 2 * 3.14159 * radius
    offset = circumference - (percentage / 100) * circumference
    
    return st.markdown(f"""
    <div style="display: flex; justify-content: center; margin: 2rem 0;">
        <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
            <circle
                cx="{size/2}"
                cy="{size/2}"
                r="{radius}"
                stroke="#e6e6e6"
                stroke-width="{stroke_width}"
                fill="transparent"
            />
            <circle
                cx="{size/2}"
                cy="{size/2}"
                r="{radius}"
                stroke="url(#progressGradient)"
                stroke-width="{stroke_width}"
                fill="transparent"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{offset}"
                stroke-linecap="round"
                style="transition: stroke-dashoffset 1s ease-in-out;"
            />
            <defs>
                <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>
        <div style="
            position: absolute;
            display: flex;
            align-items: center;
            justify-content: center;
            width: {size}px;
            height: {size}px;
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
        ">{percentage}%</div>
    </div>
    """, unsafe_allow_html=True)

def create_animated_counter(target_value, label, icon="📊", duration=2):
    """2025 Animated counter with smooth transitions"""
    placeholder = st.empty()
    
    for i in range(int(duration * 10)):
        current_value = int((i / (duration * 10)) * target_value)
        placeholder.markdown(f"""
        <div style="
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 20px;
            margin: 1rem 0;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 3rem; font-weight: bold; color: #667eea; margin-bottom: 0.5rem;">
                {current_value}
            </div>
            <div style="font-size: 1.2rem; color: #666;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

def create_voice_interaction_ui():
    """2025 Voice-enabled interface"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        color: white;
        text-align: center;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎤</div>
        <h3 style="margin: 0 0 1rem 0;">Voice Assistant</h3>
        <p style="margin: 0 0 1.5rem 0; opacity: 0.9;">
            Nói "Bắt đầu đánh giá" hoặc "Tôi cần trợ giúp"
        </p>
        <div style="
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        ">
            <button style="
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
            ">🎯 Bắt đầu</button>
            <button style="
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
            ">❓ Trợ giúp</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_mood_selector_2025():
    """2025 Interactive mood selector with haptic feedback simulation"""
    moods = [
        {"emoji": "😊", "label": "Tuyệt vời", "color": "#4ade80"},
        {"emoji": "🙂", "label": "Tốt", "color": "#22d3ee"},
        {"emoji": "😐", "label": "Bình thường", "color": "#fbbf24"},
        {"emoji": "😔", "label": "Không tốt", "color": "#f97316"},
        {"emoji": "😢", "label": "Khó khăn", "color": "#ef4444"},
    ]
    
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="text-align: center; margin-bottom: 2rem; color: #333;">
            🌈 Bạn cảm thấy thế nào hôm nay?
        </h3>
        <div style="
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 1rem;
        ">
    """, unsafe_allow_html=True)
    
    for mood in moods:
        st.markdown(f"""
            <div style="
                width: 80px;
                height: 80px;
                background: {mood['color']};
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 0 auto 1rem auto;
            " onmouseover="
                this.style.transform='scale(1.1) translateY(-5px)';
                this.style.boxShadow='0 8px 25px rgba(0,0,0,0.2)';
            " onmouseout="
                this.style.transform='scale(1) translateY(0px)';
                this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)';
            ">
                <div style="font-size: 2rem; margin-bottom: 0.2rem;">{mood['emoji']}</div>
                <div style="font-size: 0.7rem; color: white; font-weight: 600;">{mood['label']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def create_ai_chat_preview():
    """2025 AI Chat interface preview with modern design"""
    messages = [
        {"role": "ai", "content": "Xin chào! Tôi là AI Assistant của bạn. Tôi có thể giúp gì?", "time": "09:30"},
        {"role": "user", "content": "Tôi đang cảm thấy lo âu về công việc", "time": "09:31"},
        {"role": "ai", "content": "Tôi hiểu cảm giác của bạn. Hãy cùng tìm hiểu những kỹ thuật thư giãn nhé.", "time": "09:31"},
    ]
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        max-height: 400px;
        overflow-y: auto;
    ">
        <div style="
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e2e8f0;
        ">
            <div style="
                width: 50px;
                height: 50px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
            ">
                <span style="font-size: 1.5rem;">🤖</span>
            </div>
            <div>
                <h4 style="margin: 0; color: #333;">AI Mental Health Assistant</h4>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">🟢 Trực tuyến</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    for msg in messages:
        if msg["role"] == "ai":
            st.markdown(f"""
            <div style="
                display: flex;
                margin-bottom: 1rem;
                animation: slideInLeft 0.5s ease;
            ">
                <div style="
                    background: white;
                    padding: 1rem;
                    border-radius: 20px 20px 20px 5px;
                    max-width: 70%;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                ">
                    <p style="margin: 0; color: #333;">{msg['content']}</p>
                    <small style="color: #666; font-size: 0.8rem;">{msg['time']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin-bottom: 1rem;
                animation: slideInRight 0.5s ease;
            ">
                <div style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 1rem;
                    border-radius: 20px 20px 5px 20px;
                    max-width: 70%;
                    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
                ">
                    <p style="margin: 0;">{msg['content']}</p>
                    <small style="opacity: 0.8; font-size: 0.8rem;">{msg['time']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_wellness_dashboard():
    """2025 Personal wellness dashboard with real-time metrics"""
    st.markdown("""
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    ">
    """, unsafe_allow_html=True)
    
    metrics = [
        {"title": "Tâm trạng hôm nay", "value": "😊 Tích cực", "change": "+15%", "color": "#4ade80"},
        {"title": "Mức độ stress", "value": "Thấp", "change": "-20%", "color": "#22d3ee"},
        {"title": "Giấc ngủ", "value": "7.5h", "change": "+30min", "color": "#a855f7"},
        {"title": "Hoạt động", "value": "Cao", "change": "+25%", "color": "#f59e0b"},
    ]
    
    for metric in metrics:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-left: 4px solid {metric['color']};
            transition: transform 0.3s ease;
        " onmouseover="this.style.transform='translateY(-5px)'" 
           onmouseout="this.style.transform='translateY(0)'">
            <h4 style="margin: 0 0 0.5rem 0; color: #333; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                {metric['title']}
            </h4>
            <div style="font-size: 1.5rem; font-weight: bold; color: {metric['color']}; margin-bottom: 0.5rem;">
                {metric['value']}
            </div>
            <div style="font-size: 0.8rem; color: #4ade80;">
                ↗️ {metric['change']} so với tuần trước
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
