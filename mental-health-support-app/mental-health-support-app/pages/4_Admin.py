import streamlit as st
import os, json, datetime as dt
from components.ui import app_header

st.set_page_config(page_title="Admin", page_icon="⚙️", layout="centered")
app_header()

st.subheader("Xuat cau hinh DASS-21")
path = os.path.join(os.path.dirname(__file__), "..", "data", "dass21_vi.json")
with open(path, "r", encoding="utf-8") as f:
    txt = f.read()
st.code(txt, language="json")

st.download_button("Tai DASS-21 JSON", txt.encode("utf-8"), file_name=f"dass21_vi_{dt.date.today()}.json")
