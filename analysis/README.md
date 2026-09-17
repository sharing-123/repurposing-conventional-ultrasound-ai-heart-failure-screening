# Analysis pipeline: raw predictions to reported results

This folder holds the statistical methods that turn the study's raw,
patient-linked video-level data into the aggregate tables committed in
[`data/results/`](../data/results). It exists so a reader can check exactly
how every reported number, confidence interval, and P value was computed,
even though the raw input file itself is not published here.

## Why the raw file is not included

`data/raw/Dataset_Acta_medica.xlsx` (referenced by these scripts) contains
patient-level demographic data and video-level AI prediction scores. Both are
withheld to protect participant privacy, consistent with the study's ethics
approval — see the manuscript's *Availability of data and materials*
statement. Publishing the code without the linked data lets anyone audit the
method without exposing anyone in the cohort.

## What each script does

| Script | Input sheet(s) | Output | Method |
|---|---|---|---|
| `01_table1_baseline.py` | `Patient_Data` | `data/results/baseline_characteristics.csv` | Welch's two-sample t-test for continuous variables; Pearson chi-square (Fisher exact when any expected cell count < 5) for categorical variables |
| `02_delong_auc_ci.py` | `AI_Predictions_Binary` | `data/results/binary_classification_results.csv` | DeLong (1988) nonparametric AUC variance estimator for the 95% CI, cross-checked against a stratified bootstrap (2000 resamples) |
| `03_multiclass_bootstrap_ci.py` | `AI_Predictions_Multiclass` | `data/results/multiclass_classification_results.csv` | One-vs-rest hard-classifier metrics per class, macro-averaged; 95% bootstrap CI (2000 patient-level resamples) for overall accuracy |
| `04_platform_comparison_test.py` | `AI_Predictions_Binary` | `data/results/platform_comparison_test.csv` | Unpaired two-sample DeLong test (`z = (AUC_high - AUC_low) / sqrt(var_high + var_low)`) comparing the high-end and low-end platforms per view |

## Running it

These scripts expect the private raw dataset at `data/raw/Dataset_Acta_medica.xlsx`,
which is not part of this repository. If you are the corresponding author
reproducing the committed CSVs, place that file at that path and run:

```bash
pip install openpyxl pandas numpy scipy
cd analysis
python 01_table1_baseline.py
python 02_delong_auc_ci.py
python 03_multiclass_bootstrap_ci.py
python 04_platform_comparison_test.py
```

Each script writes straight to the corresponding file in `data/results/`,
which `src/export_site.py` then turns into the interactive charts on the
[live site](https://sharing-123.github.io/repurposing-conventional-ultrasound-ai-heart-failure-screening/).
