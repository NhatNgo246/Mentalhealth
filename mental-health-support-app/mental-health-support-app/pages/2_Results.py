import streamlit as st
import pandas as pd
from components.ui import app_header, show_disclaimer

st.set_page_config(page_title="Results", page_icon="📊", layout="centered")
app_header()
show_disclaimer()

st.subheader("Ket qua DASS-21")

scores = st.session_state.get("scores")
if not scores:
    st.warning("Chua co ket qua. Hay thuc hien Assessment truoc.")
    st.stop()

df = pd.DataFrame(scores).T
st.dataframe(df)

tips = []
sev_order = {"Normal":0,"Mild":1,"Moderate":2,"Severe":3,"Extremely Severe":4}
for sub, row in df.iterrows():
    sev = row["severity"]
    if sev_order.get(sev,0) >= 2:
        tips.append(f"- **{sub}** muc **{sev}** -> Nen trao doi voi nha chuyen mon; tap tho cham, ngu du, van dong nhe.")
    else:
        tips.append(f"- **{sub}** muc **{sev}** -> Tiep tuc theo doi, thuc hanh tu tro (tho, mindfulness, lich sinh hoat).")
st.markdown("\\n".join(tips))

st.download_button("Tai CSV", df.to_csv(index=True).encode("utf-8"), "dass21_results.csv", "text/csv")
