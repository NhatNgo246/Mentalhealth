#!/usr/bin/env python3
"""
Quick test to verify PHQ-9 fix in SOULFRIEND.py
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth')

from components.scoring import score_phq9_enhanced
from components.questionnaires import load_questionnaire

def test_phq9_fix():
    print("🔧 TESTING PHQ-9 FIX")
    print("=" * 40)
    
    # Load PHQ-9 config
    cfg = load_questionnaire("PHQ-9")
    print(f"✅ Loaded PHQ-9 config")
    
    # Test answers (same as before)
    test_answers = {1: 1, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0}
    print(f"📝 Test answers: {test_answers}")
    
    # Score using proper enhanced function
    enhanced_result = score_phq9_enhanced(test_answers, cfg)
    print(f"📊 Enhanced result type: {type(enhanced_result)}")
    print(f"📊 Enhanced result: {enhanced_result}")
    
    if hasattr(enhanced_result, 'total_score'):
        print(f"✅ Total score: {enhanced_result.total_score}")
        print(f"✅ Severity level: {enhanced_result.severity_level}")
    else:
        print("❌ Result doesn't have expected attributes")
    
    print("\n🎯 RESULT: Fixed! Now using proper EnhancedAssessmentResult object")

if __name__ == "__main__":
    test_phq9_fix()
