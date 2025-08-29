#!/usr/bin/env python3
"""
📊 SOULFRIEND QUALITY DASHBOARD
==============================
Real-time quality monitoring dashboard

Usage: python3 quality_dashboard.py
"""

import os
import json
from datetime import datetime

def display_quality_dashboard():
    """Display comprehensive quality dashboard"""
    
    print("📊 SOULFRIEND QUALITY DASHBOARD")
    print("=" * 50)
    print(f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # System Status
    print("🔥 SYSTEM STATUS")
    print("-" * 20)
    
    critical_files = {
        "Main App": "/workspaces/Mentalhealth/SOULFRIEND.py",
        "UI Core": "/workspaces/Mentalhealth/components/ui.py", 
        "UI Advanced": "/workspaces/Mentalhealth/components/ui_advanced.py",
        "Questionnaires": "/workspaces/Mentalhealth/components/questionnaires.py",
        "Scoring": "/workspaces/Mentalhealth/components/scoring.py",
        "DASS-21 Data": "/workspaces/Mentalhealth/data/dass21_vi.json",
        "Requirements": "/workspaces/Mentalhealth/requirements.txt"
    }
    
    all_present = True
    for name, path in critical_files.items():
        if os.path.exists(path):
            print(f"🟢 {name}")
        else:
            print(f"🔴 {name} - MISSING")
            all_present = False
            
    status = "🟢 ALL SYSTEMS OPERATIONAL" if all_present else "🔴 CRITICAL FILES MISSING"
    print(f"\nStatus: {status}")
    
    # Quality Metrics
    print(f"\n📈 QUALITY METRICS")
    print("-" * 20)
    
    try:
        app_size = os.path.getsize("/workspaces/Mentalhealth/SOULFRIEND.py") / 1024
        print(f"📁 App Size: {app_size:.1f}KB")
        
        with open("/workspaces/Mentalhealth/SOULFRIEND.py", 'r') as f:
            lines = len(f.readlines())
        print(f"📝 Code Lines: {lines}")
        
        # Component count
        components_dir = "/workspaces/Mentalhealth/components"
        if os.path.exists(components_dir):
            components = len([f for f in os.listdir(components_dir) if f.endswith('.py')])
            print(f"🧩 Components: {components}")
            
        # Data files
        data_dir = "/workspaces/Mentalhealth/data"
        if os.path.exists(data_dir):
            data_files = len([f for f in os.listdir(data_dir) if f.endswith('.json')])
            print(f"📊 Data Files: {data_files}")
            
    except Exception as e:
        print(f"⚠️ Error reading metrics: {e}")
    
    # Quick Health Check
    print(f"\n🏥 HEALTH CHECK")
    print("-" * 15)
    
    health_checks = []
    
    # Check if main app exists and has content
    if os.path.exists("/workspaces/Mentalhealth/SOULFRIEND.py"):
        try:
            with open("/workspaces/Mentalhealth/SOULFRIEND.py", 'r') as f:
                content = f.read()
                if "streamlit" in content:
                    health_checks.append("✅ Streamlit Integration")
                if "SmartUIExperience" in content:
                    health_checks.append("✅ Smart UI Experience")
                if "dass21" in content.lower():
                    health_checks.append("✅ DASS-21 Integration")
                if "logging" in content:
                    health_checks.append("✅ Logging System")
        except:
            health_checks.append("❌ Main App Error")
    else:
        health_checks.append("❌ Main App Missing")
        
    for check in health_checks:
        print(check)
        
    # Test Results Summary
    print(f"\n🧪 LATEST TEST RESULTS")
    print("-" * 25)
    
    # Look for latest QA report
    test_dir = "/workspaces/Mentalhealth/tests"
    latest_report = None
    
    if os.path.exists(test_dir):
        reports = [f for f in os.listdir(test_dir) if f.startswith("QA_REPORT_")]
        if reports:
            latest_report = max(reports)
            print(f"📄 Latest Report: {latest_report}")
            
            try:
                with open(f"{test_dir}/{latest_report}", 'r') as f:
                    content = f.read()
                    if "Success Rate:" in content:
                        for line in content.split('\n'):
                            if "Success Rate:" in line:
                                print(f"📊 {line}")
                                break
            except:
                print("⚠️ Error reading report")
        else:
            print("📄 No test reports found")
    
    # Actions Available
    print(f"\n🎯 AVAILABLE ACTIONS")
    print("-" * 20)
    print("1. Run Full Pipeline: python3 tests/test_runner.py")
    print("2. Functional Test: python3 tests/tester.py")
    print("3. QA Analysis: python3 tests/qa.py")
    print("4. QC Validation: python3 tests/qc.py")
    print("5. Launch App: ./launch_soulfriend.sh")
    
    # Final Status
    print(f"\n🎉 DEPLOYMENT READINESS")
    print("-" * 25)
    
    readiness_score = 0
    max_score = 5
    
    if all_present:
        readiness_score += 1
        print("✅ All files present")
    else:
        print("❌ Missing files")
        
    if len(health_checks) >= 4:
        readiness_score += 1
        print("✅ Health checks passed")
    else:
        print("❌ Health checks failed")
        
    if latest_report:
        readiness_score += 1
        print("✅ Tests completed")
    else:
        print("⚠️ No test results")
        
    if app_size < 50:  # < 50KB is good
        readiness_score += 1
        print("✅ Optimized size")
    else:
        print("⚠️ Large file size")
        
    if lines < 500:  # < 500 lines is manageable
        readiness_score += 1
        print("✅ Maintainable code")
    else:
        print("⚠️ Complex codebase")
        
    readiness_percentage = (readiness_score / max_score) * 100
    
    if readiness_percentage >= 80:
        readiness_status = "🟢 READY FOR DEPLOYMENT"
    elif readiness_percentage >= 60:
        readiness_status = "🟡 NEEDS MINOR FIXES"
    else:
        readiness_status = "🔴 NEEDS MAJOR WORK"
        
    print(f"\n🏆 READINESS: {readiness_percentage:.0f}% - {readiness_status}")
    
    print("\n" + "=" * 50)
    print("💡 TIP: Run 'python3 tests/test_runner.py' for complete analysis")
    print("=" * 50)

if __name__ == "__main__":
    display_quality_dashboard()
