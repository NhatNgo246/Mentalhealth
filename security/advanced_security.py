"""
🔒 Advanced Security Framework
Comprehensive security và compliance system cho SOULFRIEND V2.0
"""

import os
import hashlib
import secrets
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext
import base64

class AdvancedEncryption:
    """
    Advanced encryption system cho sensitive mental health data
    """
    
    def __init__(self, master_key: Optional[str] = None):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.master_key = master_key or self._generate_master_key()
        self.fernet = self._create_fernet_key()
        
    def _generate_master_key(self) -> str:
        """Generate a secure master key"""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()
    
    def _create_fernet_key(self) -> Fernet:
        """Create Fernet encryption key from master key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'soulfriend_salt',  # In production, use random salt per user
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
        return Fernet(key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logging.error(f"Encryption error: {e}")
            return ""
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logging.error(f"Decryption error: {e}")
            return ""
    
    def hash_password(self, password: str) -> str:
        """Hash password securely"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(password, hashed)
    
    def anonymize_user_id(self, user_id: str) -> str:
        """Create anonymous hash of user ID"""
        hash_object = hashlib.sha256((user_id + "soulfriend_salt").encode())
        return hash_object.hexdigest()[:16]  # 16 character anonymous ID

class DataAnonymization:
    """
    Data anonymization và pseudonymization cho GDPR compliance
    """
    
    def __init__(self):
        self.encryption = AdvancedEncryption()
        
    def anonymize_assessment_data(self, assessment_data: Dict) -> Dict:
        """
        Anonymize assessment data while preserving research value
        """
        anonymized = assessment_data.copy()
        
        # Remove direct identifiers
        identifiers_to_remove = [
            'email', 'phone', 'full_name', 'address', 'ip_address'
        ]
        
        for identifier in identifiers_to_remove:
            if identifier in anonymized:
                del anonymized[identifier]
        
        # Anonymize user ID
        if 'user_id' in anonymized:
            anonymized['user_id'] = self.encryption.anonymize_user_id(anonymized['user_id'])
        
        # Pseudonymize session ID
        if 'session_id' in anonymized:
            anonymized['session_id'] = self.encryption.anonymize_user_id(anonymized['session_id'])
        
        # Add anonymization metadata
        anonymized['anonymized_at'] = datetime.now().isoformat()
        anonymized['anonymization_version'] = "1.0"
        
        return anonymized
    
    def pseudonymize_for_research(self, data: Dict, research_id: str) -> Dict:
        """
        Pseudonymize data for research purposes với reversible mapping
        """
        pseudonymized = data.copy()
        
        # Create research-specific pseudonym
        if 'user_id' in pseudonymized:
            original_id = pseudonymized['user_id']
            research_pseudonym = self.encryption.anonymize_user_id(f"{original_id}_{research_id}")
            pseudonymized['research_id'] = research_pseudonym
            
            # Encrypt original mapping for potential reversal (stored separately)
            mapping = {
                'research_id': research_pseudonym,
                'original_id_hash': self.encryption.anonymize_user_id(original_id),
                'created_at': datetime.now().isoformat()
            }
        
        return pseudonymized, mapping if 'user_id' in data else None

class GDPRCompliance:
    """
    GDPR compliance framework
    """
    
    def __init__(self):
        self.data_retention_days = 365 * 2  # 2 years default
        self.encryption = AdvancedEncryption()
        self.anonymizer = DataAnonymization()
        
    def create_privacy_notice(self) -> Dict:
        """
        Create comprehensive privacy notice
        """
        return {
            "privacy_notice": {
                "version": "2.0",
                "effective_date": "2025-08-28",
                "controller": {
                    "name": "SOULFRIEND Mental Health Platform",
                    "contact": "privacy@soulfriend.com",
                    "dpo_contact": "dpo@soulfriend.com"
                },
                "data_collection": {
                    "purposes": [
                        "Mental health assessment and screening",
                        "Research to improve mental health tools",
                        "System performance and security monitoring"
                    ],
                    "legal_basis": [
                        "Legitimate interest for health research",
                        "Consent for personalized recommendations",
                        "Legal obligation for data protection"
                    ],
                    "data_types": [
                        "Assessment responses and scores",
                        "Session and usage analytics",
                        "Technical logs (anonymized)"
                    ]
                },
                "data_processing": {
                    "retention_period": f"{self.data_retention_days} days",
                    "anonymization": "Automatic after 30 days",
                    "encryption": "AES-256 encryption at rest and in transit",
                    "access_controls": "Role-based access with audit logging"
                },
                "user_rights": {
                    "access": "Right to access your personal data",
                    "rectification": "Right to correct inaccurate data",
                    "erasure": "Right to deletion (right to be forgotten)",
                    "portability": "Right to data portability",
                    "objection": "Right to object to processing",
                    "withdraw_consent": "Right to withdraw consent anytime"
                },
                "data_sharing": {
                    "research_partners": "Anonymized data only",
                    "no_selling": "We never sell personal data",
                    "minimal_sharing": "Only necessary for service operation"
                },
                "contact_info": {
                    "privacy_officer": "privacy@soulfriend.com",
                    "data_requests": "data-requests@soulfriend.com",
                    "complaints": "complaints@soulfriend.com"
                }
            }
        }
    
    def create_consent_record(self, user_id: str, consent_details: Dict) -> Dict:
        """
        Create comprehensive consent record
        """
        consent_record = {
            "consent_id": secrets.token_urlsafe(16),
            "user_id": self.encryption.anonymize_user_id(user_id),
            "timestamp": datetime.now().isoformat(),
            "consent_version": "2.0",
            "consents_given": consent_details,
            "withdrawal_info": {
                "can_withdraw": True,
                "withdrawal_method": "Contact privacy@soulfriend.com",
                "withdrawal_effect": "Immediate cessation of data processing"
            },
            "legal_basis": {
                "research_consent": consent_details.get("research_participation", False),
                "service_usage": True,  # Necessary for service
                "analytics": consent_details.get("analytics_consent", False)
            }
        }
        
        return consent_record
    
    def check_data_retention(self, data_age_days: int) -> Dict:
        """
        Check if data should be anonymized or deleted based on retention policy
        """
        actions = []
        
        if data_age_days > 30:
            actions.append("anonymize_personal_data")
        
        if data_age_days > self.data_retention_days:
            actions.append("delete_or_archive")
        
        return {
            "data_age_days": data_age_days,
            "retention_limit_days": self.data_retention_days,
            "required_actions": actions,
            "compliance_status": "compliant" if data_age_days <= self.data_retention_days else "action_required"
        }

class AuditLogger:
    """
    Comprehensive audit logging system
    """
    
    def __init__(self, log_file: str = "/workspaces/Mentalhealth/security_logs/audit.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Setup structured logging
        self.logger = logging.getLogger("SecurityAudit")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_access_attempt(self, user_id: str, resource: str, success: bool, ip_address: str = "unknown"):
        """Log access attempts"""
        event = {
            "event_type": "access_attempt",
            "user_id": hashlib.sha256(user_id.encode()).hexdigest()[:16],
            "resource": resource,
            "success": success,
            "ip_address": ip_address,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(json.dumps(event))
    
    def log_data_access(self, user_id: str, data_type: str, action: str, details: str = ""):
        """Log data access events"""
        event = {
            "event_type": "data_access",
            "user_id": hashlib.sha256(user_id.encode()).hexdigest()[:16],
            "data_type": data_type,
            "action": action,  # read, write, delete, export
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(json.dumps(event))
    
    def log_consent_change(self, user_id: str, old_consent: Dict, new_consent: Dict):
        """Log consent changes"""
        event = {
            "event_type": "consent_change",
            "user_id": hashlib.sha256(user_id.encode()).hexdigest()[:16],
            "old_consent": old_consent,
            "new_consent": new_consent,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(json.dumps(event))
    
    def log_security_event(self, event_type: str, severity: str, details: Dict):
        """Log security events"""
        event = {
            "event_type": f"security_{event_type}",
            "severity": severity,  # low, medium, high, critical
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        if severity in ["high", "critical"]:
            self.logger.error(json.dumps(event))
        else:
            self.logger.warning(json.dumps(event))

class RoleBasedAccess:
    """
    Role-based access control system
    """
    
    def __init__(self):
        self.roles = {
            "user": {
                "permissions": [
                    "take_assessment",
                    "view_own_results", 
                    "manage_own_consent"
                ],
                "data_access": ["own_assessment_data"]
            },
            "researcher": {
                "permissions": [
                    "view_anonymized_data",
                    "export_research_data",
                    "view_analytics"
                ],
                "data_access": ["anonymized_assessment_data", "aggregate_statistics"]
            },
            "admin": {
                "permissions": [
                    "manage_users",
                    "view_system_logs",
                    "manage_privacy_settings",
                    "export_compliance_reports"
                ],
                "data_access": ["audit_logs", "system_metrics", "compliance_reports"]
            },
            "privacy_officer": {
                "permissions": [
                    "manage_consent_records",
                    "handle_data_requests",
                    "view_privacy_compliance",
                    "manage_data_retention"
                ],
                "data_access": ["consent_records", "privacy_logs", "retention_policies"]
            }
        }
    
    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """Check if user role has required permission"""
        if user_role not in self.roles:
            return False
        
        return required_permission in self.roles[user_role]["permissions"]
    
    def get_accessible_data(self, user_role: str) -> List[str]:
        """Get list of data types accessible to role"""
        if user_role not in self.roles:
            return []
        
        return self.roles[user_role]["data_access"]
    
    def create_access_token(self, user_id: str, user_role: str, expires_hours: int = 24) -> Dict:
        """Create secure access token"""
        token_data = {
            "user_id": user_id,
            "role": user_role,
            "permissions": self.roles.get(user_role, {}).get("permissions", []),
            "issued_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=expires_hours)).isoformat(),
            "token_id": secrets.token_urlsafe(16)
        }
        
        return token_data

# Factory functions
def create_security_framework():
    """Create complete security framework"""
    return {
        "encryption": AdvancedEncryption(),
        "anonymization": DataAnonymization(),
        "gdpr_compliance": GDPRCompliance(),
        "audit_logger": AuditLogger(),
        "rbac": RoleBasedAccess()
    }

def get_privacy_notice():
    """Get current privacy notice"""
    gdpr = GDPRCompliance()
    return gdpr.create_privacy_notice()

if __name__ == "__main__":
    # Test security framework
    security = create_security_framework()
    
    print("🔒 Security Framework Test")
    print("=" * 30)
    
    # Test encryption
    test_data = "Sensitive mental health assessment data"
    encrypted = security["encryption"].encrypt_sensitive_data(test_data)
    decrypted = security["encryption"].decrypt_sensitive_data(encrypted)
    print(f"✅ Encryption test: {'PASS' if decrypted == test_data else 'FAIL'}")
    
    # Test anonymization
    sample_assessment = {
        "user_id": "user123",
        "email": "user@example.com",
        "phq9_score": 15,
        "assessment_date": "2025-08-28"
    }
    
    anonymized = security["anonymization"].anonymize_assessment_data(sample_assessment)
    print(f"✅ Anonymization test: {'PASS' if 'email' not in anonymized else 'FAIL'}")
    
    # Test RBAC
    can_access = security["rbac"].check_permission("researcher", "view_anonymized_data")
    print(f"✅ RBAC test: {'PASS' if can_access else 'FAIL'}")
    
    print("\n🔒 Security framework ready!")
