"""
Optimized UI Components - Clean, Accessible, and Maintainable
Giải quyết các vấn đề về inline styling và accessibility
"""

import streamlit as st

def load_optimized_css():
    """Load optimized CSS with variables"""
    try:
        with open('/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/assets/ui-optimized.css', 'r', encoding='utf-8') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Optimized CSS file not found, using fallback styles")

def create_hero_section(title: str, subtitle: str, description: str):
    """Create hero section with optimized styling"""
    st.markdown(f"""
    <div class="hero-section">
        <h1 style="margin: 0; font-size: var(--font-xxl); color: white;">{title}</h1>
        <p style="margin: var(--spacing-sm) 0; font-size: var(--font-lg); opacity: 0.9;">
            {subtitle}
        </p>
        <div style="font-size: var(--font-sm); opacity: 0.8;">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_mood_check_section():
    """Create mood check section with accessibility"""
    st.markdown("""
    <div class="mood-check-section">
        <h3 style="margin: 0 0 var(--spacing-sm) 0; color: #92400e;">
            🌈 Hôm nay tâm trạng bạn thế nào?
        </h3>
        <div style="display: flex; justify-content: center; gap: var(--spacing-sm); flex-wrap: wrap;">
            <button class="feature-card" style="border: none; cursor: pointer;" 
                    aria-label="Tâm trạng rất vui" role="button">
                😄 Rất vui
            </button>
            <button class="feature-card" style="border: none; cursor: pointer;"
                    aria-label="Tâm trạng ổn định" role="button">
                😊 Ổn định
            </button>
            <button class="feature-card" style="border: none; cursor: pointer;"
                    aria-label="Tâm trạng bình thường" role="button">
                😐 Bình thường
            </button>
            <button class="feature-card" style="border: none; cursor: pointer;"
                    aria-label="Tâm trạng hơi buồn" role="button">
                😔 Hơi buồn
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_info_card(title: str, description: str, icon: str = "📋"):
    """Create information card with consistent styling"""
    st.markdown(f"""
    <div class="info-card">
        <div style="display: flex; align-items: center; margin-bottom: var(--spacing-sm);">
            <div style="font-size: 2.5rem; margin-right: var(--spacing-sm);">{icon}</div>
            <div>
                <h3 style="margin: 0; color: var(--text-primary);">{title}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">
                    Bài test ngắn chỉ mất 5 phút
                </p>
            </div>
        </div>
        <p style="color: var(--text-secondary); line-height: 1.6; margin: 0;">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_consent_section():
    """Create consent section with proper structure"""
    st.markdown("""
    <div class="consent-section">
        <div style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: var(--spacing-sm);">🤝</div>
            <h3 style="color: var(--text-primary); margin-bottom: var(--spacing-sm);">
                Chúng ta hãy làm quen trước nhé!
            </h3>
            <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: var(--spacing-md);">
                Trước khi bắt đầu cuộc trò chuyện thú vị này, tôi muốn bạn biết rằng:
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--spacing-sm); margin: var(--spacing-md) 0;">
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔐</div>
                <h4 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">Bí mật tuyệt đối</h4>
                <p style="margin: 0; color: var(--text-muted); font-size: var(--font-xs);">
                    Thông tin của bạn được bảo vệ như kim cương 💎
                </p>
            </div>
            
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <h4 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">AI thông minh</h4>
                <p style="margin: 0; color: var(--text-muted); font-size: var(--font-xs);">
                    Sẵn sàng trò chuyện 24/7, không bao giờ mệt mỏi! 🌙
                </p>
            </div>
            
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <h4 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">Chính xác cao</h4>
                <p style="margin: 0; color: var(--text-muted); font-size: var(--font-xs);">
                    Dựa trên khoa học, không phải đoán mò 🔬
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_progress_indicator(current_step: int, total_steps: int, title: str):
    """Create progress indicator with accessibility"""
    st.markdown(f"""
    <div class="progress-indicator" role="progressbar" aria-valuenow="{current_step}" 
         aria-valuemin="1" aria-valuemax="{total_steps}" aria-label="Tiến độ bài test">
        <div style="display: flex; align-items: center; justify-content: center; gap: var(--spacing-sm);">
            <div style="font-size: 1.5rem;">⚡</div>
            <div>
                <h4 style="margin: 0; color: #065f46;">Bước {current_step}/{total_steps}: {title}</h4>
                <p style="margin: 0; color: #047857;">Bạn đang làm rất tốt! 🌟</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_question_card(number: int, question: str):
    """Create question card with consistent styling"""
    st.markdown(f"""
    <div class="question-card">
        <h4 style="margin: 0 0 var(--spacing-sm) 0; color: var(--text-primary); font-size: var(--font-md);">
            <span style="background: var(--primary-gradient); color: white; padding: 0.3rem 0.8rem; 
                         border-radius: var(--radius-md); font-size: var(--font-xs); margin-right: var(--spacing-sm);">
                {number}
            </span>
            {question}
        </h4>
    </div>
    """, unsafe_allow_html=True)

def create_results_header():
    """Create results section header"""
    st.markdown("""
    <div style="text-align: center; margin: var(--spacing-lg) 0;">
        <h2 style="background: var(--primary-gradient); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent; margin: 0; font-size: var(--font-xxl);">
            🎊 Kết quả đánh giá của bạn
        </h2>
        <p style="color: var(--text-secondary); margin: var(--spacing-sm) 0; font-size: var(--font-lg);">
            Đây là "bức tranh" tâm lý của bạn trong thời gian qua! 🎨
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, score: int, severity: str, emoji: str, color: str):
    """Create metric display card"""
    st.markdown(f"""
    <div style="background: {color}; color: white; padding: var(--spacing-md); 
                border-radius: var(--radius-md); text-align: center; margin: 0.5rem; 
                box-shadow: var(--shadow-medium);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
        <h3 style="margin: 0; color: white;">{title}</h3>
        <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">{score} điểm</div>
        <div style="opacity: 0.9;">Mức độ: {severity}</div>
    </div>
    """, unsafe_allow_html=True)

def create_recommendation_card(text: str):
    """Create recommendation item"""
    st.markdown(f"""
    <div class="recommendation-card">
        <p style="margin: 0; color: #047857; font-size: var(--font-sm);">{text}</p>
    </div>
    """, unsafe_allow_html=True)

def create_success_message(title: str, message: str):
    """Create success/celebration message"""
    st.markdown(f"""
    <div style="background: var(--success-gradient); color: white; padding: var(--spacing-lg); 
                border-radius: var(--radius-lg); text-align: center; margin: var(--spacing-sm) 0;">
        <div style="font-size: 3rem; margin-bottom: var(--spacing-sm);">🎉</div>
        <h3 style="margin: 0; color: white;">{title}</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
