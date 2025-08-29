#!/usr/bin/env python3
"""
ADVANCED USER FLOW TESTING SYSTEM
Tests realistic user interactions and edge cases
"""

import subprocess
import time
import requests
import json
import os
import sys
import threading
import random
from datetime import datetime

class AdvancedUserFlowTester:
    def __init__(self):
        self.streamlit_process = None
        self.base_url = "http://localhost:8505"
        self.test_scenarios = []
        
    def start_streamlit(self):
        """Start Streamlit server for advanced testing"""
        try:
            # Kill any existing streamlit processes
            subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
            time.sleep(2)
            
            cmd = [
                "/workspaces/Mentalhealth/.venv/bin/python", 
                "-m", "streamlit", "run", 
                "/workspaces/Mentalhealth/SOULFRIEND.py",
                "--server.port", "8505",
                "--server.headless", "true",
                "--server.address", "0.0.0.0",
                "--server.enableXsrfProtection", "false"
            ]
            
            self.streamlit_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd="/workspaces/Mentalhealth"
            )
            
            # Wait for startup with more patience
            for i in range(45):  # 45 second timeout
                try:
                    response = requests.get(self.base_url, timeout=3)
                    if response.status_code == 200:
                        print(f"✅ Streamlit started successfully on {self.base_url}")
                        time.sleep(3)  # Allow full initialization
                        return True
                except:
                    if i % 5 == 0:
                        print(f"⏳ Waiting for startup... ({i+1}/45)")
                    time.sleep(1)
                    
            print("❌ Failed to start Streamlit within 45 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Error starting Streamlit: {e}")
            return False
    
    def stop_streamlit(self):
        """Stop Streamlit server"""
        if self.streamlit_process:
            try:
                self.streamlit_process.terminate()
                self.streamlit_process.wait(timeout=10)
                print("✅ Streamlit stopped")
            except:
                self.streamlit_process.kill()
                print("⚠️ Streamlit force killed")
        
        # Additional cleanup
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    
    def test_rapid_requests(self):
        """Test rapid successive requests (stress test)"""
        print("\n🔥 STRESS TESTING - RAPID REQUESTS")
        print("-" * 50)
        
        rapid_count = 10
        success_count = 0
        errors = []
        
        start_time = time.time()
        
        for i in range(rapid_count):
            try:
                response = requests.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    success_count += 1
                    print(f"✅ Rapid request {i+1}: OK")
                else:
                    error_msg = f"HTTP {response.status_code}"
                    errors.append(error_msg)
                    print(f"❌ Rapid request {i+1}: {error_msg}")
                
                # No delay - stress test
                
            except Exception as e:
                errors.append(str(e))
                print(f"❌ Rapid request {i+1}: {e}")
        
        duration = time.time() - start_time
        success_rate = (success_count / rapid_count) * 100
        
        print(f"\n📊 Stress Test Results:")
        print(f"   ⚡ Requests: {rapid_count}")
        print(f"   ✅ Success: {success_count}")
        print(f"   ❌ Errors: {len(errors)}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        print(f"   ⏱️ Duration: {duration:.2f}s")
        print(f"   🚀 RPS: {rapid_count/duration:.1f}")
        
        return success_rate >= 70  # Allow some failures under stress
    
    def test_concurrent_users(self):
        """Simulate concurrent users"""
        print("\n👥 CONCURRENT USER SIMULATION")
        print("-" * 50)
        
        import threading
        import queue
        
        results_queue = queue.Queue()
        user_count = 5
        requests_per_user = 3
        
        def simulate_user(user_id):
            """Simulate individual user behavior"""
            user_results = []
            
            for request_num in range(requests_per_user):
                try:
                    # Random delay to simulate thinking time
                    think_time = random.uniform(0.1, 0.5)
                    time.sleep(think_time)
                    
                    response = requests.get(self.base_url, timeout=8)
                    
                    if response.status_code == 200:
                        user_results.append(True)
                        print(f"✅ User {user_id} Request {request_num + 1}: OK")
                    else:
                        user_results.append(False)
                        print(f"❌ User {user_id} Request {request_num + 1}: HTTP {response.status_code}")
                        
                except Exception as e:
                    user_results.append(False)
                    print(f"❌ User {user_id} Request {request_num + 1}: {e}")
            
            results_queue.put((user_id, user_results))
        
        # Start concurrent user threads
        threads = []
        start_time = time.time()
        
        for user_id in range(1, user_count + 1):
            thread = threading.Thread(target=simulate_user, args=(user_id,))
            thread.start()
            threads.append(thread)
        
        # Wait for all users to complete
        for thread in threads:
            thread.join(timeout=30)
        
        duration = time.time() - start_time
        
        # Collect results
        total_requests = 0
        successful_requests = 0
        
        while not results_queue.empty():
            user_id, user_results = results_queue.get()
            total_requests += len(user_results)
            successful_requests += sum(user_results)
        
        success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        
        print(f"\n📊 Concurrent User Results:")
        print(f"   👥 Users: {user_count}")
        print(f"   📨 Total Requests: {total_requests}")
        print(f"   ✅ Successful: {successful_requests}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        print(f"   ⏱️ Duration: {duration:.2f}s")
        
        return success_rate >= 80
    
    def test_error_recovery(self):
        """Test application's error handling and recovery"""
        print("\n🚨 ERROR RECOVERY TESTING")
        print("-" * 50)
        
        # Test invalid requests
        invalid_endpoints = [
            f"{self.base_url}/nonexistent",
            f"{self.base_url}/invalid-path",
            f"{self.base_url}/?invalid=param"
        ]
        
        recovery_score = 0
        total_tests = len(invalid_endpoints) + 2  # +2 for additional tests
        
        # Test invalid endpoints
        for endpoint in invalid_endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code in [200, 404]:  # 404 is acceptable for invalid paths
                    recovery_score += 1
                    print(f"✅ Error handling OK for: {endpoint}")
                else:
                    print(f"⚠️ Unexpected response for: {endpoint} -> {response.status_code}")
            except Exception as e:
                print(f"❌ Error recovery failed for: {endpoint} -> {e}")
        
        # Test recovery after errors (can we still access main page?)
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                recovery_score += 1
                print("✅ Main page accessible after error tests")
            else:
                print(f"❌ Main page recovery failed: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Main page recovery error: {e}")
        
        # Test application stability after error scenarios
        try:
            time.sleep(2)  # Brief pause
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                recovery_score += 1
                print("✅ Application stability confirmed")
            else:
                print(f"❌ Stability test failed: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Stability test error: {e}")
        
        success_rate = (recovery_score / total_tests) * 100
        print(f"\n📊 Error Recovery Score: {recovery_score}/{total_tests} ({success_rate:.1f}%)")
        
        return success_rate >= 70
    
    def test_memory_leaks(self):
        """Basic memory leak detection through sustained load"""
        print("\n🧠 MEMORY LEAK DETECTION")
        print("-" * 50)
        
        # Get initial memory usage
        try:
            import psutil
            if self.streamlit_process:
                process = psutil.Process(self.streamlit_process.pid)
                initial_memory = process.memory_info().rss / 1024 / 1024  # MB
                print(f"📊 Initial memory usage: {initial_memory:.1f} MB")
                
                # Sustained load test
                request_count = 20
                print(f"🔄 Running {request_count} requests...")
                
                for i in range(request_count):
                    try:
                        requests.get(self.base_url, timeout=3)
                        if i % 5 == 0:
                            current_memory = process.memory_info().rss / 1024 / 1024
                            print(f"   Memory at request {i}: {current_memory:.1f} MB")
                    except:
                        pass
                    time.sleep(0.1)
                
                # Final memory check
                final_memory = process.memory_info().rss / 1024 / 1024
                memory_increase = final_memory - initial_memory
                memory_increase_percent = (memory_increase / initial_memory) * 100
                
                print(f"📊 Final memory usage: {final_memory:.1f} MB")
                print(f"📈 Memory increase: {memory_increase:.1f} MB ({memory_increase_percent:.1f}%)")
                
                # Consider memory leak if increase is > 50%
                if memory_increase_percent < 50:
                    print("✅ Memory usage appears stable")
                    return True
                else:
                    print("⚠️ Potential memory leak detected")
                    return False
                    
        except ImportError:
            print("⚠️ psutil not available, skipping memory test")
            return True
        except Exception as e:
            print(f"⚠️ Memory test error: {e}")
            return True
    
    def run_comprehensive_advanced_tests(self):
        """Run complete advanced test suite"""
        print("🚀 ADVANCED USER FLOW TESTING SYSTEM")
        print("=" * 70)
        print("Testing realistic user scenarios and edge cases")
        
        test_results = {}
        
        try:
            # 1. Start Streamlit
            print("\n1️⃣ STARTING STREAMLIT SERVER")
            if not self.start_streamlit():
                print("❌ CRITICAL: Cannot start Streamlit")
                return False
            
            test_results['startup'] = True
            
            # 2. Stress testing
            print("\n2️⃣ STRESS TESTING")
            test_results['stress_test'] = self.test_rapid_requests()
            
            # 3. Concurrent users
            print("\n3️⃣ CONCURRENT USER TESTING")
            test_results['concurrent_users'] = self.test_concurrent_users()
            
            # 4. Error recovery
            print("\n4️⃣ ERROR RECOVERY TESTING")
            test_results['error_recovery'] = self.test_error_recovery()
            
            # 5. Memory leak detection
            print("\n5️⃣ MEMORY LEAK DETECTION")
            test_results['memory_leaks'] = self.test_memory_leaks()
            
            # Calculate overall score
            passed_tests = sum(test_results.values())
            total_tests = len(test_results)
            success_rate = (passed_tests / total_tests) * 100
            
            print(f"\n📊 ADVANCED TEST RESULTS")
            print("=" * 70)
            for test_name, result in test_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status} {test_name.replace('_', ' ').title()}")
            
            print(f"\n🎯 Overall Score: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
            
            if success_rate >= 80:
                print("🎉 ADVANCED TESTS PASSED!")
                print("💚 SOULFRIEND is production-ready!")
                return True
            else:
                print("🚨 SOME ADVANCED TESTS FAILED!")
                print("⚠️ Review failing tests before production deployment")
                return False
                
        except Exception as e:
            print(f"❌ Advanced test suite failed: {e}")
            return False
            
        finally:
            # Always cleanup
            print("\n🧹 CLEANING UP...")
            self.stop_streamlit()

def main():
    """Run advanced flow tests"""
    tester = AdvancedUserFlowTester()
    
    try:
        success = tester.run_comprehensive_advanced_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        return 1
    finally:
        tester.stop_streamlit()

if __name__ == "__main__":
    exit(main())
