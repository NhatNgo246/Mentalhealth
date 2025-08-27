import streamlit as st
from components.ui import app_header, show_disclaimer, load_css, create_info_card

st.set_page_config(page_title="Tài nguyên hỗ trợ", page_icon="📚", layout="centered")

# Load custom CSS
load_css()

app_header()
show_disclaimer()

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h2 style="color: var(--primary-color); margin: 0;">📚 Tài nguyên hỗ trợ sức khỏe tâm thần</h2>
    <p style="color: var(--text-secondary); margin: 0.5rem 0;">
        Công cụ và thông tin hữu ích để chăm sóc bản thân
    </p>
</div>
""", unsafe_allow_html=True)

# Emergency contacts
st.markdown("### 🚨 Liên hệ khẩn cấp")
col1, col2 = st.columns(2)

with col1:
    create_info_card(
        "Đường dây nóng cấp cứu",
        "📞 **115** - Cấp cứu y tế\n"
        "📞 **113** - Công an\n"
        "📞 **114** - Cứu hỏa\n"
        "🌐 Hoạt động 24/7",
        "🚨"
    )

with col2:
    create_info_card(
        "Hỗ trợ tâm lý chuyên môn",
        "📞 **1800 6969** - Đường dây nóng tâm lý\n"
        "📞 **028 3821 2277** - BV Tâm thần TP.HCM\n"
        "📞 **024 3577 6810** - BV Tâm thần Hà Nội\n"
        "🕐 Hoạt động 8:00-20:00",
        "🏥"
    )

# Self-care techniques
st.markdown("### 🧘 Kỹ thuật tự chăm sóc")

col1, col2 = st.columns(2)

with col1:
    create_info_card(
        "Kỹ thuật thở 4-7-8",
        "1. **Hít vào** qua mũi trong 4 giây\n"
        "2. **Giữ** hơi thở trong 7 giây\n"
        "3. **Thở ra** qua miệng trong 8 giây\n"
        "4. **Lặp lại** 4-8 lần\n"
        "🕐 Thực hiện 2 lần/ngày (sáng và tối)",
        "🌬️"
    )
    
    create_info_card(
        "Mindfulness cơ bản",
        "• **5 phút thiền** mỗi sáng\n"
        "• **Quan sát** hơi thở và cảm giác cơ thể\n"
        "• **Chấp nhận** cảm xúc mà không phán xét\n"
        "• **Sống trong hiện tại** thay vì lo lắng tương lai\n"
        "📱 App: Headspace, Calm, Insight Timer",
        "🧘"
    )

with col2:
    create_info_card(
        "Nhật ký cảm xúc",
        "📝 **Ghi chép hàng ngày:**\n"
        "• Tâm trạng (1-10)\n"
        "• Sự kiện quan trọng\n"
        "• Cảm xúc chính\n"
        "• Điều biết ơn\n"
        "🎯 Giúp nhận diện pattern và trigger",
        "📔"
    )
    
    create_info_card(
        "Vận động thể chất",
        "• **Đi bộ** 30 phút/ngày\n"
        "• **Yoga** hoặc stretching\n"
        "• **Bơi lội** hoặc chạy bộ nhẹ\n"
        "• **Tập gym** 3 lần/tuần\n"
        "💡 Vận động giải phóng endorphin tự nhiên",
        "🏃"
    )

# Professional help
st.markdown("### 🩺 Khi nào cần tìm chuyên gia?")

create_info_card(
    "Dấu hiệu cần hỗ trợ chuyên môn",
    "🔴 **Cấp cứu ngay:**\n"
    "• Có ý định tự hại hoặc tự tử\n"
    "• Ảo giác, hoang tưởng\n"
    "• Không thể chăm sóc bản thân\n\n"
    "🟡 **Nên tư vấn:**\n"
    "• Triệu chứng kéo dài > 2 tuần\n"
    "• Ảnh hưởng đến công việc/học tập\n"
    "• Mất ngủ, mất ăn kéo dài\n"
    "• Cảm giác tuyệt vọng, vô giá trị",
    "⚕️"
)

# Online resources
st.markdown("### 🌐 Tài nguyên trực tuyến")

col1, col2, col3 = st.columns(3)

with col1:
    create_info_card(
        "Website hữu ích",
        "🌐 [WHO Mental Health](https://www.who.int/health-topics/mental-disorders)\n"
        "🌐 [Mind.org.uk](https://www.mind.org.uk/)\n"
        "🌐 [BetterHelp](https://www.betterhelp.com/)\n"
        "🌐 [Psychology Today](https://www.psychologytoday.com/)",
        "💻"
    )

with col2:
    create_info_card(
        "Apps di động",
        "📱 **Headspace** - Thiền và mindfulness\n"
        "📱 **Calm** - Thư giãn và ngủ ngon\n"
        "📱 **Daylio** - Theo dõi tâm trạng\n"
        "📱 **Sanvello** - Quản lý lo âu",
        "📱"
    )

with col3:
    create_info_card(
        "Sách tham khảo",
        "📚 \"Feeling Good\" - David Burns\n"
        "📚 \"The Anxiety Workbook\" - Edmund Bourne\n"
        "📚 \"Mindfulness for Beginners\" - Jon Kabat-Zinn\n"
        "📚 \"The Happiness Trap\" - Russ Harris",
        "📖"
    )

# Telemedicine info
st.markdown("### 💻 Tele-mental health")

create_info_card(
    "Tư vấn tâm lý trực tuyến",
    "🎥 **Video call với chuyên gia:**\n"
    "• Tiện lợi, riêng tư và an toàn\n"
    "• Tiết kiệm thời gian di chuyển\n"
    "• Phù hợp trong thời đại số\n\n"
    "🏥 **Các bệnh viện có dịch vụ:**\n"
    "• Bệnh viện Tâm thần TP.HCM\n"
    "• Bệnh viện Bạch Mai\n"
    "• Các phòng khám tư nhân\n\n"
    "💰 **Chi phí:** 200,000 - 800,000 VND/buổi",
    "💻"
)

# Back to home button
st.markdown('<div style="text-align: center; margin: 3rem 0;">', unsafe_allow_html=True)
if st.button("🏠 Về trang chủ", use_container_width=True):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)