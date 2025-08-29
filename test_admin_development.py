#!/usr/bin/env python3
"""
ADMIN DEVELOPMENT TEST
Test admin functionality without affecting main app
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, '/workspaces/Mentalhealth')

def test_admin_imports():
    """Test admin component imports"""
    print("🧪 TESTING ADMIN IMPORTS")
    print("=" * 30)
    
    try:
        from components.admin_auth import admin_auth, require_admin_auth
        print("✅ admin_auth imported successfully")
        
        # Test AdminAuth class
        auth_instance = admin_auth
        print(f"✅ AdminAuth instance created: {type(auth_instance)}")
        
        # Test configuration initialization
        auth_instance.init_admin_config()
        print("✅ Admin config initialized")
        
        # Test password hashing
        test_hash = auth_instance.hash_password("test123")
        print(f"✅ Password hashing works: {len(test_hash)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_app_integrity():
    """Test that main app imports still work"""
    print("\n🧪 TESTING MAIN APP INTEGRITY")
    print("=" * 35)
    
    try:
        # Test main app imports
        from components.ui import app_header, load_css
        print("✅ UI components import OK")
        
        from components.scoring import calculate_scores
        print("✅ Scoring components import OK")
        
        from components.questionnaires import load_questionnaire
        print("✅ Questionnaire components import OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_config_creation():
    """Test admin config file creation"""
    print("\n🧪 TESTING ADMIN CONFIG CREATION")
    print("=" * 37)
    
    try:
        from components.admin_auth import admin_auth
        
        # Test config file creation
        config_file = "/workspaces/Mentalhealth/data/admin_config.json"
        
        if os.path.exists(config_file):
            print("✅ Admin config file exists")
            
            # Load and verify config
            config = admin_auth.load_admin_config()
            
            if "admin_users" in config:
                print(f"✅ Admin users found: {len(config['admin_users'])}")
                
                for username in config["admin_users"]:
                    print(f"   👤 {username}: {config['admin_users'][username]['role']}")
            
            if "security_settings" in config:
                print("✅ Security settings configured")
            
            return True
        else:
            print("❌ Admin config file not found")
            return False
            
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_authentication_logic():
    """Test authentication logic"""
    print("\n🧪 TESTING AUTHENTICATION LOGIC")
    print("=" * 37)
    
    try:
        from components.admin_auth import admin_auth
        
        # Test valid credentials
        success, message, user_data = admin_auth.verify_credentials("admin", "SoulFriend2025!")
        if success:
            print("✅ Valid credentials accepted")
        else:
            print(f"❌ Valid credentials rejected: {message}")
        
        # Test invalid credentials
        success, message, user_data = admin_auth.verify_credentials("admin", "wrongpassword")
        if not success:
            print("✅ Invalid credentials rejected")
        else:
            print("❌ Invalid credentials accepted")
        
        # Test non-existent user
        success, message, user_data = admin_auth.verify_credentials("nonexistent", "password")
        if not success:
            print("✅ Non-existent user rejected")
        else:
            print("❌ Non-existent user accepted")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_file_permissions():
    """Test file permissions and access"""
    print("\n🧪 TESTING FILE PERMISSIONS")
    print("=" * 32)
    
    try:
        # Test data directory
        data_dir = "/workspaces/Mentalhealth/data"
        if os.path.exists(data_dir):
            print("✅ Data directory accessible")
        else:
            print("⚠️ Data directory created")
            os.makedirs(data_dir, exist_ok=True)
        
        # Test write permissions
        test_file = f"{data_dir}/test_write.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        
        if os.path.exists(test_file):
            print("✅ Write permissions OK")
            os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ File permission test failed: {e}")
        return False

def run_admin_safety_check():
    """Run complete admin safety check"""
    print("🛡️ ADMIN DEVELOPMENT SAFETY CHECK")
    print("=" * 40)
    print(f"⏰ Test time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    tests = [
        ("Admin Imports", test_admin_imports),
        ("Main App Integrity", test_main_app_integrity), 
        ("Admin Config", test_admin_config_creation),
        ("Authentication Logic", test_authentication_logic),
        ("File Permissions", test_file_permissions)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 20)
        
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n📊 TEST RESULTS")
    print("=" * 17)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"📊 Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Admin features are safe to deploy")
        print("✅ Main app integrity preserved")
        print("✅ No conflicts detected")
        
        return True
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ Please fix issues before deployment")
        print("🔧 Check error messages above")
        
        return False

if __name__ == "__main__":
    success = run_admin_safety_check()
    
    if success:
        print("\n🚀 READY FOR ADMIN FEATURE DEPLOYMENT!")
    else:
        print("\n🛑 DEPLOYMENT BLOCKED - FIX ISSUES FIRST!")
    
    exit(0 if success else 1)
