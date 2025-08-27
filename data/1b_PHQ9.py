import json, os, streamlit as st
st.set_page_config(page_title="PHQ-9", page_icon="📝", layout="centered")
st.title("PHQ-9 — Sàng lọc trầm cảm (tuỳ chọn)")

with open(os.path.join(os.path.dirname(__file__),"..","data","phq9_vi.json"), encoding="utf-8") as f:
    cfg = json.load(f)
opts = cfg["options"]
st.session_state.setdefault("phq9", {})

with st.form("phq9_form"):
    for it in cfg["items"]:
        st.session_state.phq9[it["id"]] = st.radio(
            f'{it["id"]}. {it["text"]}', [o["value"] for o in opts],
            format_func=lambda v: next(o["label"] for o in opts if o["value"]==v),
            horizontal=True, key=f'phq_{it["id"]}'
        )
    if st.form_submit_button("Chấm điểm PHQ-9"):
        total = sum(st.session_state.phq9.values())
        sev = next(label for lo,hi,label in cfg["severity_thresholds"] if lo<=total<=hi)
        st.session_state.phq9_result = {"total": total, "severity": sev}
        st.success(f"Tổng {total} — Mức {sev}")
        if total >= 10:
            st.error("Khuyến nghị: Trao đổi với chuyên gia. Nếu có ý nghĩ tự hại, hãy gọi 115/đến cơ sở y tế ngay.")