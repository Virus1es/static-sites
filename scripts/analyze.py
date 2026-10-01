from pathlib import Path
import shutil
import argparse
import hashlib
import json
import time
import subprocess

import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "experiment_results.csv"
OUTPUT_DIR = ROOT_DIR / "generated"

SITE_IMAGES_DIR = ROOT_DIR / "images" / "generated"
RESULTS_PAGE = ROOT_DIR / "pages" / "results.md"

CACHE_DIR = ROOT_DIR / ".cache" / "experiment"
CACHE_STATE_FILE = CACHE_DIR / "state.json"


SITE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

EXPECTED_OUTPUTS = (
    OUTPUT_DIR / "metrics.csv",
    OUTPUT_DIR / "results.md",
    OUTPUT_DIR / "hit_rate.png",
    OUTPUT_DIR / "latency.png",
    OUTPUT_DIR / "latency_distribution.png",
    SITE_IMAGES_DIR / "hit_rate.png",
    SITE_IMAGES_DIR / "latency.png",
    SITE_IMAGES_DIR / "latency_distribution.png",
    RESULTS_PAGE,
)

def load_data() -> pd.DataFrame:
    """Load and validate source experimental data."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")
    
    data = pd.read_csv(DATA_FILE)
    
    required_columns = {
        "run",
        "method",
        "scenario",
        "hit_rate",
        "latency_ms",
        "miss_rate",
    }
    
    missing_columns = required_columns - set(data.columns)
    
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )
    
    if data.empty:
        raise ValueError("Experimental data is empty.")
    
    numeric_columns = {
        "run",
        "hit_rate",
        "latency_ms",
        "miss_rate",
    }
    
    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"Column '{column}' must contain numeric values.")
    
    return data

def calculate_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate aggregated metrics for each caching method."""
    metrics = (
        data.groupby("method")
        .agg(
            runs=("run", "count"),
            hit_rate=("hit_rate", "mean"),
            miss_rate=("miss_rate", "mean"),
            latency_ms=("latency_ms", "mean"),
            latency_std_ms=("latency_ms", "std"),
        )
        .reset_index()
    )
    
    metrics["hit_rate"] = metrics["hit_rate"].round(2)
    metrics["miss_rate"] = metrics["miss_rate"].round(2)
    metrics["latency_ms"] = metrics["latency_ms"].round(2)
    metrics["latency_std_ms"] = metrics["latency_std_ms"].fillna(0).round(2)
    
    return metrics

def save_metrics(metrics: pd.DataFrame) -> Path:
    """Save aggregated metrics to CSV."""
    output_file = OUTPUT_DIR / "metrics.csv"
    metrics.to_csv(output_file, index=False)
    return output_file

def save_hit_rate_chart(metrics: pd.DataFrame) -> Path:
    """Create a chart with average cache hit rate."""
    output_file = OUTPUT_DIR / "hit_rate.png"
    
    plt.figure(figsize=(10, 6))
    plt.bar(metrics["method"], metrics["hit_rate"])
    
    plt.title("Average Cache Hit Rate")
    plt.xlabel("Caching method")
    plt.ylabel("Hit rate, %")
    plt.xticks(rotation=20, ha="right")
    plt.ylim(0, 100)
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150)
    plt.close()
    
    shutil.copy2(output_file, SITE_IMAGES_DIR / output_file.name)
    
    return output_file

def save_latency_chart(metrics: pd.DataFrame) -> Path:
    """Create a chart with average latency."""
    output_file = OUTPUT_DIR / "latency.png"
    
    plt.figure(figsize=(10, 6))
    plt.bar(metrics["method"], metrics["latency_ms"])
    
    plt.title("Average Response Latency")
    plt.xlabel("Caching method")
    plt.ylabel("Latency, ms")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150)
    plt.close()
    
    shutil.copy2(output_file, SITE_IMAGES_DIR / output_file.name)
    
    return output_file

def save_latency_distribution(data: pd.DataFrame) -> Path:
    """Create a boxplot showing latency distribution across runs."""
    output_file = OUTPUT_DIR / "latency_distribution.png"
    
    methods: list[str] = [
        str(method) for method in data["method"].unique()
    ]
    values = [
        data.loc[data["method"] == method, "latency_ms"]
        for method in methods
    ]
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(values, tick_labels=methods)
    
    plt.title("Latency Distribution Across Experimental Runs")
    plt.xlabel("Caching method")
    plt.ylabel("Latency, ms")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150)
    plt.close()
    
    shutil.copy2(output_file, SITE_IMAGES_DIR / output_file.name)
    
    return output_file

def save_markdown_report(metrics: pd.DataFrame) -> Path:
    """Generate Markdown report and publish it as a Nikola page."""
    output_file = OUTPUT_DIR / "results.md"
    
    git_commit = get_git_commit()
    dataset_version = get_dataset_version()
    build_time = get_build_time()
    
    markdown = f"""<!--
.. title: Результаты эксперимента
.. slug: results
-->

На текущем этапе используются синтетические данные,
имитирующие результаты экспериментов по сравнению методов кэширования.

## Версия результата

| Параметр | Значение |
|---|---|
| Commit | `{git_commit}` |
| Dataset version | `{dataset_version}` |
| Build time | `{build_time}` |

## Сводные результаты


"""
    
    markdown += metrics.to_markdown(index=False)
    
    markdown += """

## Метрики

- **Hit Rate** — доля запросов, обработанных из кэша.
- **Miss Rate** — доля запросов, для которых потребовалось обращение к источнику данных.
- **Latency** — среднее время ответа.
- **Latency Std** — стандартное отклонение задержки между запусками.

## Визуализация

### Cache Hit Rate

![Cache Hit Rate](/images/generated/hit_rate.png)

### Average Latency

![Average Latency](/images/generated/latency.png)

### Latency Distribution

![Latency Distribution](/images/generated/latency_distribution.png)
"""
    
    output_file.write_text(markdown, encoding="utf-8")
    
    RESULTS_PAGE.write_text(markdown, encoding="utf-8")
    
    return output_file

def calculate_fingerprint() -> str:
    """Calculate a fingerprint of the input data and analysis code."""
    hasher = hashlib.sha256()
    
    hasher.update(DATA_FILE.read_bytes())
    hasher.update(b"\0")
    hasher.update(Path(__file__).read_bytes())
    
    return hasher.hexdigest()

def is_cache_valid(fingerprint: str) -> bool:
    """Check whether cached analysis results are still valid."""
    if not CACHE_STATE_FILE.exists():
        return False
    
    if not all(path.exists() for path in EXPECTED_OUTPUTS):
        return False
    
    try:
        state = json.loads(
            CACHE_STATE_FILE.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return False
    
    return state.get("fingerprint") == fingerprint

def save_cache_state(fingerprint: str) -> None:
    """Save the current analysis fingerprint."""
    state = {
        "fingerprint": fingerprint,
        "data_file": str(DATA_FILE.relative_to(ROOT_DIR)),
        "generated_at": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(),
        ),
    }
    
    CACHE_STATE_FILE.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8",
    )

def get_git_commit() -> str: 
    """Return the current Git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()
    except(OSError, subprocess.CalledProcessError):
        return "unknown"

def get_dataset_version() -> str:
    """Return a short SHA-256 hash of the source dataset."""
    return hashlib.sha256(DATA_FILE.read_bytes()).hexdigest()[:12]

def get_build_time() -> str:
    """Return the current UTC build time."""
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate experiment results and charts."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore cache and recalculate results."
    )
    
    args = parser.parse_args()
    
    start_time = time.perf_counter()
    
    print(f"Data file: {DATA_FILE}")
    
    fingerprint = calculate_fingerprint()
    
    if not args.force and is_cache_valid(fingerprint):
        elapsed = time.perf_counter() - start_time
        
        print("Cache hit: input data and analysis code are unchanged.")
        print("Analysis skipped.")
        print(f"Elapsed time: {elapsed:.3f} s")
        
        return
    
    print("Cache miss: recalculating results.")
    
    data = load_data()
    
    print(f"Loaded {len(data)} experiment records.")
    
    metrics = calculate_metrics(data)
    
    print("\nCalculated  metrics: ")
    print(metrics.to_string(index=False))
    
    save_metrics(metrics)
    save_hit_rate_chart(metrics)
    save_latency_chart(metrics)
    save_latency_distribution(data)
    save_markdown_report(metrics)
    
    save_cache_state(fingerprint)
    
    elapsed = time.perf_counter() - start_time
    
    print("\nGenerated files: ")
    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(f" - {file.relative_to(ROOT_DIR)}")
    
    print(f"\nAnalysis completed in {elapsed:.3f} s")

if __name__ == "__main__":
    main()