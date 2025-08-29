"""
SOULFRIEND Chatbot AI
Intelligent conversational support for mental health
"""

import streamlit as st
import sys
import os
from datetime import datetime
import random

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# App header
app_header()

# Chatbot responses database
RESPONSES = {
    "greeting": [
        "Xin chào! Tôi là SOUL AI, trợ lý tâm lý của bạn. Hôm nay bạn cảm thấy thế nào?",
        "Chào bạn! Tôi ở đây để lắng nghe và hỗ trợ bạn. Có gì bạn muốn chia sẻ không?",
        "Hello! Tôi là SOUL AI. Tôi sẵn sàng trò chuyện và hỗ trợ bạn về sức khỏe tâm lý."
    ],
    "anxiety": [
        "Tôi hiểu bạn đang cảm thấy lo lắng. Hãy thử thở sâu: hít vào 4 giây, giữ 4 giây, thở ra 6 giây.",
        "Lo lắng là cảm xúc bình thường. Hãy tập trung vào hiện tại - những gì bạn có thể nhìn, nghe, cảm nhận ngay bây giờ.",
        "Khi lo lắng, hãy tự hỏi: 'Điều này có thật sự quan trọng trong 5 năm nữa không?' Nhiều khi câu trả lời sẽ giúp bạn thấy nhẹ nhõm hơn."
    ],
    "depression": [
        "Tôi hiểu bạn đang trải qua thời gian khó khăn. Bạn đã rất dũng cảm khi chia sẻ điều này.",
        "Trầm cảm không phải là lỗi của bạn. Đó là tình trạng có thể điều trị được. Bạn không đơn độc trong cuộc chiến này.",
        "Mỗi ngày bạn vượt qua đều là một chiến thắng. Hãy tự thưởng cho bản thân những điều nhỏ nhưng có ý nghĩa."
    ],
    "stress": [
        "Stress có thể áp đảo, nhưng bạn mạnh mẽ hơn bạn nghĩ. Hãy chia nhỏ vấn đề thành các bước nhỏ hơn.",
        "Khi stress, hãy dành 5 phút để làm điều gì đó bạn yêu thích - nghe nhạc, vẽ, hay chỉ đơn giản là ngắm cảnh.",
        "Hãy nhớ rằng bạn không thể kiểm soát mọi thứ, nhưng bạn có thể kiểm soát cách phản ứng của mình."
    ],
    "support": [
        "Bạn đã làm rất tốt khi tìm kiếm sự hỗ trợ. Đó là dấu hiệu của sức mạnh, không phải yếu đuối.",
        "Tôi ở đây để lắng nghe bạn. Không có gì bạn chia sẻ là quá nhỏ nhặt hay không quan trọng.",
        "Mỗi người đều có những thời điểm khó khăn. Điều quan trọng là bạn không đi qua chúng một mình."
    ]
}

def generate_response(user_input):
    """Generate chatbot response based on user input"""
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ["xin chào", "hello", "chào", "hi"]):
        return random.choice(RESPONSES["greeting"])
    elif any(word in user_input_lower for word in ["lo lắng", "anxiety", "걱정", "sợ hãi"]):
        return random.choice(RESPONSES["anxiety"])
    elif any(word in user_input_lower for word in ["buồn", "trầm cảm", "depression", "tuyệt vọng"]):
        return random.choice(RESPONSES["depression"])
    elif any(word in user_input_lower for word in ["stress", "căng thẳng", "áp lực", "mệt mỏi"]):
        return random.choice(RESPONSES["stress"])
    else:
        return random.choice(RESPONSES["support"])

def chatbot_main():
    """Main chatbot interface"""
    st.markdown("# 💬 SOUL AI Chatbot")
    st.markdown("#### Trợ lý AI hỗ trợ sức khỏe tâm lý 24/7")
    st.markdown("---")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": "assistant",
            "message": "Xin chào! Tôi là SOUL AI, trợ lý tâm lý của bạn. Hôm nay bạn cảm thấy thế nào?",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"""
                <div style="text-align: right; margin: 10px 0;">
                    <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">
                        {chat["message"]}
                    </div>
                    <div style="font-size: 0.8em; color: #666; margin-top: 2px;">
                        {chat["timestamp"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: left; margin: 10px 0;">
                    <div style="background-color: #f1f3f4; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">
                        🤖 {chat["message"]}
                    </div>
                    <div style="font-size: 0.8em; color: #666; margin-top: 2px;">
                        {chat["timestamp"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("💭 Chia sẻ cảm xúc của bạn...", key="chat_input", placeholder="Hôm nay tôi cảm thấy...")
    
    with col2:
        send_button = st.button("📤 Gửi", type="primary")
    
    # Process user input
    if send_button and user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "message": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Generate AI response
        ai_response = generate_response(user_input)
        
        # Add AI response
        st.session_state.chat_history.append({
            "role": "assistant",
            "message": ai_response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Clear input and rerun
        st.rerun()
    
    # Quick response buttons
    st.markdown("### 🚀 Phản hồi nhanh")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("😰 Tôi đang lo lắng"):
            st.session_state.chat_history.append({
                "role": "user",
                "message": "Tôi đang cảm thấy lo lắng",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            ai_response = generate_response("lo lắng")
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": ai_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col2:
        if st.button("😢 Tôi buồn"):
            st.session_state.chat_history.append({
                "role": "user",
                "message": "Tôi đang cảm thấy buồn",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            ai_response = generate_response("buồn")
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": ai_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col3:
        if st.button("😵 Tôi stress"):
            st.session_state.chat_history.append({
                "role": "user",
                "message": "Tôi đang cảm thấy stress",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            ai_response = generate_response("stress")
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": ai_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col4:
        if st.button("🆘 Cần hỗ trợ"):
            st.session_state.chat_history.append({
                "role": "user",
                "message": "Tôi cần hỗ trợ",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            ai_response = generate_response("hỗ trợ")
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": ai_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Xóa lịch sử chat", type="secondary"):
        st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": "assistant",
            "message": "Xin chào! Tôi là SOUL AI, trợ lý tâm lý của bạn. Hôm nay bạn cảm thấy thế nào?",
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.rerun()

if __name__ == "__main__":
    chatbot_main()
