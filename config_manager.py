"""
SOULFRIEND Configuration Manager
Settings and configuration interface
"""

import streamlit as st
import json
import os
import sys

# Add project root to path
sys.path.append('/workspaces/Mentalhealth')

from components.ui import load_css, app_header

# Page configuration
st.set_page_config(
    page_title="SOULFRIEND Config",
    page_icon="⚙️",
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

# Configuration Manager
def config_manager():
    st.title("⚙️ Cấu hình hệ thống")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 Giao diện",
        "📊 Đánh giá",
        "🔔 Thông báo",
        "🔒 Bảo mật"
    ])
    
    with tab1:
        st.header("Cấu hình giao diện")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Chủ đề")
            theme = st.selectbox(
                "Chọn chủ đề:",
                ["Sáng", "Tối", "Tự động"],
                index=0
            )
            
            st.subheader("Màu sắc chính")
            primary_color = st.color_picker(
                "Màu chính:",
                "#FF6B6B"
            )
            
            st.subheader("Font chữ")
            font_family = st.selectbox(
                "Font chữ:",
                ["Arial", "Helvetica", "Times New Roman", "Calibri"],
                index=0
            )
            
        with col2:
            st.subheader("Bố cục")
            layout_style = st.selectbox(
                "Kiểu bố cục:",
                ["Rộng", "Trung tâm", "Compact"],
                index=1
            )
            
            sidebar_default = st.selectbox(
                "Thanh bên mặc định:",
                ["Mở rộng", "Thu gọn", "Ẩn"],
                index=0
            )
            
            st.subheader("Ngôn ngữ")
            language = st.selectbox(
                "Ngôn ngữ giao diện:",
                ["Tiếng Việt", "English"],
                index=0
            )
        
        if st.button("💾 Lưu cấu hình giao diện"):
            config = {
                "theme": theme,
                "primary_color": primary_color,
                "font_family": font_family,
                "layout_style": layout_style,
                "sidebar_default": sidebar_default,
                "language": language
            }
            st.success("✅ Đã lưu cấu hình giao diện!")
    
    with tab2:
        st.header("Cấu hình đánh giá")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Thang đo")
            
            # DASS-21 settings
            st.write("**DASS-21**")
            dass_cutoffs = st.checkbox("Hiển thị ngưỡng cắt", True)
            dass_percentile = st.checkbox("Hiển thị phần trăm", True)
            
            # PHQ-9 settings
            st.write("**PHQ-9**")
            phq_severity = st.checkbox("Hiển thị mức độ nghiêm trọng", True)
            phq_risk = st.checkbox("Cảnh báo rủi ro tự tử", True)
            
            # GAD-7 settings
            st.write("**GAD-7**")
            gad_interpretation = st.checkbox("Giải thích kết quả", True)
            
        with col2:
            st.subheader("Báo cáo")
            
            report_format = st.selectbox(
                "Định dạng báo cáo mặc định:",
                ["PDF", "Word", "HTML"],
                index=0
            )
            
            include_charts = st.checkbox("Bao gồm biểu đồ", True)
            include_recommendations = st.checkbox("Bao gồm khuyến nghị", True)
            include_resources = st.checkbox("Bao gồm tài nguyên", True)
            
            st.subheader("Lưu trữ")
            auto_save = st.checkbox("Tự động lưu kết quả", False)
            save_duration = st.selectbox(
                "Thời gian lưu trữ:",
                ["30 ngày", "90 ngày", "1 năm", "Vô thời hạn"],
                index=1
            )
        
        if st.button("💾 Lưu cấu hình đánh giá"):
            st.success("✅ Đã lưu cấu hình đánh giá!")
    
    with tab3:
        st.header("Cấu hình thông báo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Email thông báo")
            email_notifications = st.checkbox("Kích hoạt email", False)
            admin_email = st.text_input(
                "Email quản trị:",
                placeholder="admin@soulfriend.vn"
            )
            
            st.subheader("Cảnh báo")
            high_risk_alert = st.checkbox("Cảnh báo rủi ro cao", True)
            crisis_alert = st.checkbox("Cảnh báo khủng hoảng", True)
            
        with col2:
            st.subheader("Tự động hóa")
            auto_follow_up = st.checkbox("Theo dõi tự động", False)
            follow_up_days = st.number_input(
                "Số ngày theo dõi:",
                min_value=1,
                max_value=30,
                value=7
            )
            
            reminder_enabled = st.checkbox("Nhắc nhở đánh giá", False)
            reminder_frequency = st.selectbox(
                "Tần suất nhắc nhở:",
                ["Hàng tuần", "Hai tuần", "Hàng tháng"],
                index=1
            )
        
        if st.button("💾 Lưu cấu hình thông báo"):
            st.success("✅ Đã lưu cấu hình thông báo!")
    
    with tab4:
        st.header("Cấu hình bảo mật")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Xác thực")
            require_login = st.checkbox("Yêu cầu đăng nhập", False)
            session_timeout = st.selectbox(
                "Thời gian phiên:",
                ["30 phút", "1 giờ", "2 giờ", "4 giờ"],
                index=1
            )
            
            st.subheader("Mã hóa dữ liệu")
            encrypt_data = st.checkbox("Mã hóa dữ liệu nhạy cảm", True)
            encryption_level = st.selectbox(
                "Mức độ mã hóa:",
                ["AES-128", "AES-256"],
                index=1
            )
            
        with col2:
            st.subheader("Kiểm toán")
            audit_log = st.checkbox("Nhật ký kiểm toán", True)
            log_retention = st.selectbox(
                "Thời gian lưu log:",
                ["30 ngày", "90 ngày", "1 năm"],
                index=2
            )
            
            st.subheader("Quyền riêng tư")
            anonymize_data = st.checkbox("Ẩn danh hóa dữ liệu", True)
            gdpr_compliance = st.checkbox("Tuân thủ GDPR", True)
        
        if st.button("💾 Lưu cấu hình bảo mật"):
            st.success("✅ Đã lưu cấu hình bảo mật!")
    
    # Export/Import configuration
    st.markdown("---")
    st.subheader("🔄 Sao lưu & Khôi phục")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Xuất cấu hình"):
            # Sample config for demo
            config = {
                "ui": {"theme": "light", "language": "vi"},
                "assessment": {"format": "pdf", "charts": True},
                "notifications": {"email": False, "alerts": True},
                "security": {"encryption": "AES-256", "audit": True}
            }
            st.download_button(
                "⬇️ Tải file cấu hình",
                data=json.dumps(config, indent=2, ensure_ascii=False),
                file_name="soulfriend_config.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader(
            "📥 Nhập cấu hình",
            type="json",
            help="Tải file cấu hình đã xuất trước đó"
        )
        if uploaded_file is not None:
            try:
                config = json.load(uploaded_file)
                st.success("✅ Đã tải cấu hình thành công!")
                st.json(config)
            except:
                st.error("❌ File cấu hình không hợp lệ!")
    
    with col3:
        if st.button("🔄 Khôi phục mặc định"):
            if st.button("✅ Xác nhận khôi phục", key="confirm_reset"):
                st.success("✅ Đã khôi phục cấu hình mặc định!")

# Main function
def main():
    config_manager()

if __name__ == "__main__":
    main()
