#!/usr/bin/env python3
"""
🔍 LIVE DEBUG - Insert debug statements vào SOULFRIEND.py
"""

import sys
sys.path.insert(0, '/workspaces/Mentalhealth')

print("🔍 LIVE DEBUG SOULFRIEND.PY")
print("=" * 50)

# Read current SOULFRIEND.py content
with open('/workspaces/Mentalhealth/SOULFRIEND.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find PHQ-9 scoring line
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'score_phq9_enhanced' in line:
        print(f"Found PHQ-9 scoring at line {i+1}: {line.strip()}")
        
        # Check surrounding context
        start = max(0, i-3)
        end = min(len(lines), i+10)
        
        print("\nContext:")
        for j in range(start, end):
            marker = " --> " if j == i else "     "
            print(f"{marker}{j+1}: {lines[j]}")
        break

# Also check if enhanced_result assignment
print(f"\n🔍 Looking for enhanced_result assignments...")
for i, line in enumerate(lines):
    if 'enhanced_result =' in line and 'phq9' in line:
        print(f"Line {i+1}: {line.strip()}")

print(f"\n🔍 Current session state handling...")
for i, line in enumerate(lines):
    if 'st.session_state.enhanced_scores = enhanced_result' in line:
        print(f"Line {i+1}: {line.strip()}")
        # Show context
        start = max(0, i-2)
        end = min(len(lines), i+5)
        for j in range(start, end):
            marker = " --> " if j == i else "     "
            print(f"{marker}{j+1}: {lines[j]}")
        break

print(f"\n🎯 RECOMMENDATION:")
print("Need to add debug logging right after enhanced_result assignment")
print("to see what PHQ-9 actually returns in the live app.")
