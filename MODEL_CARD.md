# Model card: LostScape-South

## Status

Coarse research pilot. A public-safe generalized ensemble has been evaluated, but it is not a field-validated discovery model.

## Intended use

Rank coarse areas for archaeologist-led survey planning and conservation triage in the four configured South Indian states. Outputs are candidates for field verification, not discoveries or legal determinations.

## Out-of-scope use

Looting, excavation without permits, disclosure of precise unprotected locations, policing, land acquisition, automatic heritage designation, or replacement of archaeological expertise.

## Training data

Positive labels combine open OSM, Wikidata, and attributed ASI/Bhuvan sources. Unlabeled locations are not assumed negative. Exact provenance and counts are in `docs/DATA_SOURCES.md` and `results/tables/label_counts.csv`.

## Evaluation requirements

Spatial leave-one-block-out validation, state/ecozone transfer, temporal holdout where dates permit, calibration, conformal coverage, PU-aware estimates, shuffled-label and distance-only controls, at least five fixed seeds, bootstrap intervals, and paired comparison with the strongest baseline.

## Implemented model families

- Regularized logistic regression, random forest and histogram gradient boosting baselines.
- Positive–unlabeled random-forest bagging with ensemble uncertainty.
- Split-conformal sets and expected calibration error.
- Persistence, ordinary linear, robust Theil–Sen and nonlinear temporal-context construction-pressure benchmarks.
- Out-of-state random-forest documentation-propensity modelling.

## Validation results relevant to use

The main archaeological PU model did not beat the best baseline. Retrospective pseudo-discovery recovered dense withheld clusters better than random in PR-AUC (one-sided p=0.021), but top-10%-area recall improvement was not significant at 0.05 (p=0.076). Exact construction-change magnitude was best predicted by persistence; robust trend is retained only for weak priority ranking. Documentation-propensity transfer is weak (weighted ROC-AUC 0.577).

## Limitations

Severe geographic and survey bias; sparse primary labels outside Tamil Nadu; uncertain discovery dates; remote-sensing ambiguity under canopy and in disturbed landscapes; possible confusion with quarries, bunds, terraces, tanks, and rubble. These limitations prohibit autonomous site claims.

The main PU variant underperformed histogram gradient boosting. Conformal coverage missed its nominal target after 225-km blocking. No temporal discovery holdout, expert review, field verification, validated quarry classifier, protected-area polygon analysis, or fine-patch CNN result exists.

Pseudo-discovery selects dense multi-class known clusters and cannot establish performance for isolated or deeply buried sites. No prospective discovery, city, empire, chronology or cultural affiliation is inferred.

