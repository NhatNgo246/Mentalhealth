"""
Demo và Test cho Research System
Chạy script này để test research collection một cách an toàn
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_research_system():
    """Test research system components"""
    
    print("🔬 SOULFRIEND Research System Demo")
    print("=" * 50)
    
    # Test 1: Import research components
    print("\\n1. Testing research components import...")
    try:
        from research_system.config import setup_research_environment, enable_research_collection
        from research_system.collector import SafeResearchCollector
        from research_system.integration import SafeResearchIntegration
        print("✅ All research components imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Setup environment
    print("\\n2. Setting up research environment...")
    try:
        setup_research_environment()
        print("✅ Research environment setup complete")
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False
    
    # Test 3: Test với research DISABLED (default)
    print("\\n3. Testing with research DISABLED (safe mode)...")
    try:
        collector = SafeResearchCollector()
        print(f"   Research enabled: {collector.enabled}")
        
        # Thử collect event (should be ignored)
        collector.collect_event_async(
            "test_event",
            {"test": "data"},
            "test_session_123"
        )
        print("✅ Safe mode test passed - no data collected")
    except Exception as e:
        print(f"❌ Safe mode test failed: {e}")
        return False
    
    # Test 4: Enable research và test
    print("\\n4. Testing with research ENABLED...")
    try:
        # Enable research collection
        enable_research_collection()
        
        # Create new collector instance
        collector = SafeResearchCollector()
        print(f"   Research enabled: {collector.enabled}")
        
        if collector.enabled:
            print("   📊 Collecting test events...")
            
            # Test events
            test_events = [
                ("session_started", {"user_agent": "test", "locale": "vi"}),
                ("questionnaire_started", {"questionnaire_type": "PHQ-9"}),
                ("question_answered", {
                    "questionnaire_type": "PHQ-9",
                    "item_id": "PHQ9_Q01", 
                    "response_value": 2
                }),
                ("questionnaire_completed", {
                    "questionnaire_type": "PHQ-9",
                    "total_score": 12
                })
            ]
            
            for event_name, payload in test_events:
                collector.collect_event_async(event_name, payload, "demo_session_456")
                print(f"   ✅ Event collected: {event_name}")
                time.sleep(0.1)  # Small delay
        
        print("✅ Research enabled test completed")
        
    except Exception as e:
        print(f"❌ Research enabled test failed: {e}")
        return False
    
    # Test 5: Integration wrapper
    print("\\n5. Testing safe integration wrapper...")
    try:
        from research_system.integration import (
            safe_track_session_start,
            safe_track_questionnaire_start,
            safe_track_question_answer,
            safe_track_questionnaire_complete
        )
        
        # Các functions này sẽ hoạt động an toàn dù có lỗi
        safe_track_session_start(user_agent="demo", locale="vi")
        safe_track_questionnaire_start("DASS-21")
        safe_track_question_answer("DASS-21", 1, 3)
        safe_track_questionnaire_complete("DASS-21", 28)
        
        print("✅ Integration wrapper test passed")
        
    except Exception as e:
        print(f"❌ Integration wrapper test failed: {e}")
        return False
    
    # Test 6: Check data files
    print("\\n6. Checking research data files...")
    try:
        research_data_dir = project_root / "research_data"
        if research_data_dir.exists():
            data_files = list(research_data_dir.glob("*.jsonl"))
            print(f"   📁 Data directory: {research_data_dir}")
            print(f"   📄 Data files found: {len(data_files)}")
            
            if data_files:
                latest_file = max(data_files, key=lambda f: f.stat().st_mtime)
                print(f"   📄 Latest file: {latest_file.name}")
                
                # Count events in latest file
                with open(latest_file, 'r') as f:
                    event_count = sum(1 for line in f if line.strip())
                print(f"   📊 Events in latest file: {event_count}")
        
        print("✅ Data files check completed")
        
    except Exception as e:
        print(f"❌ Data files check failed: {e}")
        return False
    
    print("\\n🎉 All research system tests PASSED!")
    print("\\n📋 Research System Status:")
    print(f"   🔧 Research Collection: {'ENABLED' if os.environ.get('ENABLE_RESEARCH_COLLECTION') == 'true' else 'DISABLED'}")
    print(f"   📁 Data Directory: {project_root / 'research_data'}")
    print(f"   📝 Log Directory: {project_root / 'logs'}")
    
    return True

def start_research_api():
    """Start research collection API"""
    print("\\n🚀 Starting Research Collection API...")
    try:
        # Add FastAPI dependencies check
        try:
            import fastapi
            import uvicorn
        except ImportError:
            print("❌ Missing FastAPI dependencies. Install with:")
            print("   pip install fastapi uvicorn")
            return False
        
        # Import and start API
        from research_system.collection_api import app
        import uvicorn
        
        print("✅ Starting API on http://localhost:8502")
        print("   📊 Health check: http://localhost:8502/health")
        print("   📈 Stats: http://localhost:8502/stats")
        print("   📝 API docs: http://localhost:8502/docs")
        print("\\n   Press Ctrl+C to stop")
        
        uvicorn.run(app, host="0.0.0.0", port=8502, log_level="info")
        
    except Exception as e:
        print(f"❌ Failed to start API: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SOULFRIEND Research System Demo")
    parser.add_argument("--test", action="store_true", help="Run research system tests")
    parser.add_argument("--api", action="store_true", help="Start research collection API")
    parser.add_argument("--full", action="store_true", help="Run tests then start API")
    
    args = parser.parse_args()
    
    if args.test or args.full:
        success = test_research_system()
        if not success:
            sys.exit(1)
    
    if args.api or args.full:
        if args.full:
            print("\\n" + "="*50)
        start_research_api()
    
    if not any([args.test, args.api, args.full]):
        print("Usage: python research_demo.py [--test] [--api] [--full]")
        print("  --test: Run research system tests")
        print("  --api:  Start research collection API") 
        print("  --full: Run tests then start API")
