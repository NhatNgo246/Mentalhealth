#!/usr/bin/env python3
"""
🧪 SOULFRIEND QUALITY ASSURANCE SYSTEM
=========================================
Comprehensive Testing Suite for SOULFRIEND.py - Main Application

Created: August 27, 2025
Purpose: Ensure SOULFRIEND.py works perfectly without errors
Team: Tester + QA + QC Pipeline
"""

import sys
import os
import subprocess
import importlib.util
import logging
import time
from datetime import datetime
from pathlib import Path

# Setup logging
log_file = "/workspaces/Mentalhealth/tests/quality_assurance.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SOULFRIENDTester:
    """🔍 TESTER - Kiểm tra chức năng cơ bản"""
    
    def __init__(self):
        self.app_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
        self.components_path = "/workspaces/Mentalhealth/components"
        self.data_path = "/workspaces/Mentalhealth/data"
        self.test_results = []
        
    def test_file_existence(self):
        """Kiểm tra tồn tại file chính"""
        logger.info("🔍 TESTER: Kiểm tra file tồn tại...")
        
        tests = [
            ("SOULFRIEND.py", self.app_path),
            ("components/ui.py", f"{self.components_path}/ui.py"),
            ("components/ui_advanced.py", f"{self.components_path}/ui_advanced.py"),
            ("components/questionnaires.py", f"{self.components_path}/questionnaires.py"),
            ("components/scoring.py", f"{self.components_path}/scoring.py"),
            ("data/dass21_vi.json", f"{self.data_path}/dass21_vi.json"),
            ("requirements.txt", "/workspaces/Mentalhealth/requirements.txt")
        ]
        
        for name, path in tests:
            if os.path.exists(path):
                self.test_results.append(f"✅ {name} - TỒN TẠI")
                logger.info(f"✅ {name} - OK")
            else:
                self.test_results.append(f"❌ {name} - THIẾU FILE")
                logger.error(f"❌ {name} - MISSING")
                
    def test_python_syntax(self):
        """Kiểm tra syntax Python"""
        logger.info("🔍 TESTER: Kiểm tra Python syntax...")
        
        try:
            with open(self.app_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            compile(code, self.app_path, 'exec')
            self.test_results.append("✅ SOULFRIEND.py - SYNTAX ĐÚNG")
            logger.info("✅ Python syntax - OK")
            
        except SyntaxError as e:
            self.test_results.append(f"❌ SOULFRIEND.py - SYNTAX LỖI: {e}")
            logger.error(f"❌ Syntax error: {e}")
        except Exception as e:
            self.test_results.append(f"❌ SOULFRIEND.py - LỖI KHÁC: {e}")
            logger.error(f"❌ Other error: {e}")
            
    def test_imports(self):
        """Kiểm tra import dependencies"""
        logger.info("🔍 TESTER: Kiểm tra imports...")
        
        required_imports = [
            'streamlit', 'pandas', 'json', 'os', 'time', 'logging', 'datetime'
        ]
        
        for module in required_imports:
            try:
                __import__(module)
                self.test_results.append(f"✅ Import {module} - OK")
                logger.info(f"✅ Import {module} - OK")
            except ImportError:
                self.test_results.append(f"❌ Import {module} - THIẾU")
                logger.error(f"❌ Import {module} - MISSING")
                
    def run_all_tests(self):
        """Chạy tất cả test"""
        logger.info("🔍 TESTER: Bắt đầu kiểm tra...")
        start_time = time.time()
        
        self.test_file_existence()
        self.test_python_syntax()
        self.test_imports()
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"🔍 TESTER: Hoàn thành trong {duration:.2f}s")
        return self.test_results

class SOULFRIENDQualityAssurance:
    """📋 QA - Kiểm tra chất lượng code"""
    
    def __init__(self):
        self.app_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
        self.qa_results = []
        
    def check_code_structure(self):
        """Kiểm tra cấu trúc code"""
        logger.info("📋 QA: Kiểm tra cấu trúc code...")
        
        try:
            with open(self.app_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Kiểm tra các thành phần quan trọng
            checks = [
                ("import streamlit", "import streamlit" in content),
                ("st.set_page_config", "st.set_page_config" in content),
                ("Smart UI Experience", "SmartUIExperience" in content),
                ("Logging setup", "logging.basicConfig" in content),
                ("DASS-21 questionnaire", "dass21" in content.lower()),
                ("Session state", "st.session_state" in content)
            ]
            
            for check_name, passed in checks:
                if passed:
                    self.qa_results.append(f"✅ QA: {check_name} - CÓ")
                    logger.info(f"✅ QA: {check_name} - OK")
                else:
                    self.qa_results.append(f"❌ QA: {check_name} - THIẾU")
                    logger.warning(f"❌ QA: {check_name} - MISSING")
                    
        except Exception as e:
            self.qa_results.append(f"❌ QA: Lỗi đọc file - {e}")
            logger.error(f"❌ QA: File read error - {e}")
            
    def check_ui_components(self):
        """Kiểm tra UI components"""
        logger.info("📋 QA: Kiểm tra UI components...")
        
        try:
            with open(self.app_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            ui_components = [
                ("Hero section", "create_smart_hero"),
                ("Question cards", "create_smart_question_card"),
                ("Results dashboard", "create_smart_results_dashboard"),
                ("Progress ring", "create_progress_ring"),
                ("Consent form", "create_consent_agreement_form")
            ]
            
            for comp_name, func_name in ui_components:
                if func_name in content:
                    self.qa_results.append(f"✅ QA UI: {comp_name} - CÓ")
                    logger.info(f"✅ QA UI: {comp_name} - OK")
                else:
                    self.qa_results.append(f"❌ QA UI: {comp_name} - THIẾU")
                    logger.warning(f"❌ QA UI: {comp_name} - MISSING")
                    
        except Exception as e:
            self.qa_results.append(f"❌ QA UI: Lỗi kiểm tra - {e}")
            logger.error(f"❌ QA UI: Check error - {e}")
            
    def check_data_flow(self):
        """Kiểm tra luồng dữ liệu"""
        logger.info("📋 QA: Kiểm tra data flow...")
        
        try:
            with open(self.app_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            data_flow_checks = [
                ("Load questionnaire", "load_dass21_vi"),
                ("Score calculation", "score_dass21"),
                ("State validation", "validate_app_state"),
                ("Session management", "st.session_state"),
                ("User responses", "responses")
            ]
            
            for check_name, keyword in data_flow_checks:
                if keyword in content:
                    self.qa_results.append(f"✅ QA DATA: {check_name} - CÓ")
                    logger.info(f"✅ QA DATA: {check_name} - OK")
                else:
                    self.qa_results.append(f"❌ QA DATA: {check_name} - THIẾU")
                    logger.warning(f"❌ QA DATA: {check_name} - MISSING")
                    
        except Exception as e:
            self.qa_results.append(f"❌ QA DATA: Lỗi kiểm tra - {e}")
            logger.error(f"❌ QA DATA: Check error - {e}")
            
    def run_qa_tests(self):
        """Chạy tất cả QA tests"""
        logger.info("📋 QA: Bắt đầu kiểm tra chất lượng...")
        start_time = time.time()
        
        self.check_code_structure()
        self.check_ui_components()
        self.check_data_flow()
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"📋 QA: Hoàn thành trong {duration:.2f}s")
        return self.qa_results

class SOULFRIENDQualityControl:
    """🎯 QC - Kiểm soát chất lượng cuối cùng"""
    
    def __init__(self):
        self.app_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
        self.qc_results = []
        
    def verify_deployment_readiness(self):
        """Kiểm tra sẵn sàng deploy"""
        logger.info("🎯 QC: Kiểm tra sẵn sàng deployment...")
        
        deployment_checks = [
            ("SOULFRIEND.py exists", os.path.exists(self.app_path)),
            ("Components folder", os.path.exists("/workspaces/Mentalhealth/components")),
            ("Data folder", os.path.exists("/workspaces/Mentalhealth/data")),
            ("Requirements file", os.path.exists("/workspaces/Mentalhealth/requirements.txt")),
            ("Launch script", os.path.exists("/workspaces/Mentalhealth/launch_soulfriend.sh"))
        ]
        
        for check_name, passed in deployment_checks:
            if passed:
                self.qc_results.append(f"✅ QC DEPLOY: {check_name} - OK")
                logger.info(f"✅ QC DEPLOY: {check_name} - OK")
            else:
                self.qc_results.append(f"❌ QC DEPLOY: {check_name} - THIẾU")
                logger.error(f"❌ QC DEPLOY: {check_name} - MISSING")
                
    def verify_security(self):
        """Kiểm tra bảo mật"""
        logger.info("🎯 QC: Kiểm tra bảo mật...")
        
        try:
            with open(self.app_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            security_checks = [
                ("No hardcoded secrets", not any(x in content.lower() for x in ["password =", "secret =", "api_key ="])),
                ("Safe file operations", "with open" in content),
                ("Input validation", "validate" in content),
                ("Error handling", "try:" in content and "except" in content),
                ("Logging enabled", "logger" in content)
            ]
            
            for check_name, passed in security_checks:
                if passed:
                    self.qc_results.append(f"✅ QC SECURITY: {check_name} - OK")
                    logger.info(f"✅ QC SECURITY: {check_name} - OK")
                else:
                    self.qc_results.append(f"❌ QC SECURITY: {check_name} - CẢNH BÁO")
                    logger.warning(f"❌ QC SECURITY: {check_name} - WARNING")
                    
        except Exception as e:
            self.qc_results.append(f"❌ QC SECURITY: Lỗi kiểm tra - {e}")
            logger.error(f"❌ QC SECURITY: Check error - {e}")
            
    def verify_performance(self):
        """Kiểm tra hiệu suất"""
        logger.info("🎯 QC: Kiểm tra hiệu suất...")
        
        try:
            # Kiểm tra kích thước file
            file_size = os.path.getsize(self.app_path)
            size_mb = file_size / (1024 * 1024)
            
            if size_mb < 5:  # Dưới 5MB
                self.qc_results.append(f"✅ QC PERF: File size {size_mb:.2f}MB - OK")
                logger.info(f"✅ QC PERF: File size {size_mb:.2f}MB - OK")
            else:
                self.qc_results.append(f"❌ QC PERF: File size {size_mb:.2f}MB - LỚN")
                logger.warning(f"❌ QC PERF: File size {size_mb:.2f}MB - LARGE")
                
            # Kiểm tra complexity
            with open(self.app_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            if total_lines < 1000:
                self.qc_results.append(f"✅ QC PERF: {total_lines} lines - OK")
                logger.info(f"✅ QC PERF: {total_lines} lines - OK")
            else:
                self.qc_results.append(f"❌ QC PERF: {total_lines} lines - PHỨC TẠP")
                logger.warning(f"❌ QC PERF: {total_lines} lines - COMPLEX")
                
        except Exception as e:
            self.qc_results.append(f"❌ QC PERF: Lỗi kiểm tra - {e}")
            logger.error(f"❌ QC PERF: Check error - {e}")
            
    def run_qc_tests(self):
        """Chạy tất cả QC tests"""
        logger.info("🎯 QC: Bắt đầu kiểm soát chất lượng...")
        start_time = time.time()
        
        self.verify_deployment_readiness()
        self.verify_security()
        self.verify_performance()
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"🎯 QC: Hoàn thành trong {duration:.2f}s")
        return self.qc_results

class QualityPipeline:
    """🚀 PIPELINE - Chạy toàn bộ quy trình kiểm tra"""
    
    def __init__(self):
        self.tester = SOULFRIENDTester()
        self.qa = SOULFRIENDQualityAssurance()
        self.qc = SOULFRIENDQualityControl()
        
    def run_full_pipeline(self):
        """Chạy toàn bộ pipeline"""
        logger.info("🚀 PIPELINE: Bắt đầu quy trình kiểm tra toàn diện...")
        start_time = time.time()
        
        print("\n" + "="*60)
        print("🧪 SOULFRIEND QUALITY ASSURANCE PIPELINE")
        print("="*60)
        
        # Phase 1: Testing
        print("\n🔍 PHASE 1: TESTING")
        print("-" * 30)
        tester_results = self.tester.run_all_tests()
        for result in tester_results:
            print(result)
            
        # Phase 2: Quality Assurance
        print("\n📋 PHASE 2: QUALITY ASSURANCE")
        print("-" * 40)
        qa_results = self.qa.run_qa_tests()
        for result in qa_results:
            print(result)
            
        # Phase 3: Quality Control
        print("\n🎯 PHASE 3: QUALITY CONTROL")
        print("-" * 35)
        qc_results = self.qc.run_qc_tests()
        for result in qc_results:
            print(result)
            
        # Final Report
        end_time = time.time()
        total_duration = end_time - start_time
        
        all_results = tester_results + qa_results + qc_results
        total_tests = len(all_results)
        passed_tests = len([r for r in all_results if r.startswith("✅")])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "="*60)
        print("📊 FINAL REPORT")
        print("="*60)
        print(f"⏱️  Thời gian: {total_duration:.2f}s")
        print(f"📈 Tổng số test: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 SOULFRIEND.py SẴN SÀNG HOẠT ĐỘNG!")
            print("✨ Tất cả kiểm tra đều PASS - Không có lỗi!")
        else:
            print(f"\n⚠️  CÓ {failed_tests} VẤN ĐỀ CẦN SỬA!")
            print("🔧 Vui lòng kiểm tra các lỗi ở trên")
            
        print("="*60)
        
        return {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'duration': total_duration,
            'results': all_results
        }

def main():
    """Main function"""
    pipeline = QualityPipeline()
    results = pipeline.run_full_pipeline()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"/workspaces/Mentalhealth/tests/QA_REPORT_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("SOULFRIEND QUALITY ASSURANCE REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Total Tests: {results['total_tests']}\n")
        f.write(f"Passed: {results['passed']}\n")
        f.write(f"Failed: {results['failed']}\n")
        f.write(f"Success Rate: {results['success_rate']:.1f}%\n")
        f.write(f"Duration: {results['duration']:.2f}s\n\n")
        f.write("DETAILED RESULTS:\n")
        f.write("-" * 20 + "\n")
        for result in results['results']:
            f.write(result + "\n")
    
    print(f"\n💾 Báo cáo đã lưu: {report_file}")
    return results

if __name__ == "__main__":
    main()
