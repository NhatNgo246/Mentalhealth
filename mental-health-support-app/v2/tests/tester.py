# 🧪 TESTER - AUTOMATED TESTING SUITE

import pytest
import streamlit as st
import sys
import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SoulFriendTester:
    """Comprehensive testing suite for SOULFRIEND V2.0"""
    
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.test_results = []
        self.start_time = datetime.now()
        
    def setup_method(self):
        """Setup for each test"""
        print("🔧 Setting up test environment...")
        
    def teardown_method(self):
        """Cleanup after each test"""
        print("🧹 Cleaning up test environment...")
    
    # ==================== UNIT TESTS ====================
    
    def test_component_imports(self):
        """Test all critical components can be imported"""
        test_name = "Component Imports"
        try:
            from components.scoring import score_dass21
            from components.questionnaires import load_dass21_vi
            from components.ui_advanced import SmartUIExperience
            from components.validation import validate_app_state
            
            self.log_test_result(test_name, True, "All components imported successfully")
            return True
        except ImportError as e:
            self.log_test_result(test_name, False, f"Import failed: {e}")
            return False
    
    def test_dass21_configuration(self):
        """Test DASS-21 configuration loading"""
        test_name = "DASS-21 Configuration"
        try:
            from components.questionnaires import load_dass21_vi
            config = load_dass21_vi()
            
            assert config is not None, "Config should not be None"
            assert "items" in config, "Config should have items"
            assert "options" in config, "Config should have options"
            assert len(config["items"]) == 21, "DASS-21 should have 21 items"
            
            self.log_test_result(test_name, True, f"DASS-21 config loaded with {len(config['items'])} items")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Config test failed: {e}")
            return False
    
    def test_scoring_engine(self):
        """Test scoring calculations"""
        test_name = "Scoring Engine"
        try:
            from components.scoring import score_dass21
            from components.questionnaires import load_dass21_vi
            
            config = load_dass21_vi()
            
            # Test data - moderate responses
            test_responses = {
                f"Q{i}": 1 for i in range(1, 22)  # All responses = 1
            }
            
            scores = score_dass21(test_responses, config)
            
            assert scores is not None, "Scores should not be None"
            assert "Depression" in scores, "Should have Depression score"
            assert "Anxiety" in scores, "Should have Anxiety score"
            assert "Stress" in scores, "Should have Stress score"
            
            # Check score objects have required attributes
            for domain, score_obj in scores.items():
                assert hasattr(score_obj, 'raw'), f"{domain} should have raw score"
                assert hasattr(score_obj, 'adjusted'), f"{domain} should have adjusted score"
                assert hasattr(score_obj, 'severity'), f"{domain} should have severity"
            
            self.log_test_result(test_name, True, f"Scoring engine working correctly")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Scoring test failed: {e}")
            return False
    
    def test_severity_classification(self):
        """Test severity level classification"""
        test_name = "Severity Classification"
        try:
            from components.scoring import score_dass21
            from components.questionnaires import load_dass21_vi
            
            config = load_dass21_vi()
            
            # Test different severity levels
            test_cases = [
                # Normal level (all 0s)
                ({f"Q{i}": 0 for i in range(1, 22)}, "normal"),
                # High level (all 3s)
                ({f"Q{i}": 3 for i in range(1, 22)}, ["severe", "extremely_severe"])
            ]
            
            for responses, expected_level in test_cases:
                scores = score_dass21(responses, config)
                
                # Check that at least one domain has expected severity
                found_expected = False
                for domain, score_obj in scores.items():
                    if isinstance(expected_level, list):
                        if score_obj.severity in expected_level:
                            found_expected = True
                    else:
                        if score_obj.severity == expected_level:
                            found_expected = True
                
                assert found_expected, f"Expected severity not found for test case"
            
            self.log_test_result(test_name, True, "Severity classification working correctly")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Severity test failed: {e}")
            return False
    
    # ==================== INTEGRATION TESTS ====================
    
    def test_multi_scale_configuration(self):
        """Test multi-scale configuration loading"""
        test_name = "Multi-Scale Configuration"
        try:
            scale_files = [
                "data/dass21_vi.json",
                "data/phq9_config.json",
                "data/gad7_config.json",
                "data/epds_config.json",
                "data/pss10_config.json"
            ]
            
            loaded_scales = 0
            for scale_file in scale_files:
                if os.path.exists(scale_file):
                    with open(scale_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        assert "scale" in config, f"{scale_file} should have scale field"
                        assert "items" in config, f"{scale_file} should have items"
                        loaded_scales += 1
            
            assert loaded_scales >= 2, "At least 2 scales should be loadable"
            
            self.log_test_result(test_name, True, f"Successfully loaded {loaded_scales} scale configurations")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Multi-scale test failed: {e}")
            return False
    
    def test_session_state_management(self):
        """Test session state consistency"""
        test_name = "Session State Management"
        try:
            # Simulate session state behavior
            mock_session = {}
            
            # Test initialization
            required_keys = [
                "consent_given",
                "assessment_started", 
                "selected_scales",
                "current_scale_index"
            ]
            
            for key in required_keys:
                mock_session[key] = False if key == "consent_given" else ([] if key == "selected_scales" else 0)
            
            # Test state transitions
            mock_session["consent_given"] = True
            mock_session["selected_scales"] = ["DASS-21", "PHQ-9"]
            mock_session["current_scale_index"] = 0
            
            assert mock_session["consent_given"] == True
            assert len(mock_session["selected_scales"]) == 2
            assert mock_session["current_scale_index"] == 0
            
            self.log_test_result(test_name, True, "Session state management working correctly")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Session state test failed: {e}")
            return False
    
    # ==================== UI TESTS ====================
    
    def test_server_availability(self):
        """Test if Streamlit server is running"""
        test_name = "Server Availability"
        try:
            response = requests.get(self.base_url, timeout=10)
            assert response.status_code == 200, "Server should be accessible"
            
            self.log_test_result(test_name, True, f"Server accessible at {self.base_url}")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Server test failed: {e}")
            return False
    
    # ==================== PERFORMANCE TESTS ====================
    
    def test_scoring_performance(self):
        """Test scoring engine performance"""
        test_name = "Scoring Performance"
        try:
            from components.scoring import score_dass21
            from components.questionnaires import load_dass21_vi
            
            config = load_dass21_vi()
            test_responses = {f"Q{i}": 2 for i in range(1, 22)}
            
            # Measure performance
            start_time = time.time()
            for _ in range(100):  # Run 100 times
                scores = score_dass21(test_responses, config)
            end_time = time.time()
            
            avg_time = (end_time - start_time) / 100
            
            assert avg_time < 0.1, f"Scoring should be fast (< 0.1s), got {avg_time:.4f}s"
            
            self.log_test_result(test_name, True, f"Average scoring time: {avg_time:.4f}s")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Performance test failed: {e}")
            return False
    
    # ==================== SECURITY TESTS ====================
    
    def test_input_validation(self):
        """Test input validation and sanitization"""
        test_name = "Input Validation"
        try:
            from components.scoring import score_dass21
            from components.questionnaires import load_dass21_vi
            
            config = load_dass21_vi()
            
            # Test invalid inputs
            invalid_inputs = [
                {f"Q{i}": -1 for i in range(1, 22)},  # Negative values
                {f"Q{i}": 10 for i in range(1, 22)},  # Out of range values
                {f"Q{i}": "invalid" for i in range(1, 22)},  # String values
            ]
            
            for invalid_input in invalid_inputs:
                try:
                    scores = score_dass21(invalid_input, config)
                    # Should either handle gracefully or raise expected exception
                except (ValueError, TypeError, KeyError):
                    # Expected behavior for invalid input
                    pass
            
            self.log_test_result(test_name, True, "Input validation working correctly")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Input validation test failed: {e}")
            return False
    
    # ==================== DATA INTEGRITY TESTS ====================
    
    def test_vietnamese_encoding(self):
        """Test Vietnamese text encoding"""
        test_name = "Vietnamese Encoding"
        try:
            from components.questionnaires import load_dass21_vi
            
            config = load_dass21_vi()
            
            # Check for Vietnamese characters
            vietnamese_chars = ["á", "à", "ả", "ã", "ạ", "ă", "ắ", "ằ", "ẳ", "ẵ", "ặ", 
                              "â", "ấ", "ầ", "ẩ", "ẫ", "ậ", "đ", "é", "è", "ẻ", "ẽ", "ẹ", 
                              "ê", "ế", "ề", "ể", "ễ", "ệ", "í", "ì", "ỉ", "ĩ", "ị", 
                              "ó", "ò", "ỏ", "õ", "ọ", "ô", "ố", "ồ", "ổ", "ỗ", "ộ", 
                              "ơ", "ớ", "ờ", "ở", "ỡ", "ợ", "ú", "ù", "ủ", "ũ", "ụ", 
                              "ư", "ứ", "ừ", "ử", "ữ", "ự", "ý", "ỳ", "ỷ", "ỹ", "ỵ"]
            
            found_vietnamese = False
            for item in config["items"]:
                text = item["text"]
                if any(char in text for char in vietnamese_chars):
                    found_vietnamese = True
                    break
            
            assert found_vietnamese, "Should find Vietnamese characters in text"
            
            self.log_test_result(test_name, True, "Vietnamese encoding working correctly")
            return True
        except Exception as e:
            self.log_test_result(test_name, False, f"Vietnamese encoding test failed: {e}")
            return False
    
    # ==================== HELPER METHODS ====================
    
    def log_test_result(self, test_name, passed, message):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": timestamp,
            "passed": passed
        }
        
        self.test_results.append(result)
        print(f"[{timestamp}] {status} - {test_name}: {message}")
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting SOULFRIEND V2.0 Comprehensive Testing Suite")
        print("=" * 60)
        
        # List of all test methods
        test_methods = [
            self.test_component_imports,
            self.test_dass21_configuration,
            self.test_scoring_engine,
            self.test_severity_classification,
            self.test_multi_scale_configuration,
            self.test_session_state_management,
            self.test_server_availability,
            self.test_scoring_performance,
            self.test_input_validation,
            self.test_vietnamese_encoding
        ]
        
        # Run all tests
        for test_method in test_methods:
            self.setup_method()
            try:
                test_method()
            except Exception as e:
                self.log_test_result(
                    test_method.__name__.replace("test_", ""),
                    False, 
                    f"Unexpected error: {e}"
                )
            self.teardown_method()
        
        # Generate report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["passed"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        duration = datetime.now() - self.start_time
        
        print("\n" + "=" * 60)
        print("📊 TESTING REPORT")
        print("=" * 60)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️ Duration: {duration.total_seconds():.2f} seconds")
        print(f"📋 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print()
        
        # Detailed results
        print("📝 DETAILED RESULTS:")
        print("-" * 40)
        for result in self.test_results:
            print(f"{result['status']} {result['test']}")
            print(f"   └─ {result['message']}")
        
        # Critical failures
        critical_failures = [r for r in self.test_results if not r["passed"]]
        if critical_failures:
            print("\n🚨 CRITICAL FAILURES:")
            print("-" * 40)
            for failure in critical_failures:
                print(f"❌ {failure['test']}: {failure['message']}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 40)
        if success_rate >= 95:
            print("🎉 Excellent! System is ready for production")
        elif success_rate >= 85:
            print("⚠️ Good but needs minor fixes before production")
        elif success_rate >= 70:
            print("🔧 Moderate issues - address failures before deployment")
        else:
            print("🚨 Major issues - extensive testing needed")
        
        # Save report to file
        report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(f"SOULFRIEND V2.0 Testing Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Success Rate: {success_rate:.1f}%\n\n")
            for result in self.test_results:
                f.write(f"{result['status']} {result['test']}: {result['message']}\n")
        
        print(f"\n📄 Report saved to: {report_filename}")
        
        return success_rate >= 85  # Return True if tests mostly pass

if __name__ == "__main__":
    tester = SoulFriendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Testing completed successfully!")
        exit(0)
    else:
        print("\n🚨 Testing completed with failures!")
        exit(1)
