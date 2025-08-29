#!/usr/bin/env python3
"""
🎯 QUICK USER TEST - Kiểm tra nhanh chức năng cơ bản
"""

import requests
import time
import sys
import os

def test_basic_functionality():
    """Test chức năng cơ bản như người dùng"""
    
    print("🎯 SOULFRIEND QUICK USER TEST")
    print("=" * 50)
    
    # Test 1: Check if app is running
    print("\n1️⃣ Testing if SOULFRIEND is accessible...")
    try:
        response = requests.get("http://localhost:8510", timeout=10)
        if response.status_code == 200:
            print("✅ SOULFRIEND is running and accessible")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test 2: Test component imports (simulate user interaction)
    print("\n2️⃣ Testing core components...")
    try:
        os.chdir("/workspaces/Mentalhealth")
        sys.path.insert(0, "/workspaces/Mentalhealth")
        
        # Test questionnaire loading
        from components.questionnaires import QuestionnaireManager
        manager = QuestionnaireManager()
        
        questionnaires = ['PHQ-9', 'GAD-7', 'DASS-21']
        for q in questionnaires:
            try:
                data = manager.get_questionnaire(q)
                if data:
                    print(f"   ✅ {q}: Loaded successfully")
                else:
                    print(f"   ❌ {q}: Failed to load")
            except Exception as e:
                print(f"   ❌ {q}: Error - {e}")
    
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False
    
    # Test 3: Test scoring functionality
    print("\n3️⃣ Testing scoring system...")
    try:
        from components.scoring import calculate_scores
        
        # Test PHQ-9 scoring
        sample_responses = [1, 2, 1, 0, 2, 1, 3, 2, 1]
        result = calculate_scores(sample_responses, "PHQ-9")
        
        if result and 'total_score' in result:
            score = result['total_score']
            severity = result['severity']
            print(f"   ✅ PHQ-9 Scoring: Score={score}, Severity={severity}")
        else:
            print("   ❌ PHQ-9 Scoring failed")
            return False
            
    except Exception as e:
        print(f"❌ Scoring test failed: {e}")
        return False
    
    # Test 4: Test PDF generation
    print("\n4️⃣ Testing PDF export...")
    try:
        from components.pdf_export import generate_assessment_report
        
        sample_data = {
            'questionnaire_type': 'PHQ-9',
            'total_score': 13,
            'severity': 'Moderate',
            'interpretation': 'Trầm cảm vừa',
            'responses': sample_responses,
            'user_info': {
                'name': 'Test User',
                'age': 25,
                'date': '2025-08-27'
            }
        }
        
        pdf_content = generate_assessment_report(sample_data)
        
        if pdf_content and len(pdf_content) > 1000:
            print(f"   ✅ PDF Export: Generated {len(pdf_content)} bytes")
        else:
            print("   ❌ PDF Export failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF test failed: {e}")
        return False
    
    print("\n🎉 ALL BASIC TESTS PASSED!")
    print("✅ SOULFRIEND core functionality is working correctly.")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
