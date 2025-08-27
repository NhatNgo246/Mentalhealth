import unittest
import os
import requests
import logging
from dotenv import load_dotenv

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAIMLChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Khởi tạo cho test suite"""
        load_dotenv()
        cls.api_key = os.getenv("AIML_API_KEY")
        cls.api_url = "https://aimlapi.com/api/chat"
        logger.info("Test suite initialized")

    def test_api_key_exists(self):
        """Kiểm tra API key đã được cấu hình"""
        logger.info("Testing API key configuration")
        self.assertIsNotNone(self.api_key, "AIML API key không được cấu hình")
        self.assertEqual(len(self.api_key), 32, "AIML API key không đúng độ dài")

    def test_api_connection(self):
        """Kiểm tra kết nối tới API"""
        logger.info("Testing API connection")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(
                self.api_url,
                headers=headers,
                timeout=10
            )
            self.assertIn(response.status_code, [200, 401, 404], 
                         f"API không phản hồi đúng: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.fail(f"Không thể kết nối tới API: {str(e)}")

    def test_chat_basic(self):
        """Test chat cơ bản"""
        logger.info("Testing basic chat")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": "Xin chào",
            "system_prompt": "Bạn là trợ lý hỗ trợ sức khỏe tâm thần, nói tiếng Việt.",
            "temperature": 0.7,
            "max_tokens": 300
        }
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=10
            )
            self.assertEqual(response.status_code, 200, 
                           f"API call failed: {response.text}")
            response_data = response.json()
            self.assertIn("response", response_data, 
                         "Response không có trường 'response'")
            self.assertIsInstance(response_data["response"], str,
                                "Response không phải là string")
            self.assertGreater(len(response_data["response"]), 0,
                             "Response rỗng")
            logger.info(f"Got response: {response_data['response'][:100]}...")
        except requests.exceptions.RequestException as e:
            self.fail(f"Lỗi khi gọi API: {str(e)}")

    def test_chat_context(self):
        """Test chat với context phức tạp"""
        logger.info("Testing chat with context")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": "Tôi cảm thấy căng thẳng và khó ngủ mấy ngày nay",
            "system_prompt": "Bạn là trợ lý hỗ trợ sức khỏe tâm thần, hãy đưa ra lời khuyên thiết thực và đồng cảm.",
            "temperature": 0.7,
            "max_tokens": 300
        }
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=10
            )
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertIn("response", response_data)
            content = response_data["response"].lower()
            # Kiểm tra các từ khóa quan trọng trong phản hồi
            expected_keywords = ["ngủ", "thư giãn", "stress", "căng thẳng"]
            found_keywords = [word for word in expected_keywords if word in content]
            self.assertGreater(len(found_keywords), 0, 
                             "Phản hồi không chứa từ khóa liên quan")
            logger.info(f"Response contains keywords: {found_keywords}")
        except requests.exceptions.RequestException as e:
            self.fail(f"Lỗi khi gọi API: {str(e)}")

    def test_error_handling(self):
        """Test xử lý lỗi"""
        logger.info("Testing error handling")
        headers = {
            "Authorization": "Bearer invalid_key",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": "Test message",
            "temperature": 0.7
        }
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=10
            )
            self.assertNotEqual(response.status_code, 200,
                              "API không nên chấp nhận key không hợp lệ")
        except requests.exceptions.RequestException as e:
            logger.info(f"Expected error received: {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
