"""
Optional Research Integration for SOULFRIEND
Thêm vào cuối file SOULFRIEND.py - hoàn toàn optional và safe
"""

# ===== RESEARCH SYSTEM INTEGRATION (OPTIONAL) =====
# Phần này hoàn toàn tùy chọn và không ảnh hưởng đến logic chính của SOULFRIEND

try:
    # Import research system với safe fallback
    from research_system.config import setup_research_environment
    from research_system.integration import (
        safe_track_session_start,
        safe_track_questionnaire_start,
        safe_track_question_answer,
        safe_track_questionnaire_complete,
        safe_track_results_view
    )
    
    # Setup research environment
    setup_research_environment()
    
    # Đánh dấu research system available
    RESEARCH_SYSTEM_AVAILABLE = True
    
except ImportError:
    # Nếu không có research system - không sao cả
    RESEARCH_SYSTEM_AVAILABLE = False
    
    # Tạo dummy functions để không ảnh hưởng đến code
    def safe_track_session_start(**kwargs): pass
    def safe_track_questionnaire_start(q_type): pass  
    def safe_track_question_answer(q_type, idx, answer): pass
    def safe_track_questionnaire_complete(q_type, score): pass
    def safe_track_results_view(results): pass

def research_track_if_enabled(func_name: str, *args, **kwargs):
    """
    Helper function để track research events một cách an toàn
    Chỉ chạy nếu research system có sẵn và được bật
    """
    if not RESEARCH_SYSTEM_AVAILABLE:
        return
    
    try:
        if func_name == "session_start":
            safe_track_session_start(**kwargs)
        elif func_name == "questionnaire_start":
            safe_track_questionnaire_start(args[0])
        elif func_name == "question_answer":
            safe_track_question_answer(args[0], args[1], args[2])
        elif func_name == "questionnaire_complete":
            safe_track_questionnaire_complete(args[0], args[1])
        elif func_name == "results_view":
            safe_track_results_view(args[0])
    except Exception:
        # Silent fail - không ảnh hưởng đến ứng dụng chính
        pass

# Thêm vào session state để track research
if "research_tracking_initialized" not in st.session_state:
    st.session_state["research_tracking_initialized"] = True
    # Track session start (optional)
    research_track_if_enabled("session_start", 
                             user_agent=st.context.headers.get("user-agent", "unknown"),
                             locale="vi")

# ===== END RESEARCH SYSTEM INTEGRATION =====
