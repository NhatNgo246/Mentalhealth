#!/usr/bin/env python3
"""
Test để kiểm tra các lỗi AttributeError đã được sửa
"""

import sys
import os
sys.path.append('/workspaces/Mentalhealth')

def test_soulfriend_syntax():
    print("🔧 KIỂM TRA CÚ PHÁP SOULFRIEND.PY")
    print("=" * 40)
    
    try:
        # Compile file để kiểm tra syntax errors
        with open('/workspaces/Mentalhealth/SOULFRIEND.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, '/workspaces/Mentalhealth/SOULFRIEND.py', 'exec')
        print("✅ Syntax OK - Không có lỗi cú pháp")
        
        # Kiểm tra các pattern có thể gây lỗi
        dangerous_patterns = [
            'result.level_info',
            '.level_info)',
            'hasattr(result.level_info'
        ]
        
        found_issues = []
        for pattern in dangerous_patterns:
            if pattern in code:
                found_issues.append(pattern)
        
        if found_issues:
            print("⚠️ Tìm thấy patterns có thể gây lỗi:")
            for issue in found_issues:
                print(f"   - {issue}")
        else:
            print("✅ Không tìm thấy patterns nguy hiểm")
            
        # Đếm số lần sử dụng an toàn
        safe_usage = code.count('result.get(')
        print(f"✅ Safe dict access patterns: {safe_usage}")
        
        return len(found_issues) == 0
        
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_soulfriend_syntax()
    print(f"\n🎯 RESULT: {'✅ SYNTAX OK' if success else '❌ SYNTAX ISSUES'}")
