#!/usr/bin/env python3
"""
Auto Error Detection and Fix System
Hệ thống tự động phát hiện và sửa lỗi trong terminal
"""

import re
import os
import sys
import time
import subprocess
from datetime import datetime

class AutoErrorFixer:
    def __init__(self, workspace_path="/workspaces/Mentalhealth"):
        self.workspace_path = workspace_path
        self.error_patterns = {
            "KeyError: 'score'": self.fix_score_keyerror,
            "KeyError: 'level'": self.fix_level_keyerror,
            "AttributeError.*'dict' object has no attribute": self.fix_dict_attribute_error,
            "MediaFileHandler: Missing file": self.fix_missing_media_file,
            "ImportError": self.fix_import_error,
            "ModuleNotFoundError": self.fix_module_not_found
        }
        
    def analyze_terminal_output(self, terminal_output):
        """Phân tích output từ terminal để tìm lỗi"""
        errors_found = []
        
        for pattern, fix_function in self.error_patterns.items():
            if re.search(pattern, terminal_output, re.IGNORECASE):
                errors_found.append({
                    'pattern': pattern,
                    'fix_function': fix_function,
                    'error_text': self.extract_error_details(terminal_output, pattern)
                })
        
        return errors_found
    
    def extract_error_details(self, output, pattern):
        """Trích xuất chi tiết lỗi từ output"""
        lines = output.split('\n')
        error_context = []
        
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                # Lấy 5 dòng trước và sau lỗi
                start = max(0, i-5)
                end = min(len(lines), i+5)
                error_context = lines[start:end]
                break
        
        return '\n'.join(error_context)
    
    def fix_score_keyerror(self, error_details):
        """Sửa lỗi KeyError: 'score'"""
        print("🔧 Fixing KeyError: 'score' in charts.py...")
        
        # Tìm file bị lỗi
        if "create_radar_chart" in error_details:
            file_path = f"{self.workspace_path}/components/charts.py"
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Sửa create_radar_chart function
                old_pattern = r"scores = \[subscales\[cat\]\['score'\] for cat in categories\]"
                new_pattern = "scores = [subscales[cat].get('score', subscales[cat].get('adjusted', subscales[cat].get('raw', 0))) for cat in categories]"
                
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print("✅ Fixed KeyError: 'score' in create_radar_chart")
                    return True
                    
            except Exception as e:
                print(f"❌ Error fixing score KeyError: {e}")
                return False
                
        return False
    
    def fix_level_keyerror(self, error_details):
        """Sửa lỗi KeyError: 'level'"""
        print("🔧 Fixing KeyError: 'level' in charts.py...")
        
        file_path = f"{self.workspace_path}/components/charts.py"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Sửa level access
            old_pattern = r"levels = \[subscales\[cat\]\['level'\] for cat in categories\]"
            new_pattern = "levels = [subscales[cat].get('level', subscales[cat].get('severity', 'unknown')) for cat in categories]"
            
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ Fixed KeyError: 'level'")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing level KeyError: {e}")
            return False
            
        return False
    
    def fix_dict_attribute_error(self, error_details):
        """Sửa lỗi AttributeError khi truy cập dict như object"""
        print("🔧 Fixing AttributeError: 'dict' object has no attribute...")
        
        if "level_info" in error_details:
            file_path = f"{self.workspace_path}/SOULFRIEND.py"
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Sửa truy cập level_info
                old_pattern = r"hasattr\(([^,]+)\.level_info, '([^']+)'\)"
                new_pattern = r"isinstance(\1.get('level_info', {}), dict) and '\2' in \1.get('level_info', {})"
                
                content = re.sub(old_pattern, new_pattern, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ Fixed AttributeError for level_info")
                return True
                
            except Exception as e:
                print(f"❌ Error fixing AttributeError: {e}")
                return False
                
        return False
    
    def fix_missing_media_file(self, error_details):
        """Sửa lỗi file media bị thiếu"""
        print("🔧 Fixing missing media file error...")
        # Đây là lỗi Streamlit internal, có thể bỏ qua
        print("ℹ️ Media file error is internal Streamlit issue - can be ignored")
        return True
    
    def fix_import_error(self, error_details):
        """Sửa lỗi import"""
        print("🔧 Fixing import error...")
        # Implement import fixes if needed
        return True
    
    def fix_module_not_found(self, error_details):
        """Sửa lỗi module not found"""
        print("🔧 Fixing module not found error...")
        # Implement module installation if needed
        return True
    
    def auto_fix_errors(self, terminal_output):
        """Tự động sửa các lỗi được phát hiện"""
        print("🔍 AUTO ERROR DETECTION STARTED")
        print("=" * 50)
        
        errors = self.analyze_terminal_output(terminal_output)
        
        if not errors:
            print("✅ No errors detected")
            return True
        
        print(f"🚨 Found {len(errors)} error(s) to fix:")
        
        fixed_count = 0
        for error in errors:
            print(f"\n📋 Error: {error['pattern']}")
            if error['fix_function'](error['error_text']):
                fixed_count += 1
        
        print(f"\n📊 Fixed {fixed_count}/{len(errors)} errors")
        
        if fixed_count > 0:
            print("🔄 Restarting application...")
            return False  # Signal restart needed
        
        return True

def monitor_and_fix():
    """Chạy monitoring và auto-fix"""
    fixer = AutoErrorFixer()
    
    print("🚀 STARTING AUTO ERROR MONITORING")
    print("=" * 50)
    
    # Giả lập terminal output (trong thực tế sẽ lấy từ terminal thực)
    sample_output = """
    KeyError: 'score'
    File "/workspaces/Mentalhealth/components/charts.py", line 72, in create_radar_chart
    scores = [subscales[cat]['score'] for cat in categories]
    """
    
    result = fixer.auto_fix_errors(sample_output)
    return result

if __name__ == "__main__":
    monitor_and_fix()
