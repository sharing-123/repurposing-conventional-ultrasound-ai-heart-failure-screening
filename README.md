# LIFES on Conventional Ultrasound — Transparency Hub

Companion repository for the manuscript *"Repurposing Conventional Primary Care
Ultrasound for Artificial Intelligence-Assisted Heart Failure Screening: A
Multicenter Implementation and Transfer Learning Study."*

Live site (after enabling GitHub Pages): `https://REPLACE_WITH_ORG.github.io/REPLACE_WITH_REPO/`

## What this repository is

This repository publishes the performance results reported in the manuscript
as raw, machine-readable data, together with the exact analysis code used to
turn those numbers into the interactive figures shown on the project site
(`docs/index.html`). Anyone can clone this repository, run the pipeline, and
reproduce every chart from scratch.

## What this repository is not

It is not a release of the patient-level imaging dataset or the LIFES model's
training code. Those are withheld for the reasons stated in `DATA_STATUS.md`.
Treat any placeholder marked `PENDING` in `data/results/` as exactly that —
a placeholder, not a result.

## Repository structure

```
data/results/          Result tables reported in the manuscript, as CSV
src/                    Analysis and visualization pipeline (Python)
docs/                   GitHub Pages site (landing page + generated figures)
DATA_STATUS.md          What is and is not included, and why
```

## Reproducing the figures

```bash
python -m venv .venv
source .venv/bin/activate        # .venv\Scripts\activate on Windows
pip install -r requirements.txt
cd src
python export_site.py
```

This regenerates every file in `docs/assets/figures/` directly from
`data/results/*.csv`.

## Citation

A full citation will be added once the manuscript is published. In the
meantime, please reference this repository directly if you build on the
analysis code.

## License

Code is released under the MIT License (see `LICENSE`). Site text and
figures are released under CC BY 4.0.
