#!/usr/bin/env python3
"""
Real-time Error Monitor and Auto-Fix
Theo dõi lỗi real-time và tự động sửa
"""

import subprocess
import time
import re
import os
from datetime import datetime

class RealTimeErrorMonitor:
    def __init__(self):
        self.workspace = "/workspaces/Mentalhealth"
        self.streamlit_process = None
        self.last_errors = set()
        
    def start_streamlit(self):
        """Khởi động Streamlit app"""
        print("🚀 Starting Streamlit app...")
        
        # Kill existing processes
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        time.sleep(2)
        
        # Start new process
        cmd = [
            f"{self.workspace}/.venv/bin/python", "-m", "streamlit", "run", 
            f"{self.workspace}/SOULFRIEND.py", 
            "--server.port", "8501", 
            "--server.address", "0.0.0.0"
        ]
        
        self.streamlit_process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=self.workspace
        )
        
        print("✅ Streamlit started with auto-monitoring")
        return self.streamlit_process
    
    def detect_and_fix_errors(self, output_line):
        """Phát hiện và sửa lỗi từ dòng output"""
        
        error_fixes = {
            "KeyError: 'score'": self.fix_score_error,
            "KeyError: 'level'": self.fix_level_error,
            "AttributeError.*level_info": self.fix_level_info_error,
            "MediaFileHandler: Missing file": self.ignore_media_error
        }
        
        for pattern, fix_func in error_fixes.items():
            if re.search(pattern, output_line, re.IGNORECASE):
                error_hash = hash(f"{pattern}_{output_line[:100]}")
                if error_hash not in self.last_errors:
                    self.last_errors.add(error_hash)
                    print(f"\n🚨 ERROR DETECTED: {pattern}")
                    if fix_func(output_line):
                        print("🔄 Restarting app after fix...")
                        return True
        return False
    
    def fix_score_error(self, error_line):
        """Sửa lỗi KeyError: 'score'"""
        print("🔧 Fixing KeyError: 'score'...")
        
        charts_file = f"{self.workspace}/components/charts.py"
        
        try:
            with open(charts_file, 'r') as f:
                content = f.read()
            
            # Sửa tất cả các truy cập 'score' không an toàn
            patterns_to_fix = [
                (r"subscales\[(\w+)\]\['score'\]", 
                 r"subscales[\1].get('score', subscales[\1].get('adjusted', subscales[\1].get('raw', 0)))"),
                (r"subscales\[cat\]\['score'\]",
                 r"subscales[cat].get('score', subscales[cat].get('adjusted', subscales[cat].get('raw', 0)))")
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
            print(f"❌ Error fixing: {e}")
        
        return False
    
    def fix_level_error(self, error_line):
        """Sửa lỗi KeyError: 'level'"""
        print("🔧 Fixing KeyError: 'level'...")
        
        charts_file = f"{self.workspace}/components/charts.py"
        
        try:
            with open(charts_file, 'r') as f:
                content = f.read()
            
            # Sửa truy cập 'level'
            old_pattern = r"subscales\[cat\]\['level'\]"
            new_pattern = r"subscales[cat].get('level', subscales[cat].get('severity', 'unknown'))"
            
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                
                with open(charts_file, 'w') as f:
                    f.write(content)
                print("✅ Fixed KeyError: 'level'")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing: {e}")
        
        return False
    
    def fix_level_info_error(self, error_line):
        """Sửa lỗi AttributeError level_info"""
        print("🔧 Fixing AttributeError: level_info...")
        
        soulfriend_file = f"{self.workspace}/SOULFRIEND.py"
        
        try:
            with open(soulfriend_file, 'r') as f:
                content = f.read()
            
            # Sửa truy cập level_info
            patterns_to_fix = [
                (r"hasattr\(([^,]+)\.level_info, '([^']+)'\)",
                 r"isinstance(\1.get('level_info', {}), dict) and '\2' in \1.get('level_info', {})"),
                (r"([^.]+)\.level_info\.([^,\s]+)",
                 r"\1.get('level_info', {}).get('\2')")
            ]
            
            fixed = False
            for old_pattern, new_pattern in patterns_to_fix:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    fixed = True
            
            if fixed:
                with open(soulfriend_file, 'w') as f:
                    f.write(content)
                print("✅ Fixed AttributeError: level_info")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing: {e}")
        
        return False
    
    def ignore_media_error(self, error_line):
        """Bỏ qua lỗi media file (lỗi internal của Streamlit)"""
        print("ℹ️ Ignoring Streamlit internal media error")
        return False
    
    def monitor_and_fix(self):
        """Monitor chính"""
        print("🔍 REAL-TIME ERROR MONITORING STARTED")
        print("=" * 50)
        
        process = self.start_streamlit()
        
        try:
            while True:
                if process.poll() is not None:
                    print("💀 Process died, restarting...")
                    process = self.start_streamlit()
                    continue
                
                output = process.stdout.readline()
                if output:
                    # In output ra terminal
                    print(output.strip())
                    
                    # Kiểm tra và sửa lỗi
                    if self.detect_and_fix_errors(output):
                        # Restart after fix
                        process.terminate()
                        time.sleep(2)
                        process = self.start_streamlit()
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitor...")
            if process:
                process.terminate()

def main():
    """Chạy monitoring"""
    monitor = RealTimeErrorMonitor()
    monitor.monitor_and_fix()

if __name__ == "__main__":
    main()
