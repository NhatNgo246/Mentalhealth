import streamlit as st

DISCLAIMER = (
    "**Luu y:** Ung dung mang tinh ho tro ban dau, khong thay the chan doan "
    "hay dieu tri tu bac si/nha tri lieu. Neu ban co y nghi tu hai hoac nguy co "
    "khanc cap, hay lien he 115 hoac co so y te gan nhat."
)

def app_header():
    st.title("Mental Health Support App — Prototype")
    st.caption("Sang loc tu danh gia DASS-21 · Tele-mental health · Lien nganh")

def show_disclaimer():
    st.info(DISCLAIMER)
