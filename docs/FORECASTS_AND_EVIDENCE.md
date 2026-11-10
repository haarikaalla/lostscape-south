# Forecasts and evidence statement

## Site-damage forecast

The implemented forecast measures **construction-pressure exposure**, not archaeological damage. It uses annual Dynamic World built probability averaged within a private 2-km buffer around each documented site for 2016–2025. Exact sites and time series remain private; public rankings aggregate to hashed ~10-km cells.

The backtest fits a linear trend on 2016–2020 and predicts 2020–2025 change. Reported evidence includes state sample sizes, Spearman rank correlation, mean absolute error, and a 1,000-resample 95% bootstrap interval for MAE. The final 2030/2035 projection fits 2016–2025 and reports slope uncertainty. Linear extrapolation is clipped to the physical 0–1 range.

The score is not the probability that a site will be damaged. It omits permitting, planned construction, legal protection, site condition, causal attribution, and field verification. Quarry pressure is unavailable because the quarry classifier has not passed the required 100-cell visual validation. Weak or negative backtests remain in the release.

## Survey blind spots

Blind spots are generalized cells with high model probability and few records in the three open inventory sources. The effort proxy is the number of digitized records per cell, not measured survey effort. A zero can mean no survey, an unpublished survey, missing digitization, language/access barriers, or true absence. Road access and settlement-density effort features are not yet available.

## Evidence levels

- Level 1: model output only.
- Level 2: model output plus independent historical evidence not used for training.
- Level 3: expert review.
- Level 4: field verification.

Current public candidates are Level 1. No forecast or ranking raises evidence level.
