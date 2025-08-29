import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class DataEncryptionSystem:
    """Hệ thống mã hóa dữ liệu an toàn"""
    
    def __init__(self, password: Optional[str] = None):
        self.password = password or os.environ.get('ENCRYPTION_PASSWORD', 'default_soulfriend_key_2025')
        self.salt = b'soulfriend_salt_2025_mental_health'
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self) -> bytes:
        """Tạo key mã hóa từ password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        return key
    
    def encrypt_data(self, data: Dict[str, Any]) -> str:
        """Mã hóa dữ liệu"""
        try:
            json_data = json.dumps(data, ensure_ascii=False)
            encrypted_data = self.cipher.encrypt(json_data.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")
    
    def decrypt_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Giải mã dữ liệu"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")
    
    def hash_sensitive_data(self, data: str) -> str:
        """Hash dữ liệu nhạy cảm (không thể reverse)"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def encrypt_assessment_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Mã hóa kết quả đánh giá"""
        # Separate sensitive and non-sensitive data
        sensitive_data = {
            'personal_info': results.get('personal_info', {}),
            'detailed_answers': results.get('detailed_answers', {}),
            'assessment_scores': results.get('assessment_scores', {})
        }
        
        non_sensitive_data = {
            'timestamp': results.get('timestamp', datetime.now().isoformat()),
            'assessment_type': results.get('assessment_type', ''),
            'version': results.get('version', '2.0.0')
        }
        
        # Encrypt sensitive data
        encrypted_sensitive = self.encrypt_data(sensitive_data)
        
        return {
            **non_sensitive_data,
            'encrypted_data': encrypted_sensitive,
            'data_hash': self.hash_sensitive_data(str(sensitive_data))
        }
    
    def decrypt_assessment_results(self, encrypted_results: Dict[str, Any]) -> Dict[str, Any]:
        """Giải mã kết quả đánh giá"""
        sensitive_data = self.decrypt_data(encrypted_results['encrypted_data'])
        
        # Verify data integrity
        data_hash = self.hash_sensitive_data(str(sensitive_data))
        if data_hash != encrypted_results.get('data_hash'):
            raise Exception("Data integrity check failed")
        
        # Combine data
        return {
            **encrypted_results,
            **sensitive_data
        }

# Session encryption utilities
def encrypt_session_data(session_data: Dict[str, Any]) -> str:
    """Mã hóa session data"""
    encryptor = DataEncryptionSystem()
    return encryptor.encrypt_data(session_data)

def decrypt_session_data(encrypted_session: str) -> Dict[str, Any]:
    """Giải mã session data"""
    encryptor = DataEncryptionSystem()
    return encryptor.decrypt_data(encrypted_session)

# Streamlit integration
def secure_session_backup():
    """Backup session với mã hóa"""
    import streamlit as st
    
    if hasattr(st.session_state, 'assessment_results'):
        encryptor = DataEncryptionSystem()
        
        # Get session data
        session_data = {
            'assessment_results': dict(st.session_state.assessment_results),
            'user_progress': getattr(st.session_state, 'user_progress', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        # Encrypt and save
        encrypted_data = encryptor.encrypt_assessment_results(session_data)
        
        backup_file = f"backups/encrypted_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
        
        return backup_file
    
    return None

def load_secure_session_backup(backup_file: str):
    """Load encrypted session backup"""
    import streamlit as st
    
    encryptor = DataEncryptionSystem()
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        encrypted_data = json.load(f)
    
    # Decrypt data
    session_data = encryptor.decrypt_assessment_results(encrypted_data)
    
    # Restore to session state
    if 'assessment_results' in session_data:
        st.session_state.assessment_results = session_data['assessment_results']
    
    if 'user_progress' in session_data:
        st.session_state.user_progress = session_data['user_progress']
    
    return True
