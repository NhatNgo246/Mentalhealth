"""
Enhanced Security and Compliance Module
Mô-đun Bảo mật và Tuân thủ Nâng cao

Advanced security features and compliance validation for research data collection.
Tính năng bảo mật nâng cao và xác thực tuân thủ cho thu thập dữ liệu nghiên cứu.
"""

import os
import json
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import re
import ipaddress

class SecurityConfig:
    """Security configuration management"""
    
    def __init__(self):
        # Encryption settings
        self.master_key = os.getenv('RESEARCH_MASTER_KEY', self._generate_master_key())
        self.salt = os.getenv('RESEARCH_SALT', self._generate_salt())
        
        # Data retention policies
        self.raw_data_retention_days = int(os.getenv('RAW_DATA_RETENTION_DAYS', '90'))
        self.research_data_retention_years = int(os.getenv('RESEARCH_DATA_RETENTION_YEARS', '5'))
        
        # Privacy settings
        self.k_anonymity_threshold = int(os.getenv('K_ANONYMITY_THRESHOLD', '5'))
        self.enable_differential_privacy = os.getenv('ENABLE_DIFFERENTIAL_PRIVACY', 'false').lower() == 'true'
        self.privacy_budget_epsilon = float(os.getenv('PRIVACY_BUDGET_EPSILON', '1.0'))
        
        # Security validation
        self.require_consent_validation = True
        self.enable_data_integrity_checks = True
        self.enable_audit_logging = True
        
    def _generate_master_key(self) -> str:
        """Generate a new master encryption key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    
    def _generate_salt(self) -> str:
        """Generate a new salt for key derivation"""
        return base64.urlsafe_b64encode(secrets.token_bytes(16)).decode()

class DataEncryption:
    """Data encryption and decryption utilities"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._cipher = self._initialize_cipher()
    
    def _initialize_cipher(self) -> Fernet:
        """Initialize encryption cipher"""
        # Derive key from master key and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=base64.urlsafe_b64decode(self.config.salt.encode()),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.config.master_key.encode()))
        return Fernet(key)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self._cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            self.logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"Decryption error: {e}")
            raise
    
    def hash_pii(self, pii_data: str, salt: Optional[str] = None) -> str:
        """Hash personally identifiable information"""
        if salt is None:
            salt = self.config.salt
        
        # Use HMAC-SHA256 for consistent hashing
        return hmac.new(
            salt.encode(),
            pii_data.encode(),
            hashlib.sha256
        ).hexdigest()

class PrivacyValidator:
    """Privacy compliance validation"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def validate_k_anonymity(self, dataset: List[Dict[str, Any]], 
                           quasi_identifiers: List[str]) -> Dict[str, Any]:
        """Validate K-anonymity for dataset"""
        try:
            if not dataset:
                return {"valid": True, "k_value": float('inf'), "message": "Empty dataset"}
            
            # Group records by quasi-identifier combinations
            groups = {}
            for record in dataset:
                key = tuple(record.get(qi, '') for qi in quasi_identifiers)
                if key not in groups:
                    groups[key] = []
                groups[key].append(record)
            
            # Find minimum group size (K value)
            min_group_size = min(len(group) for group in groups.values()) if groups else 0
            
            is_valid = min_group_size >= self.config.k_anonymity_threshold
            
            return {
                "valid": is_valid,
                "k_value": min_group_size,
                "threshold": self.config.k_anonymity_threshold,
                "total_groups": len(groups),
                "message": f"K-anonymity {'satisfied' if is_valid else 'violated'} (k={min_group_size})"
            }
            
        except Exception as e:
            self.logger.error(f"K-anonymity validation error: {e}")
            return {"valid": False, "error": str(e)}
    
    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """Detect potential PII in text data"""
        pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        }
        
        detected_pii = {}
        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected_pii[pii_type] = matches
        
        return detected_pii
    
    def anonymize_ip_address(self, ip_address: str) -> str:
        """Anonymize IP address by zeroing last octet"""
        try:
            ip = ipaddress.ip_address(ip_address)
            if ip.version == 4:
                # Zero out last octet for IPv4
                octets = str(ip).split('.')
                octets[-1] = '0'
                return '.'.join(octets)
            else:
                # Zero out last 64 bits for IPv6
                return str(ip.supernet(new_prefix=64).network_address)
        except ValueError:
            # If not a valid IP, hash it
            return hashlib.sha256(ip_address.encode()).hexdigest()[:16]
    
    def apply_differential_privacy(self, numeric_value: float, 
                                 epsilon: Optional[float] = None) -> float:
        """Apply differential privacy noise to numeric values"""
        if not self.config.enable_differential_privacy:
            return numeric_value
        
        if epsilon is None:
            epsilon = self.config.privacy_budget_epsilon
        
        # Add Laplace noise for differential privacy
        sensitivity = 1.0  # Assume unit sensitivity
        scale = sensitivity / epsilon
        noise = secrets.SystemRandom().gauss(0, scale)
        
        return numeric_value + noise

class ComplianceValidator:
    """Compliance validation for various regulations"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def validate_gdpr_compliance(self, consent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate GDPR compliance requirements"""
        compliance_checks = {
            "lawful_basis": False,
            "explicit_consent": False,
            "data_minimization": False,
            "purpose_limitation": False,
            "storage_limitation": False,
            "rights_information": False
        }
        
        issues = []
        
        # Check for explicit consent
        if consent_data.get('consent_given') and consent_data.get('consent_explicit'):
            compliance_checks["explicit_consent"] = True
        else:
            issues.append("Explicit consent not recorded")
        
        # Check for purpose specification
        if consent_data.get('research_purpose'):
            compliance_checks["purpose_limitation"] = True
        else:
            issues.append("Research purpose not specified")
        
        # Check for data minimization
        if consent_data.get('minimal_data_collection'):
            compliance_checks["data_minimization"] = True
        else:
            issues.append("Data minimization not confirmed")
        
        # Check for retention policy
        if consent_data.get('retention_policy_explained'):
            compliance_checks["storage_limitation"] = True
        else:
            issues.append("Data retention policy not explained")
        
        # Check for rights information
        if consent_data.get('rights_explained'):
            compliance_checks["rights_information"] = True
        else:
            issues.append("Data subject rights not explained")
        
        # Overall compliance
        is_compliant = all(compliance_checks.values())
        
        return {
            "compliant": is_compliant,
            "checks": compliance_checks,
            "issues": issues,
            "compliance_score": sum(compliance_checks.values()) / len(compliance_checks)
        }
    
    def validate_vietnam_compliance(self, data_collection: Dict[str, Any]) -> Dict[str, Any]:
        """Validate compliance with Vietnamese data protection laws (Nghị định 13/2023/NĐ-CP)"""
        compliance_checks = {
            "consent_vietnamese": False,
            "data_localization": False,
            "security_measures": False,
            "breach_notification": False,
            "data_controller_identified": False
        }
        
        issues = []
        
        # Check for Vietnamese language consent
        if data_collection.get('consent_language') == 'vi':
            compliance_checks["consent_vietnamese"] = True
        else:
            issues.append("Consent not provided in Vietnamese")
        
        # Check for data localization
        if data_collection.get('data_stored_vietnam'):
            compliance_checks["data_localization"] = True
        else:
            issues.append("Data localization requirements not met")
        
        # Check for security measures
        if data_collection.get('encryption_enabled') and data_collection.get('access_controls'):
            compliance_checks["security_measures"] = True
        else:
            issues.append("Adequate security measures not implemented")
        
        # Check for data controller identification
        if data_collection.get('data_controller_info'):
            compliance_checks["data_controller_identified"] = True
        else:
            issues.append("Data controller not properly identified")
        
        is_compliant = all(compliance_checks.values())
        
        return {
            "compliant": is_compliant,
            "checks": compliance_checks,
            "issues": issues,
            "compliance_score": sum(compliance_checks.values()) / len(compliance_checks)
        }

class SecurityAuditor:
    """Security audit and monitoring"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.audit_log_path = Path("logs/security_audit.json")
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        if not self.config.enable_audit_logging:
            return
        
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "severity": self._determine_severity(event_type)
        }
        
        try:
            # Append to audit log
            with open(self.audit_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write audit log: {e}")
    
    def _determine_severity(self, event_type: str) -> str:
        """Determine event severity level"""
        high_severity_events = ['pii_detected', 'encryption_failure', 'unauthorized_access']
        medium_severity_events = ['consent_withdrawal', 'data_export', 'configuration_change']
        
        if event_type in high_severity_events:
            return 'HIGH'
        elif event_type in medium_severity_events:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def perform_security_scan(self, data_directory: str) -> Dict[str, Any]:
        """Perform security scan of data directory"""
        scan_results = {
            "timestamp": datetime.now().isoformat(),
            "directory": data_directory,
            "issues_found": [],
            "recommendations": []
        }
        
        data_path = Path(data_directory)
        if not data_path.exists():
            scan_results["issues_found"].append("Data directory does not exist")
            return scan_results
        
        # Check file permissions
        for file_path in data_path.rglob("*"):
            if file_path.is_file():
                # Check for overly permissive file permissions
                if oct(file_path.stat().st_mode)[-3:] != '600':
                    scan_results["issues_found"].append(f"File {file_path} has permissive permissions")
                    scan_results["recommendations"].append(f"Set secure permissions: chmod 600 {file_path}")
        
        # Check for unencrypted sensitive files
        sensitive_patterns = ['*.json', '*.csv', '*.log']
        for pattern in sensitive_patterns:
            for file_path in data_path.glob(pattern):
                if self._contains_sensitive_data(file_path):
                    scan_results["issues_found"].append(f"Potentially sensitive data in {file_path}")
                    scan_results["recommendations"].append(f"Encrypt sensitive file: {file_path}")
        
        return scan_results
    
    def _contains_sensitive_data(self, file_path: Path) -> bool:
        """Check if file contains sensitive data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1024)  # Check first 1KB
                
            # Look for patterns that might indicate sensitive data
            sensitive_keywords = ['email', 'phone', 'address', 'ssn', 'id_number']
            return any(keyword in content.lower() for keyword in sensitive_keywords)
            
        except Exception:
            return False

class ResearchSecurity:
    """Main security interface for research system"""
    
    def __init__(self):
        self.config = SecurityConfig()
        self.encryption = DataEncryption(self.config)
        self.privacy_validator = PrivacyValidator(self.config)
        self.compliance_validator = ComplianceValidator(self.config)
        self.auditor = SecurityAuditor(self.config)
        self.logger = logging.getLogger(__name__)
    
    def secure_data_collection(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply security measures to collected data"""
        try:
            secured_data = raw_data.copy()
            
            # Detect and handle PII
            if 'user_data' in secured_data:
                pii_detected = self.privacy_validator.detect_pii(str(secured_data['user_data']))
                if pii_detected:
                    self.auditor.log_security_event('pii_detected', {'types': list(pii_detected.keys())})
                    # Remove or hash PII
                    for pii_type, values in pii_detected.items():
                        for value in values:
                            secured_data['user_data'] = str(secured_data['user_data']).replace(
                                value, f"[{pii_type.upper()}_HASHED]"
                            )
            
            # Anonymize IP addresses
            if 'ip_address' in secured_data:
                secured_data['ip_address'] = self.privacy_validator.anonymize_ip_address(
                    secured_data['ip_address']
                )
            
            # Apply differential privacy to numeric values
            for key, value in secured_data.items():
                if isinstance(value, (int, float)) and key.startswith('score_'):
                    secured_data[key] = self.privacy_validator.apply_differential_privacy(value)
            
            # Add data integrity hash
            secured_data['data_hash'] = self._calculate_integrity_hash(secured_data)
            
            # Log security processing
            self.auditor.log_security_event('data_secured', {
                'data_type': secured_data.get('event_type', 'unknown'),
                'security_applied': True
            })
            
            return secured_data
            
        except Exception as e:
            self.logger.error(f"Error securing data: {e}")
            self.auditor.log_security_event('security_error', {'error': str(e)})
            raise
    
    def validate_compliance(self, consent_data: Dict[str, Any], 
                          collection_context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate comprehensive compliance"""
        validation_results = {
            "overall_compliant": False,
            "gdpr_compliance": {},
            "vietnam_compliance": {},
            "security_status": {},
            "recommendations": []
        }
        
        try:
            # GDPR validation
            gdpr_result = self.compliance_validator.validate_gdpr_compliance(consent_data)
            validation_results["gdpr_compliance"] = gdpr_result
            
            # Vietnam compliance validation
            vietnam_result = self.compliance_validator.validate_vietnam_compliance(collection_context)
            validation_results["vietnam_compliance"] = vietnam_result
            
            # Security scan
            security_scan = self.auditor.perform_security_scan("research_data")
            validation_results["security_status"] = security_scan
            
            # Overall compliance
            validation_results["overall_compliant"] = (
                gdpr_result.get("compliant", False) and 
                vietnam_result.get("compliant", False) and
                len(security_scan.get("issues_found", [])) == 0
            )
            
            # Generate recommendations
            if not validation_results["overall_compliant"]:
                validation_results["recommendations"].extend(gdpr_result.get("issues", []))
                validation_results["recommendations"].extend(vietnam_result.get("issues", []))
                validation_results["recommendations"].extend(security_scan.get("recommendations", []))
            
            # Log compliance check
            self.auditor.log_security_event('compliance_check', {
                'compliant': validation_results["overall_compliant"],
                'gdpr_score': gdpr_result.get("compliance_score", 0),
                'vietnam_score': vietnam_result.get("compliance_score", 0)
            })
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Error validating compliance: {e}")
            return {"error": str(e)}
    
    def _calculate_integrity_hash(self, data: Dict[str, Any]) -> str:
        """Calculate data integrity hash"""
        # Remove existing hash if present
        data_copy = {k: v for k, v in data.items() if k != 'data_hash'}
        data_str = json.dumps(data_copy, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

def main():
    """Demo security functionality"""
    print("🔒 RESEARCH SECURITY MODULE")
    print("=" * 40)
    
    # Initialize security system
    print("🔧 Initializing security system...")
    security = ResearchSecurity()
    
    # Test data encryption
    print("🔐 Testing data encryption...")
    test_data = "sensitive research data"
    encrypted = security.encryption.encrypt_data(test_data)
    decrypted = security.encryption.decrypt_data(encrypted)
    print(f"✅ Encryption/decryption {'successful' if test_data == decrypted else 'failed'}")
    
    # Test PII detection
    print("🔍 Testing PII detection...")
    test_text = "Contact john.doe@example.com or call 555-123-4567"
    pii_detected = security.privacy_validator.detect_pii(test_text)
    print(f"✅ PII detected: {list(pii_detected.keys())}")
    
    # Test compliance validation
    print("📋 Testing compliance validation...")
    test_consent = {
        'consent_given': True,
        'consent_explicit': True,
        'research_purpose': 'Mental health research',
        'minimal_data_collection': True,
        'retention_policy_explained': True,
        'rights_explained': True
    }
    
    test_context = {
        'consent_language': 'vi',
        'data_stored_vietnam': True,
        'encryption_enabled': True,
        'access_controls': True,
        'data_controller_info': True
    }
    
    compliance_result = security.validate_compliance(test_consent, test_context)
    print(f"✅ Overall compliance: {compliance_result.get('overall_compliant', False)}")
    
    # Test security scan
    print("🔍 Testing security scan...")
    scan_result = security.auditor.perform_security_scan("research_data")
    print(f"✅ Security issues found: {len(scan_result.get('issues_found', []))}")
    
    print("\n🎉 Security module tested successfully!")

if __name__ == "__main__":
    main()
