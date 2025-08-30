def apply_mobile_first_design():
    """Apply mobile-first responsive design"""
    import streamlit as st
    
    st.markdown("""
    <style>
    /* Mobile-first approach */
    .main > div {
        padding: 0.5rem;
    }
    
    /* Touch-friendly buttons */
    .stButton > button {
        min-height: 44px;
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
        margin-bottom: 8px;
    }
    
    /* Touch-friendly radio buttons */
    .stRadio > div {
        gap: 12px;
    }
    
    .stRadio > div > label {
        min-height: 44px;
        padding: 12px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        background: white;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .stRadio > div > label:hover {
        border-color: #2196F3;
        background: #f5f9ff;
    }
    
    /* Improved selectbox for mobile */
    .stSelectbox > div > div {
        min-height: 44px;
        font-size: 16px;
    }
    
    /* Better text inputs */
    .stTextInput > div > div > input {
        min-height: 44px;
        font-size: 16px;
        padding: 12px;
    }
    
    /* Progress bar optimization */
    .stProgress > div {
        height: 12px;
        border-radius: 6px;
    }
    
    /* Card containers for mobile */
    .mobile-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Mobile navigation */
    .mobile-nav {
        position: sticky;
        top: 0;
        background: white;
        z-index: 100;
        padding: 8px 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 16px;
    }
    
    /* Tablet optimizations */
    @media (min-width: 768px) {
        .main > div {
            padding: 1rem 2rem;
        }
        
        .stColumns > div {
            padding: 0 8px;
        }
    }
    
    /* Desktop optimizations */
    @media (min-width: 1024px) {
        .main > div {
            padding: 2rem 4rem;
        }
        
        .stButton > button {
            width: auto;
            min-width: 120px;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .mobile-card {
            background: #1e1e1e;
            border-color: #333;
            color: white;
        }
        
        .stRadio > div > label {
            background: #2d2d2d;
            border-color: #444;
            color: white;
        }
        
        .stRadio > div > label:hover {
            border-color: #64b5f6;
            background: #1a237e;
        }
    }
    
    /* Accessibility improvements */
    .stButton > button:focus,
    .stRadio > div > label:focus {
        outline: 3px solid #ffcc02;
        outline-offset: 2px;
    }
    
    /* High contrast mode */
    @media (prefers-contrast: high) {
        .stButton > button {
            border: 2px solid #000;
        }
        
        .stRadio > div > label {
            border: 2px solid #000;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_mobile_optimized_questionnaire():
    """Create mobile-optimized questionnaire interface"""
    import streamlit as st
    
    # Apply mobile styles
    apply_mobile_first_design()
    
    # Mobile-friendly progress indicator
    if 'current_question' in st.session_state and 'total_questions' in st.session_state:
        progress = st.session_state.current_question / st.session_state.total_questions
        st.progress(progress, text=f"Câu hỏi {st.session_state.current_question}/{st.session_state.total_questions}")
    
    # Touch-friendly question display
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    
    # Question text with larger font for mobile
    if 'current_question_text' in st.session_state:
        st.markdown(f"""
        <div style="font-size: 18px; line-height: 1.6; margin-bottom: 20px; color: #333;">
            {st.session_state.current_question_text}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def add_mobile_navigation():
    """Add mobile-optimized navigation"""
    import streamlit as st
    
    st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
    
    # Horizontal scroll for mobile navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📋", help="Đồng ý", width="stretch"):
            st.switch_page("pages/0_Consent.py")
    
    with col2:
        if st.button("🔍", help="Đánh giá", width="stretch"):
            st.switch_page("pages/1_Assessment.py")
    
    with col3:
        if st.button("📊", help="Kết quả", width="stretch"):
            st.switch_page("pages/2_Results.py")
    
    with col4:
        if st.button("📚", help="Tài nguyên", width="stretch"):
            st.switch_page("pages/3_Resources.py")
    
    with col5:
        if st.button("💬", help="Hỗ trợ", width="stretch"):
            st.switch_page("pages/5_Chatbot.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
