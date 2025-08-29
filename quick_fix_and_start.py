#!/usr/bin/env python3
"""
Simple Error Monitor 
Hệ thống monitor lỗi đơn giản
"""

import time
import subprocess
import os

def quick_error_scan():
    """Quét nhanh các lỗi phổ biến và sửa"""
    print("🔍 QUICK ERROR SCAN & FIX")
    print("=" * 40)
    
    fixes_applied = []
    
    # 1. Sửa lỗi KeyError trong charts.py
    charts_file = "/workspaces/Mentalhealth/components/charts.py"
    if os.path.exists(charts_file):
        with open(charts_file, 'r') as f:
            content = f.read()
        
        # Tìm và sửa các pattern nguy hiểm
        dangerous_patterns = [
            (r"subscales\[cat\]\['score'\]", "subscales[cat].get('score', subscales[cat].get('adjusted', subscales[cat].get('raw', 0)))"),
            (r"subscales\[cat\]\['level'\]", "subscales[cat].get('level', subscales[cat].get('severity', 'unknown'))"),
            (r"subscales\[(\w+)\]\['score'\]", r"subscales[\1].get('score', subscales[\1].get('adjusted', subscales[\1].get('raw', 0)))"),
            (r"subscales\[(\w+)\]\['level'\]", r"subscales[\1].get('level', subscales[\1].get('severity', 'unknown'))")
        ]
        
        modified = False
        for old_pattern, new_pattern in dangerous_patterns:
            import re
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                modified = True
                fixes_applied.append(f"Fixed pattern: {old_pattern}")
        
        if modified:
            with open(charts_file, 'w') as f:
                f.write(content)
            print("✅ Fixed KeyError patterns in charts.py")
    
    # 2. Sửa lỗi AttributeError trong SOULFRIEND.py
    soulfriend_file = "/workspaces/Mentalhealth/SOULFRIEND.py"
    if os.path.exists(soulfriend_file):
        with open(soulfriend_file, 'r') as f:
            content = f.read()
        
        # Sửa truy cập level_info
        import re
        if re.search(r"hasattr\([^,]+\.level_info,", content):
            content = re.sub(
                r"hasattr\(([^,]+)\.level_info, '([^']+)'\)",
                r"isinstance(\1.get('level_info', {}), dict) and '\2' in \1.get('level_info', {})",
                content
            )
            with open(soulfriend_file, 'w') as f:
                f.write(content)
            fixes_applied.append("Fixed AttributeError level_info access")
            print("✅ Fixed AttributeError in SOULFRIEND.py")
    
    print(f"\n📊 Applied {len(fixes_applied)} fixes:")
    for fix in fixes_applied:
        print(f"   ✅ {fix}")
    
    return len(fixes_applied) > 0

def restart_streamlit():
    """Khởi động lại Streamlit"""
    print("\n🔄 Restarting Streamlit...")
    
    # Kill existing
    subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    time.sleep(2)
    
    # Start new
    cmd = [
        "/workspaces/Mentalhealth/.venv/bin/python", "-m", "streamlit", "run",
        "/workspaces/Mentalhealth/SOULFRIEND.py",
        "--server.port", "8503", "--server.address", "0.0.0.0"
    ]
    
    process = subprocess.Popen(cmd, cwd="/workspaces/Mentalhealth")
    time.sleep(3)
    
    print("✅ Streamlit restarted on port 8503")
    return process

if __name__ == "__main__":
    # Scan và fix lỗi
    if quick_error_scan():
        print("\n🎯 Fixes applied, restarting app...")
        restart_streamlit()
    else:
        print("\n✅ No fixes needed")
        restart_streamlit()
    
    print("\n🌐 Access app at: http://0.0.0.0:8503")
