import streamlit as st

def display_logo(width=80, centered=False):
    """Display logo with consistent styling across pages"""
    if centered:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("assets/logo.png", width=width, caption="Mental Health Support App Logo")
            except:
                st.markdown(f'<div style="font-size: {width//20}rem; text-align: center;" aria-label="Mental Health App Logo">🧠</div>', unsafe_allow_html=True)
    else:
        try:
            st.image("assets/logo.png", width=width, caption="App Logo")
        except:
            st.markdown(f'<div style="font-size: {width//20}rem;" aria-label="Mental Health App Logo">🧠</div>', unsafe_allow_html=True)

DISCLAIMER = (
    "**Lưu ý:** Ứng dụng mang tính hỗ trợ ban đầu, không thay thế chẩn đoán "
    "hay điều trị từ bác sĩ/nhà trị liệu. Nếu bạn có ý nghĩ tự hại hoặc nguy cơ "
    "khẩn cấp, hãy liên hệ 115 hoặc cơ sở y tế gần nhất."
)

def load_css():
    """Load custom CSS styles"""
    with open('/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/assets/styles.css', 'r', encoding='utf-8') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def app_header():
    """Display enhanced app header with logo and modern styling"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        display_logo(width=80, centered=False)
            
    st.markdown("""
    <div class="app-header fade-in">
        <h1>Mental Health Support App</h1>
        <div class="caption">
            🔬 Sàng lọc tự đánh giá DASS-21 • 💬 Tele-mental health • 🤝 Liên ngành
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_disclaimer():
    """Display enhanced disclaimer with styling"""
    st.markdown(f"""
    <div class="warning-card slide-in">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">⚠️</span>
            <div>{DISCLAIMER}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, description="", icon="📊"):
    """Create a styled metric card"""
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="margin: 0; color: var(--primary-color);">{title}</h3>
        <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0; color: var(--text-primary);">{value}</div>
        <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def create_info_card(title, content, icon="ℹ️"):
    """Create a styled info card"""
    st.markdown(f"""
    <div class="info-card slide-in">
        <div style="display: flex; align-items: flex-start;">
            <span style="font-size: 1.5rem; margin-right: 1rem; margin-top: 0.2rem;">{icon}</span>
            <div>
                <h4 style="margin: 0 0 0.5rem 0; color: var(--primary-color);">{title}</h4>
                <p style="margin: 0; color: var(--text-primary);">{content}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_result_card(level, score, description, recommendations):
    """Create a styled result card with appropriate coloring"""
    if level.lower() == "cao" or level.lower() == "high":
        card_class = "result-high"
        icon = "🚨"
    elif level.lower() == "trung bình" or level.lower() == "moderate":
        card_class = "result-moderate" 
        icon = "⚠️"
    else:
        card_class = "result-normal"
        icon = "✅"
    
    st.markdown(f"""
    <div class="info-card {card_class} fade-in">
        <div style="display: flex; align-items: flex-start;">
            <span style="font-size: 2rem; margin-right: 1rem;">{icon}</span>
            <div>
                <h3 style="margin: 0 0 0.5rem 0;">Mức độ: {level}</h3>
                <p style="font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;">Điểm số: {score}</p>
                <p style="margin: 0.5rem 0;">{description}</p>
                <div style="margin-top: 1rem;">
                    <h4 style="margin: 0 0 0.5rem 0;">🎯 Gợi ý hỗ trợ:</h4>
                    <ul style="margin: 0; padding-left: 1.5rem;">
                        {recommendations}
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_progress_indicator(current_step, total_steps):
    """Create a styled progress indicator"""
    progress = current_step / total_steps
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">Tiến trình đánh giá</span>
            <span style="color: var(--text-secondary);">{current_step}/{total_steps}</span>
        </div>
        <div style="background: var(--border-color); border-radius: 10px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); 
                        width: {progress*100}%; height: 100%; border-radius: 10px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
