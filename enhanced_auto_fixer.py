#!/usr/bin/env python3
"""
Enhanced Auto Error Fixer with switch_page support
Hệ thống auto-fix nâng cao với hỗ trợ lỗi switch_page
"""

import re
import subprocess
import time

class EnhancedAutoErrorFixer:
    def __init__(self):
        self.workspace = "/workspaces/Mentalhealth"
        self.error_patterns = {
            "StreamlitAPIException.*switch_page": self.fix_switch_page_error,
            "KeyError: 'score'": self.fix_score_keyerror,
            "KeyError: 'level'": self.fix_level_keyerror,
            "AttributeError.*'dict' object has no attribute": self.fix_dict_attribute_error,
            "IndentationError": self.fix_indentation_error,
            "SyntaxError": self.fix_syntax_error,
            "MediaFileHandler: Missing file": self.ignore_media_error
        }
    
    def detect_and_fix_from_terminal_output(self, output):
        """Phát hiện lỗi từ terminal output và auto-fix"""
        print("🔍 SCANNING FOR ERRORS...")
        
        for pattern, fix_func in self.error_patterns.items():
            if re.search(pattern, output, re.IGNORECASE | re.DOTALL):
                print(f"🚨 DETECTED: {pattern}")
                if fix_func(output):
                    print("✅ Auto-fix applied successfully!")
                    return True
        
        return False
    
    def fix_switch_page_error(self, error_output):
        """Sửa lỗi st.switch_page"""
        print("🔧 Fixing switch_page error...")
        
        try:
            soulfriend_file = f"{self.workspace}/SOULFRIEND.py"
            
            with open(soulfriend_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Sửa các lỗi indentation trong try-except blocks
            lines = content.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):
                # Tìm dòng có indentation sai trong try block
                if re.search(r'^\s+try:\s*$', line):
                    fixed_lines.append(line)
                    # Kiểm tra dòng tiếp theo
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        # Nếu dòng tiếp theo có indentation sai
                        if re.search(r'^\s+st\.switch_page', next_line):
                            # Lấy indentation của try
                            try_indent = len(line) - len(line.lstrip())
                            # Thêm 4 spaces cho nội dung try block
                            correct_indent = ' ' * (try_indent + 4)
                            fixed_next_line = correct_indent + next_line.strip()
                            fixed_lines.append(fixed_next_line)
                            continue
                
                fixed_lines.append(line)
            
            # Kiểm tra nếu có thay đổi
            new_content = '\n'.join(fixed_lines)
            if new_content != content:
                with open(soulfriend_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Fixed indentation in switch_page blocks")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error fixing switch_page: {e}")
            return False
    
    def fix_score_keyerror(self, error_output):
        """Sửa lỗi KeyError: 'score'"""
        print("🔧 Fixing KeyError: 'score'...")
        
        try:
            charts_file = f"{self.workspace}/components/charts.py"
            
            with open(charts_file, 'r') as f:
                content = f.read()
            
            # Các pattern cần sửa
            patterns_to_fix = [
                (r"subscales\[cat\]\['score'\]", 
                 "subscales[cat].get('score', subscales[cat].get('adjusted', subscales[cat].get('raw', 0)))"),
                (r"subscales\[(\w+)\]\['score'\]", 
                 r"subscales[\1].get('score', subscales[\1].get('adjusted', subscales[\1].get('raw', 0)))")
            ]
            
            fixed = False
            for old_pattern, new_pattern in patterns_to_fix:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    fixed = True
            
            if fixed:
                with open(charts_file, 'w') as f:
                    f.write(content)
                print("✅ Fixed KeyError: 'score'")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing score KeyError: {e}")
        
        return False
    
    def fix_level_keyerror(self, error_output):
        """Sửa lỗi KeyError: 'level'"""
        print("🔧 Fixing KeyError: 'level'...")
        
        try:
            charts_file = f"{self.workspace}/components/charts.py"
            
            with open(charts_file, 'r') as f:
                content = f.read()
            
            old_pattern = r"subscales\[cat\]\['level'\]"
            new_pattern = "subscales[cat].get('level', subscales[cat].get('severity', 'unknown'))"
            
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                
                with open(charts_file, 'w') as f:
                    f.write(content)
                print("✅ Fixed KeyError: 'level'")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing level KeyError: {e}")
        
        return False
    
    def fix_dict_attribute_error(self, error_output):
        """Sửa lỗi AttributeError"""
        print("🔧 Fixing AttributeError...")
        # Implementation similar to previous versions
        return False
    
    def fix_indentation_error(self, error_output):
        """Sửa lỗi IndentationError"""
        print("🔧 Fixing IndentationError...")
        # Auto-fix indentation issues
        return False
    
    def fix_syntax_error(self, error_output):
        """Sửa lỗi SyntaxError"""
        print("🔧 Fixing SyntaxError...")
        # Auto-fix syntax issues
        return False
    
    def ignore_media_error(self, error_output):
        """Bỏ qua lỗi media file"""
        print("ℹ️ Ignoring Streamlit internal media error")
        return False

def auto_monitor_and_fix():
    """Chạy ứng dụng với auto-monitoring"""
    fixer = EnhancedAutoErrorFixer()
    
    print("🚀 STARTING ENHANCED AUTO-MONITOR")
    print("=" * 50)
    
    # Kill existing processes
    subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    time.sleep(2)
    
    # Start Streamlit
    cmd = [
        "/workspaces/Mentalhealth/.venv/bin/python", "-m", "streamlit", "run",
        "/workspaces/Mentalhealth/SOULFRIEND.py",
        "--server.port", "8501", "--server.address", "0.0.0.0"
    ]
    
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        cwd="/workspaces/Mentalhealth"
    )
    
    print("✅ Streamlit started with enhanced monitoring")
    
    try:
        while True:
            if process.poll() is not None:
                print("💀 Process died, restarting...")
                time.sleep(2)
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    cwd="/workspaces/Mentalhealth"
                )
                continue
            
            output = process.stdout.readline()
            if output:
                print(output.strip())
                
                # Tích lũy output để phân tích lỗi
                if any(keyword in output.lower() for keyword in ['error', 'exception', 'traceback']):
                    # Đọc thêm một số dòng để có context đầy đủ
                    error_context = output
                    for _ in range(10):  # Đọc thêm 10 dòng
                        try:
                            additional_line = process.stdout.readline()
                            if additional_line:
                                error_context += additional_line
                            else:
                                break
                        except:
                            break
                    
                    # Thử auto-fix
                    if fixer.detect_and_fix_from_terminal_output(error_context):
                        print("🔄 Restarting after auto-fix...")
                        process.terminate()
                        time.sleep(3)
                        process = subprocess.Popen(
                            cmd, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            cwd="/workspaces/Mentalhealth"
                        )
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping enhanced monitor...")
        if process:
            process.terminate()

if __name__ == "__main__":
    auto_monitor_and_fix()
