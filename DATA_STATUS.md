# Data Status

This file exists so nobody has to guess what is real and what is a placeholder.

## Included and real

- `data/results/binary_classification_results.csv`
- `data/results/multiclass_classification_results.csv`

These reproduce Tables 2 and 3 of the manuscript exactly, and were cross-checked
against the manuscript's own AUROC figures before being committed here.

## Included but not yet real

- `data/results/baseline_characteristics_template.csv` — every cell reads
  `PENDING`. Table 1 of the manuscript is currently empty pending the
  underlying patient dataset; this file exists only so the repository
  structure is ready the moment real numbers are available. Do not treat
  `PENDING` as a result.

## Not included, and why

- **Patient-level imaging data.** Withheld to protect participant privacy,
  consistent with the ethics approval referenced in the manuscript.
- **STARD flow-diagram counts** (patients screened / excluded / included by
  reason). Not yet finalized in the source manuscript.
- **LIFES model weights and training pipeline.** Remain the authors' ongoing
  research property and are outside the scope of this results-transparency
  repository.

If you are the author finalizing this repository before publication, replace
every `PENDING` value with the real data, delete this note once resolved, and
update this file to reflect the final status.
