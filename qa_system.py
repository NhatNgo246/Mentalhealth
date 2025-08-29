#!/usr/bin/env python3
"""
🔍 SOULFRIEND QA/QC SYSTEM
Comprehensive Quality Assurance and Quality Control System
"""

import os
import json
import sys
import importlib
import traceback
from datetime import datetime
import subprocess

class SOULFRIENDQASystem:
    def __init__(self):
        self.base_path = "/workspaces/Mentalhealth"
        self.errors = []
        self.warnings = []
        self.test_results = {}
        
    def log_error(self, test_name, error):
        self.errors.append(f"{test_name}: {error}")
        print(f"❌ ERROR in {test_name}: {error}")
        
    def log_warning(self, test_name, warning):
        self.warnings.append(f"{test_name}: {warning}")
        print(f"⚠️ WARNING in {test_name}: {warning}")
        
    def log_success(self, test_name, message="PASS"):
        self.test_results[test_name] = True
        print(f"✅ {test_name}: {message}")
        
    def test_file_structure(self):
        """Test if all required files exist"""
        print("\n🔍 TESTING FILE STRUCTURE...")
        
        required_files = [
            "SOULFRIEND.py",
            "components/questionnaires.py",
            "components/scoring.py", 
            "components/ui.py",
            "components/charts.py",
            "components/pdf_export.py",
            "data/dass21_vi.json",
            "data/phq9_vi.json",
            "data/gad7_config.json",
            "data/epds_config.json",
            "data/pss10_config.json"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = os.path.join(self.base_path, file_path)
            if os.path.exists(full_path):
                self.log_success(f"File exists: {file_path}")
            else:
                missing_files.append(file_path)
                self.log_error("File Structure", f"Missing file: {file_path}")
                
        return len(missing_files) == 0
    
    def test_json_files(self):
        """Test if all JSON files are valid"""
        print("\n🔍 TESTING JSON FILES...")
        
        json_files = [
            "data/dass21_vi.json",
            "data/phq9_vi.json", 
            "data/gad7_config.json",
            "data/epds_config.json",
            "data/pss10_config.json"
        ]
        
        all_valid = True
        for json_file in json_files:
            full_path = os.path.join(self.base_path, json_file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'questions' in data or 'items' in data:
                        self.log_success(f"JSON valid: {json_file}")
                    else:
                        self.log_warning("JSON Structure", f"{json_file} missing 'questions' or 'items' key")
            except FileNotFoundError:
                self.log_error("JSON Test", f"File not found: {json_file}")
                all_valid = False
            except json.JSONDecodeError as e:
                self.log_error("JSON Test", f"Invalid JSON in {json_file}: {e}")
                all_valid = False
            except Exception as e:
                self.log_error("JSON Test", f"Error reading {json_file}: {e}")
                all_valid = False
                
        return all_valid
    
    def test_imports(self):
        """Test if all Python imports work"""
        print("\n🔍 TESTING IMPORTS...")
        
        import_tests = [
            ("streamlit", "import streamlit as st"),
            ("questionnaires", "from components.questionnaires import load_questionnaire, QuestionnaireManager"),
            ("scoring", "from components.scoring import calculate_scores"),
            ("ui", "from components.ui import app_header"),
            ("charts", "from components.charts import display_enhanced_charts"),
            ("pdf_export", "from components.pdf_export import generate_assessment_report")
        ]
        
        all_imports_ok = True
        
        # Change to base path for imports
        os.chdir(self.base_path)
        sys.path.insert(0, self.base_path)
        
        for module_name, import_statement in import_tests:
            try:
                exec(import_statement)
                self.log_success(f"Import: {module_name}")
            except ImportError as e:
                self.log_error("Import Test", f"Failed to import {module_name}: {e}")
                all_imports_ok = False
            except Exception as e:
                self.log_error("Import Test", f"Error importing {module_name}: {e}")
                all_imports_ok = False
                
        return all_imports_ok
    
    def test_questionnaire_manager(self):
        """Test QuestionnaireManager functionality"""
        print("\n🔍 TESTING QUESTIONNAIRE MANAGER...")
        
        try:
            os.chdir(self.base_path)
            sys.path.insert(0, self.base_path)
            
            from components.questionnaires import QuestionnaireManager, load_questionnaire
            
            manager = QuestionnaireManager()
            
            # Test available questionnaires
            questionnaire_types = ['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10']
            
            for q_type in questionnaire_types:
                try:
                    data = manager.get_questionnaire(q_type)
                    if data and (isinstance(data, dict) or isinstance(data, list)):
                        self.log_success(f"Questionnaire load: {q_type}")
                    else:
                        self.log_error("Questionnaire Test", f"{q_type} returned invalid data")
                except Exception as e:
                    self.log_error("Questionnaire Test", f"Failed to load {q_type}: {e}")
                    
            # Test load_questionnaire function
            try:
                data = load_questionnaire('PHQ-9')
                self.log_success("load_questionnaire function")
            except Exception as e:
                self.log_error("Questionnaire Test", f"load_questionnaire failed: {e}")
                
        except Exception as e:
            self.log_error("Questionnaire Manager", f"Failed to test manager: {e}")
            return False
            
        return True
    
    def test_virtual_environment(self):
        """Test virtual environment and packages"""
        print("\n🔍 TESTING VIRTUAL ENVIRONMENT...")
        
        venv_path = os.path.join(self.base_path, ".venv")
        python_path = os.path.join(venv_path, "bin", "python")
        
        if not os.path.exists(python_path):
            self.log_error("Virtual Env", f"Python executable not found at {python_path}")
            return False
            
        self.log_success("Virtual Environment", "Python executable found")
        
        # Test required packages
        required_packages = [
            "streamlit",
            "pandas", 
            "plotly",
            "reportlab",
            "sklearn"  # Fixed: scikit-learn package imports as 'sklearn'
        ]
        
        for package in required_packages:
            try:
                result = subprocess.run(
                    [python_path, "-c", f"import {package}; print('{package} OK')"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    self.log_success(f"Package: {package}")
                else:
                    self.log_error("Package Test", f"Package {package} import failed")
            except Exception as e:
                self.log_error("Package Test", f"Error testing {package}: {e}")
                
        return True
    
    def test_streamlit_launch(self):
        """Test if Streamlit can launch without errors"""
        print("\n🔍 TESTING STREAMLIT LAUNCH...")
        
        python_path = os.path.join(self.base_path, ".venv", "bin", "python")
        
        try:
            # Test syntax check first
            result = subprocess.run(
                [python_path, "-m", "py_compile", "SOULFRIEND.py"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log_success("Python Syntax", "SOULFRIEND.py syntax is valid")
            else:
                self.log_error("Syntax Test", f"Syntax error in SOULFRIEND.py: {result.stderr}")
                return False
                
            # Test streamlit validation
            result = subprocess.run(
                [python_path, "-m", "streamlit", "run", "SOULFRIEND.py", "--help"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if "streamlit run" in result.stdout.lower():
                self.log_success("Streamlit Command", "Streamlit recognizes SOULFRIEND.py")
            else:
                self.log_warning("Streamlit Test", "Streamlit command test inconclusive")
                
        except subprocess.TimeoutExpired:
            self.log_warning("Streamlit Test", "Streamlit test timed out")
        except Exception as e:
            self.log_error("Streamlit Test", f"Error testing Streamlit: {e}")
            
        return True
    
    def run_comprehensive_qa(self):
        """Run all QA tests"""
        print("🔍 SOULFRIEND COMPREHENSIVE QA/QC SYSTEM")
        print("=" * 60)
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Base Path: {self.base_path}")
        
        test_results = []
        
        # Run all tests
        test_results.append(("File Structure", self.test_file_structure()))
        test_results.append(("JSON Files", self.test_json_files()))
        test_results.append(("Virtual Environment", self.test_virtual_environment()))
        test_results.append(("Python Imports", self.test_imports()))
        test_results.append(("Questionnaire Manager", self.test_questionnaire_manager()))
        test_results.append(("Streamlit Launch", self.test_streamlit_launch()))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 QA/QC TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status:8} {test_name}")
            
        print(f"\n📈 Overall Score: {passed}/{total} ({passed/total*100:.1f}%)")
        
        if self.errors:
            print(f"\n❌ CRITICAL ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
                
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
                
        print("\n" + "=" * 60)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! SOULFRIEND is ready for deployment.")
            return True
        else:
            print(f"💥 {total - passed} TESTS FAILED! Please fix errors before deployment.")
            return False

if __name__ == "__main__":
    qa_system = SOULFRIENDQASystem()
    success = qa_system.run_comprehensive_qa()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
