# Results summary

Every numeric statement below points to a tracked file in `results/`. These are coarse pilot findings, not a manuscript and not claims of archaeological discovery.

## Supported findings

- Inventory: 1,465 coordinate-supported records and 174 primary megalithic records. The primary total passes the project threshold, but Karnataka, Andhra Pradesh and Kerala fail the per-block threshold. Source: `tables/label_counts.csv`, `tables/label_gate.json`.
- Coarse model table: 21,732 cells and 140 observed-positive cells (6 Andhra Pradesh, 6 Karnataka, 8 Kerala, 120 Tamil Nadu). Source: `tables/baseline_spatial_cv.csv`; construction is logged in `docs/progress.md`.
- Best baseline: histogram gradient boosting mean PR-AUC 0.03136 across 20 state/seed runs. Random forest reached 0.02575 and regularized logistic 0.01130. Source: `tables/baseline_spatial_cv.csv`.
- Main PU result: calibrated PU bagging mean PR-AUC 0.01502, ROC-AUC 0.63123 and ECE 0.03984. It did not beat histogram gradient boosting; paired Wilcoxon p=0.26110 and mean difference -0.01634. Sources: `tables/lostscape_pu_spatial_cv.csv`, `tables/significance_tests.csv`.
- Conformal result: mean observed-label coverage 0.84622 at nominal 0.90, mean set size 0.87478; some calibration folds had zero positives. The target failed. Source: `tables/conformal_coverage.csv`.
- Autocorrelation: sampled empirical feature ranges were 87.5–212.5 km; final blocks are 225 km. Source: `tables/autocorrelation_ranges.csv`.
- Ablations: removing terrain reduced mean PR-AUC from 0.03136 to 0.01524; removing SAR slightly increased it to 0.03237. Source: `tables/ablations.csv`.
- Hampi holdout: with a 75-km train exclusion and 40-km test area, 30 known broad-inventory cells occurred in 208 test cells. Mean PR-AUC was 0.28389 and mean recall in the top 10% of area was 0.21333. Source: `tables/hampi_withheld_case.csv`.
- Landsat pilots: spectral trends and confidence intervals are in `tables/landsat_pilot_trends.csv`. These regional index trends do not count damaged or vanished archaeological features.
- Blind settlement tests are supported for one verified mound record in Andhra Pradesh, Karnataka and Tamil Nadu; Kerala is insufficient. Source: `tables/lost_settlement_holdouts.csv`, `tables/lost_settlement_holdout_limitations.csv`.
- Construction-pressure forecast: the all-state backtest rank correlation was 0.21403 and MAE 0.02465 (bootstrap 95% CI 0.02322–0.02624). State correlations ranged from -0.09465 to 0.44076, so predictive evidence is weak. Sources: `tables/site_damage_forecast_backtest.csv`, `tables/site_damage_forecast_scope.csv`.
- Survey blind spots: 50 generalized cells per state are ranked with an explicit documentation-density proxy. It is not measured survey effort. Sources: `tables/survey_blind_spots.csv`, `tables/survey_blind_spot_limitations.csv`.

## Unsupported or failed claims

- No temporal discovery holdout: zero primary labels have a defensible discovery year. Source: `tables/unavailable_experiments.csv`.
- No heritage-loss rate, validated quarry-growth estimate, protected-site gap, geology transfer, expert-review precision, field verification, or multi-layer convergence significance. Sources: `tables/heritage_loss_availability.csv`, `tables/headline_unavailable_tests.csv`, `tables/unavailable_experiments.csv`.
- No zone has more than Evidence Level 1 because independent historical/route evidence is absent. Source: `tables/convergence_zones.csv`.
- Fine 10-m patches, CNN, nnPU, foundation-model comparison and dashboard are not complete.
- A separate tank model was skipped because only 18 tank records exist; burial cluster size was skipped because no reliable cluster-size labels exist.

## Manual work still required

- Authenticate to USGS EarthExplorer, inspect CORONA coverage/cloud, download only suitable existing public-domain frames, georeference them and document residual error.
- Obtain archaeologist reviews using real chips; do not use the current sheet until chips exist.
- Field-verify candidates and record outcomes.
- Approve and ingest a licensed protected-area polygon layer and an open lithology layer.
- Archive a reviewed public release on Zenodo and update `CITATION.cff` with the real DOI.
