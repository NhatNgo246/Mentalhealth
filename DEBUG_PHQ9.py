#!/usr/bin/env python3
"""
🔍 DEBUG PHQ-9 SPECIFIC ISSUE
Kiểm tra tại sao PHQ-9 trả về 0 trong thực tế
"""

import sys
sys.path.insert(0, '/workspaces/Mentalhealth')

print("🔍 DEBUG PHQ-9 SPECIFIC ISSUE")
print("=" * 50)

try:
    from components.questionnaires import QuestionnaireManager
    from components.scoring import score_phq9_enhanced
    
    qm = QuestionnaireManager()
    
    # Load PHQ-9 config
    print("📁 Loading PHQ-9 config...")
    cfg = qm.load_questionnaire("PHQ-9")
    
    if cfg:
        print("✅ PHQ-9 config loaded successfully")
        print(f"   📊 Items: {len(cfg.get('items', []))}")
        print(f"   📊 Scoring: {'✓' if cfg.get('scoring') else '✗'}")
        
        # Check scoring structure
        scoring = cfg.get('scoring', {})
        if scoring:
            severity_levels = scoring.get('severity_levels', {})
            print(f"   📊 Severity levels: {list(severity_levels.keys())}")
            
            # Show structure
            for level_name, level_data in severity_levels.items():
                print(f"      {level_name}: {level_data.get('range', 'No range')}")
        else:
            print("   ❌ No scoring configuration")
            
        # Test with actual user answers (simulate real answers that gave 0)
        print(f"\n🧪 Testing PHQ-9 enhanced scoring...")
        
        # Test with various answer sets
        test_cases = [
            {"name": "All zeros", "answers": {i: 0 for i in range(1, 10)}},
            {"name": "All ones", "answers": {i: 1 for i in range(1, 10)}},
            {"name": "Mixed answers", "answers": {1: 1, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0}},
            {"name": "Real user answers", "answers": {1: 2, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1, 8: 0, 9: 0}}
        ]
        
        for test_case in test_cases:
            answers = test_case["answers"]
            name = test_case["name"]
            
            print(f"\n   🔍 Test case: {name}")
            print(f"      Answers: {answers}")
            
            try:
                result = score_phq9_enhanced(answers, cfg)
                
                if result:
                    if hasattr(result, '__dict__'):
                        print(f"      ✅ Result type: EnhancedAssessmentResult")
                        print(f"      📊 Total score: {result.total_score}")
                        print(f"      📊 Severity: {result.severity_level}")
                        print(f"      📊 Interpretation: {result.interpretation}")
                        
                        if hasattr(result, 'subscales') and result.subscales:
                            for sub_name, sub_obj in result.subscales.items():
                                if hasattr(sub_obj, '__dict__'):
                                    print(f"      📊 {sub_name}: raw={sub_obj.raw}, adjusted={sub_obj.adjusted}")
                    else:
                        print(f"      ❌ Result type: {type(result)}")
                        print(f"      📊 Result: {result}")
                else:
                    print(f"      ❌ Result is None")
                    
            except Exception as e:
                print(f"      ❌ Scoring error: {e}")
                import traceback
                traceback.print_exc()
                
        # Test manual calculation
        print(f"\n🧮 Manual calculation test:")
        answers = {1: 2, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1, 8: 0, 9: 0}
        manual_total = sum(answers.values())
        print(f"   📊 Manual total: {manual_total}")
        
        # Check if items have reverse scoring
        items = cfg.get('items', [])
        print(f"\n📝 Items analysis:")
        for item in items[:3]:  # Show first 3 items
            print(f"   Item {item.get('id', '?')}: {item.get('text', 'No text')[:50]}...")
            if item.get('reverse_scored'):
                print(f"      ⚠️ Reverse scored!")
    else:
        print("❌ Failed to load PHQ-9 config")
        
    # Test QuestionnaireManager mapping
    print(f"\n🔧 QuestionnaireManager mapping:")
    print(f"   PHQ-9 maps to: {qm.questionnaires.get('PHQ-9', 'NOT FOUND')}")
    
except Exception as e:
    print(f"❌ Debug failed: {e}")
    import traceback
    traceback.print_exc()
