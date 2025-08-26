import streamlit as st
from components.ui import app_header, show_disclaimer

st.set_page_config(page_title="Resources", page_icon="📚", layout="centered")
app_header()
show_disclaimer()

st.markdown('''
### Tai nguyen tu tro
- Ky thuat tho 4-4-6 (4s hit vao, 4s giu, 6s tho ra) - 5 phut x 2 lan/ngay.
- Ghi chep tam trang hang ngay (muc tieu, cam xuc, giac ngu).
- Van dong nhe 20-30 phut, 3-5 lan/tuan.

### Khi nao can tim chuyen gia
- Trieu chung keo dai >2 tuan hoac anh huong ro ret den cong viec/hoc tap.
- Xuat hien y nghi tu hai/tu tu -> Goi 115 hoac den co so y te gan nhat.

### Video call / Tele-mental health (goi y ky thuat)
- Tich hop lich hen va lien ket video (Zoom/Meet) trong phien ban tiep theo.
''')
from components.logger import append_row
import datetime as dt, os
log_path = os.path.join(os.path.dirname(__file__), "..", "results_log.csv")

if st.button("Lưu kết quả (CSV nội bộ)"):
    row = {"ts": dt.datetime.utcnow().isoformat(), **{k: str(v) for k,v in scores.items()}}
    append_row(log_path, row)
    st.success("Đã lưu vào results_log.csv")