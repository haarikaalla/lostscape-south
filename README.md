# LostScape-South

LostScape-South is a reproducible remote-sensing and positive-unlabeled learning framework for ranking **candidates for archaeological field verification** across Karnataka, Andhra Pradesh, Tamil Nadu, and Kerala. It integrates open site inventories, multi-sensor Earth observation, calibrated uncertainty, survey-bias analysis, and conservation risk. It does not claim discovery, and public products generalize unprotected locations to coarse cells.

## Current status

Phase 1 inventory is complete. Phase 2 Earth Engine feature exports are running. Model results are not yet available and no performance claim is made. See `docs/progress.md` and `results/tables/label_gate.json`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
earthengine authenticate
make test
```

Set `gee.project` in `config.yaml` to a registered noncommercial Earth Engine project. Run resumable stages with `make inventory`, `make gee-submit`, and `make gee-status`.

## Data and ethics

Precise archaeological coordinates and raw responses are gitignored. Public files contain only generalized aggregates. Candidate rankings require archaeologist review and field verification. Do not use this project to locate objects for collection, excavation, tourism promotion, or enforcement without heritage-authority involvement. See `docs/ETHICS.md`, `DATASHEET.md`, and `MODEL_CARD.md`.

## License

Code is MIT licensed. Source datasets retain their original licenses and attribution requirements.

