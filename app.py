"""
SOULFRIEND - Mental Health Support App
Main entry point for Streamlit Cloud deployment
"""

import streamlit as st
import pandas as pd
import json
import os
import time
import logging
import sys
from datetime import datetime

# Add the app directory to Python path for imports
app_dir = os.path.join(os.path.dirname(__file__), 'mental-health-support-app', 'mental-health-support-app')
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import components
try:
    from components.ui import app_header, show_disclaimer, display_logo
    from components.ui_advanced import (
        SmartUIExperience, load_premium_css, create_smart_hero,
        create_smart_mood_tracker, create_progress_ring, 
        create_smart_question_card, create_smart_results_dashboard,
        create_smart_metric_card, create_smart_recommendations,
        create_smart_action_buttons, create_user_journey_summary,
        show_smart_notifications, create_consent_agreement_form
    )
    from components.questionnaires import load_dass21_vi
    from components.scoring import score_dass21
    from components.validation import validate_app_state
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Initialize Smart UI Experience
smart_ui = SmartUIExperience()

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only console logging for cloud
    ]
)
logger = logging.getLogger(__name__)

# Configure page with advanced settings
st.set_page_config(
    page_title="SoulFriend - Advanced Mental Health Support",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.who.int/mental_disorders',
        'Report a bug': None,
        'About': "SoulFriend - Advanced Mental Health Support Platform 2025"
    }
)

# Load premium CSS with animations
load_premium_css()

# Initialize enhanced session state
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False
if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False
if "show_consent_agreement" not in st.session_state:
    st.session_state.show_consent_agreement = False
if "consent_agreement_completed" not in st.session_state:
    st.session_state.consent_agreement_completed = False
if "user_journey_start" not in st.session_state:
    st.session_state.user_journey_start = datetime.now().isoformat()

# Track page load
smart_ui.track_user_interaction("page_load", "main_app")

# Logo góc trái only
col1, col2 = st.columns([1, 5])
with col1:
    display_logo(width=80, centered=False)

# Advanced Hero section
create_smart_hero(
    title="SoulFriend",
    subtitle="Người bạn tâm hồn thông minh 🌟",
    description="Hỗ trợ sức khỏe tâm lý với AI và khoa học hiện đại 💝"
)

# Smart Mood Tracker
create_smart_mood_tracker()

# Simple Assessment intro (no code text)
st.markdown("### 🧠 Đánh giá DASS-21")
st.info("Công cụ đánh giá chuẩn quốc tế về trầm cảm, lo âu và căng thẳng")

# Show disclaimer
show_disclaimer()

# Clean Consent Flow - No HTML code
if not st.session_state.consent_given:
    
    # Kiểm tra xem có đang hiển thị bảng đồng thuận không
    if st.session_state.get("show_consent_agreement", False):
        create_consent_agreement_form()
    else:
        # Trang chính giới thiệu
        st.markdown("## 🤝 Chào mừng đến với SoulFriend!")
        st.write("Hãy cùng khám phá và chăm sóc sức khỏe tâm lý của bạn")
        
        # Use pure Streamlit columns instead of HTML
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            🔐 **Bảo mật tuyệt đối**
            
            Dữ liệu được bảo vệ và không lưu trữ vĩnh viễn
            """)
        
        with col2:
            st.success("""
            🤖 **AI thông minh**
            
            Phân tích kết quả và đưa ra lời khuyên cá nhân hóa
            """)
        
        with col3:
            st.warning("""
            🏥 **Chuẩn y khoa**
            
            Sử dụng thang đo DASS-21 được công nhận quốc tế
            """)
        
        # Enhanced consent interaction
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            consent_options = st.radio(
                "Bạn có đồng ý tham gia đánh giá?",
                ["🤔 Cần suy nghĩ thêm", "✨ Sẵn sàng bắt đầu!"],
                key="consent_radio"
            )
            
            if consent_options == "✨ Sẵn sàng bắt đầu!":
                if st.button(
                    "📋 Xem bảng đồng thuận", 
                    use_container_width=True,
                    type="primary",
                    help="Đọc và xác nhận các điều khoản trước khi bắt đầu"
                ):
                    smart_ui.track_user_interaction("consent_initial", "consent_form", True)
                    logger.info("User requested to see consent agreement")
                    
                    st.session_state.show_consent_agreement = True
                    st.rerun()
            else:
                st.info("🕰️ Hãy dành thời gian suy nghĩ. SoulFriend sẽ luôn ở đây!")

else:
    # Assessment or Results Flow
    if not st.session_state.get("scores"):
        # Smart progress tracking
        create_progress_ring(2, 3, "Đánh giá DASS-21")
        
        # Assessment header with clean Streamlit components
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 📝 Câu hỏi về tâm lý")
            st.info("🎯 Trả lời thật lòng để có kết quả chính xác nhất")
        
        # Load questionnaire
        cfg = load_dass21_vi()
        if not cfg:
            logger.error("Failed to load DASS-21 configuration")
            st.error("⚠️ Không thể tải bộ câu hỏi. Vui lòng thử lại.")
            st.stop()
            
        options = cfg["options"]
        total_questions = len(cfg["items"])
        
        if "answers" not in st.session_state:
            st.session_state.answers = {}
        
        # Enhanced questionnaire form
        with st.form("dass21_smart_form"):
            for i, item in enumerate(cfg["items"], 1):
                # Smart question card
                create_smart_question_card(i, item["text"], total_questions)
                
                # Enhanced radio options
                col1, col2 = st.columns([1, 3])
                
                with col2:
                    emoji_options = ["😊", "😐", "😟", "😔"]
                    option_labels = [f"{emoji_options[j]} {opt['label']}" for j, opt in enumerate(options)]
                    
                    answer = st.radio(
                        f"Câu hỏi {i}",
                        options=range(len(options)),
                        format_func=lambda x: option_labels[x],
                        key=f"smart_q_{i}",
                        label_visibility="collapsed",
                        horizontal=True
                    )
                    
                    if answer is not None:
                        st.session_state.answers[item["id"]] = answer
                        smart_ui.track_user_interaction("answer_question", f"question_{i}", answer)
                
                if i < total_questions:
                    st.markdown("---")
            
            # Submit section
            st.markdown("### 🎯 Hoàn thành đánh giá")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                answered_count = len(st.session_state.answers)
                completion_rate = (answered_count / total_questions) * 100
                
                st.progress(completion_rate / 100)
                st.caption(f"Đã trả lời: {answered_count}/{total_questions} câu")
                
                submitted = st.form_submit_button(
                    "🎊 Xem kết quả", 
                    use_container_width=True,
                    type="primary",
                    disabled=(answered_count < total_questions)
                )
        
        # Process results
        if submitted:
            if len(st.session_state.answers) < len(cfg["items"]):
                st.warning("🤔 Hãy trả lời tất cả câu hỏi!")
                st.stop()
            
            with st.spinner("🧠 Đang phân tích kết quả..."):
                time.sleep(2)
                
                scores = score_dass21(st.session_state.answers)
                if scores:
                    st.session_state.scores = scores
                    smart_ui.track_user_interaction("assessment_completed", "dass21_form", scores)
                    logger.info(f"Assessment completed. Scores: {scores}")
                    
                    validation_result = validate_app_state(st.session_state)
                    if not validation_result["is_valid"]:
                        logger.error(f"Validation failed: {validation_result['errors']}")
                        st.error("⚠️ Lỗi validation. Vui lòng thử lại.")
                        st.stop()
                    
                    st.success("✅ Phân tích hoàn tất!")
                    time.sleep(1)
                    st.rerun()
                else:
                    logger.error("Score calculation failed")
                    st.error("⚠️ Có lỗi trong tính toán. Vui lòng thử lại.")
    
    else:
        # Results Dashboard
        create_progress_ring(3, 3, "Kết quả")
        
        create_smart_results_dashboard(st.session_state.scores)
        
        scores = st.session_state.scores
        df = pd.DataFrame(scores).T
        
        # Metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            depression_score = df.loc['Depression', 'adjusted']
            depression_severity = df.loc['Depression', 'severity']
            create_smart_metric_card("Trầm cảm", depression_score, depression_severity, "😔")
        
        with col2:
            anxiety_score = df.loc['Anxiety', 'adjusted']
            anxiety_severity = df.loc['Anxiety', 'severity'] 
            create_smart_metric_card("Lo âu", anxiety_score, anxiety_severity, "😰")
        
        with col3:
            stress_score = df.loc['Stress', 'adjusted']
            stress_severity = df.loc['Stress', 'severity']
            create_smart_metric_card("Căng thẳng", stress_score, stress_severity, "😓")
        
        # Recommendations
        st.markdown("### 💡 Gợi ý cho bạn")
        create_smart_recommendations(st.session_state.scores)
        
        # Action buttons
        create_smart_action_buttons()
        
        # User journey summary
        create_user_journey_summary()

# Clean footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("SoulFriend 2025 - Hỗ trợ sức khỏe tâm lý thông minh")
