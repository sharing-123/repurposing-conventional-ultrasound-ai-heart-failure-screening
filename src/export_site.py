from config import FIGURES_DIR
from data_loader import (
    load_binary_results, load_multiclass_results, load_baseline_characteristics,
    load_platform_comparison, load_participant_flow,
)
from metrics import platform_delta
from visualize import (
    auroc_bar, platform_gap_bar, rate_metrics_radar, rate_metrics_heatmap,
    platform_significance_bar, participant_flow_funnel, baseline_table,
)


def write_fragment(fig, filename: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / filename
    fig.write_html(path, include_plotlyjs="cdn", full_html=True)


def run() -> None:
    binary_df = load_binary_results()
    multiclass_df = load_multiclass_results()
    baseline_df = load_baseline_characteristics()
    comparison_df = load_platform_comparison()
    flow_df = load_participant_flow()

    write_fragment(
        auroc_bar(binary_df, "auroc", "Binary heart failure detection: AUROC by platform and view", "AUROC",
                   ci_low_col="auroc_ci_low", ci_high_col="auroc_ci_high"),
        "binary_auroc.html",
    )
    write_fragment(
        auroc_bar(multiclass_df, "macro_auroc", "Multiclass phenotyping: macro-AUROC by platform and view", "Macro-AUROC"),
        "multiclass_auroc.html",
    )
    write_fragment(
        platform_gap_bar(platform_delta(binary_df, "auroc"), "Where does image quality matter most? (binary AUROC gap)"),
        "binary_platform_gap.html",
    )
    write_fragment(
        platform_significance_bar(comparison_df),
        "platform_significance.html",
    )
    write_fragment(
        participant_flow_funnel(flow_df),
        "participant_flow.html",
    )
    write_fragment(
        baseline_table(baseline_df),
        "baseline_table.html",
    )
    write_fragment(
        rate_metrics_radar(binary_df, "PLAX"),
        "plax_radar.html",
    )
    write_fragment(
        rate_metrics_heatmap(binary_df, "Binary classification: full metric matrix"),
        "binary_heatmap.html",
    )
    write_fragment(
        rate_metrics_heatmap(multiclass_df, "Multiclass classification: full metric matrix"),
        "multiclass_heatmap.html",
    )


if __name__ == "__main__":
    run()
