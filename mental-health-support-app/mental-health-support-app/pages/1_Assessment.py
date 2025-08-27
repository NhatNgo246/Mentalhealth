import streamlit as st
from components.questionnaires import load_dass21_vi
from components.scoring import score_dass21
from components.ui import app_header, show_disclaimer, load_css, create_progress_indicator, create_info_card

st.set_page_config(page_title="Assessment — DASS-21", page_icon="📝", layout="centered")

# Load custom CSS
load_css()

app_header()
show_disclaimer()

cfg = load_dass21_vi()
options = cfg["options"]

if "answers" not in st.session_state:
    st.session_state.answers = {}

# Enhanced header for assessment
st.markdown("""
<div class="assessment-form fade-in">
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: var(--primary-color); margin: 0;">📝 Bảng tự đánh giá DASS-21</h2>
        <p style="color: var(--text-secondary); margin: 0.5rem 0;">
            Vui lòng đọc kỹ từng câu hỏi và chọn mức độ phù hợp nhất với tình trạng của bạn trong <strong>tuần vừa qua</strong>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Progress indicator
create_progress_indicator(1, 3)

# Info card with instructions
create_info_card(
    "Hướng dẫn làm bài",
    "• Đọc cẩn thận từng câu hỏi\n"
    "• Chọn mức độ mô tả đúng nhất tình trạng của bạn trong 7 ngày qua\n"
    "• Không có câu trả lời đúng hay sai, hãy trung thực\n"
    "• Hoàn thành tất cả 21 câu hỏi để có kết quả chính xác",
    "📋"
)

# Enhanced form with better styling
with st.form("dass21_form"):
    st.markdown('<div class="assessment-form">', unsafe_allow_html=True)
    
    for i, item in enumerate(cfg["items"], 1):
        # Question card with enhanced styling
        st.markdown(f"""
        <div class="question-card slide-in" style="animation-delay: {i*0.1}s;">
            <h4 style="margin: 0 0 1rem 0; color: var(--primary-color);">
                Câu {item['id']}/21: {item['text']}
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.answers[item["id"]] = st.radio(
            f"Lựa chọn câu {item['id']}",  # Provide label for accessibility
            options=[o["value"] for o in options],
            format_func=lambda v: next(o["label"] for o in options if o["value"]==v),
            horizontal=True,
            key=f"q_{item['id']}",
            label_visibility="hidden"  # Hide the label since we show it in HTML above
        )
        
        if i < len(cfg["items"]):
            st.markdown('<hr style="margin: 1.5rem 0; border: 1px solid var(--border-color);">', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced submit button
    st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
    submitted = st.form_submit_button("🎯 Hoàn thành đánh giá và xem kết quả", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted:
        # Check if all questions are answered
        if len(st.session_state.answers) == len(cfg["items"]):
            scores = score_dass21(st.session_state.answers, cfg)
            st.session_state.scores = {k: v.__dict__ for k, v in scores.items()}
            
            st.markdown("""
            <div class="success-card fade-in">
                <div style="display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 2rem; margin-right: 1rem;">🎉</span>
                    <div>
                        <h3 style="margin: 0; color: var(--success-color);">Đánh giá hoàn thành!</h3>
                        <p style="margin: 0.5rem 0 0 0;">Vào trang <strong>Results</strong> để xem chi tiết kết quả và gợi ý hỗ trợ.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Vui lòng trả lời tất cả các câu hỏi để có kết quả chính xác.")
