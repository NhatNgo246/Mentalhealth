#!/usr/bin/env python3
"""
DEEP PERFORMANCE ANALYSIS SCRIPT
Chạy phân tích hiệu suất chi tiết cho SOULFRIEND V2.0
"""

import cProfile
import pstats
import io
import time
import sys
import os
from memory_profiler import profile

# Add components to path
sys.path.append('.')

def performance_test():
    """Test hiệu suất các chức năng chính"""
    from components.scoring import calculate_scores
    from components.questionnaires import QuestionnaireManager
    
    print("🚀 BẮT ĐẦU DEEP PERFORMANCE ANALYSIS...")
    
    # Test 1: QuestionnaireManager initialization
    start_time = time.time()
    manager = QuestionnaireManager()
    init_time = time.time() - start_time
    print(f"✅ QuestionnaireManager init: {init_time:.4f}s")
    
    # Test 2: Scoring performance với nhiều lần gọi
    start_time = time.time()
    for i in range(1000):
        scores = calculate_scores('dass21', [1,2,0,3,1,2,0,3,1,2,0,3,1,2,0,3,1,2,0,3,1])
    scoring_time = time.time() - start_time
    print(f"✅ 1000 DASS-21 calculations: {scoring_time:.4f}s ({scoring_time/1000*1000:.2f}ms each)")
    
    # Test 3: Multiple questionnaire types
    questionnaires = ['dass21', 'phq9', 'gad7', 'epds', 'pss10']
    responses_map = {
        'dass21': [1,2,0,3] * 5 + [1],
        'phq9': [1,2,0,3,1,2,0,3,1],
        'gad7': [1,2,0,3,1,2,0],
        'epds': [1,2,0,3,1,2,0,3,1,2],
        'pss10': [1,2,0,3,1,2,0,3,1,2]
    }
    
    start_time = time.time()
    for quest_type in questionnaires:
        for i in range(100):
            calculate_scores(quest_type, responses_map[quest_type])
    multi_time = time.time() - start_time
    print(f"✅ 500 calculations (5 types × 100): {multi_time:.4f}s")
    
    return {
        'init_time': init_time,
        'scoring_time': scoring_time,
        'multi_time': multi_time
    }

def memory_test():
    """Test memory usage"""
    from components.scoring import calculate_scores
    import tracemalloc
    
    tracemalloc.start()
    
    # Memory baseline
    current, peak = tracemalloc.get_traced_memory()
    baseline = current
    
    # Run calculations
    for i in range(1000):
        scores = calculate_scores('dass21', [1,2,0,3,1,2,0,3,1,2,0,3,1,2,0,3,1,2,0,3,1])
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"🧠 MEMORY ANALYSIS:")
    print(f"   Baseline: {baseline / 1024 / 1024:.2f} MB")
    print(f"   Peak: {peak / 1024 / 1024:.2f} MB")
    print(f"   Final: {current / 1024 / 1024:.2f} MB")
    print(f"   Memory increase: {(current - baseline) / 1024 / 1024:.2f} MB")

def run_comprehensive_analysis():
    """Chạy phân tích toàn diện"""
    print("=" * 60)
    print("🔍 SOULFRIEND V2.0 - DEEP PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    # Performance test
    perf_results = performance_test()
    
    print("\n" + "=" * 60)
    memory_test()
    
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE SUMMARY:")
    print(f"   ⚡ Init Speed: {perf_results['init_time']*1000:.2f}ms")
    print(f"   🏃 Scoring Speed: {perf_results['scoring_time']/1000*1000:.2f}ms per calculation")
    print(f"   🎯 Multi-type Speed: {perf_results['multi_time']/500*1000:.2f}ms average")
    
    # Đánh giá performance
    if perf_results['scoring_time']/1000 < 0.01:  # < 10ms per calc
        print("   🏆 PERFORMANCE RATING: EXCELLENT")
    elif perf_results['scoring_time']/1000 < 0.05:  # < 50ms per calc
        print("   ✅ PERFORMANCE RATING: GOOD")
    else:
        print("   ⚠️ PERFORMANCE RATING: NEEDS OPTIMIZATION")

if __name__ == "__main__":
    # Run profiling
    pr = cProfile.Profile()
    pr.enable()
    
    run_comprehensive_analysis()
    
    pr.disable()
    
    # Save profile data
    pr.dump_stats('deep_performance.prof')
    
    # Print top functions
    print("\n" + "=" * 60)
    print("🔥 TOP PERFORMANCE HOTSPOTS:")
    print("=" * 60)
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(10)
    
    print(s.getvalue())
