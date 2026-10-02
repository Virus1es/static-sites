from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

SITE_BASE_URL = os.getenv("SITE_URL", "").rstrip("/")

DATA_FILE = ROOT_DIR / "data" / "experiment_results.csv"

OUTPUT_DIR = ROOT_DIR / "generated"

SITE_IMAGES_DIR = ROOT_DIR / "images" / "generated"
SITE_PLOTS_DIR = ROOT_DIR / "files" / "plots"

RESULTS_PAGE = ROOT_DIR / "pages" / "results.md"

CACHE_DIR = ROOT_DIR / ".cache" / "experiment"
CACHE_STATE_FILE = CACHE_DIR / "state.json"

ANALYSIS_FILES = tuple(sorted(SCRIPTS_DIR.glob("*.py")))

EXPECTED_OUTPUTS = (
    OUTPUT_DIR / "metrics.csv",
    OUTPUT_DIR / "results.md",
    OUTPUT_DIR / "hit_rate.png",
    OUTPUT_DIR / "latency.png",
    OUTPUT_DIR / "latency_distribution.png",
    OUTPUT_DIR / "interactive_hit_rate.html",
    OUTPUT_DIR / "interactive_latency.html",
    SITE_IMAGES_DIR / "hit_rate.png",
    SITE_IMAGES_DIR / "latency.png",
    SITE_IMAGES_DIR / "latency_distribution.png",
    SITE_PLOTS_DIR / "hit_rate.html",
    SITE_PLOTS_DIR / "latency.html",
    RESULTS_PAGE,
)

def ensure_directories() -> None:
    """Create directories required by the analysis pipeline."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SITE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    SITE_PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
def site_url(path: str) -> str:
    """Build a URL relative to the configured site base URL."""
    normalized_path = path.lstrip("/")
    
    if SITE_BASE_URL:
        return f"{SITE_BASE_URL}/{normalized_path}"
    
    return f"/{normalized_path}"