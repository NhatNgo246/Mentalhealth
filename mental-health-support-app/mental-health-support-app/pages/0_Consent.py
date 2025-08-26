import streamlit as st
from components.ui import app_header, show_disclaimer

st.set_page_config(page_title="Consent", page_icon="✅", layout="centered")
app_header(); show_disclaimer()

st.subheader("Thông tin & Đồng thuận")
st.markdown("""
- Ứng dụng nhằm **sàng lọc ban đầu**, không thay thế chẩn đoán/điều trị.
- Dữ liệu demo chỉ lưu **cục bộ** trong Codespace (không gửi server).
- Chọn **Tôi đồng ý** để tiếp tục.
""")
agree = st.checkbox("Tôi đồng ý và trên 16 tuổi.")
if agree:
    st.success("Cảm ơn! Vào **Assessment** để bắt đầu.")
else:
    st.warning("Vui lòng xác nhận đồng ý để dùng các tính năng khác.")