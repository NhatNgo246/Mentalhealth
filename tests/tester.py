#!/usr/bin/env python3
"""
🔧 SOULFRIEND TESTER - Kiểm tra chức năng chi tiết
==================================================
Kiểm tra từng component và chức năng của SOULFRIEND.py

Created: August 27, 2025
Purpose: Detailed functional testing for SOULFRIEND main app
"""

import sys
import os
import json
import importlib.util
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SOULFRIENDFunctionalTester:
    """🔧 Kiểm tra chức năng chi tiết"""
    
    def __init__(self):
        self.base_path = "/workspaces/Mentalhealth"
        self.app_file = f"{self.base_path}/SOULFRIEND.py"
        self.test_results = []
        
    def test_app_structure(self):
        """Kiểm tra cấu trúc ứng dụng"""
        logger.info("🔧 Testing app structure...")
        
        # Kiểm tra file chính
        if os.path.exists(self.app_file):
            self.test_results.append("✅ SOULFRIEND.py - Tồn tại")
            
            # Đọc và kiểm tra nội dung
            try:
                with open(self.app_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Kiểm tra các import quan trọng
                required_imports = [
                    "import streamlit as st",
                    "from components.ui_advanced import",
                    "from components.questionnaires import",
                    "from components.scoring import"
                ]
                
                for imp in required_imports:
                    if imp in content:
                        self.test_results.append(f"✅ Import: {imp.split('import')[1].strip()}")
                    else:
                        self.test_results.append(f"❌ Missing: {imp}")
                        
            except Exception as e:
                self.test_results.append(f"❌ Error reading SOULFRIEND.py: {e}")
        else:
            self.test_results.append("❌ SOULFRIEND.py - Không tồn tại")
            
    def test_components(self):
        """Kiểm tra components"""
        logger.info("🔧 Testing components...")
        
        components = [
            "ui.py",
            "ui_advanced.py", 
            "questionnaires.py",
            "scoring.py",
            "validation.py"
        ]
        
        components_path = f"{self.base_path}/components"
        
        for comp in components:
            comp_file = f"{components_path}/{comp}"
            if os.path.exists(comp_file):
                self.test_results.append(f"✅ Component: {comp}")
                
                # Kiểm tra syntax
                try:
                    with open(comp_file, 'r', encoding='utf-8') as f:
                        code = f.read()
                    compile(code, comp_file, 'exec')
                    self.test_results.append(f"✅ Syntax {comp}: OK")
                except SyntaxError as e:
                    self.test_results.append(f"❌ Syntax {comp}: {e}")
                except Exception as e:
                    self.test_results.append(f"❌ Error {comp}: {e}")
            else:
                self.test_results.append(f"❌ Missing: {comp}")
                
    def test_data_files(self):
        """Kiểm tra data files"""
        logger.info("🔧 Testing data files...")
        
        data_files = [
            "dass21_vi.json",
            "phq9_vi.json"
        ]
        
        data_path = f"{self.base_path}/data"
        
        for data_file in data_files:
            file_path = f"{data_path}/{data_file}"
            if os.path.exists(file_path):
                self.test_results.append(f"✅ Data: {data_file}")
                
                # Kiểm tra JSON format
                if data_file.endswith('.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            json.load(f)
                        self.test_results.append(f"✅ JSON {data_file}: Valid")
                    except json.JSONDecodeError as e:
                        self.test_results.append(f"❌ JSON {data_file}: Invalid - {e}")
            else:
                self.test_results.append(f"❌ Missing: {data_file}")
                
    def test_dependencies(self):
        """Kiểm tra dependencies"""
        logger.info("🔧 Testing dependencies...")
        
        # Đọc requirements.txt
        req_file = f"{self.base_path}/requirements.txt"
        if os.path.exists(req_file):
            self.test_results.append("✅ requirements.txt - Tồn tại")
            
            try:
                with open(req_file, 'r') as f:
                    requirements = f.read().splitlines()
                    
                # Kiểm tra các package quan trọng
                important_packages = ['streamlit', 'pandas', 'plotly']
                
                for package in important_packages:
                    found = any(package in req for req in requirements)
                    if found:
                        self.test_results.append(f"✅ Package: {package}")
                    else:
                        self.test_results.append(f"❌ Missing package: {package}")
                        
            except Exception as e:
                self.test_results.append(f"❌ Error reading requirements: {e}")
        else:
            self.test_results.append("❌ requirements.txt - Không tồn tại")
            
    def test_streamlit_config(self):
        """Kiểm tra Streamlit configuration"""
        logger.info("🔧 Testing Streamlit config...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Kiểm tra st.set_page_config
            if "st.set_page_config" in content:
                self.test_results.append("✅ Streamlit page config - Có")
                
                # Kiểm tra các tham số config
                config_params = [
                    "page_title",
                    "page_icon", 
                    "layout",
                    "initial_sidebar_state"
                ]
                
                for param in config_params:
                    if param in content:
                        self.test_results.append(f"✅ Config {param}: Có")
                    else:
                        self.test_results.append(f"❌ Config {param}: Thiếu")
            else:
                self.test_results.append("❌ Streamlit page config - Thiếu")
                
        except Exception as e:
            self.test_results.append(f"❌ Error checking config: {e}")
            
    def run_functional_tests(self):
        """Chạy tất cả functional tests"""
        logger.info("🔧 Running all functional tests...")
        
        print("\n🔧 SOULFRIEND FUNCTIONAL TESTING")
        print("=" * 40)
        
        self.test_app_structure()
        self.test_components()
        self.test_data_files()
        self.test_dependencies()
        self.test_streamlit_config()
        
        # In kết quả
        print("\n📋 TEST RESULTS:")
        print("-" * 20)
        for result in self.test_results:
            print(result)
            
        # Thống kê
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r.startswith("✅")])
        failed = total - passed
        
        print(f"\n📊 SUMMARY:")
        print(f"Total: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        return self.test_results

def main():
    """Main function"""
    tester = SOULFRIENDFunctionalTester()
    results = tester.run_functional_tests()
    
    if all(r.startswith("✅") for r in results):
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
    
    return results

if __name__ == "__main__":
    main()
