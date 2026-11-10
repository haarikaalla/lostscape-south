# LostScape-South

LostScape-South is a reproducible remote-sensing and positive-unlabeled learning framework for ranking **candidates for archaeological field verification** across Karnataka, Andhra Pradesh, Tamil Nadu, and Kerala. It integrates open site inventories, multi-sensor Earth observation, calibrated uncertainty, survey-bias analysis, and conservation risk. It does not claim discovery, and public products generalize unprotected locations to coarse cells.

## Current status

The public-safe coarse pilot is complete across all four states. It contains 21,732 5-km Earth Engine feature cells and 140 observed-positive cells after the protected spatial join. The strongest baseline mean PR-AUC was 0.0314; calibrated PU bagging reached 0.0150 and did not significantly beat it (paired Wilcoxon p=0.2611). Leakage-safe conformal coverage averaged 0.846 at a nominal 0.90 target and therefore failed. These are recovery metrics for documented cells, not evidence of discoveries. See `results/RESULTS_SUMMARY.md` and `docs/progress.md`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
earthengine authenticate
make test
```

Set `gee.project` in `config.yaml` to a registered noncommercial Earth Engine project. `make all` runs all locally available stages; private source tables remain gitignored and must be regenerated or supplied. Earth Engine stages are resumable with `make gee-submit` and `make gee-status`.

## Key outputs

- Generalized probability, uncertainty and provisional risk maps: `results/maps/`
- Five-seed spatial/state evaluation tables: `results/tables/`
- Result-led state profiles and negative findings: `results/state_profiles/HEADLINE_FINDINGS_ATLAS.md`
- Full traceability and unsupported claims: `results/RESULTS_SUMMARY.md`

## Data and ethics

Precise archaeological coordinates and raw responses are gitignored. Public files contain only generalized aggregates. Candidate rankings require archaeologist review and field verification. Do not use this project to locate objects for collection, excavation, tourism promotion, or enforcement without heritage-authority involvement. See `docs/ETHICS.md`, `DATASHEET.md`, and `MODEL_CARD.md`.

## License

Code is MIT licensed. Source datasets retain their original licenses and attribution requirements.

