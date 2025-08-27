# Đây là file placeholder - chức năng đã được tích hợp vào trang chủ
import streamlit as st

st.markdown("## 🔄 Chuyển hướng")
st.info("Chức năng này đã được tích hợp vào trang chủ. Vui lòng quay lại trang chủ.")

if st.button("🏠 Về trang chủ"):
    st.switch_page("app.py")
