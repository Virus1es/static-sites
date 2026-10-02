import pandas as pd

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