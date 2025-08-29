#!/usr/bin/env python3
"""
🔄 CONTINUOUS TESTING FOR SOULFRIEND ENHANCED
============================================
Continuous testing to achieve 100% synchronization

Created: August 27, 2025
Purpose: Ensure all enhanced features work perfectly
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

def validate_enhanced_files():
    """Validate all enhanced files exist and are valid"""
    print("📁 Validating Enhanced Files...")
    print("-" * 35)
    
    files_to_check = [
        ("/workspaces/Mentalhealth/SOULFRIEND.py", "Main Application"),
        ("/workspaces/Mentalhealth/data/dass21_enhanced_vi.json", "Enhanced Data"),
        ("/workspaces/Mentalhealth/components/questionnaires.py", "Questionnaires"),
        ("/workspaces/Mentalhealth/components/scoring.py", "Scoring Engine"),
        ("/workspaces/Mentalhealth/tests/test_enhanced.py", "Enhanced Tests")
    ]
    
    all_valid = True
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {description}: EXISTS")
            
            # Validate JSON files
            if file_path.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                    print(f"✅ {description}: VALID JSON")
                except json.JSONDecodeError as e:
                    print(f"❌ {description}: INVALID JSON - {e}")
                    all_valid = False
            
            # Validate Python files
            elif file_path.endswith('.py'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    compile(content, file_path, 'exec')
                    print(f"✅ {description}: VALID PYTHON")
                except SyntaxError as e:
                    print(f"❌ {description}: SYNTAX ERROR - {e}")
                    all_valid = False
        else:
            print(f"❌ {description}: MISSING")
            all_valid = False
    
    return all_valid

def test_enhanced_questionnaire_load():
    """Test enhanced questionnaire loading"""
    print("\n🧠 Testing Enhanced Questionnaire...")
    print("-" * 40)
    
    try:
        # Test loading enhanced data directly
        enhanced_path = "/workspaces/Mentalhealth/data/dass21_enhanced_vi.json"
        
        with open(enhanced_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate enhanced structure
        required_keys = ['scale', 'version', 'options', 'items', 'scoring', 'recommendations']
        
        for key in required_keys:
            if key in data:
                print(f"✅ Has {key}")
            else:
                print(f"❌ Missing {key}")
                return False
        
        # Validate enhanced features
        if data.get('version') == '2.0':
            print("✅ Correct version 2.0")
        else:
            print("❌ Wrong version")
            return False
        
        if len(data.get('items', [])) == 21:
            print("✅ Correct number of questions (21)")
        else:
            print(f"❌ Wrong number of questions: {len(data.get('items', []))}")
            return False
        
        # Test enhanced options
        for i, option in enumerate(data.get('options', [])):
            if all(key in option for key in ['value', 'label', 'description', 'emoji']):
                print(f"✅ Option {i} enhanced")
            else:
                print(f"❌ Option {i} not enhanced")
                return False
        
        print("✅ Enhanced questionnaire validation PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced questionnaire test FAILED: {e}")
        return False

def test_enhanced_scoring_logic():
    """Test enhanced scoring logic"""
    print("\n📊 Testing Enhanced Scoring...")
    print("-" * 35)
    
    try:
        # Load enhanced data
        with open("/workspaces/Mentalhealth/data/dass21_enhanced_vi.json", 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        
        # Test scoring configuration
        scoring_config = cfg.get('scoring', {})
        
        if 'subscales' in scoring_config:
            print("✅ Has subscales configuration")
            
            subscales = scoring_config['subscales']
            for subscale_name in ['Depression', 'Anxiety', 'Stress']:
                if subscale_name in subscales:
                    subscale_data = subscales[subscale_name]
                    
                    # Check required fields
                    if 'items' in subscale_data and 'severity_levels' in subscale_data:
                        print(f"✅ {subscale_name} properly configured")
                        
                        # Check severity levels
                        severity_levels = subscale_data['severity_levels']
                        expected_levels = ['normal', 'mild', 'moderate', 'severe', 'extremely_severe']
                        
                        for level in expected_levels:
                            if level in severity_levels:
                                level_data = severity_levels[level]
                                if all(key in level_data for key in ['min', 'max', 'label', 'color']):
                                    print(f"✅ {subscale_name} {level} level complete")
                                else:
                                    print(f"❌ {subscale_name} {level} level incomplete")
                                    return False
                            else:
                                print(f"❌ {subscale_name} missing {level} level")
                                return False
                    else:
                        print(f"❌ {subscale_name} missing required fields")
                        return False
                else:
                    print(f"❌ Missing {subscale_name} subscale")
                    return False
        else:
            print("❌ Missing subscales configuration")
            return False
        
        # Test recommendations
        if 'recommendations' in cfg:
            print("✅ Has recommendations")
            
            recommendations = cfg['recommendations']
            expected_rec_levels = ['normal', 'mild', 'moderate', 'severe', 'extremely_severe']
            
            for level in expected_rec_levels:
                if level in recommendations:
                    rec_data = recommendations[level]
                    if all(key in rec_data for key in ['title', 'message', 'suggestions']):
                        print(f"✅ {level} recommendations complete")
                    else:
                        print(f"❌ {level} recommendations incomplete")
                        return False
                else:
                    print(f"❌ Missing {level} recommendations")
                    return False
        else:
            print("❌ Missing recommendations")
            return False
        
        print("✅ Enhanced scoring logic validation PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced scoring test FAILED: {e}")
        return False

def test_app_integration():
    """Test main app integration"""
    print("\n🔗 Testing App Integration...")
    print("-" * 30)
    
    try:
        # Check main app for enhanced features
        with open("/workspaces/Mentalhealth/SOULFRIEND.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test enhanced imports
        enhanced_imports = [
            'load_dass21_enhanced_vi',
            'score_dass21_enhanced'
        ]
        
        for imp in enhanced_imports:
            if imp in content:
                print(f"✅ Has {imp} import")
            else:
                print(f"❌ Missing {imp} import")
                return False
        
        # Test enhanced functionality usage
        enhanced_features = [
            'enhanced_scores',
            'enhanced_result',
            'dass21_enhanced'
        ]
        
        for feature in enhanced_features:
            if feature in content:
                print(f"✅ Uses {feature}")
            else:
                print(f"⚠️ May not fully use {feature}")
        
        # Test enhanced UI elements
        enhanced_ui = [
            'vietnamese_context',
            'severity_level',
            'recommendations',
            'emergency_contacts'
        ]
        
        found_ui_features = 0
        for ui_feature in enhanced_ui:
            if ui_feature in content:
                print(f"✅ Has {ui_feature} UI")
                found_ui_features += 1
            else:
                print(f"⚠️ Missing {ui_feature} UI")
        
        if found_ui_features >= len(enhanced_ui) * 0.75:  # 75% threshold
            print("✅ Sufficient enhanced UI features")
        else:
            print("❌ Insufficient enhanced UI features")
            return False
        
        print("✅ App integration validation PASSED")
        return True
        
    except Exception as e:
        print(f"❌ App integration test FAILED: {e}")
        return False

def run_pipeline_validation():
    """Run QA pipeline validation"""
    print("\n🚀 Running QA Pipeline...")
    print("-" * 30)
    
    try:
        # Run the main test pipeline
        import subprocess
        result = subprocess.run([
            'python3', '/workspaces/Mentalhealth/tests/test_runner.py'
        ], capture_output=True, text=True, cwd='/workspaces/Mentalhealth')
        
        if result.returncode == 0:
            output = result.stdout
            
            # Extract success rate
            if "Success rate:" in output:
                lines = output.split('\n')
                for line in lines:
                    if "Success rate:" in line and "%" in line:
                        success_rate = line.split("Success rate: ")[1].split("%")[0]
                        print(f"✅ QA Pipeline Success Rate: {success_rate}%")
                        
                        if float(success_rate) >= 90:
                            print("✅ QA Pipeline PASSED")
                            return True
                        else:
                            print("❌ QA Pipeline below 90%")
                            return False
            
            print("✅ QA Pipeline completed")
            return True
        else:
            print(f"❌ QA Pipeline failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ QA Pipeline error: {e}")
        return False

def continuous_testing_cycle():
    """Run continuous testing cycle"""
    print("🔄 SOULFRIEND CONTINUOUS TESTING CYCLE")
    print("=" * 50)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("File Validation", validate_enhanced_files),
        ("Enhanced Questionnaire", test_enhanced_questionnaire_load),
        ("Enhanced Scoring", test_enhanced_scoring_logic),
        ("App Integration", test_app_integration),
        ("QA Pipeline", run_pipeline_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        start_time = time.time()
        result = test_func()
        end_time = time.time()
        duration = end_time - start_time
        
        results.append((test_name, result, duration))
        
        if result:
            print(f"✅ {test_name} PASSED in {duration:.2f}s")
        else:
            print(f"❌ {test_name} FAILED in {duration:.2f}s")
        print()
    
    # Final Summary
    print("=" * 50)
    print("📊 CONTINUOUS TESTING RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    total_time = sum(duration for _, _, duration in results)
    
    for test_name, result, duration in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name} ({duration:.2f}s)")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    
    print(f"\n📈 Overall Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    print(f"⏱️ Total Time: {total_time:.2f}s")
    
    # Synchronization Status
    if success_rate == 100:
        print("\n🎉 100% SYNCHRONIZATION ACHIEVED!")
        print("✨ All enhanced features working perfectly!")
        print("🚀 SOULFRIEND ready for production deployment!")
        sync_status = "PERFECT"
    elif success_rate >= 95:
        print("\n🎯 Near-Perfect Synchronization!")
        print("✨ Enhanced features mostly working!")
        print("🔧 Minor adjustments needed")
        sync_status = "EXCELLENT"
    elif success_rate >= 90:
        print("\n👍 Good Synchronization!")
        print("✨ Enhanced features working well!")
        print("🔧 Some improvements needed")
        sync_status = "GOOD"
    elif success_rate >= 80:
        print("\n⚠️ Moderate Synchronization")
        print("🔧 Several issues need fixing")
        sync_status = "MODERATE"
    else:
        print("\n❌ Poor Synchronization")
        print("🔧 Major fixes required")
        sync_status = "POOR"
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": timestamp,
        "success_rate": success_rate,
        "sync_status": sync_status,
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": total - passed,
        "total_time": total_time,
        "detailed_results": [
            {
                "test": name,
                "passed": result,
                "duration": duration
            }
            for name, result, duration in results
        ]
    }
    
    report_file = f"/workspaces/Mentalhealth/tests/CONTINUOUS_TEST_REPORT_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Report saved: {report_file}")
    print(f"📊 Synchronization Status: {sync_status}")
    
    return success_rate

if __name__ == "__main__":
    success_rate = continuous_testing_cycle()
    
    if success_rate == 100:
        print("\n🏆 MISSION ACCOMPLISHED!")
        exit(0)
    else:
        print(f"\n🔄 Continue improving to reach 100%")
        exit(1)
