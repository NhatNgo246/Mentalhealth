"""
Research Data Collector - Non-invasive Optional Component
Hoàn toàn tách biệt khỏi logic chính của SOULFRIEND
"""

import os
import json
import hmac
import hashlib
import uuid
import threading
import requests
from datetime import datetime
from typing import Optional, Dict, Any
import logging

# Setup logging riêng cho research system
research_logger = logging.getLogger('research_system')
research_logger.setLevel(logging.INFO)

class SafeResearchCollector:
    """
    Thu thập dữ liệu nghiên cứu một cách an toàn, không ảnh hưởng đến ứng dụng chính
    """
    
    def __init__(self):
        self.enabled = self._check_research_enabled()
        self.collection_url = os.environ.get("RESEARCH_COLLECTION_URL", "http://localhost:8502/collect")
        self.secret = os.environ.get("RESEARCH_SECRET", "default_research_secret_change_me")
        self.timeout = 1.0  # Very short timeout to not block UI
        
    def _check_research_enabled(self) -> bool:
        """Kiểm tra xem research collection có được bật không"""
        return os.environ.get("ENABLE_RESEARCH_COLLECTION", "false").lower() in ["true", "1", "yes"]
    
    def _create_user_hash(self, user_id: str) -> str:
        """Tạo hash an toàn cho user ID"""
        try:
            return hmac.new(
                self.secret.encode(), 
                user_id.encode(), 
                hashlib.sha256
            ).hexdigest()
        except Exception:
            return "anonymous"
    
    def collect_event_async(
        self, 
        event_name: str, 
        payload: Dict[str, Any], 
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> bool:
        """
        Thu thập event một cách bất đồng bộ, không chặn UI
        Hoàn toàn an toàn - nếu có lỗi sẽ không ảnh hưởng đến app chính
        """
        if not self.enabled:
            return False
            
        def _send_event():
            try:
                event_data = {
                    "client_ts": datetime.utcnow().isoformat(),
                    "session_id": session_id or "default_session",
                    "user_hash": self._create_user_hash(user_id) if user_id else "anonymous",
                    "event_name": event_name,
                    "payload": payload,
                    "cohort_version": "soulfriend_v2.0"
                }
                
                requests.post(
                    self.collection_url,
                    json=event_data,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json"}
                )
                research_logger.info(f"Research event collected: {event_name}")
                
            except Exception as e:
                # Silent fail - không in error để không làm phiền user
                research_logger.debug(f"Research collection failed (safe): {e}")
        
        try:
            # Chạy trong thread riêng để không chặn UI
            thread = threading.Thread(target=_send_event, daemon=True)
            thread.start()
            return True
        except Exception as e:
            research_logger.debug(f"Thread creation failed (safe): {e}")
            return False

# Global collector instance (lazy initialization)
_collector = None

def get_research_collector() -> SafeResearchCollector:
    """Lazy initialization của collector"""
    global _collector
    if _collector is None:
        _collector = SafeResearchCollector()
    return _collector

def collect_research_event(
    event_name: str, 
    payload: Dict[str, Any], 
    session_id: str,
    user_id: Optional[str] = None
):
    """
    Public API để thu thập research events
    Hoàn toàn an toàn và optional
    """
    try:
        collector = get_research_collector()
        collector.collect_event_async(event_name, payload, session_id, user_id)
    except Exception:
        # Silent fail - không ảnh hưởng đến ứng dụng chính
        pass

# Helper functions cho các event types phổ biến
def collect_session_started(session_id: str, user_info: Dict[str, Any]):
    """Thu thập event bắt đầu session"""
    collect_research_event(
        "session_started",
        {
            "user_agent": user_info.get("user_agent", "unknown"),
            "locale": user_info.get("locale", "vi"),
            "timestamp": datetime.utcnow().isoformat()
        },
        session_id
    )

def collect_questionnaire_started(session_id: str, questionnaire_type: str):
    """Thu thập event bắt đầu questionnaire"""
    collect_research_event(
        "questionnaire_started",
        {
            "questionnaire_type": questionnaire_type,
            "timestamp": datetime.utcnow().isoformat()
        },
        session_id
    )

def collect_question_answered(
    session_id: str, 
    questionnaire_type: str, 
    item_id: str, 
    response_value: int,
    response_time_ms: Optional[int] = None
):
    """Thu thập event trả lời câu hỏi"""
    collect_research_event(
        "question_answered",
        {
            "questionnaire_type": questionnaire_type,
            "item_id": item_id,
            "response_value": response_value,
            "response_time_ms": response_time_ms,
            "timestamp": datetime.utcnow().isoformat()
        },
        session_id
    )

def collect_questionnaire_completed(
    session_id: str, 
    questionnaire_type: str, 
    total_score: int,
    completion_time_seconds: Optional[int] = None
):
    """Thu thập event hoàn thành questionnaire"""
    collect_research_event(
        "questionnaire_completed",
        {
            "questionnaire_type": questionnaire_type,
            "total_score": total_score,
            "completion_time_seconds": completion_time_seconds,
            "timestamp": datetime.utcnow().isoformat()
        },
        session_id
    )

def collect_results_viewed(session_id: str, results_data: Dict[str, Any]):
    """Thu thập event xem kết quả"""
    collect_research_event(
        "results_viewed",
        {
            "questionnaires_completed": results_data.get("questionnaires", []),
            "total_assessments": len(results_data.get("scores", {})),
            "timestamp": datetime.utcnow().isoformat()
        },
        session_id
    )
