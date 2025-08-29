#!/usr/bin/env python3
"""
Auto-fix cho lỗi Streamlit pages
Sửa lỗi "Could not find page" trong st.switch_page
"""

import os
import shutil

def fix_streamlit_pages_error():
    """Sửa lỗi Streamlit pages"""
    print("🔧 AUTO-FIXING STREAMLIT PAGES ERROR")
    print("=" * 40)
    
    workspace = "/workspaces/Mentalhealth"
    pages_dir = f"{workspace}/pages"
    soulfriend_file = f"{workspace}/SOULFRIEND.py"
    
    # Tạo thư mục pages nếu chưa có
    if not os.path.exists(pages_dir):
        os.makedirs(pages_dir)
        print("✅ Created pages/ directory")
    
    # Danh sách files cần di chuyển vào pages/
    page_files = [
        "admin_panel.py",
        "ai_platform.py", 
        "chatbot_ai.py",
        "advanced_reports.py",
        "config_manager.py",
        "analytics_dashboard.py"
    ]
    
    moved_files = []
    
    # Di chuyển files vào pages/
    for file_name in page_files:
        src_path = f"{workspace}/{file_name}"
        dst_path = f"{pages_dir}/{file_name}"
        
        if os.path.exists(src_path):
            try:
                shutil.move(src_path, dst_path)
                moved_files.append(file_name)
                print(f"✅ Moved {file_name} to pages/")
            except Exception as e:
                print(f"⚠️ Could not move {file_name}: {e}")
        else:
            print(f"⚠️ File not found: {file_name}")
    
    # Cập nhật SOULFRIEND.py để sử dụng đường dẫn pages/
    try:
        with open(soulfriend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Thay thế các st.switch_page calls
        replacements = {
            'st.switch_page("admin_panel.py")': 'st.switch_page("pages/admin_panel.py")',
            'st.switch_page("ai_platform.py")': 'st.switch_page("pages/ai_platform.py")',
            'st.switch_page("chatbot_ai.py")': 'st.switch_page("pages/chatbot_ai.py")',
            'st.switch_page("advanced_reports.py")': 'st.switch_page("pages/advanced_reports.py")',
            'st.switch_page("config_manager.py")': 'st.switch_page("pages/config_manager.py")',
            'st.switch_page("analytics_dashboard.py")': 'st.switch_page("pages/analytics_dashboard.py")'
        }
        
        updated = False
        for old_path, new_path in replacements.items():
            if old_path in content:
                content = content.replace(old_path, new_path)
                updated = True
                print(f"✅ Updated path: {old_path} -> {new_path}")
        
        if updated:
            with open(soulfriend_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Updated SOULFRIEND.py with correct paths")
        
        return len(moved_files) > 0 or updated
        
    except Exception as e:
        print(f"❌ Error updating SOULFRIEND.py: {e}")
        return False

def alternative_fix_disable_navigation():
    """Cách thay thế: Disable các navigation buttons có vấn đề"""
    print("\n🔧 ALTERNATIVE FIX - Disable problematic navigation")
    print("=" * 50)
    
    soulfriend_file = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    try:
        with open(soulfriend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Thay thế các switch_page bằng thông báo tạm thời
        replacements = {
            'st.switch_page("admin_panel.py")': 'st.info("🔧 Tính năng Admin Panel đang được cập nhật...")',
            'st.switch_page("ai_platform.py")': 'st.info("🔧 Tính năng AI Platform đang được cập nhật...")',
            'st.switch_page("chatbot_ai.py")': 'st.info("🔧 Tính năng Chatbot đang được cập nhật...")',
            'st.switch_page("advanced_reports.py")': 'st.info("🔧 Tính năng Advanced Reports đang được cập nhật...")',
            'st.switch_page("config_manager.py")': 'st.info("🔧 Tính năng Config Manager đang được cập nhật...")',
            'st.switch_page("analytics_dashboard.py")': 'st.info("🔧 Tính năng Analytics đang được cập nhật...")'
        }
        
        updated = False
        for old_call, new_call in replacements.items():
            if old_call in content:
                content = content.replace(old_call, new_call)
                updated = True
                print(f"✅ Disabled: {old_call}")
        
        if updated:
            with open(soulfriend_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Disabled problematic navigation calls")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error in alternative fix: {e}")
        return False

def smart_fix_pages_paths():
    """Smart fix: Cập nhật paths trong SOULFRIEND.py để sử dụng pages/"""
    print("\n🔧 SMART FIX - Update paths to use pages/")
    print("=" * 45)
    
    soulfriend_file = "/workspaces/Mentalhealth/SOULFRIEND.py"
    
    try:
        with open(soulfriend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern matching để tìm các st.switch_page calls
        import re
        
        # Tìm tất cả st.switch_page calls
        pattern = r'st\.switch_page\("([^"]+)\.py"\)'
        matches = re.findall(pattern, content)
        
        updated = False
        for file_name in matches:
            if file_name in ["admin_panel", "ai_platform", "chatbot_ai", "advanced_reports", "config_manager", "analytics_dashboard"]:
                old_call = f'st.switch_page("{file_name}.py")'
                new_call = f'st.switch_page("pages/{file_name}.py")'
                
                if old_call in content:
                    content = content.replace(old_call, new_call)
                    updated = True
                    print(f"✅ Updated: {file_name}.py -> pages/{file_name}.py")
        
        if updated:
            with open(soulfriend_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Smart fix applied successfully!")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error in smart fix: {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING STREAMLIT PAGES AUTO-FIX")
    print("=" * 50)
    
    # Thử fix chính trước
    if fix_streamlit_pages_error():
        print("\n🎯 Primary fix completed!")
    elif smart_fix_pages_paths():
        print("\n🎯 Smart fix completed!")
    elif alternative_fix_disable_navigation():
        print("\n🎯 Alternative fix completed!")
    else:
        print("\n❌ No fixes could be applied")
    
    print("\n🔄 Please restart Streamlit to see changes")
