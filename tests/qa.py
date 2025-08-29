#!/usr/bin/env python3
"""
📋 SOULFRIEND QA - Quality Assurance System
===========================================
Kiểm tra chất lượng code và user experience

Created: August 27, 2025
Purpose: Quality assurance for SOULFRIEND.py
"""

import os
import re
import ast
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SOULFRIENDQualityAssurance:
    """📋 QA System cho SOULFRIEND"""
    
    def __init__(self):
        self.base_path = "/workspaces/Mentalhealth"
        self.app_file = f"{self.base_path}/SOULFRIEND.py"
        self.qa_results = []
        
    def check_code_quality(self):
        """Kiểm tra chất lượng code"""
        logger.info("📋 Checking code quality...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Kiểm tra docstrings
            if '"""' in content or "'''" in content:
                self.qa_results.append("✅ QA: Có docstrings")
            else:
                self.qa_results.append("❌ QA: Thiếu docstrings")
                
            # Kiểm tra comments
            comment_lines = [line for line in content.split('\n') if line.strip().startswith('#')]
            if len(comment_lines) > 5:
                self.qa_results.append(f"✅ QA: Có {len(comment_lines)} comments")
            else:
                self.qa_results.append(f"❌ QA: Quá ít comments ({len(comment_lines)})")
                
            # Kiểm tra error handling
            if 'try:' in content and 'except' in content:
                self.qa_results.append("✅ QA: Có error handling")
            else:
                self.qa_results.append("❌ QA: Thiếu error handling")
                
            # Kiểm tra logging
            if 'logging' in content and 'logger' in content:
                self.qa_results.append("✅ QA: Có logging system")
            else:
                self.qa_results.append("❌ QA: Thiếu logging")
                
        except Exception as e:
            self.qa_results.append(f"❌ QA: Error checking code quality - {e}")
            
    def check_user_experience(self):
        """Kiểm tra user experience"""
        logger.info("📋 Checking user experience...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Kiểm tra UI components
            ui_components = [
                ("Progress indicator", "progress"),
                ("Loading states", "spinner"),
                ("Success messages", "success"),
                ("Error messages", "error"),
                ("Help text", "help")
            ]
            
            for comp_name, keyword in ui_components:
                if keyword in content.lower():
                    self.qa_results.append(f"✅ QA UX: {comp_name}")
                else:
                    self.qa_results.append(f"❌ QA UX: Thiếu {comp_name}")
                    
            # Kiểm tra responsive design
            if "layout=" in content:
                self.qa_results.append("✅ QA UX: Có responsive layout")
            else:
                self.qa_results.append("❌ QA UX: Thiếu responsive design")
                
            # Kiểm tra accessibility
            accessibility_features = [
                ("Alt text", "alt="),
                ("Labels", "label="),
                ("Help text", "help=")
            ]
            
            for feature_name, keyword in accessibility_features:
                if keyword in content:
                    self.qa_results.append(f"✅ QA A11Y: {feature_name}")
                else:
                    self.qa_results.append(f"❌ QA A11Y: Thiếu {feature_name}")
                    
        except Exception as e:
            self.qa_results.append(f"❌ QA UX: Error checking UX - {e}")
            
    def check_performance(self):
        """Kiểm tra performance"""
        logger.info("📋 Checking performance...")
        
        try:
            # Kiểm tra file size
            file_size = os.path.getsize(self.app_file)
            size_kb = file_size / 1024
            
            if size_kb < 500:  # < 500KB
                self.qa_results.append(f"✅ QA PERF: File size OK ({size_kb:.1f}KB)")
            elif size_kb < 1000:  # < 1MB
                self.qa_results.append(f"⚠️ QA PERF: File size lớn ({size_kb:.1f}KB)")
            else:
                self.qa_results.append(f"❌ QA PERF: File size quá lớn ({size_kb:.1f}KB)")
                
            # Kiểm tra complexity
            with open(self.app_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Đếm functions
            func_count = len([line for line in lines if line.strip().startswith('def ')])
            if func_count < 20:
                self.qa_results.append(f"✅ QA PERF: Function count OK ({func_count})")
            else:
                self.qa_results.append(f"❌ QA PERF: Quá nhiều functions ({func_count})")
                
            # Kiểm tra imports
            import_lines = [line for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
            if len(import_lines) < 15:
                self.qa_results.append(f"✅ QA PERF: Import count OK ({len(import_lines)})")
            else:
                self.qa_results.append(f"❌ QA PERF: Quá nhiều imports ({len(import_lines)})")
                
        except Exception as e:
            self.qa_results.append(f"❌ QA PERF: Error checking performance - {e}")
            
    def check_security(self):
        """Kiểm tra bảo mật"""
        logger.info("📋 Checking security...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Kiểm tra hardcoded secrets
            security_issues = [
                ("Password hardcoded", "password ="),
                ("API key hardcoded", "api_key ="),
                ("Secret hardcoded", "secret ="),
                ("Token hardcoded", "token =")
            ]
            
            for issue_name, pattern in security_issues:
                if pattern.lower() in content.lower():
                    self.qa_results.append(f"❌ QA SEC: {issue_name}")
                else:
                    self.qa_results.append(f"✅ QA SEC: Không có {issue_name}")
                    
            # Kiểm tra input validation
            if "validate" in content.lower():
                self.qa_results.append("✅ QA SEC: Có input validation")
            else:
                self.qa_results.append("❌ QA SEC: Thiếu input validation")
                
            # Kiểm tra safe file operations
            if "with open" in content:
                self.qa_results.append("✅ QA SEC: Safe file operations")
            else:
                self.qa_results.append("❌ QA SEC: Unsafe file operations")
                
        except Exception as e:
            self.qa_results.append(f"❌ QA SEC: Error checking security - {e}")
            
    def check_data_handling(self):
        """Kiểm tra xử lý dữ liệu"""
        logger.info("📋 Checking data handling...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Kiểm tra data validation
            data_checks = [
                ("JSON handling", "json."),
                ("Pandas usage", "pd."),
                ("Session state", "st.session_state"),
                ("Data persistence", "save" in content.lower() or "store" in content.lower())
            ]
            
            for check_name, condition in data_checks:
                if isinstance(condition, str) and condition in content:
                    self.qa_results.append(f"✅ QA DATA: {check_name}")
                elif isinstance(condition, bool) and condition:
                    self.qa_results.append(f"✅ QA DATA: {check_name}")
                else:
                    self.qa_results.append(f"❌ QA DATA: Thiếu {check_name}")
                    
            # Kiểm tra error handling cho data
            if "try:" in content and ("json.load" in content or "pd.read" in content):
                self.qa_results.append("✅ QA DATA: Có error handling cho data")
            else:
                self.qa_results.append("❌ QA DATA: Thiếu error handling cho data")
                
        except Exception as e:
            self.qa_results.append(f"❌ QA DATA: Error checking data handling - {e}")
            
    def run_qa_analysis(self):
        """Chạy tất cả QA analysis"""
        logger.info("📋 Running complete QA analysis...")
        
        print("\n📋 SOULFRIEND QUALITY ASSURANCE")
        print("=" * 45)
        
        self.check_code_quality()
        self.check_user_experience()
        self.check_performance()
        self.check_security()
        self.check_data_handling()
        
        # In kết quả
        print("\n📋 QA RESULTS:")
        print("-" * 15)
        for result in self.qa_results:
            print(result)
            
        # Thống kê
        total = len(self.qa_results)
        passed = len([r for r in self.qa_results if r.startswith("✅")])
        warnings = len([r for r in self.qa_results if r.startswith("⚠️")])
        failed = len([r for r in self.qa_results if r.startswith("❌")])
        
        print(f"\n📊 QA SUMMARY:")
        print(f"Total checks: {total}")
        print(f"Passed: {passed}")
        print(f"Warnings: {warnings}")
        print(f"Failed: {failed}")
        print(f"Quality score: {(passed/total)*100:.1f}%")
        
        # Đánh giá chung
        if failed == 0:
            print("\n✨ QUALITY: EXCELLENT")
        elif failed <= 3:
            print("\n👍 QUALITY: GOOD")
        elif failed <= 6:
            print("\n⚠️ QUALITY: NEEDS IMPROVEMENT")
        else:
            print("\n❌ QUALITY: POOR")
            
        return self.qa_results

def main():
    """Main function"""
    qa = SOULFRIENDQualityAssurance()
    results = qa.run_qa_analysis()
    return results

if __name__ == "__main__":
    main()
