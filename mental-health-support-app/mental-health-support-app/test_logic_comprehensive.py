"""
Test script để kiểm tra logic ứng dụng Mental Health Support
Đảm bảo tính chính xác và an toàn của ứng dụng
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app')

from components.questionnaires import load_dass21_vi
from components.scoring import score_dass21

def test_questionnaire_loading():
    """Test việc load questionnaire"""
    print("🔍 Testing questionnaire loading...")
    
    try:
        cfg = load_dass21_vi()
        
        # Kiểm tra cấu trúc cơ bản
        assert "items" in cfg, "Missing 'items' in config"
        assert "options" in cfg, "Missing 'options' in config"
        assert "severity_thresholds" in cfg, "Missing 'severity_thresholds' in config"
        
        # Kiểm tra số lượng câu hỏi
        assert len(cfg["items"]) == 21, f"Expected 21 items, got {len(cfg['items'])}"
        
        # Kiểm tra options
        assert len(cfg["options"]) == 4, f"Expected 4 options, got {len(cfg['options'])}"
        
        # Kiểm tra từng item có đủ field
        for i, item in enumerate(cfg["items"]):
            assert "id" in item, f"Item {i} missing 'id'"
            assert "text" in item, f"Item {i} missing 'text'"
            assert "subscale" in item, f"Item {i} missing 'subscale'"
            assert item["subscale"] in ["Depression", "Anxiety", "Stress"], f"Invalid subscale: {item['subscale']}"
        
        # Kiểm tra severity thresholds
        for subscale in ["Depression", "Anxiety", "Stress"]:
            assert subscale in cfg["severity_thresholds"], f"Missing thresholds for {subscale}"
            thresholds = cfg["severity_thresholds"][subscale]
            expected_levels = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
            for level in expected_levels:
                assert level in thresholds, f"Missing {level} threshold for {subscale}"
                assert len(thresholds[level]) == 2, f"Threshold {level} should have 2 values"
        
        print("✅ Questionnaire loading test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Questionnaire loading test FAILED: {e}")
        return False

def test_scoring_logic():
    """Test logic tính điểm"""
    print("🔍 Testing scoring logic...")
    
    try:
        cfg = load_dass21_vi()
        
        # Test case 1: Tất cả câu trả lời = 0 (Normal)
        answers_normal = {item["id"]: 0 for item in cfg["items"]}
        scores_normal = score_dass21(answers_normal, cfg)
        
        for subscale in ["Depression", "Anxiety", "Stress"]:
            assert subscale in scores_normal, f"Missing {subscale} in scores"
            score_obj = scores_normal[subscale]
            assert score_obj.raw == 0, f"{subscale} raw score should be 0"
            assert score_obj.adjusted == 0, f"{subscale} adjusted score should be 0"
            assert score_obj.severity == "Normal", f"{subscale} severity should be Normal"
        
        # Test case 2: Tất cả câu trả lời = 3 (Extremely Severe)
        answers_severe = {item["id"]: 3 for item in cfg["items"]}
        scores_severe = score_dass21(answers_severe, cfg)
        
        for subscale in ["Depression", "Anxiety", "Stress"]:
            score_obj = scores_severe[subscale]
            assert score_obj.severity == "Extremely Severe", f"{subscale} should be Extremely Severe with max scores"
        
        # Test case 3: Test mixed scores
        answers_mixed = {}
        for i, item in enumerate(cfg["items"]):
            answers_mixed[item["id"]] = i % 4  # 0,1,2,3,0,1,2,3...
        
        scores_mixed = score_dass21(answers_mixed, cfg)
        for subscale in ["Depression", "Anxiety", "Stress"]:
            score_obj = scores_mixed[subscale]
            assert hasattr(score_obj, 'raw'), f"{subscale} missing raw score"
            assert hasattr(score_obj, 'adjusted'), f"{subscale} missing adjusted score"
            assert hasattr(score_obj, 'severity'), f"{subscale} missing severity"
            assert score_obj.adjusted == score_obj.raw * 2, f"{subscale} adjusted calculation error"
        
        print("✅ Scoring logic test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Scoring logic test FAILED: {e}")
        return False

def test_severity_classification():
    """Test phân loại mức độ nghiêm trọng"""
    print("🔍 Testing severity classification...")
    
    try:
        cfg = load_dass21_vi()
        
        # Test các boundary values
        test_cases = [
            # Depression boundaries
            ({"Depression": [(0, "Normal"), (9, "Normal"), (10, "Mild"), (13, "Mild"), 
                           (14, "Moderate"), (20, "Moderate"), (21, "Severe"), (27, "Severe"),
                           (28, "Extremely Severe"), (42, "Extremely Severe")]}),
            # Anxiety boundaries  
            ({"Anxiety": [(0, "Normal"), (7, "Normal"), (8, "Mild"), (9, "Mild"),
                        (10, "Moderate"), (14, "Moderate"), (15, "Severe"), (19, "Severe"), 
                        (20, "Extremely Severe"), (42, "Extremely Severe")]}),
            # Stress boundaries
            ({"Stress": [(0, "Normal"), (14, "Normal"), (15, "Mild"), (18, "Mild"),
                       (19, "Moderate"), (25, "Moderate"), (26, "Severe"), (33, "Severe"),
                       (34, "Extremely Severe"), (42, "Extremely Severe")]})
        ]
        
        from components.scoring import severity_from_thresholds, load_thresholds
        
        for test_group in test_cases:
            for subscale, test_points in test_group.items():
                thresholds = load_thresholds(cfg, subscale)
                for adjusted_score, expected_severity in test_points:
                    actual_severity = severity_from_thresholds(adjusted_score, thresholds)
                    assert actual_severity == expected_severity, \
                        f"{subscale} score {adjusted_score}: expected {expected_severity}, got {actual_severity}"
        
        print("✅ Severity classification test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Severity classification test FAILED: {e}")
        return False

def test_data_integrity():
    """Test tính toàn vẹn dữ liệu"""
    print("🔍 Testing data integrity...")
    
    try:
        cfg = load_dass21_vi()
        
        # Kiểm tra distribution of items across subscales
        subscale_counts = {"Depression": 0, "Anxiety": 0, "Stress": 0}
        for item in cfg["items"]:
            subscale_counts[item["subscale"]] += 1
        
        # DASS-21 should have 7 items per subscale
        for subscale, count in subscale_counts.items():
            assert count == 7, f"{subscale} should have 7 items, got {count}"
        
        # Kiểm tra item IDs are unique
        item_ids = [item["id"] for item in cfg["items"]]
        assert len(item_ids) == len(set(item_ids)), "Duplicate item IDs found"
        
        # Kiểm tra option values
        option_values = [opt["value"] for opt in cfg["options"]]
        expected_values = [0, 1, 2, 3]
        assert option_values == expected_values, f"Option values should be {expected_values}"
        
        print("✅ Data integrity test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Data integrity test FAILED: {e}")
        return False

def run_comprehensive_test():
    """Chạy tất cả tests"""
    print("🚀 Starting comprehensive Mental Health App testing...")
    print("=" * 60)
    
    tests = [
        test_questionnaire_loading,
        test_scoring_logic, 
        test_severity_classification,
        test_data_integrity
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Application logic is SAFE and RELIABLE")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - Please fix issues before deployment")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
