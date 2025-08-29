#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE QUESTIONNAIRE TEST
Kiểm tra tất cả 5 questionnaires và display logic
"""

import sys
sys.path.insert(0, '/workspaces/Mentalhealth')

print("🔍 COMPREHENSIVE QUESTIONNAIRE TEST")
print("=" * 60)

# Test data for all questionnaires
test_cases = {
    "GAD-7": {
        "answers": {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1},  # Score: 13
        "expected_score": 13,
        "max_score": 21
    },
    "PHQ-9": {
        "answers": {1: 2, 2: 2, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0},  # Score: 11
        "expected_score": 11,
        "max_score": 27
    },
    "DASS-21": {
        "answers": {i: 1 for i in range(1, 22)},  # Score: 21 * 2 = 42 total
        "expected_score": 42,
        "max_score": 126
    },
    "EPDS": {
        "answers": {1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1},  # Score: 11
        "expected_score": 11,
        "max_score": 30
    },
    "PSS-10": {
        "answers": {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2},  # Score: 20
        "expected_score": 20,
        "max_score": 40
    }
}

try:
    from components.questionnaires import QuestionnaireManager
    from components.scoring import (
        score_gad7_enhanced, score_phq9_enhanced, score_dass21_enhanced,
        score_epds_enhanced, score_pss10_enhanced
    )
    
    scoring_functions = {
        "GAD-7": score_gad7_enhanced,
        "PHQ-9": score_phq9_enhanced,
        "DASS-21": score_dass21_enhanced,
        "EPDS": score_epds_enhanced,
        "PSS-10": score_pss10_enhanced
    }
    
    qm = QuestionnaireManager()
    
    results_summary = []
    
    for questionnaire_name, test_data in test_cases.items():
        print(f"\n🧪 Testing {questionnaire_name}")
        print("-" * 40)
        
        try:
            # Load config
            cfg = qm.load_questionnaire(questionnaire_name)
            if not cfg:
                print(f"❌ Failed to load config for {questionnaire_name}")
                continue
                
            # Get scoring function
            scoring_func = scoring_functions.get(questionnaire_name)
            if not scoring_func:
                print(f"❌ No scoring function for {questionnaire_name}")
                continue
                
            # Test scoring
            answers = test_data["answers"]
            expected_score = test_data["expected_score"]
            max_score = test_data["max_score"]
            
            result = scoring_func(answers, cfg)
            
            if result and hasattr(result, '__dict__'):
                actual_score = result.total_score
                severity = result.severity_level
                
                print(f"✅ Scoring successful")
                print(f"   📊 Expected: {expected_score}, Actual: {actual_score}")
                print(f"   📊 Severity: {severity}")
                print(f"   📊 Subscales: {list(result.subscales.keys()) if hasattr(result, 'subscales') and result.subscales else 'None'}")
                
                # Test object to dict conversion
                enhanced_dict = {
                    'total_score': result.total_score,
                    'severity_level': result.severity_level,
                    'interpretation': result.interpretation,
                    'recommendations': result.recommendations,
                    'subscales': {}
                }
                
                if hasattr(result, 'subscales') and result.subscales:
                    for subscale_name, subscale_obj in result.subscales.items():
                        if hasattr(subscale_obj, '__dict__'):
                            enhanced_dict['subscales'][subscale_name] = {
                                'raw': subscale_obj.raw,
                                'adjusted': subscale_obj.adjusted,
                                'severity': subscale_obj.severity,
                                'color': getattr(subscale_obj, 'color', 'green'),
                                'level_info': getattr(subscale_obj, 'level_info', {})
                            }
                
                # Test display logic simulation
                display_total = enhanced_dict.get('total_score', 0)
                display_severity = enhanced_dict.get('severity_level', 'Unknown')
                
                print(f"   📺 Display total: {display_total}/{max_score}")
                print(f"   📺 Display severity: {display_severity}")
                
                # Test subscale display
                for sub_name, sub_data in enhanced_dict['subscales'].items():
                    if isinstance(sub_data, dict):
                        sub_score = sub_data.get('adjusted', sub_data.get('raw', 0))
                        sub_severity = sub_data.get('severity', 'Unknown')
                        print(f"   📺 {sub_name}: {sub_score} ({sub_severity})")
                
                # Check if display will show 0 or actual value
                will_show_zero = all(
                    sub_data.get('adjusted', 0) == 0 or sub_data.get('raw', 0) == 0
                    for sub_data in enhanced_dict['subscales'].values()
                    if isinstance(sub_data, dict)
                )
                
                status = "❌ WILL SHOW 0" if will_show_zero and enhanced_dict['subscales'] else "✅ WILL SHOW CORRECT VALUES"
                print(f"   🎯 Status: {status}")
                
                results_summary.append({
                    'questionnaire': questionnaire_name,
                    'expected': expected_score,
                    'actual': actual_score,
                    'will_show_zero': will_show_zero and bool(enhanced_dict['subscales']),
                    'status': 'PASS' if not (will_show_zero and enhanced_dict['subscales']) else 'FAIL'
                })
                
            else:
                print(f"❌ Scoring failed or returned wrong type")
                results_summary.append({
                    'questionnaire': questionnaire_name,
                    'status': 'FAIL',
                    'error': 'Scoring failed'
                })
                
        except Exception as e:
            print(f"❌ Error testing {questionnaire_name}: {e}")
            results_summary.append({
                'questionnaire': questionnaire_name,
                'status': 'ERROR',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY RESULTS")
    print("="*60)
    
    total_questionnaires = len(test_cases)
    passing_questionnaires = sum(1 for r in results_summary if r.get('status') == 'PASS')
    failing_questionnaires = sum(1 for r in results_summary if r.get('will_show_zero', False))
    
    for result in results_summary:
        q_name = result['questionnaire']
        status = result.get('status', 'UNKNOWN')
        
        if status == 'PASS':
            print(f"✅ {q_name}: Chi tiết sẽ hiển thị ĐÚNG")
        elif result.get('will_show_zero'):
            print(f"❌ {q_name}: Chi tiết sẽ hiển thị 0 (SAI)")
        else:
            error = result.get('error', 'Unknown error')
            print(f"❌ {q_name}: Lỗi - {error}")
    
    print(f"\n🎯 CONCLUSION:")
    print(f"   📊 Tổng: {total_questionnaires} questionnaires")
    print(f"   ✅ Hoạt động đúng: {passing_questionnaires}")
    print(f"   ❌ Hiển thị 0: {failing_questionnaires}")
    
    if failing_questionnaires == 0:
        print("   🎉 TẤT CẢ QUESTIONNAIRES SẼ HIỂN THỊ ĐÚNG!")
    else:
        print(f"   ⚠️ {failing_questionnaires} questionnaires vẫn hiển thị 0")
        
except Exception as e:
    print(f"❌ Comprehensive test failed: {e}")
    import traceback
    traceback.print_exc()
