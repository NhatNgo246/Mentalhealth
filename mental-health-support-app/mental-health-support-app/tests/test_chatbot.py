import os
import unittest
from unittest.mock import patch
import requests
from dotenv import load_dotenv
import sys
import logging

# Thêm đường dẫn để import được các module từ thư mục gốc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup cho toàn bộ test class"""
        load_dotenv()
        cls.api_key = os.getenv("CEREBRAS_API_KEY")
        cls.base_url = "https://cloud.cerebras.ai/api/v1/chat/completions"
        logger.info("Test setup completed")

    def test_api_key_exists(self):
        """Kiểm tra API key đã được cấu hình"""
        logger.info("Testing API key configuration")
        self.assertIsNotNone(self.api_key, "API key không được cấu hình")
        self.assertTrue(self.api_key.startswith("csk-"), "API key không đúng định dạng")

    def test_api_connection(self):
        """Kiểm tra kết nối tới API"""
        logger.info("Testing API connection")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(
                self.base_url,
                headers=headers,
                timeout=5
            )
            self.assertIn(response.status_code, [200, 401, 404], 
                         f"API không phản hồi đúng: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.fail(f"Không thể kết nối tới API: {str(e)}")

    def test_chat_completion(self):
        """Test chức năng chat completion"""
        logger.info("Testing chat completion")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                {"role": "system", "content": "Bạn là trợ lý hỗ trợ tinh tế."},
                {"role": "user", "content": "Xin chào"}
            ],
            "model": "cerebras/btlm-3b-8k-base",
            "temperature": 0.6,
            "max_tokens": 300
        }
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=10
            )
            self.assertEqual(response.status_code, 200, 
                           f"API call failed: {response.text}")
            response_data = response.json()
            self.assertIn("choices", response_data, 
                         "Response không có trường 'choices'")
            self.assertGreater(len(response_data["choices"]), 0, 
                             "Không có phản hồi trong choices")
        except requests.exceptions.RequestException as e:
            self.fail(f"Lỗi khi gọi API: {str(e)}")

    @patch("requests.post")
    def test_error_handling(self, mock_post):
        """Test xử lý lỗi"""
        logger.info("Testing error handling")
        # Test timeout
        mock_post.side_effect = requests.exceptions.Timeout
        with self.assertRaises(requests.exceptions.Timeout):
            self.test_chat_completion()

        # Test connection error
        mock_post.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.test_chat_completion()

if __name__ == '__main__':
    unittest.main(verbosity=2)
