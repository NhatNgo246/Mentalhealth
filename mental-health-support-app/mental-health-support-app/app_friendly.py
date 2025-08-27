import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime
from components.ui import app_header, show_disclaimer, load_css, create_info_card
from components.friendly_ui import (
    create_friendly_button, create_hero_section_friendly, create_mood_check_section,
    create_assessment_intro, create_friendly_progress_indicator, create_encouraging_message,
    create_result_celebration
)
from components.modern_ui import (
    create_glassmorphism_card, create_neumorphism_button, create_floating_action_menu,
    create_progress_ring, create_animated_counter, create_voice_interaction_ui,
    create_mood_selector_2025, create_ai_chat_preview, create_wellness_dashboard
)
from assets.graphics import (
    get_hero_ascii, get_wellness_icons, get_mood_faces, 
    get_progress_indicators, SEVERITY_COLORS, GRADIENTS
)

# Configure page
st.set_page_config(
    page_title="Mental Health Support App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
load_css()

# Initialize session state for flow control
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False
if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False

# Header và disclaimer
app_header()

# Main content with enhanced styling
st.markdown("""
<div class="fade-in" style="margin: 2rem 0;">
""", unsafe_allow_html=True)

# Hero section thân thiện và vui nhộn
create_hero_section_friendly()

# Section kiểm tra tâm trạng
create_mood_check_section()

# Giới thiệu về assessment 
create_assessment_intro()

# Show disclaimer first
show_disclaimer()

# Consent and flow control với giao diện thân thiện
if not st.session_state.consent_given:
    
    # Consent section thân thiện
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fff7ed 0%, #f0f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 2px solid #fed7aa;
    ">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤝</div>
            <h3 style="color: #2d3748; margin-bottom: 1rem;">
                Chúng ta hãy làm quen trước nhé!
            </h3>
            <p style="color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem;">
                Trước khi bắt đầu cuộc trò chuyện thú vị này, tôi muốn bạn biết rằng:
            </p>
        </div>
        
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        ">
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔐</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">Bí mật tuyệt đối</h4>
                <p style="margin: 0; color: #718096; font-size: 0.9rem;">
                    Thông tin của bạn được bảo vệ như kim cương 💎
                </p>
            </div>
            
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">AI thông minh</h4>
                <p style="margin: 0; color: #718096; font-size: 0.9rem;">
                    Sẵn sàng trò chuyện 24/7, không bao giờ mệt mỏi! 🌙
                </p>
            </div>
            
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">Chính xác cao</h4>
                <p style="margin: 0; color: #718096; font-size: 0.9rem;">
                    Dựa trên khoa học, không phải đoán mò 🔬
                </p>
            </div>
        </div>
        
        <div style="
            background: linear-gradient(135deg, #dbeafe 0%, #fef3c7 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.8rem;">💝</div>
            <p style="margin: 0; color: #1e40af; font-weight: 500; line-height: 1.5;">
                <strong>Lời hứa nhỏ:</strong> Tôi sẽ ở bên bạn trong suốt hành trình này, 
                không phán xét, chỉ lắng nghe và hỗ trợ! 🌟
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Consent checkbox và button thân thiện
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        consent_check = st.checkbox(
            "✨ Tôi sẵn sàng bắt đầu cuộc hành trình khám phá bản thân!",
            key="consent_checkbox",
            help="Đừng lo, chỉ là bước đầu thôi! 😊"
        )
        
        st.markdown('<div style="margin: 1.5rem 0;">', unsafe_allow_html=True)
        
        if st.button(
            "🚀 Bắt đầu thôi nào!", 
            disabled=not consent_check,
            use_container_width=True,
            type="primary",
            help="Nhấp để bắt đầu cuộc phiêu lưu! 🎯"
        ):
            # Animation chúc mừng
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                margin: 1rem 0;
                animation: celebration 1s ease;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                <h3 style="margin: 0; color: white;">Tuyệt vời! Chúng ta bắt đầu nhé!</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Đang chuẩn bị những câu hỏi thú vị...</p>
            </div>
            
            <style>
            @keyframes celebration {
                0% { transform: scale(0.8); opacity: 0; }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); opacity: 1; }
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.session_state.consent_given = True
            st.session_state.assessment_started = True
            time.sleep(1)  # Để người dùng thấy animation
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Show assessment or results based on state
    if not st.session_state.get("scores"):
        # Import and show assessment directly
        from components.questionnaires import load_dass21_vi
        from components.scoring import score_dass21
        from components.ui import create_progress_indicator
        
        # Progress indicator thân thiện
        create_friendly_progress_indicator(2, 3, "Bài đánh giá DASS-21")
        
        # Encouraging message
        create_encouraging_message()
        
        st.markdown("""
        <div class="assessment-form fade-in">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                    font-size: 2rem;
                ">📝 Câu hỏi thú vị về tâm trạng</h2>
                <p style="color: #4a5568; margin: 1rem 0; font-size: 1.1rem; line-height: 1.6;">
                    Hãy chọn mức độ phù hợp nhất với cảm nhận của bạn trong <strong>tuần vừa qua</strong> nhé! 
                    Đừng suy nghĩ quá nhiều, cảm giác đầu tiên thường chính xác nhất đấy 😊
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        cfg = load_dass21_vi()
        options = cfg["options"]
        
        if "answers" not in st.session_state:
            st.session_state.answers = {}
        
        # Enhanced form with better styling
        with st.form("dass21_form"):
            st.markdown('<div class="assessment-form">', unsafe_allow_html=True)
            
            for i, item in enumerate(cfg["items"], 1):
                # Question card with enhanced styling
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    border-left: 4px solid #667eea;
                ">
                    <h4 style="margin: 0 0 1rem 0; color: #2d3748; font-size: 1.1rem;">
                        <span style="
                            background: linear-gradient(135deg, #667eea, #764ba2);
                            color: white;
                            padding: 0.3rem 0.8rem;
                            border-radius: 15px;
                            font-size: 0.9rem;
                            margin-right: 1rem;
                        ">{i}</span>
                        {item["text"]}
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Radio buttons with emoji options
                option_labels = [f"{opt['emoji']} {opt['label']}" for opt in options]
                
                answer = st.radio(
                    f"Câu {i}",
                    options=range(len(options)),
                    format_func=lambda x: option_labels[x],
                    key=f"q_{i}",
                    label_visibility="collapsed",
                    horizontal=True
                )
                
                if answer is not None:
                    st.session_state.answers[item["id"]] = answer
                
                st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Submit button thân thiện
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button(
                    "🎯 Xem kết quả ngay!", 
                    use_container_width=True,
                    type="primary",
                    help="Bạn đã sẵn sàng xem kết quả chưa? 🎉"
                )
            
            if submitted:
                # Check if all questions are answered
                if len(st.session_state.answers) == len(cfg["items"]):
                    scores = score_dass21(st.session_state.answers, cfg)
                    st.session_state.scores = {k: v.__dict__ for k, v in scores.items()}
                    
                    # Celebration animation
                    create_result_celebration()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("⚠️ Hãy trả lời hết các câu hỏi nhé! Chỉ còn thiếu một chút thôi! 😊")
    
    else:
        # Show results directly
        import pandas as pd
        try:
            import plotly.express as px
        except ImportError:
            px = None  # Fallback if plotly not available
        from components.ui import create_result_card, create_metric_card, create_progress_indicator
        
        # Progress completion với celebration
        create_friendly_progress_indicator(3, 3, "Kết quả đánh giá")
        
        # Show celebration
        create_result_celebration()
        
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                font-size: 2.5rem;
            ">🎊 Kết quả đánh giá của bạn</h2>
            <p style="color: #4a5568; margin: 1rem 0; font-size: 1.2rem;">
                Đây là "bức tranh" tâm lý của bạn trong thời gian qua! 🎨
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        scores = st.session_state.scores
        df = pd.DataFrame(scores).T
        
        # Create enhanced metrics row với colors
        col1, col2, col3 = st.columns(3)
        
        def get_severity_color(severity):
            """Map severity to color"""
            severity_map = {
                'Normal': SEVERITY_COLORS['normal'],
                'Mild': SEVERITY_COLORS['mild'],
                'Moderate': SEVERITY_COLORS['moderate'],
                'Severe': SEVERITY_COLORS['severe'],
                'Extremely severe': SEVERITY_COLORS['extremely_severe']
            }
            return severity_map.get(severity, SEVERITY_COLORS['normal'])
        
        def get_mood_emoji(severity):
            """Map severity to appropriate emoji"""
            mood_faces = get_mood_faces()
            if severity in ['Normal', 'Mild']:
                return mood_faces['happy']
            elif severity == 'Moderate':
                return mood_faces['neutral']
            elif severity == 'Severe':
                return mood_faces['sad']
            else:
                return mood_faces['very_sad']
        
        with col1:
            depression_score = df.loc['Depression', 'adjusted']
            depression_severity = df.loc['Depression', 'severity']
            color = get_severity_color(depression_severity)
            emoji = get_mood_emoji(depression_severity)
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 15px; 
                 text-align: center; margin: 0.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji.split()[0]}</div>
                <h3 style="margin: 0; color: white;">😔 Trầm cảm</h3>
                <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">{depression_score} điểm</div>
                <div style="opacity: 0.9;">Mức độ: {depression_severity}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            anxiety_score = df.loc['Anxiety', 'adjusted']
            anxiety_severity = df.loc['Anxiety', 'severity']
            color = get_severity_color(anxiety_severity)
            emoji = get_mood_emoji(anxiety_severity)
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 15px; 
                 text-align: center; margin: 0.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji.split()[1] if len(emoji.split()) > 1 else emoji.split()[0]}</div>
                <h3 style="margin: 0; color: white;">😰 Lo âu</h3>
                <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">{anxiety_score} điểm</div>
                <div style="opacity: 0.9;">Mức độ: {anxiety_severity}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            stress_score = df.loc['Stress', 'adjusted']
            stress_severity = df.loc['Stress', 'severity']
            color = get_severity_color(stress_severity)
            emoji = get_mood_emoji(stress_severity)
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1.5rem; border-radius: 15px; 
                 text-align: center; margin: 0.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji.split()[-1] if len(emoji.split()) > 2 else emoji.split()[0]}</div>
                <h3 style="margin: 0; color: white;">😓 Stress</h3>
                <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">{stress_score} điểm</div>
                <div style="opacity: 0.9;">Mức độ: {stress_severity}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick recommendations với friendly tone
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%);
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem 0;
            border-left: 5px solid #10b981;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-right: 1rem;">💡</div>
                <div>
                    <h3 style="margin: 0; color: #065f46;">Lời khuyên nhỏ từ tôi</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #047857;">Dựa trên kết quả vừa rồi nhé!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Recommendations based on results
        all_normal = all(df.loc[domain, 'severity'] == 'Normal' for domain in ['Depression', 'Anxiety', 'Stress'])
        
        if all_normal:
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🌟</div>
                <h4 style="color: #065f46; margin-bottom: 1rem;">Tuyệt vời! Bạn đang trong trạng thái rất tốt!</h4>
                <p style="color: #047857; line-height: 1.6;">
                    Hãy tiếp tục duy trì lối sống tích cực này nhé! 
                    Đừng quên dành thời gian cho bản thân và những điều bạn yêu thích! 🎉
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            recommendations = []
            if depression_score > 9:
                recommendations.append("🌱 Hãy thử viết nhật ký cảm xúc mỗi ngày")
            if anxiety_score > 7:
                recommendations.append("🧘‍♀️ Thực hành hít thở sâu 5 phút mỗi ngày")
            if stress_score > 14:
                recommendations.append("🎵 Nghe nhạc thư giãn hoặc đi dạo trong công viên")
            
            recommendations.extend([
                "💤 Ngủ đủ 7-8 tiếng mỗi đêm",
                "🥗 Ăn uống lành mạnh và uống đủ nước",
                "👥 Trò chuyện với bạn bè, người thân"
            ])
            
            for rec in recommendations[:4]:  # Show max 4 recommendations
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1rem 1.5rem;
                    border-radius: 10px;
                    margin: 0.8rem 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                ">
                    <p style="margin: 0; color: #047857; font-size: 1rem;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Action buttons với friendly design
        st.markdown("### 🎯 Bước tiếp theo")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💬 Trò chuyện với AI", use_container_width=True, type="primary"):
                st.switch_page("pages/5_Chatbot.py")
        
        with col2:
            if st.button("📚 Tìm hiểu thêm", use_container_width=True):
                st.switch_page("pages/3_Resources.py")
        
        with col3:
            if st.button("🔄 Làm lại bài test", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key in ["answers", "scores", "consent_given", "assessment_started"]:
                        del st.session_state[key]
                st.rerun()

# Floating action menu
create_floating_action_menu()

st.markdown('</div>', unsafe_allow_html=True)
