import streamlit as st
import pandas as pd
import json
import os
import time
import logging
from datetime import datetime
from components.ui import app_header, show_disclaimer, display_logo
from components.charts import display_enhanced_charts, create_summary_statistics
from components.pdf_export import create_download_button, create_email_report_option, generate_assessment_report
from components.ui_advanced import (
    SmartUIExperience, load_premium_css, create_smart_hero,
    create_smart_mood_tracker, create_progress_ring, 
    create_smart_question_card, create_smart_results_dashboard,
    create_smart_metric_card, create_smart_recommendations,
    create_smart_action_buttons, create_user_journey_summary,
    show_smart_notifications, create_consent_agreement_form
)
from components.questionnaires import load_questionnaire, QuestionnaireManager
from components.scoring import calculate_scores, score_phq9_enhanced, score_gad7_enhanced, score_dass21_enhanced, score_epds_enhanced, score_pss10_enhanced
from components.ui import load_css, app_header
from components.charts import create_charts_interface
from components.pdf_export import generate_assessment_report
from components.validation import validate_app_state

# 🔬 RESEARCH SYSTEM INTEGRATION - Safe & Optional
try:
    from research_system.integration import (
        safe_track_session_start,
        safe_track_questionnaire_start,
        safe_track_question_answer,
        safe_track_questionnaire_completion,
        safe_track_results_view
    )
    from research_system.consent_ui import render_research_consent_section
    RESEARCH_SYSTEM_AVAILABLE = True
    print("🔬 Research system integration: ENABLED")
except ImportError as e:
    # Graceful fallback - app works normally without research system
    def safe_track_session_start(**kwargs): pass
    def safe_track_questionnaire_start(*args, **kwargs): pass
    def safe_track_question_answer(*args, **kwargs): pass
    def safe_track_questionnaire_completion(*args, **kwargs): pass
    def safe_track_results_view(*args, **kwargs): pass
    def render_research_consent_section(): return None
    RESEARCH_SYSTEM_AVAILABLE = False
    print("🔬 Research system: DISABLED (graceful fallback)")

# Setup enhanced logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('soul_friend_advanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Log research system status after logger is initialized
if RESEARCH_SYSTEM_AVAILABLE:
    logger.info("🔬 Research system integration: ENABLED")
else:
    logger.info("🔬 Research system: DISABLED (graceful fallback)")

# Enhanced components imports
try:
    from components.enhanced_navigation import create_enhanced_navigation, apply_responsive_design
    from components.data_export import display_export_options, DataExportSystem
    from components.data_backup import auto_backup_session, DataBackupSystem
    ENHANCED_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced components not available: {e}")
    ENHANCED_COMPONENTS_AVAILABLE = False

# Initialize Smart UI Experience
smart_ui = SmartUIExperience()

# Configure page with advanced settings
# Set page configuration
st.set_page_config(
    page_title="SOULFRIEND V2.0",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔬 RESEARCH CONSENT SECTION (Optional & Non-blocking)
if RESEARCH_SYSTEM_AVAILABLE:
    try:
        # Show research consent in sidebar (non-intrusive)
        with st.sidebar:
            st.markdown("---")
            research_consent = render_research_consent_section()
            if research_consent is not None:
                st.session_state["research_consent"] = research_consent
                if research_consent:
                    st.success("🔬 Đã đồng ý tham gia nghiên cứu")
                    # Track consent given
                    safe_track_session_start(consent_given=True)
                else:
                    st.info("ℹ️ Không tham gia nghiên cứu")
    except Exception as e:
        # Silent fail - don't affect main app
        logger.debug(f"Research consent UI error: {e}")

# Helper functions for AI integration
def create_risk_assessment(scores):
    """Create risk assessment from scores"""
    total_score = 0
    score_count = 0
    
    # Calculate average risk across all scores
    for key, value in (scores.items() if hasattr(scores, 'items') else scores):
        if isinstance(value, (int, float)) and key.endswith(('_total', '_depression', '_anxiety', '_stress')):
            total_score += value
            score_count += 1
    
    if score_count > 0:
        avg_score = total_score / score_count
        if avg_score >= 20:
            return "Rủi ro rất cao - Cần hỗ trợ chuyên nghiệp ngay lập tức"
        elif avg_score >= 15:
            return "Rủi ro cao - Nên tìm kiếm hỗ trợ chuyên nghiệp"
        elif avg_score >= 8:
            return "Rủi ro trung bình - Theo dõi và tự chăm sóc"
        else:
            return "Rủi ro thấp - Duy trì lối sống lành mạnh"
    
    return "Cần đánh giá thêm"

def get_ai_recommendations(scores):
    """Get AI-based recommendations from scores"""
    recommendations = []
    
    # Basic recommendations based on scores
    for key, value in (scores.items() if hasattr(scores, 'items') else scores):
        if isinstance(value, (int, float)):
            if 'depression' in key and value >= 15:
                recommendations.append("Tham gia hoạt động xã hội và liệu pháp tâm lý")
            elif 'anxiety' in key and value >= 12:
                recommendations.append("Thực hành kỹ thuật thư giãn và mindfulness")
            elif 'stress' in key and value >= 18:
                recommendations.append("Quản lý thời gian và giảm tải công việc")
    
    if not recommendations:
        recommendations = [
            "Duy trì lối sống lành mạnh",
            "Tập thể dục đều đặn", 
            "Ngủ đủ giấc 7-9 tiếng/đêm"
        ]
    
    return recommendations

# Enhanced scoring functions (simplified versions)
def load_dass21_enhanced_vi():
    """Load DASS-21 enhanced configuration"""
    return load_questionnaire("DASS-21")

def load_phq9_enhanced_vi():
    """Load PHQ-9 enhanced configuration"""
    return load_questionnaire("PHQ-9")

def load_gad7_enhanced_vi():
    """Load GAD-7 enhanced configuration"""
    return load_questionnaire("GAD-7")

def load_epds_enhanced_vi():
    """Load EPDS enhanced configuration"""
    return load_questionnaire("EPDS")

def load_pss10_enhanced_vi():
    """Load PSS-10 enhanced configuration"""
    return load_questionnaire("PSS-10")

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

# Questionnaire Selection
st.markdown("### 🧠 Chọn bộ đánh giá tâm lý")

# Initialize questionnaire type in session state
if "questionnaire_type" not in st.session_state:
    st.session_state.questionnaire_type = "DASS-21"

# Questionnaire selection
questionnaire_type = st.selectbox(
    "Chọn loại đánh giá phù hợp:",
    ["DASS-21", "PHQ-9", "GAD-7", "EPDS", "PSS-10"],
    key="questionnaire_selector",
    help="DASS-21: Tổng hợp | PHQ-9: Trầm cảm | GAD-7: Lo âu | EPDS: Sau sinh | PSS-10: Căng thẳng"
)

# Store selection in session state
st.session_state.questionnaire_type = questionnaire_type

# Display questionnaire info
if questionnaire_type == "DASS-21":
    st.info("📊 **DASS-21**: Đánh giá toàn diện về trầm cảm, lo âu và căng thẳng")
    st.markdown("**Đặc điểm:** 21 câu hỏi, 3 lĩnh vực chính, thời gian 5-7 phút")
elif questionnaire_type == "PHQ-9":
    st.info("🎯 **PHQ-9**: Chuyên sâu về triệu chứng trầm cảm")
    st.markdown("**Đặc điểm:** 9 câu hỏi, đánh giá nguy cơ tự sát, thời gian 3-5 phút")
elif questionnaire_type == "GAD-7":
    st.info("😰 **GAD-7**: Chuyên sâu về triệu chứng lo âu")
    st.markdown("**Đặc điểm:** 7 câu hỏi, đánh giá lo âu tổng quát, thời gian 3-5 phút")
elif questionnaire_type == "EPDS":
    st.info("🤱 **EPDS**: Chuyên về trầm cảm sau sinh và trong thai kỳ")
    st.markdown("**Đặc điểm:** 10 câu hỏi, dành cho mẹ bầu và sau sinh, thời gian 5-7 phút")
elif questionnaire_type == "PSS-10":
    st.info("😤 **PSS-10**: Chuyên về căng thẳng cảm nhận")
    st.markdown("**Đặc điểm:** 10 câu hỏi, đánh giá stress chủ quan, thời gian 5-7 phút")

# Show disclaimer
show_disclaimer()

# Clean Consent Flow - No HTML code
if not st.session_state.consent_given:
    
    # Kiểm tra xem có đang hiển thị bảng đồng thuận không
    if st.session_state.get("show_consent_agreement", False):
        # Main consent form
        create_consent_agreement_form()
        
        # ===== RESEARCH CONSENT SECTION (OPTIONAL) =====
        try:
            from research_system.consent_ui import render_research_consent_section, set_research_consent_status
            
            # Render research consent section if system is available
            st.markdown("---")
            research_consent = render_research_consent_section()
            
            # Save research consent status
            if research_consent is not None:
                set_research_consent_status(research_consent)
                
        except ImportError:
            # Research system not available - skip silently
            pass
        except Exception:
            # Any other error - skip silently
            pass
        # ===== END RESEARCH CONSENT SECTION =====
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
                    "� Xem bảng đồng thuận", 
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
    # Debug session state
    logger.info(f"Session state check - scores: {st.session_state.get('scores', 'None')}, enhanced_scores: {'enhanced_scores' in st.session_state}")
    
    # Check if results exist and offer to show them
    if st.session_state.get("enhanced_scores"):
        st.success("🎯 Kết quả đánh giá đã sẵn sàng!")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📊 Xem kết quả đã lưu", use_container_width=True, type="primary"):
                # Force show results by setting flag
                st.session_state.force_show_results = True
                st.rerun()
    
    if not st.session_state.get("scores") and not st.session_state.get("enhanced_scores") and not st.session_state.get("force_show_results"):
        # Get current questionnaire type
        current_questionnaire = st.session_state.get("questionnaire_type", "DASS-21")
        
        # Smart progress tracking
        create_progress_ring(2, 3, f"Đánh giá {current_questionnaire}")
        
        # Assessment header with clean Streamlit components
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 📝 Câu hỏi về tâm lý")
            st.info(f"🎯 Đánh giá {current_questionnaire} - Trả lời thật lòng để có kết quả chính xác nhất")
        
        # Load appropriate questionnaire configuration
        if current_questionnaire == "DASS-21":
            cfg = load_dass21_enhanced_vi()
        elif current_questionnaire == "PHQ-9":
            cfg = load_phq9_enhanced_vi()
        elif current_questionnaire == "GAD-7":
            cfg = load_gad7_enhanced_vi()
        elif current_questionnaire == "EPDS":
            cfg = load_epds_enhanced_vi()
        elif current_questionnaire == "PSS-10":
            cfg = load_pss10_enhanced_vi()
        else:
            cfg = load_dass21_enhanced_vi()  # Default fallback
            
        if not cfg:
            logger.error(f"Failed to load {current_questionnaire} enhanced configuration")
            st.error(f"⚠️ Không thể tải bộ câu hỏi {current_questionnaire}. Vui lòng thử lại.")
            st.stop()
            
        # Ensure cfg has required keys
        if "options" not in cfg:
            logger.warning(f"No 'options' found in {current_questionnaire} config, using default")
            cfg["options"] = [
                {"value": 0, "label": "0 - Không bao giờ", "emoji": "😌"},
                {"value": 1, "label": "1 - Thỉnh thoảng", "emoji": "😐"},
                {"value": 2, "label": "2 - Khá thường xuyên", "emoji": "😕"},
                {"value": 3, "label": "3 - Hầu hết thời gian", "emoji": "😰"}
            ]
        
        if "items" not in cfg and "questions" in cfg:
            cfg["items"] = cfg["questions"]  # Compatibility
        
        # Ensure instructions exist
        if "instructions" not in cfg:
            cfg["instructions"] = {
                "title": f"Hướng dẫn {current_questionnaire}",
                "content": "Vui lòng đọc kỹ từng câu hỏi và chọn đáp án phù hợp nhất với tình trạng của bạn.",
                "time_frame": "trong 2 tuần qua"
            }
            
        options = cfg["options"]
        total_questions = len(cfg.get("items", cfg.get("questions", [])))
        
        # Show enhanced instructions
        with st.expander("📖 Hướng dẫn trả lời", expanded=False):
            # Safe access to config instructions
            instructions = cfg.get('instructions', {})
            title = instructions.get('title', 'Hướng dẫn trả lời')
            content = instructions.get('content', 'Vui lòng trả lời các câu hỏi một cách chân thật nhất.')
            time_frame = instructions.get('time_frame', 'Khoảng 5-10 phút')
            
            st.markdown(f"**{title}**")
            st.write(content)
            st.write(f"**Thời gian đánh giá:** {time_frame}")
            
            # Show tips if available
            tips = instructions.get('tips', [])
            if tips:
                for tip in tips:
                    st.write(f"• {tip}")
            else:
                st.write("• Hãy suy nghĩ về tình trạng của bạn trong 2 tuần gần đây")
                st.write("• Trả lời một cách chân thật để có kết quả chính xác nhất")
        
        if "answers" not in st.session_state:
            st.session_state.answers = {}
        
        # Enhanced questionnaire form with dynamic name
        current_questionnaire = st.session_state.get("questionnaire_type", "DASS-21")
        form_name = f"{current_questionnaire.lower().replace('-', '_')}_enhanced_form"
        
        with st.form(form_name):
            for i, item in enumerate(cfg["items"], 1):
                # Enhanced question card with context
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                           padding: 20px; border-radius: 15px; margin: 10px 0; 
                           border-left: 4px solid #007bff;">
                    <h4 style="color: #007bff; margin: 0 0 10px 0;">
                        📝 Câu hỏi {i}/{total_questions}
                    </h4>
                    <p style="font-size: 18px; margin: 10px 0; color: #2c3e50;">
                        <strong>{item["text"]}</strong>
                    </p>
                    <small style="color: #6c757d; font-style: italic;">
                        💡 {item.get("vietnamese_context", "")}<br>
                        🏷️ Thuộc về: {item.get("subscale", item.get("domain", "Tâm lý"))} - {item.get("category", "")}
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced radio options with emojis and descriptions
                col1, col2 = st.columns([1, 4])
                
                with col2:
                    option_labels = []
                    for j, opt in enumerate(options):
                        emoji = opt.get("emoji", "🔘")
                        label = opt["label"]
                        desc = opt.get("description", "")
                        option_labels.append(f"{emoji} {label}")
                    
                    answer = st.radio(
                        f"Mức độ áp dụng cho bạn:",
                        options=range(len(options)),
                        format_func=lambda x: option_labels[x],
                        key=f"enhanced_q_{i}",
                        horizontal=False,
                        help="Chọn mức độ phù hợp nhất với tình trạng của bạn trong tuần vừa qua"
                    )
                    
                    # Show description for selected option
                    if answer is not None:
                        st.session_state.answers[item["id"]] = answer
                        selected_opt = options[answer]
                        if "description" in selected_opt:
                            st.info(f"💭 {selected_opt['description']}")
                        smart_ui.track_user_interaction("answer_enhanced_question", f"question_{i}", answer)
                
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
                
                # Debug info
                if answered_count >= total_questions:
                    st.success("✅ Đã hoàn thành tất cả câu hỏi!")
                else:
                    st.warning(f"⚠️ Còn lại {total_questions - answered_count} câu hỏi")
                
                submitted = st.form_submit_button(
                    "🎊 Xem kết quả", 
                    use_container_width=True,
                    type="primary",
                    disabled=(answered_count < total_questions)
                )
                
                # Debug logging
                if submitted:
                    logger.info(f"Button submitted! Answers: {len(st.session_state.answers)}, Required: {total_questions}")
                    st.success("✅ Button được bấm! Đang xử lý...")
                    
        # Alternative button outside form for testing
        if len(st.session_state.answers) >= total_questions:
            st.markdown("---")
            st.markdown("### 🔧 Phương án dự phòng")
            if st.button("🚀 Xử lý kết quả (Bypass)", type="secondary", key="bypass_button"):
                st.session_state.force_process = True
                st.rerun()
        
        # Process enhanced results
        if submitted or st.session_state.get("force_process", False):
            if st.session_state.get("force_process", False):
                st.session_state.force_process = False  # Reset flag
                logger.info("Processing via bypass button")
            
            logger.info(f"Processing submission for {current_questionnaire}")
            st.info(f"🔄 Đang xử lý {current_questionnaire}...")
            
            if len(st.session_state.answers) < len(cfg["items"]):
                st.warning("🤔 Hãy trả lời tất cả câu hỏi để có kết quả chính xác nhất!")
                logger.warning(f"Incomplete answers: {len(st.session_state.answers)}/{len(cfg['items'])}")
                st.stop()
            
            try:
                with st.spinner("🧠 Đang phân tích kết quả nâng cao..."):
                    time.sleep(1)  # Reduced delay
                    
                    # Use enhanced scoring based on questionnaire type
                    logger.info(f"Starting enhanced scoring for {current_questionnaire}")
                    
                    if current_questionnaire == "DASS-21":
                        enhanced_result = score_dass21_enhanced(st.session_state.answers, cfg)
                        track_event = "dass21_enhanced"
                    elif current_questionnaire == "PHQ-9":
                        enhanced_result = score_phq9_enhanced(st.session_state.answers, cfg)
                        track_event = "phq9_enhanced"
                    elif current_questionnaire == "GAD-7":
                        enhanced_result = score_gad7_enhanced(st.session_state.answers, cfg)
                        track_event = "gad7_enhanced"
                    elif current_questionnaire == "EPDS":
                        enhanced_result = score_epds_enhanced(st.session_state.answers, cfg)
                        track_event = "epds_enhanced"
                    elif current_questionnaire == "PSS-10":
                        enhanced_result = score_pss10_enhanced(st.session_state.answers, cfg)
                        track_event = "pss10_enhanced"
                    else:
                        enhanced_result = score_dass21_enhanced(st.session_state.answers, cfg)
                        track_event = "dass21_enhanced"
                    
                    if enhanced_result:
                        # Convert EnhancedAssessmentResult object to dict for session state
                        if hasattr(enhanced_result, '__dict__'):
                            # Convert object to dict
                            enhanced_dict = {
                                'total_score': enhanced_result.total_score,
                                'severity_level': enhanced_result.severity_level,
                                'interpretation': enhanced_result.interpretation,
                                'recommendations': enhanced_result.recommendations,
                                'subscales': {}
                            }
                            
                            # Convert subscales properly
                            if hasattr(enhanced_result, 'subscales') and enhanced_result.subscales:
                                for subscale_name, subscale_obj in enhanced_result.subscales.items():
                                    if hasattr(subscale_obj, '__dict__'):
                                        enhanced_dict['subscales'][subscale_name] = {
                                            'raw': subscale_obj.raw,
                                            'adjusted': subscale_obj.adjusted,
                                            'severity': subscale_obj.severity,
                                            'color': getattr(subscale_obj, 'color', 'green'),
                                            'level_info': getattr(subscale_obj, 'level_info', {})
                                        }
                                    else:
                                        enhanced_dict['subscales'][subscale_name] = subscale_obj
                            
                            st.session_state.enhanced_scores = enhanced_dict
                        else:
                            st.session_state.enhanced_scores = enhanced_result
                            
                        st.session_state.questionnaire_used = current_questionnaire
                        
                        # 🔬 RESEARCH TRACKING: Questionnaire completion
                        if RESEARCH_SYSTEM_AVAILABLE:
                            try:
                                # Track questionnaire completion
                                if hasattr(enhanced_result, 'total_score'):
                                    total_score = enhanced_result.total_score
                                else:
                                    total_score = enhanced_dict.get('total_score', 0) if isinstance(enhanced_dict, dict) else 0
                                
                                safe_track_questionnaire_completion(
                                    current_questionnaire, 
                                    total_score
                                )
                                logger.info(f"🔬 Tracked questionnaire completion: {current_questionnaire}")
                            except Exception as e:
                                logger.debug(f"Research tracking error: {e}")
                        
                        # Extract values for logging (check both object and dict)
                        if hasattr(enhanced_result, 'total_score'):
                            total_score = enhanced_result.total_score
                            severity_level = enhanced_result.severity_level
                            interpretation = enhanced_result.interpretation
                        elif isinstance(enhanced_result, dict):
                            total_score = enhanced_result.get('total_score', 0)
                            severity_level = enhanced_result.get('severity_level', 'Unknown')
                            interpretation = enhanced_result.get('interpretation', f'{current_questionnaire} assessment completed')
                        else:
                            total_score = 0
                            severity_level = 'Unknown'
                            interpretation = 'Unknown result type'
                        
                        smart_ui.track_user_interaction("enhanced_assessment_completed", track_event, {
                            "total_score": total_score,
                            "severity_level": severity_level,
                            "interpretation": interpretation,
                            "questionnaire_type": current_questionnaire
                        })
                        logger.info(f"Enhanced {current_questionnaire} assessment completed. Total score: {total_score}, Severity: {severity_level}")
                        
                        st.success(f"✅ Phân tích {current_questionnaire} nâng cao hoàn tất!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        logger.error(f"Enhanced {current_questionnaire} score calculation failed - result is None")
                        st.error("⚠️ Có lỗi trong tính toán nâng cao. Vui lòng thử lại.")
                        
            except Exception as e:
                logger.error(f"Exception during scoring: {str(e)}", exc_info=True)
                st.error(f"❌ Lỗi khi tính toán: {str(e)}")
                st.error("🔧 Vui lòng thử lại hoặc báo cáo lỗi cho admin.")
    
    else:
        # Enhanced Results Dashboard
        create_progress_ring(3, 3, "Kết quả nâng cao")
        
        # Check if we have enhanced results
        if "enhanced_scores" in st.session_state:
            enhanced_result = st.session_state.enhanced_scores
            questionnaire_used = st.session_state.get("questionnaire_used", "DASS-21")
            
            # Enhanced results header
            st.markdown(f"### 🎯 Kết quả đánh giá nâng cao {questionnaire_used}")
            
            # Overall status
            total_score = enhanced_result.get('total_score', 0)
            severity_level = enhanced_result.get('severity_level', 'Unknown')
            interpretation = enhanced_result.get('interpretation', f'{questionnaire_used} assessment')
            
            # Determine max score based on questionnaire
            max_scores = {
                "DASS-21": 126,
                "PHQ-9": 27,
                "GAD-7": 21,
                "EPDS": 30,
                "PSS-10": 40
            }
            max_score = max_scores.get(questionnaire_used, 21)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                       padding: 25px; border-radius: 15px; margin: 20px 0; text-align: center;">
                <h3 style="color: white; margin: 0;">
                    📊 Tổng điểm: {total_score}/{max_score}
                </h3>
                <p style="color: white; margin: 10px 0; font-size: 18px;">
                    🎯 Mức độ: {interpretation}
                </p>
                <p style="color: white; margin: 0; font-size: 16px;">
                    🏷️ Trạng thái: {severity_level.replace('_', ' ').title()}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced metrics display
            st.markdown("### 📊 Chi tiết đánh giá")
            
            # Display subscales based on questionnaire type
            if questionnaire_used == "DASS-21":
                col1, col2, col3 = st.columns(3)
                subscales = ["Depression", "Anxiety", "Stress"]
                emojis = ["😔", "😰", "😓"]
                colors = ["#e74c3c", "#f39c12", "#9b59b6"]
                
                for i, (subscale, emoji, color) in enumerate(zip(subscales, emojis, colors)):
                    with [col1, col2, col3][i]:
                        subscale_data = enhanced_result.get('subscales', {}).get(subscale, {})
                        
                        # Safely extract values with fallbacks
                        adjusted_score = subscale_data.get('adjusted', 0)
                        raw_score = subscale_data.get('raw', 0)
                        severity = subscale_data.get('severity', 'Unknown')
                        
                        st.markdown(f"""
                        <div style="background: {color}; color: white; 
                                   padding: 20px; border-radius: 15px; text-align: center;">
                            <h3 style="margin: 0; font-size: 24px;">{emoji}</h3>
                            <h4 style="margin: 10px 0;">{subscale}</h4>
                            <h2 style="margin: 10px 0;">{adjusted_score}</h2>
                            <p style="margin: 0; font-size: 16px;">{severity.title()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Progress bar
                        max_score = 42  # DASS-21 max per subscale
                        progress = min(adjusted_score / max_score, 1.0) if adjusted_score > 0 else 0
                        st.progress(progress)
                        st.caption(f"Điểm: {raw_score} → {adjusted_score} (x2)")
                        
            elif questionnaire_used == "GAD-7":
                # Single column for GAD-7 (Anxiety only)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    subscale_data = enhanced_result.get('subscales', {}).get('Anxiety', {})
                    
                    # Safely extract values
                    anxiety_score = subscale_data.get('adjusted', total_score)
                    anxiety_severity = subscale_data.get('severity', severity_level)
                    
                    st.markdown(f"""
                    <div style="background: #f39c12; color: white; 
                               padding: 20px; border-radius: 15px; text-align: center;">
                        <h3 style="margin: 0; font-size: 24px;">😰</h3>
                        <h4 style="margin: 10px 0;">Lo âu (Anxiety)</h4>
                        <h2 style="margin: 10px 0;">{anxiety_score}</h2>
                        <p style="margin: 0; font-size: 16px;">{anxiety_severity.title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    max_score = 21  # GAD-7 max
                    progress = min(anxiety_score / max_score, 1.0) if anxiety_score > 0 else 0
                    st.progress(progress)
                    st.caption(f"Điểm lo âu: {anxiety_score}/21")
                        
            elif questionnaire_used == "PHQ-9":
                # Single column for PHQ-9
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    subscale_data = enhanced_result.get('subscales', {}).get('Depression', {})
                    
                    # Safely extract values
                    depression_score = subscale_data.get('adjusted', total_score)
                    depression_severity = subscale_data.get('severity', severity_level)
                    
                    # Color based on severity
                    color_map = {
                        "minimal": "#2ecc71",
                        "mild": "#f1c40f", 
                        "moderate": "#e67e22",
                        "moderately_severe": "#e74c3c",
                        "severe": "#8e44ad"
                    }
                    color = color_map.get(depression_severity, "#95a5a6")
                    
                    st.markdown(f"""
                    <div style="background: {color}; color: white; 
                               padding: 30px; border-radius: 15px; text-align: center;">
                        <h3 style="margin: 0; font-size: 30px;">😔</h3>
                        <h4 style="margin: 15px 0;">Trầm cảm (PHQ-9)</h4>
                        <h2 style="margin: 15px 0; font-size: 36px;">{depression_score}/27</h2>
                        <p style="margin: 0; font-size: 18px; font-weight: bold;">{depression_severity.title()}</p>
                        <p style="margin: 10px 0; font-size: 14px;">{interpretation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    max_score = 27  # PHQ-9 max score
                    progress = min(depression_score / max_score, 1.0) if depression_score > 0 else 0
                    st.progress(progress)
                    st.caption(f"Điểm số: {depression_score}/27")
                    
                    # Suicide risk warning if applicable
                    if depression_score >= 15:
                        st.warning(f"⚠️ **Đánh giá nguy cơ:** Mức độ trầm cảm nghiêm trọng - Cần hỗ trợ ngay")
                        
            elif questionnaire_used == "GAD-7":
                # Single column for GAD-7
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    result = enhanced_result.get('subscales', {}).get('Anxiety', enhanced_result)
                    
                    # Color based on severity
                    color_map = {
                        "minimal": "#2ecc71",
                        "mild": "#f1c40f", 
                        "moderate": "#e67e22",
                        "severe": "#e74c3c"
                    }
                    color = color_map.get(result.get('severity', 'unknown'), "#95a5a6")
                    
                    st.markdown(f"""
                    <div style="background: {color}; color: white; 
                               padding: 30px; border-radius: 15px; text-align: center;">
                        <h3 style="margin: 0; font-size: 30px;">😰</h3>
                        <h4 style="margin: 15px 0;">Lo âu (GAD-7)</h4>
                        <h2 style="margin: 15px 0; font-size: 36px;">{result.get('score', result.get('adjusted', 0))}/21</h2>
                        <p style="margin: 0; font-size: 18px; font-weight: bold;">{result.get('level_info', {}).get('label', 'Unknown')}</p>
                        <p style="margin: 10px 0; font-size: 14px;">{result.get('level_info', {}).get('description', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    max_score = 21  # GAD-7 max score
                    progress = min(result.get('score', result.get('adjusted', 0)) / max_score, 1.0)
                    st.progress(progress)
                    st.caption(f"Điểm số: {result.get('score', result.get('adjusted', 0))}/21")
                    
            elif questionnaire_used == "EPDS":
                # Single column for EPDS
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    result = enhanced_result.get('subscales', {}).get('Postnatal Depression', enhanced_result)
                    
                    # Color based on severity
                    color_map = {
                        "no_risk": "#2ecc71",
                        "mild_risk": "#f1c40f", 
                        "moderate_risk": "#e67e22",
                        "high_risk": "#e74c3c"
                    }
                    color = color_map.get(result.get('severity', 'unknown'), "#95a5a6")
                    
                    st.markdown(f"""
                    <div style="background: {color}; color: white; 
                               padding: 30px; border-radius: 15px; text-align: center;">
                        <h3 style="margin: 0; font-size: 30px;">🤱</h3>
                        <h4 style="margin: 15px 0;">Trầm cảm sau sinh (EPDS)</h4>
                        <h2 style="margin: 15px 0; font-size: 36px;">{result.get('score', result.get('adjusted', 0))}/30</h2>
                        <p style="margin: 0; font-size: 18px; font-weight: bold;">{result.get('level_info', {}).get('label', 'Unknown')}</p>
                        <p style="margin: 10px 0; font-size: 14px;">{result.get('level_info', {}).get('description', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    max_score = 30  # EPDS max score
                    progress = min(result.get('score', result.get('adjusted', 0)) / max_score, 1.0)
                    st.progress(progress)
                    st.caption(f"Điểm số: {result.get('score', result.get('adjusted', 0))}/30")
                    
                    # Suicide risk warning if applicable
                    level_info = result.get('level_info', {})
                    if isinstance(level_info, dict) and 'suicide_risk' in level_info:
                        st.warning(f"⚠️ **Đánh giá nguy cơ tự làm hại:** {level_info.get('suicide_risk', 'Unknown')}")
                        
                    # Special considerations for postpartum
                    if result.get('severity', 'unknown') in ["moderate_risk", "high_risk"]:
                        st.info("🤱 **Lưu ý đặc biệt:** Thời kỳ sau sinh cần được chăm sóc đặc biệt về tâm lý")
                        
            elif questionnaire_used == "PSS-10":
                # Single column for PSS-10
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    result = enhanced_result.get('subscales', {}).get('Perceived Stress', enhanced_result)
                    
                    # Color based on severity
                    color_map = {
                        "low": "#2ecc71",
                        "moderate": "#f1c40f", 
                        "high": "#e74c3c"
                    }
                    color = color_map.get(result.get('severity', 'unknown'), "#95a5a6")
                    
                    st.markdown(f"""
                    <div style="background: {color}; color: white; 
                               padding: 30px; border-radius: 15px; text-align: center;">
                        <h3 style="margin: 0; font-size: 30px;">😤</h3>
                        <h4 style="margin: 15px 0;">Căng thẳng cảm nhận (PSS-10)</h4>
                        <h2 style="margin: 15px 0; font-size: 36px;">{result.get('score', result.get('adjusted', 0))}/40</h2>
                        <p style="margin: 0; font-size: 18px; font-weight: bold;">{result.get('level_info', {}).get('label', 'Unknown')}</p>
                        <p style="margin: 10px 0; font-size: 14px;">{result.get('level_info', {}).get('description', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar
                    max_score = 40  # PSS-10 max score
                    progress = min(result.get('score', result.get('adjusted', 0)) / max_score, 1.0)
                    st.progress(progress)
                    st.caption(f"Điểm số: {result.get('score', result.get('adjusted', 0))}/40")
                    
                    # High stress warning
                    if result.get('severity', 'unknown') == "high":
                        st.warning("⚠️ **Căng thẳng cao:** Cần học kỹ năng quản lý stress hiệu quả")
            
            # Enhanced recommendations
            st.markdown("### 💡 Khuyến nghị cá nhân hóa")
            recommendations = enhanced_result.get('recommendations', [])
            
            # Handle both dict and list formats
            if isinstance(recommendations, dict):
                # Dict format
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                           padding: 25px; border-radius: 15px; margin: 20px 0;">
                    <h4 style="color: white; margin: 0 0 15px 0;">
                        🎯 {recommendations.get('title', 'Khuyến nghị')}
                    </h4>
                    <p style="color: white; margin: 0; font-size: 16px; line-height: 1.6;">
                        {recommendations.get('message', 'Hãy chăm sóc sức khỏe tâm thần của bạn.')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Action suggestions
                suggestions = recommendations.get('suggestions', [])
                if suggestions:
                    st.markdown("#### 🚀 Các bước cần thực hiện:")
                    for i, suggestion in enumerate(suggestions, 1):
                        st.markdown(f"**{i}.** {suggestion}")
            
            elif isinstance(recommendations, list) and recommendations:
                # List format
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                           padding: 25px; border-radius: 15px; margin: 20px 0;">
                    <h4 style="color: white; margin: 0 0 15px 0;">
                        🎯 Khuyến nghị cho bạn
                    </h4>
                    <p style="color: white; margin: 0; font-size: 16px; line-height: 1.6;">
                        Dựa trên kết quả đánh giá, chúng tôi có một số gợi ý cho bạn.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Action suggestions
                st.markdown("#### 🚀 Các bước cần thực hiện:")
                for i, suggestion in enumerate(recommendations, 1):
                    st.markdown(f"**{i}.** {suggestion}")
            
            else:
                # Default recommendations
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                           padding: 25px; border-radius: 15px; margin: 20px 0;">
                    <h4 style="color: white; margin: 0 0 15px 0;">
                        🎯 Khuyến nghị chung
                    </h4>
                    <p style="color: white; margin: 0; font-size: 16px; line-height: 1.6;">
                        Hãy tiếp tục chăm sóc sức khỏe tâm thần và tìm kiếm sự hỗ trợ khi cần thiết.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Default suggestions
                st.markdown("#### 🚀 Các bước cần thực hiện:")
                st.markdown("**1.** Duy trì lối sống lành mạnh")
                st.markdown("**2.** Thực hành thư giãn và mindfulness")
                st.markdown("**3.** Tìm kiếm sự hỗ trợ từ bạn bè và gia đình")
                st.markdown("**4.** Cân nhắc tham khảo ý kiến chuyên gia nếu cần")
            
            # Emergency contacts if needed
            if enhanced_result.get('severity_level', enhanced_result.get('severity', 'normal')).lower() in ["severe", "extremely_severe"]:
                st.markdown("### 🆘 Liên hệ khẩn cấp")
                st.error("""
                **Quan trọng:** Nếu bạn có ý định tự làm hại bản thân, hãy liên hệ ngay:
                - **Đường dây nóng:** 1800-1567
                - **Cấp cứu:** 115
                - **Tư vấn tâm lý:** 1900-555-555
                """)
            
            # ============================================
            # ENHANCED CHARTS & VISUALIZATION  
            # ============================================
            st.markdown("---")
            
            # Summary statistics
            create_summary_statistics(enhanced_result, questionnaire_used)
            
            # Interactive charts
            display_enhanced_charts(enhanced_result, questionnaire_used)
            
            # Email report option
            create_email_report_option(enhanced_result, questionnaire_used)
        
        elif "scores" in st.session_state:
            # Fallback to legacy results if enhanced not available
            create_smart_results_dashboard(st.session_state.scores)
            
            scores = st.session_state.scores
            # Convert SubscaleScore objects to dict for DataFrame
            scores_dict = {}
            for subscale, score_obj in scores.items():
                scores_dict[subscale] = {
                    'raw': score_obj.raw,
                    'adjusted': score_obj.adjusted,
                    'severity': score_obj.severity
                }
            df = pd.DataFrame(scores_dict).T
            
            # Basic metrics display
            st.markdown("### 📊 Kết quả cơ bản")
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
            
            # Basic recommendations
            st.markdown("### 💡 Gợi ý cho bạn")
            # Convert SubscaleScore objects to dict for recommendations
            scores_dict = {}
            for key, value in st.session_state.scores.items():
                if hasattr(value, 'adjusted'):
                    scores_dict[key] = {'adjusted': value.adjusted, 'severity': value.severity}
                else:
                    scores_dict[key] = value
            create_smart_recommendations(scores_dict)
        
        else:
            st.error("Không có kết quả để hiển thị. Vui lòng thực hiện đánh giá lại.")
        
        # Enhanced action buttons
        st.markdown("### 🎯 Các hành động tiếp theo")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Đánh giá lại", key="reassess_button_1", use_container_width=True):
                # Reset all states for new assessment
                for key in list(st.session_state.keys()):
                    if key in ["answers", "scores", "enhanced_scores"]:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🤖 AI Insights", use_container_width=True):
                try:
                    st.switch_page("pages/ai_platform.py")
                except Exception as e:
                    st.error(f"Không thể mở AI Platform: {e}")
                    st.info("🔧 Tính năng đang được cập nhật...")
        
        with col3:
            if st.button("📊 Biểu đồ", use_container_width=True):
                st.session_state.show_charts = True
                st.rerun()
        
        with col4:
            if st.button("📄 Tải PDF", use_container_width=True):
                # Generate and download PDF report
                if 'enhanced_scores' in st.session_state:
                    assessment_data = {
                        'assessment_date': datetime.now().strftime("%d/%m/%Y"),
                        'assessment_type': st.session_state.get('selected_questionnaire', 'DASS-21'),
                        'scores': st.session_state.enhanced_scores,
                        'risk_assessment': create_risk_assessment(st.session_state.enhanced_scores),
                        'recommendations': get_ai_recommendations(st.session_state.enhanced_scores)
                    }
                    
                    pdf_buffer = generate_assessment_report(assessment_data)
                    if pdf_buffer:
                        st.download_button(
                            "⬇️ Tải báo cáo PDF",
                            data=pdf_buffer,
                            file_name=f"soulfriend_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
        
        # AI-powered insights section
        if st.session_state.get('enhanced_scores'):
            st.markdown("---")
            st.markdown("### 🤖 AI Insights & Predictions")
            
            # Quick AI analysis
            with st.expander("🔮 Phân tích thông minh", expanded=False):
                try:
                    from components.ai_insights import MentalHealthAI
                    
                    # Initialize AI if not exists
                    if 'ai_engine' not in st.session_state:
                        st.session_state.ai_engine = MentalHealthAI()
                    
                    ai_engine = st.session_state.ai_engine
                    
                    # Prepare user data from current assessment
                    current_scores = st.session_state.enhanced_scores
                    user_data = {
                        'age': st.session_state.get('user_age', 30),
                        'gender': st.session_state.get('user_gender', 'Female'),
                        'dass_depression': current_scores.get('dass_depression', 0),
                        'dass_anxiety': current_scores.get('dass_anxiety', 0),
                        'dass_stress': current_scores.get('dass_stress', 0),
                        'phq9_score': current_scores.get('phq9_total', 0),
                        'gad7_score': current_scores.get('gad7_total', 0),
                        'sleep_hours': st.session_state.get('sleep_hours', 7),
                        'exercise_freq': st.session_state.get('exercise_freq', 3),
                        'social_support': st.session_state.get('social_support', 5),
                        'stress_level': st.session_state.get('stress_level', 5)
                    }
                    
                    # Get AI prediction
                    prediction = ai_engine.predict_risk(user_data)
                    
                    if 'error' not in prediction:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "🎯 Mức độ rủi ro AI",
                                prediction['risk_level'],
                                delta=f"Tin cậy: {prediction['confidence']:.1%}"
                            )
                        
                        with col2:
                            st.metric(
                                "📈 Khả năng cải thiện",
                                f"{prediction['intervention_success_rate']:.1%}",
                                delta="Dự đoán can thiệp"
                            )
                        
                        with col3:
                            # Quick risk indicator
                            risk_color = {
                                'Low': '🟢',
                                'Moderate': '🟡', 
                                'High': '🟠',
                                'Very High': '🔴'
                            }.get(prediction['risk_level'], '⚪')
                            
                            st.metric(
                                "🚨 Cảnh báo",
                                f"{risk_color} {prediction['risk_level']}",
                                delta="Mức độ ưu tiên"
                            )
                        
                        # AI Recommendations
                        st.markdown("**💡 Khuyến nghị AI:**")
                        ai_recommendations = ai_engine.generate_recommendations(prediction, user_data)
                        for i, rec in enumerate(ai_recommendations[:3]):  # Show top 3
                            st.write(f"{i+1}. {rec}")
                        
                        if st.button("🔍 Xem phân tích chi tiết", key="detailed_ai"):
                            try:
                                st.switch_page("pages/ai_platform.py")
                            except Exception as e:
                                st.error(f"Không thể mở AI Platform: {e}")
                                st.info("🔧 Tính năng đang được cập nhật...")
                    
                    else:
                        st.info("🤖 AI chưa được huấn luyện. Truy cập AI Platform để huấn luyện mô hình.")
                        if st.button("🚀 Huấn luyện AI ngay", key="train_ai"):
                            try:
                                st.switch_page("pages/ai_platform.py")
                            except Exception as e:
                                st.error(f"Không thể mở AI Platform: {e}")
                                st.info("🔧 Tính năng đang được cập nhật...")
                
                except ImportError:
                    st.warning("⚠️ Module AI chưa được cài đặt đầy đủ")
                except Exception as e:
                    st.error(f"Lỗi AI: {str(e)}")
        
        # Enhanced action buttons (continued)
        with col1:
            if st.button("🔄 Đánh giá lại", key="reassess_button_2", use_container_width=True):
                # Reset all states for new assessment
                for key in list(st.session_state.keys()):
                    if key in ["answers", "scores", "enhanced_scores"]:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if "enhanced_scores" in st.session_state:
                # PDF Export functionality
                enhanced_result = st.session_state.enhanced_scores
                questionnaire_used = st.session_state.get("questionnaire_used", "DASS-21")
                create_download_button(enhanced_result, questionnaire_used)
            else:
                st.button("📊 Xuất báo cáo", disabled=True, use_container_width=True)
                st.caption("Cần hoàn thành đánh giá trước")
        
        with col3:
            if st.button("🔍 Tìm hiểu thêm", use_container_width=True):
                st.info("📚 Tài liệu về sức khỏe tâm lý và DASS-21 sẽ được cung cấp")
        
        # User journey summary
        create_user_journey_summary()

# Footer with navigation
st.markdown("---")

# Navigation and access buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🤖 AI Platform", key="ai_access", help="Truy cập nền tảng AI", use_container_width=True):
        try:
            st.switch_page("pages/03_🤖_Nền_tảng_AI.py")
        except Exception as e:
            st.error(f"Không thể mở AI Platform: {e}")
            st.info("🔧 Tính năng đang được cập nhật...")

with col2:
    if st.button("💬 Chatbot", key="chatbot_access", help="Trò chuyện với AI", use_container_width=True):
        try:
            st.switch_page("pages/04_💬_Chatbot_AI.py")
        except Exception as e:
            st.error(f"Không thể mở Chatbot: {e}")
            st.info("🔧 Tính năng đang được cập nhật...")

with col3:
    if st.button("📋 Báo cáo cá nhân", key="reports_access", help="Xem báo cáo kết quả cá nhân của bạn", use_container_width=True):
        try:
            st.switch_page("pages/02_📋_Báo_cáo_cá_nhân.py")
        except Exception as e:
            st.error(f"Không thể mở trang: {e}")
            st.info("🔧 Tính năng đang được cập nhật...")

# ===== RESEARCH SYSTEM INTEGRATION (OPTIONAL) =====
# Phần này hoàn toàn tùy chọn và không ảnh hưởng đến logic chính của SOULFRIEND

try:
    # Import research system với safe fallback
    from research_system.integration import (
        safe_track_session_start,
        safe_track_questionnaire_start,
        safe_track_question_answer,
        safe_track_questionnaire_complete,
        safe_track_results_view
    )
    
    # Đánh dấu research system available
    RESEARCH_SYSTEM_AVAILABLE = True
    
    # Track session start nếu chưa track
    if "research_session_tracked" not in st.session_state:
        st.session_state["research_session_tracked"] = True
        safe_track_session_start(
            user_agent=st.context.headers.get("user-agent", "unknown") if hasattr(st, 'context') else "unknown",
            locale="vi"
        )
    
    # Track questionnaire events based on current state
    if st.session_state.get("questionnaire_type") and "research_questionnaire_tracked" not in st.session_state:
        safe_track_questionnaire_start(st.session_state["questionnaire_type"])
        st.session_state["research_questionnaire_tracked"] = True
    
    # Track results view if enhanced scores exist
    if st.session_state.get("enhanced_scores") and "research_results_tracked" not in st.session_state:
        results_summary = {
            "questionnaires": [st.session_state.get("questionnaire_used", "Unknown")],
            "scores": st.session_state.get("enhanced_scores", {}),
            "completion_time": datetime.now().isoformat()
        }
        safe_track_results_view(results_summary)
        st.session_state["research_results_tracked"] = True
    
except ImportError:
    # Nếu không có research system - không sao cả
    RESEARCH_SYSTEM_AVAILABLE = False
except Exception:
    # Bất kỳ lỗi nào khác - silent fail
    RESEARCH_SYSTEM_AVAILABLE = False

# ===== END RESEARCH SYSTEM INTEGRATION =====

# App info
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    💚 <strong>SOULFRIEND V2.0</strong> | 0938.02.1111 - CHUN
</div>
""", unsafe_allow_html=True)
