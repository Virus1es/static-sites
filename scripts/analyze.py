import argparse
import time

from scripts.cache import (
    calculate_fingerprint,
    is_cache_valid,
    save_cache_state,
)
from scripts.charts import (
    save_hit_rate_chart,
    save_interactive_hit_rate_chart,
    save_interactive_latency_chart,
    save_latency_chart,
    save_latency_distribution,
    save_metrics,
)
from scripts.config import (
    ANALYSIS_FILES,
    CACHE_STATE_FILE,
    DATA_FILE,
    EXPECTED_OUTPUTS,
    ROOT_DIR,
    ensure_directories,
    OUTPUT_DIR,
)
from scripts.data import load_data
from scripts.metrics import calculate_metrics
from scripts.report import generate_report
from scripts.version import get_build_time

def main() -> None:
    """Run the complete experiment analysis pipeline."""
    parser = argparse.ArgumentParser(
        description="Generate experiment results and charts."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore cache and recalculate results."
    )
    
    args = parser.parse_args()
    
    ensure_directories()
    
    start_time = time.perf_counter()
    
    print(f"Data file: {DATA_FILE}")
    
    fingerprint = calculate_fingerprint(DATA_FILE, ANALYSIS_FILES)
    
    if not args.force and is_cache_valid(
        fingerprint,
        CACHE_STATE_FILE,
        EXPECTED_OUTPUTS
    ):
        elapsed = time.perf_counter() - start_time
        
        print("Cache hit: input data and analysis code are unchanged.")
        print("Analysis skipped.")
        print(f"Elapsed time: {elapsed:.3f} s")
        
        return
    
    print("Cache miss: recalculating results.")
    
    data = load_data(DATA_FILE)
    
    print(f"Loaded {len(data)} experiment records.")
    
    metrics = calculate_metrics(data)
    
    print("\nCalculated  metrics: ")
    print(metrics.to_string(index=False))
    
    save_metrics(metrics)
    
    save_hit_rate_chart(metrics)
    save_interactive_hit_rate_chart(metrics)
    
    save_latency_chart(metrics)
    save_interactive_latency_chart(metrics)
    save_latency_distribution(data)
    
    generate_report(metrics)
    
    save_cache_state(
        fingerprint=fingerprint,
        data_file=DATA_FILE,
        root_dir=ROOT_DIR,
        cache_state_file=CACHE_STATE_FILE,
        build_time=get_build_time(),
    )
    
    elapsed = time.perf_counter() - start_time
    
    print("\nGenerated files: ")
        
    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(f" - {file.relative_to(ROOT_DIR)}")
    
    print(f"\nAnalysis completed in {elapsed:.3f} s")

if __name__ == "__main__":
    main()