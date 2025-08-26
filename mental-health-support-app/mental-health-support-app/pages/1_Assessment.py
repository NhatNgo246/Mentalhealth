import streamlit as st
from components.questionnaires import load_dass21_vi
from components.scoring import score_dass21
from components.ui import app_header, show_disclaimer

st.set_page_config(page_title="Assessment — DASS-21", page_icon="📝", layout="centered")
app_header()
show_disclaimer()

cfg = load_dass21_vi()
options = cfg["options"]

if "answers" not in st.session_state:
    st.session_state.answers = {}

st.subheader("Bang tu danh gia DASS-21")
with st.form("dass21_form"):
    for item in cfg["items"]:
        st.session_state.answers[item["id"]] = st.radio(
            f"{item['id']}. {item['text']}",
            options=[o["value"] for o in options],
            format_func=lambda v: next(o["label"] for o in options if o["value"]==v),
            horizontal=True,
            key=f"q_{item['id']}"
        )
    submitted = st.form_submit_button("Cham diem")
    if submitted:
        scores = score_dass21(st.session_state.answers, cfg)
        st.session_state.scores = {k: v.__dict__ for k, v in scores.items()}
        st.success("Da cham diem! Vao trang **Results** de xem chi tiet.")
