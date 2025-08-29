#!/usr/bin/env python3
"""
COMPREHENSIVE ERROR DETECTION SYSTEM
Phát hiện lỗi tiềm ẩn trong SOULFRIEND.py
"""

import ast
import re
import json
import os
from typing import List, Dict, Any

class SOULFRIENDErrorDetector:
    def __init__(self):
        self.file_path = "/workspaces/Mentalhealth/SOULFRIEND.py"
        self.errors_found = []
        self.warnings_found = []
        
    def load_file_content(self):
        """Load và parse file content"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            self.errors_found.append(f"Cannot read file: {e}")
            return False
    
    def check_syntax_errors(self):
        """Kiểm tra syntax errors"""
        print("🔍 CHECKING SYNTAX ERRORS...")
        try:
            ast.parse(self.content)
            print("✅ No syntax errors found")
            return True
        except SyntaxError as e:
            error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
            self.errors_found.append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def check_object_attribute_access(self):
        """Kiểm tra object.attribute access patterns"""
        print("🔍 CHECKING OBJECT ATTRIBUTE ACCESS...")
        
        # Patterns có thể gây lỗi runtime
        dangerous_patterns = [
            r'result\.(\w+)',           # result.attribute
            r'enhanced_result\.(\w+)',  # enhanced_result.attribute  
            r'scores\.(\w+)',           # scores.attribute
            r'data\.(\w+)',             # data.attribute
            r'config\.(\w+)',           # config.attribute
        ]
        
        issues_found = 0
        lines = self.content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in dangerous_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    # Check if it's likely a dict/object mismatch
                    if not ('get(' in line or 'hasattr(' in line):
                        issue = f"Line {line_num}: Potentially unsafe attribute access: {line.strip()}"
                        self.warnings_found.append(issue)
                        print(f"⚠️ {issue}")
                        issues_found += 1
        
        if issues_found == 0:
            print("✅ No unsafe attribute access patterns found")
        else:
            print(f"⚠️ Found {issues_found} potentially unsafe attribute access patterns")
        
        return issues_found == 0
    
    def check_session_state_usage(self):
        """Kiểm tra session state usage"""
        print("🔍 CHECKING SESSION STATE USAGE...")
        
        # Find all session state accesses
        session_patterns = [
            r'st\.session_state\.(\w+)',
            r'session_state\.(\w+)',
        ]
        
        session_keys = set()
        lines = self.content.split('\n')
        issues_found = 0
        
        for line_num, line in enumerate(lines, 1):
            for pattern in session_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    session_keys.add(match)
                    
                    # Check for unsafe direct access
                    if f"session_state.{match}" in line and "get(" not in line:
                        if "=" in line.split(f"session_state.{match}")[0]:
                            # Assignment is OK
                            continue
                        issue = f"Line {line_num}: Unsafe session state access: {line.strip()}"
                        self.warnings_found.append(issue)
                        print(f"⚠️ {issue}")
                        issues_found += 1
        
        print(f"📊 Found {len(session_keys)} session state keys: {', '.join(sorted(session_keys))}")
        
        if issues_found == 0:
            print("✅ Session state usage appears safe")
        else:
            print(f"⚠️ Found {issues_found} potentially unsafe session state accesses")
        
        return issues_found == 0
    
    def check_import_consistency(self):
        """Kiểm tra import consistency"""
        print("🔍 CHECKING IMPORT CONSISTENCY...")
        
        # Extract all imports
        import_lines = []
        lines = self.content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                import_lines.append((line_num, stripped))
        
        # Check for duplicate imports
        seen_imports = set()
        duplicates = []
        
        for line_num, import_line in import_lines:
            if import_line in seen_imports:
                duplicates.append(f"Line {line_num}: Duplicate import: {import_line}")
            seen_imports.add(import_line)
        
        # Check for required components
        required_components = [
            'streamlit',
            'questionnaires',
            'scoring', 
            'ui',
            'charts',
            'pdf_export'
        ]
        
        missing_components = []
        all_imports = ' '.join([imp[1] for imp in import_lines])
        
        for component in required_components:
            if component not in all_imports:
                missing_components.append(component)
        
        issues_found = len(duplicates) + len(missing_components)
        
        if duplicates:
            print("❌ Duplicate imports found:")
            for dup in duplicates:
                print(f"   {dup}")
                self.warnings_found.append(dup)
        
        if missing_components:
            print("❌ Missing required components:")
            for missing in missing_components:
                print(f"   Missing: {missing}")
                self.errors_found.append(f"Missing required import: {missing}")
        
        if issues_found == 0:
            print("✅ Import consistency looks good")
        
        print(f"📊 Total imports: {len(import_lines)}")
        return issues_found == 0
    
    def check_function_definitions(self):
        """Kiểm tra function definitions và calls"""
        print("🔍 CHECKING FUNCTION DEFINITIONS...")
        
        # Extract function definitions
        function_defs = re.findall(r'def (\w+)\(', self.content)
        function_calls = re.findall(r'(\w+)\(', self.content)
        
        # Remove built-in functions and common libraries
        builtin_functions = {
            'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple',
            'range', 'enumerate', 'zip', 'map', 'filter', 'sum', 'max', 'min',
            'open', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
            'json', 'time', 'datetime', 'os', 'sys', 'st', 'pd'
        }
        
        # Find potentially undefined function calls
        undefined_calls = []
        for call in set(function_calls):
            if (call not in function_defs and 
                call not in builtin_functions and
                not call.startswith('st.') and
                not call.startswith('pd.') and
                not call.isupper()):  # Exclude constants
                undefined_calls.append(call)
        
        if undefined_calls:
            print("⚠️ Potentially undefined function calls:")
            for call in sorted(undefined_calls):
                warning = f"Function call '{call}' not defined in file"
                print(f"   {warning}")
                self.warnings_found.append(warning)
        else:
            print("✅ No obviously undefined function calls")
        
        print(f"📊 Function definitions: {len(set(function_defs))}")
        print(f"📊 Function calls: {len(set(function_calls))}")
        
        return len(undefined_calls) == 0
    
    def check_string_formatting(self):
        """Kiểm tra string formatting issues"""
        print("🔍 CHECKING STRING FORMATTING...")
        
        lines = self.content.split('\n')
        issues_found = 0
        
        for line_num, line in enumerate(lines, 1):
            # Check f-string usage
            if 'f"' in line or "f'" in line:
                # Look for potential undefined variables in f-strings
                f_string_pattern = r'f["\'].*?\{([^}]+)\}.*?["\']'
                matches = re.findall(f_string_pattern, line)
                
                for match in matches:
                    # Simple check for common undefined variables
                    var_name = match.split('.')[0].split('(')[0].strip()
                    if var_name in ['result', 'enhanced_result', 'scores', 'data']:
                        # Could be problematic if it's object access
                        if '.' in match and 'get(' not in match:
                            issue = f"Line {line_num}: Potential f-string issue: {line.strip()}"
                            self.warnings_found.append(issue)
                            print(f"⚠️ {issue}")
                            issues_found += 1
        
        if issues_found == 0:
            print("✅ String formatting appears safe")
        
        return issues_found == 0
    
    def check_exception_handling(self):
        """Kiểm tra exception handling"""
        print("🔍 CHECKING EXCEPTION HANDLING...")
        
        # Count try/except blocks
        try_count = self.content.count('try:')
        except_count = self.content.count('except:') + self.content.count('except ')
        
        # Look for bare except statements (potentially dangerous)
        bare_except_count = self.content.count('except:')
        
        print(f"📊 Try blocks: {try_count}")
        print(f"📊 Except blocks: {except_count}")
        
        if bare_except_count > 0:
            print(f"⚠️ Found {bare_except_count} bare except statements (consider being more specific)")
            warning = f"Found {bare_except_count} bare except statements"
            self.warnings_found.append(warning)
        
        if try_count > 0:
            print("✅ Exception handling is present")
        else:
            print("⚠️ No exception handling found - consider adding try/except blocks")
            self.warnings_found.append("No exception handling found")
        
        return True
    
    def run_comprehensive_error_detection(self):
        """Chạy comprehensive error detection"""
        print("🔍 COMPREHENSIVE ERROR DETECTION SYSTEM")
        print("=" * 70)
        print("Analyzing SOULFRIEND.py for potential runtime errors...")
        
        if not self.load_file_content():
            return False
        
        test_results = {}
        
        # Run all checks
        print("\n1️⃣ SYNTAX ANALYSIS")
        test_results['syntax'] = self.check_syntax_errors()
        
        print("\n2️⃣ OBJECT ATTRIBUTE ACCESS")
        test_results['attribute_access'] = self.check_object_attribute_access()
        
        print("\n3️⃣ SESSION STATE USAGE")
        test_results['session_state'] = self.check_session_state_usage()
        
        print("\n4️⃣ IMPORT CONSISTENCY")
        test_results['imports'] = self.check_import_consistency()
        
        print("\n5️⃣ FUNCTION DEFINITIONS")
        test_results['functions'] = self.check_function_definitions()
        
        print("\n6️⃣ STRING FORMATTING")
        test_results['string_formatting'] = self.check_string_formatting()
        
        print("\n7️⃣ EXCEPTION HANDLING")
        test_results['exception_handling'] = self.check_exception_handling()
        
        # Summary
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n📊 ERROR DETECTION RESULTS")
        print("=" * 70)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name.replace('_', ' ').title()}")
        
        print(f"\n🎯 Overall Score: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"❌ Errors Found: {len(self.errors_found)}")
        print(f"⚠️ Warnings Found: {len(self.warnings_found)}")
        
        if self.errors_found:
            print(f"\n🚨 CRITICAL ERRORS:")
            for error in self.errors_found:
                print(f"   ❌ {error}")
        
        if self.warnings_found and len(self.warnings_found) <= 10:  # Show limited warnings
            print(f"\n⚠️ WARNINGS (showing first 10):")
            for warning in self.warnings_found[:10]:
                print(f"   ⚠️ {warning}")
        elif self.warnings_found:
            print(f"\n⚠️ WARNINGS: {len(self.warnings_found)} warnings found (too many to display)")
        
        if success_rate >= 85 and len(self.errors_found) == 0:
            print("\n🎉 ERROR DETECTION PASSED!")
            print("💚 Code quality looks good!")
            return True
        else:
            print("\n🚨 ISSUES DETECTED!")
            print("⚠️ Review errors and warnings before deployment")
            return False

def main():
    """Run error detection"""
    detector = SOULFRIENDErrorDetector()
    success = detector.run_comprehensive_error_detection()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
