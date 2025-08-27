#!/bin/bash

# Di chuyển vào thư mục tests
cd "$(dirname "$0")/tests"

echo "=== Bắt đầu kiểm tra chatbot ==="
echo "1. Kiểm tra môi trường..."
python3 -c "import requests; import dotenv" 2>/dev/null || {
    echo "Cài đặt dependencies..."
    pip install requests python-dotenv
}

echo "2. Chạy tests..."
python3 -m unittest test_chatbot.py -v

echo "=== Kết thúc kiểm tra ==="
