#!/bin/bash
"""
🚀 SOULFRIEND COMPLETE QUALITY PIPELINE
=======================================
Chạy toàn bộ quy trình kiểm tra: Tester → QA → QC

Created: August 27, 2025
Purpose: Complete quality assurance pipeline for SOULFRIEND.py
"""

echo "🚀 SOULFRIEND QUALITY PIPELINE - START"
echo "======================================"
echo "📅 $(date)"
echo "📍 Working Directory: $(pwd)"
echo ""

# Ensure we're in the right directory
cd /workspaces/Mentalhealth

echo "🔧 Phase 1: FUNCTIONAL TESTING"
echo "------------------------------"
python3 tests/tester.py
echo ""

echo "📋 Phase 2: QUALITY ASSURANCE"
echo "-----------------------------"
python3 tests/qa.py
echo ""

echo "🎯 Phase 3: QUALITY CONTROL"
echo "---------------------------"
python3 tests/qc.py
echo ""

echo "🚀 Phase 4: COMPLETE PIPELINE"
echo "-----------------------------"
python3 tests/test_runner.py
echo ""

echo "✅ QUALITY PIPELINE COMPLETED!"
echo "=============================="
echo "📅 $(date)"
echo ""
echo "📋 Check the following files for detailed reports:"
echo "   - tests/QA_REPORT_*.txt"
echo "   - tests/QC_REPORT_*.json"
echo "   - quality_assurance.log"
echo ""
echo "🎯 Next step: Review results and fix any issues before deployment"
