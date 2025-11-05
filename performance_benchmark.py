"""
Performance Benchmark Script for 가송장 생성기

This script measures and analyzes performance across all critical paths:
1. Tracking number generation speed
2. Excel I/O performance
3. Memory efficiency
4. Algorithm complexity
5. UI responsiveness (simulated)

Target: ≥ 95/100 with < 5s total time for 1000 rows
"""

import time
import sys
import os
import json
import tracemalloc
from pathlib import Path
from typing import Dict, List, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from src.core.tracking_generator import TrackingNumberGenerator
from src.core.uniqueness_checker import UniquenessChecker
from src.handlers.excel_uploader import ExcelUploadHandler
from src.handlers.excel_exporter import ExcelExportHandler


class PerformanceBenchmark:
    """Comprehensive performance analysis tool"""

    def __init__(self):
        self.results: Dict = {}
        self.test_dir = Path(__file__).parent / "test_data"
        self.test_dir.mkdir(exist_ok=True)

    def run_all_benchmarks(self):
        """Execute all performance benchmarks"""
        print("=" * 70)
        print("🚀 가송장 생성기 - PERFORMANCE BENCHMARK")
        print("=" * 70)
        print()

        # Run benchmarks
        self.benchmark_tracking_generation()
        self.benchmark_uniqueness_checker()
        self.benchmark_excel_upload()
        self.benchmark_excel_export()
        self.benchmark_memory_usage()
        self.benchmark_end_to_end()

        # Calculate overall score
        self.calculate_overall_score()

        # Display results
        self.display_results()

        return self.results

    def benchmark_tracking_generation(self):
        """Benchmark 1: Tracking number generation speed"""
        print("📊 Benchmark 1: Tracking Number Generation Speed")
        print("-" * 70)

        test_sizes = [100, 1000, 5000, 10000]
        results = []

        for size in test_sizes:
            generator = TrackingNumberGenerator()

            start_time = time.perf_counter()
            numbers = generator.generate_batch(size)
            elapsed = time.perf_counter() - start_time

            # Verify uniqueness
            unique_count = len(set(numbers))
            duplicates = size - unique_count

            time_per_1000 = (elapsed / size) * 1000

            result = {
                'size': size,
                'elapsed': elapsed,
                'time_per_1000': time_per_1000,
                'duplicates': duplicates,
                'success': duplicates == 0
            }
            results.append(result)

            print(f"  Size: {size:>6} | Time: {elapsed:>7.4f}s | "
                  f"Per 1000: {time_per_1000:>7.4f}s | Dupes: {duplicates}")

        # Calculate score (target: < 1s per 1000)
        avg_time_per_1000 = sum(r['time_per_1000'] for r in results) / len(results)
        score = min(100, max(0, 100 - (avg_time_per_1000 - 1.0) * 50))

        self.results['generation'] = {
            'score': score,
            'avg_time_per_1000': avg_time_per_1000,
            'target_time': 1.0,
            'details': results,
            'pass': avg_time_per_1000 < 1.0
        }

        print(f"\n  ✅ Score: {score:.1f}/100")
        print(f"  ⏱  Avg time per 1000: {avg_time_per_1000:.4f}s (target: < 1.0s)")
        print()

    def benchmark_uniqueness_checker(self):
        """Benchmark 2: Uniqueness checking performance (O(1) lookup)"""
        print("📊 Benchmark 2: Uniqueness Checker Performance")
        print("-" * 70)

        # Create temp history file
        temp_history = self.test_dir / "temp_history.json"

        # Test with different existing number counts
        test_sizes = [1000, 5000, 10000, 50000]
        results = []

        for existing_count in test_sizes:
            # Create checker with pre-existing numbers
            checker = UniquenessChecker(str(temp_history))
            checker.used_numbers = set(f"20251234{i:06d}" for i in range(existing_count))
            checker._save_history()

            # Benchmark batch check (1000 numbers)
            test_numbers = [f"20259999{i:06d}" for i in range(1000)]

            start_time = time.perf_counter()
            unique, dupes = checker.check_batch(test_numbers)
            elapsed = time.perf_counter() - start_time

            result = {
                'existing_count': existing_count,
                'check_count': 1000,
                'elapsed': elapsed,
                'ops_per_sec': 1000 / elapsed if elapsed > 0 else float('inf')
            }
            results.append(result)

            print(f"  Existing: {existing_count:>6} | Check: 1000 | "
                  f"Time: {elapsed:>7.4f}s | Ops/s: {result['ops_per_sec']:>10.0f}")

        # Calculate score (should be O(1), very fast)
        avg_time = sum(r['elapsed'] for r in results) / len(results)
        score = min(100, max(0, 100 - (avg_time - 0.01) * 1000))

        self.results['uniqueness'] = {
            'score': score,
            'avg_time': avg_time,
            'target_time': 0.01,
            'details': results,
            'pass': avg_time < 0.1
        }

        # Cleanup
        if temp_history.exists():
            temp_history.unlink()

        print(f"\n  ✅ Score: {score:.1f}/100")
        print(f"  ⏱  Avg check time: {avg_time:.4f}s (target: < 0.01s)")
        print()

    def benchmark_excel_upload(self):
        """Benchmark 3: Excel upload performance"""
        print("📊 Benchmark 3: Excel Upload Performance")
        print("-" * 70)

        # Create test Excel files
        test_sizes = [100, 1000, 5000]
        results = []

        for size in test_sizes:
            # Create test data
            test_df = pd.DataFrame({
                '주문번호': [f'ORDER-{i:06d}' for i in range(size)],
                '고객명': [f'고객{i}' for i in range(size)],
                '주소': [f'서울시 강남구 테헤란로 {i}' for i in range(size)],
                '전화번호': [f'010-{i:04d}-{i:04d}' for i in range(size)]
            })

            # Save to temp file
            temp_file = self.test_dir / f"test_upload_{size}.xlsx"
            test_df.to_excel(temp_file, index=False, engine='openpyxl')

            # Benchmark read
            start_time = time.perf_counter()
            df = ExcelUploadHandler.read_excel(str(temp_file))
            elapsed = time.perf_counter() - start_time

            time_per_1000 = (elapsed / size) * 1000

            result = {
                'size': size,
                'elapsed': elapsed,
                'time_per_1000': time_per_1000,
                'success': len(df) == size
            }
            results.append(result)

            print(f"  Size: {size:>6} rows | Time: {elapsed:>7.4f}s | "
                  f"Per 1000: {time_per_1000:>7.4f}s")

            # Cleanup
            temp_file.unlink()

        # Calculate score (target: < 2s per 1000)
        avg_time_per_1000 = sum(r['time_per_1000'] for r in results) / len(results)
        score = min(100, max(0, 100 - (avg_time_per_1000 - 2.0) * 25))

        self.results['excel_upload'] = {
            'score': score,
            'avg_time_per_1000': avg_time_per_1000,
            'target_time': 2.0,
            'details': results,
            'pass': avg_time_per_1000 < 2.0
        }

        print(f"\n  ✅ Score: {score:.1f}/100")
        print(f"  ⏱  Avg time per 1000: {avg_time_per_1000:.4f}s (target: < 2.0s)")
        print()

    def benchmark_excel_export(self):
        """Benchmark 4: Excel export with formatting"""
        print("📊 Benchmark 4: Excel Export Performance (with formatting)")
        print("-" * 70)

        test_sizes = [100, 1000, 5000]
        results = []

        for size in test_sizes:
            # Create test data - special codes and tracking numbers
            special_codes = [f'CODE-{i:06d}' for i in range(size)]

            # Generate tracking numbers
            generator = TrackingNumberGenerator()
            tracking_numbers = generator.generate_batch(size)

            # Benchmark export
            temp_file = self.test_dir / f"test_export_{size}.xlsx"

            start_time = time.perf_counter()
            ExcelExportHandler.create_output(
                special_codes,
                tracking_numbers,
                str(temp_file),
                apply_formatting=True
            )
            elapsed = time.perf_counter() - start_time

            time_per_1000 = (elapsed / size) * 1000

            result = {
                'size': size,
                'elapsed': elapsed,
                'time_per_1000': time_per_1000,
                'success': temp_file.exists()
            }
            results.append(result)

            print(f"  Size: {size:>6} rows | Time: {elapsed:>7.4f}s | "
                  f"Per 1000: {time_per_1000:>7.4f}s")

            # Cleanup
            if temp_file.exists():
                temp_file.unlink()

        # Calculate score (target: < 2s per 1000)
        avg_time_per_1000 = sum(r['time_per_1000'] for r in results) / len(results)
        score = min(100, max(0, 100 - (avg_time_per_1000 - 2.0) * 25))

        self.results['excel_export'] = {
            'score': score,
            'avg_time_per_1000': avg_time_per_1000,
            'target_time': 2.0,
            'details': results,
            'pass': avg_time_per_1000 < 2.0
        }

        print(f"\n  ✅ Score: {score:.1f}/100")
        print(f"  ⏱  Avg time per 1000: {avg_time_per_1000:.4f}s (target: < 2.0s)")
        print()

    def benchmark_memory_usage(self):
        """Benchmark 5: Memory efficiency"""
        print("📊 Benchmark 5: Memory Usage Analysis")
        print("-" * 70)

        test_sizes = [1000, 5000, 10000]
        results = []

        for size in test_sizes:
            # Start memory tracking
            tracemalloc.start()

            # Generate numbers
            generator = TrackingNumberGenerator()
            numbers = generator.generate_batch(size)

            # Create DataFrame
            test_df = pd.DataFrame({
                '주문번호': [f'ORDER-{i:06d}' for i in range(size)],
                '가송장 번호': numbers
            })

            # Get memory snapshot
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            memory_mb = peak / (1024 * 1024)
            memory_per_1000 = (memory_mb / size) * 1000

            result = {
                'size': size,
                'memory_mb': memory_mb,
                'memory_per_1000': memory_per_1000
            }
            results.append(result)

            print(f"  Size: {size:>6} rows | Memory: {memory_mb:>7.2f}MB | "
                  f"Per 1000: {memory_per_1000:>7.2f}MB")

        # Calculate score (target: < 100MB for 10000 rows)
        max_memory = max(r['memory_mb'] for r in results if r['size'] == 10000)
        score = min(100, max(0, 100 - (max_memory - 100) * 2))

        self.results['memory'] = {
            'score': score,
            'max_memory_mb': max_memory,
            'target_memory': 100.0,
            'details': results,
            'pass': max_memory < 100
        }

        print(f"\n  ✅ Score: {score:.1f}/100")
        print(f"  💾 Max memory: {max_memory:.2f}MB (target: < 100MB)")
        print()

    def benchmark_end_to_end(self):
        """Benchmark 6: End-to-end workflow (1000 rows)"""
        print("📊 Benchmark 6: End-to-End Workflow (1000 rows)")
        print("-" * 70)

        size = 1000

        # Create input file with 주문고유코드 column
        input_df = pd.DataFrame({
            '주문고유코드': [f'CODE-{i:06d}' for i in range(size)],
            '고객명': [f'고객{i}' for i in range(size)],
            '주소': [f'서울시 강남구 테헤란로 {i}' for i in range(size)]
        })
        input_file = self.test_dir / "test_e2e_input.xlsx"
        input_df.to_excel(input_file, index=False, engine='openpyxl')

        # Measure end-to-end
        start_time = time.perf_counter()

        # 1. Upload
        t1 = time.perf_counter()
        df = ExcelUploadHandler.read_excel(str(input_file))
        special_codes = ExcelUploadHandler.extract_special_codes(df)
        upload_time = time.perf_counter() - t1

        # 2. Generate
        t2 = time.perf_counter()
        generator = TrackingNumberGenerator()
        checker = UniquenessChecker(str(self.test_dir / "temp_e2e_history.json"))
        numbers = generator.generate_batch(size, used_numbers=checker.used_numbers)
        checker.register_batch(numbers)
        generation_time = time.perf_counter() - t2

        # 3. Export
        t3 = time.perf_counter()
        output_file = self.test_dir / "test_e2e_output.xlsx"
        ExcelExportHandler.create_output(special_codes, numbers, str(output_file), apply_formatting=True)
        export_time = time.perf_counter() - t3

        total_time = time.perf_counter() - start_time

        print(f"  1. Upload:     {upload_time:>7.4f}s")
        print(f"  2. Generate:   {generation_time:>7.4f}s")
        print(f"  3. Export:     {export_time:>7.4f}s")
        print(f"  ────────────────────────")
        print(f"  Total:         {total_time:>7.4f}s")

        # Calculate score (target: < 5s)
        score = min(100, max(0, 100 - (total_time - 5.0) * 10))

        self.results['end_to_end'] = {
            'score': score,
            'total_time': total_time,
            'upload_time': upload_time,
            'generation_time': generation_time,
            'export_time': export_time,
            'target_time': 5.0,
            'pass': total_time < 5.0
        }

        # Cleanup
        input_file.unlink()
        output_file.unlink()
        history_file = self.test_dir / "temp_e2e_history.json"
        if history_file.exists():
            history_file.unlink()

        print(f"\n  ✅ Score: {score:.1f}/100")
        print(f"  ⏱  Total time: {total_time:.4f}s (target: < 5.0s)")
        print()

    def calculate_overall_score(self):
        """Calculate weighted overall performance score"""
        weights = {
            'generation': 0.30,      # 30% - Most critical
            'uniqueness': 0.15,      # 15% - Important for correctness
            'excel_upload': 0.15,    # 15% - User-facing
            'excel_export': 0.15,    # 15% - User-facing
            'memory': 0.10,          # 10% - Important but not critical
            'end_to_end': 0.15       # 15% - Overall experience
        }

        total_score = sum(
            self.results[key]['score'] * weight
            for key, weight in weights.items()
        )

        self.results['overall'] = {
            'score': total_score,
            'weights': weights,
            'pass': total_score >= 95.0
        }

    def display_results(self):
        """Display comprehensive performance report"""
        print("=" * 70)
        print("📈 PERFORMANCE REPORT")
        print("=" * 70)
        print()

        print("Individual Scores:")
        print("-" * 70)
        print(f"  1. Generation Speed:     {self.results['generation']['score']:>6.1f}/100  {'✅' if self.results['generation']['pass'] else '❌'}")
        print(f"  2. Uniqueness Check:     {self.results['uniqueness']['score']:>6.1f}/100  {'✅' if self.results['uniqueness']['pass'] else '❌'}")
        print(f"  3. Excel Upload:         {self.results['excel_upload']['score']:>6.1f}/100  {'✅' if self.results['excel_upload']['pass'] else '❌'}")
        print(f"  4. Excel Export:         {self.results['excel_export']['score']:>6.1f}/100  {'✅' if self.results['excel_export']['pass'] else '❌'}")
        print(f"  5. Memory Usage:         {self.results['memory']['score']:>6.1f}/100  {'✅' if self.results['memory']['pass'] else '❌'}")
        print(f"  6. End-to-End:           {self.results['end_to_end']['score']:>6.1f}/100  {'✅' if self.results['end_to_end']['pass'] else '❌'}")
        print()

        overall_score = self.results['overall']['score']
        overall_pass = self.results['overall']['pass']

        print("=" * 70)
        print(f"🎯 OVERALL PERFORMANCE SCORE: {overall_score:.1f}/100  {'✅ PASS' if overall_pass else '❌ FAIL'}")
        print("=" * 70)
        print()

        # Bottleneck analysis
        self.analyze_bottlenecks()

        # Recommendations
        self.provide_recommendations()

    def analyze_bottlenecks(self):
        """Identify performance bottlenecks"""
        print("🔍 BOTTLENECK ANALYSIS")
        print("-" * 70)

        bottlenecks = []

        # Check each component
        if self.results['generation']['score'] < 90:
            bottlenecks.append({
                'component': 'Tracking Generation',
                'severity': 'HIGH',
                'issue': f"Generation time {self.results['generation']['avg_time_per_1000']:.4f}s per 1000 (target: < 1.0s)",
                'impact': 'Slow number generation delays entire workflow'
            })

        if self.results['uniqueness']['score'] < 90:
            bottlenecks.append({
                'component': 'Uniqueness Checker',
                'severity': 'MEDIUM',
                'issue': f"Check time {self.results['uniqueness']['avg_time']:.4f}s (target: < 0.01s)",
                'impact': 'O(1) lookup may be compromised'
            })

        if self.results['excel_upload']['score'] < 90:
            bottlenecks.append({
                'component': 'Excel Upload',
                'severity': 'MEDIUM',
                'issue': f"Upload time {self.results['excel_upload']['avg_time_per_1000']:.4f}s per 1000 (target: < 2.0s)",
                'impact': 'Slow file loading affects user experience'
            })

        if self.results['excel_export']['score'] < 90:
            bottlenecks.append({
                'component': 'Excel Export',
                'severity': 'MEDIUM',
                'issue': f"Export time {self.results['excel_export']['avg_time_per_1000']:.4f}s per 1000 (target: < 2.0s)",
                'impact': 'Slow export delays final file delivery'
            })

        if self.results['memory']['score'] < 90:
            bottlenecks.append({
                'component': 'Memory Usage',
                'severity': 'LOW',
                'issue': f"Memory usage {self.results['memory']['max_memory_mb']:.2f}MB (target: < 100MB)",
                'impact': 'High memory usage may cause issues on low-end systems'
            })

        if bottlenecks:
            for i, b in enumerate(bottlenecks, 1):
                print(f"  {i}. [{b['severity']}] {b['component']}")
                print(f"     Issue:  {b['issue']}")
                print(f"     Impact: {b['impact']}")
                print()
        else:
            print("  ✅ No significant bottlenecks detected!")
            print()

    def provide_recommendations(self):
        """Provide optimization recommendations"""
        print("💡 OPTIMIZATION RECOMMENDATIONS")
        print("-" * 70)

        recommendations = []

        overall_score = self.results['overall']['score']

        if overall_score >= 95:
            print("  🎉 Excellent performance! All targets met.")
            print("  System is production-ready with optimal performance.")
        elif overall_score >= 85:
            print("  ✅ Good performance overall.")
            print("  Minor optimizations recommended:")
            print()

            if self.results['generation']['score'] < 95:
                print("  • Generation: Consider batch size tuning")

            if self.results['excel_export']['score'] < 95:
                print("  • Export: Consider optional formatting to speed up large exports")

            if self.results['memory']['score'] < 95:
                print("  • Memory: Consider streaming for very large files")

        else:
            print("  ⚠️  Performance needs improvement.")
            print()

            if self.results['generation']['score'] < 85:
                print("  🔴 CRITICAL: Generation performance")
                print("     → Optimize random number generation")
                print("     → Review duplicate checking algorithm")
                print("     → Consider reducing MAX_RETRY_ATTEMPTS")
                print()

            if self.results['uniqueness']['score'] < 85:
                print("  🟡 HIGH: Uniqueness checker performance")
                print("     → Ensure O(1) set lookup is used (not list)")
                print("     → Consider lazy loading history file")
                print("     → Review history save frequency")
                print()

            if self.results['excel_upload']['score'] < 85:
                print("  🟡 HIGH: Excel upload performance")
                print("     → Consider reading only necessary columns")
                print("     → Use chunked reading for large files")
                print()

            if self.results['excel_export']['score'] < 85:
                print("  🟡 HIGH: Excel export performance")
                print("     → Make formatting optional")
                print("     → Consider using xlsxwriter for better performance")
                print()

            if self.results['memory']['score'] < 85:
                print("  🟢 MEDIUM: Memory usage")
                print("     → Implement streaming for large datasets")
                print("     → Clear intermediate DataFrames")
                print()

        print()
        print("=" * 70)


def main():
    """Run performance benchmark"""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_all_benchmarks()

    # Save results to JSON
    output_file = Path(__file__).parent / "performance_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"💾 Results saved to: {output_file}")
    print()

    # Return exit code based on pass/fail
    return 0 if results['overall']['pass'] else 1


if __name__ == "__main__":
    sys.exit(main())
