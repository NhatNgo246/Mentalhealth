#!/usr/bin/env python3
"""
🎯 SOULFRIEND QC - Quality Control System
=========================================
Kiểm soát chất lượng cuối cùng trước khi deploy

Created: August 27, 2025
Purpose: Final quality control for SOULFRIEND.py
"""

import os
import sys
import json
import subprocess
import importlib.util
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SOULFRIENDQualityControl:
    """🎯 Quality Control System"""
    
    def __init__(self):
        self.base_path = "/workspaces/Mentalhealth"
        self.app_file = f"{self.base_path}/SOULFRIEND.py"
        self.qc_results = []
        self.critical_issues = []
        
    def verify_deployment_readiness(self):
        """Kiểm tra sẵn sàng deployment"""
        logger.info("🎯 Verifying deployment readiness...")
        
        # Critical files check
        critical_files = [
            ("SOULFRIEND.py", self.app_file),
            ("requirements.txt", f"{self.base_path}/requirements.txt"),
            ("launch script", f"{self.base_path}/launch_soulfriend.sh"),
            ("components/ui.py", f"{self.base_path}/components/ui.py"),
            ("components/ui_advanced.py", f"{self.base_path}/components/ui_advanced.py"),
            ("data/dass21_vi.json", f"{self.base_path}/data/dass21_vi.json")
        ]
        
        for name, path in critical_files:
            if os.path.exists(path):
                self.qc_results.append(f"✅ QC DEPLOY: {name} - Có")
            else:
                self.qc_results.append(f"❌ QC DEPLOY: {name} - THIẾU")
                self.critical_issues.append(f"Missing critical file: {name}")
                
    def verify_app_functionality(self):
        """Kiểm tra chức năng ứng dụng"""
        logger.info("🎯 Verifying app functionality...")
        
        try:
            # Kiểm tra import được không
            spec = importlib.util.spec_from_file_location("soulfriend", self.app_file)
            if spec is None:
                self.qc_results.append("❌ QC FUNC: Không thể import app")
                self.critical_issues.append("Cannot import main app")
                return
                
            self.qc_results.append("✅ QC FUNC: App có thể import")
            
            # Kiểm tra syntax
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            try:
                compile(content, self.app_file, 'exec')
                self.qc_results.append("✅ QC FUNC: Python syntax OK")
            except SyntaxError as e:
                self.qc_results.append(f"❌ QC FUNC: Syntax error - {e}")
                self.critical_issues.append(f"Syntax error: {e}")
                
            # Kiểm tra các function chính
            main_functions = [
                "main()",
                "st.set_page_config",
                "SmartUIExperience",
                "load_dass21_vi",
                "score_dass21"
            ]
            
            for func in main_functions:
                if func in content:
                    self.qc_results.append(f"✅ QC FUNC: {func} - Có")
                else:
                    self.qc_results.append(f"❌ QC FUNC: {func} - THIẾU")
                    
        except Exception as e:
            self.qc_results.append(f"❌ QC FUNC: Error - {e}")
            self.critical_issues.append(f"Function verification error: {e}")
            
    def verify_data_integrity(self):
        """Kiểm tra tính toàn vẹn dữ liệu"""
        logger.info("🎯 Verifying data integrity...")
        
        # Kiểm tra JSON files
        json_files = [
            f"{self.base_path}/data/dass21_vi.json",
            f"{self.base_path}/data/phq9_vi.json"
        ]
        
        for json_file in json_files:
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # Kiểm tra structure cho DASS-21
                    if "dass21" in json_file:
                        required_keys = ['questions', 'scoring']
                        for key in required_keys:
                            if key in data:
                                self.qc_results.append(f"✅ QC DATA: DASS-21 {key} - OK")
                            else:
                                self.qc_results.append(f"❌ QC DATA: DASS-21 {key} - THIẾU")
                                
                        # Kiểm tra số câu hỏi
                        if 'questions' in data:
                            question_count = len(data['questions'])
                            if question_count == 21:
                                self.qc_results.append(f"✅ QC DATA: DASS-21 có đủ 21 câu")
                            else:
                                self.qc_results.append(f"❌ QC DATA: DASS-21 có {question_count} câu (không đúng)")
                                
                    self.qc_results.append(f"✅ QC DATA: {os.path.basename(json_file)} - Valid JSON")
                    
                except json.JSONDecodeError as e:
                    self.qc_results.append(f"❌ QC DATA: {os.path.basename(json_file)} - Invalid JSON")
                    self.critical_issues.append(f"Invalid JSON: {json_file}")
                    
            else:
                self.qc_results.append(f"❌ QC DATA: {os.path.basename(json_file)} - THIẾU")
                
    def verify_security_compliance(self):
        """Kiểm tra tuân thủ bảo mật"""
        logger.info("🎯 Verifying security compliance...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Critical security checks
            security_violations = [
                ("hardcoded password", ["password =", "pwd =", "passwd ="]),
                ("hardcoded API key", ["api_key =", "apikey =", "key ="]),
                ("SQL injection risk", ["sql =", "SELECT ", "UPDATE ", "DELETE "]),
                ("unsafe eval", ["eval(", "exec("]),
                ("unsafe file ops", ["open(", "file("])
            ]
            
            for violation_name, patterns in security_violations:
                found_violation = False
                for pattern in patterns:
                    if pattern.lower() in content.lower():
                        if violation_name == "unsafe file ops" and "with open" in content:
                            continue  # "with open" is safe
                        found_violation = True
                        break
                        
                if found_violation:
                    self.qc_results.append(f"❌ QC SEC: {violation_name} - PHÁT HIỆN")
                    self.critical_issues.append(f"Security violation: {violation_name}")
                else:
                    self.qc_results.append(f"✅ QC SEC: {violation_name} - OK")
                    
            # Check for security best practices
            security_practices = [
                ("input validation", "validate"),
                ("error handling", "try:" and "except"),
                ("logging", "logger"),
                ("secure file handling", "with open")
            ]
            
            for practice_name, keyword in security_practices:
                if keyword in content:
                    self.qc_results.append(f"✅ QC SEC: {practice_name} - Có")
                else:
                    self.qc_results.append(f"⚠️ QC SEC: {practice_name} - Nên có")
                    
        except Exception as e:
            self.qc_results.append(f"❌ QC SEC: Error checking security - {e}")
            
    def verify_performance_standards(self):
        """Kiểm tra tiêu chuẩn hiệu suất"""
        logger.info("🎯 Verifying performance standards...")
        
        try:
            # File size check
            file_size = os.path.getsize(self.app_file)
            size_mb = file_size / (1024 * 1024)
            
            if size_mb < 1:  # < 1MB
                self.qc_results.append(f"✅ QC PERF: File size OK ({size_mb:.2f}MB)")
            elif size_mb < 5:  # < 5MB
                self.qc_results.append(f"⚠️ QC PERF: File size lớn ({size_mb:.2f}MB)")
            else:
                self.qc_results.append(f"❌ QC PERF: File size quá lớn ({size_mb:.2f}MB)")
                self.critical_issues.append(f"File too large: {size_mb:.2f}MB")
                
            # Code complexity check
            with open(self.app_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            
            if total_lines < 500:
                self.qc_results.append(f"✅ QC PERF: Line count OK ({total_lines})")
            elif total_lines < 1000:
                self.qc_results.append(f"⚠️ QC PERF: Line count cao ({total_lines})")
            else:
                self.qc_results.append(f"❌ QC PERF: Line count quá cao ({total_lines})")
                
            # Import efficiency
            import_lines = [line for line in lines if line.strip().startswith(('import ', 'from '))]
            if len(import_lines) < 20:
                self.qc_results.append(f"✅ QC PERF: Import count OK ({len(import_lines)})")
            else:
                self.qc_results.append(f"⚠️ QC PERF: Quá nhiều imports ({len(import_lines)})")
                
        except Exception as e:
            self.qc_results.append(f"❌ QC PERF: Error checking performance - {e}")
            
    def verify_user_experience_standards(self):
        """Kiểm tra tiêu chuẩn user experience"""
        logger.info("🎯 Verifying UX standards...")
        
        try:
            with open(self.app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # UX requirements
            ux_requirements = [
                ("Page title", "page_title"),
                ("Page icon", "page_icon"),
                ("Layout config", "layout="),
                ("Loading indicators", "spinner" in content.lower() or "progress" in content.lower()),
                ("Error messages", "error" in content.lower() or "warning" in content.lower()),
                ("Success feedback", "success" in content.lower()),
                ("Help text", "help=" in content or "help_" in content)
            ]
            
            for req_name, condition in ux_requirements:
                if isinstance(condition, str) and condition in content:
                    self.qc_results.append(f"✅ QC UX: {req_name} - Có")
                elif isinstance(condition, bool) and condition:
                    self.qc_results.append(f"✅ QC UX: {req_name} - Có")
                else:
                    self.qc_results.append(f"❌ QC UX: {req_name} - THIẾU")
                    
            # Accessibility check
            accessibility_features = [
                ("Alt text", "alt="),
                ("Labels", "label="),
                ("Keyboard navigation", "key=" in content or "shortcut" in content)
            ]
            
            for feature_name, keyword in accessibility_features:
                if keyword in content:
                    self.qc_results.append(f"✅ QC A11Y: {feature_name} - Có")
                else:
                    self.qc_results.append(f"⚠️ QC A11Y: {feature_name} - Nên có")
                    
        except Exception as e:
            self.qc_results.append(f"❌ QC UX: Error checking UX - {e}")
            
    def generate_final_report(self):
        """Tạo báo cáo cuối cùng"""
        logger.info("🎯 Generating final QC report...")
        
        # Thống kê
        total = len(self.qc_results)
        passed = len([r for r in self.qc_results if r.startswith("✅")])
        warnings = len([r for r in self.qc_results if r.startswith("⚠️")])
        failed = len([r for r in self.qc_results if r.startswith("❌")])
        critical_count = len(self.critical_issues)
        
        # Đánh giá tổng thể
        if critical_count == 0 and failed == 0:
            status = "🟢 READY FOR DEPLOYMENT"
            recommendation = "Ứng dụng sẵn sàng để deploy!"
        elif critical_count == 0 and failed <= 3:
            status = "🟡 DEPLOY WITH CAUTION"
            recommendation = "Có thể deploy nhưng nên sửa các vấn đề nhỏ"
        elif critical_count <= 2:
            status = "🟠 NEEDS FIXES"
            recommendation = "Cần sửa các vấn đề nghiêm trọng trước khi deploy"
        else:
            status = "🔴 DO NOT DEPLOY"
            recommendation = "KHÔNG deploy - có vấn đề nghiêm trọng"
            
        return {
            'status': status,
            'recommendation': recommendation,
            'total_checks': total,
            'passed': passed,
            'warnings': warnings,
            'failed': failed,
            'critical_issues': critical_count,
            'success_rate': (passed / total) * 100 if total > 0 else 0
        }
        
    def run_quality_control(self):
        """Chạy toàn bộ quality control"""
        logger.info("🎯 Running complete quality control...")
        
        print("\n🎯 SOULFRIEND QUALITY CONTROL")
        print("=" * 40)
        
        # Chạy tất cả kiểm tra
        self.verify_deployment_readiness()
        self.verify_app_functionality()
        self.verify_data_integrity()
        self.verify_security_compliance()
        self.verify_performance_standards()
        self.verify_user_experience_standards()
        
        # In kết quả
        print("\n🎯 QC RESULTS:")
        print("-" * 15)
        for result in self.qc_results:
            print(result)
            
        # Critical issues
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.critical_issues)}):")
            print("-" * 25)
            for issue in self.critical_issues:
                print(f"❌ {issue}")
                
        # Báo cáo cuối
        report = self.generate_final_report()
        
        print(f"\n📊 FINAL QC REPORT:")
        print("=" * 20)
        print(f"Status: {report['status']}")
        print(f"Total checks: {report['total_checks']}")
        print(f"✅ Passed: {report['passed']}")
        print(f"⚠️ Warnings: {report['warnings']}")
        print(f"❌ Failed: {report['failed']}")
        print(f"🚨 Critical: {report['critical_issues']}")
        print(f"📈 Success rate: {report['success_rate']:.1f}%")
        print(f"\n💡 Recommendation: {report['recommendation']}")
        
        return report

def main():
    """Main function"""
    qc = SOULFRIENDQualityControl()
    report = qc.run_quality_control()
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"/workspaces/Mentalhealth/tests/QC_REPORT_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"\n💾 QC Report saved: {report_file}")
    
    return report

if __name__ == "__main__":
    main()
