"""
Optional Research Consent Component
Tích hợp nhẹ nhàng vào consent page hiện có
"""

import streamlit as st
from typing import Optional

def render_research_consent_section() -> Optional[bool]:
    """
    Render phần đồng ý nghiên cứu - hoàn toàn optional
    Returns: True nếu đồng ý, False nếu từ chối, None nếu chưa chọn
    """
    
    # Chỉ hiển thị nếu research system được bật
    import os
    if not os.environ.get("ENABLE_RESEARCH_COLLECTION", "false").lower() in ["true", "1", "yes"]:
        return None
    
    st.markdown("---")
    st.markdown("### 🔬 Chia sẻ Dữ liệu cho Nghiên cứu (Tùy chọn)")
    
    with st.expander("ℹ️ Thông tin về việc chia sẻ dữ liệu nghiên cứu"):
        st.markdown("""
        **Mục đích nghiên cứu:**
        - Cải thiện hiệu quả của các công cụ đánh giá sức khỏe tâm thần
        - Phát triển các phương pháp sàng lọc tốt hơn
        - Nghiên cứu xu hướng sức khỏe tâm thần trong cộng đồng
        
        **Dữ liệu được thu thập:**
        - Câu trả lời của bạn (đã ẩn danh hoàn toàn)
        - Thời gian hoàn thành đánh giá
        - Thông tin nhân khẩu học cơ bản (tuổi, giới tính - nếu bạn cung cấp)
        
        **Cam kết bảo mật:**
        ✅ Dữ liệu được ẩn danh hoàn toàn  
        ✅ Không thu thập thông tin cá nhân định danh  
        ✅ Dữ liệu được mã hóa và bảo mật  
        ✅ Chỉ sử dụng cho mục đích nghiên cứu khoa học  
        ✅ Bạn có thể rút lại sự đồng ý bất kỳ lúc nào  
        
        **Quyền lợi của bạn:**
        - Việc tham gia hoàn toàn tự nguyện
        - Không ảnh hưởng đến dịch vụ bạn nhận được
        - Có thể thay đổi quyết định bất kỳ lúc nào
        """)
    
    # Radio button cho lựa chọn
    research_choice = st.radio(
        "Bạn có đồng ý chia sẻ dữ liệu ẩn danh cho nghiên cứu khoa học không?",
        options=[
            "Có, tôi đồng ý chia sẻ dữ liệu ẩn danh cho nghiên cứu",
            "Không, tôi không muốn chia sẻ dữ liệu",
            "Tôi cần thêm thời gian để quyết định"
        ],
        index=2,  # Default: chưa quyết định
        key="research_consent_choice"
    )
    
    # Xử lý lựa chọn
    if research_choice == "Có, tôi đồng ý chia sẻ dữ liệu ẩn danh cho nghiên cứu":
        st.success("✅ Cảm ơn bạn đã đồng ý tham gia nghiên cứu! Dữ liệu của bạn sẽ giúp cải thiện chăm sóc sức khỏe tâm thần.")
        return True
    elif research_choice == "Không, tôi không muốn chia sẻ dữ liệu":
        st.info("✅ Lựa chọn của bạn đã được ghi nhận. Bạn vẫn có thể sử dụng đầy đủ các dịch vụ đánh giá.")
        return False
    else:
        st.info("💭 Bạn có thể quyết định sau. Việc đánh giá sức khỏe tâm thần của bạn sẽ không bị ảnh hưởng.")
        return None

def get_research_consent_status() -> Optional[bool]:
    """Lấy trạng thái đồng ý nghiên cứu từ session state"""
    return st.session_state.get("research_consent", None)

def set_research_consent_status(status: Optional[bool]):
    """Lưu trạng thái đồng ý nghiên cứu vào session state"""
    st.session_state["research_consent"] = status

def is_research_enabled() -> bool:
    """Kiểm tra xem research collection có được bật không"""
    import os
    return os.environ.get("ENABLE_RESEARCH_COLLECTION", "false").lower() in ["true", "1", "yes"]
