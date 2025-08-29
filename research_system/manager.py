"""
Advanced Research System Manager
Quản lý Hệ thống Nghiên cứu Nâng cao

Central management interface for all research system components.
Giao diện quản lý trung tâm cho tất cả các thành phần hệ thống nghiên cứu.
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import threading
import time
from dataclasses import dataclass

# Import research system components
from .analytics import ResearchAnalytics
from .database import ResearchDatabase
from .security import ResearchSecurity
from .collector import SafeResearchCollector
from .integration import (
    safe_track_session_start,
    safe_track_questionnaire_start,
    safe_track_questionnaire_completion,
    safe_track_question_answer,
    safe_track_results_view
)

@dataclass
class SystemStatus:
    """System status information"""
    component: str
    status: str  # 'healthy', 'warning', 'error', 'offline'
    last_check: datetime
    details: Dict[str, Any]
    metrics: Dict[str, Any]

class ResearchSystemManager:
    """Advanced manager for the entire research system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_configuration()
        
        # Initialize components
        self.analytics = ResearchAnalytics()
        self.database = ResearchDatabase()
        self.security = ResearchSecurity()
        self.collector = SafeResearchCollector()
        
        # System monitoring
        self.component_status: Dict[str, SystemStatus] = {}
        self.monitoring_enabled = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {
            'data_collected': [],
            'compliance_violation': [],
            'security_alert': [],
            'system_error': []
        }
        
        # Performance metrics
        self.metrics = {
            'total_events_processed': 0,
            'events_per_hour': 0,
            'error_rate': 0,
            'last_activity': None
        }
        
        self._initialize_system()
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load system configuration"""
        config_file = Path("research_system/config.json")
        default_config = {
            "monitoring_interval": 30,
            "health_check_timeout": 5,
            "auto_cleanup_enabled": True,
            "compliance_validation_interval": 3600,
            "performance_alert_threshold": 100,
            "max_error_rate": 0.05,
            "enable_real_time_monitoring": True,
            "enable_automated_responses": True,
            "log_level": "INFO"
        }
        
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            self.logger.warning(f"Could not load config file: {e}")
        
        return default_config
    
    def _initialize_system(self):
        """Initialize the research system"""
        self.logger.info("Initializing Research System Manager...")
        
        # Set up logging
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        logging.basicConfig(level=log_level)
        
        # Initialize component status
        components = ['analytics', 'database', 'security', 'collector', 'api']
        for component in components:
            self.component_status[component] = SystemStatus(
                component=component,
                status='offline',
                last_check=datetime.now(),
                details={},
                metrics={}
            )
        
        # Start monitoring if enabled
        if self.config.get('enable_real_time_monitoring', True):
            self.start_monitoring()
    
    def start_monitoring(self):
        """Start system monitoring"""
        if self.monitoring_enabled:
            return
        
        self.monitoring_enabled = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("System monitoring started")
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_enabled = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("System monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_enabled:
            try:
                self._perform_health_checks()
                self._update_performance_metrics()
                self._check_compliance()
                
                # Sleep for monitoring interval
                time.sleep(self.config.get('monitoring_interval', 30))
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Brief pause before retrying
    
    def _perform_health_checks(self):
        """Perform health checks on all components"""
        # Check analytics component
        try:
            df = self.analytics.load_collected_data(days_back=1)
            self.component_status['analytics'] = SystemStatus(
                component='analytics',
                status='healthy',
                last_check=datetime.now(),
                details={'data_available': not df.empty},
                metrics={'records_loaded': len(df)}
            )
        except Exception as e:
            self.component_status['analytics'] = SystemStatus(
                component='analytics',
                status='error',
                last_check=datetime.now(),
                details={'error': str(e)},
                metrics={}
            )
        
        # Check database component
        try:
            test_event = {
                'session_id': 'health_check',
                'event_type': 'health_check',
                'timestamp': datetime.now().isoformat(),
                'anonymized_user_id': 'health_check_user',
                'consent_status': 'given'
            }
            success = self.database.store_event(test_event)
            
            self.component_status['database'] = SystemStatus(
                component='database',
                status='healthy' if success else 'warning',
                last_check=datetime.now(),
                details={'write_test': success},
                metrics={}
            )
        except Exception as e:
            self.component_status['database'] = SystemStatus(
                component='database',
                status='error',
                last_check=datetime.now(),
                details={'error': str(e)},
                metrics={}
            )
        
        # Check security component
        try:
            # Test encryption
            test_data = "health_check_data"
            encrypted = self.security.encryption.encrypt_data(test_data)
            decrypted = self.security.encryption.decrypt_data(encrypted)
            encryption_ok = (test_data == decrypted)
            
            self.component_status['security'] = SystemStatus(
                component='security',
                status='healthy' if encryption_ok else 'error',
                last_check=datetime.now(),
                details={'encryption_test': encryption_ok},
                metrics={}
            )
        except Exception as e:
            self.component_status['security'] = SystemStatus(
                component='security',
                status='error',
                last_check=datetime.now(),
                details={'error': str(e)},
                metrics={}
            )
        
        # Check collector component
        try:
            # Test collector functionality
            collector_status = self.collector.get_collection_status()
            
            self.component_status['collector'] = SystemStatus(
                component='collector',
                status='healthy',
                last_check=datetime.now(),
                details=collector_status,
                metrics={'events_collected': collector_status.get('total_events', 0)}
            )
        except Exception as e:
            self.component_status['collector'] = SystemStatus(
                component='collector',
                status='error',
                last_check=datetime.now(),
                details={'error': str(e)},
                metrics={}
            )
        
        # Check API component (if running)
        try:
            import requests
            response = requests.get('http://localhost:8502/health', timeout=5)
            api_healthy = response.status_code == 200
            
            self.component_status['api'] = SystemStatus(
                component='api',
                status='healthy' if api_healthy else 'warning',
                last_check=datetime.now(),
                details={'response_code': response.status_code if api_healthy else 'timeout'},
                metrics={'response_time_ms': response.elapsed.total_seconds() * 1000 if api_healthy else 0}
            )
        except Exception as e:
            self.component_status['api'] = SystemStatus(
                component='api',
                status='offline',
                last_check=datetime.now(),
                details={'error': str(e)},
                metrics={}
            )
    
    def _update_performance_metrics(self):
        """Update system performance metrics"""
        try:
            # Load recent data
            df = self.analytics.load_collected_data(days_back=1)
            
            if not df.empty:
                # Calculate events per hour
                now = datetime.now()
                hour_ago = now - timedelta(hours=1)
                recent_events = len(df[df['timestamp'] >= hour_ago])
                self.metrics['events_per_hour'] = recent_events
                
                # Update total events
                self.metrics['total_events_processed'] = len(df)
                self.metrics['last_activity'] = df['timestamp'].max().isoformat()
                
                # Calculate error rate (placeholder - would need error tracking)
                self.metrics['error_rate'] = 0.01  # 1% placeholder
            
            # Check for performance alerts
            if self.metrics['events_per_hour'] > self.config.get('performance_alert_threshold', 100):
                self._trigger_event('system_alert', {
                    'type': 'high_load',
                    'events_per_hour': self.metrics['events_per_hour']
                })
            
            if self.metrics['error_rate'] > self.config.get('max_error_rate', 0.05):
                self._trigger_event('system_alert', {
                    'type': 'high_error_rate',
                    'error_rate': self.metrics['error_rate']
                })
                
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    def _check_compliance(self):
        """Check compliance status"""
        try:
            # Get recent events for compliance checking
            df = self.analytics.load_collected_data(days_back=7)
            
            if not df.empty:
                # Generate compliance report
                privacy_report = self.analytics.generate_privacy_compliance_report(df)
                
                if privacy_report.get('privacy_status') != 'COMPLIANT':
                    self._trigger_event('compliance_violation', privacy_report)
                
        except Exception as e:
            self.logger.error(f"Error checking compliance: {e}")
    
    def _trigger_event(self, event_type: str, data: Dict[str, Any]):
        """Trigger system events"""
        try:
            # Log the event
            self.logger.info(f"System event triggered: {event_type}")
            
            # Call registered handlers
            for handler in self.event_handlers.get(event_type, []):
                try:
                    handler(data)
                except Exception as e:
                    self.logger.error(f"Error in event handler: {e}")
            
            # Auto-responses if enabled
            if self.config.get('enable_automated_responses', True):
                self._handle_automated_response(event_type, data)
                
        except Exception as e:
            self.logger.error(f"Error triggering event: {e}")
    
    def _handle_automated_response(self, event_type: str, data: Dict[str, Any]):
        """Handle automated responses to system events"""
        if event_type == 'compliance_violation':
            # Auto-cleanup if privacy issues detected
            if self.config.get('auto_cleanup_enabled', True):
                self.logger.info("Auto-cleaning old data due to compliance violation")
                self.database.cleanup_old_data(retention_days=30)
        
        elif event_type == 'high_error_rate':
            # Reduce collection rate if error rate is high
            self.logger.warning("High error rate detected, implementing throttling")
            # Could implement collection throttling here
        
        elif event_type == 'security_alert':
            # Auto-disable collection if security breach detected
            self.logger.critical("Security alert detected, consider disabling collection")
            # Could auto-disable collection here
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register custom event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status_summary = {
            'overall_status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {},
            'metrics': self.metrics,
            'alerts': []
        }
        
        # Component status
        for component, status in self.component_status.items():
            status_summary['components'][component] = {
                'status': status.status,
                'last_check': status.last_check.isoformat(),
                'details': status.details,
                'metrics': status.metrics
            }
            
            # Update overall status
            if status.status in ['error', 'offline']:
                status_summary['overall_status'] = 'degraded'
            elif status.status == 'warning' and status_summary['overall_status'] == 'healthy':
                status_summary['overall_status'] = 'warning'
        
        # Generate alerts
        alerts = []
        for component, status in self.component_status.items():
            if status.status in ['error', 'offline']:
                alerts.append({
                    'severity': 'high',
                    'component': component,
                    'message': f"{component} is {status.status}",
                    'details': status.details
                })
            elif status.status == 'warning':
                alerts.append({
                    'severity': 'medium',
                    'component': component,
                    'message': f"{component} has warnings",
                    'details': status.details
                })
        
        status_summary['alerts'] = alerts
        return status_summary
    
    def perform_maintenance(self) -> Dict[str, Any]:
        """Perform system maintenance tasks"""
        maintenance_results = {
            'timestamp': datetime.now().isoformat(),
            'tasks_performed': [],
            'issues_found': [],
            'recommendations': []
        }
        
        try:
            # Data cleanup
            if self.config.get('auto_cleanup_enabled', True):
                cleaned_records = self.database.cleanup_old_data()
                maintenance_results['tasks_performed'].append(
                    f"Cleaned up {cleaned_records} old records"
                )
            
            # Security scan
            security_scan = self.security.auditor.perform_security_scan("research_data")
            if security_scan.get('issues_found'):
                maintenance_results['issues_found'].extend(security_scan['issues_found'])
                maintenance_results['recommendations'].extend(security_scan['recommendations'])
            
            # Analytics optimization
            analytics_report = self.analytics.export_analytics_report()
            maintenance_results['tasks_performed'].append(
                f"Generated analytics report: {analytics_report}"
            )
            
            # Component health verification
            unhealthy_components = [
                name for name, status in self.component_status.items()
                if status.status in ['error', 'offline']
            ]
            
            if unhealthy_components:
                maintenance_results['issues_found'].append(
                    f"Unhealthy components: {', '.join(unhealthy_components)}"
                )
                maintenance_results['recommendations'].append(
                    "Investigate and fix unhealthy components"
                )
            
            self.logger.info("System maintenance completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during maintenance: {e}")
            maintenance_results['issues_found'].append(f"Maintenance error: {str(e)}")
        
        return maintenance_results
    
    def export_system_report(self, output_path: Optional[str] = None) -> str:
        """Export comprehensive system report"""
        report = {
            'system_status': self.get_system_status(),
            'analytics_summary': {},
            'compliance_status': {},
            'performance_metrics': self.metrics,
            'configuration': self.config
        }
        
        try:
            # Add analytics data
            df = self.analytics.load_collected_data(days_back=30)
            if not df.empty:
                report['analytics_summary'] = self.analytics.generate_usage_statistics(df)
                report['compliance_status'] = self.analytics.generate_privacy_compliance_report(df)
            
            # Export to file
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"research_system_report_{timestamp}.json"
            
            output_file = Path("research_data") / output_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"System report exported to {output_file}")
            return str(output_file)
            
        except Exception as e:
            self.logger.error(f"Error exporting system report: {e}")
            raise
    
    def shutdown(self):
        """Gracefully shutdown the research system"""
        self.logger.info("Shutting down Research System Manager...")
        
        try:
            # Stop monitoring
            self.stop_monitoring()
            
            # Perform final maintenance
            self.perform_maintenance()
            
            # Export final report
            self.export_system_report("shutdown_report.json")
            
            self.logger.info("Research System Manager shutdown completed")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

# Global manager instance
_manager_instance: Optional[ResearchSystemManager] = None

def get_research_manager() -> ResearchSystemManager:
    """Get or create the global research system manager"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = ResearchSystemManager()
    return _manager_instance

def main():
    """Demo advanced research system management"""
    print("🎛️ ADVANCED RESEARCH SYSTEM MANAGER")
    print("=" * 50)
    
    # Initialize manager
    print("🚀 Initializing Research System Manager...")
    manager = ResearchSystemManager()
    
    # Wait for initial health checks
    print("⏳ Performing initial health checks...")
    time.sleep(5)
    
    # Get system status
    print("📊 Getting system status...")
    status = manager.get_system_status()
    print(f"✅ Overall status: {status['overall_status']}")
    print(f"✅ Components healthy: {sum(1 for c in status['components'].values() if c['status'] == 'healthy')}")
    print(f"✅ Active alerts: {len(status['alerts'])}")
    
    # Perform maintenance
    print("🔧 Performing system maintenance...")
    maintenance_result = manager.perform_maintenance()
    print(f"✅ Maintenance tasks: {len(maintenance_result['tasks_performed'])}")
    print(f"✅ Issues found: {len(maintenance_result['issues_found'])}")
    
    # Export system report
    print("📄 Exporting system report...")
    report_file = manager.export_system_report()
    print(f"✅ Report exported to: {report_file}")
    
    # Shutdown
    print("🛑 Shutting down system...")
    manager.shutdown()
    
    print("\n🎉 Advanced research system management demo completed!")

if __name__ == "__main__":
    main()
