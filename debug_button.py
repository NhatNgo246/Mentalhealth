#!/usr/bin/env python3
"""
DEBUG SCRIPT - Test button "Xem kết quả" 
Kiểm tra tại sao button không hoạt động
"""

import streamlit as st
import sys
sys.path.append('/workspaces/Mentalhealth')

from components.questionnaires import load_dass21_enhanced_vi
from components.scoring import score_dass21_enhanced

st.title("🔍 DEBUG: Test Button Xem Kết Quả")

# Load sample data
if "debug_answers" not in st.session_state:
    st.session_state.debug_answers = {i: 1 for i in range(1, 22)}

st.write("### Sample answers:", st.session_state.debug_answers)

# Test form
with st.form("debug_form"):
    st.write("Form với button test:")
    
    submitted = st.form_submit_button("🎊 Test Xem Kết Quả", type="primary")
    
    if submitted:
        st.write("✅ Button được bấm!")
        
        try:
            config = load_dass21_enhanced_vi()
            result = score_dass21_enhanced(st.session_state.debug_answers, config)
            
            st.write("✅ Scoring thành công!")
            st.write(f"Total score: {result.total_score}")
            st.write(f"Severity: {result.severity_level}")
            
            # Save to session state
            st.session_state.debug_result = result
            st.write("✅ Lưu vào session state thành công!")
            
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# Display result if available
if "debug_result" in st.session_state:
    st.write("### 🎯 KẾT QUẢ ĐƯỢC LƯU:")
    result = st.session_state.debug_result
    st.write(f"Score: {result.total_score}")
    st.write(f"Severity: {result.severity_level}")
    st.write(f"Interpretation: {result.interpretation[:100]}...")

# Debug session state
st.write("### 🔍 Session State Debug:")
st.write(st.session_state)
