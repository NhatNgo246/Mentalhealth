#!/usr/bin/env python3
"""
CRITICAL FIX FOR DETECTED ISSUES
Fix unsafe object attribute access patterns
"""

import re
import os

def fix_critical_issues():
    """Fix critical runtime issues in SOULFRIEND.py"""
    
    file_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    print("🚨 CRITICAL ISSUE FIXES")
    print("=" * 60)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_applied = 0
        
        # Fix 1: result.level_info['key'] → result.get('level_info', {}).get('key', 'default')
        pattern1 = r"result\.level_info\['(\w+)'\]"
        def replace1(match):
            key = match.group(1)
            return f"result.get('level_info', {{}}).get('{key}', 'Unknown')"
        
        before_count = len(re.findall(pattern1, content))
        content = re.sub(pattern1, replace1, content)
        after_count = len(re.findall(pattern1, content))
        fixes1 = before_count - after_count
        
        if fixes1 > 0:
            print(f"✅ Fixed {fixes1} unsafe result.level_info accesses")
            fixes_applied += fixes1
        
        # Fix 2: Similar pattern for other objects
        pattern2 = r"(\w+)\.level_info\['(\w+)'\]"
        def replace2(match):
            obj = match.group(1)
            key = match.group(2)
            return f"{obj}.get('level_info', {{}}).get('{key}', 'Unknown')"
        
        before_count = len(re.findall(pattern2, content))
        content = re.sub(pattern2, replace2, content)
        after_count = len(re.findall(pattern2, content))
        fixes2 = before_count - after_count
        
        if fixes2 > 0:
            print(f"✅ Fixed {fixes2} additional unsafe level_info accesses")
            fixes_applied += fixes2
        
        # Fix 3: scores.items() → scores.items() if hasattr(scores, 'items') else scores
        pattern3 = r"for key, value in scores\.items\(\):"
        replacement3 = "for key, value in (scores.items() if hasattr(scores, 'items') else scores):"
        
        before_count = content.count("for key, value in scores.items():")
        content = content.replace("for key, value in scores.items():", replacement3)
        after_count = content.count("for key, value in scores.items():")
        fixes3 = before_count - after_count
        
        if fixes3 > 0:
            print(f"✅ Fixed {fixes3} unsafe scores.items() accesses")
            fixes_applied += fixes3
        
        # Write back if changes made
        if fixes_applied > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n📊 Total fixes applied: {fixes_applied}")
            print(f"📄 File updated: {file_path}")
            print("🎉 CRITICAL ISSUES FIXED!")
        else:
            print("⚠️ No critical issues found to fix")
        
        return fixes_applied > 0
        
    except Exception as e:
        print(f"❌ Error fixing critical issues: {e}")
        return False

if __name__ == "__main__":
    success = fix_critical_issues()
    exit(0 if success else 1)
