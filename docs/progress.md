# Progress log

## 2026-11-10 — Phase 0 started

- Created the reproducible repository skeleton and configuration.
- Detected Python 3.14.6, Docker 29.7.2, Git 2.55.0, Make, and GitHub CLI.
- GitHub CLI is installed but not authenticated; manual `gh auth login` is required.
- Earth Engine API was absent from the base environment; it is pinned in `requirements.txt`. Manual authentication will be required after installation.
- Verified that Wikidata is reachable. The Overpass status endpoint returned HTTP 406 to a HEAD-like probe; the inventory script uses the supported POST interface and records the response.
- No GitHub repository URL was available; it must be supplied before publication.

## 2026-11-10 — Phase 1 completed; label gate failed

- Queried OpenStreetMap through Overpass separately for Karnataka, Andhra Pradesh, Tamil Nadu, and Kerala; cached the exact queries and local responses.
- Queried Wikidata separately by state and cached the exact SPARQL queries and local responses.
- Used geoBoundaries `gbOpen` India ADM1 boundaries and corrected diacritic-normalized state names before spatial validation.
- Removed records outside the four-state region and deduplicated records within 250 m.
- Produced a private precise inventory (gitignored), a public 10 km cell aggregation, a traceable count table, and a public-safe coarse density map.
- Final deduplicated inventory: 1,140 records. Primary megalithic-burial labels: 46 total — Karnataka 1, Andhra Pradesh 1, Tamil Nadu 39, Kerala 5.
- **LABEL GATE FAILED:** fewer than 100 total primary positives and three provisional blocks have fewer than 30. Modeling is paused pending a user decision.
- Discovery/documentation year coverage is sparse and comes only from available Wikidata inception/date statements; OSM contributed no discovery years. No dates were inferred.
- GitHub remote recorded as `https://github.com/haarikaalla/lostscape-south`; GitHub CLI remains unauthenticated and nothing has been pushed.

## 2026-11-10 — Phase 1 enrichment and authorized continuation

- Added the MIT-licensed `prachatos/asi-wikidata` ASI/Bhuvan coordinate compilation and cross-checked the current official ASI protected-monument list.
- Corrected a caught-before-modeling classifier defect: word-boundary matching now prevents `cistern` from being mislabeled as `cist`.
- Enriched deduplicated inventory: 1,465 coordinate-supported records. Primary megalithic-burial labels: 174 total — Karnataka 5, Andhra Pradesh 4, Tamil Nadu 159, Kerala 6.
- The total-positive threshold now passes, but the per-state/provisional-block threshold still fails outside Tamil Nadu.
- Following explicit user direction to preserve value across all four states and proceed, adopted a hierarchical design: quantitative megalithic modeling where labels support it, a broader archaeological-potential model across all states, and clearly identified sparse-label transfer/case-study results for Karnataka, Andhra Pradesh, and Kerala.
- No locality-only government-list record is promoted to a spatial label unless a defensible coordinate source is available.

## 2026-11-10 — Phase 2 setup and Earth Engine registration

- Registered and verified Google Earth Engine project `lostscape-south-123456`; all configured imagery/climate/land-cover collections responded to live probes.
- Replaced the deprecated Copernicus DEM asset with `USGS/SRTMGL1_003`.
- Added a resumable state/season observation-QA module. Two synchronous full-archive reductions (5 km and 20 km) exceeded the interactive time budget and were cancelled safely; no paid exports or storage tasks were launched.
- Detailed QA remains pending conversion to tiled asynchronous exports. This phase is not marked complete.
- Added a tracked-file privacy scanner for private/raw paths, precise coordinate patterns, credentials and files larger than 10 MiB.

## 2026-11-10 — Phase 2 asynchronous exports submitted

- Submitted four state-tiled 5 km private feature-table exports and one combined scene-metadata QA export to the private Google Drive folder `lostscape_south_private`.
- Feature stack includes dry/post-monsoon Sentinel-2 NDVI, NDWI and EVI medians/variability and valid counts; Sentinel-1 VV/VH medians/variability; SRTM elevation/slope/aspect; CHIRPS rainfall; ESA WorldCover; Dynamic World built probability; and grid-centre coordinates.
- Task IDs are cached under `results/tasks/` and can be monitored with `scripts/gee_task_status.py`.
- These are coarse Tier-1 tabular features. Fine 10 m patches and time-series trend exports remain pending after this resource-safe validation run.

## 2026-11-10 — Phase 2 coarse feature ingestion completed; Phase 3 started

- Retrieved and validated all four completed private Earth Engine tables: 21,732 5-km cells (Andhra Pradesh 6,822; Karnataka 7,975; Kerala 1,594; Tamil Nadu 5,341), 28 columns each, with no missing exported values.
- Joined coordinate-supported megalithic inventory points to cells using the predeclared 3.6-km radius: 140 positive cells (6 Andhra Pradesh, 6 Karnataka, 8 Kerala, 120 Tamil Nadu). Exact coordinates and model tables remain gitignored.
- Ran 60 leave-one-state-out baseline evaluations (3 models x 4 held-out states x 5 seeds) with identical features and splits. Raw per-run results are in `results/tables/baseline_spatial_cv.csv`.
- Results confirm severe sparse-state uncertainty. Aggregate PR-AUC means were 0.0314 (histogram gradient boosting), 0.0257 (random forest), and 0.0113 (regularized logistic); these are observed-label metrics, not verified discovery precision.
- Fine patches, autocorrelation-based block finalization, PU variants, calibration/conformal evaluation, temporal holdout, and risk products remain pending. Phase 2 is complete only for the coarse tabular pilot, not the requested fine-resolution stack.

## 2026-11-10 — Phase 4 coarse PU, uncertainty and conformal experiments completed

- Ran PU bagging with spatially separated calibration blocks for five seeds and four held-out states (20 paired runs); saved raw metrics, uncertainty and private predictions.
- After finalizing 225-km blocks from the Phase-5 variograms and rerunning, coarse PU mean PR-AUC was 0.01502 versus 0.03136 for the best baseline (histogram gradient boosting). The paired Wilcoxon test was not significant (p=0.26110); LostScape-PU therefore does **not** outperform the baseline in this pilot.
- Observed-label split-conformal coverage averaged 0.84622 at nominal 0.90, with mean set size 0.87478. Some calibration folds contained zero positives. The conformal target therefore failed and is not valid evidence of coverage for undiscovered sites.
- Added shuffled-label controls and survey-efficiency tables/figures. Metrics count documented positive cells, not newly field-verified discoveries.

## 2026-11-10 — Phase 5 supported coarse experiments completed

- Sampled empirical feature variograms gave approximate 95%-sill ranges of 87.5–212.5 km; finalized the conservative spatial block size at 225 km and reran block-dependent experiments.
- Completed 120 five-seed ablation runs. Removing terrain caused the largest mean PR-AUC reduction (0.03136 to 0.01524); removing SAR slightly increased mean PR-AUC to 0.03237, so SAR added no demonstrated value at this coarse scale.
- Completed leave-one-WorldCover-class-out tests for five classes with at least five observed positives. These are land-cover transfer diagnostics, not independent discovery validation.
- Temporal holdout is not estimable: zero of 174 primary megalithic records have a defensible discovery/documentation year. Geology transfer remains unrun because no licensed lithology feature has yet been ingested.

## 2026-11-10 — Phase 6 coarse conservation and review products completed

- Trained a five-seed histogram-gradient-boosting ensemble on all coarse cells and generalized predictions to hashed ~10-km public cell identifiers.
- Produced probability, ensemble-uncertainty and provisional risk maps plus per-state top-risk tables. Risk uses only built-probability, cropland and bare-ground proxies; it is not a validated quarry-growth or heritage-loss product.
- Created a blinded 60-cell review sheet (40 high-ranked, 20 controls) and a non-simulating analysis script. Fine Sentinel-2/NDVI/hillshade chips remain pending fine-resolution exports, so expert review must not start yet.
- Protected-site gap analysis remains unavailable because no open protected-area polygon layer has been approved and ingested. Point protection status is not treated as an area boundary.

## 2026-11-10 — Phase 7 in progress: Hampi complete, historical exports complete

- Checked authoritative availability: USGS Landsat Collection 2 provides open Level-2 surface reflectance from 1982 onward. CORONA Declass-1 is public domain (1960–1972), but frames are not georeferenced, existing scans can be hundreds of megabytes, and EarthExplorer login is required.
- Completed a broader-inventory Hampi/Vijayanagara holdout: train cells within 75 km were excluded and 208 cells within 40 km formed the test area, containing 30 known inventory cells. Across five seeds, mean PR-AUC was 0.28390 and mean recall in the top 10% of area was 0.21333. This is modest recovery of documented cells, not discovery.
- Submitted and completed private Landsat five-year dry-season pressure-index exports for the approved Chennai-south, Tirupati–Srikalahasti and Thrissur pilots. The three CSVs are awaiting local retrieval from the private Drive folder before change rates can be computed.
- CORONA georeferencing and historical-map comparison remain pending EarthExplorer authentication, frame availability/quality review, and item-specific map rights checks.

## 2026-11-10 — Phase 7 Landsat analysis and lost-settlement holdouts

- Retrieved the three approved Landsat pilot tables directly into private storage and analysed eight five-year periods spanning 1985–2024. Results are spectral trends with 95% confidence intervals; they are not interpreted as counts of lost heritage features.
- The only pilot NDBI trend whose 95% interval excluded zero was Thrissur (+0.0311 per decade, 95% CI 0.0041 to 0.0581). Cross-sensor/compositing effects and regional averaging prevent causal attribution to built growth.
- Ran spatially buffered blind tests for verified settlement-mound records in Andhra Pradesh, Karnataka and Tamil Nadu. Kerala is marked insufficient data because the verified inventory contains no settlement-mound record. River-only comparison remains unavailable because river distance has not been ingested.

## 2026-11-10 — Headline Findings Atlas generated

- Generated result-led cross-state findings, four state profiles, coarse hotspot tables and Level-1 model-only candidate zones.
- No convergence randomization p-value was computed because no zone currently has two independent evidence layers. Historical, paleo-route and unlocated-place layers are absent; remote-sensing features already used by the model are not double-counted as independent evidence.
- Statewide pressure growth near known sites versus matched random controls and validated quarry growth remain explicitly unavailable.

