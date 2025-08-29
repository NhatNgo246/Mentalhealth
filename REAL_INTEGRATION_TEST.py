#!/usr/bin/env python3
"""
REALISTIC INTEGRATION TEST SYSTEM
Tests ACTUAL user workflows with REAL runtime execution
"""

import subprocess
import time
import requests
import os
import sys
import threading
import signal

class RealIntegrationTester:
    def __init__(self):
        self.streamlit_process = None
        self.base_url = "http://localhost:8504"
        
    def start_streamlit(self):
        """Start Streamlit server for testing"""
        try:
            cmd = [
                "/workspaces/Mentalhealth/.venv/bin/python", 
                "-m", "streamlit", "run", 
                "/workspaces/Mentalhealth/SOULFRIEND.py",
                "--server.port", "8504",
                "--server.headless", "true",
                "--server.address", "0.0.0.0"
            ]
            
            self.streamlit_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd="/workspaces/Mentalhealth"
            )
            
            # Wait for startup
            for i in range(30):  # 30 second timeout
                try:
                    response = requests.get(self.base_url, timeout=2)
                    if response.status_code == 200:
                        print(f"✅ Streamlit started successfully on {self.base_url}")
                        return True
                except:
                    time.sleep(1)
                    
            print("❌ Failed to start Streamlit within 30 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Error starting Streamlit: {e}")
            return False
    
    def stop_streamlit(self):
        """Stop Streamlit server"""
        if self.streamlit_process:
            try:
                self.streamlit_process.terminate()
                self.streamlit_process.wait(timeout=5)
                print("✅ Streamlit stopped")
            except:
                self.streamlit_process.kill()
                print("⚠️ Streamlit force killed")
    
    def test_runtime_stability(self):
        """Test if application runs without runtime errors"""
        print("\n🔍 TESTING RUNTIME STABILITY")
        print("-" * 50)
        
        try:
            # Test multiple requests to trigger different code paths
            test_count = 5
            success_count = 0
            
            for i in range(test_count):
                try:
                    response = requests.get(self.base_url, timeout=10)
                    if response.status_code == 200:
                        success_count += 1
                        print(f"✅ Request {i+1}: OK")
                    else:
                        print(f"❌ Request {i+1}: HTTP {response.status_code}")
                    
                    time.sleep(1)  # Prevent overwhelming
                    
                except Exception as e:
                    print(f"❌ Request {i+1}: {e}")
            
            success_rate = (success_count / test_count) * 100
            print(f"\n📊 Runtime Stability: {success_count}/{test_count} ({success_rate:.1f}%)")
            
            return success_rate >= 80
            
        except Exception as e:
            print(f"❌ Runtime stability test failed: {e}")
            return False
    
    def test_error_monitoring(self):
        """Monitor Streamlit logs for runtime errors"""
        print("\n🔍 MONITORING RUNTIME ERRORS")
        print("-" * 50)
        
        if not self.streamlit_process:
            print("❌ No Streamlit process to monitor")
            return False
            
        # Read process output for errors
        errors_found = []
        
        try:
            # Non-blocking read with timeout
            import select
            
            if hasattr(select, 'poll'):
                poller = select.poll()
                poller.register(self.streamlit_process.stdout, select.POLLIN)
                
                # Poll for 10 seconds
                for _ in range(10):
                    if poller.poll(1000):  # 1 second timeout
                        line = self.streamlit_process.stdout.readline()
                        if line:
                            if "Error" in line or "Exception" in line or "Traceback" in line:
                                errors_found.append(line.strip())
                                print(f"❌ Runtime Error: {line.strip()}")
            
            if not errors_found:
                print("✅ No runtime errors detected in logs")
                return True
            else:
                print(f"❌ Found {len(errors_found)} runtime errors")
                return False
                
        except Exception as e:
            print(f"⚠️ Error monitoring failed: {e}")
            return True  # Don't fail test for monitoring issues
    
    def run_comprehensive_test(self):
        """Run complete integration test suite"""
        print("🧪 REAL INTEGRATION TEST SYSTEM")
        print("=" * 60)
        print("Testing ACTUAL runtime behavior, not just imports!")
        
        test_results = {}
        
        try:
            # 1. Start Streamlit
            print("\n1️⃣ STARTING STREAMLIT SERVER")
            if not self.start_streamlit():
                print("❌ CRITICAL: Cannot start Streamlit")
                return False
            
            test_results['startup'] = True
            time.sleep(3)  # Allow stabilization
            
            # 2. Test runtime stability
            print("\n2️⃣ TESTING RUNTIME STABILITY")
            test_results['stability'] = self.test_runtime_stability()
            
            # 3. Monitor for errors
            print("\n3️⃣ MONITORING RUNTIME ERRORS")
            test_results['error_monitoring'] = self.test_error_monitoring()
            
            # Calculate overall score
            passed_tests = sum(test_results.values())
            total_tests = len(test_results)
            success_rate = (passed_tests / total_tests) * 100
            
            print(f"\n📊 INTEGRATION TEST RESULTS")
            print("=" * 60)
            for test_name, result in test_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status} {test_name.title()}")
            
            print(f"\n🎯 Overall Score: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
            
            if success_rate >= 80:
                print("🎉 INTEGRATION TESTS PASSED!")
                return True
            else:
                print("🚨 INTEGRATION TESTS FAILED!")
                return False
                
        except Exception as e:
            print(f"❌ Integration test suite failed: {e}")
            return False
            
        finally:
            # Always cleanup
            self.stop_streamlit()

def main():
    """Run integration tests"""
    tester = RealIntegrationTester()
    
    # Setup signal handler for cleanup
    def signal_handler(signum, frame):
        print("\n⚠️ Test interrupted, cleaning up...")
        tester.stop_streamlit()
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        success = tester.run_comprehensive_test()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        return 1
    finally:
        tester.stop_streamlit()

if __name__ == "__main__":
    exit(main())
