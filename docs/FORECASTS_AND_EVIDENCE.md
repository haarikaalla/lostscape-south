# Forecasts and evidence statement

## Site-damage forecast

The implemented forecast measures **construction-pressure exposure**, not archaeological damage. It uses annual Dynamic World built probability averaged within a private 2-km buffer around each documented site for 2016–2025. Exact sites and time series remain private; public rankings aggregate to hashed ~10-km cells.

The backtest uses 2016–2020 histories to predict 2020–2025 change and withholds each state in turn. It compares persistence, ordinary linear trend, robust Theil–Sen trend, and a nonlinear histogram-gradient-boosting model. Reported evidence includes state sample sizes, Spearman rank correlation, top-decile recall, MAE/RMSE, and 1,000-resample confidence intervals. The nonlinear model uses a separate state for conformal calibration.

The operational task is ranking the fastest-growing pressure, so the model-selection metric is predeclared as weighted top-decile recall. The robust Theil–Sen trend is selected for the 2025–2030 screen because it has the highest value (0.3644). Persistence has the best MAE (0.01213), proving that exact change magnitude has no demonstrated forecasting skill. Therefore the output is a weak ranking screen, not a calibrated damage forecast. A 2035 forecast is withheld because recursive ten-year extrapolation has not been backtested.

The score is not the probability that a site will be damaged. It omits permitting, planned construction, legal protection, site condition, causal attribution, and field verification. Quarry pressure is unavailable because the quarry classifier has not passed the required 100-cell visual validation. Weak or negative backtests remain in the release.

## Survey blind spots

Blind spots are generalized cells with high lower-bound archaeological probability and low predicted documentation propensity. A five-seed random-forest effort model is evaluated by leave-one-state-out transfer using terrain, land cover, rainfall, built probability and observation proxies. The ranking multiplies the archaeological lower 90% score by one minus out-of-state documentation propensity. The top-50 lists are stable across seeds (mean pairwise Jaccard 0.905–0.976), but effort-model discrimination is weak overall (weighted ROC-AUC 0.5766).

Documentation propensity is not measured survey coverage. A zero record count can mean no survey, unpublished survey, missing digitization, language/access barriers, or true absence. Road and settlement-distance features are unavailable, so the correction remains incomplete.

## Evidence levels

- Level 1: model output only.
- Level 2: model output plus independent historical evidence not used for training.
- Level 3: expert review.
- Level 4: field verification.

Current public candidates are Level 1. No forecast or ranking raises evidence level.
