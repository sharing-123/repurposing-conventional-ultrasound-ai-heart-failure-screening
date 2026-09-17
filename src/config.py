from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "data" / "results"
FIGURES_DIR = REPO_ROOT / "docs" / "assets" / "figures"

BINARY_RESULTS_CSV = RESULTS_DIR / "binary_classification_results.csv"
MULTICLASS_RESULTS_CSV = RESULTS_DIR / "multiclass_classification_results.csv"
BASELINE_CSV = RESULTS_DIR / "baseline_characteristics.csv"
PLATFORM_COMPARISON_CSV = RESULTS_DIR / "platform_comparison_test.csv"
PARTICIPANT_FLOW_CSV = RESULTS_DIR / "participant_flow.csv"

VIEW_ORDER = ["PLAX", "A4C", "A2C"]
PLATFORM_ORDER = ["High-end", "Low-end"]
PLATFORM_COLORS = {"High-end": "#f97316", "Low-end": "#2563eb"}
