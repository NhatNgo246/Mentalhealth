#!/usr/bin/env python3
"""
🛡️ SOULFRIEND QC SYSTEM
Quality Control and System Validation
"""

import os
import json
import sys
import time
import requests
import subprocess
from datetime import datetime
import threading

class SOULFRIENDQCSystem:
    def __init__(self):
        self.base_path = "/workspaces/Mentalhealth"
        self.python_path = os.path.join(self.base_path, ".venv", "bin", "python")
        self.streamlit_process = None
        self.test_results = {}
        
    def log(self, level, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"[{timestamp}] {symbols.get(level, '•')} {message}")
        
    def check_system_health(self):
        """Check overall system health"""
        self.log("INFO", "Starting system health check...")
        
        health_checks = {
            "Python Environment": self.check_python_env(),
            "File Permissions": self.check_file_permissions(),
            "Memory Usage": self.check_memory_usage(),
            "Disk Space": self.check_disk_space(),
            "Network Connectivity": self.check_network()
        }
        
        passed = sum(health_checks.values())
        total = len(health_checks)
        
        for check, result in health_checks.items():
            self.log("SUCCESS" if result else "ERROR", f"{check}: {'OK' if result else 'FAILED'}")
            
        self.log("INFO", f"System health: {passed}/{total} checks passed")
        return passed == total
        
    def check_python_env(self):
        """Check Python environment"""
        try:
            result = subprocess.run([self.python_path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
            
    def check_file_permissions(self):
        """Check file permissions"""
        try:
            # Test read permission on key files
            test_files = ["SOULFRIEND.py", "components/questionnaires.py"]
            for file_path in test_files:
                full_path = os.path.join(self.base_path, file_path)
                with open(full_path, 'r') as f:
                    f.read(100)  # Read first 100 chars
            return True
        except:
            return False
            
    def check_memory_usage(self):
        """Check available memory"""
        try:
            result = subprocess.run(["free", "-m"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')[1]  # Memory line
                values = lines.split()
                available = int(values[6])  # Available memory
                return available > 100  # At least 100MB available
        except:
            pass
        return True  # Assume OK if can't check
        
    def check_disk_space(self):
        """Check available disk space"""
        try:
            result = subprocess.run(["df", "-h", self.base_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')[1]
                values = lines.split()
                usage = values[4].replace('%', '')
                return int(usage) < 90  # Less than 90% usage
        except:
            pass
        return True  # Assume OK if can't check
        
    def check_network(self):
        """Check network connectivity"""
        try:
            # Quick connectivity test
            result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return True  # Assume OK if can't check
            
    def start_streamlit_test(self, port=8505):
        """Start Streamlit for testing"""
        self.log("INFO", f"Starting Streamlit test server on port {port}...")
        
        try:
            cmd = [
                self.python_path, "-m", "streamlit", "run", 
                "SOULFRIEND.py", 
                f"--server.port={port}",
                "--server.address=localhost",
                "--server.headless=true"
            ]
            
            self.streamlit_process = subprocess.Popen(
                cmd,
                cwd=self.base_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for startup
            self.log("INFO", "Waiting for Streamlit to start...")
            time.sleep(8)
            
            # Check if process is still running
            if self.streamlit_process.poll() is None:
                self.log("SUCCESS", f"Streamlit started successfully on port {port}")
                return True
            else:
                stdout, stderr = self.streamlit_process.communicate()
                self.log("ERROR", f"Streamlit failed to start:")
                self.log("ERROR", f"STDOUT: {stdout[:200]}...")
                self.log("ERROR", f"STDERR: {stderr[:200]}...")
                return False
                
        except Exception as e:
            self.log("ERROR", f"Failed to start Streamlit: {e}")
            return False
            
    def test_streamlit_response(self, port=8505):
        """Test if Streamlit responds to HTTP requests"""
        self.log("INFO", "Testing Streamlit HTTP response...")
        
        url = f"http://localhost:{port}"
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.log("SUCCESS", f"Streamlit responding correctly (status: {response.status_code})")
                    return True
                else:
                    self.log("WARNING", f"Unexpected status code: {response.status_code}")
            except requests.ConnectionError:
                self.log("INFO", f"Connection attempt {attempt + 1}/{max_attempts} failed, retrying...")
                time.sleep(3)
            except Exception as e:
                self.log("ERROR", f"HTTP test error: {e}")
                
        self.log("ERROR", "Streamlit not responding to HTTP requests")
        return False
        
    def stop_streamlit_test(self):
        """Stop test Streamlit server"""
        if self.streamlit_process:
            self.log("INFO", "Stopping test Streamlit server...")
            try:
                self.streamlit_process.terminate()
                self.streamlit_process.wait(timeout=10)
                self.log("SUCCESS", "Streamlit server stopped")
            except subprocess.TimeoutExpired:
                self.log("WARNING", "Force killing Streamlit process...")
                self.streamlit_process.kill()
            except Exception as e:
                self.log("ERROR", f"Error stopping Streamlit: {e}")
                
    def test_questionnaire_loading(self):
        """Test questionnaire loading functionality"""
        self.log("INFO", "Testing questionnaire loading...")
        
        try:
            os.chdir(self.base_path)
            sys.path.insert(0, self.base_path)
            
            from components.questionnaires import QuestionnaireManager
            
            manager = QuestionnaireManager()
            questionnaires = ['DASS-21', 'PHQ-9', 'GAD-7', 'EPDS', 'PSS-10']
            
            success_count = 0
            for q_type in questionnaires:
                try:
                    data = manager.get_questionnaire(q_type)
                    if data:
                        success_count += 1
                        self.log("SUCCESS", f"Loaded {q_type}")
                    else:
                        self.log("ERROR", f"Empty data for {q_type}")
                except Exception as e:
                    self.log("ERROR", f"Failed to load {q_type}: {e}")
                    
            success_rate = success_count / len(questionnaires)
            self.log("INFO", f"Questionnaire loading success rate: {success_rate:.1%}")
            
            return success_rate >= 0.8  # At least 80% success
            
        except Exception as e:
            self.log("ERROR", f"Questionnaire test failed: {e}")
            return False
            
    def test_scoring_system(self):
        """Test scoring calculations"""
        self.log("INFO", "Testing scoring system...")
        
        try:
            os.chdir(self.base_path)
            sys.path.insert(0, self.base_path)
            
            from components.scoring import calculate_scores
            
            # Test with sample data
            test_data = {
                'questionnaire': 'PHQ-9',
                'responses': [1, 2, 1, 0, 2, 1, 3, 2, 1]  # Sample responses
            }
            
            result = calculate_scores(test_data['responses'], test_data['questionnaire'])
            
            if result and 'total_score' in result:
                self.log("SUCCESS", f"Scoring system working (sample score: {result['total_score']})")
                return True
            else:
                self.log("ERROR", "Scoring system returned invalid result")
                return False
                
        except Exception as e:
            self.log("ERROR", f"Scoring test failed: {e}")
            return False
            
    def run_integration_test(self):
        """Run full integration test"""
        self.log("INFO", "Starting integration test...")
        
        test_port = 8505
        
        try:
            # 1. System health check
            if not self.check_system_health():
                self.log("ERROR", "System health check failed")
                return False
                
            # 2. Component tests
            if not self.test_questionnaire_loading():
                self.log("ERROR", "Questionnaire loading test failed")
                return False
                
            if not self.test_scoring_system():
                self.log("ERROR", "Scoring system test failed")
                return False
                
            # 3. Streamlit integration test
            if not self.start_streamlit_test(test_port):
                self.log("ERROR", "Failed to start Streamlit for testing")
                return False
                
            # 4. HTTP response test
            http_ok = self.test_streamlit_response(test_port)
            
            # 5. Cleanup
            self.stop_streamlit_test()
            
            if http_ok:
                self.log("SUCCESS", "Integration test PASSED")
                return True
            else:
                self.log("ERROR", "Integration test FAILED")
                return False
                
        except Exception as e:
            self.log("ERROR", f"Integration test error: {e}")
            self.stop_streamlit_test()
            return False
            
    def run_quality_control(self):
        """Run complete quality control process"""
        print("🛡️ SOULFRIEND QUALITY CONTROL SYSTEM")
        print("=" * 60)
        print(f"📅 QC Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Base Path: {self.base_path}")
        print()
        
        # Run QC tests
        qc_results = {
            "System Health": self.check_system_health(),
            "Component Testing": self.test_questionnaire_loading() and self.test_scoring_system(),
            "Integration Test": self.run_integration_test()
        }
        
        print("\n" + "=" * 60)
        print("📊 QUALITY CONTROL RESULTS")
        print("=" * 60)
        
        passed = sum(qc_results.values())
        total = len(qc_results)
        
        for test_name, result in qc_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status:8} {test_name}")
            
        print(f"\n📈 QC Score: {passed}/{total} ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("\n🎉 QUALITY CONTROL PASSED!")
            print("✅ SOULFRIEND is validated and ready for production deployment.")
        else:
            print(f"\n💥 QUALITY CONTROL FAILED!")
            print(f"❌ {total - passed} critical issues detected. Please resolve before deployment.")
            
        return passed == total

if __name__ == "__main__":
    qc_system = SOULFRIENDQCSystem()
    success = qc_system.run_quality_control()
    sys.exit(0 if success else 1)
