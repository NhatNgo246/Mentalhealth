#!/usr/bin/env python3
"""
DEEP ARCHITECTURE ANALYSIS SCRIPT
Phân tích kiến trúc và dependencies của SOULFRIEND V2.0
"""

import os
import ast
import json
from collections import defaultdict, Counter
import sys

def analyze_imports(file_path):
    """Phân tích imports trong một file Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append({
                        'type': 'from_import',
                        'module': module,
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
        
        return imports
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return []

def analyze_functions(file_path):
    """Phân tích functions trong một file Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count parameters
                args = len(node.args.args)
                defaults = len(node.args.defaults) if node.args.defaults else 0
                
                # Check for decorators
                decorators = [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
                
                # Count lines in function
                if hasattr(node, 'end_lineno'):
                    lines = node.end_lineno - node.lineno + 1
                else:
                    lines = None
                
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': args,
                    'defaults': defaults,
                    'decorators': decorators,
                    'lines': lines,
                    'is_async': isinstance(node, ast.AsyncFunctionDef)
                })
        
        return functions
    except Exception as e:
        print(f"Error analyzing functions in {file_path}: {e}")
        return []

def analyze_classes(file_path):
    """Phân tích classes trong một file Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Count methods
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                
                # Get base classes
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(f"{base.value.id}.{base.attr}")
                
                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': len(methods),
                    'bases': bases,
                    'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
                })
        
        return classes
    except Exception as e:
        print(f"Error analyzing classes in {file_path}: {e}")
        return []

def get_file_stats(file_path):
    """Lấy thống kê cơ bản của file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        blank_lines = len([line for line in lines if not line.strip()])
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'file_size': len(content)
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_project_structure():
    """Phân tích toàn bộ cấu trúc project"""
    print("🏗️  ANALYZING PROJECT ARCHITECTURE...")
    print("=" * 60)
    
    # Tìm tất cả Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Analysis results
    project_analysis = {
        'total_files': len(python_files),
        'files': {},
        'imports_summary': defaultdict(int),
        'functions_summary': [],
        'classes_summary': [],
        'total_stats': {
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'total_functions': 0,
            'total_classes': 0
        }
    }
    
    print(f"📁 Found {len(python_files)} Python files")
    print("\n🔍 ANALYZING EACH FILE:")
    print("-" * 60)
    
    for file_path in sorted(python_files):
        print(f"📄 {file_path}")
        
        # Basic stats
        stats = get_file_stats(file_path)
        
        # Imports
        imports = analyze_imports(file_path)
        
        # Functions
        functions = analyze_functions(file_path)
        
        # Classes
        classes = analyze_classes(file_path)
        
        # Store results
        project_analysis['files'][file_path] = {
            'stats': stats,
            'imports': imports,
            'functions': functions,
            'classes': classes
        }
        
        # Update summaries
        if 'error' not in stats:
            project_analysis['total_stats']['total_lines'] += stats['total_lines']
            project_analysis['total_stats']['code_lines'] += stats['code_lines']
            project_analysis['total_stats']['comment_lines'] += stats['comment_lines']
            project_analysis['total_stats']['blank_lines'] += stats['blank_lines']
        
        project_analysis['total_stats']['total_functions'] += len(functions)
        project_analysis['total_stats']['total_classes'] += len(classes)
        
        # Import summary
        for imp in imports:
            if imp['type'] == 'import':
                project_analysis['imports_summary'][imp['module']] += 1
            else:
                project_analysis['imports_summary'][imp['module']] += 1
        
        print(f"   📊 {stats.get('total_lines', 0)} lines, {len(functions)} functions, {len(classes)} classes")
    
    return project_analysis

def print_summary(analysis):
    """In summary của phân tích"""
    print("\n" + "=" * 60)
    print("📊 PROJECT ANALYSIS SUMMARY")
    print("=" * 60)
    
    stats = analysis['total_stats']
    print(f"📁 Total Files: {analysis['total_files']}")
    print(f"📏 Total Lines: {stats['total_lines']:,}")
    print(f"💻 Code Lines: {stats['code_lines']:,}")
    print(f"💬 Comment Lines: {stats['comment_lines']:,}")
    print(f"⬜ Blank Lines: {stats['blank_lines']:,}")
    print(f"🔧 Total Functions: {stats['total_functions']}")
    print(f"🏗️ Total Classes: {stats['total_classes']}")
    
    # Code quality metrics
    if stats['total_lines'] > 0:
        comment_ratio = stats['comment_lines'] / stats['total_lines'] * 100
        code_ratio = stats['code_lines'] / stats['total_lines'] * 100
        print(f"\n📈 CODE QUALITY METRICS:")
        print(f"   💬 Comment Ratio: {comment_ratio:.1f}%")
        print(f"   💻 Code Ratio: {code_ratio:.1f}%")
        
        if comment_ratio > 20:
            print("   ✅ EXCELLENT documentation")
        elif comment_ratio > 10:
            print("   ✅ GOOD documentation")
        else:
            print("   ⚠️ NEEDS more documentation")
    
    # Most used imports
    print(f"\n🔗 TOP DEPENDENCIES:")
    import_counter = Counter(analysis['imports_summary'])
    for module, count in import_counter.most_common(10):
        if module and not module.startswith('.'):
            print(f"   📦 {module}: {count} files")
    
    # Largest files
    print(f"\n📄 LARGEST FILES:")
    file_sizes = [(path, data['stats'].get('total_lines', 0)) 
                  for path, data in analysis['files'].items()]
    file_sizes.sort(key=lambda x: x[1], reverse=True)
    
    for path, lines in file_sizes[:10]:
        print(f"   📄 {path}: {lines:,} lines")
    
    # Architecture assessment
    print(f"\n🏗️ ARCHITECTURE ASSESSMENT:")
    avg_file_size = stats['total_lines'] / analysis['total_files'] if analysis['total_files'] > 0 else 0
    
    if avg_file_size < 200:
        print("   ✅ EXCELLENT: Well-modularized code")
    elif avg_file_size < 500:
        print("   ✅ GOOD: Reasonably sized modules")
    else:
        print("   ⚠️ CONSIDER: Breaking down large modules")
    
    print(f"   📊 Average file size: {avg_file_size:.0f} lines")

def main():
    """Main analysis function"""
    print("🔍 SOULFRIEND V2.0 - DEEP ARCHITECTURE ANALYSIS")
    print("=" * 60)
    
    # Run analysis
    analysis = analyze_project_structure()
    
    # Print summary
    print_summary(analysis)
    
    # Save detailed results
    with open('architecture_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Detailed analysis saved to 'architecture_analysis.json'")

if __name__ == "__main__":
    main()
