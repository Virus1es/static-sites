from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "experiment_results.csv"
OUTPUT_DIR = ROOT_DIR / "generated"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    
    return output_file

def save_markdown_report(metrics: pd.DataFrame) -> Path:
    """Generate a Markdown report from calculated metrics"""
    output_file = OUTPUT_DIR / "result.md"
    
    markdown = """# Результаты эксперимента

Ha текущем этапе используются синтетические данные,
имитирующие результаты экспериментов по сравнению методов кэширования.

## Сводные результаты

"""
    
    table = metrics.to_markdown(index=False)
    
    markdown += table
    
    markdown += """
## Метрики

- **Hit Rate** — доля запросов, обработанных из кэша.
- **Miss Rate** — доля запросов, для которых потребовалось обращение к источнику данных.
- **Latency** — среднее время ответа.
- **Latency Std** — стандартное отклонение задержки между запусками.

## Визуализация

![Cache Hit Rate](hit_rate.png)

![Average Latency](latency.png)

![Latency Distribution](latency_distribution.png)
"""
    
    output_file.write_text(markdown, encoding="utf-8")
    
    return output_file

def main() -> None:
    print(f"Loading data from: {DATA_FILE}")
    
    data = load_data()
    
    print(f"Loaded {len(data)} experiment recors.")
    
    metrics = calculate_metrics(data)
    
    print("\nCalculated metrics:")
    print(metrics.to_string(index=False))
    
    save_metrics(metrics)
    save_hit_rate_chart(metrics)
    save_latency_chart(metrics)
    save_latency_distribution(data)
    save_markdown_report(metrics)
    
    print("\nGenerated files:")
    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(f" - {file.relative_to(ROOT_DIR)}")

if __name__ == "__main__":
    main()