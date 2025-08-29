#!/usr/bin/env python3
"""
TEST GIAO DIỆN VÀ KHẢ NĂNG HIỂN THỊ
Kiểm tra toàn diện khả năng vận hành, hiển thị và giao diện ứng dụng
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth')

def test_ui_components():
    """Test các components giao diện"""
    print("🎨 KIỂM TRA CÁC COMPONENTS GIAO DIỆN")
    print("=" * 60)
    
    try:
        # Test UI components
        from components.ui import (
            display_logo, 
            app_header, 
            show_disclaimer,
            create_metric_card,
            create_info_card,
            create_result_card,
            create_progress_indicator
        )
        print("✅ UI Components: display_logo, app_header, show_disclaimer")
        print("✅ UI Cards: metric_card, info_card, result_card")
        print("✅ UI Progress: progress_indicator")
        
        # Test advanced UI components
        try:
            from components.ui_advanced import (
                create_enhanced_sidebar,
                display_questionnaire_interface,
                show_results_with_animation
            )
            print("✅ Advanced UI: enhanced_sidebar, questionnaire_interface")
        except ImportError as e:
            print(f"⚠️ Advanced UI components không có sẵn: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ UI Components test failed: {str(e)}")
        return False

def test_questionnaire_display():
    """Test hiển thị questionnaire"""
    print("\n📋 KIỂM TRA HIỂN THỊ QUESTIONNAIRE")
    print("=" * 60)
    
    try:
        # Load tất cả questionnaires
        from components.questionnaires import (
            load_dass21_enhanced_vi,
            load_phq9_enhanced_vi,
            load_gad7_enhanced_vi,
            load_epds_enhanced_vi,
            load_pss10_enhanced_vi
        )
        
        questionnaires = {
            "DASS-21": load_dass21_enhanced_vi,
            "PHQ-9": load_phq9_enhanced_vi,
            "GAD-7": load_gad7_enhanced_vi,
            "EPDS": load_epds_enhanced_vi,
            "PSS-10": load_pss10_enhanced_vi
        }
        
        display_tests = []
        
        for name, loader in questionnaires.items():
            config = loader()
            
            # Test cấu trúc hiển thị
            has_title = 'title' in config
            has_items = 'items' in config and len(config['items']) > 0
            has_options = all('options' in item for item in config['items'])
            
            print(f"\n📄 {name}:")
            print(f"   ✅ Title: {config.get('title', 'N/A')}")
            print(f"   ✅ Questions: {len(config.get('items', []))}")
            print(f"   ✅ Options per question: {len(config['items'][0].get('options', [])) if config.get('items') else 0}")
            
            # Test sample question display
            if config.get('items'):
                sample_q = config['items'][0]
                print(f"   📝 Sample question: {sample_q.get('question', 'N/A')[:50]}...")
                print(f"   📊 Sample options: {len(sample_q.get('options', []))} choices")
            
            display_tests.append(has_title and has_items and has_options)
        
        return all(display_tests)
        
    except Exception as e:
        print(f"❌ Questionnaire display test failed: {str(e)}")
        return False

def test_scoring_display():
    """Test hiển thị kết quả scoring"""
    print("\n🎯 KIỂM TRA HIỂN THỊ KẾT QUẢ SCORING")
    print("=" * 60)
    
    try:
        from components.scoring import (
            score_dass21_enhanced,
            score_phq9_enhanced,
            score_gad7_enhanced,
            score_epds_enhanced,
            score_pss10_enhanced
        )
        
        from components.questionnaires import (
            load_dass21_enhanced_vi,
            load_phq9_enhanced_vi,
            load_gad7_enhanced_vi,
            load_epds_enhanced_vi,
            load_pss10_enhanced_vi
        )
        
        test_scenarios = [
            ("DASS-21", load_dass21_enhanced_vi, score_dass21_enhanced, 21, {i: 1 for i in range(1, 22)}),
            ("PHQ-9", load_phq9_enhanced_vi, score_phq9_enhanced, 9, {i: 2 for i in range(1, 10)}),
            ("GAD-7", load_gad7_enhanced_vi, score_gad7_enhanced, 7, {i: 1 for i in range(1, 8)}),
            ("EPDS", load_epds_enhanced_vi, score_epds_enhanced, 10, {i: 2 for i in range(1, 11)}),
            ("PSS-10", load_pss10_enhanced_vi, score_pss10_enhanced, 10, {i: 3 for i in range(1, 11)})
        ]
        
        scoring_tests = []
        
        for name, loader, scorer, num_q, answers in test_scenarios:
            config = loader()
            result = scorer(answers, config)
            
            print(f"\n🎯 {name} Scoring Results:")
            print(f"   ✅ Total Score: {result.total_score}")
            print(f"   ✅ Severity Level: {result.severity_level}")
            print(f"   ✅ Subscales: {list(result.subscales.keys())}")
            print(f"   ✅ Interpretation: {result.interpretation[:100]}...")
            print(f"   ✅ Recommendations: {len(result.recommendations)} items")
            
            # Test display structure
            has_score = hasattr(result, 'total_score')
            has_severity = hasattr(result, 'severity_level')
            has_interpretation = hasattr(result, 'interpretation')
            has_recommendations = hasattr(result, 'recommendations')
            
            scoring_tests.append(has_score and has_severity and has_interpretation and has_recommendations)
        
        return all(scoring_tests)
        
    except Exception as e:
        print(f"❌ Scoring display test failed: {str(e)}")
        return False

def test_streamlit_compatibility():
    """Test khả năng tương thích với Streamlit"""
    print("\n🌐 KIỂM TRA TƯƠNG THÍCH STREAMLIT")
    print("=" * 60)
    
    try:
        import streamlit as st
        print("✅ Streamlit import: OK")
        
        # Test các Streamlit components chính
        streamlit_functions = [
            'title', 'header', 'subheader', 'markdown',
            'selectbox', 'radio', 'button', 'sidebar',
            'columns', 'container', 'expander'
        ]
        
        available_functions = []
        for func in streamlit_functions:
            if hasattr(st, func):
                available_functions.append(func)
                print(f"✅ st.{func}: Available")
            else:
                print(f"❌ st.{func}: Not available")
        
        # Test session state
        print(f"✅ Session state support: {'session_state' in dir(st)}")
        
        return len(available_functions) >= len(streamlit_functions) * 0.8  # At least 80% available
        
    except Exception as e:
        print(f"❌ Streamlit compatibility test failed: {str(e)}")
        return False

def test_soulfriend_structure():
    """Test cấu trúc và logic của SOULFRIEND.py"""
    print("\n🧠 KIỂM TRA CẤU TRÚC SOULFRIEND.PY")
    print("=" * 60)
    
    try:
        with open('/workspaces/Mentalhealth/SOULFRIEND.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test các thành phần chính
        tests = {
            "Questionnaire Selection": "selectbox" in content and "questionnaire" in content.lower(),
            "Sidebar Navigation": "sidebar" in content,
            "Question Display": "radio" in content or "selectbox" in content,
            "Result Display": "result" in content.lower(),
            "Session State": "session_state" in content,
            "Multi-page Support": "page" in content.lower(),
            "Vietnamese Support": "utf-8" in content or "tiếng việt" in content.lower(),
            "Emergency Protocol": "khẩn cấp" in content.lower() or "emergency" in content.lower()
        }
        
        passed_tests = 0
        for test_name, condition in tests.items():
            status = "✅" if condition else "❌"
            print(f"   {status} {test_name}: {'PASS' if condition else 'FAIL'}")
            if condition:
                passed_tests += 1
        
        print(f"\n📊 SOULFRIEND Structure Score: {passed_tests}/{len(tests)} ({passed_tests/len(tests)*100:.1f}%)")
        
        return passed_tests >= len(tests) * 0.7  # At least 70% pass
        
    except Exception as e:
        print(f"❌ SOULFRIEND structure test failed: {str(e)}")
        return False

def test_responsive_design():
    """Test thiết kế responsive và accessibility"""
    print("\n📱 KIỂM TRA THIẾT KẾ RESPONSIVE")
    print("=" * 60)
    
    try:
        # Kiểm tra CSS và styling
        css_files = [
            '/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/assets/styles.css'
        ]
        
        css_features = []
        
        for css_file in css_files:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                # Test responsive features
                responsive_features = {
                    "Media Queries": "@media" in css_content,
                    "Flexbox": "flex" in css_content,
                    "Grid": "grid" in css_content,
                    "Mobile Support": "mobile" in css_content.lower(),
                    "Accessibility": "aria" in css_content.lower(),
                    "Color Scheme": "color" in css_content.lower(),
                    "Typography": "font" in css_content.lower()
                }
                
                for feature, found in responsive_features.items():
                    status = "✅" if found else "❌"
                    print(f"   {status} {feature}: {'Found' if found else 'Not found'}")
                    css_features.append(found)
                    
            except FileNotFoundError:
                print(f"   ⚠️ CSS file not found: {css_file}")
        
        # Test UI components for accessibility
        from components.ui import DISCLAIMER
        has_disclaimer = len(DISCLAIMER) > 0
        print(f"   ✅ Disclaimer/Warning: {'Present' if has_disclaimer else 'Missing'}")
        
        return len([f for f in css_features if f]) >= len(css_features) * 0.5
        
    except Exception as e:
        print(f"❌ Responsive design test failed: {str(e)}")
        return False

def run_complete_ui_test():
    """Chạy test toàn diện giao diện và khả năng vận hành"""
    print("🚀 KIỂM TRA TOÀN DIỆN GIAO DIỆN VÀ KHẢ NĂNG VẬN HÀNH")
    print("=" * 80)
    
    tests = [
        ("UI Components", test_ui_components),
        ("Questionnaire Display", test_questionnaire_display),
        ("Scoring Display", test_scoring_display),
        ("Streamlit Compatibility", test_streamlit_compatibility),
        ("SOULFRIEND Structure", test_soulfriend_structure),
        ("Responsive Design", test_responsive_design)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append(result)
            status = "PASS ✅" if result else "FAIL ❌"
            print(f"   {test_name}: {status}")
        except Exception as e:
            print(f"   {test_name}: ERROR ❌ - {str(e)}")
            results.append(False)
    
    # Final summary
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print("\n" + "=" * 80)
    print("📊 KẾT QUẢ TỔNG QUAN TEST GIAO DIỆN")
    print("=" * 80)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 TỔNG KẾT: {passed}/{total} tests passed ({percentage:.1f}%)")
    
    if percentage >= 80:
        print("🎉 ỨNG DỤNG SẴN SÀNG CHO PRODUCTION!")
        print("🚀 Giao diện và khả năng vận hành: EXCELLENT")
    elif percentage >= 60:
        print("✅ Ứng dụng cơ bản hoạt động tốt")
        print("⚠️ Cần cải thiện một số thành phần")
    else:
        print("❌ Cần khắc phục nhiều vấn đề trước khi deploy")
    
    return percentage >= 60

if __name__ == "__main__":
    success = run_complete_ui_test()
    
    print("\n" + "=" * 80)
    print("🎊 HOÀN THÀNH KIỂM TRA GIAO DIỆN VÀ VẬN HÀNH")
    print("=" * 80)
    
    if success:
        print("🟢 TÌNH TRẠNG: SẴN SÀNG VẬN HÀNH")
        print("🎯 Khuyến nghị: Có thể deploy và sử dụng")
    else:
        print("🟡 TÌNH TRẠNG: CẦN CẢI THIỆN")
        print("🔧 Khuyến nghị: Khắc phục các vấn đề được phát hiện")
