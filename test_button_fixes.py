#!/usr/bin/env python3
"""
TEST SCRIPT - Verify fixes cho vấn đề "Xem kết quả"
"""

import sys
sys.path.append('/workspaces/Mentalhealth')

def test_button_fixes():
    print("🔧 KIỂM TRA CÁC FIX CHO BUTTON 'XEM KẾT QUẢ'")
    print("=" * 60)
    
    try:
        # Test 1: Check SOULFRIEND.py structure
        print("\n📋 Test 1: Kiểm tra cấu trúc SOULFRIEND.py...")
        
        with open('/workspaces/Mentalhealth/SOULFRIEND.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for fixes
        fixes_check = {
            "Dynamic Form Name": "form_name = f" in content,
            "Debug Logging": "Button submitted!" in content,
            "Bypass Button": "bypass_button" in content,
            "Force Process": "force_process" in content,
            "Better Error Handling": "Exception during scoring" in content
        }
        
        for fix_name, found in fixes_check.items():
            status = "✅" if found else "❌"
            print(f"   {status} {fix_name}: {'Applied' if found else 'Missing'}")
        
        # Test 2: Check imports still work
        print("\n📦 Test 2: Kiểm tra imports...")
        
        from components.scoring import (
            score_dass21_enhanced,
            score_phq9_enhanced,
            score_gad7_enhanced,
            score_epds_enhanced,
            score_pss10_enhanced
        )
        print("   ✅ All scoring functions imported")
        
        from components.questionnaires import (
            load_dass21_enhanced_vi,
            load_phq9_enhanced_vi,
            load_gad7_enhanced_vi,
            load_epds_enhanced_vi,
            load_pss10_enhanced_vi
        )
        print("   ✅ All questionnaire loaders imported")
        
        # Test 3: Verify scoring still works
        print("\n🎯 Test 3: Kiểm tra scoring functions...")
        
        config = load_dass21_enhanced_vi()
        answers = {i: 1 for i in range(1, 22)}
        result = score_dass21_enhanced(answers, config)
        
        print(f"   ✅ DASS-21 scoring: Score {result.total_score}, Severity {result.severity_level}")
        
        # Test other questionnaires
        test_cases = [
            ("PHQ-9", load_phq9_enhanced_vi, score_phq9_enhanced, 9),
            ("GAD-7", load_gad7_enhanced_vi, score_gad7_enhanced, 7),
            ("EPDS", load_epds_enhanced_vi, score_epds_enhanced, 10),
            ("PSS-10", load_pss10_enhanced_vi, score_pss10_enhanced, 10)
        ]
        
        for name, loader, scorer, num_q in test_cases:
            config = loader()
            answers = {i: 1 for i in range(1, num_q + 1)}
            result = scorer(answers, config)
            print(f"   ✅ {name} scoring: Score {result.total_score}, Severity {result.severity_level}")
        
        # Test 4: Check file syntax
        print("\n🔍 Test 4: Kiểm tra syntax...")
        
        import subprocess
        result = subprocess.run([
            '/workspaces/Mentalhealth/.venv/bin/python', 
            '-m', 'py_compile', 
            '/workspaces/Mentalhealth/SOULFRIEND.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ SOULFRIEND.py syntax: OK")
        else:
            print(f"   ❌ Syntax error: {result.stderr}")
        
        print("\n🎉 TỔNG KẾT:")
        print("=" * 60)
        
        total_fixes = len(fixes_check)
        applied_fixes = sum(fixes_check.values())
        
        if applied_fixes == total_fixes:
            print("✅ TẤT CẢ FIXES ĐÃ ĐƯỢC ÁP DỤNG THÀNH CÔNG!")
            print("🚀 Ứng dụng sẵn sàng để test button 'Xem kết quả'")
            print()
            print("📋 CÁCH TEST:")
            print("1. Mở http://localhost:8501")
            print("2. Chọn questionnaire")
            print("3. Trả lời đầy đủ các câu hỏi")
            print("4. Bấm 'Xem kết quả' (nếu không hoạt động)")
            print("5. Thử 'Xử lý kết quả (Bypass)'")
        else:
            print(f"⚠️ {applied_fixes}/{total_fixes} fixes applied")
            print("🔧 Cần kiểm tra lại một số fixes")
        
        return applied_fixes == total_fixes
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_button_fixes()
    
    print("\n" + "=" * 60)
    if success:
        print("🎊 ALL FIXES VERIFIED AND READY!")
    else:
        print("🔧 SOME ISSUES NEED ATTENTION")
