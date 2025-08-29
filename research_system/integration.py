"""
Non-invasive Integration Wrapper for SOULFRIEND
Tích hợp nghiên cứu một cách an toàn, không ảnh hưởng đến logic chính
"""

import streamlit as st
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

# Import research components với safe fallback
try:
    from research_system.collector import (
        collect_session_started,
        collect_questionnaire_started, 
        collect_question_answered,
        collect_questionnaire_completed,
        collect_results_viewed
    )
    from research_system.consent_ui import (
        get_research_consent_status,
        is_research_enabled
    )
    RESEARCH_AVAILABLE = True
except ImportError:
    RESEARCH_AVAILABLE = False

class SafeResearchIntegration:
    """
    Wrapper an toàn cho việc tích hợp research collection
    """
    
    def __init__(self):
        self.enabled = RESEARCH_AVAILABLE and is_research_enabled()
        self.session_id = self._get_or_create_session_id()
    
    def _get_or_create_session_id(self) -> str:
        """Tạo hoặc lấy session ID từ session state"""
        if "research_session_id" not in st.session_state:
            st.session_state["research_session_id"] = str(uuid.uuid4())
        return st.session_state["research_session_id"]
    
    def _should_collect(self) -> bool:
        """Kiểm tra xem có nên thu thập dữ liệu không"""
        if not self.enabled:
            return False
        
        consent_status = get_research_consent_status()
        return consent_status is True
    
    def track_session_start(self, user_info: Optional[Dict[str, Any]] = None):
        """Track session start - an toàn"""
        if not self._should_collect():
            return
            
        try:
            user_data = user_info or {}
            collect_session_started(self.session_id, user_data)
        except Exception:
            pass  # Silent fail
    
    def track_questionnaire_start(self, questionnaire_type: str):
        """Track questionnaire start - an toàn"""
        if not self._should_collect():
            return
            
        try:
            collect_questionnaire_started(self.session_id, questionnaire_type)
        except Exception:
            pass  # Silent fail
    
    def track_question_answer(
        self, 
        questionnaire_type: str, 
        question_index: int, 
        answer_value: int,
        response_time_ms: Optional[int] = None
    ):
        """Track question answer - an toàn"""
        if not self._should_collect():
            return
            
        try:
            item_id = f"{questionnaire_type}_Q{question_index:02d}"
            collect_question_answered(
                self.session_id,
                questionnaire_type,
                item_id,
                answer_value,
                response_time_ms
            )
        except Exception:
            pass  # Silent fail
    
    def track_questionnaire_complete(
        self, 
        questionnaire_type: str, 
        total_score: int,
        completion_time: Optional[int] = None
    ):
        """Track questionnaire completion - an toàn"""
        if not self._should_collect():
            return
            
        try:
            collect_questionnaire_completed(
                self.session_id,
                questionnaire_type,
                total_score,
                completion_time
            )
        except Exception:
            pass  # Silent fail
    
    def track_results_view(self, results_summary: Dict[str, Any]):
        """Track results viewing - an toàn"""
        if not self._should_collect():
            return
            
        try:
            collect_results_viewed(self.session_id, results_summary)
        except Exception:
            pass  # Silent fail

# Global instance
_research_integration = None

def get_research_integration() -> SafeResearchIntegration:
    """Lazy initialization of research integration"""
    global _research_integration
    if _research_integration is None:
        _research_integration = SafeResearchIntegration()
    return _research_integration

# Convenience functions for easy integration
def safe_track_session_start(**kwargs):
    """Convenience function - completely safe"""
    try:
        get_research_integration().track_session_start(kwargs)
    except Exception:
        pass

def safe_track_questionnaire_start(questionnaire_type: str, test_mode: bool = False, session_id: str = None):
    """Convenience function - completely safe"""
    try:
        get_research_integration().track_questionnaire_start(questionnaire_type)
    except Exception:
        pass

def safe_track_question_answer(questionnaire_type: str, question_idx: int, answer: int, test_mode: bool = False, session_id: str = None):
    """Convenience function - completely safe"""
    try:
        get_research_integration().track_question_answer(questionnaire_type, question_idx, answer)
    except Exception:
        pass

def safe_track_questionnaire_completion(questionnaire_type: str, score: int, test_mode: bool = False, session_id: str = None):
    """Convenience function - completely safe"""
    try:
        get_research_integration().track_questionnaire_complete(questionnaire_type, score)
    except Exception:
        pass

def safe_track_results_view(results: Dict[str, Any], test_mode: bool = False, session_id: str = None):
    """Convenience function - completely safe"""
    try:
        get_research_integration().track_results_view(results)
    except Exception:
        pass
