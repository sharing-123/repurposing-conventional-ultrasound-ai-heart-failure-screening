"""
Test whether the AUROC gap between the high-end and low-end platforms is
statistically significant for each cardiac view (binary classification),
using an unpaired two-sample DeLong test. High-end and low-end test sets are
independent samples of cine loops (different N per platform), so this is not
a paired test. Writes data/results/platform_comparison_test.csv.
"""
import csv
from pathlib import Path

import numpy as np
import openpyxl
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "Dataset_Acta_medica.xlsx"
OUT = ROOT / "data" / "results" / "platform_comparison_test.csv"


def midrank(x):
    order = np.argsort(x)
    ranked = np.empty(len(x))
    sorted_x = x[order]
    i = 0
    while i < len(x):
        j = i
        while j < len(x) - 1 and sorted_x[j + 1] == sorted_x[i]:
            j += 1
        ranked[order[i:j + 1]] = 0.5 * (i + j) + 1
        i = j + 1
    return ranked


def delong_auc_var(scores_pos, scores_neg):
    m, n = len(scores_pos), len(scores_neg)
    all_scores = np.concatenate([scores_pos, scores_neg])
    all_rank = midrank(all_scores)
    rank_pos, rank_neg = all_rank[:m], all_rank[m:]
    pos_only_rank = midrank(scores_pos)
    neg_only_rank = midrank(scores_neg)
    v10 = (rank_pos - pos_only_rank) / n
    v01 = 1.0 - (rank_neg - neg_only_rank) / m
    auc = np.mean(v10)
    s10 = np.cov(v10, ddof=1) if m > 1 else 0.0
    s01 = np.cov(v01, ddof=1) if n > 1 else 0.0
    return float(auc), float(s10 / m + s01 / n)


wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["AI_Predictions_Binary"]
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
col = {n: i for i, n in enumerate(header)}
data = rows[1:]

out_rows = []
for view in ["PLAX", "A4C", "A2C"]:
    stats_by_platform = {}
    for platform in ["High-end", "Low-end"]:
        sub = [r for r in data if r[col["platform"]] == platform and r[col["view"]] == view]
        y_true = np.array([r[col["true_label"]] for r in sub])
        y_score = np.array([r[col["ai_score"]] for r in sub], dtype=float)
        auc, var = delong_auc_var(y_score[y_true == "HF"], y_score[y_true != "HF"])
        stats_by_platform[platform] = (auc, var)

    auc_h, var_h = stats_by_platform["High-end"]
    auc_l, var_l = stats_by_platform["Low-end"]
    se_diff = np.sqrt(var_h + var_l)
    z = (auc_h - auc_l) / se_diff if se_diff > 0 else float("nan")
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    out_rows.append([view, round(auc_h, 4), round(auc_l, 4), round(auc_h - auc_l, 4),
                      round(float(z), 3), p, bool(p < 0.05)])

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["view", "auroc_high_end", "auroc_low_end", "difference", "z_statistic",
                "p_value", "significant_at_0.05"])
    w.writerows(out_rows)

print("Wrote", OUT)
