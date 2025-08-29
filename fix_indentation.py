#!/usr/bin/env python3
"""
Auto-fix all indentation errors in SOULFRIEND.py
"""

import re

def fix_all_indentation_errors():
    """Tự động sửa tất cả lỗi indentation"""
    print("🔧 AUTO-FIXING ALL INDENTATION ERRORS")
    print("=" * 40)
    
    file_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        fixed_lines = []
        fixes_applied = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Tìm dòng có try:
            if re.search(r'^\s+try:\s*$', line):
                try_indent = len(line) - len(line.lstrip())
                fixed_lines.append(line)
                
                # Kiểm tra dòng tiếp theo
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    
                    # Nếu dòng tiếp theo là st.switch_page mà không có indentation đúng
                    if 'st.switch_page' in next_line:
                        next_indent = len(next_line) - len(next_line.lstrip()) if next_line.strip() else 0
                        
                        # Nếu indentation không đúng (phải lớn hơn try)
                        if next_indent <= try_indent:
                            correct_indent = ' ' * (try_indent + 4)
                            fixed_next_line = correct_indent + next_line.strip()
                            fixed_lines.append(fixed_next_line)
                            fixes_applied.append(f"Fixed indentation at line {i+2}: {next_line.strip()}")
                            i += 2
                            continue
                
                # Nếu không có vấn đề, tiếp tục bình thường
                i += 1
                continue
            
            fixed_lines.append(line)
            i += 1
        
        # Lưu file nếu có thay đổi
        new_content = '\n'.join(fixed_lines)
        if fixes_applied:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Applied fixes:")
            for fix in fixes_applied:
                print(f"   ✅ {fix}")
            
            return True
        else:
            print("ℹ️ No indentation errors found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def validate_syntax():
    """Kiểm tra syntax của file"""
    print("\n🔍 VALIDATING SYNTAX...")
    
    try:
        with open("/workspaces/Mentalhealth/SOULFRIEND.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, "/workspaces/Mentalhealth/SOULFRIEND.py", 'exec')
        print("✅ Syntax is valid!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error at line {e.lineno}: {e.msg}")
        print(f"   Text: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Sửa indentation errors
    if fix_all_indentation_errors():
        print("\n🎯 Indentation fixes applied!")
    
    # Validate syntax
    if validate_syntax():
        print("\n🚀 Ready to restart Streamlit!")
    else:
        print("\n⚠️ Still have syntax issues - manual fix needed")
