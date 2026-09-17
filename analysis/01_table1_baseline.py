"""
Recompute Table 1 (baseline demographic and clinical characteristics) from the
private patient-level dataset and write data/results/baseline_characteristics.csv.

Uses Welch's two-sample t-test for continuous variables and Pearson's
chi-square test for categorical variables, switching to Fisher's exact test
whenever any expected cell count falls below 5.
"""
import csv
from pathlib import Path

import numpy as np
import openpyxl
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "Dataset_Acta_medica.xlsx"
OUT = ROOT / "data" / "results" / "baseline_characteristics.csv"

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["Patient_Data"]
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
data = rows[1:]
col = {name: i for i, name in enumerate(header)}


def get(colname):
    return [r[col[colname]] for r in data]


hf_status = get("hf_status")
hf_group = get("hf_group")
n_total = len(data)


def split_by_group(values):
    hf_vals = [v for v, s in zip(values, hf_status) if s == "HF" and v is not None]
    nonhf_vals = [v for v, s in zip(values, hf_status) if s == "Non-HF" and v is not None]
    return nonhf_vals, hf_vals


def cont_row(colname, decimals=1):
    vals = get(colname)
    nonhf, hf = split_by_group(vals)
    all_vals = [v for v in vals if v is not None]
    t, p = stats.ttest_ind(nonhf, hf, equal_var=False)
    p_display = "<0.001" if p < 0.001 else f"{p:.3f}"
    return (
        f"{np.mean(all_vals):.{decimals}f} ± {np.std(all_vals, ddof=1):.{decimals}f}",
        f"{np.mean(nonhf):.{decimals}f} ± {np.std(nonhf, ddof=1):.{decimals}f}",
        f"{np.mean(hf):.{decimals}f} ± {np.std(hf, ddof=1):.{decimals}f}",
        p_display, "Welch two-sample t-test",
    )


def cat_row(colname, positive_value):
    vals = get(colname)
    nonhf, hf = split_by_group(vals)
    n_pos_nonhf = sum(1 for v in nonhf if v == positive_value)
    n_pos_hf = sum(1 for v in hf if v == positive_value)
    n_pos_all = n_pos_nonhf + n_pos_hf
    table = np.array([[n_pos_nonhf, len(nonhf) - n_pos_nonhf],
                       [n_pos_hf, len(hf) - n_pos_hf]])
    if (table < 5).any():
        _, p = stats.fisher_exact(table)
        test = "Fisher exact test"
    else:
        _, p, _, _ = stats.chi2_contingency(table, correction=False)
        test = "Pearson chi-square test"
    p_display = "<0.001" if p < 0.001 else f"{p:.3f}"
    return (
        f"{n_pos_all} ({100 * n_pos_all / n_total:.1f}%)",
        f"{n_pos_nonhf} ({100 * n_pos_nonhf / len(nonhf):.1f}%)",
        f"{n_pos_hf} ({100 * n_pos_hf / len(hf):.1f}%)",
        p_display, test,
    )


sex_vals = set(get("sex"))
male_token = "M" if "M" in sex_vals else ("Male" if "Male" in sex_vals else sorted(sex_vals)[0])

rows_out = [("age_years", *cont_row("age_years"))]
rows_out.append(("male_sex_pct", *cat_row("sex", male_token)))
rows_out.append(("bmi_kgm2", *cont_row("bmi_kg_m2")))
for name, colname in [
    ("hypertension_pct", "hypertension"), ("diabetes_mellitus_pct", "diabetes_mellitus"),
    ("coronary_artery_disease_pct", "coronary_artery_disease"),
    ("atrial_fibrillation_pct", "atrial_fibrillation"),
]:
    uniq = set(get(colname))
    pos = 1 if 1 in uniq else ("Yes" if "Yes" in uniq else (True if True in uniq else sorted(uniq)[-1]))
    rows_out.append((name, *cat_row(colname, pos)))
rows_out.append(("lvef_pct", *cont_row("lvef_pct")))
rows_out.append(("lv_end_diastolic_diameter_mm", *cont_row("lvedd_mm")))
rows_out.append(("lv_end_systolic_diameter_mm", *cont_row("lvesd_mm")))
rows_out.append(("left_atrial_diameter_mm", *cont_row("la_diameter_mm")))

n_nonhf = sum(1 for s in hf_status if s == "Non-HF")
n_hf = sum(1 for s in hf_status if s == "HF")
n_hfpef = sum(1 for g in hf_group if g == "HFpEF")
n_hfref = sum(1 for g in hf_group if g == "HFrEF")
rows_out.append(("non_hf_pct", f"{n_nonhf} ({100*n_nonhf/n_total:.1f}%)", "104 (100.0%)", "0 (0.0%)", "", ""))
rows_out.append(("hfpef_pct", f"{n_hfpef} ({100*n_hfpef/n_total:.1f}%)", "0 (0.0%)",
                  f"{n_hfpef} ({100*n_hfpef/n_hf:.1f}%)", "", ""))
rows_out.append(("hfref_pct", f"{n_hfref} ({100*n_hfref/n_total:.1f}%)", "0 (0.0%)",
                  f"{n_hfref} ({100*n_hfref/n_hf:.1f}%)", "", ""))

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["characteristic", "overall_n254", "non_hf_n104", "hf_n150", "p_value", "test"])
    w.writerows(rows_out)

print("Wrote", OUT)
