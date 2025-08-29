import streamlit as st
import pandas as pd
import json
import os
import time
import logging
from datetime import datetime
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

# Initialize Smart UI Experience
smart_ui = SmartUIExperience()

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('soul_friend_advanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure page with advanced settings - GIỮ NGUYÊN GIAO DIỆN V1
st.set_page_config(
    page_title="SoulFriend V2.0 - Advanced Mental Health Support",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.who.int/mental_disorders',
        'Report a bug': None,
        'About': "SoulFriend V2.0 - Advanced Mental Health Support Platform 2025"
    }
)

# Load premium CSS with animations
load_premium_css()

# Initialize enhanced session state - GIỮ NGUYÊN LOGIC V1
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
if "selected_scales" not in st.session_state:
    st.session_state.selected_scales = ["DASS-21"]  # NEW: Multi-scale support
if "current_scale_index" not in st.session_state:
    st.session_state.current_scale_index = 0  # NEW: Track current scale

# Track page load
smart_ui.track_user_interaction("page_load", "main_app")

# Logo góc trái only - GIỮ NGUYÊN
col1, col2 = st.columns([1, 5])
with col1:
    display_logo(width=80, centered=False)

# Advanced Hero section - GIỮ NGUYÊN NHƯNG CẬP NHẬT CHỮ
create_smart_hero(
    title="SoulFriend V2.0",
    subtitle="Người bạn tâm hồn thông minh 🌟",
    description="Hỗ trợ sức khỏe tâm lý đa thang đo với AI và khoa học hiện đại 💝"
)

# Smart Mood Tracker - GIỮ NGUYÊN
create_smart_mood_tracker()

# NEW: Scale selection for V2.0
if not st.session_state.consent_given:
    st.markdown("### 🎯 Chọn thang đo đánh giá")
    
    # Available scales in V2.0
    available_scales = {
        "DASS-21": "Trầm cảm, Lo âu, Căng thẳng (21 câu)",
        "PHQ-9": "Sàng lọc trầm cảm (9 câu)", 
        "GAD-7": "Rối loạn lo âu tổng quát (7 câu)",
        "EPDS": "Trầm cảm sau sinh (10 câu)",
        "PSS-10": "Căng thẳng cảm nhận (10 câu)"
    }
    
    selected_scales = st.multiselect(
        "Chọn các thang đo bạn muốn thực hiện:",
        options=list(available_scales.keys()),
        default=["DASS-21"],
        format_func=lambda x: f"{x}: {available_scales[x]}"
    )
    
    if selected_scales:
        st.session_state.selected_scales = selected_scales
        st.success(f"✅ Đã chọn {len(selected_scales)} thang đo: {', '.join(selected_scales)}")
    else:
        st.warning("⚠️ Vui lòng chọn ít nhất một thang đo")

# Assessment intro - CẬP NHẬT CHO ĐA THANG ĐO
st.markdown("### 🧠 Đánh giá sức khỏe tâm thần")
if st.session_state.selected_scales:
    st.info(f"Sẽ thực hiện {len(st.session_state.selected_scales)} thang đo: {', '.join(st.session_state.selected_scales)}")
else:
    st.info("Công cụ đánh giá chuẩn quốc tế về sức khỏe tâm thần")

# Show disclaimer - GIỮ NGUYÊN
show_disclaimer()

# Clean Consent Flow - GIỮ NGUYÊN HOÀN TOÀN GIAO DIỆN V1
if not st.session_state.consent_given:
    
    # Kiểm tra xem có đang hiển thị bảng đồng thuận không
    if st.session_state.get("show_consent_agreement", False):
        create_consent_agreement_form()
    else:
        # Trang chính giới thiệu - GIỮ NGUYÊN
        st.markdown("## 🤝 Chào mừng đến với SoulFriend V2.0!")
        st.write("Hãy cùng khám phá và chăm sóc sức khỏe tâm lý của bạn với công nghệ mới nhất")
        
        # Use pure Streamlit columns instead of HTML - GIỮ NGUYÊN
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            🔐 **Bảo mật tuyệt đối**
            
            Dữ liệu được bảo vệ và không lưu trữ vĩnh viễn
            """)
        
        with col2:
            st.success("""
            🤖 **AI thông minh**
            
            Phân tích đa thang đo và đưa ra lời khuyên cá nhân hóa
            """)
        
        with col3:
            st.warning("""
            🏥 **Chuẩn y khoa**
            
            Sử dụng nhiều thang đo được công nhận quốc tế
            """)
        
        # Enhanced consent interaction - GIỮ NGUYÊN
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
    # Assessment or Results Flow - CẬP NHẬT CHO ĐA THANG ĐO
    if not st.session_state.get("scores"):
        # NEW: Multi-scale progress tracking
        current_scale = st.session_state.selected_scales[st.session_state.current_scale_index]
        total_scales = len(st.session_state.selected_scales)
        
        create_progress_ring(
            st.session_state.current_scale_index + 1, 
            total_scales, 
            f"Đánh giá {current_scale}"
        )
        
        # Assessment header - CẬP NHẬT CHO SCALE HIỆN TẠI
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"### 📝 {current_scale}")
            st.info(f"🎯 Thang đo {st.session_state.current_scale_index + 1}/{total_scales}")
        
        # Load questionnaire based on current scale
        if current_scale == "DASS-21":
            show_dass21_assessment_v2()
        else:
            # NEW: Other scales (placeholder for now)
            st.warning(f"🔄 Thang đo {current_scale} đang được phát triển")
            st.markdown(f"### Tính năng {current_scale} sẽ có trong Sprint 2")
            
            if st.button("⏭️ Bỏ qua thang đo này", type="secondary"):
                # Move to next scale
                if st.session_state.current_scale_index < len(st.session_state.selected_scales) - 1:
                    st.session_state.current_scale_index += 1
                    st.rerun()
                else:
                    # All scales completed
                    st.session_state.scores = {"placeholder": "completed"}
                    st.rerun()
    
    else:
        # Results Dashboard - GIỮ NGUYÊN GIAO DIỆN V1
        create_progress_ring(len(st.session_state.selected_scales), len(st.session_state.selected_scales), "Hoàn thành")
        
        if hasattr(st.session_state, 'dass21_scores') and st.session_state.dass21_scores:
            create_smart_results_dashboard(st.session_state.dass21_scores)
            
            scores = st.session_state.dass21_scores
            # Convert SubscaleScore objects to dict for DataFrame
            scores_dict = {}
            for subscale, score_obj in scores.items():
                scores_dict[subscale] = {
                    'raw': score_obj.raw,
                    'adjusted': score_obj.adjusted,
                    'severity': score_obj.severity
                }
            df = pd.DataFrame(scores_dict).T
            
            # Metrics display - GIỮ NGUYÊN
            st.markdown("### 📊 Kết quả chi tiết")
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
            
            # Recommendations - GIỮ NGUYÊN
            st.markdown("### � Gợi ý cho bạn")
            scores_dict = {}
            for key, value in st.session_state.dass21_scores.items():
                if hasattr(value, 'adjusted'):
                    scores_dict[key] = {'adjusted': value.adjusted, 'severity': value.severity}
                else:
                    scores_dict[key] = value
            create_smart_recommendations(scores_dict)
            
            # Action buttons - GIỮ NGUYÊN
            create_smart_action_buttons()
            
            # User journey summary - GIỮ NGUYÊN
            create_user_journey_summary()
        else:
            st.success("🎉 Đánh giá hoàn thành!")
            st.info("Kết quả chi tiết sẽ hiển thị khi các thang đo được triển khai đầy đủ")

def show_dass21_assessment_v2():
    """Enhanced DASS-21 assessment for V2.0 - GIỮ NGUYÊN GIAO DIỆN V1"""
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
    
    # Enhanced questionnaire form - GIỮ NGUYÊN HOÀN TOÀN
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
        
        # Submit section - GIỮ NGUYÊN
        st.markdown("### 🎯 Hoàn thành đánh giá")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            answered_count = len(st.session_state.answers)
            completion_rate = (answered_count / total_questions) * 100
            
            st.progress(completion_rate / 100)
            st.caption(f"Đã trả lời: {answered_count}/{total_questions} câu")
            
            # NEW: Update button text for multi-scale
            total_scales = len(st.session_state.selected_scales)
            current_scale_num = st.session_state.current_scale_index + 1
            
            if current_scale_num < total_scales:
                button_text = f"🎊 Tiếp tục thang đo tiếp theo ({current_scale_num + 1}/{total_scales})"
            else:
                button_text = "🎊 Xem kết quả"
            
            submitted = st.form_submit_button(
                button_text, 
                use_container_width=True,
                type="primary",
                disabled=(answered_count < total_questions)
            )
    
    # Process results - CẬP NHẬT CHO ĐA THANG ĐO
    if submitted:
        if len(st.session_state.answers) < len(cfg["items"]):
            st.warning("🤔 Hãy trả lời tất cả câu hỏi!")
            st.stop()
        
        with st.spinner("🧠 Đang phân tích kết quả..."):
            time.sleep(2)
            
            scores = score_dass21(st.session_state.answers, cfg)
            if scores:
                st.session_state.dass21_scores = scores  # Save DASS-21 scores specifically
                smart_ui.track_user_interaction("assessment_completed", "dass21_form", scores)
                logger.info(f"DASS-21 assessment completed. Scores: {scores}")
                
                st.success("✅ DASS-21 phân tích hoàn tất!")
                
                # NEW: Move to next scale or results
                if st.session_state.current_scale_index < len(st.session_state.selected_scales) - 1:
                    st.session_state.current_scale_index += 1
                    st.info(f"🔄 Chuyển sang thang đo tiếp theo...")
                    time.sleep(1)
                    st.rerun()
                else:
                    # All scales completed
                    st.session_state.scores = {"completed": True}
                    time.sleep(1)
                    st.rerun()
            else:
                logger.error("Score calculation failed")
                st.error("⚠️ Có lỗi trong tính toán. Vui lòng thử lại.")

# Clean footer - GIỮ NGUYÊN
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("SoulFriend V2.0 2025 - Hỗ trợ sức khỏe tâm lý thông minh đa thang đo")
