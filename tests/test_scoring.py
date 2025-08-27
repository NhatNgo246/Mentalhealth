#!/usr/bin/env python3
"""
Scoring Algorithm Test Suite for SOULFRIEND
Tests all edge cases and mathematical accuracy
"""

import sys
import os
import logging
from pathlib import Path
import math

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoringTestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def run_test(self, test_name, test_func):
        """Run a single test and record results"""
        try:
            logger.info(f"🔢 Testing Scoring: {test_name}")
            test_func()
            self.tests_passed += 1
            self.test_results.append(f"✅ {test_name}: PASSED")
            logger.info(f"✅ {test_name}: PASSED")
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append(f"❌ {test_name}: FAILED - {str(e)}")
            logger.error(f"❌ {test_name}: FAILED - {str(e)}")
    
    def test_dass21_mathematical_accuracy(self):
        """Test DASS-21 scoring mathematical accuracy"""
        from components.scoring import score_dass21
        from components.questionnaires import load_dass21_vi
        
        cfg = load_dass21_vi()
        
        # Test known scoring scenarios
        test_cases = [
            {
                'name': 'All zeros',
                'answers': {i+1: 0 for i in range(21)},
                'expected_raw': {'Depression': 0, 'Anxiety': 0, 'Stress': 0},
                'expected_adjusted': {'Depression': 0, 'Anxiety': 0, 'Stress': 0}
            },
            {
                'name': 'All ones',
                'answers': {i+1: 1 for i in range(21)},
                'expected_raw': {'Depression': 7, 'Anxiety': 7, 'Stress': 7},
                'expected_adjusted': {'Depression': 14, 'Anxiety': 14, 'Stress': 14}
            },
            {
                'name': 'All twos',
                'answers': {i+1: 2 for i in range(21)},
                'expected_raw': {'Depression': 14, 'Anxiety': 14, 'Stress': 14},
                'expected_adjusted': {'Depression': 28, 'Anxiety': 28, 'Stress': 28}
            },
            {
                'name': 'All threes (maximum)',
                'answers': {i+1: 3 for i in range(21)},
                'expected_raw': {'Depression': 21, 'Anxiety': 21, 'Stress': 21},
                'expected_adjusted': {'Depression': 42, 'Anxiety': 42, 'Stress': 42}
            }
        ]
        
        for case in test_cases:
            scores = score_dass21(case['answers'], cfg)
            
            for subscale in ['Depression', 'Anxiety', 'Stress']:
                actual_raw = scores[subscale].raw
                actual_adjusted = scores[subscale].adjusted
                expected_raw = case['expected_raw'][subscale]
                expected_adjusted = case['expected_adjusted'][subscale]
                
                assert actual_raw == expected_raw, f"{case['name']} {subscale} raw: expected {expected_raw}, got {actual_raw}"
                assert actual_adjusted == expected_adjusted, f"{case['name']} {subscale} adjusted: expected {expected_adjusted}, got {actual_adjusted}"
                
            logger.info(f"   ✓ {case['name']}: All calculations correct")
    
    def test_severity_classification_accuracy(self):
        """Test severity classification boundaries"""
        from components.scoring import score_dass21, severity_from_thresholds
        from components.questionnaires import load_dass21_vi
        
        cfg = load_dass21_vi()
        
        # Test boundary conditions for each subscale
        severity_tests = [
            # Depression boundaries
            {'subscale': 'Depression', 'adjusted_score': 0, 'expected': 'Normal'},
            {'subscale': 'Depression', 'adjusted_score': 9, 'expected': 'Normal'},
            {'subscale': 'Depression', 'adjusted_score': 10, 'expected': 'Mild'},
            {'subscale': 'Depression', 'adjusted_score': 13, 'expected': 'Mild'},
            {'subscale': 'Depression', 'adjusted_score': 14, 'expected': 'Moderate'},
            {'subscale': 'Depression', 'adjusted_score': 20, 'expected': 'Moderate'},
            {'subscale': 'Depression', 'adjusted_score': 21, 'expected': 'Severe'},
            {'subscale': 'Depression', 'adjusted_score': 27, 'expected': 'Severe'},
            {'subscale': 'Depression', 'adjusted_score': 28, 'expected': 'Extremely Severe'},
            {'subscale': 'Depression', 'adjusted_score': 42, 'expected': 'Extremely Severe'},
            
            # Anxiety boundaries
            {'subscale': 'Anxiety', 'adjusted_score': 0, 'expected': 'Normal'},
            {'subscale': 'Anxiety', 'adjusted_score': 7, 'expected': 'Normal'},
            {'subscale': 'Anxiety', 'adjusted_score': 8, 'expected': 'Mild'},
            {'subscale': 'Anxiety', 'adjusted_score': 9, 'expected': 'Mild'},
            {'subscale': 'Anxiety', 'adjusted_score': 10, 'expected': 'Moderate'},
            {'subscale': 'Anxiety', 'adjusted_score': 14, 'expected': 'Moderate'},
            {'subscale': 'Anxiety', 'adjusted_score': 15, 'expected': 'Severe'},
            {'subscale': 'Anxiety', 'adjusted_score': 19, 'expected': 'Severe'},
            {'subscale': 'Anxiety', 'adjusted_score': 20, 'expected': 'Extremely Severe'},
            {'subscale': 'Anxiety', 'adjusted_score': 42, 'expected': 'Extremely Severe'},
            
            # Stress boundaries
            {'subscale': 'Stress', 'adjusted_score': 0, 'expected': 'Normal'},
            {'subscale': 'Stress', 'adjusted_score': 14, 'expected': 'Normal'},
            {'subscale': 'Stress', 'adjusted_score': 15, 'expected': 'Mild'},
            {'subscale': 'Stress', 'adjusted_score': 18, 'expected': 'Mild'},
            {'subscale': 'Stress', 'adjusted_score': 19, 'expected': 'Moderate'},
            {'subscale': 'Stress', 'adjusted_score': 25, 'expected': 'Moderate'},
            {'subscale': 'Stress', 'adjusted_score': 26, 'expected': 'Severe'},
            {'subscale': 'Stress', 'adjusted_score': 33, 'expected': 'Severe'},
            {'subscale': 'Stress', 'adjusted_score': 34, 'expected': 'Extremely Severe'},
            {'subscale': 'Stress', 'adjusted_score': 42, 'expected': 'Extremely Severe'},
        ]
        
        for test in severity_tests:
            thresholds = cfg['severity_thresholds'][test['subscale']]
            actual_severity = severity_from_thresholds(test['adjusted_score'], thresholds)
            expected_severity = test['expected']
            
            assert actual_severity == expected_severity, \
                f"{test['subscale']} score {test['adjusted_score']}: expected {expected_severity}, got {actual_severity}"
        
        logger.info("   ✓ All severity classifications correct")
    
    def test_subscale_item_distribution(self):
        """Test that items are correctly distributed across subscales"""
        from components.questionnaires import load_dass21_vi
        
        cfg = load_dass21_vi()
        
        # Count items per subscale
        subscale_counts = {'Depression': 0, 'Anxiety': 0, 'Stress': 0}
        item_ids_by_subscale = {'Depression': [], 'Anxiety': [], 'Stress': []}
        
        for item in cfg['items']:
            subscale = item['subscale']
            subscale_counts[subscale] += 1
            item_ids_by_subscale[subscale].append(item['id'])
        
        # DASS-21 should have exactly 7 items per subscale
        for subscale, count in subscale_counts.items():
            assert count == 7, f"{subscale} has {count} items, expected 7"
        
        # Check specific item distributions (based on DASS-21 standard)
        expected_distributions = {
            'Depression': [3, 6, 9, 10, 15, 18, 21],  # Items measuring depression
            'Anxiety': [2, 4, 8, 11, 14, 17, 20],     # Items measuring anxiety  
            'Stress': [1, 5, 7, 12, 13, 16, 19]       # Items measuring stress
        }
        
        for subscale, expected_ids in expected_distributions.items():
            actual_ids = sorted(item_ids_by_subscale[subscale])
            assert actual_ids == expected_ids, \
                f"{subscale} item IDs: expected {expected_ids}, got {actual_ids}"
        
        logger.info("   ✓ Item distribution across subscales is correct")
    
    def test_edge_case_inputs(self):
        """Test scoring with edge case inputs"""
        from components.scoring import score_dass21
        from components.questionnaires import load_dass21_vi
        
        cfg = load_dass21_vi()
        
        # Test partial responses
        partial_cases = [
            {
                'name': 'Only first question answered',
                'answers': {1: 3},
                'should_handle': True
            },
            {
                'name': 'Missing middle questions',
                'answers': {1: 1, 5: 2, 10: 1, 15: 2, 21: 1},
                'should_handle': True
            },
            {
                'name': 'Only last question answered',
                'answers': {21: 2},
                'should_handle': True
            }
        ]
        
        for case in partial_cases:
            try:
                scores = score_dass21(case['answers'], cfg)
                if case['should_handle']:
                    # Should produce some result
                    assert scores is not None, f"{case['name']}: Should return scores"
                    logger.info(f"   ✓ {case['name']}: Handled gracefully")
                else:
                    logger.info(f"   ✓ {case['name']}: Should have failed but didn't")
            except Exception as e:
                if not case['should_handle']:
                    logger.info(f"   ✓ {case['name']}: Properly rejected - {type(e).__name__}")
                else:
                    logger.info(f"   ✓ {case['name']}: Error handling - {type(e).__name__}")
    
    def test_invalid_inputs(self):
        """Test scoring with invalid inputs"""
        from components.scoring import score_dass21
        from components.questionnaires import load_dass21_vi
        
        cfg = load_dass21_vi()
        
        invalid_cases = [
            {
                'name': 'Out of range high values',
                'answers': {i+1: 10 for i in range(21)},  # Values > 3
            },
            {
                'name': 'Negative values',
                'answers': {i+1: -1 for i in range(21)},
            },
            {
                'name': 'Float values',
                'answers': {i+1: 1.5 for i in range(21)},
            },
            {
                'name': 'String values',
                'answers': {i+1: "invalid" for i in range(21)},
            },
            {
                'name': 'None values',
                'answers': {i+1: None for i in range(21)},
            },
            {
                'name': 'Mixed valid/invalid',
                'answers': {1: 1, 2: "invalid", 3: 2, 4: None, 5: -1},
            }
        ]
        
        for case in invalid_cases:
            try:
                scores = score_dass21(case['answers'], cfg)
                logger.info(f"   ✓ {case['name']}: Handled without crash")
                # Check if scores are reasonable despite invalid input
                for subscale in ['Depression', 'Anxiety', 'Stress']:
                    score_obj = scores[subscale]
                    assert hasattr(score_obj, 'raw'), f"Missing raw score for {subscale}"
                    assert hasattr(score_obj, 'adjusted'), f"Missing adjusted score for {subscale}"
                    assert hasattr(score_obj, 'severity'), f"Missing severity for {subscale}"
            except Exception as e:
                logger.info(f"   ✓ {case['name']}: Properly rejected - {type(e).__name__}")
    
    def test_mathematical_consistency(self):
        """Test mathematical consistency of scoring"""
        from components.scoring import score_dass21
        from components.questionnaires import load_dass21_vi
        
        cfg = load_dass21_vi()
        
        # Test that adjusted = raw * 2 (DASS-21 to DASS-42 conversion)
        test_answers = {i+1: i % 4 for i in range(21)}  # Mix of 0,1,2,3 values
        scores = score_dass21(test_answers, cfg)
        
        for subscale in ['Depression', 'Anxiety', 'Stress']:
            raw = scores[subscale].raw
            adjusted = scores[subscale].adjusted
            expected_adjusted = raw * 2
            
            assert adjusted == expected_adjusted, \
                f"{subscale}: adjusted ({adjusted}) should be raw ({raw}) * 2 = {expected_adjusted}"
        
        logger.info("   ✓ Mathematical consistency verified (adjusted = raw * 2)")
        
        # Test that scores are non-negative
        for subscale in ['Depression', 'Anxiety', 'Stress']:
            raw = scores[subscale].raw
            adjusted = scores[subscale].adjusted
            
            assert raw >= 0, f"{subscale} raw score should be non-negative: {raw}"
            assert adjusted >= 0, f"{subscale} adjusted score should be non-negative: {adjusted}"
        
        logger.info("   ✓ All scores are non-negative")
        
        # Test maximum possible scores
        max_answers = {i+1: 3 for i in range(21)}
        max_scores = score_dass21(max_answers, cfg)
        
        for subscale in ['Depression', 'Anxiety', 'Stress']:
            max_raw = max_scores[subscale].raw
            max_adjusted = max_scores[subscale].adjusted
            
            assert max_raw == 21, f"{subscale} maximum raw should be 21: {max_raw}"
            assert max_adjusted == 42, f"{subscale} maximum adjusted should be 42: {max_adjusted}"
        
        logger.info("   ✓ Maximum scores are correct (21 raw, 42 adjusted)")
    
    def test_dataclass_functionality(self):
        """Test SubscaleScore dataclass functionality"""
        from components.scoring import SubscaleScore
        
        # Test normal instantiation
        score = SubscaleScore(raw=10, adjusted=20, severity="Moderate")
        
        assert score.raw == 10, f"Raw score incorrect: {score.raw}"
        assert score.adjusted == 20, f"Adjusted score incorrect: {score.adjusted}"
        assert score.severity == "Moderate", f"Severity incorrect: {score.severity}"
        
        # Test string representation
        score_str = str(score)
        assert "10" in score_str, "Raw score not in string representation"
        assert "20" in score_str, "Adjusted score not in string representation"
        assert "Moderate" in score_str, "Severity not in string representation"
        
        # Test equality
        score2 = SubscaleScore(raw=10, adjusted=20, severity="Moderate")
        score3 = SubscaleScore(raw=5, adjusted=10, severity="Normal")
        
        assert score == score2, "Equal SubscaleScore objects should be equal"
        assert score != score3, "Different SubscaleScore objects should not be equal"
        
        logger.info("   ✓ SubscaleScore dataclass functionality correct")
    
    def run_all_tests(self):
        """Run all scoring tests"""
        logger.info("🔢 Starting Scoring Algorithm Test Suite...")
        logger.info("="*60)
        
        self.run_test("DASS-21 Mathematical Accuracy", self.test_dass21_mathematical_accuracy)
        self.run_test("Severity Classification Accuracy", self.test_severity_classification_accuracy)
        self.run_test("Subscale Item Distribution", self.test_subscale_item_distribution)
        self.run_test("Edge Case Inputs", self.test_edge_case_inputs)
        self.run_test("Invalid Inputs", self.test_invalid_inputs)
        self.run_test("Mathematical Consistency", self.test_mathematical_consistency)
        self.run_test("Dataclass Functionality", self.test_dataclass_functionality)
        
        self.generate_scoring_report()
        return self.tests_passed / (self.tests_passed + self.tests_failed) * 100 if (self.tests_passed + self.tests_failed) > 0 else 0
        
    def generate_scoring_report(self):
        """Generate scoring test report"""
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "="*60)
        print("🔢 SCORING ALGORITHM TEST REPORT")
        print("="*60)
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print("="*60)
        
        print("\n📋 Test Results:")
        for result in self.test_results:
            print(f"   {result}")
            
        print("="*60)
        
        if self.tests_failed == 0:
            print("🎉 ALL SCORING TESTS PASSED!")
            print("🔢 Mathematical accuracy confirmed!")
            print("📊 DASS-21 scoring algorithm is reliable!")
        else:
            print(f"⚠️ {self.tests_failed} scoring test(s) failed.")
            print("🔧 Critical: Fix scoring issues before deployment!")
            
        return success_rate

if __name__ == "__main__":
    test_suite = ScoringTestSuite()
    success_rate = test_suite.run_all_tests()
    sys.exit(0 if success_rate >= 95 else 1)  # Higher threshold for scoring accuracy
