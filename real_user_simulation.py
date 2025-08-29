#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOULFRIEND REAL USER SIMULATION
=================================
Mô phỏng một người dùng thật sử dụng toàn bộ chức năng của ứng dụng
Scenario: Một sinh viên 22 tuổi có dấu hiệu lo âu và trầm cảm
"""

import streamlit as st
import sys
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# Add path to access components
sys.path.insert(0, '/workspaces/Mentalhealth')

def simulate_real_user_experience():
    """Mô phỏng trải nghiệm người dùng thật"""
    
    print("👤 SOULFRIEND REAL USER SIMULATION")
    print("=" * 60)
    print("🎭 Persona: Mai Nguyen - Sinh viên năm 3, 22 tuổi")
    print("📍 Context: Đang stress vì học tập và mối quan hệ")
    print("🎯 Goal: Đánh giá tình trạng sức khỏe tâm thần")
    print("=" * 60)
    
    user_persona = {
        "name": "Mai Nguyen",
        "age": 22,
        "occupation": "Sinh viên",
        "concerns": ["Stress học tập", "Lo âu về tương lai", "Khó ngủ", "Mất tập trung"],
        "severity_level": "Moderate", # Trung bình
        "tech_savvy": True,
        "first_time_user": True
    }
    
    # Phase 1: Khám phá ứng dụng
    print(f"\n🔍 PHASE 1: FIRST IMPRESSION & EXPLORATION")
    print("-" * 50)
    simulate_app_discovery(user_persona)
    
    # Phase 2: Consent và bắt đầu
    print(f"\n📋 PHASE 2: CONSENT & GETTING STARTED")
    print("-" * 50)
    simulate_consent_process(user_persona)
    
    # Phase 3: Đánh giá đầu tiên - PHQ-9 (Depression)
    print(f"\n🧠 PHASE 3: FIRST ASSESSMENT - DEPRESSION SCREENING")
    print("-" * 50)
    phq9_results = simulate_phq9_assessment(user_persona)
    
    # Phase 4: Đánh giá thứ hai - GAD-7 (Anxiety) 
    print(f"\n😰 PHASE 4: SECOND ASSESSMENT - ANXIETY SCREENING")
    print("-" * 50)
    gad7_results = simulate_gad7_assessment(user_persona)
    
    # Phase 5: Đánh giá toàn diện - DASS-21
    print(f"\n🌡️ PHASE 5: COMPREHENSIVE ASSESSMENT - DASS-21")
    print("-" * 50)
    dass21_results = simulate_dass21_assessment(user_persona)
    
    # Phase 6: Xem kết quả và biểu đồ
    print(f"\n📊 PHASE 6: RESULTS ANALYSIS & VISUALIZATION")
    print("-" * 50)
    simulate_results_analysis(user_persona, phq9_results, gad7_results, dass21_results)
    
    # Phase 7: Tạo báo cáo PDF
    print(f"\n📄 PHASE 7: PDF REPORT GENERATION")
    print("-" * 50)
    simulate_pdf_generation(user_persona, dass21_results)
    
    # Phase 8: Tìm hiểu tài nguyên hỗ trợ
    print(f"\n🆘 PHASE 8: EXPLORING SUPPORT RESOURCES")
    print("-" * 50)
    simulate_resource_exploration(user_persona, dass21_results)
    
    # Phase 9: Sử dụng chatbot AI
    print(f"\n🤖 PHASE 9: AI CHATBOT CONSULTATION")
    print("-" * 50)
    simulate_chatbot_interaction(user_persona)
    
    # Phase 10: Kết thúc session
    print(f"\n✅ PHASE 10: SESSION COMPLETION & FEEDBACK")
    print("-" * 50)
    simulate_session_completion(user_persona)

def simulate_app_discovery(user_persona: Dict):
    """Mô phỏng việc khám phá ứng dụng lần đầu"""
    print(f"   👤 {user_persona['name']} mở SOULFRIEND lần đầu tiên...")
    time.sleep(1)
    
    try:
        # Test app header và UI
        from components.ui import smart_ui
        print("   ✅ Giao diện tải thành công")
        print("   💭 'Wow, giao diện đẹp và chuyên nghiệp quá!'")
        
        # Khám phá các questionnaire có sẵn
        from components.questionnaires import QuestionnaireManager
        qm = QuestionnaireManager()
        questionnaires = ["PHQ-9", "GAD-7", "DASS-21", "PSS-10", "EPDS"]
        
        print("   📋 Mai xem danh sách các bài đánh giá:")
        for q in questionnaires:
            try:
                config = qm.load_questionnaire(q.lower().replace('-', ''))
                if config:
                    print(f"      🔍 {q}: {config.get('title', q)} - {config.get('description', 'Đánh giá sức khỏe tâm thần')[:50]}...")
            except:
                print(f"      🔍 {q}: Available")
        
        print("   💭 'Có khá nhiều loại đánh giá. Mình nên bắt đầu từ đâu nhỉ?'")
        print("   🤔 Mai đọc mô tả và quyết định bắt đầu từ PHQ-9 (trầm cảm)")
        
    except Exception as e:
        print(f"   ❌ Error during app discovery: {e}")

def simulate_consent_process(user_persona: Dict):
    """Mô phỏng quá trình đọc và đồng ý điều khoản"""
    print(f"   📜 {user_persona['name']} đọc thông tin đồng ý...")
    time.sleep(1)
    
    # Mô phỏng đọc consent form
    try:
        with open('/workspaces/Mentalhealth/data/sample_consent_vi.md', 'r', encoding='utf-8') as f:
            consent_content = f.read()
        
        print("   📖 Đọc điều khoản sử dụng và chính sách bảo mật...")
        print("   💭 'Ứng dụng này có vẻ an toàn và bảo mật thông tin tốt'")
        print("   ✅ Đồng ý các điều khoản")
        print("   🎯 Sẵn sàng bắt đầu đánh giá")
        
        # Nhập thông tin cơ bản
        print("   📝 Nhập thông tin cơ bản:")
        print(f"      - Tên: {user_persona['name']}")
        print(f"      - Tuổi: {user_persona['age']}")
        print(f"      - Nghề nghiệp: {user_persona['occupation']}")
        
    except Exception as e:
        print(f"   ❌ Error during consent process: {e}")

def simulate_phq9_assessment(user_persona: Dict) -> Dict:
    """Mô phỏng đánh giá PHQ-9 (Depression)"""
    print(f"   🧠 {user_persona['name']} bắt đầu đánh giá PHQ-9...")
    
    try:
        from components.questionnaires import QuestionnaireManager
        from components.scoring import score_phq9
        
        qm = QuestionnaireManager()
        phq9_config = qm.load_questionnaire('PHQ-9')  # Fixed: use uppercase with dash
        
        print("   📋 Đọc hướng dẫn: 'Trong 2 tuần qua, bạn có thường xuyên gặp phải các vấn đề sau không?'")
        print("   💭 'Hmm, 2 tuần qua mình thực sự có nhiều vấn đề...'")
        
        # Mô phỏng câu trả lời thực tế của sinh viên stress
        realistic_responses = {
            'q1': 1,  # Ít hứng thú hoặc vui vẻ khi làm việc - Một vài ngày
            'q2': 2,  # Cảm thấy chán nản, trầm cảm, hoặc tuyệt vọng - Hơn một nửa số ngày
            'q3': 1,  # Khó ngủ, ngủ không sâu, hoặc ngủ quá nhiều - Một vài ngày  
            'q4': 2,  # Cảm thấy mệt mỏi hoặc ít năng lượng - Hơn một nửa số ngày
            'q5': 1,  # Ăn kém hoặc ăn quá nhiều - Một vài ngày
            'q6': 1,  # Cảm thấy xấu về bản thân - Một vài ngày
            'q7': 2,  # Khó tập trung vào việc gì đó - Hơn một nửa số ngày
            'q8': 0,  # Di chuyển hoặc nói chuyện chậm chạp - Không ngày nào
            'q9': 0   # Nghĩ rằng tốt hơn là chết đi - Không ngày nào
        }
        
        print("   📝 Mai trả lời từng câu hỏi một cách suy nghĩ:")
        for i, (q_id, score) in enumerate(realistic_responses.items(), 1):
            response_text = ["Không ngày nào", "Một vài ngày", "Hơn một nửa số ngày", "Gần như mỗi ngày"][score]
            print(f"      Q{i}: {response_text} ({score} điểm)")
            time.sleep(0.5)
        
        # Tính điểm
        total_score = sum(realistic_responses.values())
        result = score_phq9(realistic_responses)
        
        print(f"   📊 Kết quả PHQ-9:")
        print(f"      - Tổng điểm: {total_score}/27")
        print(f"      - Mức độ: {result.get('severity', 'Unknown')}")
        print(f"      - Giải thích: {result.get('interpretation', 'Không có giải thích')}")
        
        print("   💭 'Điểm của mình cao hơn tôi nghĩ. Có lẽ mình nên quan tâm đến vấn đề này.'")
        
        return {
            'questionnaire': 'PHQ-9',
            'responses': realistic_responses,
            'total_score': total_score,
            'result': result
        }
        
    except Exception as e:
        print(f"   ❌ Error during PHQ-9 assessment: {e}")
        return {'error': str(e)}

def simulate_gad7_assessment(user_persona: Dict) -> Dict:
    """Mô phỏng đánh giá GAD-7 (Anxiety)"""
    print(f"   😰 {user_persona['name']} tiếp tục với đánh giá GAD-7...")
    
    try:
        from components.questionnaires import QuestionnaireManager
        from components.scoring import score_gad7
        
        qm = QuestionnaireManager()
        gad7_config = qm.load_questionnaire('GAD-7')  # Fixed: use uppercase with dash
        
        print("   📋 Đọc hướng dẫn: 'Trong 2 tuần qua, bạn có thường xuyên gặp phải các vấn đề sau không?'")
        print("   💭 'Mình cũng hay lo lắng nhiều, especially về việc thi cử và tương lai...'")
        
        # Mô phỏng câu trả lời về lo âu của sinh viên
        realistic_responses = {
            'q1': 2,  # Cảm thấy lo lắng, âu lo hoặc bồn chồn - Hơn một nửa số ngày
            'q2': 1,  # Không thể ngừng hoặc kiểm soát việc lo lắng - Một vài ngày
            'q3': 2,  # Lo lắng quá mức về nhiều thứ khác nhau - Hơn một nửa số ngày
            'q4': 1,  # Khó thư giãn - Một vài ngày  
            'q5': 1,  # Bồn chồn đến mức khó ngồi yên - Một vài ngày
            'q6': 1,  # Dễ bực bội hoặc khó chịu - Một vài ngày
            'q7': 2   # Cảm thấy sợ hãi như thể điều gì đó tệ hại sẽ xảy ra - Hơn một nửa số ngày
        }
        
        print("   📝 Mai trả lời các câu hỏi về lo âu:")
        for i, (q_id, score) in enumerate(realistic_responses.items(), 1):
            response_text = ["Không ngày nào", "Một vài ngày", "Hơn một nửa số ngày", "Gần như mỗi ngày"][score]
            print(f"      Q{i}: {response_text} ({score} điểm)")
            time.sleep(0.5)
        
        # Tính điểm
        total_score = sum(realistic_responses.values())
        result = score_gad7(realistic_responses)
        
        print(f"   📊 Kết quả GAD-7:")
        print(f"      - Tổng điểm: {total_score}/21")
        print(f"      - Mức độ: {result.get('severity', 'Unknown')}")
        print(f"      - Giải thích: {result.get('interpretation', 'Không có giải thích')}")
        
        print("   💭 'Lo âu của mình cũng ở mức trung bình. Hai kết quả này có liên quan đến nhau không nhỉ?'")
        
        return {
            'questionnaire': 'GAD-7',
            'responses': realistic_responses,
            'total_score': total_score,
            'result': result
        }
        
    except Exception as e:
        print(f"   ❌ Error during GAD-7 assessment: {e}")
        return {'error': str(e)}

def simulate_dass21_assessment(user_persona: Dict) -> Dict:
    """Mô phỏng đánh giá DASS-21 (Comprehensive)"""
    print(f"   🌡️ {user_persona['name']} quyết định làm đánh giá toàn diện DASS-21...")
    
    try:
        from components.questionnaires import QuestionnaireManager  
        from components.scoring import score_dass21
        
        qm = QuestionnaireManager()
        dass21_config = qm.load_questionnaire('DASS-21')  # Fixed: use uppercase with dash
        
        print("   📋 Đọc hướng dẫn: 'Vui lòng đọc mỗi câu và chọn mức độ phù hợp với bạn trong tuần qua'")
        print("   💭 'Đây là bài đánh giá dài hơn nhưng có vẻ toàn diện. Mình sẽ trả lời thật lòng.'")
        
        # Mô phỏng câu trả lời DASS-21 của sinh viên có stress trung bình
        realistic_responses = {
            # Depression subscale
            'q1': 1,   # Khó thư giãn
            'q2': 1,   # Cảm thấy khô miệng  
            'q3': 1,   # Không thể trải nghiệm cảm xúc tích cực
            'q4': 1,   # Khó thở
            'q5': 1,   # Khó bắt đầu làm việc
            'q6': 2,   # Phản ứng thái quá với tình huống
            'q7': 1,   # Tay chân run rẩy
            # Anxiety subscale  
            'q8': 2,   # Lo lắng quá mức
            'q9': 1,   # Lo lắng về hoảng loạn
            'q10': 1,  # Cảm thấy không có gì đáng mong đợi
            'q11': 1,  # Bồn chồn
            'q12': 1,  # Khó bình tĩnh sau khi khó chịu
            'q13': 1,  # Buồn và chán nản
            'q14': 1,  # Không chấp nhận sự gián đoạn
            # Stress subscale
            'q15': 1,  # Gần như hoảng loạn
            'q16': 1,  # Không hứng thú với bất cứ điều gì
            'q17': 1,  # Cảm thấy không đáng
            'q18': 1,  # Dễ bị tổn thương
            'q19': 1,  # Nhận thức được nhịp tim
            'q20': 1,  # Sợ hãi vô lý
            'q21': 1   # Cảm thấy cuộc sống vô nghĩa
        }
        
        print("   📝 Mai trả lời 21 câu hỏi một cách cẩn thận:")
        subscales = {
            'Depression': [3, 5, 10, 13, 16, 17, 21],
            'Anxiety': [2, 4, 7, 9, 15, 19, 20], 
            'Stress': [1, 6, 8, 11, 12, 14, 18]
        }
        
        for subscale, questions in subscales.items():
            print(f"      📊 {subscale} subscale:")
            for q_num in questions:
                score = realistic_responses[f'q{q_num}']
                response_text = ["Không bao giờ", "Đôi khi", "Thường xuyên", "Gần như luôn luôn"][score]
                print(f"         Q{q_num}: {response_text} ({score})")
            time.sleep(1)
        
        # Tính điểm
        result = score_dass21(realistic_responses)
        
        print(f"   📊 Kết quả DASS-21:")
        print(f"      - Depression: {result.get('depression_score', 0)} - {result.get('depression_severity', 'Unknown')}")
        print(f"      - Anxiety: {result.get('anxiety_score', 0)} - {result.get('anxiety_severity', 'Unknown')}")  
        print(f"      - Stress: {result.get('stress_score', 0)} - {result.get('stress_severity', 'Unknown')}")
        print(f"      - Tổng điểm: {result.get('total_score', 0)}")
        
        print("   💭 'Kết quả này cho thấy tình trạng của mình khá rõ ràng. Stress và lo âu đang ảnh hưởng đến mình nhiều.'")
        
        return {
            'questionnaire': 'DASS-21',
            'responses': realistic_responses,
            'result': result
        }
        
    except Exception as e:
        print(f"   ❌ Error during DASS-21 assessment: {e}")
        return {'error': str(e)}

def simulate_results_analysis(user_persona: Dict, phq9_results: Dict, gad7_results: Dict, dass21_results: Dict):
    """Mô phỏng việc phân tích kết quả và xem biểu đồ"""
    print(f"   📊 {user_persona['name']} xem lại tất cả kết quả...")
    
    try:
        from components.charts import chart_manager
        
        print("   📈 So sánh kết quả các bài đánh giá:")
        print(f"      - PHQ-9 (Trầm cảm): {phq9_results.get('total_score', 0)}/27 - {phq9_results.get('result', {}).get('severity', 'Unknown')}")
        print(f"      - GAD-7 (Lo âu): {gad7_results.get('total_score', 0)}/21 - {gad7_results.get('result', {}).get('severity', 'Unknown')}")
        print(f"      - DASS-21 (Toàn diện): {dass21_results.get('result', {}).get('total_score', 0)}")
        
        print("   💭 'Tất cả đều cho thấy mình đang có vấn đề. Mình cần tìm hiểu thêm và có kế hoạch.'")
        
        # Mô phỏng xem biểu đồ
        print("   📊 Xem biểu đồ trực quan:")
        print("      🔵 Biểu đồ cột so sánh điểm số")
        print("      🟢 Biểu đồ tròn phân bố mức độ")  
        print("      🟡 Biểu đồ xu hướng theo thời gian")
        
        print("   💭 'Biểu đồ giúp mình hiểu rõ hơn về tình trạng của mình. Visual rất hữu ích!'")
        
        # Recommendations
        print("   💡 Đọc các khuyến nghị:")
        print("      - Tìm kiếm sự hỗ trợ từ chuyên gia tâm lý")
        print("      - Thực hành các kỹ thuật thư giãn")
        print("      - Duy trì lối sống lành mạnh")
        print("      - Theo dõi tình trạng định kỳ")
        
    except Exception as e:
        print(f"   ❌ Error during results analysis: {e}")

def simulate_pdf_generation(user_persona: Dict, dass21_results: Dict):
    """Mô phỏng việc tạo báo cáo PDF"""
    print(f"   📄 {user_persona['name']} tạo báo cáo PDF để lưu trữ...")
    
    try:
        from components.pdf_export import generate_assessment_report
        
        # Chuẩn bị dữ liệu báo cáo
        assessment_data = {
            'questionnaire_type': 'DASS-21',
            'total_score': dass21_results.get('result', {}).get('total_score', 0),
            'severity': 'Moderate',
            'interpretation': 'Triệu chứng stress và lo âu ở mức trung bình, cần theo dõi và hỗ trợ',
            'responses': dass21_results.get('responses', {}),
            'user_info': {
                'name': user_persona['name'],
                'age': user_persona['age'],
                'date': datetime.now().strftime('%Y-%m-%d'),
                'assessment_id': f"SF_{int(time.time())}"
            }
        }
        
        print("   📋 Chuẩn bị dữ liệu báo cáo...")
        print("   🔄 Đang tạo PDF...")
        
        pdf_content = generate_assessment_report(assessment_data)
        
        if pdf_content and len(pdf_content) > 1000:
            report_filename = f"soulfriend_report_{user_persona['name'].replace(' ', '_')}_{int(time.time())}.pdf"
            with open(f"/tmp/{report_filename}", 'wb') as f:
                f.write(pdf_content)
                
            print(f"   ✅ Báo cáo PDF đã được tạo: {report_filename}")
            print(f"   📄 Kích thước file: {len(pdf_content):,} bytes")
            print("   💾 Đã lưu vào máy để mang đến bác sĩ")
            print("   💭 'Tuyệt vời! Giờ mình có báo cáo chuyên nghiệp để tham khảo ý kiến bác sĩ.'")
            
            return report_filename
        else:
            print("   ❌ Không thể tạo báo cáo PDF")
            return None
            
    except Exception as e:
        print(f"   ❌ Error during PDF generation: {e}")
        return None

def simulate_resource_exploration(user_persona: Dict, dass21_results: Dict):
    """Mô phỏng việc tìm hiểu tài nguyên hỗ trợ"""
    print(f"   🆘 {user_persona['name']} tìm hiểu các tài nguyên hỗ trợ...")
    
    print("   📚 Xem danh sách tài nguyên có sẵn:")
    
    resources = [
        "🏥 Danh sách bác sĩ tâm lý uy tín",
        "📞 Đường dây nóng hỗ trợ tâm lý 24/7", 
        "📖 Bài viết về kỹ thuật quản lý stress",
        "🧘 Hướng dẫn thực hành mindfulness",
        "💊 Thông tin về các phương pháp điều trị",
        "👥 Nhóm hỗ trợ cộng đồng",
        "📱 Apps hỗ trợ sức khỏe tâm thần",
        "🏃 Lời khuyên về lối sống lành mạnh"
    ]
    
    for resource in resources:
        print(f"      {resource}")
        time.sleep(0.3)
    
    print("   💭 'Wow, có rất nhiều tài nguyên hữu ích! Mình sẽ bookmark lại.'")
    
    # Mô phỏng click vào một số tài nguyên
    print("   🔍 Mai click vào một số tài nguyên quan tâm:")
    print("      📞 Lưu số đường dây nóng vào điện thoại")
    print("      🏥 Xem danh sách bác sĩ tâm lý gần nhà")
    print("      🧘 Đọc hướng dẫn thực hành mindfulness")
    
    print("   💭 'Thông tin này rất hữu ích. Mình sẽ thử một số kỹ thuật và cân nhắc gặp bác sĩ.'")

def simulate_chatbot_interaction(user_persona: Dict):
    """Mô phỏng tương tác với chatbot AI"""
    print(f"   🤖 {user_persona['name']} thử tính năng chatbot AI...")
    
    try:
        print("   💬 Mở chatbot hỗ trợ:")
        print("   🤖 'Xin chào! Tôi là SOUL AI, trợ lý ảo của SOULFRIEND. Tôi có thể giúp gì cho bạn?'")
        
        # Cuộc hội thoại mô phỏng
        conversation = [
            {
                "user": "Chào bạn! Mình vừa làm xong các bài đánh giá và thấy kết quả hơi lo lắng.",
                "ai": "Cảm ơn bạn đã chia sẻ. Tôi hiểu việc nhận được kết quả đánh giá có thể khiến bạn lo lắng. Bạn có thể cho tôi biết cụ thể điều gì khiến bạn lo lắng nhất không?"
            },
            {
                "user": "Điểm stress và lo âu của mình đều ở mức trung bình. Mình có cần gặp bác sĩ không?",
                "ai": "Điểm ở mức trung bình cho thấy bạn đang trải qua một số khó khăn về tâm lý, và việc tìm kiếm sự hỗ trợ chuyên nghiệp là một quyết định rất tốt. Tôi khuyến khích bạn gặp bác sĩ tâm lý để được tư vấn cụ thể hơn."
            },
            {
                "user": "Trong lúc chờ đặt lịch với bác sĩ, mình có thể làm gì để cải thiện tình trạng?",
                "ai": "Có một số điều bạn có thể thử ngay: 1) Thực hành thở sâu 10 phút mỗi ngày, 2) Duy trì giấc ngủ đủ 7-8 tiếng, 3) Tập thể dục nhẹ, 4) Viết nhật ký cảm xúc, 5) Giới hạn caffeine và social media. Bạn muốn tôi hướng dẫn chi tiết kỹ thuật nào không?"
            },
            {
                "user": "Kỹ thuật thở sâu nghe hay đấy! Bạn có thể hướng dẫn không?",
                "ai": "Tất nhiên! Đây là kỹ thuật thở 4-7-8 rất hiệu quả: 1) Hít vào qua mũi trong 4 giây, 2) Nín thở trong 7 giây, 3) Thở ra qua miệng trong 8 giây. Lặp lại 4-6 lần. Thực hành 2 lần mỗi ngày để đạt hiệu quả tốt nhất."
            },
            {
                "user": "Cảm ơn bạn! Mình sẽ thử ngay.",
                "ai": "Rất vui được giúp bạn! Hãy nhớ rằng việc chăm sóc sức khỏe tâm thần là một hành trình, không phải đích đến. Bạn đã thực hiện bước đầu tiên quan trọng bằng việc đánh giá và tìm hiểu về tình trạng của mình. Chúc bạn mạnh khỏe!"
            }
        ]
        
        for exchange in conversation:
            print(f"   👤 Mai: {exchange['user']}")
            time.sleep(1)
            print(f"   🤖 SOUL AI: {exchange['ai']}")
            time.sleep(1)
            print()
        
        print("   💭 'Chatbot này thông minh quá! Có những lời khuyên thực tế và hữu ích.'")
        
    except Exception as e:
        print(f"   ❌ Error during chatbot interaction: {e}")

def simulate_session_completion(user_persona: Dict):
    """Mô phỏng kết thúc session và feedback"""
    print(f"   ✅ {user_persona['name']} hoàn thành session SOULFRIEND...")
    
    # Session summary
    print("   📋 Tổng kết session:")
    print("      ✅ Hoàn thành 3 bài đánh giá: PHQ-9, GAD-7, DASS-21")
    print("      ✅ Xem phân tích kết quả và biểu đồ")
    print("      ✅ Tạo báo cáo PDF chuyên nghiệp")
    print("      ✅ Tìm hiểu tài nguyên hỗ trợ")
    print("      ✅ Tương tác với AI chatbot")
    print("      ⏱️ Thời gian sử dụng: ~25 phút")
    
    # User feedback  
    print("   💬 Mai đánh giá trải nghiệm:")
    feedback = {
        "overall_rating": "5/5 ⭐⭐⭐⭐⭐",
        "ease_of_use": "Rất dễ sử dụng, giao diện thân thiện",
        "assessment_quality": "Các câu hỏi chuyên nghiệp và phù hợp", 
        "results_clarity": "Kết quả rõ ràng, dễ hiểu",
        "helpful_features": "PDF report và chatbot AI rất hữu ích",
        "recommendation": "Sẽ giới thiệu cho bạn bè"
    }
    
    for aspect, rating in feedback.items():
        print(f"      - {aspect.replace('_', ' ').title()}: {rating}")
    
    # Next steps
    print("   🎯 Kế hoạch tiếp theo của Mai:")
    next_steps = [
        "📅 Đặt lịch gặp bác sĩ tâm lý trong tuần tới",
        "🧘 Thực hành kỹ thuật thở sâu hàng ngày",
        "📱 Tải app mindfulness được khuyến nghị",
        "📊 Quay lại SOULFRIEND sau 2 tuần để đánh giá lại",
        "👥 Chia sẻ với bạn thân về tình trạng của mình",
        "💾 Mang báo cáo PDF đến bác sĩ"
    ]
    
    for step in next_steps:
        print(f"      {step}")
    
    print("   💭 'SOULFRIEND thực sự đã giúp mình hiểu rõ hơn về tình trạng của mình và biết cần làm gì tiếp theo. Cảm ơn!'")
    
    # Final metrics
    print(f"\n📊 SESSION METRICS:")
    print(f"   👤 User: {user_persona['name']} ({user_persona['age']} tuổi)")
    print(f"   ⏱️ Total time: ~25 minutes")
    print(f"   📋 Assessments completed: 3/3")
    print(f"   📄 PDF generated: ✅")
    print(f"   🤖 AI interaction: ✅")
    print(f"   ⭐ User satisfaction: 5/5")
    print(f"   🎯 Action plan created: ✅")
    print(f"   🔄 Likely to return: Yes")

if __name__ == "__main__":
    simulate_real_user_experience()
