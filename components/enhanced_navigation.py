def create_enhanced_navigation():
    """Create enhanced navigation with better UX"""
    import streamlit as st
    
    st.markdown("""
    <style>
    .nav-container {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        margin-bottom: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .nav-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .nav-subtitle {
        color: #e0e6ed;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .nav-buttons {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .nav-button {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .status-ready { background-color: #4CAF50; }
    .status-progress { background-color: #FF9800; }
    .status-disabled { background-color: #757575; }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation container
    st.markdown("""
    <div class="nav-container">
        <div class="nav-title">🧠 SOULFRIEND V2.0</div>
        <div class="nav-subtitle">Hệ thống đánh giá sức khỏe tâm thần toàn diện</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status display
    if 'enhanced_scores' in st.session_state and st.session_state.enhanced_scores:
        st.success("✅ Đánh giá đã hoàn thành - Xem kết quả chi tiết")
    
    # Enhanced navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📋 Đồng ý tham gia", width="stretch"):
            st.switch_page("pages/0_Consent.py")
    
    with col2:
        disabled = 'consent_given' not in st.session_state or not st.session_state.consent_given
        if st.button("🔍 Bắt đầu đánh giá", disabled=disabled, width="stretch"):
            st.switch_page("pages/1_Assessment.py")
    
    with col3:
        disabled = 'enhanced_scores' not in st.session_state or not st.session_state.enhanced_scores
        if st.button("📊 Xem kết quả", disabled=disabled, width="stretch"):
            st.switch_page("pages/2_Results.py")
    
    with col4:
        if st.button("📚 Tài nguyên", width="stretch"):
            st.switch_page("pages/3_Resources.py")
    
    with col5:
        if st.button("💬 Hỗ trợ AI", width="stretch"):
            st.switch_page("pages/5_Chatbot.py")
    
    # Progress indicator
    if 'assessment_progress' in st.session_state:
        progress = st.session_state.assessment_progress
        st.progress(progress, text=f"Tiến độ đánh giá: {int(progress * 100)}%")


def apply_responsive_design():
    """Apply responsive design styles for mobile optimization"""
    import streamlit as st
    
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .nav-buttons {
            flex-direction: column;
        }
        
        .nav-button {
            width: 100%;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .nav-title {
            font-size: 1.2rem;
        }
        
        .metric-card {
            margin-bottom: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
