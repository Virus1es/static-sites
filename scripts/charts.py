import shutil

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

from scripts.config import (
    OUTPUT_DIR,
    SITE_IMAGES_DIR,
    SITE_PLOTS_DIR,
)

def _copy_to_site(source: Path, destination: Path) -> None:
    """Copy generated artifact to the directory published by Nikola."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

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
    
    _copy_to_site(output_file, SITE_IMAGES_DIR / output_file.name)
    
    return output_file

def save_interactive_hit_rate_chart(metrics: pd.DataFrame) -> Path:
    """Create an interactive Plotly chart for cache hit rate."""
    output_file = OUTPUT_DIR / "interactive_hit_rate.html"
    site_output_file = SITE_PLOTS_DIR / "hit_rate.html"
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=metrics["method"],
                y=metrics["hit_rate"],
                customdata=metrics["runs"],
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Hit rate: %{y:.2f}%<br>"
                    "Runs: %{customdata}"
                    "<extra></extra>"
                ),
            )
        ]
    )
    
    fig.update_layout(
        title="Interactive Cache Hit Rate",
        xaxis_title="Caching method",
        yaxis_title="Hit rate, %",
        yaxis=dict(range=[0, 100]),
        hovermode="x",
        template="plotly_white",
    )
    
    fig.write_html(
        output_file,
        include_plotlyjs=True,
        full_html=True,
    )
    
    _copy_to_site(output_file, site_output_file)
    
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
    
    _copy_to_site(output_file, SITE_IMAGES_DIR / output_file.name)
    
    return output_file

def save_interactive_latency_chart(metrics: pd.DataFrame) -> Path:
    """Create an interactive Plotly chart for average latency."""
    output_file = OUTPUT_DIR / "interactive_latency.html"
    site_output_file = SITE_PLOTS_DIR / "latency.html"

    fig = go.Figure(
        data=[
            go.Bar(
                x=metrics["method"],
                y=metrics["latency_ms"],
                customdata=metrics[
                    ["hit_rate", "miss_rate", "runs"]
                ],
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Latency: %{y:.2f} ms<br>"
                    "Hit Rate: %{customdata[0]:.2f}%<br>"
                    "Miss Rate: %{customdata[1]:.2f}%<br>"
                    "Runs: %{customdata[2]}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        title="Interactive Response Latency",
        xaxis_title="Caching method",
        yaxis_title="Latency, ms",
        hovermode="x",
        template="plotly_white",
    )

    fig.write_html(
        output_file,
        include_plotlyjs=True,
        full_html=True,
    )

    _copy_to_site(output_file, site_output_file)

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
    
    _copy_to_site(output_file, SITE_IMAGES_DIR / output_file.name)
    
    return output_file