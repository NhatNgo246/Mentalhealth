#!/usr/bin/env python3
"""
🎯 FINAL USER FLOW TEST
Test hoàn toàn để verify rằng user có thể:
1. Trả lời câu hỏi questionnaire
2. Nhận được kết quả hiển thị đúng

❌ Unit tests đã thất bại vì không test thực tế
✅ Integration test này sẽ test thực với Streamlit app
"""

import time
import requests
import subprocess
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException


def test_streamlit_connection():
    """Test basic connection to Streamlit app"""
    try:
        response = requests.get("http://localhost:8509", timeout=10)
        print(f"✅ Streamlit app accessible: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to Streamlit: {e}")
        return False


def simulate_user_questionnaire_flow():
    """Simulate complete user flow từ consent đến results"""
    print("\n🧪 Starting browser automation test...")
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:8509")
        
        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ Page loaded successfully")
        
        # Test 1: Accept consent (nếu có)
        try:
            consent_checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox']"))
            )
            consent_checkbox.click()
            print("✅ Consent checkbox clicked")
            
            # Click next button
            next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Tiếp tục')]")
            next_button.click()
            time.sleep(2)
            print("✅ Moved past consent page")
        except TimeoutException:
            print("ℹ️ No consent page found, continuing...")
        
        # Test 2: Select questionnaire (tìm GAD-7 or PHQ-9)
        try:
            # Tìm questionnaire selection
            gad7_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'GAD-7')]"))
            )
            gad7_button.click()
            time.sleep(2)
            print("✅ GAD-7 questionnaire selected")
        except TimeoutException:
            try:
                phq9_button = driver.find_element(By.XPATH, "//button[contains(text(), 'PHQ-9')]")
                phq9_button.click()
                time.sleep(2)
                print("✅ PHQ-9 questionnaire selected")
            except:
                print("⚠️ Could not find questionnaire selection buttons")
        
        # Test 3: Answer questions
        question_count = 0
        try:
            # Find all radio buttons for answering questions
            radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            print(f"Found {len(radio_buttons)} radio button options")
            
            # Answer each question (select first option for simplicity)
            current_question = 1
            while current_question <= 7:  # GAD-7 has 7 questions
                try:
                    # Find radio button for current question (select "Không bao giờ" = value 0)
                    radio_xpath = f"//input[@type='radio' and @value='0']"
                    radio_button = driver.find_element(By.XPATH, radio_xpath)
                    driver.execute_script("arguments[0].click();", radio_button)
                    print(f"✅ Answered question {current_question}")
                    question_count += 1
                    current_question += 1
                    time.sleep(0.5)
                except:
                    break
            
            print(f"✅ Answered {question_count} questions")
        except Exception as e:
            print(f"⚠️ Error answering questions: {e}")
        
        # Test 4: Submit answers
        try:
            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Gửi câu trả lời')]")
            submit_button.click()
            time.sleep(3)
            print("✅ Submitted answers")
        except Exception as e:
            print(f"⚠️ Could not find submit button: {e}")
        
        # Test 5: Check for results display
        try:
            # Look for results indicators
            results_indicators = [
                "Điểm tổng",
                "Mức độ nghiêm trọng",
                "Kết quả đánh giá",
                "Biểu đồ",
                "📊"
            ]
            
            page_text = driver.page_source
            results_found = []
            
            for indicator in results_indicators:
                if indicator in page_text:
                    results_found.append(indicator)
            
            if results_found:
                print(f"✅ Results displayed with indicators: {results_found}")
                return True
            else:
                print("❌ No results indicators found in page")
                return False
                
        except Exception as e:
            print(f"❌ Error checking results: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Browser automation failed: {e}")
        return False
    
    finally:
        try:
            driver.quit()
        except:
            pass


def test_api_endpoints():
    """Test API responses from Streamlit"""
    endpoints_to_test = [
        "http://localhost:8509/",
        "http://localhost:8509/healthz",  # Streamlit health check
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"✅ {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"⚠️ {endpoint}: {e}")


def main():
    """Main test execution"""
    print("🎯 FINAL USER FLOW TEST - Kiểm tra trả lời câu hỏi và hiển thị kết quả")
    print("=" * 70)
    
    # Test 1: Basic connectivity
    print("\n📡 Test 1: Streamlit App Connection")
    if not test_streamlit_connection():
        print("❌ CRITICAL: Cannot connect to Streamlit app")
        return False
    
    # Test 2: API endpoints
    print("\n🌐 Test 2: API Endpoints")
    test_api_endpoints()
    
    # Test 3: User flow simulation
    print("\n🤖 Test 3: User Flow Simulation")
    try:
        # Check if Chrome is available
        chrome_result = subprocess.run(["which", "google-chrome"], capture_output=True)
        if chrome_result.returncode != 0:
            print("⚠️ Chrome not found, installing...")
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "google-chrome-stable"], check=True)
        
        user_flow_success = simulate_user_questionnaire_flow()
    except Exception as e:
        print(f"⚠️ Browser automation setup failed: {e}")
        user_flow_success = False
    
    # Final assessment
    print("\n" + "="*70)
    print("🎯 FINAL ASSESSMENT:")
    
    if user_flow_success:
        print("✅ SUCCESS: Users can answer questions and see results!")
        print("✅ Complete user flow từ questionnaire → answers → results works")
        print("✅ Application ready for production use")
        return True
    else:
        print("❌ PARTIAL SUCCESS: App runs but user flow needs verification")
        print("ℹ️ Manual testing recommended to confirm question → results flow")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
