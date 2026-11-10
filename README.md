# LostScape-South

LostScape-South is a reproducible remote-sensing and positive-unlabeled learning framework for ranking **candidates for archaeological field verification** across Karnataka, Andhra Pradesh, Tamil Nadu, and Kerala. It integrates open site inventories, multi-sensor Earth observation, calibrated uncertainty, survey-bias analysis, and conservation risk. It does not claim discovery, and public products generalize unprotected locations to coarse cells.

The practical goal is twofold: help archaeologists decide **where limited survey effort may be most informative**, and help heritage managers identify **which documented areas deserve pressure monitoring first**. The system separates archaeological opportunity from modern-development pressure and records when a sophisticated model fails to outperform a simple baseline.

## Current status

The public-safe coarse pilot is complete across all four states. It contains 21,732 5-km Earth Engine feature cells and 140 observed-positive cells after the protected spatial join. The strongest baseline mean PR-AUC was 0.0314; calibrated PU bagging reached 0.0150 and did not significantly beat it (paired Wilcoxon p=0.2611). Leakage-safe conformal coverage averaged 0.846 at a nominal 0.90 target and therefore failed. These are recovery metrics for documented cells, not evidence of discoveries. See `results/RESULTS_SUMMARY.md` and `docs/progress.md`.

## High-value outcomes

- **Field-verification portfolio:** ten generalized Level-1 candidate zones per state selected using a lower-bound archaeological score and out-of-state documentation propensity. These are not sites until independently reviewed and field-verified.
- **Known-site conservation portfolio:** generalized cells ranked by robust 2025–2030 construction-pressure trend around documented sites. Exact magnitude forecasting has no demonstrated skill over persistence; the ranking recovers 36.4% of the observed top-growth decile in state-holdout backtesting.
- **Survey-bias evidence:** the documentation-propensity model transfers only weakly (weighted ROC-AUC 0.577), but its top-50 lists are stable across seeds. This makes the output useful for designing validation surveys, not for claiming absence.
- **Blind validation:** Hampi/Vijayanagara was excluded with a 75-km training buffer. Recovery was modest (mean PR-AUC 0.284; mean recall 0.213 in the top 10% of test area), providing a realistic benchmark rather than a showcase-only success.
- **Retrospective pseudo-discovery:** twelve dense, multi-class known-site clusters were completely withheld with a 75-km buffer. Mean cluster PR-AUC improved from 0.228 for random ranking to 0.314 for the full model (paired one-sided Wilcoxon p=0.021). Top-10%-area recall improved from 0.103 to 0.223, but that result was weaker (p=0.076). This tests recovery of known clusters, not prospective discovery.
- **Negative results with value:** PU learning did not beat gradient boosting, conformal coverage missed target, SAR added no coarse-scale value, and exact damage-change magnitude was best predicted by persistence.

## What the project does not claim

LostScape-South has not discovered a lost city, empire, burial, tank, or settlement. Coarse remote-sensing susceptibility cannot establish archaeological identity, date, extent, cultural affiliation, or legal status. A real discovery claim requires independent imagery or historical convergence, expert assessment, permitted field verification, and authority review. The machine-readable claim register is `results/tables/candidate_claims_register.csv`.

Documented historical landscapes—including Vijayanagara/Hampi, the Chola monumental centres, Amaravati, and the Muziris heritage region—are included only as authoritative context or known-site validation cases. The model does not infer that any candidate belongs to those polities. See `docs/HISTORICAL_CONTEXT.md` and `results/tables/historical_context_scope.csv`.

## Training and evaluation algorithms

| Component | Algorithms | Purpose |
|---|---|---|
| Archaeological baselines | Regularized logistic regression (MaxEnt-style), random forest, histogram gradient boosting | Comparable state-transfer ranking baselines |
| Main incomplete-label model | Positive–unlabeled random-forest bagging with ensemble uncertainty and calibration | Avoid treating every unrecorded cell as a confirmed absence |
| Uncertainty | Seed ensembles, expected calibration error, spatial split-conformal prediction sets | Separate ranking from confidence and test nominal coverage |
| Spatial validation | Leave-one-state-out, 225-km blocks from empirical variograms, leave-one-land-cover-out, withheld known clusters | Reduce spatial leakage and test transfer |
| Construction pressure | Persistence, linear trend, robust Theil–Sen trend, temporal-context gradient boosting | Benchmark five-year built-pressure ranking before projecting 2025–2030 |
| Survey blind spots | Five-seed random-forest documentation-propensity model with out-of-state predictions | Down-rank well-documented cells and expose possible survey/digitization gaps |
| Interpretation | Ablations, shuffled-label control, distance-to-known-site baseline, failure diagnostics | Test whether apparent skill is plausible and useful |

## Requested module status

| Module | Status | Evidence boundary |
|---|---|---|
| Five-to-ten-year site-damage forecast | **Partially implemented** | Backtested 2025–2030 construction-pressure ranking; exact magnitude has no skill over persistence, 2035 is withheld, quarry and actual damage outcomes are unavailable |
| Survey blind spots | **Implemented, provisional** | Out-of-state documentation propensity, lower-bound archaeological score and seed-stability analysis; not measured survey coverage |
| Ancient tanks and canals | **Not modelled** | Only 18 ancient-tank records across four states; insufficient for spatial training/validation |
| Trade routes and river courses | **Not duplicated** | Remains in the Lost Settlements landscape design; no independent reconstructed route/paleo-river layer has yet been ingested |
| Burial cluster size | **Unavailable** | Inventory has subtype labels but no reliable cluster-size field |
| Discovery readiness | **Retrospectively tested** | Full model outperforms random PR-AUC on 12 withheld dense clusters; no prospective candidate is verified |

## Real-world use

- **Survey planning:** compare candidate cells at fixed area budgets and select diverse, low-documentation zones for archaeologist review.
- **Conservation triage:** screen documented-site regions for construction-pressure growth, then check planning records and current imagery before intervention.
- **Evidence-gap design:** identify states, land covers and site classes where new systematic survey would most improve the model.
- **Authority engagement:** provide generalized rankings and reproducible evidence without publicly exposing vulnerable coordinates.

The system should not choose excavation locations autonomously, determine legal protection, infer cultural affiliation, or replace field survey. Its strongest deliverable is a testable, privacy-safe allocation of attention.

## Research-design strengths

The project combines temporal backtesting, spatial transfer, autocorrelation-informed blocks, PU learning, calibration/conformal checks, ablations, negative controls, retrospective pseudo-discovery, explicit survey-bias modelling, and responsible coordinate generalization. Weak results are retained. This design is suitable for a rigorous remote-sensing/heritage research submission, but journal quality still requires fine-resolution patches, independent expert review, and prospective field validation.

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
- Generalized candidate and conservation portfolios: `results/tables/high_value_candidate_portfolio.csv`, `results/tables/high_value_conservation_portfolio.csv`
- Forecast and survey-bias benchmarks: `results/tables/site_damage_forecast_model_comparison.csv`, `results/tables/survey_effort_model_cv.csv`
- Retrospective discovery-readiness tests: `results/tables/pseudo_discovery_summary.csv`, `results/tables/pseudo_discovery_significance.csv`
- Full traceability and unsupported claims: `results/RESULTS_SUMMARY.md`
- Historical context separated from model inference: `docs/HISTORICAL_CONTEXT.md`
- Submission-strength evidence audit and remaining validation gaps: `docs/RESEARCH_READINESS_AUDIT.md`

## Data and ethics

Precise archaeological coordinates and raw responses are gitignored. Public files contain only generalized aggregates. Candidate rankings require archaeologist review and field verification. Do not use this project to locate objects for collection, excavation, tourism promotion, or enforcement without heritage-authority involvement. See `docs/ETHICS.md`, `DATASHEET.md`, and `MODEL_CARD.md`.

## License

Code is MIT licensed. Source datasets retain their original licenses and attribution requirements.

