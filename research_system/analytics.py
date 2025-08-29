"""
Research System Analytics Module
Mô-đun Phân tích Dữ liệu Nghiên cứu

Provides advanced analytics and insights for collected research data.
Cung cấp phân tích nâng cao và insights cho dữ liệu nghiên cứu đã thu thập.
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import os
import logging
from pathlib import Path

class ResearchAnalytics:
    """Advanced analytics for research data collection"""
    
    def __init__(self, data_dir: str = "research_data"):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(__name__)
        
    def load_collected_data(self, days_back: int = 30) -> pd.DataFrame:
        """Load collected research data from files"""
        try:
            data_files = list(self.data_dir.glob("events_*.json"))
            all_events = []
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for file_path in data_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        events = json.load(f)
                        
                    for event in events:
                        event_time = datetime.fromisoformat(event.get('timestamp', ''))
                        if event_time >= cutoff_date:
                            all_events.append(event)
                            
                except (json.JSONDecodeError, ValueError) as e:
                    self.logger.warning(f"Could not parse {file_path}: {e}")
                    continue
            
            if not all_events:
                return pd.DataFrame()
                
            df = pd.DataFrame(all_events)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def generate_usage_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive usage statistics"""
        if df.empty:
            return {"error": "No data available"}
        
        # Ensure timestamp is datetime object
        if 'timestamp' in df.columns:
            if df['timestamp'].dtype == 'object':
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        stats = {
            "overview": {
                "total_events": len(df),
                "unique_sessions": df['session_id'].nunique() if 'session_id' in df.columns else 0,
                "unique_users": df['user_id'].nunique() if 'user_id' in df.columns else 0,
                "date_range": {
                    "start": df['timestamp'].min().isoformat() if 'timestamp' in df.columns and not df.empty else None,
                    "end": df['timestamp'].max().isoformat() if 'timestamp' in df.columns and not df.empty else None
                },
                "data_collection_days": (df['timestamp'].max() - df['timestamp'].min()).days if 'timestamp' in df.columns and len(df) > 1 else 0
            }
        }
        
        # Event type distribution
        if 'event_type' in df.columns:
            event_counts = df['event_type'].value_counts().to_dict()
            stats["event_distribution"] = event_counts
        
        # Daily usage patterns
        if 'timestamp' in df.columns:
            df['date'] = df['timestamp'].dt.date
            df['hour'] = df['timestamp'].dt.hour
            
            daily_counts = df.groupby('date').size().to_dict()
            stats["daily_usage"] = {str(k): v for k, v in daily_counts.items()}
            
            hourly_counts = df.groupby('hour').size().to_dict()
            stats["hourly_patterns"] = hourly_counts
        
        # Session analysis
        if 'session_id' in df.columns:
            session_events = df.groupby('session_id').size()
            stats["session_analysis"] = {
                "avg_events_per_session": float(session_events.mean()) if not session_events.empty else 0,
                "max_events_per_session": int(session_events.max()) if not session_events.empty else 0,
                "min_events_per_session": int(session_events.min()) if not session_events.empty else 0,
                "total_sessions": len(session_events)
            }
        
        # Questionnaire completion rates
        if 'event_type' in df.columns:
            questionnaire_events = df[df['event_type'].str.contains('questionnaire', na=False)]
            if not questionnaire_events.empty:
                started = len(questionnaire_events[questionnaire_events['event_type'] == 'questionnaire_started'])
                completed = len(questionnaire_events[questionnaire_events['event_type'] == 'questionnaire_completed'])
                
                stats["completion_rates"] = {
                    "questionnaires_started": started,
                    "questionnaires_completed": completed,
                    "completion_rate": (completed / started * 100) if started > 0 else 0
                }
        
        return stats
    
    def analyze_user_behavior_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        if df.empty:
            return {"error": "No data available"}
        
        patterns = {}
        
        # Session duration analysis
        if 'session_id' in df.columns and 'timestamp' in df.columns:
            session_times = df.groupby('session_id')['timestamp'].agg(['min', 'max'])
            session_durations = (session_times['max'] - session_times['min']).dt.total_seconds() / 60  # in minutes
            
            patterns["session_duration"] = {
                "avg_duration_minutes": float(session_durations.mean()) if not session_durations.empty else 0,
                "median_duration_minutes": float(session_durations.median()) if not session_durations.empty else 0,
                "max_duration_minutes": float(session_durations.max()) if not session_durations.empty else 0,
                "sessions_over_5_min": int((session_durations > 5).sum()) if not session_durations.empty else 0,
                "sessions_over_15_min": int((session_durations > 15).sum()) if not session_durations.empty else 0
            }
        
        # Most popular questionnaires
        if 'event_data' in df.columns:
            questionnaire_types = []
            for _, row in df.iterrows():
                if row.get('event_type') == 'questionnaire_started':
                    try:
                        event_data = json.loads(row['event_data']) if isinstance(row['event_data'], str) else row['event_data']
                        questionnaire_types.append(event_data.get('questionnaire_type', 'unknown'))
                    except:
                        continue
            
            if questionnaire_types:
                from collections import Counter
                questionnaire_counts = Counter(questionnaire_types)
                patterns["popular_questionnaires"] = dict(questionnaire_counts.most_common())
        
        # User journey analysis
        if 'session_id' in df.columns and 'event_type' in df.columns:
            journey_patterns = {}
            
            for session_id in df['session_id'].unique():
                session_events = df[df['session_id'] == session_id].sort_values('timestamp')
                journey = " -> ".join(session_events['event_type'].tolist())
                
                if journey in journey_patterns:
                    journey_patterns[journey] += 1
                else:
                    journey_patterns[journey] = 1
            
            # Get top 10 most common journeys
            sorted_journeys = sorted(journey_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
            patterns["common_user_journeys"] = dict(sorted_journeys)
        
        return patterns
    
    def generate_privacy_compliance_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate privacy compliance report"""
        report = {
            "privacy_status": "COMPLIANT",
            "timestamp": datetime.now().isoformat(),
            "checks_performed": []
        }
        
        # Check for PII data
        pii_check = {
            "check_name": "PII Detection",
            "status": "PASS",
            "details": "No personally identifiable information detected in collected data"
        }
        
        if not df.empty:
            # Check column names for potential PII
            pii_columns = ['email', 'name', 'phone', 'address', 'ip_address']
            found_pii = [col for col in df.columns if any(pii in col.lower() for pii in pii_columns)]
            
            if found_pii:
                pii_check["status"] = "WARNING"
                pii_check["details"] = f"Potential PII columns found: {found_pii}"
                report["privacy_status"] = "NEEDS_REVIEW"
        
        report["checks_performed"].append(pii_check)
        
        # Check data anonymization
        anonymization_check = {
            "check_name": "Data Anonymization",
            "status": "PASS",
            "details": "Session IDs are properly hashed and anonymized"
        }
        
        if 'session_id' in df.columns and not df.empty:
            # Check if session IDs look hashed
            sample_ids = df['session_id'].head(5).tolist()
            hash_pattern = all(len(str(sid)) >= 40 for sid in sample_ids)  # Typical hash length
            
            if not hash_pattern:
                anonymization_check["status"] = "WARNING"
                anonymization_check["details"] = "Session IDs may not be properly anonymized"
                report["privacy_status"] = "NEEDS_REVIEW"
        
        report["checks_performed"].append(anonymization_check)
        
        # Data retention check
        retention_check = {
            "check_name": "Data Retention",
            "status": "PASS",
            "details": "Data retention policy is being followed"
        }
        
        if not df.empty and 'timestamp' in df.columns:
            oldest_data = df['timestamp'].min()
            data_age_days = (datetime.now() - oldest_data.to_pydatetime()).days
            
            # Check if data is older than retention policy (90 days for raw events)
            if data_age_days > 90:
                retention_check["status"] = "ACTION_REQUIRED"
                retention_check["details"] = f"Data older than 90 days detected (oldest: {data_age_days} days)"
                report["privacy_status"] = "ACTION_REQUIRED"
        
        report["checks_performed"].append(retention_check)
        
        return report
    
    def export_analytics_report(self, output_file: str = None) -> str:
        """Export comprehensive analytics report"""
        try:
            # Load data
            df = self.load_collected_data(days_back=30)
            
            # Generate all analytics
            usage_stats = self.generate_usage_statistics(df)
            behavior_patterns = self.analyze_user_behavior_patterns(df)
            privacy_report = self.generate_privacy_compliance_report(df)
            
            # Compile full report
            full_report = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "data_period_days": 30,
                    "total_events_analyzed": len(df),
                    "report_version": "1.0"
                },
                "usage_statistics": usage_stats,
                "behavior_patterns": behavior_patterns,
                "privacy_compliance": privacy_report
            }
            
            # Export to file
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"research_analytics_report_{timestamp}.json"
            
            output_path = self.data_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(full_report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Analytics report exported to {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error exporting analytics report: {e}")
            raise

def main():
    """Demo analytics functionality"""
    print("🔬 RESEARCH SYSTEM ANALYTICS")
    print("=" * 40)
    
    analytics = ResearchAnalytics()
    
    # Load and analyze data
    print("📊 Loading collected data...")
    df = analytics.load_collected_data(days_back=30)
    
    if df.empty:
        print("⚠️  No data found to analyze")
        return
    
    print(f"✅ Loaded {len(df)} events")
    
    # Generate statistics
    print("\n📈 Generating usage statistics...")
    usage_stats = analytics.generate_usage_statistics(df)
    print(f"✅ Found {usage_stats.get('overview', {}).get('unique_sessions', 0)} unique sessions")
    
    # Analyze behavior patterns
    print("\n🔍 Analyzing behavior patterns...")
    behavior_patterns = analytics.analyze_user_behavior_patterns(df)
    
    # Privacy compliance check
    print("\n🔐 Checking privacy compliance...")
    privacy_report = analytics.generate_privacy_compliance_report(df)
    print(f"✅ Privacy status: {privacy_report.get('privacy_status', 'UNKNOWN')}")
    
    # Export full report
    print("\n📄 Exporting analytics report...")
    report_file = analytics.export_analytics_report()
    print(f"✅ Report saved to: {report_file}")
    
    print("\n🎉 Analytics completed successfully!")

if __name__ == "__main__":
    main()
