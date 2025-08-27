#!/usr/bin/env python3
"""
Comprehensive testing suite for SOULFRIEND application
Tests all major functionality and integration
"""

import sys
import os
import json
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from components.questionnaires import load_dass21_vi as load_dass21_config
from components.scoring import score_dass21
from components.ui_advanced import (
    get_encouraging_message, 
    create_smart_recommendations,
    create_consent_agreement_form
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def run_test(self, test_name, test_func):
        """Run a single test and record results"""
        try:
            logger.info(f"Running test: {test_name}")
            test_func()
            self.tests_passed += 1
            self.test_results.append(f"✅ {test_name}: PASSED")
            logger.info(f"✅ {test_name}: PASSED")
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append(f"❌ {test_name}: FAILED - {str(e)}")
            logger.error(f"❌ {test_name}: FAILED - {str(e)}")
    
    def test_data_files_spelling(self):
        """Test that data files have correct Vietnamese spelling and formatting"""
        # Test DASS-21 config file
        dass21_path = project_root / "data" / "dass21_vi.json"
        assert dass21_path.exists(), "DASS-21 config file not found"
        
        with open(dass21_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check for proper Vietnamese diacritics in options
        options = data['options']
        expected_labels = [
            "0 - Không bao giờ",
            "1 - Thỉnh thoảng", 
            "2 - Khá thường xuyên",
            "3 - Hầu hết/luôn luôn"
        ]
        
        for i, option in enumerate(options):
            assert option['label'] == expected_labels[i], f"Option {i} has incorrect spelling: {option['label']}"
        
        # Check sample items for Vietnamese diacritics
        items = data['items']
        for item in items[:3]:  # Check first 3 items
            assert 'ô' in item['text'] or 'ế' in item['text'] or 'ỗ' in item['text'] or 'ị' in item['text'], \
                f"Item {item['id']} may have spelling issues: {item['text']}"
                
        # Check scoring note
        assert "tổng điểm" in data['scoring_note'], "Scoring note should use proper Vietnamese"
        
    def test_dass21_config_loading(self):
        """Test DASS-21 configuration loading"""
        cfg = load_dass21_config()
        assert cfg is not None, "Failed to load DASS-21 config"
        assert 'items' in cfg, "Config missing items"
        assert len(cfg['items']) == 21, f"Expected 21 items, got {len(cfg['items'])}"
        assert 'severity_thresholds' in cfg, "Config missing severity thresholds"
        
        # Check all subscales exist
        subscales = ['Depression', 'Anxiety', 'Stress']
        for subscale in subscales:
            assert subscale in cfg['severity_thresholds'], f"Missing {subscale} thresholds"
            
    def test_scoring_functionality(self):
        """Test DASS-21 scoring with various inputs"""
        cfg = load_dass21_config()
        
        # Test with all zeros (normal range) - convert list to dict
        answers_normal = {i+1: 0 for i in range(21)}
        scores = score_dass21(answers_normal, cfg)
        assert scores is not None, "Scoring failed for normal answers"
        assert all(hasattr(scores[key], 'adjusted') for key in scores), "Scores missing adjusted values"
        
        # Test with moderate scores
        answers_moderate = {i+1: 1 for i in range(21)}  # All "sometimes"
        scores = score_dass21(answers_moderate, cfg)
        assert scores is not None, "Scoring failed for moderate answers"
        
        # Test with high scores
        answers_high = {i+1: 3 for i in range(21)}  # All "always"
        scores = score_dass21(answers_high, cfg)
        assert scores is not None, "Scoring failed for high answers"
        
        # Verify score structure
        for subscale in ['Depression', 'Anxiety', 'Stress']:
            assert subscale in scores, f"Missing {subscale} in scores"
            score_obj = scores[subscale]
            assert hasattr(score_obj, 'raw'), f"{subscale} missing raw score"
            assert hasattr(score_obj, 'adjusted'), f"{subscale} missing adjusted score"
            assert hasattr(score_obj, 'severity'), f"{subscale} missing severity"
            
    def test_mood_tracker_messages(self):
        """Test encouraging message system"""
        moods = [("😊", "Vui vẻ"), ("😐", "Bình thường"), ("😔", "Buồn"), ("😰", "Lo lắng"), ("😡", "Tức giận")]
        
        for mood_value, mood_label in moods:
            message = get_encouraging_message(mood_value, mood_label)
            assert message is not None, f"No message for mood {mood_value}"
            assert len(message) > 10, f"Message too short for mood {mood_value}: {message}"
            assert any(char in message for char in "🌟💪🌈❤️🎯🍃🌸🌊🌙⭐💖🦋🌻") or len(message) > 20, f"Message should contain encouraging emoji or be meaningful: {message}"
            
    def test_recommendations_system(self):
        """Test smart recommendations"""
        # Test with dict format scores
        test_scores = {
            'Depression': {'adjusted': 20, 'severity': 'Moderate'},
            'Anxiety': {'adjusted': 15, 'severity': 'Severe'}, 
            'Stress': {'adjusted': 25, 'severity': 'Moderate'}
        }
        
        # This should not raise an exception
        try:
            create_smart_recommendations(test_scores)
        except Exception as e:
            raise AssertionError(f"Recommendations failed with dict scores: {e}")
            
        # Test with SubscaleScore objects (simulate real usage)
        from components.scoring import SubscaleScore
        test_scores_obj = {
            'Depression': SubscaleScore(raw=10, adjusted=20, severity='Moderate'),
            'Anxiety': SubscaleScore(raw=7, adjusted=14, severity='Moderate'),
            'Stress': SubscaleScore(raw=12, adjusted=24, severity='Moderate')
        }
        
        try:
            create_smart_recommendations(test_scores_obj)
        except Exception as e:
            raise AssertionError(f"Recommendations failed with SubscaleScore objects: {e}")
            
    def test_file_structure(self):
        """Test that all required files exist"""
        required_files = [
            "SOULFRIEND.py",
            "requirements.txt",
            "data/dass21_vi.json",
            "data/sample_consent_vi.md",
            "components/ui_advanced.py",
            "components/scoring.py",
            "components/questionnaires.py",
            "assets/logo.txt"
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Required file missing: {file_path}"
            
    def test_json_file_validity(self):
        """Test that JSON files are valid"""
        json_files = [
            "data/dass21_vi.json"
        ]
        
        for json_file in json_files:
            file_path = project_root / json_file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                raise AssertionError(f"Invalid JSON in {json_file}: {e}")
                
    def test_application_imports(self):
        """Test that all imports in main application work"""
        try:
            # Test main imports
            import streamlit as st
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            # Skip plotly test if not available
            
            # Test component imports
            from components.questionnaires import load_dass21_vi as load_dass21_config
            from components.scoring import score_dass21, SubscaleScore
            from components.ui_advanced import (
                create_progress_ring, create_consent_agreement_form,
                get_encouraging_message, create_smart_recommendations
            )
            
        except ImportError as e:
            raise AssertionError(f"Import error: {e}")
            
    def run_all_tests(self):
        """Run all tests and generate report"""
        logger.info("Starting comprehensive test suite...")
        
        # Data and spelling tests
        self.run_test("Data Files Spelling Check", self.test_data_files_spelling)
        self.run_test("JSON File Validity", self.test_json_file_validity)
        
        # Configuration tests  
        self.run_test("DASS-21 Config Loading", self.test_dass21_config_loading)
        
        # Core functionality tests
        self.run_test("Scoring Functionality", self.test_scoring_functionality)
        self.run_test("Mood Tracker Messages", self.test_mood_tracker_messages)
        self.run_test("Recommendations System", self.test_recommendations_system)
        
        # Infrastructure tests
        self.run_test("File Structure", self.test_file_structure)
        self.run_test("Application Imports", self.test_application_imports)
        
        # Generate report
        self.generate_report()
        
    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "="*60)
        print("🧪 COMPREHENSIVE TEST REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        print("="*60)
        
        print("\nTest Results:")
        for result in self.test_results:
            print(result)
            
        print("="*60)
        
        if self.tests_failed == 0:
            print("🎉 ALL TESTS PASSED! Application is ready for deployment.")
        else:
            print(f"⚠️  {self.tests_failed} test(s) failed. Please fix issues before deployment.")
            
        print("="*60)
        
        return success_rate

if __name__ == "__main__":
    test_suite = TestSuite()
    success_rate = test_suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success_rate == 100 else 1)
