#!/usr/bin/env python3
"""
Test PHQ-9 Enhanced Integration
Kiểm tra tích hợp PHQ-9 Enhanced với SOULFRIEND.py
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth')

def test_phq9_enhanced():
    """Test PHQ-9 Enhanced functionality"""
    print("🧪 Testing PHQ-9 Enhanced Integration...")
    
    try:
        # Test 1: Import questionnaire loader
        print("\n1. Testing PHQ-9 Enhanced questionnaire loading...")
        from components.questionnaires import load_phq9_enhanced_vi
        
        cfg = load_phq9_enhanced_vi()
        print(f"✅ PHQ-9 Enhanced loaded successfully")
        print(f"   - Scale: {cfg['scale']}")
        print(f"   - Version: {cfg['version']}")
        print(f"   - Questions: {len(cfg['items'])}")
        print(f"   - Severity levels: {len(cfg['scoring']['severity_levels'])}")
        
        # Test 2: Import scoring function
        print("\n2. Testing PHQ-9 Enhanced scoring...")
        from components.scoring import score_phq9_enhanced
        
        # Test with sample answers
        test_answers = {
            1: 2,  # Moderate
            2: 1,  # Mild
            3: 2,  # Moderate
            4: 1,  # Mild
            5: 0,  # None
            6: 1,  # Mild
            7: 2,  # Moderate
            8: 0,  # None
            9: 1   # Mild (suicide risk)
        }
        
        result = score_phq9_enhanced(test_answers, cfg)
        print(f"✅ PHQ-9 Enhanced scoring successful")
        print(f"   - Total score: {result.total_score}/27")
        print(f"   - Severity: {result.severity_level}")
        print(f"   - Interpretation: {result.interpretation}")
        print(f"   - Has recommendations: {'recommendations' in result.__dict__}")
        
        # Test 3: Check suicide risk handling
        print("\n3. Testing suicide risk assessment...")
        high_risk_answers = {i: 3 for i in range(1, 10)}  # All severe
        high_risk_result = score_phq9_enhanced(high_risk_answers, cfg)
        
        print(f"✅ High risk scenario tested")
        print(f"   - Total score: {high_risk_result.total_score}/27")
        print(f"   - Severity: {high_risk_result.severity_level}")
        print(f"   - Emergency contacts included: {'emergency_contacts' in high_risk_result.recommendations}")
        
        # Test 4: Validate data structure
        print("\n4. Validating PHQ-9 Enhanced data structure...")
        required_keys = ['scale', 'version', 'items', 'options', 'scoring', 'recommendations']
        missing_keys = [key for key in required_keys if key not in cfg]
        
        if not missing_keys:
            print("✅ All required keys present in configuration")
        else:
            print(f"❌ Missing keys: {missing_keys}")
            
        # Test 5: Check Vietnamese context
        print("\n5. Testing Vietnamese localization...")
        vietnamese_items = [item for item in cfg['items'] if 'vietnamese_context' in item]
        print(f"✅ Vietnamese context: {len(vietnamese_items)}/{len(cfg['items'])} items")
        
        emergency_vietnam = 'vietnam' in cfg.get('emergency_contacts', {})
        print(f"✅ Vietnam emergency contacts: {'Yes' if emergency_vietnam else 'No'}")
        
        print("\n🎉 PHQ-9 Enhanced Integration Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ PHQ-9 Enhanced Integration Test FAILED!")
        print(f"Error: {str(e)}")
        return False

def test_multi_questionnaire_support():
    """Test multi-questionnaire support in SOULFRIEND.py"""
    print("\n🧪 Testing Multi-Questionnaire Support...")
    
    try:
        # Test both questionnaire loaders
        from components.questionnaires import load_dass21_enhanced_vi, load_phq9_enhanced_vi
        from components.scoring import score_dass21_enhanced, score_phq9_enhanced
        
        print("✅ All questionnaire functions imported successfully")
        
        # Test DASS-21
        dass_cfg = load_dass21_enhanced_vi()
        print(f"✅ DASS-21: {len(dass_cfg['items'])} questions, {len(dass_cfg['scoring']['subscales'])} subscales")
        
        # Test PHQ-9
        phq_cfg = load_phq9_enhanced_vi()
        print(f"✅ PHQ-9: {len(phq_cfg['items'])} questions, severity levels: {list(phq_cfg['scoring']['severity_levels'].keys())}")
        
        print("\n🎉 Multi-Questionnaire Support Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Multi-Questionnaire Support Test FAILED!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PHQ-9 ENHANCED INTEGRATION TEST SUITE")
    print("=" * 60)
    
    test1_result = test_phq9_enhanced()
    test2_result = test_multi_questionnaire_support()
    
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    if test1_result and test2_result:
        print("🟢 ALL TESTS PASSED - PHQ-9 Enhanced ready for deployment!")
        exit(0)
    else:
        print("🔴 SOME TESTS FAILED - Check logs for details")
        exit(1)
