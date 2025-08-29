#!/usr/bin/env python3
"""
🎯 SOULFRIEND DEMO - Simplified User Testing Version
"""

import streamlit as st
import sys
import os
sys.path.insert(0, "/workspaces/Mentalhealth")

from components.questionnaires import QuestionnaireManager
from components.scoring import calculate_scores
from components.pdf_export import generate_assessment_report

st.set_page_config(
    page_title="SOULFRIEND Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🧠 SOULFRIEND V2.0 - Mental Health Assessment")
    st.subheader("Demo Version for User Testing")
    
    # Sidebar
    st.sidebar.title("🎯 User Test Demo")
    st.sidebar.markdown("---")
    
    # Test scenarios
    scenario = st.sidebar.selectbox(
        "Chọn Scenario Test:",
        [
            "Basic Questionnaire Test",
            "Scoring System Test", 
            "PDF Export Test",
            "Full User Journey"
        ]
    )
    
    if scenario == "Basic Questionnaire Test":
        test_questionnaire_loading()
    elif scenario == "Scoring System Test":
        test_scoring_system()
    elif scenario == "PDF Export Test":
        test_pdf_export()
    elif scenario == "Full User Journey":
        test_full_user_journey()

def test_questionnaire_loading():
    st.header("📝 Test 1: Questionnaire Loading")
    
    try:
        manager = QuestionnaireManager()
        questionnaires = ['PHQ-9', 'GAD-7', 'DASS-21', 'PSS-10', 'EPDS']
        
        selected_q = st.selectbox("Chọn Questionnaire:", questionnaires)
        
        if st.button("Load Questionnaire"):
            with st.spinner("Đang tải questionnaire..."):
                data = manager.get_questionnaire(selected_q)
                
                if data:
                    st.success(f"✅ {selected_q} loaded successfully!")
                    st.json({"status": "success", "questionnaire": selected_q, "data_type": type(data).__name__})
                    
                    # Show sample question if available
                    if isinstance(data, dict):
                        if 'items' in data and len(data['items']) > 0:
                            st.write("**Sample Question:**")
                            st.write(data['items'][0])
                        elif 'questions' in data and len(data['questions']) > 0:
                            st.write("**Sample Question:**")
                            st.write(data['questions'][0])
                else:
                    st.error(f"❌ Failed to load {selected_q}")
                    
    except Exception as e:
        st.error(f"❌ Error: {e}")

def test_scoring_system():
    st.header("🧮 Test 2: Scoring System")
    
    questionnaire_type = st.selectbox(
        "Chọn Questionnaire:",
        ['PHQ-9', 'GAD-7', 'DASS-21', 'PSS-10', 'EPDS']
    )
    
    # Sample responses for each questionnaire
    sample_responses = {
        'PHQ-9': [1, 2, 1, 0, 2, 1, 3, 2, 1],
        'GAD-7': [2, 1, 3, 2, 1, 0, 2],
        'DASS-21': [1] * 21,
        'PSS-10': [2] * 10,
        'EPDS': [1, 0, 2, 1, 0, 1, 2, 1, 0, 1]
    }
    
    responses = sample_responses[questionnaire_type]
    
    st.write(f"**Sample responses for {questionnaire_type}:**")
    st.write(responses)
    
    if st.button("Calculate Score"):
        with st.spinner("Đang tính điểm..."):
            try:
                result = calculate_scores(responses, questionnaire_type)
                
                if result:
                    st.success("✅ Scoring successful!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Score", result['total_score'])
                    
                    with col2:
                        st.metric("Severity", result['severity'])
                    
                    with col3:
                        st.metric("Questionnaire", questionnaire_type)
                    
                    st.write("**Interpretation:**")
                    st.write(result['interpretation'])
                    
                    st.json(result)
                else:
                    st.error("❌ Scoring failed")
                    
            except Exception as e:
                st.error(f"❌ Scoring error: {e}")

def test_pdf_export():
    st.header("📄 Test 3: PDF Export")
    
    # Sample assessment data
    sample_data = {
        'questionnaire_type': 'PHQ-9',
        'total_score': 12,
        'severity': 'Moderate',
        'interpretation': 'Trầm cảm vừa',
        'responses': [1, 2, 1, 0, 2, 1, 3, 2, 1],
        'user_info': {
            'name': 'Test User',
            'age': 25,
            'date': '2025-08-27'
        }
    }
    
    st.write("**Sample Assessment Data:**")
    st.json(sample_data)
    
    if st.button("Generate PDF Report"):
        with st.spinner("Đang tạo báo cáo PDF..."):
            try:
                pdf_content = generate_assessment_report(sample_data)
                
                if pdf_content and len(pdf_content) > 100:
                    st.success(f"✅ PDF generated successfully! ({len(pdf_content)} bytes)")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_content,
                        file_name="soulfriend_demo_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ PDF generation failed")
                    
            except Exception as e:
                st.error(f"❌ PDF error: {e}")

def test_full_user_journey():
    st.header("👤 Test 4: Full User Journey")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'questionnaire' not in st.session_state:
        st.session_state.questionnaire = 'PHQ-9'
    
    # Progress bar
    progress = st.session_state.step / 4
    st.progress(progress)
    st.write(f"**Step {st.session_state.step}/4**")
    
    if st.session_state.step == 1:
        st.subheader("1️⃣ Chọn Questionnaire")
        
        questionnaire = st.selectbox(
            "Chọn bộ câu hỏi:",
            ['PHQ-9', 'GAD-7', 'DASS-21', 'PSS-10', 'EPDS']
        )
        
        if st.button("Tiếp tục"):
            st.session_state.questionnaire = questionnaire
            st.session_state.step = 2
            st.rerun()
    
    elif st.session_state.step == 2:
        st.subheader(f"2️⃣ Trả lời {st.session_state.questionnaire}")
        
        # Simulate answering questions
        num_questions = {
            'PHQ-9': 9, 'GAD-7': 7, 'DASS-21': 21, 'PSS-10': 10, 'EPDS': 10
        }[st.session_state.questionnaire]
        
        st.write(f"Mô phỏng trả lời {num_questions} câu hỏi:")
        
        responses = []
        for i in range(min(3, num_questions)):  # Show only first 3 questions
            response = st.selectbox(
                f"Câu {i+1}: Sample question {i+1}",
                options=[0, 1, 2, 3],
                format_func=lambda x: f"{x} - {'Không bao giờ' if x==0 else 'Thỉnh thoảng' if x==1 else 'Thường xuyên' if x==2 else 'Hầu hết thời gian'}",
                key=f"q_{i}"
            )
            responses.append(response)
        
        # Auto-fill remaining responses for demo
        while len(responses) < num_questions:
            responses.append(1)  # Default response
        
        if st.button("Hoàn thành"):
            st.session_state.responses = responses
            st.session_state.step = 3
            st.rerun()
    
    elif st.session_state.step == 3:
        st.subheader("3️⃣ Kết quả đánh giá")
        
        try:
            result = calculate_scores(st.session_state.responses, st.session_state.questionnaire)
            
            if result:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Điểm tổng", result['total_score'])
                
                with col2:
                    st.metric("Mức độ", result['severity'])
                
                with col3:
                    st.metric("Questionnaire", st.session_state.questionnaire)
                
                st.write("**Giải thích:**")
                st.info(result['interpretation'])
                
                if st.button("Tạo báo cáo PDF"):
                    st.session_state.step = 4
                    st.rerun()
            else:
                st.error("❌ Không thể tính điểm")
                
        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
    
    elif st.session_state.step == 4:
        st.subheader("4️⃣ Báo cáo PDF")
        
        assessment_data = {
            'questionnaire_type': st.session_state.questionnaire,
            'total_score': sum(st.session_state.responses),
            'severity': 'Moderate',
            'interpretation': 'Demo interpretation',
            'responses': st.session_state.responses,
            'user_info': {
                'name': 'Demo User',
                'age': 25,
                'date': '2025-08-27'
            }
        }
        
        try:
            pdf_content = generate_assessment_report(assessment_data)
            
            if pdf_content:
                st.success("✅ Báo cáo PDF đã được tạo thành công!")
                
                st.download_button(
                    label="📥 Tải báo cáo PDF",
                    data=pdf_content,
                    file_name=f"soulfriend_{st.session_state.questionnaire}_report.pdf",
                    mime="application/pdf"
                )
                
                if st.button("🔄 Bắt đầu lại"):
                    st.session_state.step = 1
                    st.session_state.responses = []
                    st.rerun()
            else:
                st.error("❌ Không thể tạo báo cáo PDF")
                
        except Exception as e:
            st.error(f"❌ Lỗi PDF: {e}")

if __name__ == "__main__":
    main()
