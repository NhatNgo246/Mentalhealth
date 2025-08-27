"""
Comprehensive UI Inspection Tool for Mental Health Support App
Kiểm tra toàn diện giao diện để phát hiện vấn đề hiển thị
"""

import streamlit as st
import os
import re
from typing import List, Dict, Tuple

class UIInspector:
    """Tool kiểm tra giao diện ứng dụng"""
    
    def __init__(self):
        self.issues = []
        self.suggestions = []
        
    def inspect_html_styling(self, file_path: str) -> List[Dict]:
        """Kiểm tra inline HTML styling trong file"""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Kiểm tra inline styles quá dài
        inline_styles = re.findall(r'style="([^"]*)"', content)
        for i, style in enumerate(inline_styles):
            if len(style) > 200:
                issues.append({
                    'type': 'LONG_INLINE_STYLE',
                    'description': f'Inline style quá dài ({len(style)} chars)',
                    'line': f'Style #{i+1}',
                    'suggestion': 'Chuyển sang CSS class'
                })
                
        # Kiểm tra hardcoded colors
        hardcoded_colors = re.findall(r'#[0-9a-fA-F]{3,6}', content)
        unique_colors = set(hardcoded_colors)
        if len(unique_colors) > 10:
            issues.append({
                'type': 'TOO_MANY_COLORS',
                'description': f'Quá nhiều màu hardcoded ({len(unique_colors)} màu)',
                'suggestion': 'Sử dụng CSS variables hoặc color palette'
            })
            
        # Kiểm tra responsive issues
        fixed_widths = re.findall(r'width:\s*(\d+)px', content)
        if len(fixed_widths) > 5:
            issues.append({
                'type': 'FIXED_WIDTH_OVERUSE',
                'description': f'Quá nhiều fixed width ({len(fixed_widths)} instances)',
                'suggestion': 'Sử dụng responsive units (%, rem, vw)'
            })
            
        # Kiểm tra margin/padding inconsistency
        margins = re.findall(r'margin:\s*([^;]+)', content)
        paddings = re.findall(r'padding:\s*([^;]+)', content)
        
        margin_values = set(margins)
        padding_values = set(paddings)
        
        if len(margin_values) > 8:
            issues.append({
                'type': 'INCONSISTENT_SPACING',
                'description': f'Margin không nhất quán ({len(margin_values)} values)',
                'suggestion': 'Sử dụng spacing scale system'
            })
            
        return issues
    
    def inspect_streamlit_components(self, file_path: str) -> List[Dict]:
        """Kiểm tra Streamlit components"""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Kiểm tra deprecated parameters
        deprecated_patterns = [
            (r'use_column_width=False', 'use_container_width parameter'),
            (r'allow_output_mutation=True', 'hash_funcs parameter'),
        ]
        
        for pattern, suggestion in deprecated_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append({
                    'type': 'DEPRECATED_PARAMETER',
                    'description': f'Deprecated parameter: {pattern}',
                    'suggestion': f'Use {suggestion} instead'
                })
                
        # Kiểm tra missing form validation
        form_submits = re.findall(r'st\.form_submit_button', content)
        form_declarations = re.findall(r'with st\.form', content)
        
        if len(form_declarations) != len(form_submits):
            issues.append({
                'type': 'FORM_VALIDATION',
                'description': f'Forms ({len(form_declarations)}) vs Submits ({len(form_submits)}) mismatch',
                'suggestion': 'Ensure each form has exactly one submit button'
            })
            
        # Kiểm tra accessibility issues
        images_without_alt = re.findall(r'st\.image\([^)]*\)', content)
        for img in images_without_alt:
            if 'caption=' not in img and 'use_column_width' not in img:
                issues.append({
                    'type': 'ACCESSIBILITY',
                    'description': 'Image without caption or description',
                    'suggestion': 'Add caption for screen readers'
                })
                
        return issues
    
    def inspect_layout_structure(self, file_path: str) -> List[Dict]:
        """Kiểm tra cấu trúc layout"""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Kiểm tra nested columns
        column_nesting = content.count('st.columns')
        if column_nesting > 5:
            issues.append({
                'type': 'COMPLEX_LAYOUT',
                'description': f'Quá nhiều column layouts ({column_nesting})',
                'suggestion': 'Simplify layout structure'
            })
            
        # Kiểm tra container usage
        containers = re.findall(r'with st\.(container|columns|expander)', content)
        if len(containers) > 15:
            issues.append({
                'type': 'LAYOUT_COMPLEXITY',
                'description': f'Layout quá phức tạp ({len(containers)} containers)',
                'suggestion': 'Break into smaller components'
            })
            
        # Kiểm tra markdown abuse
        markdown_calls = content.count('st.markdown')
        if markdown_calls > 20:
            issues.append({
                'type': 'MARKDOWN_OVERUSE',
                'description': f'Quá nhiều st.markdown calls ({markdown_calls})',
                'suggestion': 'Create reusable UI components'
            })
            
        return issues
    
    def inspect_text_content(self, file_path: str) -> List[Dict]:
        """Kiểm tra nội dung text"""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Kiểm tra text quá dài trong inline HTML
        html_texts = re.findall(r'>([^<]{50,})<', content)
        for text in html_texts:
            if len(text) > 150:
                issues.append({
                    'type': 'LONG_TEXT_INLINE',
                    'description': f'Text quá dài trong HTML ({len(text)} chars)',
                    'suggestion': 'Break into smaller paragraphs'
                })
                
        # Kiểm tra consistent messaging
        emoji_overuse = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿]', content))
        if emoji_overuse > 50:
            issues.append({
                'type': 'EMOJI_OVERUSE',
                'description': f'Quá nhiều emoji ({emoji_overuse})',
                'suggestion': 'Use emojis sparingly for better readability'
            })
            
        return issues
    
    def inspect_performance(self, file_path: str) -> List[Dict]:
        """Kiểm tra performance issues"""
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Kiểm tra heavy operations in main thread
        heavy_ops = [
            'pd.read_csv',
            'json.load',
            'requests.get',
            'time.sleep'
        ]
        
        for op in heavy_ops:
            if op in content and '@st.cache' not in content and 'st.cache_data' not in content:
                issues.append({
                    'type': 'PERFORMANCE',
                    'description': f'Heavy operation {op} without caching',
                    'suggestion': 'Use @st.cache_data decorator'
                })
                
        # Kiểm tra session state abuse
        session_state_usage = content.count('st.session_state')
        if session_state_usage > 20:
            issues.append({
                'type': 'SESSION_STATE_OVERUSE',
                'description': f'Quá nhiều session state usage ({session_state_usage})',
                'suggestion': 'Consider state management refactoring'
            })
            
        return issues
    
    def generate_report(self, file_path: str) -> Dict:
        """Tạo báo cáo comprehensive"""
        print(f"🔍 Inspecting UI: {file_path}")
        
        all_issues = []
        all_issues.extend(self.inspect_html_styling(file_path))
        all_issues.extend(self.inspect_streamlit_components(file_path))
        all_issues.extend(self.inspect_layout_structure(file_path))
        all_issues.extend(self.inspect_text_content(file_path))
        all_issues.extend(self.inspect_performance(file_path))
        
        # Categorize issues by severity
        critical = [i for i in all_issues if i['type'] in ['FORM_VALIDATION', 'DEPRECATED_PARAMETER', 'ACCESSIBILITY']]
        major = [i for i in all_issues if i['type'] in ['PERFORMANCE', 'LAYOUT_COMPLEXITY', 'TOO_MANY_COLORS']]
        minor = [i for i in all_issues if i['type'] in ['EMOJI_OVERUSE', 'LONG_TEXT_INLINE', 'INCONSISTENT_SPACING']]
        
        return {
            'critical': critical,
            'major': major, 
            'minor': minor,
            'total_issues': len(all_issues),
            'file': file_path
        }

def main():
    """Run comprehensive UI inspection"""
    inspector = UIInspector()
    
    # Files to inspect
    files_to_check = [
        '/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/app_simple.py',
        '/workspaces/Mentalhealth/mental-health-support-app/mental-health-support-app/components/ui.py'
    ]
    
    print("🔍 COMPREHENSIVE UI INSPECTION REPORT")
    print("=" * 60)
    
    total_critical = 0
    total_major = 0
    total_minor = 0
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            report = inspector.generate_report(file_path)
            
            print(f"\n📁 File: {os.path.basename(file_path)}")
            print(f"🔴 Critical Issues: {len(report['critical'])}")
            print(f"🟡 Major Issues: {len(report['major'])}")
            print(f"🟢 Minor Issues: {len(report['minor'])}")
            
            # Print critical issues
            if report['critical']:
                print("\n🔴 CRITICAL ISSUES:")
                for issue in report['critical']:
                    print(f"  - {issue['description']}")
                    print(f"    💡 {issue['suggestion']}")
                    
            # Print major issues
            if report['major']:
                print("\n🟡 MAJOR ISSUES:")
                for issue in report['major']:
                    print(f"  - {issue['description']}")
                    print(f"    💡 {issue['suggestion']}")
                    
            # Print first few minor issues
            if report['minor']:
                print(f"\n🟢 MINOR ISSUES (showing first 3 of {len(report['minor'])}):")
                for issue in report['minor'][:3]:
                    print(f"  - {issue['description']}")
                    print(f"    💡 {issue['suggestion']}")
                    
            total_critical += len(report['critical'])
            total_major += len(report['major'])
            total_minor += len(report['minor'])
            
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"🔴 Total Critical: {total_critical}")
    print(f"🟡 Total Major: {total_major}")
    print(f"🟢 Total Minor: {total_minor}")
    print(f"📈 Total Issues: {total_critical + total_major + total_minor}")
    
    if total_critical > 0:
        print("\n⚠️  RECOMMENDATION: Fix critical issues immediately")
    elif total_major > 0:
        print("\n💡 RECOMMENDATION: Address major issues for better UX")
    else:
        print("\n✅ RECOMMENDATION: UI quality is good, minor optimizations available")
    
    return total_critical + total_major + total_minor

if __name__ == "__main__":
    issues_count = main()
    print(f"\n🏁 Inspection completed with {issues_count} total issues found.")
