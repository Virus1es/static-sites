import hashlib
import subprocess
import time

from pathlib import Path

def get_git_commit(root_dir: Path) -> str: 
    """Return the current Git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root_dir,
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()
    except(OSError, subprocess.CalledProcessError):
        return "unknown"

def get_dataset_version(data_file: Path) -> str:
    """Return a short SHA-256 hash of the source dataset."""
    return hashlib.sha256(data_file.read_bytes()).hexdigest()[:12]

def get_build_time() -> str:
    """Return the current UTC build time."""
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
