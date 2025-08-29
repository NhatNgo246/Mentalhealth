import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any

class DataBackupSystem:
    """Hệ thống sao lưu dữ liệu"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_session_backup(self, session_data: Dict[str, Any]) -> str:
        """Tạo backup cho session hiện tại"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{self.backup_dir}/session_backup_{timestamp}.json"
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "session_data": session_data,
            "system_info": {
                "version": "2.0.0",
                "backup_type": "session"
            }
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        return backup_file
    
    def restore_session_backup(self, backup_file: str) -> Dict[str, Any]:
        """Khôi phục session từ backup"""
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        return backup_data.get('session_data', {})
    
    def list_backups(self) -> list:
        """Liệt kê các file backup"""
        backup_files = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.json'):
                backup_files.append(os.path.join(self.backup_dir, file))
        
        return sorted(backup_files, reverse=True)  # Newest first

def auto_backup_session():
    """Tự động backup session state"""
    import streamlit as st
    
    if hasattr(st.session_state, 'enhanced_scores') and st.session_state.enhanced_scores:
        backup_system = DataBackupSystem()
        session_data = dict(st.session_state)
        
        # Clean sensitive data
        cleaned_data = {k: v for k, v in session_data.items() 
                       if not k.startswith('_') and k != 'user_credentials'}
        
        backup_file = backup_system.create_session_backup(cleaned_data)
        return backup_file
    
    return None
