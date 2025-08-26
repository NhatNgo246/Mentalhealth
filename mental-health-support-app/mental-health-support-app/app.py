import streamlit as st
from components.ui import app_header, show_disclaimer

st.set_page_config(page_title="Mental Health Support App", page_icon="🧠", layout="centered")

app_header()
show_disclaimer()

st.markdown(
    "Chao mung! Ung dung giup ban tu danh gia nhanh bang DASS-21 va xem goi y buoc tiep theo. "
    "Chon muc **Assessment** o thanh ben de bat dau lam bang cau hoi."
)

st.divider()
st.markdown("**Goi y trich dan trong bai bao:** Mo ta ung dung, quy trinh cham diem, va thu nghiem kha dung (SUS).")
