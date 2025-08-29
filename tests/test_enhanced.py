#!/usr/bin/env python3
"""
🧪 ENHANCED SOULFRIEND TESTING
==============================
Test specific enhanced features and functions

Created: August 27, 2025
Purpose: Validate enhanced DASS-21 functionality
"""

import sys
import os
import json
import importlib.util
import traceback

def test_enhanced_questionnaire():
    """Test enhanced questionnaire loading"""
    print("🧪 Testing Enhanced Questionnaire Loading...")
    print("-" * 45)
    
    try:
        # Add components to path
        sys.path.append('/workspaces/Mentalhealth')
        
        from components.questionnaires import load_dass21_enhanced_vi
        
        # Test loading enhanced questionnaire
        cfg = load_dass21_enhanced_vi()
        
        if cfg:
            print("✅ Enhanced questionnaire loaded successfully")
            print(f"✅ Scale: {cfg.get('scale', 'Unknown')}")
            print(f"✅ Version: {cfg.get('version', 'Unknown')}")
            print(f"✅ Questions count: {len(cfg.get('items', []))}")
            print(f"✅ Options count: {len(cfg.get('options', []))}")
            
            # Test structure
            required_keys = ['scale', 'version', 'options', 'items', 'scoring', 'recommendations']
            for key in required_keys:
                if key in cfg:
                    print(f"✅ Has {key}")
                else:
                    print(f"❌ Missing {key}")
                    
            # Test enhanced features
            if 'instructions' in cfg:
                print("✅ Has enhanced instructions")
            
            if 'emergency_contacts' in cfg:
                print("✅ Has emergency contacts")
                
            if 'metadata' in cfg:
                print("✅ Has metadata")
                
            return True
        else:
            print("❌ Failed to load enhanced questionnaire")
            return False
            
    except Exception as e:
        print(f"❌ Error testing enhanced questionnaire: {e}")
        traceback.print_exc()
        return False

def test_enhanced_scoring():
    """Test enhanced scoring function"""
    print("\n🧪 Testing Enhanced Scoring...")
    print("-" * 35)
    
    try:
        from components.questionnaires import load_dass21_enhanced_vi
        from components.scoring import score_dass21_enhanced
        
        # Load config
        cfg = load_dass21_enhanced_vi()
        if not cfg:
            print("❌ Cannot load config for scoring test")
            return False
        
        # Test with sample answers
        sample_answers = {}
        for item in cfg['items']:
            sample_answers[item['id']] = 1  # All answers = 1 (mild responses)
        
        print(f"✅ Created sample answers for {len(sample_answers)} questions")
        
        # Test enhanced scoring
        result = score_dass21_enhanced(sample_answers, cfg)
        
        if result:
            print("✅ Enhanced scoring completed successfully")
            print(f"✅ Total score: {result.total_score}")
            print(f"✅ Interpretation: {result.interpretation}")
            print(f"✅ Severity level: {result.severity_level}")
            print(f"✅ Has recommendations: {'title' in result.recommendations}")
            
            # Test subscales
            for subscale, score_obj in result.subscales.items():
                print(f"✅ {subscale}: {score_obj.raw} → {score_obj.adjusted} ({score_obj.severity})")
                
            return True
        else:
            print("❌ Enhanced scoring failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing enhanced scoring: {e}")
        traceback.print_exc()
        return False

def test_enhanced_data_structure():
    """Test enhanced data file structure"""
    print("\n🧪 Testing Enhanced Data Structure...")
    print("-" * 40)
    
    try:
        # Test enhanced data file
        enhanced_path = "/workspaces/Mentalhealth/data/dass21_enhanced_vi.json"
        
        if os.path.exists(enhanced_path):
            print("✅ Enhanced data file exists")
            
            with open(enhanced_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Test enhanced structure
            enhanced_features = [
                'version',
                'description', 
                'instructions',
                'recommendations',
                'emergency_contacts',
                'metadata'
            ]
            
            for feature in enhanced_features:
                if feature in data:
                    print(f"✅ Has {feature}")
                else:
                    print(f"❌ Missing {feature}")
            
            # Test enhanced options
            if 'options' in data:
                for i, option in enumerate(data['options']):
                    required_option_keys = ['value', 'label', 'description', 'emoji']
                    missing_keys = [key for key in required_option_keys if key not in option]
                    if missing_keys:
                        print(f"⚠️ Option {i} missing: {missing_keys}")
                    else:
                        print(f"✅ Option {i} complete")
            
            # Test enhanced items
            if 'items' in data:
                for i, item in enumerate(data['items'][:3]):  # Test first 3
                    enhanced_item_keys = ['vietnamese_context', 'category']
                    for key in enhanced_item_keys:
                        if key in item:
                            print(f"✅ Item {i+1} has {key}")
                        else:
                            print(f"❌ Item {i+1} missing {key}")
            
            return True
        else:
            print("❌ Enhanced data file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing enhanced data: {e}")
        traceback.print_exc()
        return False

def test_app_syntax():
    """Test main app syntax"""
    print("\n🧪 Testing Main App Syntax...")
    print("-" * 35)
    
    try:
        app_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
        
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Test compilation
        compile(content, app_path, 'exec')
        print("✅ Main app syntax is valid")
        
        # Test enhanced imports
        enhanced_imports = [
            'load_dass21_enhanced_vi',
            'score_dass21_enhanced'
        ]
        
        for imp in enhanced_imports:
            if imp in content:
                print(f"✅ Has {imp} import")
            else:
                print(f"❌ Missing {imp} import")
        
        # Test enhanced features in code
        enhanced_features = [
            'enhanced_scores',
            'enhanced_result',
            'dass21_enhanced',
            'vietnamese_context'
        ]
        
        for feature in enhanced_features:
            if feature in content:
                print(f"✅ Uses {feature}")
            else:
                print(f"⚠️ May not use {feature}")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in main app: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing app syntax: {e}")
        return False

def run_complete_enhanced_test():
    """Run all enhanced tests"""
    print("🚀 ENHANCED SOULFRIEND TESTING SUITE")
    print("=" * 50)
    
    tests = [
        ("Enhanced Questionnaire", test_enhanced_questionnaire),
        ("Enhanced Scoring", test_enhanced_scoring),
        ("Enhanced Data Structure", test_enhanced_data_structure),
        ("App Syntax", test_app_syntax)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ENHANCED TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    print(f"\n📈 Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎉 ALL ENHANCED TESTS PASSED!")
        print("✨ SOULFRIEND Enhanced Features Ready!")
    elif success_rate >= 75:
        print("👍 Most Enhanced Tests Passed!")
        print("🔧 Minor fixes needed")
    else:
        print("⚠️ Enhanced Features Need Work!")
        print("🔧 Major fixes required")
    
    return success_rate

if __name__ == "__main__":
    run_complete_enhanced_test()
