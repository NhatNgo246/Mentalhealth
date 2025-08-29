#!/usr/bin/env python3
"""
Test GAD-7 Enhanced Integration
Kiểm tra tích hợp GAD-7 Enhanced với hệ thống
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth')

def test_gad7_enhanced():
    """Test GAD-7 Enhanced functionality"""
    print("🧪 Testing GAD-7 Enhanced Integration...")
    
    try:
        # Test 1: Import questionnaire loader
        print("\n1. Testing GAD-7 Enhanced questionnaire loading...")
        from components.questionnaires import load_gad7_enhanced_vi
        
        cfg = load_gad7_enhanced_vi()
        print(f"✅ GAD-7 Enhanced loaded successfully")
        print(f"   - Scale: {cfg['scale']}")
        print(f"   - Version: {cfg['version']}")
        print(f"   - Questions: {len(cfg['items'])}")
        print(f"   - Severity levels: {len(cfg['scoring']['severity_levels'])}")
        
        # Test 2: Import scoring function
        print("\n2. Testing GAD-7 Enhanced scoring...")
        from components.scoring import score_gad7_enhanced
        
        # Test with sample answers (moderate anxiety)
        test_answers = {
            1: 2,  # Moderate
            2: 1,  # Mild
            3: 2,  # Moderate
            4: 1,  # Mild
            5: 2,  # Moderate
            6: 1,  # Mild
            7: 2   # Moderate
        }
        
        result = score_gad7_enhanced(test_answers, cfg)
        print(f"✅ GAD-7 Enhanced scoring successful")
        print(f"   - Total score: {result.total_score}/21")
        print(f"   - Severity: {result.severity_level}")
        print(f"   - Interpretation: {result.interpretation}")
        print(f"   - Has recommendations: {'recommendations' in result.__dict__}")
        
        # Test 3: Check high anxiety scenario
        print("\n3. Testing high anxiety scenario...")
        high_anxiety_answers = {i: 3 for i in range(1, 8)}  # All severe
        high_anxiety_result = score_gad7_enhanced(high_anxiety_answers, cfg)
        
        print(f"✅ High anxiety scenario tested")
        print(f"   - Total score: {high_anxiety_result.total_score}/21")
        print(f"   - Severity: {high_anxiety_result.severity_level}")
        print(f"   - Emergency contacts included: {'emergency_contacts' in high_anxiety_result.recommendations}")
        
        # Test 4: Validate data structure
        print("\n4. Validating GAD-7 Enhanced data structure...")
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
        
        print("\n🎉 GAD-7 Enhanced Integration Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ GAD-7 Enhanced Integration Test FAILED!")
        print(f"Error: {str(e)}")
        return False

def test_all_questionnaires():
    """Test all questionnaire types integration"""
    print("\n🧪 Testing All Questionnaires Integration...")
    
    try:
        # Test imports
        from components.questionnaires import (
            load_dass21_enhanced_vi, 
            load_phq9_enhanced_vi, 
            load_gad7_enhanced_vi
        )
        from components.scoring import (
            score_dass21_enhanced, 
            score_phq9_enhanced, 
            score_gad7_enhanced
        )
        
        print("✅ All questionnaire functions imported successfully")
        
        # Test DASS-21
        dass_cfg = load_dass21_enhanced_vi()
        print(f"✅ DASS-21: {len(dass_cfg['items'])} questions, {len(dass_cfg['scoring']['subscales'])} subscales")
        
        # Test PHQ-9
        phq_cfg = load_phq9_enhanced_vi()
        print(f"✅ PHQ-9: {len(phq_cfg['items'])} questions, severity levels: {list(phq_cfg['scoring']['severity_levels'].keys())}")
        
        # Test GAD-7
        gad_cfg = load_gad7_enhanced_vi()
        print(f"✅ GAD-7: {len(gad_cfg['items'])} questions, severity levels: {list(gad_cfg['scoring']['severity_levels'].keys())}")
        
        print("\n🎉 All Questionnaires Integration Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ All Questionnaires Integration Test FAILED!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GAD-7 ENHANCED & MULTI-QUESTIONNAIRE TEST SUITE")
    print("=" * 60)
    
    test1_result = test_gad7_enhanced()
    test2_result = test_all_questionnaires()
    
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    if test1_result and test2_result:
        print("🟢 ALL TESTS PASSED - GAD-7 Enhanced & Multi-Questionnaire ready!")
        exit(0)
    else:
        print("🔴 SOME TESTS FAILED - Check logs for details")
        exit(1)
