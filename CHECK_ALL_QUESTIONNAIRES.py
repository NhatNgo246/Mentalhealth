#!/usr/bin/env python3
"""
🔍 KIỂM TRA TOÀN BỘ CÁC BỘ CÂU HỎI
Phân tích tại sao kết quả chi tiết hiển thị 0 cho tất cả questionnaires
"""

import sys
import json
import os
sys.path.insert(0, '/workspaces/Mentalhealth')

print("🔍 KIỂM TRA TOÀN BỘ CÁC BỘ CÂU HỎI")
print("=" * 60)

# Test 1: Kiểm tra file config tồn tại
print("\n📁 Test 1: Kiểm tra file config")
config_files = [
    'data/phq9_vi.json',
    'data/gad7_vi.json', 
    'data/dass21_vi.json',
    'data/epds_vi.json',
    'data/pss10_vi.json',
    'data/gad7_enhanced_vi.json',
    'data/phq9_enhanced_vi.json'
]

for file_path in config_files:
    full_path = f'/workspaces/Mentalhealth/{file_path}'
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions_count = len(data.get('questions', []))
                items_count = len(data.get('items', []))
                has_scoring = 'scoring' in data
                has_severity = 'severity_levels' in data.get('scoring', {})
                print(f"✅ {file_path}: {questions_count} questions, {items_count} items, scoring={has_scoring}, severity={has_severity}")
        except Exception as e:
            print(f"❌ {file_path}: Error loading - {e}")
    else:
        print(f"❌ {file_path}: File not found")

# Test 2: Kiểm tra QuestionnaireManager
print("\n🔧 Test 2: Kiểm tra QuestionnaireManager")
try:
    from components.questionnaires import QuestionnaireManager
    
    qm = QuestionnaireManager()
    questionnaires = ["DASS-21", "PHQ-9", "GAD-7", "EPDS", "PSS-10"]
    
    for q_name in questionnaires:
        try:
            cfg = qm.load_questionnaire(q_name)
            if cfg:
                questions = cfg.get('questions', [])
                items = cfg.get('items', [])
                scoring = cfg.get('scoring', {})
                print(f"✅ {q_name}: {len(questions)} questions, {len(items)} items, scoring={'✓' if scoring else '✗'}")
                
                # Kiểm tra scoring structure
                if scoring:
                    severity_levels = scoring.get('severity_levels', {})
                    print(f"   📊 Severity levels: {list(severity_levels.keys())}")
                else:
                    print(f"   ❌ No scoring configuration")
            else:
                print(f"❌ {q_name}: Failed to load config")
        except Exception as e:
            print(f"❌ {q_name}: Error - {e}")
            
except Exception as e:
    print(f"❌ QuestionnaireManager import error: {e}")

# Test 3: Kiểm tra scoring functions
print("\n🎯 Test 3: Kiểm tra scoring functions")
try:
    from components.scoring import (
        score_dass21_enhanced, score_phq9_enhanced, 
        score_gad7_enhanced, score_epds_enhanced, score_pss10_enhanced
    )
    
    # Test data - answers for 7 questions (GAD-7)
    test_answers = {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1}  # Should give score 15
    
    # Load GAD-7 config
    from components.questionnaires import QuestionnaireManager
    qm = QuestionnaireManager()
    gad7_cfg = qm.load_questionnaire("GAD-7")
    
    if gad7_cfg:
        print(f"✅ GAD-7 config loaded")
        
        # Test enhanced scoring
        try:
            result = score_gad7_enhanced(test_answers, gad7_cfg)
            print(f"✅ GAD-7 enhanced scoring works")
            print(f"   📊 Result type: {type(result)}")
            
            if hasattr(result, '__dict__'):
                print(f"   📊 total_score: {result.total_score}")
                print(f"   📊 severity_level: {result.severity_level}")
                print(f"   📊 subscales: {result.subscales}")
                
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
                        else:
                            enhanced_dict['subscales'][subscale_name] = subscale_obj
                
                print(f"   ✅ Converted to dict successfully")
                print(f"   📊 Dict total_score: {enhanced_dict['total_score']}")
                print(f"   📊 Dict subscales: {list(enhanced_dict['subscales'].keys())}")
                
                # Check subscale values
                for sub_name, sub_data in enhanced_dict['subscales'].items():
                    if isinstance(sub_data, dict):
                        print(f"      {sub_name}: raw={sub_data.get('raw', 0)}, adjusted={sub_data.get('adjusted', 0)}")
                    
            else:
                print(f"   ❌ Result is not an object: {result}")
                
        except Exception as e:
            print(f"❌ GAD-7 enhanced scoring error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ GAD-7 config not loaded")
        
except Exception as e:
    print(f"❌ Scoring functions import error: {e}")

# Test 4: Simulate complete user flow
print("\n🔄 Test 4: Simulate complete user flow")
try:
    # Mock session state
    mock_answers = {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1}
    current_questionnaire = "GAD-7"
    
    from components.questionnaires import QuestionnaireManager
    from components.scoring import score_gad7_enhanced
    
    qm = QuestionnaireManager()
    cfg = qm.load_questionnaire(current_questionnaire)
    
    if cfg:
        enhanced_result = score_gad7_enhanced(mock_answers, cfg)
        
        if enhanced_result:
            # Simulate object to dict conversion (như trong SOULFRIEND.py)
            if hasattr(enhanced_result, '__dict__'):
                enhanced_dict = {
                    'total_score': enhanced_result.total_score,
                    'severity_level': enhanced_result.severity_level,
                    'interpretation': enhanced_result.interpretation,
                    'recommendations': enhanced_result.recommendations,
                    'subscales': {}
                }
                
                if hasattr(enhanced_result, 'subscales') and enhanced_result.subscales:
                    for subscale_name, subscale_obj in enhanced_result.subscales.items():
                        if hasattr(subscale_obj, '__dict__'):
                            enhanced_dict['subscales'][subscale_name] = {
                                'raw': subscale_obj.raw,
                                'adjusted': subscale_obj.adjusted,
                                'severity': subscale_obj.severity,
                                'color': getattr(subscale_obj, 'color', 'green'),
                                'level_info': getattr(subscale_obj, 'level_info', {})
                            }
                        else:
                            enhanced_dict['subscales'][subscale_name] = subscale_obj
                
                # Simulate display logic (như trong SOULFRIEND.py)
                total_score = enhanced_dict.get('total_score', 0)
                severity_level = enhanced_dict.get('severity_level', 'Unknown')
                interpretation = enhanced_dict.get('interpretation', f'{current_questionnaire} assessment')
                
                print(f"✅ User flow simulation successful")
                print(f"   📊 Display total_score: {total_score}")
                print(f"   📊 Display severity_level: {severity_level}")
                print(f"   📊 Display interpretation: {interpretation}")
                
                # Test GAD-7 specific display logic
                subscale_data = enhanced_dict.get('subscales', {}).get('Anxiety', {})
                anxiety_score = subscale_data.get('adjusted', total_score)
                anxiety_severity = subscale_data.get('severity', severity_level)
                
                print(f"   📊 Anxiety subscale score: {anxiety_score}")
                print(f"   📊 Anxiety subscale severity: {anxiety_severity}")
                
                if anxiety_score > 0:
                    print(f"✅ PROBLEM SOLVED: Chi tiết sẽ hiển thị {anxiety_score} thay vì 0")
                else:
                    print(f"❌ PROBLEM PERSISTS: Chi tiết vẫn hiển thị 0")
                    
            else:
                print(f"❌ Enhanced result is not an object")
        else:
            print(f"❌ Enhanced result is None")
    else:
        print(f"❌ Config not loaded")
        
except Exception as e:
    print(f"❌ User flow simulation error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("🎯 CONCLUSION:")
print("Nếu các test trên PASS, vấn đề có thể là:")
print("1. ❌ Session state không lưu đúng enhanced_dict")
print("2. ❌ Display logic không access đúng keys")
print("3. ❌ Config files thiếu severity_levels structure")
print("4. ❌ Object conversion logic có bug")
