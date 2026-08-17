<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2563eb,100:f97316&height=200&section=header&text=LIFES%20%C3%97%20Conventional%20Ultrasound&fontSize=38&fontColor=ffffff&fontAlignY=38&desc=AI-Assisted%20Heart%20Failure%20Screening%20on%20Primary%20Care%20Ultrasound&descAlignY=58&descSize=16&animation=fadeIn" width="100%" />

<a href="https://sharing-123.github.io/repurposing-conventional-ultrasound-ai-heart-failure-screening/">
<img src="https://readme-typing-svg.demolab.com?font=Inter&size=20&duration=2800&pause=900&color=F97316&center=true&vCenter=true&width=700&lines=Open+results.+Open+code.+Zero+black+boxes.;254+patients+%C2%B7+4+hospitals+%C2%B7+2+ultrasound+platforms;Every+chart+on+this+page+is+reproducible+from+CSV." alt="animated tagline" />
</a>

<br/>

[![View Live Site](https://img.shields.io/badge/live%20site-visit%20now-f97316?style=for-the-badge&logo=githubpages&logoColor=white)](https://sharing-123.github.io/repurposing-conventional-ultrasound-ai-heart-failure-screening/)
[![License: MIT](https://img.shields.io/badge/code%20license-MIT-2563eb?style=for-the-badge)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content%20license-CC%20BY%204.0-2563eb?style=for-the-badge)](#license)
[![Python](https://img.shields.io/badge/python-3.10%2B-2563eb?style=for-the-badge&logo=python&logoColor=white)](requirements.txt)
[![Plotly](https://img.shields.io/badge/plots-plotly-f97316?style=for-the-badge&logo=plotly&logoColor=white)](src/visualize.py)

</div>

<br/>

## About

Companion repository for the manuscript **"Repurposing Conventional Primary
Care Ultrasound for Artificial Intelligence-Assisted Heart Failure
Screening: A Multicenter Implementation and Transfer Learning Study."**

This repo answers one question honestly: *when the manuscript says AUROC was
0.777, where does that number actually come from?* Here. Clone it, run one
script, and every chart on the [live site][site] rebuilds itself from the
same CSV the manuscript's tables were built from.

<p align="center"><b><a href="#-table-of-contents">Jump to the table of contents ↓</a></b></p>

---

## 📑 Table of Contents

- [What's here, at a glance](#whats-here-at-a-glance)
- [Live site](#-live-site)
- [Key results](#-key-results)
- [Repository structure](#-repository-structure)
- [Reproducing the analysis](#-reproducing-the-analysis)
- [Data transparency statement](#-data-transparency-statement)
- [Study design, in brief](#-study-design-in-brief)
- [Citation](#-citation)
- [License](#-license)

---

## What's here, at a glance

| | |
|---|---|
| 🧪 **Study type** | Multicenter model-adaptation / implementation study |
| 👥 **Participants** | 254 adults, 4 tertiary hospitals in Indonesia |
| 🩺 **Task** | Binary HF detection + 3-class phenotyping (Normal / HFpEF / HFrEF) |
| 📷 **Platforms compared** | GE LOGIQ S7 (high-end) vs. Mindray DP-20 (low-end) |
| 🫀 **Views** | PLAX, A4C, A2C *(PSAX acquired, excluded from final analysis)* |
| 🔁 **Reproducibility** | 100% of charts regenerate from `data/results/*.csv` via `src/` |

---

## 🌐 Live Site

**→ [sharing-123.github.io/repurposing-conventional-ultrasound-ai-heart-failure-screening][site]**

An animated, interactive walkthrough of every result below — hover any
chart for the full metric breakdown per platform and view.

---

## 📊 Key Results

| Metric | High-end (GE LOGIQ S7) | Low-end (Mindray DP-20) |
|---|---|---|
| Binary AUROC — PLAX (best view) | **0.777** | 0.548 |
| Binary AUROC — A4C | 0.662 | 0.604 |
| Binary AUROC — A2C | 0.577 | 0.563 |
| Multiclass macro-AUROC — PLAX (best view) | **0.759** | 0.607 |
| Multiclass macro-AUROC — A4C | 0.608 | 0.516 |
| Multiclass macro-AUROC — A2C | 0.551 | 0.584 |

Full metrics (accuracy, PPV, sensitivity, F1, specificity, NPV, likelihood
ratios) are in [`data/results/`](data/results) and rendered interactively
in [`docs/assets/figures/`](docs/assets/figures).

---

## 🗂 Repository Structure

```text
.
├── data/results/                    Result tables from the manuscript, as CSV
│   ├── binary_classification_results.csv
│   ├── multiclass_classification_results.csv
│   └── baseline_characteristics_template.csv   (placeholder — see DATA_STATUS.md)
├── src/                              Analysis + visualization pipeline
│   ├── config.py                     Paths and shared constants
│   ├── data_loader.py                CSV → typed, ordered DataFrames
│   ├── metrics.py                    Derived comparisons (platform deltas, best view)
│   ├── visualize.py                  Plotly figure builders
│   └── export_site.py                Orchestrates the pipeline, writes docs/assets/figures/
├── docs/                              GitHub Pages site
│   ├── index.html                     Landing page (3D animated banner + embedded charts)
│   └── assets/                        CSS, JS (Three.js banner), generated figure HTML
├── DATA_STATUS.md                     What's real, what's a placeholder, and why
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ▶️ Reproducing the Analysis

```bash
git clone https://github.com/sharing-123/repurposing-conventional-ultrasound-ai-heart-failure-screening.git
cd repurposing-conventional-ultrasound-ai-heart-failure-screening

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd src
python export_site.py
```

This rewrites every file in `docs/assets/figures/` directly from
`data/results/*.csv`. Open `docs/index.html` locally afterward to confirm
the charts match — there is no hidden step between the CSV and the page.

---

## 🔍 Data Transparency Statement

**Included and real:** binary and multiclass performance tables, verified
against the manuscript's own AUROC figures before being committed.

**Included but not yet real:** `baseline_characteristics_template.csv` is
entirely `PENDING` — Table 1 of the manuscript is still being finalized
with the underlying patient dataset. Placeholders are placeholders, not
results.

**Not included, on purpose:** patient-level imaging data (participant
privacy, per the study's ethics approval), STARD flow-diagram counts (not
yet finalized), and the LIFES model's training pipeline and weights
(ongoing research property, outside the scope of this results-transparency
repository).

Full detail: [`DATA_STATUS.md`](DATA_STATUS.md).

---

## 🧬 Study Design, in Brief

- Multicenter model-adaptation study across four tertiary hospitals in Indonesia.
- The previously validated **LIFES** echocardiographic AI model was adapted
  to conventional convex ultrasound via transfer learning.
- Two ultrasound platforms compared head-to-head: a high-end and a low-end
  conventional convex system.
- Patient-level 70% / 15% / 15% split into training, validation, and testing.
- Reported per **TRIPOD+AI** where applicable.

Full methodology lives in the manuscript, not here — this repository is the
results and code appendix, not a substitute for the paper.

---

## 📖 Citation

A full citation will be added once the manuscript is published. In the
meantime, please cite this repository directly if you build on the analysis
code.

---

## 📄 License

Code is released under the [MIT License](LICENSE). Site text and figures
are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:f97316,100:2563eb&height=120&section=footer" width="100%" />
</div>

[site]: https://sharing-123.github.io/repurposing-conventional-ultrasound-ai-heart-failure-screening/
