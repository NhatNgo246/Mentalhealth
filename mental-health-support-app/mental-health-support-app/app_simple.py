import streamlit as st
import pandas as pd
import json
import os
import time
import logging
from datetime import datetime
from components.ui import app_header, show_disclaimer, display_logo
from components.ui_optimized import (
    load_optimized_css, create_hero_section, create_mood_check_section,
    create_info_card, create_consent_section, create_progress_indicator,
    create_question_card, create_results_header, create_metric_card,
    create_recommendation_card, create_success_message
)
from components.questionnaires import load_dass21_vi
from components.scoring import score_dass21
from components.validation import validate_app_state

# Setup logging for production safety
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mental_health_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure page
st.set_page_config(
    page_title="Mental Health Support App",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load optimized CSS
load_optimized_css()

# Initialize session state for flow control
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False
if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False

# Header và disclaimer
app_header()

# Hero section thân thiện với logo
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    display_logo(width=150, centered=True)

# Use optimized hero and mood sections
create_hero_section(
    title="Mental Health Buddy",
    subtitle="Hãy cùng khám phá tâm hồn bạn nhé! 🌟",
    description="Nơi an toàn để chia sẻ cảm xúc và nhận được hỗ trợ 💝"
)

create_mood_check_section()

# Assessment intro with optimized card
create_info_card(
    title="Đánh giá sức khỏe tâm lý DASS-21",
    description="Đây là công cụ đánh giá khoa học giúp bạn hiểu rõ hơn về tình trạng trầm cảm, lo âu và stress hiện tại. Kết quả sẽ giúp bạn có cái nhìn khách quan về tâm lý và đưa ra những bước tiếp theo phù hợp! 🎯",
    icon="📋"
)

# Show disclaimer first
show_disclaimer()

# Consent and flow control
if not st.session_state.consent_given:
    
    # Consent section with optimized component
    create_consent_section()
    
    # Consent checkbox và button thân thiện
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        consent_check = st.checkbox(
            "✨ Tôi sẵn sàng bắt đầu cuộc hành trình khám phá bản thân!",
            key="consent_checkbox",
            help="Đừng lo, chỉ là bước đầu thôi! 😊"
        )
        
        if st.button(
            "🚀 Bắt đầu thôi nào!", 
            disabled=not consent_check,
            use_container_width=True,
            type="primary",
            help="Nhấp để bắt đầu cuộc phiêu lưu! 🎯"
        ):
            # Log user consent for audit trail
            logger.info("User provided consent and started assessment")
            
            
            create_success_message(
                title="Tuyệt vời! Chúng ta bắt đầu nhé!",
                message="Đang chuẩn bị những câu hỏi thú vị..."
            )
            
            st.session_state.consent_given = True
            st.session_state.assessment_started = True
            time.sleep(1)
            st.rerun()

else:
    # Show assessment or results based on state
    if not st.session_state.get("scores"):
        # Progress indicator
        create_progress_indicator(
            current_step=2, 
            total_steps=3, 
            title="Bài đánh giá DASS-21"
        )
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                font-size: 2rem;
            ">📝 Câu hỏi thú vị về tâm trạng</h2>
            <p style="color: #4a5568; margin: 1rem 0; font-size: 1.1rem; line-height: 1.6;">>
                Hãy chọn mức độ phù hợp nhất với cảm nhận của bạn trong <strong>tuần vừa qua</strong> nhé! 
                Đừng suy nghĩ quá nhiều, cảm giác đầu tiên thường chính xác nhất đấy 😊
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        cfg = load_dass21_vi()
        
        # 🔒 CRITICAL VALIDATION: Validate questionnaire config
        if not validate_app_state(cfg):
            st.error("⚠️ System error: Questionnaire configuration invalid. Please contact support.")
            st.stop()
            
        options = cfg["options"]
        
        if "answers" not in st.session_state:
            st.session_state.answers = {}
        
        # Enhanced form
        with st.form("dass21_form"):
            for i, item in enumerate(cfg["items"], 1):
                # Question card with optimized component
                create_question_card(i, item["text"])
                
                # Radio buttons với emoji tự định nghĩa
                emoji_options = ["😊", "😐", "😟", "😔"]
                option_labels = [f"{emoji_options[j]} {opt['label']}" for j, opt in enumerate(options)]
                
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
            
            # Submit button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button(
                    "🎯 Xem kết quả ngay!", 
                    use_container_width=True,
                    type="primary"
                )
            
            if submitted:
                # 🔒 CRITICAL VALIDATION: Validate user answers
                if not validate_app_state(cfg, st.session_state.answers):
                    st.error("⚠️ Invalid responses detected. Please review your answers.")
                    st.stop()
                    
                if len(st.session_state.answers) == len(cfg["items"]):
                    scores = score_dass21(st.session_state.answers, cfg)
                    
                    # 🔒 CRITICAL VALIDATION: Validate computed scores
                    if not validate_app_state(cfg, st.session_state.answers, scores):
                        logger.error("Score validation failed for user session")
                        st.error("⚠️ Score calculation error. Please try again or contact support.")
                        st.stop()
                        
                    # Log successful assessment completion
                    logger.info(f"Assessment completed successfully. Scores: {[(k, v.severity) for k, v in scores.items()]}")
                    
                    st.session_state.scores = {k: v.__dict__ for k, v in scores.items()}
                    
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                        color: white;
                        padding: 2rem;
                        border-radius: 20px;
                        text-align: center;
                        margin: 1rem 0;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">🎊</div>
                        <h3 style="margin: 0; color: white;">Hoàn thành! Đang tính toán kết quả...</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("⚠️ Hãy trả lời hết các câu hỏi nhé! Chỉ còn thiếu một chút thôi! 😊")
    
    else:
        # Show results with optimized components
        create_progress_indicator(
            current_step=3, 
            total_steps=3, 
            title="Kết quả đánh giá"
        )
        
        create_results_header()
        
        scores = st.session_state.scores
        df = pd.DataFrame(scores).T
        
        # Create metrics row
        col1, col2, col3 = st.columns(3)
        
        def get_severity_color(severity):
            severity_map = {
                'Normal': 'var(--success-500)',
                'Mild': 'var(--warning-500)',
                'Moderate': 'var(--error-500)',
                'Severe': 'var(--error-600)',
                'Extremely severe': 'var(--error-700)'
            }
            return severity_map.get(severity, severity_map['Normal'])
        
        def get_mood_emoji(severity):
            if severity in ['Normal', 'Mild']:
                return '😊'
            elif severity == 'Moderate':
                return '😐'
            elif severity == 'Severe':
                return '😔'
            else:
                return '😭'
        
        with col1:
            depression_score = df.loc['Depression', 'adjusted']
            depression_severity = df.loc['Depression', 'severity']
            color = get_severity_color(depression_severity)
            emoji = get_mood_emoji(depression_severity)
            
            create_metric_card("😔 Trầm cảm", depression_score, depression_severity, emoji, color)
        
        with col2:
            anxiety_score = df.loc['Anxiety', 'adjusted']
            anxiety_severity = df.loc['Anxiety', 'severity']
            color = get_severity_color(anxiety_severity)
            emoji = get_mood_emoji(anxiety_severity)
            
            create_metric_card("😰 Lo âu", anxiety_score, anxiety_severity, emoji, color)
        
        with col3:
            stress_score = df.loc['Stress', 'adjusted']
            stress_severity = df.loc['Stress', 'severity']
            color = get_severity_color(stress_severity)
            emoji = get_mood_emoji(stress_severity)
            
            create_metric_card("😓 Stress", stress_score, stress_severity, emoji, color)
        
        # Quick recommendations
        st.markdown("""
        <div class="recommendation-section">
            <div style="display: flex; align-items: center; margin-bottom: var(--spacing-md);">
                <div style="font-size: 3rem; margin-right: var(--spacing-sm);">💡</div>
                <div>
                    <h3 style="margin: 0; color: var(--success-600);">Lời khuyên nhỏ từ tôi</h3>
                    <p style="margin: 0.5rem 0 0 0; color: var(--success-500);">Dựa trên kết quả vừa rồi nhé!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
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
            recommendations = [
                "🌱 Hãy thử viết nhật ký cảm xúc mỗi ngày",
                "🧘‍♀️ Thực hành hít thở sâu 5 phút mỗi ngày",
                "🎵 Nghe nhạc thư giãn hoặc đi dạo trong công viên",
                "💤 Ngủ đủ 7-8 tiếng mỗi đêm"
            ]
            
            for rec in recommendations:
                create_recommendation_card(rec)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Action buttons
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
