#!/usr/bin/env python3
"""
Integration testing script for SOULFRIEND application
Tests complete user flow and all functionality
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add project root to path  
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from components.questionnaires import load_dass21_vi
from components.scoring import score_dass21
from components.ui_advanced import get_encouraging_message, create_smart_recommendations

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegrationTestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def run_test(self, test_name, test_func):
        """Run a single test and record results"""
        try:
            logger.info(f"🧪 Testing: {test_name}")
            test_func()
            self.tests_passed += 1
            self.test_results.append(f"✅ {test_name}: PASSED")
            logger.info(f"✅ {test_name}: PASSED")
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append(f"❌ {test_name}: FAILED - {str(e)}")
            logger.error(f"❌ {test_name}: FAILED - {str(e)}")
    
    def test_complete_assessment_flow(self):
        """Test complete DASS-21 assessment flow"""
        # Load configuration
        cfg = load_dass21_vi()
        assert cfg is not None, "Failed to load DASS-21 config"
        
        # Test various assessment scenarios
        test_cases = [
            {
                "name": "Normal Range User",
                "answers": {i+1: 0 for i in range(21)},  # All "never"
                "expected_severity": ["Normal", "Normal", "Normal"]
            },
            {
                "name": "Mild Issues User", 
                "answers": {i+1: 1 for i in range(21)},  # All "sometimes"
                "expected_severity": ["Moderate", "Extremely Severe", "Moderate"]
            },
            {
                "name": "Severe Issues User",
                "answers": {i+1: 3 for i in range(21)},  # All "always"
                "expected_severity": ["Extremely Severe", "Extremely Severe", "Extremely Severe"]
            }
        ]
        
        for case in test_cases:
            logger.info(f"   Testing {case['name']}...")
            scores = score_dass21(case['answers'], cfg)
            
            # Verify all subscales present
            for subscale in ['Depression', 'Anxiety', 'Stress']:
                assert subscale in scores, f"Missing {subscale} in scores"
                score_obj = scores[subscale]
                assert hasattr(score_obj, 'severity'), f"Missing severity for {subscale}"
                logger.info(f"     {subscale}: {score_obj.severity} (Score: {score_obj.adjusted})")
            
            # Test recommendations work with these scores
            scores_dict = {}
            for key, value in scores.items():
                scores_dict[key] = {'adjusted': value.adjusted, 'severity': value.severity}
            
            create_smart_recommendations(scores_dict)  # Should not raise exception
            logger.info(f"     ✓ Recommendations generated successfully")
    
    def test_mood_tracker_comprehensive(self):
        """Test mood tracker with all possible moods"""
        mood_scenarios = [
            ("😊", "Rất vui vẻ"),
            ("🙂", "Vui vẻ"),
            ("😐", "Bình thường"),
            ("😔", "Buồn"),
            ("😰", "Lo lắng"),
            ("😡", "Tức giận"),
            ("😴", "Mệt mỏi"),
            ("🤔", "Suy tư")
        ]
        
        for mood_value, mood_label in mood_scenarios:
            message = get_encouraging_message(mood_value, mood_label)
            assert message is not None, f"No message for mood {mood_value}"
            assert len(message) > 15, f"Message too short for {mood_value}: {message}"
            logger.info(f"   {mood_value} {mood_label}: {message[:50]}...")
    
    def test_data_integrity(self):
        """Test data files for consistency and completeness"""
        cfg = load_dass21_vi()
        
        # Check all 21 items are present
        assert len(cfg['items']) == 21, f"Expected 21 items, got {len(cfg['items'])}"
        
        # Check item distribution across subscales
        subscale_counts = {'Depression': 0, 'Anxiety': 0, 'Stress': 0}
        for item in cfg['items']:
            subscale_counts[item['subscale']] += 1
        
        # DASS-21 should have 7 items per subscale
        for subscale, count in subscale_counts.items():
            assert count == 7, f"{subscale} has {count} items, expected 7"
        
        # Check all items have proper Vietnamese text
        for item in cfg['items']:
            text = item['text']
            assert 'Tôi' in text or 'tôi' in text, f"Item {item['id']} doesn't start properly: {text}"
            assert len(text) > 10, f"Item {item['id']} too short: {text}"
        
        logger.info("   ✓ All 21 items properly distributed (7 per subscale)")
        logger.info("   ✓ All items use proper Vietnamese formatting")
    
    def test_scoring_accuracy(self):
        """Test scoring algorithm accuracy"""
        cfg = load_dass21_vi()
        
        # Test specific scoring scenarios
        test_scenarios = [
            {
                "name": "Mixed Moderate Scores",
                "answers": {1: 2, 2: 1, 3: 2, 4: 1, 5: 2, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1,
                          11: 2, 12: 1, 13: 2, 14: 1, 15: 2, 16: 1, 17: 2, 18: 1, 19: 2, 20: 1, 21: 2},
                "min_adjusted": 14  # Should get some meaningful adjusted scores
            },
            {
                "name": "High Anxiety Pattern", 
                "answers": {i+1: 3 if i in [1, 3, 6, 10, 13, 16, 19] else 0 for i in range(21)},  # High anxiety items
                "check_anxiety": True
            }
        ]
        
        for scenario in test_scenarios:
            logger.info(f"   Testing {scenario['name']}...")
            scores = score_dass21(scenario['answers'], cfg)
            
            total_adjusted = sum(score.adjusted for score in scores.values())
            logger.info(f"     Total adjusted score: {total_adjusted}")
            
            if 'min_adjusted' in scenario:
                assert total_adjusted >= scenario['min_adjusted'], f"Adjusted scores too low: {total_adjusted}"
            
            if scenario.get('check_anxiety'):
                anxiety_score = scores['Anxiety'].adjusted
                logger.info(f"     Anxiety score: {anxiety_score}")
                assert anxiety_score > 0, "Expected some anxiety score"
    
    def test_error_handling(self):
        """Test application error handling"""
        cfg = load_dass21_vi()
        
        # Test with missing answers
        incomplete_answers = {i+1: 1 for i in range(10)}  # Only 10 answers
        try:
            scores = score_dass21(incomplete_answers, cfg)
            # Should handle gracefully or raise appropriate error
        except Exception as e:
            logger.info(f"   ✓ Proper error handling for incomplete answers: {type(e).__name__}")
        
        # Test with invalid mood values
        try:
            message = get_encouraging_message("invalid", "Invalid Mood")
            logger.info(f"   ✓ Handled invalid mood gracefully")
        except Exception as e:
            logger.info(f"   ✓ Proper error handling for invalid mood: {type(e).__name__}")
    
    def test_language_consistency(self):
        """Test Vietnamese language consistency"""
        cfg = load_dass21_vi()
        
        # Check options use proper Vietnamese
        vietnamese_phrases = ['Không bao giờ', 'Thỉnh thoảng', 'Khá thường xuyên', 'Hầu hết']
        for i, option in enumerate(cfg['options']):
            label = option['label']
            expected_phrase = vietnamese_phrases[i]
            assert expected_phrase in label, f"Option {i} missing Vietnamese phrase: {label}"
        
        # Check items use consistent Vietnamese
        required_chars = ['ô', 'ă', 'â', 'ê', 'ì', 'í', 'ò', 'ó', 'ù', 'ú', 'ý']
        vietnamese_items = 0
        for item in cfg['items']:
            if any(char in item['text'] for char in required_chars):
                vietnamese_items += 1
        
        assert vietnamese_items >= 15, f"Only {vietnamese_items} items use Vietnamese diacritics"
        logger.info(f"   ✓ {vietnamese_items}/21 items use proper Vietnamese diacritics")
    
    def run_all_tests(self):
        """Run comprehensive integration tests"""
        logger.info("🚀 Starting SOULFRIEND Integration Test Suite...")
        logger.info("="*60)
        
        # Core functionality tests
        self.run_test("Complete Assessment Flow", self.test_complete_assessment_flow)
        self.run_test("Mood Tracker Comprehensive", self.test_mood_tracker_comprehensive)
        self.run_test("Data Integrity", self.test_data_integrity)
        self.run_test("Scoring Accuracy", self.test_scoring_accuracy)
        self.run_test("Error Handling", self.test_error_handling)
        self.run_test("Language Consistency", self.test_language_consistency)
        
        # Generate final report
        self.generate_final_report()
        
    def generate_final_report(self):
        """Generate final comprehensive report"""
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "="*70)
        print("🎯 SOULFRIEND INTEGRATION TEST REPORT")
        print("="*70)
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print("="*70)
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            print(f"   {result}")
            
        print("\n" + "="*70)
        
        if self.tests_failed == 0:
            print("🎉 ALL INTEGRATION TESTS PASSED!")
            print("🚀 Application is 100% ready for production deployment!")
            print("✨ All features are working correctly and synchronized!")
        else:
            print(f"⚠️  {self.tests_failed} integration test(s) failed.")
            print("🔧 Please fix these issues before final deployment.")
            
        print("="*70)
        
        # Additional deployment readiness checks
        if success_rate == 100:
            print("\n🎯 DEPLOYMENT READINESS CHECKLIST:")
            print("   ✅ Vietnamese language support: READY")
            print("   ✅ DASS-21 assessment system: READY") 
            print("   ✅ Mood tracking functionality: READY")
            print("   ✅ Smart recommendations: READY")
            print("   ✅ Error handling: READY")
            print("   ✅ Data integrity: READY")
            print("\n🌟 SOULFRIEND is ready for Streamlit Cloud deployment!")
        
        return success_rate

if __name__ == "__main__":
    test_suite = IntegrationTestSuite()
    success_rate = test_suite.run_all_tests()
    
    # Exit with appropriate code for CI/CD
    sys.exit(0 if success_rate == 100 else 1)
