#!/bin/bash

echo "=== Bắt đầu test AIML Chatbot ==="

# Kiểm tra môi trường
echo "1. Kiểm tra biến môi trường..."
if [ -z "$AIML_API_KEY" ]; then
    echo "❌ AIML_API_KEY chưa được cấu hình"
    exit 1
else
    echo "✅ AIML_API_KEY đã được cấu hình"
fi

# Test kết nối API
echo -e "\n2. Test kết nối API..."
response=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $AIML_API_KEY" \
    -H "Content-Type: application/json" \
    "https://aimlapi.com/api/chat")

if [ "$response" == "200" ] || [ "$response" == "401" ] || [ "$response" == "404" ]; then
    echo "✅ API có phản hồi (HTTP $response)"
else
    echo "❌ API không phản hồi đúng (HTTP $response)"
fi

# Test chat đơn giản
echo -e "\n3. Test chat đơn giản..."
chat_response=$(curl -s -X POST \
    -H "Authorization: Bearer $AIML_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "prompt": "Xin chào",
        "system_prompt": "Bạn là trợ lý hỗ trợ sức khỏe tâm thần, nói tiếng Việt.",
        "temperature": 0.7,
        "max_tokens": 300
    }' \
    "https://aimlapi.com/api/chat")

if [[ $chat_response == *"response"* ]]; then
    echo "✅ Chat hoạt động"
    echo "Phản hồi: $(echo $chat_response | python3 -c "import sys, json; print(json.load(sys.stdin)['response'][:100] + '...')")"
else
    echo "❌ Chat không hoạt động"
    echo "Lỗi: $chat_response"
fi

echo -e "\n=== Kết thúc test ==="
