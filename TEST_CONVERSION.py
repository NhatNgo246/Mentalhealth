#!/usr/bin/env python3
"""
🧪 TEST ENHANCED RESULT CONVERSION
Test để verify rằng object -> dict conversion đã fix vấn đề 15/21 vs 0
"""

import sys
sys.path.insert(0, '/workspaces/Mentalhealth')

print("🧪 TESTING ENHANCED RESULT CONVERSION")
print("=" * 60)

try:
    from components.scoring import score_gad7_enhanced
    from components.questionnaires import load_questionnaire
    
    # Load GAD-7 config
    cfg = load_questionnaire("GAD-7")
    print("✅ GAD-7 config loaded")
    
    # Simulate user answers (moderately severe anxiety)
    answers = {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1}  # Total = 13 points
    
    # Get enhanced result object
    enhanced_result_obj = score_gad7_enhanced(answers, cfg)
    print(f"✅ Enhanced result object created: {type(enhanced_result_obj)}")
    
    # Check object attributes
    print(f"📊 Object total_score: {enhanced_result_obj.total_score}")
    print(f"📊 Object severity_level: {enhanced_result_obj.severity_level}")
    print(f"📊 Object interpretation: {enhanced_result_obj.interpretation}")
    print(f"📊 Object subscales: {enhanced_result_obj.subscales}")
    
    # Test conversion to dict (SOULFRIEND.py logic)
    if hasattr(enhanced_result_obj, '__dict__'):
        enhanced_dict = {
            'total_score': enhanced_result_obj.total_score,
            'severity_level': enhanced_result_obj.severity_level,
            'interpretation': enhanced_result_obj.interpretation,
            'recommendations': enhanced_result_obj.recommendations,
            'subscales': {}
        }
        
        # Convert subscales properly
        if hasattr(enhanced_result_obj, 'subscales') and enhanced_result_obj.subscales:
            for subscale_name, subscale_obj in enhanced_result_obj.subscales.items():
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
        
        print("\n✅ CONVERTED TO DICT:")
        print(f"📊 Dict total_score: {enhanced_dict.get('total_score', 'MISSING')}")
        print(f"📊 Dict severity_level: {enhanced_dict.get('severity_level', 'MISSING')}")
        print(f"📊 Dict interpretation: {enhanced_dict.get('interpretation', 'MISSING')}")
        print(f"📊 Dict subscales keys: {list(enhanced_dict.get('subscales', {}).keys())}")
        
        # Test subscale access (như trong SOULFRIEND.py)
        anxiety_subscale = enhanced_dict.get('subscales', {}).get('Anxiety', {})
        print(f"📊 Anxiety subscale data: {anxiety_subscale}")
        
        if anxiety_subscale:
            anxiety_score = anxiety_subscale.get('adjusted', 0)
            anxiety_severity = anxiety_subscale.get('severity', 'Unknown')
            print(f"✅ Anxiety score extracted: {anxiety_score}")
            print(f"✅ Anxiety severity extracted: {anxiety_severity}")
        else:
            print("❌ Anxiety subscale data missing!")
        
        # Final verification
        if enhanced_dict.get('total_score', 0) > 0 and anxiety_subscale.get('adjusted', 0) > 0:
            print("\n🎉 SUCCESS: Conversion successful! Chi tiết đánh giá should now show correct values")
        else:
            print("\n❌ ISSUE: Some values still missing after conversion")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
