# Research-readiness audit

This audit evaluates whether the repository supports a strong remote-sensing/ML research submission. It does not claim acceptance by any journal and is not manuscript text.

## Evidence already complete

| Requirement | Status | Traceable evidence |
|---|---|---|
| Four-state open inventory with privacy protection | Complete, state-imbalanced | `results/tables/label_counts.csv`, `results/tables/label_gate.json` |
| Multi-sensor coarse Earth-observation features | Complete | `results/tables/gee_observation_qa.csv`, `docs/DATA_SOURCES.md` |
| Spatial/state transfer evaluation with fixed seeds | Complete | `results/tables/baseline_spatial_cv.csv` |
| PU learning, calibration, uncertainty, conformal audit | Complete; PU and conformal results are negative/weak | `results/tables/lostscape_pu_spatial_cv.csv`, `results/tables/conformal_coverage.csv` |
| Ablations and sanity controls | Complete at coarse scale | `results/tables/ablations.csv`, `results/tables/sanity_checks.csv` |
| Known-city and dense-cluster withholding | Complete retrospectively | `results/tables/hampi_withheld_case.csv`, `results/tables/pseudo_discovery_summary.csv` |
| Survey-bias and blind-spot screening | Complete but weak | `results/tables/survey_effort_model_cv.csv` |
| Construction-pressure backtest | Complete; useful only for weak ranking | `results/tables/site_damage_forecast_model_comparison.csv` |
| Reproducible public-safe code, tests and CI | Complete | `.github/workflows/ci.yml`, `tests/`, `scripts/run_all.sh` |

## Evidence that remains incomplete

| Gap | Why it matters | Minimum completion standard |
|---|---|---|
| Fine 10-m patches and CNN/nnPU comparison | Coarse cells cannot resolve archaeological morphology | Leakage-safe patch export, identical splits, at least five seeds, full baseline comparison |
| Independent expert review | Model rank is not archaeological identification | Blinded review of real chips, controls, inter-rater agreement and precision at k |
| Prospective field validation | Retrospective recovery can overestimate operational value | Freeze candidates before permitted survey; report every visited cell and outcome |
| Validated quarry-change labels | Bare ground is not equivalent to quarrying or damage | At least 100 independently checked cells and temporal backtest |
| Protected-area polygons | Point protection flags cannot measure spatial gaps | Licensed authoritative boundaries and documented overlay rules |
| Geology transfer | Lithology may dominate megalith preservation/detectability | Licensed lithology layer and leave-one-geology-out evaluation |
| Historical/CORONA convergence | Independent historical support is absent | Authenticated acquisition, georeferencing residuals, blinded feature protocol |
| Discovery-year temporal holdout | Current labels have no defensible dates | Source-backed documentation years with adequate pre/post sample size |

## Defensible contribution now

The present contribution is a reproducible, privacy-safe evaluation framework that exposes how coarse archaeological susceptibility models behave under state transfer, label incompleteness, spatial autocorrelation, calibration checks, bias correction, withheld known landscapes, and conservation-pressure backtesting. It demonstrates both limited retrospective cluster-recovery value and important failures. It does not yet provide the independent validation required for a prospective archaeological-discovery claim.

## Claim policy

Every quantitative claim must cite a tracked file under `results/`. Historical statements require an authoritative source. Candidate identity, chronology, cultural affiliation, and physical condition are unavailable until independently verified. No journal tier, impact, acceptance, or discovery is claimed.
