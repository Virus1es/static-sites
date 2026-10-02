from pathlib import Path

import pandas as pd

REQIRED_COLUMNS = {
    "run",
    "method",
    "scenario",
    "hit_rate",
    "latency_ms",
    "miss_rate",
}

NUMERIC_COLUMNS = {
    "run",
    "hit_rate",
    "latency_ms",
    "miss_rate",
}

def load_data(data_file: Path) -> pd.DataFrame:
    """Load and validate source experimental data."""
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    data = pd.read_csv(data_file)
    
    missing_columns = REQIRED_COLUMNS - set(data.columns)
    
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )
    
    if data.empty:
        raise ValueError("Experimental data is empty.")
    
    for column in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"Column '{column}' must contain numeric values.")
    
    return data