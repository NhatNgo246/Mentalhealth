#!/usr/bin/env python3
"""
Final comprehensive test of all enhanced scoring functions
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth')

from components.scoring import (
    score_phq9_enhanced, score_gad7_enhanced, score_dass21_enhanced, 
    score_epds_enhanced, score_pss10_enhanced
)
from components.questionnaires import load_questionnaire

def test_all_enhanced_scoring():
    print("🎯 FINAL COMPREHENSIVE TEST")
    print("=" * 50)
    
    # Test data for each questionnaire
    test_cases = {
        "PHQ-9": {
            "function": score_phq9_enhanced,
            "answers": {1: 1, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0},
            "expected_score": 9
        },
        "GAD-7": {
            "function": score_gad7_enhanced, 
            "answers": {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1},
            "expected_score": 13
        },
        "DASS-21": {
            "function": score_dass21_enhanced,
            "answers": {i: 2 for i in range(1, 22)},  # All 2s = 42 total
            "expected_score": 42
        },
        "EPDS": {
            "function": score_epds_enhanced,
            "answers": {1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1},
            "expected_score": 12
        },
        "PSS-10": {
            "function": score_pss10_enhanced,
            "answers": {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2},
            "expected_score": 20
        }
    }
    
    results = {}
    
    for questionnaire_name, test_data in test_cases.items():
        print(f"\n📋 Testing {questionnaire_name}")
        print("-" * 30)
        
        try:
            # Load config
            cfg = load_questionnaire(questionnaire_name)
            print(f"✅ Loaded {questionnaire_name} config")
            
            # Run scoring
            enhanced_result = test_data["function"](test_data["answers"], cfg)
            print(f"✅ Enhanced result type: {type(enhanced_result)}")
            
            # Check if it's proper EnhancedAssessmentResult
            if hasattr(enhanced_result, 'total_score') and hasattr(enhanced_result, 'severity_level'):
                actual_score = enhanced_result.total_score
                severity = enhanced_result.severity_level
                print(f"✅ Total score: {actual_score}/{test_data['expected_score']} (expected)")
                print(f"✅ Severity level: {severity}")
                
                if actual_score == test_data["expected_score"]:
                    results[questionnaire_name] = "✅ PASS"
                else:
                    results[questionnaire_name] = f"❌ FAIL (got {actual_score}, expected {test_data['expected_score']})"
            else:
                results[questionnaire_name] = "❌ FAIL (not EnhancedAssessmentResult)"
                print(f"❌ Missing attributes: {enhanced_result}")
                
        except Exception as e:
            results[questionnaire_name] = f"❌ ERROR: {str(e)}"
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    
    all_passed = True
    for questionnaire, result in results.items():
        print(f"{questionnaire:10} | {result}")
        if "FAIL" in result or "ERROR" in result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TẤT CẢ ENHANCED SCORING FUNCTIONS HOẠT ĐỘNG ĐÚNG!")
        print("✅ Sửa lỗi thành công - PHQ-9 và tất cả questionnaires sẽ hiển thị đúng điểm!")
    else:
        print("❌ Vẫn còn lỗi cần xử lý")
    print("=" * 50)

if __name__ == "__main__":
    test_all_enhanced_scoring()
