import hashlib
import json

from pathlib import Path

def calculate_fingerprint(data_file: Path, analysis_file: tuple[Path, ...]) -> str:
    """Calculate a fingerprint of the input data and analysis code."""
    hasher = hashlib.sha256()
    
    hasher.update(data_file.read_bytes())
    
    for file in analysis_file:
        hasher.update(b"\0")
        hasher.update(str(file.name).encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(file.read_bytes())
    
    return hasher.hexdigest()

def is_cache_valid(
    fingerprint: str, 
    cache_state_file: Path, 
    expected_outputs: tuple[Path, ...]
) -> bool:
    """Check whether cached analysis results are still valid."""
    if not cache_state_file.exists():
        return False
    
    if not all(path.exists() for path in expected_outputs):
        return False
    
    try:
        state = json.loads(
            cache_state_file.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return False
    
    return state.get("fingerprint") == fingerprint

def save_cache_state(
    fingerprint: str,
    data_file: Path,
    root_dir: Path,
    cache_state_file: Path,
    build_time: str,
) -> None:
    """Save the current analysis fingerprint."""
    state = {
        "fingerprint": fingerprint,
        "data_file": str(data_file.relative_to(root_dir)),
        "generated_at": build_time,
    }
    
    cache_state_file.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8",
    )
