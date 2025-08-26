import os, streamlit as st
st.set_page_config(page_title="Chatbot hỗ trợ", page_icon="💬", layout="centered")
st.title("Chatbot hỗ trợ (tuỳ chọn)")

st.markdown("Đặt biến môi trường **OPENAI_API_KEY** để dùng API; nếu không, app trả gợi ý mặc định.")
msg = st.text_area("Bạn muốn chia sẻ/ hỏi gì?", height=120)
if st.button("Gửi") and msg.strip():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.warning("Chưa có OPENAI_API_KEY → gợi ý cơ bản:")
        st.write("- Thu nhỏ mục tiêu hôm nay.\n- Thở 4-4-6 trong 5 phút.\n- Liên hệ người thân tin cậy.")
    else:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            rsp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Bạn là trợ lý hỗ trợ tinh tế, không thay thế chuyên gia y tế."},
                    {"role":"user","content": msg}
                ],
                temperature=0.6, max_tokens=300
            )
            st.write(rsp.choices[0].message.content)
        except Exception as e:
            st.error(f"Lỗi API: {e}")