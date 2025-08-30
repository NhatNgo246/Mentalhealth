"""
API Keys Configuration for SOULFRIEND V3.0
Quản lý các API keys cho các dịch vụ AI - Hỗ trợ Streamlit Cloud
"""

import os
from typing import Optional
import streamlit as st

class APIKeyManager:
    """Quản lý API keys cho các dịch vụ AI"""
    
    def __init__(self):
        # Gemini AI API Key - Priority: Streamlit secrets > hardcoded > env
        self.GEMINI_API_KEY = "AIzaSyCAX2r_vMJE7-41bpBb6MBMEyLDBkmO6BE"
        
        # Environment variables
        self.GEMINI_API_KEY_ENV = os.getenv("GEMINI_API_KEY")
        
        # Other AI services (for future expansion)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    def get_gemini_key(self) -> Optional[str]:
        """Lấy Gemini API key với priority: Streamlit secrets > hardcoded > env"""
        # Try Streamlit secrets first (for cloud deployment)
        try:
            if hasattr(st, 'secrets') and 'gemini' in st.secrets and 'api_key' in st.secrets['gemini']:
                return st.secrets['gemini']['api_key']
        except:
            pass
        
        # Fall back to hardcoded or environment
        return self.GEMINI_API_KEY or self.GEMINI_API_KEY_ENV
    
    def get_openai_key(self) -> Optional[str]:
        """Lấy OpenAI API key"""
        return self.OPENAI_API_KEY
    
    def get_anthropic_key(self) -> Optional[str]:
        """Lấy Anthropic API key"""
        return self.ANTHROPIC_API_KEY
    
    def validate_gemini_key(self) -> bool:
        """Kiểm tra tính hợp lệ của Gemini API key"""
        key = self.get_gemini_key()
        if not key:
            return False
        
        # Kiểm tra format cơ bản
        if not key.startswith("AIza"):
            return False
        
        if len(key) < 30:
            return False
            
        return True
    
    def is_gemini_available(self) -> bool:
        """Kiểm tra xem Gemini có sẵn để sử dụng"""
        return self.validate_gemini_key()
    
    def get_available_models(self) -> dict:
        """Lấy danh sách models có sẵn"""
        models = {}
        
        if self.validate_gemini_key():
            models["gemini"] = {
                "name": "Gemini 2.5",
                "provider": "Google",
                "capabilities": ["text", "vision", "reasoning"],
                "status": "active"
            }
        
        if self.get_openai_key():
            models["openai"] = {
                "name": "GPT-4",
                "provider": "OpenAI", 
                "capabilities": ["text", "vision"],
                "status": "active"
            }
            
        if self.get_anthropic_key():
            models["anthropic"] = {
                "name": "Claude 3",
                "provider": "Anthropic",
                "capabilities": ["text", "reasoning"],
                "status": "active"
            }
        
        return models

# Global instance
api_keys = APIKeyManager()

# Convenience functions
def get_gemini_api_key() -> Optional[str]:
    """Lấy Gemini API key"""
    return api_keys.get_gemini_key()

def validate_api_keys() -> dict:
    """Kiểm tra tất cả API keys"""
    return {
        "gemini": api_keys.validate_gemini_key(),
        "openai": bool(api_keys.get_openai_key()),
        "anthropic": bool(api_keys.get_anthropic_key())
    }

def get_active_ai_models() -> dict:
    """Lấy các AI models đang hoạt động"""
    return api_keys.get_available_models()
