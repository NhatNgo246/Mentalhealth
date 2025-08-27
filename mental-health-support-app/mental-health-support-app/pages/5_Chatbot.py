import os
import requests
import streamlit as st
from dotenv import load_dotenv
import logging
import json
from components.ui import app_header, show_disclaimer, load_css, create_info_card, create_progress_indicator

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(page_title="Chatbot Support", page_icon="💬", layout="centered")

# Load custom CSS
load_css()

# Constants
API_ENDPOINTS = {
    "openai": "https://api.openai.com/v1/chat/completions"
}
DEFAULT_MODELS = {
    "openai": "gpt-3.5-turbo"
}
FALLBACK_MODELS = {
    "openai": "gpt-3.5-turbo-16k"
}
MAX_RETRIES = 3
TIMEOUT = 30

# Cấu hình API mặc định
DEFAULT_API = "openai"

# Load biến môi trường từ file .env
load_dotenv()
logger.info("Loaded environment variables")

def call_chat_api(message, api_provider=DEFAULT_API, retry_count=0, use_fallback=False):
    """
    Gọi Chat API với retry và xử lý lỗi
    """
    # Lấy OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not configured")
    
    if not api_key:
        raise ValueError(f"{api_provider.upper()}_API_KEY not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Chuẩn bị system prompt
    system_prompt = (
        "Bạn là trợ lý hỗ trợ tinh tế về sức khỏe tâm thần, nói tiếng Việt. "
        "Hãy trả lời ngắn gọn, đồng cảm và khuyến khích. "
        "Không thay thế tư vấn chuyên môn. "
        "Nếu phát hiện dấu hiệu nguy cơ cao, luôn nhắc tìm hỗ trợ y tế."
    )
    
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "model": FALLBACK_MODELS[api_provider] if use_fallback else DEFAULT_MODELS[api_provider],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(
            API_ENDPOINTS[api_provider],
            headers=headers,
            json=data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 404 and not use_fallback:
            logger.warning(f"Model not found, trying fallback model")
            return call_chat_api(message, api_provider, retry_count, use_fallback=True)
        elif response.status_code in [429, 500, 502, 503, 504] and retry_count < MAX_RETRIES:
            logger.warning(f"API error {response.status_code}, retrying... ({retry_count + 1}/{MAX_RETRIES})")
            import time
            time.sleep(2 ** retry_count)  # Exponential backoff
            return call_chat_api(message, api_provider, retry_count + 1, use_fallback)
        else:
            error_response = response.json() if response.text else {"message": "Unknown error"}
            raise requests.exceptions.RequestException(
                f"API error: {response.status_code} - {json.dumps(error_response, ensure_ascii=False)}")
    
    except requests.exceptions.Timeout:
        if retry_count < MAX_RETRIES:
            logger.warning(f"Request timeout, retrying... ({retry_count + 1}/{MAX_RETRIES})")
            return call_chat_api(message, api_provider, retry_count + 1, use_fallback)
        raise
    
    except json.JSONDecodeError as e:
        raise requests.exceptions.RequestException(f"Invalid JSON response: {str(e)}")
    
    except Exception as e:
        raise requests.exceptions.RequestException(f"Unexpected error: {str(e)}")

def get_default_response():
    """
    Trả về gợi ý mặc định khi không có API
    """
    return [
        "- Thu nhỏ mục tiêu hôm nay, tập trung từng bước nhỏ.",
        "- Thở 4-4-6 trong 5 phút (4s hít vào, 4s giữ, 6s thở ra).",
        "- Liên hệ người thân tin cậy hoặc chuyên gia nếu cần.",
        "- Đảm bảo nghỉ ngơi và giấc ngủ đầy đủ.",
        "- Dành thời gian cho hoạt động thư giãn yêu thích."
    ]

# UI Components
app_header()
show_disclaimer()

# Progress indicator
create_progress_indicator(3, 3)

# Enhanced header for chatbot
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h2 style="color: var(--primary-color); margin: 0;">💬 Chatbot hỗ trợ tâm lý</h2>
    <p style="color: var(--text-secondary); margin: 0.5rem 0;">
        Trò chuyện với AI để nhận được lời khuyên và hỗ trợ ban đầu về sức khỏe tâm thần
    </p>
</div>
""", unsafe_allow_html=True)

# Info cards about chatbot
create_info_card(
    "Chatbot có thể giúp gì?",
    "• 💭 Lắng nghe và chia sẻ cảm xúc\n"
    "• 🧘 Gợi ý kỹ thuật thư giãn và mindfulness\n"
    "• 📚 Cung cấp thông tin về sức khỏe tâm thần\n"
    "• 🎯 Định hướng tìm kiếm sự hỗ trợ chuyên môn\n"
    "• ⚠️ Lưu ý: Không thay thế tư vấn y tế chuyên nghiệp",
    "🤖"
)

# Khởi tạo session state cho chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình Chatbot")
    
    # Chọn API provider (giấu vì chỉ dùng OpenAI)
    api_provider = "openai"
    
    # Kiểm tra API key
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if api_key:
        st.success("✅ OpenAI API đã sẵn sàng")
        st.markdown("**Model:** GPT-3.5 Turbo")
    else:
        st.warning("❌ Chưa cấu hình OpenAI API")
        st.markdown("Sẽ sử dụng phản hồi mặc định")
    
    # Chat controls
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📞 Hỗ trợ khẩn cấp")
    st.markdown("""
    **Đường dây nóng:**
    - 📞 115 (Cấp cứu)
    - 📞 1800 6969 (Tâm lý)
    - 📞 028 3821 2277 (BV Tâm thần)
    """)

# Chat container with enhanced styling
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history with enhanced styling
for i, message in enumerate(st.session_state.chat_history):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message slide-in" style="animation-delay: {i*0.1}s;">
            <div style="display: flex; align-items: flex-start;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">👤</span>
                <div>{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message slide-in" style="animation-delay: {i*0.1}s;">
            <div style="display: flex; align-items: flex-start;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">🤖</span>
                <div>{message["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
st.markdown("### 💬 Tin nhắn mới")
msg = st.text_area(
    "Bạn muốn chia sẻ hoặc hỏi gì?", 
    placeholder="Ví dụ: Tôi cảm thấy căng thẳng gần đây...",
    height=100
)

col1, col2 = st.columns([3, 1])
with col2:
    send_button = st.button("📤 Gửi", use_container_width=True)

if (send_button or msg) and msg and msg.strip():
    # Thêm tin nhắn người dùng vào lịch sử
    st.session_state.chat_history.append({"role": "user", "content": msg})

    # Xử lý và tạo phản hồi
    try:
        if not api_key:
            response = "\n".join(get_default_response())
            st.session_state.chat_history.append({"role": "assistant", "content": f"⚠️ Sử dụng phản hồi mặc định (chưa cấu hình API):\n\n{response}"})
        else:
            with st.spinner("🤖 Đang xử lý..."):
                response = call_chat_api(msg, api_provider)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    except requests.exceptions.Timeout:
        error_msg = "⚠️ Hết thời gian chờ. Vui lòng thử lại."
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        logger.error(error_msg)

    except requests.exceptions.RequestException as e:
        error_msg = f"⚠️ Lỗi kết nối API: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        logger.error(f"API error: {str(e)}")
        
    except Exception as e:
        error_msg = f"⚠️ Lỗi không xác định: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        logger.error(f"Unexpected error: {str(e)}")
    
    # Refresh page to show new messages
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Tips section
st.markdown("### 💡 Gợi ý sử dụng")
col1, col2 = st.columns(2)

with col1:
    create_info_card(
        "Cách đặt câu hỏi hiệu quả",
        "• Mô tả cụ thể cảm xúc và tình huống\n"
        "• Chia sẻ thời gian và mức độ ảnh hưởng\n"
        "• Hỏi về kỹ thuật cụ thể (thở, meditation)\n"
        "• Tìm hiểu về triệu chứng và cách xử lý",
        "💬"
    )

with col2:
    create_info_card(
        "Các chủ đề có thể thảo luận",
        "• Quản lý stress và lo âu\n"
        "• Kỹ thuật thư giãn và mindfulness\n"
        "• Cải thiện giấc ngủ và tâm trạng\n"
        "• Xây dựng thói quen tích cực\n"
        "• Tìm kiếm sự hỗ trợ chuyên môn",
        "📋"
    )
