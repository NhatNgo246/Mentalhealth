def apply_responsive_design():
    """Apply responsive design for better mobile experience"""
    import streamlit as st
    
    st.markdown("""
    <style>
    /* Mobile responsive design */
    @media (max-width: 768px) {
        .stColumns > div {
            margin-bottom: 1rem;
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
            padding: 0.75rem;
            font-size: 1rem;
        }
    }
    
    /* Improved button styling */
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stButton > button:disabled {
        background: #cccccc;
        color: #666666;
        transform: none;
        box-shadow: none;
    }
    
    /* Progress indicator styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 10px;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    
    .stError {
        border-radius: 10px;
        border-left: 5px solid #f44336;
    }
    
    .stWarning {
        border-radius: 10px;
        border-left: 5px solid #ff9800;
    }
    
    /* Card-like containers */
    .assessment-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
