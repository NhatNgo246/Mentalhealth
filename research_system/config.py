"""
Safe Environment Setup for Research System
Thiết lập môi trường an toàn, không ảnh hưởng đến ứng dụng chính
"""

import os
import logging
from pathlib import Path

def setup_research_environment():
    """
    Thiết lập môi trường research system một cách an toàn
    Chỉ thiết lập nếu được yêu cầu explicit
    """
    
    # Mặc định: TẮT research collection
    if "ENABLE_RESEARCH_COLLECTION" not in os.environ:
        os.environ["ENABLE_RESEARCH_COLLECTION"] = "false"
    
    # Setup logging riêng cho research
    research_log_path = Path(__file__).parent.parent / "logs" / "research.log"
    research_log_path.parent.mkdir(exist_ok=True)
    
    research_logger = logging.getLogger('research_system')
    if not research_logger.handlers:  # Avoid duplicate handlers
        handler = logging.FileHandler(research_log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        research_logger.addHandler(handler)
        research_logger.setLevel(logging.INFO)
    
    return research_logger

def is_research_safe_to_enable() -> bool:
    """
    Kiểm tra xem research system có an toàn để bật không
    """
    try:
        # Kiểm tra các dependencies cần thiết
        import requests
        import threading
        import uuid
        import hmac
        import hashlib
        return True
    except ImportError:
        return False

def enable_research_collection():
    """
    Bật research collection một cách an toàn
    Chỉ gọi function này nếu bạn muốn bật research
    """
    if is_research_safe_to_enable():
        os.environ["ENABLE_RESEARCH_COLLECTION"] = "true"
        print("✅ Research collection enabled safely")
    else:
        print("❌ Research collection cannot be enabled - missing dependencies")

def disable_research_collection():
    """
    Tắt research collection
    """
    os.environ["ENABLE_RESEARCH_COLLECTION"] = "false"
    print("✅ Research collection disabled")

# Setup automatically when imported
setup_research_environment()
