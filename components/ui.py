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
    """Load custom CSS styles with error handling"""
    try:
        # Try different possible paths
        css_paths = [
            '/workspaces/Mentalhealth/assets/styles.css',
            'assets/styles.css',
            './assets/styles.css'
        ]
        
        css_content = None
        for css_path in css_paths:
            try:
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                break
            except FileNotFoundError:
                continue
        
        if css_content:
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        else:
            # Fallback minimal CSS
            st.markdown("""
            <style>
            .main .block-container { padding: 1rem !important; }
            @media (max-width: 768px) {
                .main .block-container { padding: 0.5rem !important; }
                .stButton > button { width: 100% !important; min-height: 44px !important; }
                .stSelectbox > div > div { font-size: 16px !important; }
            }
            </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load CSS: {e}")
        # Continue without custom CSS

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

def create_sidebar_navigation(current_page="Home"):
    """Create enhanced sidebar navigation with modern styling"""
    with st.sidebar:
        # Logo và header
        display_logo(width=60, centered=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <h3 style="color: var(--primary-color); margin: 0.5rem 0;">SOULFRIEND</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">Mental Health Support</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Trang chủ": "Home",
            "📝 Đánh giá": "Assessment", 
            "📊 Kết quả": "Results",
            "🎧 Tự trợ": "SelfHelp",
            "👨‍⚕️ Tư vấn": "Consult",
            "⚙️ Quản trị": "Admin"
        }
        
        selected_page = st.selectbox(
            "Điều hướng",
            options=list(pages.keys()),
            index=list(pages.values()).index(current_page) if current_page in pages.values() else 0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Emergency contact
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b, #ff8e8e); 
                    padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <h4 style="margin: 0 0 0.5rem 0;">🚨 Khẩn cấp</h4>
            <p style="margin: 0; font-size: 0.9rem;">Hotline: <strong>115</strong></p>
            <p style="margin: 0; font-size: 0.8rem;">24/7 hỗ trợ</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats (if available)
        if 'assessment_count' in st.session_state:
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <p style="color: var(--text-secondary); font-size: 0.9rem;">
                    Đã hoàn thành: <strong>{st.session_state.assessment_count}</strong> đánh giá
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    return pages[selected_page]

def create_accessibility_controls():
    """Create accessibility control panel"""
    with st.expander("🔧 Tùy chọn trợ năng", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            # Font size control
            font_size = st.selectbox(
                "📖 Kích thước chữ",
                options=["Bình thường", "Lớn", "Rất lớn"],
                index=0
            )
            
            if font_size != "Bình thường":
                css_class = "large-text" if font_size == "Lớn" else "extra-large-text"
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        
        with col2:
            # High contrast mode
            high_contrast = st.checkbox("🔆 Chế độ tương phản cao")
            
            if high_contrast:
                st.markdown('<div class="high-contrast">', unsafe_allow_html=True)
        
        # Voice guidance (placeholder)
        if st.button("🔊 Hướng dẫn bằng giọng nói"):
            st.info("💡 Tính năng hướng dẫn giọng nói sẽ có trong phiên bản tiếp theo")
        
        # Quick tutorial
        if st.button("📚 Hướng dẫn sử dụng"):
            show_quick_tutorial()

def show_quick_tutorial():
    """Display quick tutorial for users"""
    st.markdown("""
    ### 📚 Hướng dẫn sử dụng SOULFRIEND
    
    **Bước 1:** Chọn thang đo phù hợp từ menu bên trái  
    **Bước 2:** Trả lời các câu hỏi một cách trung thực  
    **Bước 3:** Xem kết quả và khuyến nghị  
    **Bước 4:** Tìm hiểu tài nguyên tự trợ hoặc liên hệ chuyên gia
    
    ⚠️ **Lưu ý quan trọng:** Ứng dụng chỉ mang tính tham khảo, không thay thế ý kiến chuyên gia y tế.
    """)

def create_emergency_contact():
    """Create prominent emergency contact section"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b, #ff8e8e); 
                padding: 1.5rem; border-radius: 12px; color: white; 
                text-align: center; margin: 2rem 0; box-shadow: 0 4px 12px rgba(255,107,107,0.3);">
        <h3 style="margin: 0 0 1rem 0; font-size: 1.5rem;">🚨 KHẨN CẤP</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
            <div>
                <h4 style="margin: 0; font-size: 1.2rem;">📞 Hotline 24/7</h4>
                <p style="margin: 0.5rem 0; font-size: 1.1rem; font-weight: bold;">115</p>
            </div>
            <div>
                <h4 style="margin: 0; font-size: 1.2rem;">🏥 Cấp cứu</h4>
                <p style="margin: 0.5rem 0; font-size: 1.1rem; font-weight: bold;">113</p>
            </div>
            <div>
                <h4 style="margin: 0; font-size: 1.2rem;">👨‍⚕️ Tư vấn</h4>
                <p style="margin: 0.5rem 0; font-size: 1.1rem; font-weight: bold;">1900-2042</p>
            </div>
        </div>
        <p style="margin: 1rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            Nếu bạn có ý nghĩ tự hại, vui lòng liên hệ ngay lập tức
        </p>
    </div>
    """, unsafe_allow_html=True)

class SmartUI:
    """Smart UI Manager for SOULFRIEND"""
    
    def __init__(self):
        self.interaction_count = 0
    
    def track_user_interaction(self, event_type, callback=None, data=None):
        """Track user interactions"""
        self.interaction_count += 1
        if callback:
            callback(event_type, data)
    
    def display_progress_bar(self, current, total, label="Progress"):
        """Display progress bar"""
        progress = current / total if total > 0 else 0
        st.progress(progress, text=f"{label}: {current}/{total}")
    
    def show_success_message(self, message):
        """Show success message"""
        st.success(message)
    
    def show_error_message(self, message):
        """Show error message"""
        st.error(message)
    
    def show_info_message(self, message):
        """Show info message"""
        st.info(message)

# Create global instance
smart_ui = SmartUI()
