"""
Compute AUROC with 95% DeLong confidence intervals for binary heart failure
classification, per ultrasound platform and cardiac view, from the raw
video-level predictions. Writes data/results/binary_classification_results.csv.
"""
import csv
from pathlib import Path

import numpy as np
import openpyxl
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "Dataset_Acta_medica.xlsx"
OUT = ROOT / "data" / "results" / "binary_classification_results.csv"


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
    var = s10 / m + s01 / n
    return float(auc), float(var)


def confusion_metrics(y_true, y_pred, positive_label="HF"):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive_label and p == positive_label)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive_label and p != positive_label)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive_label and p == positive_label)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t != positive_label and p != positive_label)
    n = tp + fn + fp + tn
    sens = tp / (tp + fn) if (tp + fn) else float("nan")
    spec = tn / (tn + fp) if (tn + fp) else float("nan")
    ppv = tp / (tp + fp) if (tp + fp) else float("nan")
    npv = tn / (tn + fn) if (tn + fn) else float("nan")
    acc = (tp + tn) / n if n else float("nan")
    f1 = 2 * ppv * sens / (ppv + sens) if (ppv + sens) else float("nan")
    lr_pos = sens / (1 - spec) if (1 - spec) else float("nan")
    lr_neg = (1 - sens) / spec if spec else float("nan")
    return n, acc, ppv, sens, f1, spec, npv, lr_pos, lr_neg


wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["AI_Predictions_Binary"]
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
col = {n: i for i, n in enumerate(header)}
data = rows[1:]

out_rows = []
for platform in ["High-end", "Low-end"]:
    for view in ["PLAX", "A4C", "A2C"]:
        sub = [r for r in data if r[col["platform"]] == platform and r[col["view"]] == view]
        y_true = [r[col["true_label"]] for r in sub]
        y_pred = [r[col["predicted_label"]] for r in sub]
        y_score = np.array([r[col["ai_score"]] for r in sub], dtype=float)

        pos = y_score[np.array(y_true) == "HF"]
        neg = y_score[np.array(y_true) != "HF"]
        auc, var = delong_auc_var(pos, neg)
        se = np.sqrt(max(var, 0))
        z = stats.norm.ppf(0.975)
        lo, hi = max(0.0, auc - z * se), min(1.0, auc + z * se)

        n, acc, ppv, sens, f1, spec, npv, lr_pos, lr_neg = confusion_metrics(y_true, y_pred)
        out_rows.append([
            platform, view, n, round(100 * acc, 2), round(100 * ppv, 2), round(100 * sens, 2),
            round(100 * f1, 2), round(100 * spec, 2), round(100 * npv, 2), round(lr_pos, 2),
            round(lr_neg, 2), round(auc, 4), round(lo, 4), round(hi, 4),
        ])

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["platform", "view", "n", "accuracy", "ppv", "sensitivity", "f1", "specificity",
                "npv", "lr_positive", "lr_negative", "auroc", "auroc_ci_low", "auroc_ci_high"])
    w.writerows(out_rows)

print("Wrote", OUT)
