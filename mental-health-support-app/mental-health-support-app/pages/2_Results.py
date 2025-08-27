import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.ui import app_header, show_disclaimer, load_css, create_result_card, create_metric_card, create_progress_indicator

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

# Load custom CSS
load_css()

app_header()
show_disclaimer()

# Progress indicator
create_progress_indicator(2, 3)

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h2 style="color: var(--primary-color); margin: 0;">📊 Kết quả đánh giá DASS-21</h2>
    <p style="color: var(--text-secondary); margin: 0.5rem 0;">
        Phân tích chi tiết mức độ trầm cảm, lo âu và stress của bạn
    </p>
</div>
""", unsafe_allow_html=True)

scores = st.session_state.get("scores")
if not scores:
    st.markdown("""
    <div class="warning-card fade-in">
        <div style="display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2rem; margin-right: 1rem;">⚠️</span>
            <div>
                <h3 style="margin: 0;">Chưa có kết quả đánh giá</h3>
                <p style="margin: 0.5rem 0 0 0;">Hãy thực hiện bài đánh giá ở trang <strong>Assessment</strong> trước.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(scores).T

# Check if DataFrame has the expected structure
if df.empty or 'adjusted' not in df.columns:
    st.error("❌ Dữ liệu kết quả không hợp lệ. Vui lòng thực hiện đánh giá lại.")
    st.stop()

# Create metrics row
col1, col2, col3 = st.columns(3)

with col1:
    depression_score = df.loc['Depression', 'adjusted']
    depression_severity = df.loc['Depression', 'severity']
    create_metric_card("Trầm cảm", f"{depression_score} điểm", f"Mức độ: {depression_severity}", "😔")

with col2:
    anxiety_score = df.loc['Anxiety', 'adjusted']
    anxiety_severity = df.loc['Anxiety', 'severity']
    create_metric_card("Lo âu", f"{anxiety_score} điểm", f"Mức độ: {anxiety_severity}", "😰")

with col3:
    stress_score = df.loc['Stress', 'adjusted']
    stress_severity = df.loc['Stress', 'severity']
    create_metric_card("Stress", f"{stress_score} điểm", f"Mức độ: {stress_severity}", "😓")

# Visualization
st.markdown("### 📈 Biểu đồ phân tích")

# Create bar chart
fig = px.bar(
    x=['Trầm cảm', 'Lo âu', 'Stress'],
    y=[depression_score, anxiety_score, stress_score],
    title="Điểm số các chỉ số DASS-21",
    color=[depression_score, anxiety_score, stress_score],
    color_continuous_scale="RdYlBu_r"
)
fig.update_layout(
    showlegend=False,
    height=400,
    title_font_size=16,
    title_x=0.5
)
st.plotly_chart(fig, use_container_width=True)

# Detailed results for each dimension
st.markdown("### 📋 Phân tích chi tiết")

# Severity mapping for Vietnamese
severity_map = {
    "Normal": "Bình thường",
    "Mild": "Nhẹ", 
    "Moderate": "Trung bình",
    "Severe": "Nặng",
    "Extremely Severe": "Rất nặng"
}

# Get recommendations based on severity
def get_recommendations(severity):
    sev_order = {"Normal":0,"Mild":1,"Moderate":2,"Severe":3,"Extremely Severe":4}
    if sev_order.get(severity, 0) >= 3:
        return """
        <li>🏥 Nên tìm kiếm sự hỗ trợ từ chuyên gia tâm lý/bác sĩ ngay</li>
        <li>📞 Liên hệ đường dây nóng tâm lý: 1800 6969</li>
        <li>🧘 Thực hành kỹ thuật thở sâu và mindfulness hàng ngày</li>
        <li>💤 Ưu tiên nghỉ ngơi và ngủ đủ giấc</li>
        <li>🚶 Tập thể dục nhẹ nhàng, đi bộ ngoài trời</li>
        """
    elif sev_order.get(severity, 0) >= 2:
        return """
        <li>💬 Nên trao đổi với nhà chuyên môn để được tư vấn</li>
        <li>🧘 Thực hành thở sâu, meditation và mindfulness</li>
        <li>💤 Duy trì giấc ngủ đủ 7-8 tiếng mỗi đêm</li>
        <li>🏃 Tập thể dục nhẹ, yoga hoặc đi bộ</li>
        <li>📚 Đọc sách self-help về quản lý cảm xúc</li>
        """
    else:
        return """
        <li>✅ Tiếp tục duy trì lối sống lành mạnh hiện tại</li>
        <li>🧘 Thực hành mindfulness để duy trì sự cân bằng</li>
        <li>📅 Lập lịch sinh hoạt khoa học và hợp lý</li>
        <li>🤝 Duy trì mối quan hệ xã hội tích cực</li>
        <li>📊 Theo dõi định kỳ tình trạng tinh thần</li>
        """

# Display detailed results
for dimension in ['Depression', 'Anxiety', 'Stress']:
    score = df.loc[dimension, 'adjusted']
    severity = df.loc[dimension, 'severity']
    severity_vi = severity_map.get(severity, severity)
    
    if dimension == 'Depression':
        title = "Trầm cảm (Depression)"
        description = "Đánh giá mức độ buồn chán, mất hứng thú, cảm giác vô vọng và thiếu động lực."
    elif dimension == 'Anxiety':
        title = "Lo âu (Anxiety)"
        description = "Đánh giá mức độ lo lắng, căng thẳng, sợ hãi và bồn chồn."
    else:
        title = "Stress"
        description = "Đánh giá mức độ căng thẳng, khó thư giãn và dễ bị kích động."
    
    recommendations = get_recommendations(severity)
    
    create_result_card(severity_vi, score, description, recommendations)

# Data download section
st.markdown("### 💾 Tải xuống kết quả")

col1, col2 = st.columns(2)
with col1:
    csv_data = df.to_csv(index=True).encode("utf-8")
    st.download_button(
        "📄 Tải file CSV",
        csv_data,
        "dass21_results.csv",
        "text/csv",
        use_container_width=True
    )

with col2:
    # Create a detailed report
    report = f"""
# Báo cáo kết quả DASS-21
    
## Tổng quan
- **Trầm cảm**: {depression_score} điểm - {severity_map.get(depression_severity, depression_severity)}
- **Lo âu**: {anxiety_score} điểm - {severity_map.get(anxiety_severity, anxiety_severity)}  
- **Stress**: {stress_score} điểm - {severity_map.get(stress_severity, stress_severity)}

## Gợi ý hỗ trợ
Dựa trên kết quả đánh giá, bạn nên:
1. Theo dõi tình trạng tinh thần định kỳ
2. Thực hành các kỹ thuật thư giãn
3. Duy trì lối sống lành mạnh
4. Tìm kiếm hỗ trợ chuyên môn nếu cần

*Lưu ý: Kết quả này chỉ mang tính tham khảo, không thay thế chẩn đoán y khoa.*
"""
    
    st.download_button(
        "📋 Tải báo cáo chi tiết",
        report.encode("utf-8"),
        "dass21_detailed_report.md",
        "text/markdown",
        use_container_width=True
    )

# Next steps
st.markdown("""
<div class="info-card fade-in" style="margin-top: 2rem;">
    <div style="display: flex; align-items: flex-start;">
        <span style="font-size: 1.5rem; margin-right: 1rem; margin-top: 0.2rem;">🎯</span>
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--primary-color);">Bước tiếp theo</h4>
            <p style="margin: 0; color: var(--text-primary);">
                • Truy cập trang <strong>Resources</strong> để tìm hiểu thêm tài nguyên hỗ trợ<br>
                • Sử dụng <strong>Chatbot</strong> để được tư vấn ban đầu<br>
                • Lưu lại kết quả và theo dõi định kỳ<br>
                • Tìm kiếm sự hỗ trợ chuyên môn nếu cần thiết
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
