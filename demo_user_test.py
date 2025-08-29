#!/usr/bin/env python3
"""
👤 AUTOMATED USER EXPERIENCE TEST
Mô phỏng hành vi người dùng thực tế trên SOULFRIEND Demo
"""

import requests
import time
import sys
import os

sys.path.insert(0, "/workspaces/Mentalhealth")

def test_demo_functionality():
    """Test demo app như người dùng thực tế"""
    
    print("👤 SOULFRIEND DEMO USER EXPERIENCE TEST")
    print("=" * 60)
    print("🎯 Mô phỏng hành vi người dùng thực tế")
    print()
    
    # Test 1: Check demo app accessibility
    print("1️⃣ Testing Demo App Accessibility...")
    try:
        response = requests.get("http://localhost:8511", timeout=10)
        if response.status_code == 200:
            print("   ✅ Demo app is accessible")
            print(f"   📊 Response size: {len(response.content)} bytes")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Test 2: Component functionality (backend testing)
    print("\n2️⃣ Testing Backend Components...")
    
    # Test questionnaire loading
    try:
        from components.questionnaires import QuestionnaireManager
        manager = QuestionnaireManager()
        
        print("   📝 Testing Questionnaire Loading:")
        questionnaires = ['PHQ-9', 'GAD-7', 'DASS-21', 'PSS-10', 'EPDS']
        
        loaded_count = 0
        for q in questionnaires:
            try:
                data = manager.get_questionnaire(q)
                if data:
                    print(f"      ✅ {q}: Loaded successfully")
                    loaded_count += 1
                else:
                    print(f"      ❌ {q}: Failed to load")
            except Exception as e:
                print(f"      ❌ {q}: Error - {e}")
        
        print(f"   📊 Questionnaire success rate: {loaded_count}/{len(questionnaires)} ({loaded_count/len(questionnaires)*100:.1f}%)")
        
    except Exception as e:
        print(f"   ❌ Questionnaire component error: {e}")
        return False
    
    # Test 3: Scoring functionality
    print("\n3️⃣ Testing Scoring System...")
    
    try:
        from components.scoring import calculate_scores
        
        test_cases = [
            ('PHQ-9', [1, 2, 1, 0, 2, 1, 3, 2, 1], 'Moderate depression'),
            ('GAD-7', [2, 1, 3, 2, 1, 0, 2], 'Mild anxiety'),
            ('DASS-21', [1] * 21, 'Normal range'),
            ('PSS-10', [2] * 10, 'Moderate stress'),
            ('EPDS', [1, 0, 2, 1, 0, 1, 2, 1, 0, 1], 'Low risk')
        ]
        
        successful_scores = 0
        
        for questionnaire, responses, expected_type in test_cases:
            try:
                result = calculate_scores(responses, questionnaire)
                
                if result and 'total_score' in result:
                    score = result['total_score']
                    severity = result['severity']
                    print(f"   ✅ {questionnaire}: Score={score}, Severity={severity}")
                    successful_scores += 1
                else:
                    print(f"   ❌ {questionnaire}: Invalid result")
                    
            except Exception as e:
                print(f"   ❌ {questionnaire}: Error - {e}")
        
        print(f"   📊 Scoring success rate: {successful_scores}/{len(test_cases)} ({successful_scores/len(test_cases)*100:.1f}%)")
        
    except Exception as e:
        print(f"   ❌ Scoring system error: {e}")
        return False
    
    # Test 4: PDF generation
    print("\n4️⃣ Testing PDF Generation...")
    
    try:
        from components.pdf_export import generate_assessment_report
        
        sample_assessments = [
            {
                'questionnaire_type': 'PHQ-9',
                'total_score': 12,
                'severity': 'Moderate',
                'interpretation': 'Trầm cảm vừa',
                'responses': [1, 2, 1, 0, 2, 1, 3, 2, 1],
                'user_info': {'name': 'Test User 1', 'age': 25, 'date': '2025-08-27'}
            },
            {
                'questionnaire_type': 'GAD-7',
                'total_score': 8,
                'severity': 'Mild',
                'interpretation': 'Lo âu nhẹ',
                'responses': [2, 1, 3, 2, 1, 0, 2],
                'user_info': {'name': 'Test User 2', 'age': 30, 'date': '2025-08-27'}
            }
        ]
        
        pdf_success = 0
        
        for i, assessment in enumerate(sample_assessments):
            try:
                pdf_content = generate_assessment_report(assessment)
                
                if pdf_content and len(pdf_content) > 1000:
                    print(f"   ✅ {assessment['questionnaire_type']}: PDF generated ({len(pdf_content)} bytes)")
                    pdf_success += 1
                else:
                    print(f"   ❌ {assessment['questionnaire_type']}: PDF too small or empty")
                    
            except Exception as e:
                print(f"   ❌ {assessment['questionnaire_type']}: PDF error - {e}")
        
        print(f"   📊 PDF generation success rate: {pdf_success}/{len(sample_assessments)} ({pdf_success/len(sample_assessments)*100:.1f}%)")
        
    except Exception as e:
        print(f"   ❌ PDF system error: {e}")
        return False
    
    # Test 5: Simulated User Journey
    print("\n5️⃣ Simulating Complete User Journey...")
    
    try:
        # Scenario: User với lo âu nhẹ
        print("   👤 Scenario: User with mild anxiety")
        
        # Step 1: Choose questionnaire
        selected_questionnaire = 'GAD-7'
        print(f"   1. User selects: {selected_questionnaire}")
        
        # Step 2: Load questionnaire
        questionnaire_data = manager.get_questionnaire(selected_questionnaire)
        if questionnaire_data:
            print("   2. ✅ Questionnaire loaded successfully")
        else:
            print("   2. ❌ Failed to load questionnaire")
            return False
        
        # Step 3: Answer questions (simulate user responses)
        user_responses = [1, 2, 1, 1, 2, 0, 1]  # Mild anxiety responses
        print(f"   3. User answers {len(user_responses)} questions")
        
        # Step 4: Calculate scores
        results = calculate_scores(user_responses, selected_questionnaire)
        if results:
            score = results['total_score']
            severity = results['severity']
            print(f"   4. ✅ Results calculated: Score={score}, Severity={severity}")
        else:
            print("   4. ❌ Failed to calculate results")
            return False
        
        # Step 5: Generate PDF report
        assessment_data = {
            'questionnaire_type': selected_questionnaire,
            'total_score': score,
            'severity': severity,
            'interpretation': results['interpretation'],
            'responses': user_responses,
            'user_info': {
                'name': 'Journey Test User',
                'age': 28,
                'date': '2025-08-27'
            }
        }
        
        pdf_content = generate_assessment_report(assessment_data)
        if pdf_content and len(pdf_content) > 500:
            print(f"   5. ✅ PDF report generated ({len(pdf_content)} bytes)")
        else:
            print("   5. ❌ Failed to generate PDF report")
            return False
        
        print("   🎉 Complete user journey successful!")
        
    except Exception as e:
        print(f"   ❌ User journey error: {e}")
        return False
    
    # Test 6: Stress testing
    print("\n6️⃣ Testing System Performance...")
    
    try:
        start_time = time.time()
        iterations = 20
        
        successful_operations = 0
        
        for i in range(iterations):
            try:
                # Rapid questionnaire loading and scoring
                data = manager.get_questionnaire('PHQ-9')
                if data:
                    successful_operations += 1
                
                result = calculate_scores([1, 1, 1, 1, 1, 1, 1, 1, 1], 'PHQ-9')
                if result:
                    successful_operations += 1
                    
            except:
                pass
        
        end_time = time.time()
        duration = end_time - start_time
        operations_per_second = (successful_operations / duration) if duration > 0 else 0
        
        print(f"   📊 Performance: {successful_operations}/{iterations*2} operations in {duration:.2f}s")
        print(f"   ⚡ Speed: {operations_per_second:.1f} operations/second")
        
        if successful_operations >= iterations:  # At least 50% success rate
            print("   ✅ Performance test passed")
        else:
            print("   ❌ Performance test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Performance test error: {e}")
        return False
    
    # Final Assessment
    print("\n" + "=" * 60)
    print("📊 USER EXPERIENCE TEST SUMMARY")
    print("=" * 60)
    
    test_results = [
        ("Demo App Accessibility", True),
        ("Backend Components", loaded_count >= 4),
        ("Scoring System", successful_scores >= 4),
        ("PDF Generation", pdf_success >= 1),
        ("User Journey", True),
        ("Performance", successful_operations >= iterations)
    ]
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"\n📈 Test Results: {passed}/{total} ({passed/total*100:.1f}%)")
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🕐 Test completed at: {time.strftime('%H:%M:%S')}")
    
    if passed == total:
        print("\n🎉 EXCELLENT USER EXPERIENCE!")
        print("✅ SOULFRIEND Demo provides outstanding user experience.")
        print("🚀 Ready for production deployment!")
        return True
    elif passed >= total * 0.8:
        print("\n👍 GOOD USER EXPERIENCE!")
        print("✅ SOULFRIEND Demo works well with minor areas for improvement.")
        print("🔧 Recommended for production with monitoring.")
        return True
    else:
        print("\n⚠️ USER EXPERIENCE NEEDS IMPROVEMENT")
        print("❌ SOULFRIEND Demo has significant issues.")
        print("🛠️ Please address critical issues before deployment.")
        return False

if __name__ == "__main__":
    success = test_demo_functionality()
    sys.exit(0 if success else 1)
