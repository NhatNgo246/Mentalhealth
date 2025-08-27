"""
Advanced UI/UX Components - 2025 Premium Experience
Nâng cao trải nghiệm người dùng với logic thông minh và tương tác động
"""

import streamlit as st
import time
from datetime import datetime
import json

class SmartUIExperience:
    """Hệ thống UI/UX thông minh với logic nâng cao"""
    
    def __init__(self):
        self.user_journey = []
        self.interaction_history = []
        
    def track_user_interaction(self, action: str, component: str, value=None):
        """Theo dõi hành vi người dùng để cải thiện UX"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'component': component,
            'value': value
        }
        if 'user_interactions' not in st.session_state:
            st.session_state.user_interactions = []
        st.session_state.user_interactions.append(interaction)

def load_premium_css():
    """Load CSS nâng cao với animations và responsive design"""
    premium_css = """
    <style>
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        --error-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        --info-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        --spacing-xxl: 3rem;
        
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
        --shadow-md: 0 4px 8px rgba(0,0,0,0.12);
        --shadow-lg: 0 8px 16px rgba(0,0,0,0.15);
        --shadow-xl: 0 12px 24px rgba(0,0,0,0.18);
        
        --font-xs: 0.75rem;
        --font-sm: 0.875rem;
        --font-md: 1rem;
        --font-lg: 1.125rem;
        --font-xl: 1.25rem;
        --font-xxl: 2rem;
        
        --text-primary: #1f2937;
        --text-secondary: #4b5563;
        --text-muted: #9ca3af;
    }

    /* Smooth animations */
    .smooth-entrance {
        animation: smoothEnter 0.6s ease-out;
    }
    
    @keyframes smoothEnter {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .pulse-glow {
        animation: pulseGlow 2s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.4); }
        50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.8); }
    }

    /* Interactive Cards */
    .interactive-card {
        background: white;
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-md);
        border: 1px solid #f3f4f6;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .interactive-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-xl);
        border-color: #667eea;
    }
    
    .interactive-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .interactive-card:hover::before {
        left: 100%;
    }

    /* Progress Indicators */
    .progress-ring {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: conic-gradient(#667eea 0deg, #f3f4f6 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .progress-ring::after {
        content: '';
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: white;
        position: absolute;
    }

    /* Mood Tracker */
    .mood-selector {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: var(--spacing-sm);
        margin: var(--spacing-md) 0;
    }
    
    .mood-option {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: var(--radius-md);
        padding: var(--spacing-md);
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: var(--font-lg);
    }
    
    .mood-option:hover {
        border-color: #667eea;
        background: #f8fafc;
        transform: scale(1.05);
    }
    
    .mood-option.selected {
        border-color: #667eea;
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-lg);
    }

    /* Smart Notifications */
    .smart-notification {
        background: var(--info-gradient);
        color: white;
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
        margin: var(--spacing-sm) 0;
        position: relative;
        overflow: hidden;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .interactive-card {
            padding: var(--spacing-md);
            margin: var(--spacing-sm) 0;
        }
        
        .mood-selector {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    /* Dark Mode Support */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --text-muted: #6b7280;
        }
        
        .interactive-card {
            background: #1f2937;
            border-color: #374151;
        }
    }

    /* Accessibility Improvements */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    .focus-visible {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
    </style>
    """
    st.markdown(premium_css, unsafe_allow_html=True)

def create_smart_hero(title: str, subtitle: str, description: str, show_animation: bool = True):
    """Hero section thông minh với animations"""
    animation_class = "smooth-entrance float-animation" if show_animation else ""
    
    st.markdown(f"""
    <div class="interactive-card {animation_class}" style="
        background: var(--primary-gradient);
        color: white;
        text-align: center;
        margin: var(--spacing-lg) 0;
        border: none;
    ">
        <div class="sr-only">Main hero section</div>
        <h1 style="margin: 0; font-size: var(--font-xxl); font-weight: 700;">
            {title}
        </h1>
        <p style="margin: var(--spacing-sm) 0; font-size: var(--font-lg); opacity: 0.9;">
            {subtitle}
        </p>
        <div style="font-size: var(--font-md); opacity: 0.8; line-height: 1.6;">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_encouraging_message(mood_value, mood_label):
    """Trả về câu an ủi, động viên phù hợp với tâm trạng"""
    messages = {
        5: [  # Rất vui
            "🌟 Thật tuyệt vời! Hãy giữ gìn tinh thần tích cực này nhé!",
            "✨ Năng lượng tích cực của bạn thật đáng ngưỡng mộ!",
            "🎉 Niềm vui của bạn chắc chắn sẽ lan tỏa đến mọi người!",
            "🌈 Hôm nay là một ngày tuyệt vời, và bạn đang tỏa sáng!",
            "💫 Hạnh phúc bắt đầu từ nội tâm, và bạn đã làm được điều đó!",
            "🌺 Nụ cười của bạn là liều thuốc tốt nhất cho tâm hồn!",
            "🦋 Bạn đang bay cao như chú bướm xinh đẹp!"
        ],
        4: [  # Vui vẻ
            "😊 Thật tốt khi thấy bạn có tâm trạng vui vẻ!",
            "🌸 Sự tích cực của bạn làm ngày hôm nay thêm đẹp!",
            "💖 Hãy cứ giữ nụ cười này nhé, nó rất đáng quý!",
            "🌺 Tâm trạng tốt là món quà tuyệt vời bạn dành cho bản thân!",
            "🍀 May mắn đang mỉm cười với bạn hôm nay!",
            "☀️ Ánh nắng trong lòng bạn đang sưởi ấm cả thế giới!",
            "🌻 Bạn như bông hướng dương luôn hướng về phía mặt trời!"
        ],
        3: [  # Bình thường
            "🤗 Không sao, có những ngày như vậy là bình thường!",
            "🌱 Mỗi ngày đều có giá trị riêng, kể cả những ngày bình thường!",
            "💙 Đôi khi việc cảm thấy bình thường cũng là một điều tốt!",
            "🕊️ Hãy để tâm hồn nghỉ ngơi, ngày mai sẽ khác!",
            "🌤️ Những ngày êm đềm cũng cần thiết cho tâm hồn!",
            "🌊 Như sóng biển êm ả, tâm hồn bạn đang bình yên!",
            "🍃 Đôi khi sự tĩnh lặng mang lại nhiều điều tốt đẹp!"
        ],
        2: [  # Hơi buồn
            "🤲 Mình hiểu bạn đang cảm thấy không thoải mái. Hãy nhớ rằng cảm xúc này sẽ qua!",
            "🌙 Buồn bã là cảm xúc bình thường, đừng tự trách bản thân nhé!",
            "💝 Bạn không đơn độc, luôn có người quan tâm và sẵn sàng lắng nghe!",
            "🕯️ Ánh sáng sẽ lại tỏa sáng, ngay cả sau những khoảnh khắc tối tăm!",
            "🌿 Hãy dành thời gian chăm sóc bản thân, bạn xứng đáng được yêu thương!",
            "🌧️ Mưa sẽ tạnh, và cầu vồng sẽ xuất hiện sau cơn mưa!",
            "💜 Tâm hồn bạn cần được âu yếm, hãy nhẹ nhàng với bản thân!"
        ],
        1: [  # Buồn
            "🤗 Mình thật sự hiểu và đồng cảm với những gì bạn đang trải qua!",
            "💚 Bạn rất mạnh mẽ khi chia sẻ cảm xúc này. Đó là bước đầu để khỏe mạnh hơn!",
            "🌅 Sau mỗi đêm tối luôn có bình minh. Bạn sẽ vượt qua được!",
            "🫂 Đừng cô đơn trong lúc này, hãy tìm kiếm sự hỗ trợ từ những người thân yêu!",
            "🌱 Từ những khó khăn này, bạn sẽ trở nên mạnh mẽ và kiên cường hơn!",
            "💞 Bạn có giá trị và được yêu thương, ngay cả khi bạn không cảm nhận được!",
            "🕊️ Hãy để những giọt nước mắt cuốn đi nỗi buồn, tâm hồn sẽ nhẹ nhõm hơn!",
            "🌈 Dù bây giờ trời có mưa, nhưng cầu vồng sẽ xuất hiện sau cơn mưa!"
        ]
    }
    
    import random
    return random.choice(messages.get(mood_value, messages[3]))

def get_helpful_tips(mood_value):
    """Trả về gợi ý hữu ích phù hợp với tâm trạng"""
    if mood_value >= 4:
        return {
            "title": "🌟 Cách duy trì tâm trạng tích cực:",
            "tips": [
                "📝 Viết nhật ký về những điều tốt đẹp hôm nay",
                "🤝 Chia sẻ niềm vui với người thân",
                "🎯 Đặt mục tiêu nhỏ cho ngày mai",
                "🙏 Thực hành lòng biết ơn",
                "🎨 Tham gia hoạt động sáng tạo",
                "🌱 Chăm sóc cây cối hoặc thú cưng"
            ]
        }
    elif mood_value == 3:
        return {
            "title": "💡 Cách cải thiện tâm trạng:",
            "tips": [
                "🚶‍♀️ Đi dạo ngoài trời hoặc tập thể dục nhẹ",
                "📞 Gọi điện cho bạn bè lâu ngày chưa gặp",
                "🎵 Nghe nhạc yêu thích hoặc xem phim vui",
                "🍃 Thực hành thiền hoặc yoga",
                "📚 Đọc sách hoặc học điều gì đó mới",
                "🍰 Nấu món ăn yêu thích"
            ]
        }
    else:
        return {
            "title": "💪 Cách vượt qua giai đoạn khó khăn:",
            "tips": [
                "🧘‍♀️ Thực hành hít thở sâu (4-7-8)",
                "📞 Liên hệ với người bạn tin tương",
                "📝 Viết ra những suy nghĩ và cảm xúc",
                "🚶‍♀️ Đi dạo trong tự nhiên",
                "🫖 Uống trà thảo mộc ấm",
                "🛁 Tắm nước ấm và nghỉ ngơi",
                "💭 Nhắc nhở bản thân về những điều tích cực",
                "🎧 Nghe nhạc thư giãn hoặc podcast tích cực"
            ]
        }

def create_smart_mood_tracker():
    """Mood tracker thông minh với native Streamlit components"""
    
    st.markdown("### 🌈 Hôm nay tâm trạng bạn thế nào?")
    
    moods = [
        {"emoji": "😄", "label": "Rất vui", "value": 5},
        {"emoji": "😊", "label": "Vui vẻ", "value": 4},
        {"emoji": "😐", "label": "Bình thường", "value": 3},
        {"emoji": "😔", "label": "Hơi buồn", "value": 2},
        {"emoji": "😢", "label": "Buồn", "value": 1}
    ]
    
    cols = st.columns(len(moods))
    selected_mood = None
    
    for i, (col, mood) in enumerate(zip(cols, moods)):
        with col:
            # Tạo style đặc biệt cho từng emoji button
            button_style = ""
            if mood['value'] >= 4:
                button_style = "🟢"  # Xanh cho tích cực
            elif mood['value'] == 3:
                button_style = "🟡"  # Vàng cho bình thường
            else:
                button_style = "🔴"  # Đỏ cho tiêu cực
                
            if st.button(
                f"{mood['emoji']}\n{mood['label']}\n{button_style}", 
                key=f"mood_{i}",
                use_container_width=True,
                help=f"Bấm để chia sẻ tâm trạng: {mood['label']}"
            ):
                selected_mood = mood
                st.session_state.current_mood = mood
                # Hiển thị animation khi chọn
                st.balloons() if mood['value'] >= 4 else (st.snow() if mood['value'] <= 2 else None)
    
    if selected_mood:
        SmartUIExperience().track_user_interaction("mood_select", "mood_tracker", selected_mood)
        
        # Hiển thị câu động viên, an ủi phù hợp
        encouraging_msg = get_encouraging_message(selected_mood['value'], selected_mood['label'])
        
        # Hiển thị với style đẹp tùy theo tâm trạng
        if selected_mood['value'] >= 4:
            st.success(f"**{selected_mood['emoji']} {selected_mood['label']}**\n\n{encouraging_msg}")
        elif selected_mood['value'] == 3:
            st.info(f"**{selected_mood['emoji']} {selected_mood['label']}**\n\n{encouraging_msg}")
        else:
            st.warning(f"**{selected_mood['emoji']} {selected_mood['label']}**\n\n{encouraging_msg}")
            
        # Thêm một số gợi ý hữu ích
        tips = get_helpful_tips(selected_mood['value'])
        
        with st.expander(f"💡 {tips['title']}"):
            if selected_mood['value'] <= 2:
                st.markdown("**🆘 Quan trọng:** Nếu bạn có ý định tự gây hại, hãy liên hệ ngay:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("📞 **Hotline tâm lý:** 1900-0147")
                with col2:
                    st.markdown("🏥 **Cấp cứu:** 115")
                st.markdown("---")
            
            col1, col2 = st.columns(2)
            mid_point = len(tips['tips']) // 2
            
            with col1:
                for tip in tips['tips'][:mid_point]:
                    st.markdown(f"• {tip}")
            with col2:
                for tip in tips['tips'][mid_point:]:
                    st.markdown(f"• {tip}")
        
        # Thêm nút để thay đổi tâm trạng
        if st.button("🔄 Chọn lại tâm trạng", key="reset_mood"):
            if 'current_mood' in st.session_state:
                del st.session_state.current_mood
            if 'mood_message' in st.session_state:
                del st.session_state.mood_message
            st.rerun()
        
        # Lưu vào session state để hiển thị lại
        st.session_state.current_mood = selected_mood
        st.session_state.mood_message = encouraging_msg
    
    # Hiển thị lại mood đã chọn nếu có
    elif hasattr(st.session_state, 'current_mood') and st.session_state.current_mood:
        mood = st.session_state.current_mood
        msg = getattr(st.session_state, 'mood_message', get_encouraging_message(mood['value'], mood['label']))
        
        if mood['value'] >= 4:
            st.success(f"**{mood['emoji']} {mood['label']}**\n\n{msg}")
        elif mood['value'] == 3:
            st.info(f"**{mood['emoji']} {mood['label']}**\n\n{msg}")
        else:
            st.warning(f"**{mood['emoji']} {mood['label']}**\n\n{msg}")
        
        tips = get_helpful_tips(mood['value'])
        with st.expander(f"💡 {tips['title']}"):
            if mood['value'] <= 2:
                st.markdown("**🆘 Quan trọng:** Nếu bạn có ý định tự gây hại, hãy liên hệ ngay:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("📞 **Hotline tâm lý:** 1900-0147")
                with col2:
                    st.markdown("🏥 **Cấp cứu:** 115")
                st.markdown("---")
            
            col1, col2 = st.columns(2)
            mid_point = len(tips['tips']) // 2
            
            with col1:
                for tip in tips['tips'][:mid_point]:
                    st.markdown(f"• {tip}")
            with col2:
                for tip in tips['tips'][mid_point:]:
                    st.markdown(f"• {tip}")
        
        # Nút thay đổi tâm trạng
        if st.button("🔄 Chọn lại tâm trạng", key="reset_mood_display"):
            if 'current_mood' in st.session_state:
                del st.session_state.current_mood
            if 'mood_message' in st.session_state:
                del st.session_state.mood_message
            st.rerun()

def create_consent_agreement_form():
    """Hiển thị bảng đồng thuận chi tiết"""
    st.markdown("# 📋 Bảng Đồng Thuận Tham Gia Đánh Giá")
    st.markdown("*SoulFriend - Hỗ trợ Sức khỏe Tâm lý*")
    
    st.markdown("---")
    
    # Giới thiệu ngắn gọn
    st.info("""
    🎯 **Trước khi bắt đầu**, vui lòng đọc kỹ thông tin dưới đây và xác nhận đồng ý. 
    Điều này giúp đảm bảo bạn hiểu rõ về quá trình đánh giá và quyền lợi của mình.
    """)
    
    # Thông tin chi tiết về nghiên cứu
    st.markdown("### 🔬 **Thông tin về đánh giá tâm lý**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Mục đích và nội dung:**
        - ✅ Sàng lọc mức độ trầm cảm, lo âu và căng thẳng
        - ✅ Sử dụng thang đo DASS-21 chuẩn quốc tế
        - ✅ Cung cấp thông tin hỗ trợ tâm lý cá nhân hóa
        - ✅ Đề xuất các biện pháp cải thiện phù hợp
        
        **⏱️ Thời gian thực hiện:**
        - 📝 21 câu hỏi ngắn gọn, dễ hiểu
        - ⏰ Hoàn thành trong 5-10 phút
        - 🔄 Có thể tạm dừng và tiếp tục bất cứ lúc nào
        """)
    
    with col2:
        st.markdown("""
        **🔒 Quyền riêng tư và bảo mật:**
        - 🛡️ Dữ liệu được mã hóa và bảo mật tuyệt đối
        - 🚫 Không thu thập thông tin cá nhân
        - 💾 Không lưu trữ dữ liệu vĩnh viễn
        - 🔓 Bạn có thể dừng bất cứ lúc nào
        
        **📞 Hỗ trợ khẩn cấp:**
        - 🆘 Hotline tâm lý 24/7: **1900-0147**
        - 🏥 Cấp cứu: **115**
        - 👨‍⚕️ Tư vấn trực tuyến: **1900-1234**
        """)
    
    st.markdown("---")
    
    # Lưu ý quan trọng
    st.error("""
    ⚠️ **LưU Ý QUAN TRỌNG:**
    
    Công cụ này chỉ có tính chất **sàng lọc và tham khảo**, không thay thế cho chẩn đoán y khoa chính thức. 
    Nếu bạn có dấu hiệu nghiêm trọng hoặc ý định tự gây hại, hãy liên hệ ngay với chuyên gia y tế!
    """)
    
    st.markdown("---")
    
    # Các điều khoản đồng ý
    st.markdown("### ✅ **Xác nhận đồng ý tham gia**")
    st.markdown("*Vui lòng đọc kỹ và tích chọn TẤT CẢ các mục sau để tiếp tục:*")
    
    # Container cho các checkbox
    with st.container():
        # Sử dụng checkboxes cho từng điều khoản
        consent_items = []
        
        st.markdown("**📋 Về nội dung đánh giá:**")
        consent_1 = st.checkbox(
            "🔍 Tôi hiểu đây là công cụ sàng lọc tâm lý, không phải chẩn đoán y khoa",
            key="consent_1"
        )
        consent_items.append(consent_1)
        
        consent_2 = st.checkbox(
            "📊 Tôi sẽ trả lời các câu hỏi một cách trung thực về tình trạng tâm lý hiện tại",
            key="consent_2"
        )
        consent_items.append(consent_2)
        
        st.markdown("**🔐 Về quyền riêng tư:**")
        consent_3 = st.checkbox(
            "�️ Tôi hiểu rằng dữ liệu sẽ được bảo mật và không lưu trữ vĩnh viễn",
            key="consent_3"
        )
        consent_items.append(consent_3)
        
        consent_4 = st.checkbox(
            "🚫 Tôi đồng ý không chia sẻ thông tin đăng nhập (nếu có) cho người khác",
            key="consent_4"
        )
        consent_items.append(consent_4)
        
        st.markdown("**⚕️ Về trách nhiệm và hành động:**")
        consent_5 = st.checkbox(
            "🏥 Tôi cam kết tìm kiếm hỗ trợ chuyên nghiệp nếu có dấu hiệu nghiêm trọng",
            key="consent_5"
        )
        consent_items.append(consent_5)
        
        consent_6 = st.checkbox(
            "✋ Tôi hiểu rằng có thể dừng đánh giá bất cứ lúc nào mà không cần lý do",
            key="consent_6"
        )
        consent_items.append(consent_6)
    
    st.markdown("---")
    
    # Kiểm tra tất cả checkbox đã được chọn
    all_consents_given = all(consent_items)
    total_items = len(consent_items)
    checked_items = sum(consent_items)
    
    # Progress bar cho consent
    progress = checked_items / total_items
    st.progress(progress)
    st.caption(f"Đã xác nhận: {checked_items}/{total_items} điều khoản")
    
    if all_consents_given:
        st.success("🎉 **Tuyệt vời!** Bạn đã xác nhận tất cả các điều khoản!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🎯 Bắt đầu đánh giá tâm lý!", 
                use_container_width=True,
                type="primary"
            ):
                # Lưu thông tin đồng ý với timestamp
                st.session_state.consent_given = True
                st.session_state.consent_agreement_completed = True
                st.session_state.assessment_started = True
                st.session_state.consent_timestamp = datetime.now().isoformat()
                
                # Track user action
                SmartUIExperience().track_user_interaction(
                    "full_consent_given", 
                    "consent_agreement_form", 
                    {
                        "timestamp": st.session_state.consent_timestamp,
                        "all_items_confirmed": True
                    }
                )
                
                st.balloons()
                st.success("🎉 Cảm ơn bạn! Đang chuyển sang phần đánh giá...")
                time.sleep(2)
                st.rerun()
    else:
        missing_count = total_items - checked_items
        st.warning(f"⚠️ Vui lòng xác nhận thêm **{missing_count} điều khoản** để có thể tiếp tục")
        
        if checked_items > 0:
            st.info(f"✅ Bạn đã xác nhận {checked_items}/{total_items} điều khoản. Tiếp tục nhé!")
    
    # Nút quay lại
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↩️ Quay lại trang chính", use_container_width=True):
            # Reset consent state
            for i in range(1, 7):
                if f"consent_{i}" in st.session_state:
                    del st.session_state[f"consent_{i}"]
            if "show_consent_agreement" in st.session_state:
                del st.session_state["show_consent_agreement"]
            st.rerun()

def create_progress_ring(current_step: int, total_steps: int, title: str):
    """Progress indicator dạng ring với animation"""
    progress_percentage = (current_step / total_steps) * 100
    progress_degrees = (progress_percentage / 100) * 360
    
    st.markdown(f"""
    <div class="interactive-card" style="text-align: center;">
        <div style="display: flex; align-items: center; justify-content: center; gap: var(--spacing-md);">
            <div class="progress-ring" style="
                background: conic-gradient(#667eea {progress_degrees}deg, #f3f4f6 {progress_degrees}deg);
            ">
                <div style="
                    position: relative; 
                    z-index: 1; 
                    font-weight: bold; 
                    color: var(--text-primary);
                ">
                    {current_step}/{total_steps}
                </div>
            </div>
            <div style="text-align: left;">
                <h4 style="margin: 0; color: var(--text-primary);">
                    Bước {current_step}/{total_steps}: {title}
                </h4>
                <p style="margin: 0; color: var(--text-secondary);">
                    Hoàn thành {progress_percentage:.0f}% 🌟
                </p>
                <div style="
                    width: 200px; 
                    height: 6px; 
                    background: #f3f4f6; 
                    border-radius: 3px; 
                    margin-top: var(--spacing-xs);
                    overflow: hidden;
                ">
                    <div style="
                        width: {progress_percentage}%; 
                        height: 100%; 
                        background: var(--primary-gradient);
                        border-radius: 3px;
                        transition: width 0.5s ease;
                    "></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_smart_question_card(number: int, question: str, total_questions: int):
    """Question card với progress và smart hints"""
    progress = (number / total_questions) * 100
    
    st.markdown(f"""
    <div class="interactive-card pulse-glow">
        <div style="display: flex; align-items: flex-start; gap: var(--spacing-md);">
            <div style="
                background: var(--primary-gradient);
                color: white;
                padding: var(--spacing-sm) var(--spacing-md);
                border-radius: var(--radius-md);
                font-weight: bold;
                min-width: 40px;
                text-align: center;
            ">
                {number}
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 var(--spacing-sm) 0; color: var(--text-primary); line-height: 1.4;">
                    {question}
                </h4>
                <div style="
                    font-size: var(--font-xs); 
                    color: var(--text-muted);
                    margin-top: var(--spacing-xs);
                ">
                    Câu {number} / {total_questions} • Tiến độ: {progress:.0f}%
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_smart_results_dashboard(scores: dict):
    """Dashboard kết quả với visualizations nâng cao"""
    st.markdown("""
    <div class="interactive-card smooth-entrance">
        <div style="text-align: center; margin-bottom: var(--spacing-lg);">
            <h2 style="
                background: var(--primary-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                font-size: var(--font-xxl);
            ">
                🎊 Báo cáo chi tiết của bạn
            </h2>
            <p style="color: var(--text-secondary); margin: var(--spacing-sm) 0;">
                Phân tích dựa trên thang đo DASS-21 chuẩn quốc tế
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_smart_metric_card(title: str, score: int, severity: str, emoji: str, max_score: int = 42):
    """Metric card với progress bar và color coding"""
    score_percentage = (score / max_score) * 100
    
    # Color mapping based on severity
    color_map = {
        'Normal': 'var(--success-gradient)',
        'Mild': 'var(--warning-gradient)', 
        'Moderate': 'var(--error-gradient)',
        'Severe': 'var(--error-gradient)',
        'Extremely severe': 'var(--error-gradient)'
    }
    
    bg_color = color_map.get(severity, 'var(--info-gradient)')
    
    st.markdown(f"""
    <div class="interactive-card" style="
        background: {bg_color};
        color: white;
        text-align: center;
        margin: var(--spacing-sm);
        border: none;
    ">
        <div style="font-size: 3rem; margin-bottom: var(--spacing-sm);">{emoji}</div>
        <h3 style="margin: 0; color: white; font-size: var(--font-lg);">{title}</h3>
        <div style="font-size: 2rem; font-weight: bold; margin: var(--spacing-sm) 0;">
            {score} / {max_score}
        </div>
        <div style="opacity: 0.9; margin-bottom: var(--spacing-sm);">
            Mức độ: {severity}
        </div>
        <div style="
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.3);
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                width: {score_percentage}%;
                height: 100%;
                background: rgba(255,255,255,0.8);
                border-radius: 4px;
                transition: width 0.8s ease;
            "></div>
        </div>
        <div style="font-size: var(--font-xs); opacity: 0.8; margin-top: var(--spacing-xs);">
            {score_percentage:.1f}% của thang đo
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_smart_recommendations(scores: dict):
    """Recommendations thông minh dựa trên scores"""
    recommendations = []
    
    # Analyze scores and provide smart recommendations
    # Check if scores values are SubscaleScore objects or dicts
    if 'Depression' in scores:
        if hasattr(scores['Depression'], 'adjusted'):
            depression_score = scores['Depression'].adjusted
        else:
            depression_score = scores.get('Depression', {}).get('adjusted', 0)
    else:
        depression_score = 0
        
    if 'Anxiety' in scores:
        if hasattr(scores['Anxiety'], 'adjusted'):
            anxiety_score = scores['Anxiety'].adjusted
        else:
            anxiety_score = scores.get('Anxiety', {}).get('adjusted', 0)
    else:
        anxiety_score = 0
        
    if 'Stress' in scores:
        if hasattr(scores['Stress'], 'adjusted'):
            stress_score = scores['Stress'].adjusted
        else:
            stress_score = scores.get('Stress', {}).get('adjusted', 0)
    else:
        stress_score = 0
    
    if depression_score > 14:
        recommendations.extend([
            "🌅 Thử thức dậy sớm và tiếp xúc với ánh sáng mặt trời",
            "🎨 Tham gia hoạt động sáng tạo để thể hiện cảm xúc",
            "📞 Kết nối với bạn bè, gia đình thường xuyên hơn"
        ])
    
    if anxiety_score > 10:
        recommendations.extend([
            "🧘‍♀️ Luyện tập hít thở sâu và thiền định",
            "📱 Hạn chế sử dụng mạng xã hội trước khi ngủ",
            "🎵 Nghe nhạc thư giãn hoặc âm thanh thiên nhiên"
        ])
    
    if stress_score > 18:
        recommendations.extend([
            "⏰ Lập kế hoạch và ưu tiên công việc hàng ngày",
            "🚶‍♀️ Đi bộ ngoài trời ít nhất 30 phút mỗi ngày",
            "📚 Học kỹ thuật quản lý thời gian và căng thẳng"
        ])
    
    # General recommendations
    recommendations.extend([
        "💤 Duy trì lịch ngủ đều đặn 7-8 tiếng/đêm",
        "🥗 Ăn uống cân bằng và đủ chất dinh dưỡng",
        "💧 Uống đủ nước (2-3 lít/ngày)"
    ])
    
    st.markdown("""
    <div class="interactive-card">
        <h3 style="margin: 0 0 var(--spacing-md) 0; color: var(--text-primary);">
            💡 Gợi ý cá nhân hóa cho bạn
        </h3>
        <p style="color: var(--text-secondary); margin-bottom: var(--spacing-md);">
            Dựa trên kết quả đánh giá và nghiên cứu khoa học
        </p>
    """, unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations[:6]):  # Show top 6 recommendations
        st.markdown(f"""
        <div style="
            background: #f8fafc;
            border-left: 4px solid #667eea;
            padding: var(--spacing-md);
            margin: var(--spacing-sm) 0;
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            transition: all 0.3s ease;
        " 
        onmouseover="this.style.background='#f1f5f9'; this.style.transform='translateX(5px)'"
        onmouseout="this.style.background='#f8fafc'; this.style.transform='translateX(0)'">
            <p style="margin: 0; color: var(--text-primary); font-weight: 500;">
                {rec}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_smart_action_buttons():
    """Action buttons với smart suggestions"""
    st.markdown("### 🎯 Bước tiếp theo được đề xuất")
    
    cols = st.columns(3)
    
    with cols[0]:
        if st.button("💬 Trò chuyện với AI", use_container_width=True, type="primary"):
            SmartUIExperience().track_user_interaction("click", "ai_chat_button")
            st.switch_page("pages/5_Chatbot.py")
    
    with cols[1]:
        if st.button("📚 Tài nguyên hỗ trợ", use_container_width=True):
            SmartUIExperience().track_user_interaction("click", "resources_button")
            st.switch_page("pages/3_Resources.py")
    
    with cols[2]:
        if st.button("🔄 Đánh giá lại", use_container_width=True):
            SmartUIExperience().track_user_interaction("click", "retake_button")
            # Clear relevant session state
            for key in ["answers", "scores", "consent_given", "assessment_started"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def create_user_journey_summary():
    """Hiển thị tóm tắt hành trình người dùng"""
    if 'user_interactions' in st.session_state and st.session_state.user_interactions:
        with st.expander("📊 Tóm tắt hành trình của bạn", expanded=False):
            interactions = st.session_state.user_interactions
            st.write(f"🕒 Bắt đầu: {interactions[0]['timestamp'][:19]}")
            st.write(f"⚡ Tổng tương tác: {len(interactions)}")
            st.write(f"🎯 Hoàn thành: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Show interaction timeline
            st.markdown("**Timeline tương tác:**")
            for interaction in interactions[-5:]:  # Show last 5 interactions
                st.caption(f"• {interaction['action']} tại {interaction['component']}")

def show_smart_notifications():
    """Hiển thị notifications thông minh"""
    if 'current_mood' in st.session_state:
        mood = st.session_state.current_mood
        if mood['value'] <= 2:  # Sad moods
            st.markdown("""
            <div class="smart-notification">
                🤗 Tôi hiểu bạn đang trải qua khoảng thời gian khó khăn. 
                Hãy nhớ rằng cảm xúc này sẽ qua đi và bạn không đơn độc!
            </div>
            """, unsafe_allow_html=True)
        elif mood['value'] >= 4:  # Happy moods
            st.markdown("""
            <div class="smart-notification" style="background: var(--success-gradient);">
                🌟 Thật tuyệt khi bạn đang có tâm trạng tích cực! 
                Hãy chia sẻ năng lượng này với những người xung quanh bạn nhé!
            </div>
            """, unsafe_allow_html=True)
