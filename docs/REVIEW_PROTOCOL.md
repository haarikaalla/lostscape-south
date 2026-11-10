# Expert review protocol

## Status

Protocol prepared; no reviews have been collected or simulated.

Reviewers receive a stratified, randomized set of generalized candidate identifiers with Sentinel-2 true colour, NDVI, and hillshade chips. The set includes top-ranked cells across states/ecozones and a blinded low-ranked control sample. Exact coordinates are shared only through an approved private channel when necessary.

The current coarse pilot sheet contains 40 high-ranked cells and 20 blinded low-ranked controls. Image chips are not yet attached because the completed export is a 5-km tabular sample rather than the required fine-resolution patch export. Review must not begin until real chips have been generated.

Fixed labels: **likely site**, **likely natural**, **likely modern disturbance**, **unclear**. Reviewers record confidence, visible cues, likely confounder, and whether field verification is recommended. They must not see model rank or control status.

Analysis reports precision at fixed budgets, class distribution, missing responses, and inter-rater agreement with confidence intervals. Reviewer identities may be pseudonymized. No consensus label is created without a documented adjudication rule.

After reviewers fill the sheet, run `python -m src.eval.review_analysis`. The script exits without producing results when no ratings exist; it never creates simulated reviews.

