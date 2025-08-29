"""
Research System Configuration Management
Quản lý Cấu hình Hệ thống Nghiên cứu

Centralized configuration management for all research system components.
Quản lý cấu hình tập trung cho tất cả các thành phần hệ thống nghiên cứu.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    master_key: str = ""
    salt: str = ""
    encryption_enabled: bool = True
    k_anonymity_threshold: int = 5
    enable_differential_privacy: bool = False
    privacy_budget_epsilon: float = 1.0
    require_consent_validation: bool = True
    enable_data_integrity_checks: bool = True
    enable_audit_logging: bool = True

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    db_type: str = "sqlite"  # sqlite or postgresql
    db_path: str = "research_data/research.db"
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_database: str = "research_db"
    pg_username: str = "research_user"
    pg_password: str = ""
    connection_pool_size: int = 10
    query_timeout: int = 30

@dataclass
class CollectionConfig:
    """Data collection configuration settings"""
    enable_collection: bool = False
    api_endpoint: str = "http://localhost:8502"
    timeout_seconds: int = 1
    max_retries: int = 3
    batch_size: int = 100
    collection_interval: int = 60
    enable_real_time_collection: bool = True

@dataclass
class AnalyticsConfig:
    """Analytics configuration settings"""
    enable_analytics: bool = True
    report_generation_interval: int = 3600
    data_retention_days: int = 90
    enable_behavioral_analysis: bool = True
    enable_compliance_monitoring: bool = True
    export_format: str = "json"  # json, csv, xlsx

@dataclass
class MonitoringConfig:
    """System monitoring configuration settings"""
    enable_monitoring: bool = True
    monitoring_interval: int = 30
    health_check_timeout: int = 5
    enable_real_time_alerts: bool = True
    alert_channels: list = None
    performance_thresholds: Dict[str, float] = None

@dataclass
class ComplianceConfig:
    """Compliance configuration settings"""
    gdpr_compliance: bool = True
    vietnam_compliance: bool = True
    data_localization: bool = True
    consent_language: str = "vi"
    retention_policy_days: int = 1825  # 5 years
    enable_right_to_erasure: bool = True

class ResearchSystemConfig:
    """Main configuration manager for research system"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = Path(config_file) if config_file else Path("research_system/config.yaml")
        self.logger = logging.getLogger(__name__)
        
        # Initialize configuration sections
        self.security = SecurityConfig()
        self.database = DatabaseConfig()
        self.collection = CollectionConfig()
        self.analytics = AnalyticsConfig()
        self.monitoring = MonitoringConfig()
        self.compliance = ComplianceConfig()
        
        # Set default values for complex fields
        if self.monitoring.alert_channels is None:
            self.monitoring.alert_channels = ["console", "log"]
        
        if self.monitoring.performance_thresholds is None:
            self.monitoring.performance_thresholds = {
                "max_error_rate": 0.05,
                "max_response_time_ms": 1000,
                "max_events_per_hour": 1000
            }
        
        # Load configuration if file exists
        self.load_config()
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if not self.config_file.exists():
                self.logger.info(f"Config file {self.config_file} not found, using defaults")
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if self.config_file.suffix.lower() == '.yaml':
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            # Update configuration sections
            if 'security' in config_data:
                self._update_dataclass(self.security, config_data['security'])
            
            if 'database' in config_data:
                self._update_dataclass(self.database, config_data['database'])
            
            if 'collection' in config_data:
                self._update_dataclass(self.collection, config_data['collection'])
            
            if 'analytics' in config_data:
                self._update_dataclass(self.analytics, config_data['analytics'])
            
            if 'monitoring' in config_data:
                self._update_dataclass(self.monitoring, config_data['monitoring'])
            
            if 'compliance' in config_data:
                self._update_dataclass(self.compliance, config_data['compliance'])
            
            self.logger.info(f"Configuration loaded from {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            # Create directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare configuration data
            config_data = {
                'security': asdict(self.security),
                'database': asdict(self.database),
                'collection': asdict(self.collection),
                'analytics': asdict(self.analytics),
                'monitoring': asdict(self.monitoring),
                'compliance': asdict(self.compliance)
            }
            
            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.suffix.lower() == '.yaml':
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
                else:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
    
    def _update_dataclass(self, instance, data: Dict[str, Any]):
        """Update dataclass instance with dictionary data"""
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
    
    def get_env_overrides(self) -> Dict[str, Any]:
        """Get configuration overrides from environment variables"""
        overrides = {}
        
        # Security overrides
        if os.getenv('RESEARCH_MASTER_KEY'):
            overrides.setdefault('security', {})['master_key'] = os.getenv('RESEARCH_MASTER_KEY')
        
        if os.getenv('RESEARCH_ENCRYPTION_ENABLED'):
            overrides.setdefault('security', {})['encryption_enabled'] = os.getenv('RESEARCH_ENCRYPTION_ENABLED').lower() == 'true'
        
        # Database overrides
        if os.getenv('RESEARCH_DB_TYPE'):
            overrides.setdefault('database', {})['db_type'] = os.getenv('RESEARCH_DB_TYPE')
        
        if os.getenv('RESEARCH_DB_PATH'):
            overrides.setdefault('database', {})['db_path'] = os.getenv('RESEARCH_DB_PATH')
        
        # Collection overrides
        if os.getenv('ENABLE_RESEARCH_COLLECTION'):
            overrides.setdefault('collection', {})['enable_collection'] = os.getenv('ENABLE_RESEARCH_COLLECTION').lower() == 'true'
        
        if os.getenv('RESEARCH_API_ENDPOINT'):
            overrides.setdefault('collection', {})['api_endpoint'] = os.getenv('RESEARCH_API_ENDPOINT')
        
        # Apply overrides
        for section, values in overrides.items():
            if section == 'security':
                self._update_dataclass(self.security, values)
            elif section == 'database':
                self._update_dataclass(self.database, values)
            elif section == 'collection':
                self._update_dataclass(self.collection, values)
        
        return overrides
    
    def apply_env_overrides(self):
        """Apply environment variable overrides"""
        overrides = self.get_env_overrides()
        if overrides:
            self.logger.info(f"Applied environment overrides: {list(overrides.keys())}")
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Validate configuration settings"""
        issues = {}
        
        # Validate security settings
        security_issues = []
        if not self.security.master_key:
            security_issues.append("Master key is not set")
        
        if self.security.k_anonymity_threshold < 1:
            security_issues.append("K-anonymity threshold must be >= 1")
        
        if security_issues:
            issues['security'] = security_issues
        
        # Validate database settings
        database_issues = []
        if self.database.db_type not in ['sqlite', 'postgresql']:
            database_issues.append("Database type must be 'sqlite' or 'postgresql'")
        
        if self.database.db_type == 'sqlite' and not self.database.db_path:
            database_issues.append("SQLite database path is required")
        
        if self.database.db_type == 'postgresql':
            if not self.database.pg_host:
                database_issues.append("PostgreSQL host is required")
            if not self.database.pg_database:
                database_issues.append("PostgreSQL database name is required")
        
        if database_issues:
            issues['database'] = database_issues
        
        # Validate collection settings
        collection_issues = []
        if self.collection.timeout_seconds <= 0:
            collection_issues.append("Timeout must be > 0")
        
        if self.collection.max_retries < 0:
            collection_issues.append("Max retries must be >= 0")
        
        if collection_issues:
            issues['collection'] = collection_issues
        
        # Validate compliance settings
        compliance_issues = []
        if self.compliance.retention_policy_days <= 0:
            compliance_issues.append("Retention policy days must be > 0")
        
        if self.compliance.consent_language not in ['vi', 'en']:
            compliance_issues.append("Consent language must be 'vi' or 'en'")
        
        if compliance_issues:
            issues['compliance'] = compliance_issues
        
        return issues
    
    def export_config_template(self, output_file: str = "research_config_template.yaml"):
        """Export configuration template with comments"""
        template = {
            'security': {
                'master_key': '# Set your master encryption key here',
                'salt': '# Set your encryption salt here',
                'encryption_enabled': True,
                'k_anonymity_threshold': 5,
                'enable_differential_privacy': False,
                'privacy_budget_epsilon': 1.0,
                'require_consent_validation': True,
                'enable_data_integrity_checks': True,
                'enable_audit_logging': True
            },
            'database': {
                'db_type': 'sqlite',  # or 'postgresql'
                'db_path': 'research_data/research.db',
                'pg_host': 'localhost',
                'pg_port': 5432,
                'pg_database': 'research_db',
                'pg_username': 'research_user',
                'pg_password': '# Set PostgreSQL password',
                'connection_pool_size': 10,
                'query_timeout': 30
            },
            'collection': {
                'enable_collection': False,  # Set to true to enable
                'api_endpoint': 'http://localhost:8502',
                'timeout_seconds': 1,
                'max_retries': 3,
                'batch_size': 100,
                'collection_interval': 60,
                'enable_real_time_collection': True
            },
            'analytics': {
                'enable_analytics': True,
                'report_generation_interval': 3600,
                'data_retention_days': 90,
                'enable_behavioral_analysis': True,
                'enable_compliance_monitoring': True,
                'export_format': 'json'
            },
            'monitoring': {
                'enable_monitoring': True,
                'monitoring_interval': 30,
                'health_check_timeout': 5,
                'enable_real_time_alerts': True,
                'alert_channels': ['console', 'log'],
                'performance_thresholds': {
                    'max_error_rate': 0.05,
                    'max_response_time_ms': 1000,
                    'max_events_per_hour': 1000
                }
            },
            'compliance': {
                'gdpr_compliance': True,
                'vietnam_compliance': True,
                'data_localization': True,
                'consent_language': 'vi',
                'retention_policy_days': 1825,
                'enable_right_to_erasure': True
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(template, f, default_flow_style=False, allow_unicode=True)
        
        self.logger.info(f"Configuration template exported to {output_file}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary"""
        return {
            'security': {
                'encryption_enabled': self.security.encryption_enabled,
                'k_anonymity_threshold': self.security.k_anonymity_threshold,
                'audit_logging': self.security.enable_audit_logging
            },
            'database': {
                'type': self.database.db_type,
                'path': self.database.db_path if self.database.db_type == 'sqlite' else f"{self.database.pg_host}:{self.database.pg_port}/{self.database.pg_database}"
            },
            'collection': {
                'enabled': self.collection.enable_collection,
                'endpoint': self.collection.api_endpoint,
                'real_time': self.collection.enable_real_time_collection
            },
            'compliance': {
                'gdpr': self.compliance.gdpr_compliance,
                'vietnam': self.compliance.vietnam_compliance,
                'retention_days': self.compliance.retention_policy_days
            }
        }

def main():
    """Demo configuration management"""
    print("⚙️ RESEARCH SYSTEM CONFIGURATION")
    print("=" * 40)
    
    # Initialize configuration
    print("🔧 Initializing configuration...")
    config = ResearchSystemConfig()
    
    # Apply environment overrides
    print("🌍 Applying environment overrides...")
    config.apply_env_overrides()
    
    # Validate configuration
    print("✅ Validating configuration...")
    issues = config.validate_config()
    if issues:
        print("⚠️ Configuration issues found:")
        for section, section_issues in issues.items():
            print(f"   {section}:")
            for issue in section_issues:
                print(f"     - {issue}")
    else:
        print("✅ Configuration is valid")
    
    # Show configuration summary
    print("\n📊 Configuration Summary:")
    summary = config.get_config_summary()
    for section, values in summary.items():
        print(f"   {section}:")
        for key, value in values.items():
            print(f"     {key}: {value}")
    
    # Save configuration
    print("\n💾 Saving configuration...")
    success = config.save_config()
    if success:
        print(f"✅ Configuration saved to {config.config_file}")
    else:
        print("❌ Failed to save configuration")
    
    # Export template
    print("\n📄 Exporting configuration template...")
    config.export_config_template()
    print("✅ Template exported to research_config_template.yaml")
    
    print("\n🎉 Configuration management demo completed!")

if __name__ == "__main__":
    main()
