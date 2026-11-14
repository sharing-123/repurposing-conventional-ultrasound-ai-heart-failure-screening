"""
Recompute multiclass (Normal / HFpEF / HFrEF) performance from the raw
video-level predictions, with a 95% bootstrap confidence interval for overall
accuracy. Writes data/results/multiclass_classification_results.csv.

The shared prediction data retain only the discrete predicted class, not
per-class probability scores, so macro-AUROC cannot be computed from them.
The file reports macro-averaged balanced accuracy instead: for each class
c, (sensitivity_c + specificity_c) / 2 in a one-vs-rest comparison, averaged
over the three classes. Sensitivity, specificity, PPV, NPV, F1-score and the
likelihood ratios are likewise macro-averages of the one-vs-rest values.
No CI is reported for balanced accuracy; the bootstrap CI applies to overall
accuracy (2000 resamples of cine loops). See analysis/README.md.
"""
import csv
from pathlib import Path

import numpy as np
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "Dataset_Acta_medica.xlsx"
OUT = ROOT / "data" / "results" / "multiclass_classification_results.csv"

CLASSES = ["Normal", "HFpEF", "HFrEF"]
rng = np.random.default_rng(20250917)


def multiclass_metrics(y_true, y_pred):
    n = len(y_true)
    per_class = {}
    for c in CLASSES:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == c and p == c)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == c and p != c)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != c and p == c)
        tn = sum(1 for t, p in zip(y_true, y_pred) if t != c and p != c)
        sens = tp / (tp + fn) if (tp + fn) else 0.0
        spec = tn / (tn + fp) if (tn + fp) else 0.0
        ppv = tp / (tp + fp) if (tp + fp) else 0.0
        npv = tn / (tn + fn) if (tn + fn) else 0.0
        f1 = 2 * ppv * sens / (ppv + sens) if (ppv + sens) else 0.0
        lr_pos = sens / (1 - spec) if spec < 1 else float("nan")
        lr_neg = (1 - sens) / spec if spec > 0 else float("nan")
        per_class[c] = dict(sensitivity=sens, specificity=spec, ppv=ppv, npv=npv, f1=f1,
                             lr_pos=lr_pos, lr_neg=lr_neg, auc=(sens + spec) / 2)
    acc = sum(1 for t, p in zip(y_true, y_pred) if t == p) / n
    macro = {k: float(np.mean([per_class[c][k] for c in CLASSES]))
              for k in ["sensitivity", "specificity", "ppv", "npv", "f1", "lr_pos", "lr_neg", "auc"]}
    macro["accuracy"] = acc
    return macro


def bootstrap_accuracy_ci(y_true, y_pred, n_boot=2000, alpha=0.05):
    n = len(y_true)
    y_true, y_pred = np.array(y_true, dtype=object), np.array(y_pred, dtype=object)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        boots.append(multiclass_metrics(y_true[idx], y_pred[idx])["accuracy"])
    boots = np.array(boots)
    return np.percentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)])


wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["AI_Predictions_Multiclass"]
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
col = {n: i for i, n in enumerate(header)}
data = rows[1:]

out_rows = []
for platform in ["High-end", "Low-end"]:
    for view in ["PLAX", "A4C", "A2C"]:
        sub = [r for r in data if r[col["platform"]] == platform and r[col["view"]] == view]
        y_true = [r[col["true_class"]] for r in sub]
        y_pred = [r[col["predicted_class"]] for r in sub]
        macro = multiclass_metrics(y_true, y_pred)
        lo, hi = bootstrap_accuracy_ci(y_true, y_pred)
        out_rows.append([
            platform, view, len(sub), round(100 * macro["accuracy"], 2), round(100 * macro["ppv"], 2),
            round(100 * macro["sensitivity"], 2), round(100 * macro["f1"], 2),
            round(100 * macro["specificity"], 2), round(100 * macro["npv"], 2),
            f"{macro['lr_pos']:.2f}", f"{macro['lr_neg']:.2f}", f"{macro['auc']:.3f}",
            round(100 * lo, 2), round(100 * hi, 2),
        ])

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["platform", "view", "n", "accuracy", "ppv", "sensitivity", "f1", "specificity",
                "npv", "lr_positive", "lr_negative", "macro_balanced_accuracy",
                "accuracy_ci_low", "accuracy_ci_high"])
    w.writerows(out_rows)

print("Wrote", OUT)
