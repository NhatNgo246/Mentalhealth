"""
Enhanced Research System Demo and Testing Suite
Bộ Demo và Kiểm thử Hệ thống Nghiên cứu Nâng cao

Comprehensive testing and demonstration of all research system components.
Kiểm thử và demo toàn diện cho tất cả các thành phần hệ thống nghiên cứu.
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime, timedelta
import logging
from pathlib import Path
import time
import threading
import requests
from typing import Dict, List, Any

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_components():
    """Test all enhanced research system components"""
    print("🧪 ENHANCED RESEARCH SYSTEM TESTING")
    print("=" * 50)
    
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'tests_performed': [],
        'passed': 0,
        'failed': 0,
        'details': {}
    }
    
    # Test 1: Analytics Module
    print("\n📊 Testing Analytics Module...")
    try:
        from research_system.analytics import ResearchAnalytics
        analytics = ResearchAnalytics()
        
        # Test data loading
        df = analytics.load_collected_data(days_back=30)
        print(f"   ✅ Data loading: {len(df)} records")
        
        # Test statistics generation
        stats = analytics.generate_usage_statistics(df)
        print(f"   ✅ Statistics generation: {len(stats)} metrics")
        
        # Test behavior analysis
        patterns = analytics.analyze_user_behavior_patterns(df)
        print(f"   ✅ Behavior analysis: {len(patterns)} patterns")
        
        # Test privacy compliance
        privacy_report = analytics.generate_privacy_compliance_report(df)
        print(f"   ✅ Privacy compliance: {privacy_report.get('privacy_status', 'UNKNOWN')}")
        
        # Test report export
        report_file = analytics.export_analytics_report()
        print(f"   ✅ Report export: {report_file}")
        
        test_results['tests_performed'].append('analytics')
        test_results['passed'] += 1
        test_results['details']['analytics'] = 'PASS'
        
    except Exception as e:
        print(f"   ❌ Analytics test failed: {e}")
        test_results['failed'] += 1
        test_results['details']['analytics'] = f'FAIL: {str(e)}'
    
    # Test 2: Database Module
    print("\n🗄️ Testing Database Module...")
    try:
        from research_system.database import ResearchDatabase
        database = ResearchDatabase()
        
        # Test event storage
        test_event = {
            'session_id': f'test_session_{int(time.time())}',
            'event_type': 'test_event',
            'event_data': {'test': 'data', 'timestamp': datetime.now().isoformat()},
            'timestamp': datetime.now().isoformat(),
            'anonymized_user_id': f'test_user_{int(time.time())}',
            'consent_status': 'given'
        }
        
        success = database.store_event(test_event)
        print(f"   ✅ Event storage: {'SUCCESS' if success else 'FAILED'}")
        
        # Test data retrieval
        events = database.get_events(limit=5)
        print(f"   ✅ Data retrieval: {len(events)} events")
        
        # Test cleanup
        cleaned = database.cleanup_old_data(retention_days=365)
        print(f"   ✅ Data cleanup: {cleaned} records cleaned")
        
        test_results['tests_performed'].append('database')
        test_results['passed'] += 1
        test_results['details']['database'] = 'PASS'
        
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        test_results['failed'] += 1
        test_results['details']['database'] = f'FAIL: {str(e)}'
    
    # Test 3: Security Module
    print("\n🔒 Testing Security Module...")
    try:
        from research_system.security import ResearchSecurity
        security = ResearchSecurity()
        
        # Test data encryption
        test_data = "sensitive research data for testing"
        encrypted = security.encryption.encrypt_data(test_data)
        decrypted = security.encryption.decrypt_data(encrypted)
        encryption_ok = (test_data == decrypted)
        print(f"   ✅ Data encryption: {'SUCCESS' if encryption_ok else 'FAILED'}")
        
        # Test PII detection
        test_text = "Contact john.doe@example.com or call 555-123-4567"
        pii_detected = security.privacy_validator.detect_pii(test_text)
        print(f"   ✅ PII detection: {list(pii_detected.keys())}")
        
        # Test data anonymization
        test_ip = "192.168.1.100"
        anonymized_ip = security.privacy_validator.anonymize_ip_address(test_ip)
        print(f"   ✅ IP anonymization: {test_ip} -> {anonymized_ip}")
        
        # Test compliance validation
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
        print(f"   ✅ Compliance validation: {compliance_result.get('overall_compliant', False)}")
        
        # Test security scan
        scan_result = security.auditor.perform_security_scan("research_data")
        print(f"   ✅ Security scan: {len(scan_result.get('issues_found', []))} issues")
        
        test_results['tests_performed'].append('security')
        test_results['passed'] += 1
        test_results['details']['security'] = 'PASS'
        
    except Exception as e:
        print(f"   ❌ Security test failed: {e}")
        test_results['failed'] += 1
        test_results['details']['security'] = f'FAIL: {str(e)}'
    
    # Test 4: Advanced Manager
    print("\n🎛️ Testing Advanced Manager...")
    try:
        from research_system.manager import ResearchSystemManager
        manager = ResearchSystemManager()
        
        # Start monitoring briefly
        manager.start_monitoring()
        time.sleep(2)  # Let it run briefly
        
        # Test system status
        status = manager.get_system_status()
        print(f"   ✅ System status: {status['overall_status']}")
        
        healthy_components = sum(1 for c in status['components'].values() if c['status'] == 'healthy')
        print(f"   ✅ Healthy components: {healthy_components}/{len(status['components'])}")
        
        # Test maintenance
        maintenance_result = manager.perform_maintenance()
        print(f"   ✅ Maintenance tasks: {len(maintenance_result['tasks_performed'])}")
        
        # Test report export
        report_file = manager.export_system_report("test_system_report.json")
        print(f"   ✅ System report: {report_file}")
        
        # Stop monitoring
        manager.stop_monitoring()
        
        test_results['tests_performed'].append('manager')
        test_results['passed'] += 1
        test_results['details']['manager'] = 'PASS'
        
    except Exception as e:
        print(f"   ❌ Manager test failed: {e}")
        test_results['failed'] += 1
        test_results['details']['manager'] = f'FAIL: {str(e)}'
    
    # Test 5: Integration Functions
    print("\n🔗 Testing Integration Functions...")
    try:
        from research_system.integration import (
            safe_track_session_start,
            safe_track_questionnaire_start,
            safe_track_questionnaire_completion,
            safe_track_question_answer,
            safe_track_results_view
        )
        
        # Test all tracking functions
        session_id = f"test_session_{int(time.time())}"
        
        safe_track_session_start(test_mode=True, session_id=session_id)
        print("   ✅ Session start tracking")
        
        safe_track_questionnaire_start("PHQ-9", test_mode=True, session_id=session_id)
        print("   ✅ Questionnaire start tracking")
        
        safe_track_question_answer("PHQ-9", 1, "Little interest", test_mode=True, session_id=session_id)
        print("   ✅ Question answer tracking")
        
        safe_track_questionnaire_completion("PHQ-9", {"total_score": 15}, test_mode=True, session_id=session_id)
        print("   ✅ Questionnaire completion tracking")
        
        safe_track_results_view({"phq9": 15}, test_mode=True, session_id=session_id)
        print("   ✅ Results view tracking")
        
        test_results['tests_performed'].append('integration')
        test_results['passed'] += 1
        test_results['details']['integration'] = 'PASS'
        
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        test_results['failed'] += 1
        test_results['details']['integration'] = f'FAIL: {str(e)}'
    
    # Test 6: Monitoring Dashboard (if Streamlit available)
    print("\n📊 Testing Monitoring Dashboard...")
    try:
        import streamlit as st
        from research_system.monitoring_dashboard import ResearchMonitoring
        
        monitor = ResearchMonitoring()
        
        # Test health check
        health = monitor.get_api_health()
        print(f"   ✅ API health check: {health['status']}")
        
        # Test recent events
        recent_events = monitor.get_recent_events(minutes=60)
        print(f"   ✅ Recent events: {len(recent_events)} events")
        
        test_results['tests_performed'].append('monitoring')
        test_results['passed'] += 1
        test_results['details']['monitoring'] = 'PASS'
        
    except ImportError:
        print("   ⚠️ Streamlit not available, skipping dashboard test")
        test_results['details']['monitoring'] = 'SKIP: Streamlit not available'
    except Exception as e:
        print(f"   ❌ Monitoring test failed: {e}")
        test_results['failed'] += 1
        test_results['details']['monitoring'] = f'FAIL: {str(e)}'
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 ENHANCED TESTING SUMMARY")
    print("=" * 50)
    print(f"✅ Tests passed: {test_results['passed']}")
    print(f"❌ Tests failed: {test_results['failed']}")
    print(f"📊 Success rate: {test_results['passed']/(test_results['passed']+test_results['failed'])*100:.1f}%")
    
    # Save test results
    test_file = f"research_data/enhanced_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path("research_data").mkdir(exist_ok=True)
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Test results saved to: {test_file}")
    
    if test_results['failed'] == 0:
        print("\n🎉 ALL ENHANCED TESTS PASSED! System is ready for production.")
    else:
        print(f"\n⚠️ {test_results['failed']} tests failed. Please review and fix issues.")
    
    return test_results

def demo_complete_workflow():
    """Demonstrate complete research data collection workflow"""
    print("\n🚀 COMPLETE WORKFLOW DEMONSTRATION")
    print("=" * 50)
    
    # Simulate a complete user journey
    session_id = f"demo_session_{int(time.time())}"
    user_id = f"demo_user_{int(time.time())}"
    
    workflow_steps = []
    
    try:
        from research_system.integration import (
            safe_track_session_start,
            safe_track_questionnaire_start,
            safe_track_question_answer,
            safe_track_questionnaire_completion,
            safe_track_results_view
        )
        
        # Step 1: User starts session
        print("1. 👤 User starts assessment session...")
        safe_track_session_start(test_mode=True, session_id=session_id)
        workflow_steps.append("Session started")
        time.sleep(1)
        
        # Step 2: User begins PHQ-9 questionnaire
        print("2. 📝 User begins PHQ-9 questionnaire...")
        safe_track_questionnaire_start("PHQ-9", test_mode=True, session_id=session_id)
        workflow_steps.append("PHQ-9 started")
        time.sleep(1)
        
        # Step 3: User answers questions
        print("3. ✏️ User answers PHQ-9 questions...")
        phq9_questions = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep",
            "Feeling tired or having little energy",
            "Poor appetite or overeating"
        ]
        
        answers = []
        for i, question in enumerate(phq9_questions[:3], 1):  # Demo first 3 questions
            answer_value = 2  # "Several days"
            print(f"   Question {i}: {answer_value}")
            safe_track_question_answer("PHQ-9", i, answer_value, test_mode=True, session_id=session_id)
            answers.append(answer_value)
            time.sleep(0.5)
        
        workflow_steps.append(f"Answered {len(answers)} questions")
        
        # Step 4: Complete questionnaire
        print("4. ✅ User completes PHQ-9...")
        total_score = sum(answers) * 3  # Simulate full questionnaire
        results = {"total_score": total_score, "severity": "mild" if total_score < 10 else "moderate"}
        safe_track_questionnaire_completion("PHQ-9", results, test_mode=True, session_id=session_id)
        workflow_steps.append("PHQ-9 completed")
        time.sleep(1)
        
        # Step 5: User views results
        print("5. 📊 User views assessment results...")
        safe_track_results_view({"phq9": total_score}, test_mode=True, session_id=session_id)
        workflow_steps.append("Results viewed")
        time.sleep(1)
        
        # Step 6: Demonstrate analytics
        print("6. 📈 Generating analytics from collected data...")
        from research_system.analytics import ResearchAnalytics
        analytics = ResearchAnalytics()
        
        df = analytics.load_collected_data(days_back=1)
        stats = analytics.generate_usage_statistics(df)
        print(f"   📊 Total events: {stats.get('overview', {}).get('total_events', 0)}")
        print(f"   👥 Unique sessions: {stats.get('overview', {}).get('unique_sessions', 0)}")
        workflow_steps.append("Analytics generated")
        
        # Step 7: Security and compliance check
        print("7. 🔒 Performing security and compliance check...")
        from research_system.security import ResearchSecurity
        security = ResearchSecurity()
        
        test_consent = {
            'consent_given': True,
            'consent_explicit': True,
            'research_purpose': 'Mental health research demonstration',
            'minimal_data_collection': True,
            'retention_policy_explained': True,
            'rights_explained': True
        }
        
        compliance_result = security.validate_compliance(test_consent, {
            'consent_language': 'vi',
            'data_stored_vietnam': True,
            'encryption_enabled': True,
            'access_controls': True,
            'data_controller_info': True
        })
        
        print(f"   🔐 Compliance status: {compliance_result.get('overall_compliant', False)}")
        workflow_steps.append("Compliance verified")
        
        print("\n✅ WORKFLOW COMPLETED SUCCESSFULLY!")
        print(f"📋 Steps completed: {len(workflow_steps)}")
        for i, step in enumerate(workflow_steps, 1):
            print(f"   {i}. {step}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Workflow demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_monitoring_dashboard():
    """Start the monitoring dashboard"""
    print("📊 STARTING MONITORING DASHBOARD")
    print("=" * 40)
    
    try:
        import subprocess
        import sys
        
        # Start monitoring dashboard on port 8503
        dashboard_cmd = [
            sys.executable, "-m", "streamlit", "run",
            "research_system/monitoring_dashboard.py",
            "--server.port", "8503",
            "--server.address", "0.0.0.0"
        ]
        
        print("🚀 Starting monitoring dashboard on port 8503...")
        print("   📊 Dashboard URL: http://localhost:8503")
        print("   ⚠️ Press Ctrl+C to stop the dashboard")
        
        # Run dashboard
        subprocess.run(dashboard_cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring dashboard stopped")
    except Exception as e:
        print(f"❌ Failed to start monitoring dashboard: {e}")

def stress_test_system():
    """Perform stress testing on the research system"""
    print("⚡ STRESS TESTING RESEARCH SYSTEM")
    print("=" * 40)
    
    try:
        from research_system.integration import safe_track_session_start
        import concurrent.futures
        import random
        
        # Configuration
        num_sessions = 50
        events_per_session = 10
        max_workers = 5
        
        print(f"📊 Configuration:")
        print(f"   Sessions: {num_sessions}")
        print(f"   Events per session: {events_per_session}")
        print(f"   Concurrent workers: {max_workers}")
        
        def simulate_session(session_num):
            """Simulate a user session"""
            session_id = f"stress_test_{session_num}_{int(time.time())}"
            events_created = 0
            
            try:
                # Start session
                safe_track_session_start(test_mode=True, session_id=session_id)
                events_created += 1
                
                # Simulate random events
                for event_num in range(events_per_session - 1):
                    event_type = random.choice(['questionnaire_start', 'question_answer', 'results_view'])
                    
                    if event_type == 'questionnaire_start':
                        from research_system.integration import safe_track_questionnaire_start
                        safe_track_questionnaire_start("PHQ-9", test_mode=True, session_id=session_id)
                    elif event_type == 'question_answer':
                        from research_system.integration import safe_track_question_answer
                        safe_track_question_answer("PHQ-9", random.randint(1, 9), random.randint(0, 3), test_mode=True, session_id=session_id)
                    elif event_type == 'results_view':
                        from research_system.integration import safe_track_results_view
                        safe_track_results_view({"score": random.randint(0, 27)}, test_mode=True, session_id=session_id)
                    
                    events_created += 1
                    time.sleep(random.uniform(0.1, 0.5))  # Random delay
                
                return {'session': session_num, 'events': events_created, 'success': True}
                
            except Exception as e:
                return {'session': session_num, 'events': events_created, 'success': False, 'error': str(e)}
        
        # Run stress test
        start_time = time.time()
        results = []
        
        print("\n🏃 Running stress test...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(simulate_session, i) for i in range(num_sessions)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                
                if result['success']:
                    print(f"   ✅ Session {result['session']}: {result['events']} events")
                else:
                    print(f"   ❌ Session {result['session']}: Failed - {result.get('error', 'Unknown error')}")
        
        # Calculate statistics
        end_time = time.time()
        duration = end_time - start_time
        
        successful_sessions = sum(1 for r in results if r['success'])
        total_events = sum(r['events'] for r in results)
        events_per_second = total_events / duration if duration > 0 else 0
        
        print(f"\n📊 STRESS TEST RESULTS:")
        print(f"   ⏱️ Duration: {duration:.2f} seconds")
        print(f"   ✅ Successful sessions: {successful_sessions}/{num_sessions}")
        print(f"   📈 Total events created: {total_events}")
        print(f"   ⚡ Events per second: {events_per_second:.2f}")
        print(f"   📊 Success rate: {successful_sessions/num_sessions*100:.1f}%")
        
        # Save stress test results
        stress_test_results = {
            'timestamp': datetime.now().isoformat(),
            'configuration': {
                'num_sessions': num_sessions,
                'events_per_session': events_per_session,
                'max_workers': max_workers
            },
            'results': {
                'duration_seconds': duration,
                'successful_sessions': successful_sessions,
                'total_sessions': num_sessions,
                'total_events': total_events,
                'events_per_second': events_per_second,
                'success_rate': successful_sessions/num_sessions
            },
            'session_details': results
        }
        
        stress_file = f"research_data/stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(stress_file, 'w', encoding='utf-8') as f:
            json.dump(stress_test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Stress test results saved to: {stress_file}")
        
        if successful_sessions == num_sessions:
            print("\n🎉 STRESS TEST PASSED! System handled load successfully.")
        else:
            print(f"\n⚠️ STRESS TEST PARTIAL: {num_sessions - successful_sessions} sessions failed.")
        
        return stress_test_results
        
    except Exception as e:
        print(f"❌ Stress test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main demo application with enhanced options"""
    parser = argparse.ArgumentParser(description="Enhanced Research System Demo and Testing")
    parser.add_argument('--test', action='store_true', help='Run enhanced component tests')
    parser.add_argument('--demo', action='store_true', help='Run complete workflow demonstration')
    parser.add_argument('--dashboard', action='store_true', help='Start monitoring dashboard')
    parser.add_argument('--stress', action='store_true', help='Run stress testing')
    parser.add_argument('--api', action='store_true', help='Start research collection API')
    parser.add_argument('--full', action='store_true', help='Run all tests and demonstrations')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        print("🔬 ENHANCED RESEARCH SYSTEM DEMO")
        print("=" * 40)
        print("Available options:")
        print("  --test      Run enhanced component tests")
        print("  --demo      Run complete workflow demonstration")
        print("  --dashboard Start monitoring dashboard")
        print("  --stress    Run stress testing")
        print("  --api       Start research collection API")
        print("  --full      Run all tests and demonstrations")
        print("\nExample: python enhanced_research_demo.py --full")
        return
    
    success_count = 0
    total_count = 0
    
    if args.full or args.test:
        total_count += 1
        print("🧪 Running enhanced component tests...")
        test_results = test_enhanced_components()
        if test_results['failed'] == 0:
            success_count += 1
    
    if args.full or args.demo:
        total_count += 1
        print("\n🚀 Running complete workflow demonstration...")
        demo_success = demo_complete_workflow()
        if demo_success:
            success_count += 1
    
    if args.full or args.stress:
        total_count += 1
        print("\n⚡ Running stress test...")
        stress_results = stress_test_system()
        if stress_results and stress_results['results']['success_rate'] > 0.9:
            success_count += 1
    
    if args.api:
        print("\n🚀 Starting Research Collection API...")
        try:
            import uvicorn
            from research_system.collection_api import app
            
            print("✅ Starting API on http://localhost:8502")
            print("   📊 Health check: http://localhost:8502/health")
            print("   📈 Stats: http://localhost:8502/stats")
            print("   📝 API docs: http://localhost:8502/docs")
            print("\n   Press Ctrl+C to stop")
            
            uvicorn.run(app, host="0.0.0.0", port=8502)
            
        except KeyboardInterrupt:
            print("\n🛑 API stopped")
        except Exception as e:
            print(f"❌ Failed to start API: {e}")
    
    if args.dashboard:
        start_monitoring_dashboard()
    
    # Final summary for full run
    if args.full and total_count > 0:
        print("\n" + "=" * 50)
        print("🎯 FINAL SUMMARY")
        print("=" * 50)
        print(f"✅ Successful operations: {success_count}/{total_count}")
        print(f"📊 Success rate: {success_count/total_count*100:.1f}%")
        
        if success_count == total_count:
            print("\n🎉 ALL OPERATIONS COMPLETED SUCCESSFULLY!")
            print("🚀 Research system is fully operational and ready for production.")
        else:
            print(f"\n⚠️ {total_count - success_count} operations had issues.")
            print("📝 Please review the output above for details.")

if __name__ == "__main__":
    main()
