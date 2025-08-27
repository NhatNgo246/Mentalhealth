#!/usr/bin/env python3

import streamlit as st
import sys
import os

# Add the app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.questionnaires import load_dass21_vi
from components.scoring import score_dass21
from components.ui import load_css, app_header

st.set_page_config(page_title="Test App", page_icon="🧪", layout="centered")

# Load CSS
load_css()

# Header
app_header()

st.title("🧪 Test App - Quick Functionality Check")

# Test scoring function
st.subheader("1. Test Scoring Function")
if st.button("Test DASS-21 Scoring"):
    cfg = load_dass21_vi()
    # Create sample answers (all moderate responses)
    answers = {i: 1 for i in range(1, 22)}
    scores = score_dass21(answers, cfg)
    
    st.success("✅ Scoring function works!")
    for k, v in scores.items():
        st.write(f"**{k}**: Raw={v.raw}, Adjusted={v.adjusted}, Severity={v.severity}")

# Test CSS
st.subheader("2. Test CSS Loading")
st.markdown("""
<div class="info-card">
    <h4>CSS Test Card</h4>
    <p>If this card has styling (border, colors, etc), CSS is working!</p>
</div>
""", unsafe_allow_html=True)

# Test navigation
st.subheader("3. Navigation")
st.write("✅ Main page loaded successfully")
st.write("Try navigating to other pages in the sidebar to test full functionality.")

# Quick assessment test
st.subheader("4. Quick Assessment Test")
with st.form("quick_test"):
    st.write("Answer a few questions to test the flow:")
    q1 = st.radio("How are you feeling today?", [0, 1, 2, 3], format_func=lambda x: ["Good", "Okay", "Not great", "Bad"][x])
    q2 = st.radio("Stress level?", [0, 1, 2, 3], format_func=lambda x: ["Low", "Medium", "High", "Very High"][x])
    
    if st.form_submit_button("Test Submit"):
        st.session_state.test_answers = {"feeling": q1, "stress": q2}
        st.success("✅ Form submission works!")
        st.write(f"Your answers: Feeling={q1}, Stress={q2}")

st.divider()
st.info("🎉 If all tests above work, the app functionality is ready!")
