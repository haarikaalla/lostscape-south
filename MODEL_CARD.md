# Model card: LostScape-South

## Status

Development. No trained release model or validated performance claim exists yet.

## Intended use

Rank coarse areas for archaeologist-led survey planning and conservation triage in the four configured South Indian states. Outputs are candidates for field verification, not discoveries or legal determinations.

## Out-of-scope use

Looting, excavation without permits, disclosure of precise unprotected locations, policing, land acquisition, automatic heritage designation, or replacement of archaeological expertise.

## Training data

Positive labels combine open OSM, Wikidata, and attributed ASI/Bhuvan sources. Unlabeled locations are not assumed negative. Exact provenance and counts are in `docs/DATA_SOURCES.md` and `results/tables/label_counts.csv`.

## Evaluation requirements

Spatial leave-one-block-out validation, state/ecozone transfer, temporal holdout where dates permit, calibration, conformal coverage, PU-aware estimates, shuffled-label and distance-only controls, at least five fixed seeds, bootstrap intervals, and paired comparison with the strongest baseline.

## Limitations

Severe geographic and survey bias; sparse primary labels outside Tamil Nadu; uncertain discovery dates; remote-sensing ambiguity under canopy and in disturbed landscapes; possible confusion with quarries, bunds, terraces, tanks, and rubble. These limitations prohibit autonomous site claims.

