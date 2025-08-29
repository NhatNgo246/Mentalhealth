"""
SOULFRIEND AI Chatbot
Intelligent mental health support chatbot
"""

import streamlit as st
import json
import random
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
try:
    load_css()
except:
    pass

# Header
app_header()

class MentalHealthChatbot:
    """AI Chatbot for mental health support"""
    
    def __init__(self):
        self.responses = {
            "greeting": [
                "Xin chào! Tôi là SoulBot, trợ lý AI của SOULFRIEND. Tôi có thể giúp gì cho bạn hôm nay?",
                "Chào bạn! Tôi ở đây để lắng nghe và hỗ trợ bạn. Bạn muốn chia sẻ điều gì?",
                "Xin chào! Rất vui được gặp bạn. Hãy cùng nói chuyện về sức khỏe tâm thần nhé."
            ],
            "anxiety": [
                "Tôi hiểu cảm giác lo âu có thể rất khó chịu. Hãy thử kỹ thuật thở 4-7-8: Hít vào 4 giây, giữ 7 giây, thở ra 8 giây.",
                "Lo âu là cảm xúc bình thường. Hãy thử tập trung vào hiện tại - nhìn xung quanh và kể tên 5 thứ bạn có thể nhìn thấy.",
                "Khi cảm thấy lo âu, hãy nhớ rằng: 'Cảm xúc này sẽ qua đi'. Bạn có muốn thử một bài tập thư giãn không?"
            ],
            "depression": [
                "Tôi hiểu bạn đang trải qua thời gian khó khăn. Điều quan trọng là bạn đã chia sẻ - đó là bước đầu rất dũng cảm.",
                "Trầm cảm có thể khiến mọi thứ trở nên tối tăm, nhưng hãy nhớ rằng có hy vọng và hỗ trợ. Bạn không cô đơn.",
                "Mỗi ngày nhỏ bé cũng là một chiến thắng. Hôm nay bạn đã làm được điều gì khiến bản thân tự hào?"
            ],
            "stress": [
                "Căng thẳng là phản ứng tự nhiên của cơ thể. Hãy thử chia nhỏ vấn đề thành các phần nhỏ hơn để dễ quản lý.",
                "Khi căng thẳng, não bộ cần nghỉ ngơi. Hãy thử nghỉ 5 phút và làm điều gì đó bạn thích.",
                "Bạn có thể kiểm soát được phản ứng của mình với căng thẳng. Hãy thử nói với bản thân: 'Tôi có thể vượt qua điều này'."
            ],
            "sleep": [
                "Giấc ngủ rất quan trọng cho sức khỏe tâm thần. Hãy thử tạo thói quen đi ngủ đều giờ và tránh màn hình trước khi ngủ 1 giờ.",
                "Nếu khó ngủ, hãy thử kỹ thuật thư giãn cơ từng phần - căng rồi thả lỏng từng nhóm cơ từ chân lên đầu.",
                "Môi trường ngủ lý tưởng: tối, mát, yên tĩnh. Bạn có thể điều chỉnh phòng ngủ để tối ưu không?"
            ],
            "support": [
                "Việc tìm kiếm hỗ trợ chuyên nghiệp là dấu hiệu của sự mạnh mẽ, không phải yếu đuối.",
                "Có nhiều nguồn hỗ trợ: tâm lý trị liệu, nhóm hỗ trợ, đường dây nóng. Bạn muốn tôi chia sẻ thông tin cụ thể không?",
                "Gia đình và bạn bè cũng có thể là nguồn hỗ trợ tuyệt vời. Bạn có người tin tưởng để chia sẻ không?"
            ],
            "crisis": [
                "Tôi rất lo lắng về bạn. Nếu bạn có ý định tự làm hại bản thân, hãy liên hệ ngay:",
                "📞 Đường dây nóng quốc gia: 1800-1612",
                "🏥 Cấp cứu: 115",
                "Bạn rất quan trọng và cuộc sống của bạn có giá trị. Hãy tìm kiếm hỗ trợ ngay lập tức."
            ],
            "positive": [
                "Thật tuyệt vời khi nghe bạn cảm thấy tích cực! Hãy ghi nhớ khoảnh khắc này.",
                "Tâm trạng tốt của bạn thật tuyệt! Bạn có muốn chia sẻ điều gì đã mang lại cảm giác này không?",
                "Rất vui khi thấy bạn có tinh thần tích cực. Hãy tiếp tục duy trì năng lượng này!"
            ],
            "default": [
                "Tôi hiểu bạn đang chia sẻ về cảm xúc của mình. Bạn có thể kể thêm về tình huống cụ thể không?",
                "Cảm ơn bạn đã tin tưởng chia sẻ với tôi. Điều gì đang khiến bạn cảm thấy như vậy?",
                "Tôi đang lắng nghe. Bạn có muốn nói thêm về những gì đang diễn ra trong cuộc sống của bạn không?"
            ]
        }
        
        self.keywords = {
            "greeting": ["xin chào", "chào", "hello", "hi", "hey"],
            "anxiety": ["lo âu", "lo lắng", "anxiety", "sợ hãi", "hoảng loạn", "căng thẳng tâm lý"],
            "depression": ["trầm cảm", "buồn", "depression", "tuyệt vọng", "cô đơn", "không còn hy vọng"],
            "stress": ["căng thẳng", "stress", "áp lực", "quá tải", "mệt mỏi"],
            "sleep": ["ngủ", "mất ngủ", "khó ngủ", "sleep", "insomnia", "tiểu đêm"],
            "support": ["giúp đỡ", "hỗ trợ", "support", "tư vấn", "liệu pháp"],
            "crisis": ["tự tử", "suicide", "tự làm hại", "kết thúc cuộc đời", "không muốn sống"],
            "positive": ["vui", "happy", "hạnh phúc", "tốt", "tuyệt vời", "tích cực"]
        }
    
    def analyze_sentiment(self, message):
        """Analyze message sentiment and categorize"""
        message_lower = message.lower()
        
        # Crisis detection (highest priority)
        for keyword in self.keywords["crisis"]:
            if keyword in message_lower:
                return "crisis"
        
        # Check other categories
        for category, keywords in self.keywords.items():
            if category == "crisis":
                continue
            for keyword in keywords:
                if keyword in message_lower:
                    return category
        
        return "default"
    
    def get_response(self, message, user_context=None):
        """Get appropriate response based on message analysis"""
        category = self.analyze_sentiment(message)
        
        # Select response
        responses = self.responses[category]
        response = random.choice(responses)
        
        # Add personalized elements if context available
        if user_context:
            if user_context.get('name'):
                response = response.replace("bạn", user_context['name'])
        
        return {
            "response": response,
            "category": category,
            "suggestions": self.get_suggestions(category),
            "resources": self.get_resources(category)
        }
    
    def get_suggestions(self, category):
        """Get follow-up suggestions based on category"""
        suggestions = {
            "anxiety": [
                "Thử bài tập thở 4-7-8",
                "Kỹ thuật grounding 5-4-3-2-1",
                "Nghe nhạc thư giãn",
                "Đi bộ ngoài trời"
            ],
            "depression": [
                "Viết nhật ký cảm xúc",
                "Gọi điện cho bạn bè",
                "Tham gia hoạt động yêu thích",
                "Tìm kiếm hỗ trợ chuyên nghiệp"
            ],
            "stress": [
                "Chia nhỏ công việc",
                "Thiết lập ưu tiên",
                "Nghỉ ngơi đầy đủ",
                "Tập thể dục nhẹ"
            ],
            "sleep": [
                "Tạo thói quen ngủ đều giờ",
                "Tránh caffeine buổi tối",
                "Thiền trước khi ngủ",
                "Đọc sách thay vì xem điện thoại"
            ]
        }
        
        return suggestions.get(category, [])
    
    def get_resources(self, category):
        """Get relevant resources based on category"""
        resources = {
            "crisis": [
                {
                    "name": "Đường dây nóng quốc gia",
                    "contact": "1800-1612",
                    "description": "Hỗ trợ 24/7"
                },
                {
                    "name": "Cấp cứu",
                    "contact": "115",
                    "description": "Dịch vụ cấp cứu"
                }
            ],
            "anxiety": [
                {
                    "name": "Ứng dụng thiền Headspace",
                    "contact": "headspace.com",
                    "description": "Bài tập mindfulness"
                }
            ],
            "depression": [
                {
                    "name": "Viện Sức khỏe Tâm thần",
                    "contact": "028-3829-2295",
                    "description": "Tư vấn chuyên nghiệp"
                }
            ]
        }
        
        return resources.get(category, [])

def chatbot_interface():
    """Main chatbot interface"""
    st.title("🤖 SoulBot - Trợ lý AI")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = MentalHealthChatbot()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'user_context' not in st.session_state:
        st.session_state.user_context = {}
    
    chatbot = st.session_state.chatbot
    
    # Sidebar with user context
    with st.sidebar:
        st.header("👤 Thông tin cá nhân")
        
        name = st.text_input("Tên của bạn (tùy chọn)", value=st.session_state.user_context.get('name', ''))
        if name:
            st.session_state.user_context['name'] = name
        
        mood = st.selectbox(
            "Tâm trạng hiện tại:",
            ["Chọn tâm trạng", "😊 Vui vẻ", "😐 Bình thường", "😔 Buồn", "😰 Lo âu", "😫 Căng thẳng", "😴 Mệt mỏi"]
        )
        if mood != "Chọn tâm trạng":
            st.session_state.user_context['mood'] = mood
        
        st.markdown("---")
        st.markdown("### 🆘 Trường hợp khẩn cấp")
        st.markdown("**Đường dây nóng 24/7:**")
        st.markdown("📞 **1800-1612**")
        st.markdown("🏥 **Cấp cứu: 115**")
        
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat interface
    st.markdown("### 💬 Cuộc trò chuyện")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_history:
            # Welcome message
            with st.chat_message("assistant"):
                st.write("👋 Xin chào! Tôi là SoulBot, trợ lý AI của SOULFRIEND. Tôi ở đây để lắng nghe và hỗ trợ bạn về sức khỏe tâm thần. Bạn muốn chia sẻ điều gì hôm nay?")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["user_message"])
            
            with st.chat_message("assistant"):
                st.write(chat["bot_response"]["response"])
                
                # Show suggestions if available
                if chat["bot_response"]["suggestions"]:
                    st.markdown("**💡 Gợi ý:**")
                    for suggestion in chat["bot_response"]["suggestions"]:
                        st.write(f"• {suggestion}")
                
                # Show resources if available
                if chat["bot_response"]["resources"]:
                    st.markdown("**📋 Tài nguyên hữu ích:**")
                    for resource in chat["bot_response"]["resources"]:
                        st.write(f"• **{resource['name']}**: {resource['contact']} - {resource['description']}")
    
    # Chat input
    user_input = st.chat_input("Nhập tin nhắn của bạn...")
    
    if user_input:
        # Get bot response
        bot_response = chatbot.get_response(user_input, st.session_state.user_context)
        
        # Add to chat history
        st.session_state.chat_history.append({
            "timestamp": datetime.now(),
            "user_message": user_input,
            "bot_response": bot_response
        })
        
        # Rerun to show new message
        st.rerun()
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Hành động nhanh")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("😰 Tôi đang lo âu"):
            bot_response = chatbot.get_response("Tôi đang cảm thấy lo âu", st.session_state.user_context)
            st.session_state.chat_history.append({
                "timestamp": datetime.now(),
                "user_message": "Tôi đang cảm thấy lo âu",
                "bot_response": bot_response
            })
            st.rerun()
    
    with col2:
        if st.button("😔 Tôi cảm thấy buồn"):
            bot_response = chatbot.get_response("Tôi đang cảm thấy buồn và trầm cảm", st.session_state.user_context)
            st.session_state.chat_history.append({
                "timestamp": datetime.now(),
                "user_message": "Tôi đang cảm thấy buồn",
                "bot_response": bot_response
            })
            st.rerun()
    
    with col3:
        if st.button("😫 Tôi căng thẳng"):
            bot_response = chatbot.get_response("Tôi đang rất căng thẳng", st.session_state.user_context)
            st.session_state.chat_history.append({
                "timestamp": datetime.now(),
                "user_message": "Tôi đang căng thẳng",
                "bot_response": bot_response
            })
            st.rerun()
    
    with col4:
        if st.button("😴 Tôi mất ngủ"):
            bot_response = chatbot.get_response("Tôi gặp vấn đề về giấc ngủ", st.session_state.user_context)
            st.session_state.chat_history.append({
                "timestamp": datetime.now(),
                "user_message": "Tôi mất ngủ",
                "bot_response": bot_response
            })
            st.rerun()
    
    # Chatbot analytics
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📊 Phân tích cuộc trò chuyện")
        
        # Analyze chat patterns
        categories = [chat["bot_response"]["category"] for chat in st.session_state.chat_history]
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏷️ Chủ đề thảo luận:**")
            for category, count in category_counts.items():
                st.write(f"• {category.title()}: {count} lần")
        
        with col2:
            st.markdown("**📈 Thống kê:**")
            st.write(f"• Tổng tin nhắn: {len(st.session_state.chat_history)}")
            st.write(f"• Thời gian trò chuyện: {(datetime.now() - st.session_state.chat_history[0]['timestamp']).seconds // 60} phút")
            
            # Mood tracking
            if 'mood' in st.session_state.user_context:
                st.write(f"• Tâm trạng hiện tại: {st.session_state.user_context['mood']}")

# Main function
def main():
    chatbot_interface()

if __name__ == "__main__":
    main()
