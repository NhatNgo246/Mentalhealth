#!/usr/bin/env python3
"""
CRITICAL RUNTIME FIX FOR SOULFRIEND.PY
Fixes all 'result.' object access issues to dict access
"""

import re
import os

def fix_soulfriend_runtime_errors():
    """Fix all runtime errors in SOULFRIEND.py"""
    
    file_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    print("🚨 CRITICAL RUNTIME FIX - SOULFRIEND.PY")
    print("=" * 60)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix all result.attribute access to result.get() or enhanced_result.get()
        fixes = [
            # result.severity → result.get('severity', 'unknown')
            (r'result\.severity', "result.get('severity', 'unknown')"),
            
            # result.adjusted → result.get('score', result.get('adjusted', 0))
            (r'result\.adjusted', "result.get('score', result.get('adjusted', 0))"),
            
            # result.raw → result.get('raw', 0)  
            (r'result\.raw', "result.get('raw', 0)"),
            
            # result.score → result.get('score', 0)
            (r'result\.score', "result.get('score', 0)"),
        ]
        
        fixes_applied = 0
        for pattern, replacement in fixes:
            before_count = len(re.findall(pattern, content))
            content = re.sub(pattern, replacement, content)
            after_count = len(re.findall(pattern, content))
            applied = before_count - after_count
            if applied > 0:
                print(f"✅ Fixed {applied} instances of: {pattern}")
                fixes_applied += applied
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n📊 Total fixes applied: {fixes_applied}")
        print(f"📄 File updated: {file_path}")
        
        if fixes_applied > 0:
            print("🎉 RUNTIME ERRORS FIXED!")
        else:
            print("⚠️ No fixes needed")
            
        return fixes_applied > 0
        
    except Exception as e:
        print(f"❌ Error fixing runtime issues: {e}")
        return False

if __name__ == "__main__":
    success = fix_soulfriend_runtime_errors()
    exit(0 if success else 1)
