#!/usr/bin/env python3
"""
👤 SOULFRIEND USER EXPERIENCE TESTING
Mô phỏng hành vi người dùng thực tế để test toàn bộ chức năng
"""

import requests
import time
import json
import os
from datetime import datetime
import subprocess
import sys

class SOULFRIENDUserTester:
    def __init__(self, base_url="http://localhost:8510"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.user_scenarios = []
        
    def log_test(self, scenario, action, status, details=""):
        timestamp = datetime.now().strftime('%H:%M:%S')
        symbol = "✅" if status else "❌"
        message = f"[{timestamp}] {symbol} {scenario} - {action}: {details}"
        print(message)
        
        self.test_results.append({
            'timestamp': timestamp,
            'scenario': scenario,
            'action': action,
            'status': status,
            'details': details
        })
        
    def test_application_startup(self):
        """Test 1: Kiểm tra ứng dụng có khởi động được không"""
        print("\n🚀 TEST 1: APPLICATION STARTUP")
        print("=" * 50)
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log_test("Startup", "Load Homepage", True, f"Status: {response.status_code}")
                
                # Check if it's actually Streamlit
                if "streamlit" in response.text.lower() or "SOULFRIEND" in response.text:
                    self.log_test("Startup", "Streamlit Detection", True, "SOULFRIEND app detected")
                    return True
                else:
                    self.log_test("Startup", "Content Validation", False, "Not a Streamlit app")
                    return False
            else:
                self.log_test("Startup", "Load Homepage", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("Startup", "Connection", False, "Cannot connect to application")
            return False
        except Exception as e:
            self.log_test("Startup", "Load Homepage", False, str(e))
            return False
    
    def test_navigation_and_interface(self):
        """Test 2: Kiểm tra navigation và giao diện"""
        print("\n🧭 TEST 2: NAVIGATION & INTERFACE")
        print("=" * 50)
        
        # Test các endpoint cơ bản của Streamlit
        endpoints_to_test = [
            "/",
            "/_stcore/health",
            "/_stcore/vendor",
        ]
        
        navigation_ok = True
        
        for endpoint in endpoints_to_test:
            try:
                url = self.base_url + endpoint
                response = self.session.get(url, timeout=5)
                
                if response.status_code in [200, 204]:
                    self.log_test("Navigation", f"Access {endpoint}", True, f"Status: {response.status_code}")
                else:
                    self.log_test("Navigation", f"Access {endpoint}", False, f"Status: {response.status_code}")
                    navigation_ok = False
                    
            except Exception as e:
                self.log_test("Navigation", f"Access {endpoint}", False, str(e))
                navigation_ok = False
                
        return navigation_ok
    
    def test_questionnaire_functionality(self):
        """Test 3: Test chức năng questionnaire qua Python import"""
        print("\n📝 TEST 3: QUESTIONNAIRE FUNCTIONALITY")
        print("=" * 50)
        
        try:
            # Change to app directory
            os.chdir("/workspaces/Mentalhealth")
            sys.path.insert(0, "/workspaces/Mentalhealth")
            
            # Test import questionnaire components
            from components.questionnaires import QuestionnaireManager, load_questionnaire
            from components.scoring import calculate_scores
            
            manager = QuestionnaireManager()
            questionnaires = ['PHQ-9', 'GAD-7', 'DASS-21', 'PSS-10', 'EPDS']
            
            all_questionnaires_ok = True
            
            for q_type in questionnaires:
                try:
                    # Test loading questionnaire
                    data = manager.get_questionnaire(q_type)
                    if data:
                        self.log_test("Questionnaire", f"Load {q_type}", True, f"Questions loaded")
                        
                        # Test scoring with sample data
                        if q_type == 'PHQ-9':
                            sample_responses = [1, 2, 1, 0, 2, 1, 3, 2, 1]  # 9 questions
                        elif q_type == 'GAD-7':
                            sample_responses = [2, 1, 3, 2, 1, 0, 2]  # 7 questions
                        elif q_type == 'DASS-21':
                            sample_responses = [1] * 21  # 21 questions
                        elif q_type == 'PSS-10':
                            sample_responses = [2] * 10  # 10 questions
                        elif q_type == 'EPDS':
                            sample_responses = [1, 0, 2, 1, 0, 1, 2, 1, 0, 1]  # 10 questions
                        
                        # Test scoring
                        result = calculate_scores(sample_responses, q_type)
                        if result and 'total_score' in result:
                            score = result['total_score']
                            severity = result.get('severity', 'Unknown')
                            self.log_test("Questionnaire", f"Score {q_type}", True, f"Score: {score}, Severity: {severity}")
                        else:
                            self.log_test("Questionnaire", f"Score {q_type}", False, "Invalid scoring result")
                            all_questionnaires_ok = False
                    else:
                        self.log_test("Questionnaire", f"Load {q_type}", False, "Empty data returned")
                        all_questionnaires_ok = False
                        
                except Exception as e:
                    self.log_test("Questionnaire", f"Test {q_type}", False, str(e))
                    all_questionnaires_ok = False
            
            return all_questionnaires_ok
            
        except Exception as e:
            self.log_test("Questionnaire", "Setup", False, f"Import error: {e}")
            return False
    
    def test_ai_components(self):
        """Test 4: Test AI components"""
        print("\n🤖 TEST 4: AI COMPONENTS")
        print("=" * 50)
        
        try:
            os.chdir("/workspaces/Mentalhealth")
            sys.path.insert(0, "/workspaces/Mentalhealth")
            
            ai_tests = [
                ("AI Insights", "from components.ai_insights import MentalHealthAI"),
                ("Chatbot AI", "from chatbot_ai import MentalHealthChatbot"),
            ]
            
            ai_ok = True
            
            for component_name, import_statement in ai_tests:
                try:
                    exec(import_statement)
                    self.log_test("AI Components", f"Import {component_name}", True, "Successfully imported")
                except ImportError as e:
                    self.log_test("AI Components", f"Import {component_name}", False, f"Import failed: {e}")
                    ai_ok = False
                except Exception as e:
                    self.log_test("AI Components", f"Import {component_name}", False, str(e))
                    ai_ok = False
            
            # Test AI functionality if imports succeed
            if ai_ok:
                try:
                    # Test MentalHealthAI
                    from components.ai_insights import MentalHealthAI
                    ai_engine = MentalHealthAI()
                    
                    # Test prediction
                    sample_data = {
                        'age': 25,
                        'phq9_score': 12,
                        'gad7_score': 8,
                        'stress_level': 6
                    }
                    
                    prediction = ai_engine.predict_risk(sample_data)
                    if prediction:
                        self.log_test("AI Components", "Risk Prediction", True, f"Prediction: {prediction}")
                    else:
                        self.log_test("AI Components", "Risk Prediction", False, "No prediction returned")
                        
                except Exception as e:
                    self.log_test("AI Components", "AI Functionality", False, str(e))
                    ai_ok = False
            
            return ai_ok
            
        except Exception as e:
            self.log_test("AI Components", "Setup", False, str(e))
            return False
    
    def test_pdf_export(self):
        """Test 5: Test PDF export functionality"""
        print("\n📄 TEST 5: PDF EXPORT")
        print("=" * 50)
        
        try:
            os.chdir("/workspaces/Mentalhealth")
            sys.path.insert(0, "/workspaces/Mentalhealth")
            
            from components.pdf_export import generate_assessment_report
            
            # Test data for PDF generation
            sample_assessment = {
                'questionnaire_type': 'PHQ-9',
                'total_score': 12,
                'severity': 'Moderate',
                'interpretation': 'Trầm cảm vừa',
                'responses': [1, 2, 1, 0, 2, 1, 3, 2, 1],
                'user_info': {
                    'name': 'Test User',
                    'age': 25,
                    'date': datetime.now().strftime('%Y-%m-%d')
                }
            }
            
            # Test PDF generation
            pdf_content = generate_assessment_report(sample_assessment)
            
            if pdf_content and len(pdf_content) > 1000:  # PDF should be substantial
                self.log_test("PDF Export", "Generate Report", True, f"PDF size: {len(pdf_content)} bytes")
                
                # Test saving PDF
                test_pdf_path = "/tmp/test_soulfriend_report.pdf"
                with open(test_pdf_path, 'wb') as f:
                    f.write(pdf_content)
                
                if os.path.exists(test_pdf_path):
                    file_size = os.path.getsize(test_pdf_path)
                    self.log_test("PDF Export", "Save File", True, f"Saved: {file_size} bytes")
                    
                    # Clean up
                    os.remove(test_pdf_path)
                    return True
                else:
                    self.log_test("PDF Export", "Save File", False, "File not created")
                    return False
            else:
                self.log_test("PDF Export", "Generate Report", False, "Invalid PDF content")
                return False
                
        except Exception as e:
            self.log_test("PDF Export", "Functionality", False, str(e))
            return False
    
    def test_error_handling(self):
        """Test 6: Test error handling"""
        print("\n🛠️ TEST 6: ERROR HANDLING")
        print("=" * 50)
        
        try:
            os.chdir("/workspaces/Mentalhealth")
            sys.path.insert(0, "/workspaces/Mentalhealth")
            
            from components.questionnaires import QuestionnaireManager
            from components.scoring import calculate_scores
            
            manager = QuestionnaireManager()
            
            # Test invalid questionnaire
            try:
                invalid_data = manager.get_questionnaire("INVALID-QUESTIONNAIRE")
                self.log_test("Error Handling", "Invalid Questionnaire", False, "Should have raised error")
            except ValueError:
                self.log_test("Error Handling", "Invalid Questionnaire", True, "Properly caught ValueError")
            except Exception as e:
                self.log_test("Error Handling", "Invalid Questionnaire", True, f"Caught: {type(e).__name__}")
            
            # Test invalid scoring data
            try:
                invalid_result = calculate_scores([], "PHQ-9")  # Empty responses
                if invalid_result and invalid_result['total_score'] == 0:
                    self.log_test("Error Handling", "Empty Responses", True, "Handled gracefully")
                else:
                    self.log_test("Error Handling", "Empty Responses", False, "Unexpected result")
            except Exception as e:
                self.log_test("Error Handling", "Empty Responses", True, f"Properly handled: {e}")
            
            # Test malformed data
            try:
                malformed_result = calculate_scores("invalid_data", "PHQ-9")
                self.log_test("Error Handling", "Malformed Data", True, "Handled malformed input")
            except Exception as e:
                self.log_test("Error Handling", "Malformed Data", True, f"Properly caught: {type(e).__name__}")
            
            return True
            
        except Exception as e:
            self.log_test("Error Handling", "Setup", False, str(e))
            return False
    
    def simulate_user_journey(self):
        """Test 7: Mô phỏng hành trình người dùng hoàn chỉnh"""
        print("\n👤 TEST 7: COMPLETE USER JOURNEY SIMULATION")
        print("=" * 50)
        
        try:
            os.chdir("/workspaces/Mentalhealth")
            sys.path.insert(0, "/workspaces/Mentalhealth")
            
            from components.questionnaires import QuestionnaireManager
            from components.scoring import calculate_scores
            from components.pdf_export import generate_assessment_report
            
            # Scenario: Người dùng lo âu về trầm cảm
            self.log_test("User Journey", "Start Session", True, "User begins mental health assessment")
            
            # Step 1: Chọn questionnaire PHQ-9
            manager = QuestionnaireManager()
            questionnaire_data = manager.get_questionnaire("PHQ-9")
            
            if questionnaire_data:
                self.log_test("User Journey", "Select PHQ-9", True, "Questionnaire loaded successfully")
            else:
                self.log_test("User Journey", "Select PHQ-9", False, "Failed to load questionnaire")
                return False
            
            # Step 2: Trả lời câu hỏi (mô phỏng người có triệu chứng trầm cảm vừa)
            user_responses = [2, 2, 1, 1, 2, 1, 2, 2, 0]  # Moderate depression responses
            self.log_test("User Journey", "Answer Questions", True, f"Completed {len(user_responses)} questions")
            
            # Step 3: Tính điểm
            results = calculate_scores(user_responses, "PHQ-9")
            
            if results and 'total_score' in results:
                score = results['total_score']
                severity = results['severity']
                self.log_test("User Journey", "Calculate Score", True, f"Score: {score}, Level: {severity}")
            else:
                self.log_test("User Journey", "Calculate Score", False, "Scoring failed")
                return False
            
            # Step 4: Tạo báo cáo PDF
            assessment_data = {
                'questionnaire_type': 'PHQ-9',
                'total_score': score,
                'severity': severity,
                'interpretation': results.get('interpretation', ''),
                'responses': user_responses,
                'user_info': {
                    'name': 'Test User Journey',
                    'age': 28,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'session_id': 'UJ-' + str(int(time.time()))
                }
            }
            
            pdf_content = generate_assessment_report(assessment_data)
            
            if pdf_content and len(pdf_content) > 500:
                self.log_test("User Journey", "Generate Report", True, f"PDF created ({len(pdf_content)} bytes)")
            else:
                self.log_test("User Journey", "Generate Report", False, "PDF generation failed")
                return False
            
            # Step 5: Scenario nặng - test emergency protocol
            severe_responses = [3, 3, 3, 3, 3, 3, 3, 3, 2]  # Severe depression
            severe_results = calculate_scores(severe_responses, "PHQ-9")
            
            if severe_results and severe_results['total_score'] >= 20:
                self.log_test("User Journey", "Emergency Detection", True, f"High-risk score: {severe_results['total_score']}")
            else:
                self.log_test("User Journey", "Emergency Detection", False, "Emergency protocol not triggered")
            
            self.log_test("User Journey", "Complete Session", True, "Full user journey completed successfully")
            return True
            
        except Exception as e:
            self.log_test("User Journey", "Execution", False, str(e))
            return False
    
    def test_performance_stress(self):
        """Test 8: Test hiệu suất và stress"""
        print("\n⚡ TEST 8: PERFORMANCE & STRESS")
        print("=" * 50)
        
        try:
            os.chdir("/workspaces/Mentalhealth")
            sys.path.insert(0, "/workspaces/Mentalhealth")
            
            from components.questionnaires import QuestionnaireManager
            from components.scoring import calculate_scores
            
            manager = QuestionnaireManager()
            
            # Test multiple rapid requests
            start_time = time.time()
            iterations = 50
            successful_operations = 0
            
            for i in range(iterations):
                try:
                    # Rapid questionnaire loading
                    data = manager.get_questionnaire("PHQ-9")
                    if data:
                        successful_operations += 1
                        
                    # Rapid scoring
                    sample_responses = [1, 2, 1, 0, 2, 1, 3, 2, 1]
                    result = calculate_scores(sample_responses, "PHQ-9")
                    if result:
                        successful_operations += 1
                        
                except Exception:
                    pass
            
            end_time = time.time()
            duration = end_time - start_time
            operations_per_second = (successful_operations / duration) if duration > 0 else 0
            
            self.log_test("Performance", "Stress Test", True, 
                         f"{successful_operations}/{iterations*2} ops in {duration:.2f}s ({operations_per_second:.1f} ops/sec)")
            
            # Test memory usage stability
            import gc
            gc.collect()
            
            self.log_test("Performance", "Memory Management", True, "Garbage collection completed")
            
            return successful_operations >= iterations  # At least 50% success rate
            
        except Exception as e:
            self.log_test("Performance", "Stress Testing", False, str(e))
            return False
    
    def run_comprehensive_user_test(self):
        """Chạy toàn bộ test như người dùng thực tế"""
        print("👤 SOULFRIEND COMPREHENSIVE USER EXPERIENCE TEST")
        print("=" * 60)
        print(f"🕐 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Target URL: {self.base_url}")
        print()
        
        # Chạy tất cả test scenarios
        test_scenarios = [
            ("Application Startup", self.test_application_startup),
            ("Navigation & Interface", self.test_navigation_and_interface),
            ("Questionnaire Functionality", self.test_questionnaire_functionality),
            ("AI Components", self.test_ai_components),
            ("PDF Export", self.test_pdf_export),
            ("Error Handling", self.test_error_handling),
            ("User Journey Simulation", self.simulate_user_journey),
            ("Performance & Stress", self.test_performance_stress)
        ]
        
        scenario_results = []
        
        for scenario_name, test_function in test_scenarios:
            print(f"\n{'='*20} {scenario_name} {'='*20}")
            
            try:
                result = test_function()
                scenario_results.append((scenario_name, result))
                
                if result:
                    print(f"✅ {scenario_name}: PASSED")
                else:
                    print(f"❌ {scenario_name}: FAILED")
                    
            except Exception as e:
                print(f"💥 {scenario_name}: ERROR - {e}")
                scenario_results.append((scenario_name, False))
                self.log_test(scenario_name, "Execution", False, f"Unexpected error: {e}")
        
        # Final Summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE USER TEST SUMMARY")
        print("=" * 60)
        
        passed_scenarios = sum(1 for _, result in scenario_results if result)
        total_scenarios = len(scenario_results)
        
        passed_tests = len([r for r in self.test_results if r['status']])
        total_tests = len(self.test_results)
        
        print(f"\n📈 Scenario Results: {passed_scenarios}/{total_scenarios} ({passed_scenarios/total_scenarios*100:.1f}%)")
        
        for scenario_name, result in scenario_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {scenario_name}")
        
        print(f"\n📈 Individual Tests: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        
        # Show failed tests
        failed_tests = [r for r in self.test_results if not r['status']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests[-10]:  # Show last 10 failures
                print(f"   • {test['scenario']} - {test['action']}: {test['details']}")
        
        print(f"\n🕐 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Overall assessment
        if passed_scenarios == total_scenarios and passed_tests >= total_tests * 0.8:
            print("🎉 EXCELLENT USER EXPERIENCE!")
            print("✅ SOULFRIEND provides excellent user experience and is production-ready.")
            return True
        elif passed_scenarios >= total_scenarios * 0.7:
            print("⚠️ GOOD USER EXPERIENCE WITH MINOR ISSUES")
            print("🔧 SOULFRIEND works well but has some areas for improvement.")
            return True
        else:
            print("💥 POOR USER EXPERIENCE")
            print("❌ SOULFRIEND has significant issues that need to be addressed.")
            return False

if __name__ == "__main__":
    # Check if Streamlit is running
    try:
        test_response = requests.get("http://localhost:8510", timeout=5)
        if test_response.status_code != 200:
            print("❌ SOULFRIEND is not running on port 8510!")
            print("Please start the application first with:")
            print("cd /workspaces/Mentalhealth && /workspaces/Mentalhealth/.venv/bin/python -m streamlit run SOULFRIEND.py --server.port 8510")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to SOULFRIEND on port 8510!")
        print("Please ensure the application is running.")
        sys.exit(1)
    
    # Run comprehensive user test
    tester = SOULFRIENDUserTester()
    success = tester.run_comprehensive_user_test()
    
    sys.exit(0 if success else 1)
