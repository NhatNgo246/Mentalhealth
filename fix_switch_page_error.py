#!/usr/bin/env python3
"""
Auto-fix cho lỗi st.switch_page
"""

import re
import os

def fix_switch_page_error():
    """Tự động sửa lỗi st.switch_page"""
    print("🔧 AUTO-FIXING st.switch_page ERROR")
    print("=" * 40)
    
    soulfriend_file = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    try:
        with open(soulfriend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tìm và thay thế st.switch_page với cách an toàn hơn
        fixes_applied = []
        
        # Pattern 1: st.switch_page("ai_platform.py")
        if 'st.switch_page("ai_platform.py")' in content:
            content = content.replace(
                'st.switch_page("ai_platform.py")',
                '''try:
                st.switch_page("ai_platform.py")
            except Exception as e:
                st.error(f"Không thể mở AI Platform: {e}")
                st.info("🔧 Tính năng đang được cập nhật...")'''
            )
            fixes_applied.append("Fixed ai_platform.py switch_page")
        
        # Pattern 2: st.switch_page("chatbot_ai.py")
        if 'st.switch_page("chatbot_ai.py")' in content:
            content = content.replace(
                'st.switch_page("chatbot_ai.py")',
                '''try:
                st.switch_page("chatbot_ai.py")
            except Exception as e:
                st.error(f"Không thể mở Chatbot: {e}")
                st.info("🔧 Tính năng đang được cập nhật...")'''
            )
            fixes_applied.append("Fixed chatbot_ai.py switch_page")
        
        # Pattern 3: Các switch_page khác
        other_switch_patterns = re.findall(r'st\.switch_page\("([^"]+)"\)', content)
        for file_name in other_switch_patterns:
            if file_name not in ["ai_platform.py", "chatbot_ai.py"]:
                old_pattern = f'st.switch_page("{file_name}")'
                new_pattern = f'''try:
                st.switch_page("{file_name}")
            except Exception as e:
                st.error(f"Không thể mở trang: {{e}}")
                st.info("🔧 Tính năng đang được cập nhật...")'''
                
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    fixes_applied.append(f"Fixed {file_name} switch_page")
        
        # Lưu file đã sửa
        if fixes_applied:
            with open(soulfriend_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Applied fixes:")
            for fix in fixes_applied:
                print(f"   ✅ {fix}")
            
            return True
        else:
            print("ℹ️ No switch_page errors found to fix")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing switch_page: {e}")
        return False

def alternative_fix_switch_page():
    """Cách sửa thay thế - disable problematic buttons"""
    print("\n🔧 ALTERNATIVE FIX - Disable problematic buttons")
    print("=" * 50)
    
    soulfriend_file = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    try:
        with open(soulfriend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tìm và comment out các button có vấn đề
        problematic_buttons = [
            'if st.button("🤖 AI Platform"',
            'if st.button("💬 Chatbot"'
        ]
        
        fixes_applied = []
        for button_pattern in problematic_buttons:
            if button_pattern in content:
                # Tìm toàn bộ block button và comment out
                lines = content.split('\n')
                new_lines = []
                in_problematic_block = False
                indent_level = 0
                
                for line in lines:
                    if button_pattern in line:
                        in_problematic_block = True
                        indent_level = len(line) - len(line.lstrip())
                        new_lines.append(f"{'    ' * (indent_level // 4)}# DISABLED: {line.strip()}")
                        fixes_applied.append(f"Disabled: {button_pattern}")
                        continue
                    
                    if in_problematic_block:
                        current_indent = len(line) - len(line.lstrip()) if line.strip() else 0
                        if line.strip() and current_indent <= indent_level:
                            in_problematic_block = False
                        else:
                            new_lines.append(f"{'    ' * (indent_level // 4)}# {line.strip()}")
                            continue
                    
                    new_lines.append(line)
                
                content = '\n'.join(new_lines)
        
        if fixes_applied:
            with open(soulfriend_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Applied alternative fixes:")
            for fix in fixes_applied:
                print(f"   ✅ {fix}")
            
            return True
        else:
            print("ℹ️ No problematic buttons found")
            return False
            
    except Exception as e:
        print(f"❌ Error in alternative fix: {e}")
        return False

if __name__ == "__main__":
    # Thử fix chính trước
    if fix_switch_page_error():
        print("\n🎯 Primary fix applied successfully!")
    else:
        # Nếu không được, thử cách thay thế
        if alternative_fix_switch_page():
            print("\n🎯 Alternative fix applied successfully!")
        else:
            print("\n❌ No fixes could be applied")
    
    print("\n🚀 Please restart the application to see changes")
