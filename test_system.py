#!/usr/bin/env python3
"""
🧪 SOULFRIEND AUTOMATED TESTING SYSTEM
Comprehensive automated testing for all system components
"""

import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime

class SOULFRIENDTestSystem:
    def __init__(self):
        self.base_path = "/workspaces/Mentalhealth"
        self.python_path = os.path.join(self.base_path, ".venv", "bin", "python")
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name, status, message=""):
        timestamp = datetime.now().strftime('%H:%M:%S')
        symbol = "✅" if status else "❌"
        print(f"[{timestamp}] {symbol} {test_name}: {message}")
        
        self.test_results.append({
            'name': test_name,
            'status': status,
            'message': message,
            'timestamp': timestamp
        })
        
        if not status:
            self.failed_tests.append(test_name)
    
    def test_imports_comprehensive(self):
        """Comprehensive import testing"""
        print("\n🧪 TESTING IMPORTS (COMPREHENSIVE)...")
        
        import_tests = [
            # Core Python imports
            ("Python Core", "import os, sys, json, time"),
            ("Data Science", "import pandas as pd, numpy as np"),
            
            # Streamlit ecosystem
            ("Streamlit Core", "import streamlit as st"),
            ("Streamlit Components", "import streamlit.components.v1 as components"),
            
            # Plotting and visualization
            ("Plotly", "import plotly.graph_objects as go, plotly.express as px"),
            ("Charts", "import matplotlib.pyplot as plt"),
            
            # PDF and reporting
            ("ReportLab", "from reportlab.lib.pagesizes import letter"),
            ("ReportLab Canvas", "from reportlab.pdfgen import canvas"),
            
            # Machine Learning (if available)
            ("Scikit-Learn", "from sklearn.ensemble import RandomForestClassifier"),
            ("Joblib", "import joblib"),
            
            # SOULFRIEND components
            ("Questionnaires", "from components.questionnaires import QuestionnaireManager, load_questionnaire"),
            ("Scoring", "from components.scoring import calculate_scores"),
            ("UI Components", "from components.ui import app_header"),
            ("Charts", "from components.charts import display_enhanced_charts"),
            ("PDF Export", "from components.pdf_export import generate_assessment_report"),
        ]
        
        # Change to base path for imports
        os.chdir(self.base_path)
        sys.path.insert(0, self.base_path)
        
        success_count = 0
        for test_name, import_statement in import_tests:
            try:
                exec(import_statement)
                self.log_test(f"Import {test_name}", True, "OK")
                success_count += 1
            except ImportError as e:
                self.log_test(f"Import {test_name}", False, f"ImportError: {e}")
            except Exception as e:
                self.log_test(f"Import {test_name}", False, f"Error: {e}")
                
        return success_count == len(import_tests)
    
    def test_data_files_comprehensive(self):
        """Comprehensive data file testing"""
        print("\n🧪 TESTING DATA FILES (COMPREHENSIVE)...")
        
        # Test all questionnaire data files
        questionnaire_files = {
            "DASS-21": ["data/dass21_vi.json", "data/dass21_enhanced_vi.json"],
            "PHQ-9": ["data/phq9_vi.json", "data/phq9_enhanced_vi.json"],
            "GAD-7": ["data/gad7_config.json", "data/gad7_enhanced_vi.json"],
            "EPDS": ["data/epds_config.json", "data/epds_enhanced_vi.json"],
            "PSS-10": ["data/pss10_config.json", "data/pss10_enhanced_vi.json"]
        }
        
        all_files_valid = True
        
        for questionnaire, files in questionnaire_files.items():
            for file_path in files:
                full_path = os.path.join(self.base_path, file_path)
                
                # Test file exists
                if os.path.exists(full_path):
                    self.log_test(f"File exists: {file_path}", True)
                    
                    # Test JSON validity
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        # Test structure
                        if isinstance(data, dict):
                            required_keys = ['questions', 'title'] if 'questions' in data else ['items', 'name']
                            missing_keys = [key for key in required_keys if key not in data]
                            
                            if not missing_keys:
                                self.log_test(f"JSON structure: {file_path}", True)
                            else:
                                self.log_test(f"JSON structure: {file_path}", False, f"Missing keys: {missing_keys}")
                                all_files_valid = False
                        else:
                            self.log_test(f"JSON format: {file_path}", False, "Not a JSON object")
                            all_files_valid = False
                            
                    except json.JSONDecodeError as e:
                        self.log_test(f"JSON validity: {file_path}", False, f"Invalid JSON: {e}")
                        all_files_valid = False
                    except Exception as e:
                        self.log_test(f"JSON read: {file_path}", False, f"Read error: {e}")
                        all_files_valid = False
                else:
                    self.log_test(f"File exists: {file_path}", False, "File not found")
                    all_files_valid = False
                    
        return all_files_valid
    
    def test_questionnaire_functionality(self):
        """Test questionnaire loading and functionality"""
        print("\n🧪 TESTING QUESTIONNAIRE FUNCTIONALITY...")
        
        try:
            os.chdir(self.base_path)
            sys.path.insert(0, self.base_path)
            
            from components.questionnaires import QuestionnaireManager, load_questionnaire
            
            # Test QuestionnaireManager
            try:
                manager = QuestionnaireManager()
                self.log_test("QuestionnaireManager creation", True)
            except Exception as e:
                self.log_test("QuestionnaireManager creation", False, str(e))
                return False
            
            # Test each questionnaire type
            questionnaire_types = ['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10']
            all_questionnaires_ok = True
            
            for q_type in questionnaire_types:
                try:
                    # Test QuestionnaireManager.get_questionnaire
                    data = manager.get_questionnaire(q_type)
                    if data:
                        self.log_test(f"Manager load: {q_type}", True)
                    else:
                        self.log_test(f"Manager load: {q_type}", False, "Empty data")
                        all_questionnaires_ok = False
                        
                    # Test load_questionnaire function
                    data2 = load_questionnaire(q_type)
                    if data2:
                        self.log_test(f"Function load: {q_type}", True)
                    else:
                        self.log_test(f"Function load: {q_type}", False, "Empty data")
                        all_questionnaires_ok = False
                        
                except Exception as e:
                    self.log_test(f"Load {q_type}", False, str(e))
                    all_questionnaires_ok = False
                    
            return all_questionnaires_ok
            
        except Exception as e:
            self.log_test("Questionnaire functionality", False, f"Setup error: {e}")
            return False
    
    def test_scoring_functionality(self):
        """Test scoring system"""
        print("\n🧪 TESTING SCORING FUNCTIONALITY...")
        
        try:
            os.chdir(self.base_path)
            sys.path.insert(0, self.base_path)
            
            from components.scoring import calculate_scores
            
            # Test scoring for each questionnaire type
            test_cases = {
                'PHQ-9': [1, 2, 1, 0, 2, 1, 3, 2, 1],
                'GAD-7': [2, 1, 3, 2, 1, 0, 2],
                'DASS-21': [1] * 21,  # 21 items
                'PSS-10': [2] * 10,   # 10 items
                'EPDS': [1, 0, 2, 1, 0, 1, 2, 1, 0, 1]  # 10 items
            }
            
            all_scoring_ok = True
            
            for questionnaire, responses in test_cases.items():
                try:
                    result = calculate_scores(responses, questionnaire)
                    
                    if result and isinstance(result, dict) and 'total_score' in result:
                        score = result['total_score']
                        self.log_test(f"Scoring {questionnaire}", True, f"Score: {score}")
                    else:
                        self.log_test(f"Scoring {questionnaire}", False, "Invalid result format")
                        all_scoring_ok = False
                        
                except Exception as e:
                    self.log_test(f"Scoring {questionnaire}", False, str(e))
                    all_scoring_ok = False
                    
            return all_scoring_ok
            
        except Exception as e:
            self.log_test("Scoring functionality", False, f"Setup error: {e}")
            return False
    
    def test_ui_components(self):
        """Test UI components"""
        print("\n🧪 TESTING UI COMPONENTS...")
        
        try:
            os.chdir(self.base_path)
            sys.path.insert(0, self.base_path)
            
            # Test UI imports
            ui_tests = [
                ("app_header", "from components.ui import app_header"),
                ("Charts", "from components.charts import display_enhanced_charts"),
                ("PDF Export", "from components.pdf_export import generate_assessment_report"),
            ]
            
            all_ui_ok = True
            
            for component_name, import_statement in ui_tests:
                try:
                    exec(import_statement)
                    self.log_test(f"UI Component: {component_name}", True)
                except Exception as e:
                    self.log_test(f"UI Component: {component_name}", False, str(e))
                    all_ui_ok = False
                    
            return all_ui_ok
            
        except Exception as e:
            self.log_test("UI components", False, f"Setup error: {e}")
            return False
    
    def test_streamlit_syntax(self):
        """Test SOULFRIEND.py syntax"""
        print("\n🧪 TESTING STREAMLIT SYNTAX...")
        
        try:
            result = subprocess.run(
                [self.python_path, "-m", "py_compile", "SOULFRIEND.py"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log_test("SOULFRIEND.py syntax", True, "Valid Python syntax")
                return True
            else:
                self.log_test("SOULFRIEND.py syntax", False, f"Syntax error: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_test("SOULFRIEND.py syntax", False, f"Compilation error: {e}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🧪 SOULFRIEND COMPREHENSIVE TESTING SYSTEM")
        print("=" * 60)
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Base Path: {self.base_path}")
        
        # Run all test suites
        test_suites = [
            ("Import Tests", self.test_imports_comprehensive),
            ("Data File Tests", self.test_data_files_comprehensive),
            ("Questionnaire Tests", self.test_questionnaire_functionality),
            ("Scoring Tests", self.test_scoring_functionality),
            ("UI Component Tests", self.test_ui_components),
            ("Syntax Tests", self.test_streamlit_syntax)
        ]
        
        suite_results = []
        
        for suite_name, test_function in test_suites:
            print(f"\n{'='*40}")
            print(f"🔍 {suite_name}")
            print(f"{'='*40}")
            
            try:
                result = test_function()
                suite_results.append((suite_name, result))
            except Exception as e:
                self.log_test(suite_name, False, f"Suite error: {e}")
                suite_results.append((suite_name, False))
        
        # Final summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        passed_suites = sum(1 for _, result in suite_results if result)
        total_suites = len(suite_results)
        
        passed_tests = len([r for r in self.test_results if r['status']])
        total_tests = len(self.test_results)
        
        print(f"\n📈 Test Suite Results: {passed_suites}/{total_suites} ({passed_suites/total_suites*100:.1f}%)")
        for suite_name, result in suite_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {suite_name}")
        
        print(f"\n📈 Individual Tests: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS ({len(self.failed_tests)}):")
            for test_name in self.failed_tests:
                print(f"   • {test_name}")
        
        print("\n" + "=" * 60)
        
        if passed_suites == total_suites:
            print("🎉 ALL TESTS PASSED!")
            print("✅ SOULFRIEND is fully tested and ready for deployment.")
            return True
        else:
            print(f"💥 {total_suites - passed_suites} TEST SUITES FAILED!")
            print("❌ Please fix issues before proceeding to deployment.")
            return False

if __name__ == "__main__":
    test_system = SOULFRIENDTestSystem()
    success = test_system.run_comprehensive_tests()
    sys.exit(0 if success else 1)
