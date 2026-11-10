# Decision log

## D001 — Public coordinate protection

**Date:** 2026-11-10  
**Decision:** Store source coordinates only under `data/private/`, which is gitignored. Public inventory products contain 10 km grid identifiers and aggregated counts, never exact point coordinates.  
**Reason:** Archaeological locations can create looting and disturbance risk. The public artifacts must remain useful for coverage assessment without exposing locations.

## D002 — Initial boundaries and blocks

**Date:** 2026-11-10  
**Decision:** Use geoBoundaries `gbOpen` ADM1 polygons for India and select Karnataka, Andhra Pradesh, Tamil Nadu, and Kerala. Treat states as provisional Phase-1 blocks only.  
**Reason:** Final modeling blocks must be set after label distribution and autocorrelation are observed. geoBoundaries provides an open, versioned boundary API.

## D003 — Inventory semantics

**Date:** 2026-11-10  
**Decision:** OSM and Wikidata records are evidence of documentation, not ground-truth absence/presence quality. Preserve source tags, map deterministically to broad classes, and report missing discovery years rather than infer them.  
**Reason:** Source coverage and tagging are heterogeneous and survey-biased.

## D004 — Stop at the label gate

**Date:** 2026-11-10
**Decision:** Do not begin Earth Engine feature export or model training with the current primary labels.
**Evidence:** The deduplicated open-source inventory contains 46 megalithic-burial records: Karnataka 1, Andhra Pradesh 1, Tamil Nadu 39, Kerala 5. The configured gate requires at least 100 total and 30 per provisional block.
**Reason:** Continuing would produce unstable spatial validation, misleading transfer claims, and poorly constrained PU estimates. Options requiring user choice are: merge defensible burial/archaeological classes; add approved public monument/inventory sources; widen the region; or treat Tamil Nadu as the primary study and Kerala as a qualitative case study.

## D005 — User-authorized hierarchical continuation across four states

**Date:** 2026-11-10
**Decision:** After the failed initial gate, the user authorized adding official/open inventories and proceeding while demonstrating value in all four states. Use two explicitly separated targets: (1) megalithic burial susceptibility where coordinate-supported labels permit quantitative modeling, and (2) broader archaeological-site potential across all four states. Treat sparse-state megalithic results as transfer or case-study evidence, not equally powered primary validation.
**Reason:** This preserves the primary scientific target without fabricating labels or silently merging unlike classes. State-specific sample sizes and uncertainty will remain visible in every result.

## D006 — Earth Engine project and stable DEM

**Date:** 2026-11-10
**Decision:** Use Earth Engine project `lostscape-south-123456`. Replace deprecated `COPERNICUS/DEM/GLO30` with `USGS/SRTMGL1_003` for the reproducible terrain baseline.
**Reason:** The Earth Engine API emitted a deprecation warning for the configured Copernicus collection during the live availability probe. SRTM is an allowed project source and avoids building new work on a deprecated asset.

## D007 — Coarse interactive QA scale

**Date:** 2026-11-10
**Decision:** Run the archive-wide state/season clear-observation diagnostic at 20 km, after the initial 5 km synchronous reduction exceeded three minutes. Preserve 10–30 m processing for tiled, resumable batch exports.
**Reason:** The QA statistic is a coverage diagnostic rather than a modeling feature. Coarsening it prevents an expensive interactive computation while retaining state and seasonal comparisons.

## D008 — Point-sampled archive QA

**Date:** 2026-11-10
**Decision:** Replace synchronous statewide raster reduction with 40 deterministic random interior sample points per state at 5 km evaluation scale.
**Reason:** Both 5 km and 20 km full-polygon reductions exceeded the interactive budget. Point sampling preserves an auditable state/season diagnostic while detailed rasters are produced later through tiled batch exports.

## D009 — Separate metadata and pixel-validity QA

**Date:** 2026-11-10
**Decision:** Use Sentinel-2 `CLOUDY_PIXEL_PERCENTAGE` only as a fast scene-level clear-observation proxy. Do not label it as pixel-validity percentage. Produce SCL-based valid-pixel QA through tiled batch exports.
**Reason:** Even the point-sampled count mosaic traversed the entire archive and exceeded the interactive budget. Separating the proxy from the definitive tiled product avoids misrepresenting metadata as pixel QA.

## D010 — Treat 5-km exports as a coarse pilot

**Date:** 2026-11-10
**Decision:** Use the completed 5-km state tables to validate ingestion, leakage controls, state transfer, and the experiment pipeline, but do not present them as the final archaeological candidate product.
**Reason:** A 5-km sample cannot resolve individual burials, tanks, or mounds. It is scientifically useful for regional susceptibility and pipeline validation only; final candidate ranking requires finer tiled features and patches.

## D011 — Preserve sparse-state results

**Date:** 2026-11-10
**Decision:** Retain all held-out state runs and report their low/unstable metrics. Do not pool away the imbalance or tune against held-out states.
**Evidence:** The coarse join produced 6, 6, 8, and 120 positive cells for Andhra Pradesh, Karnataka, Kerala, and Tamil Nadu respectively.
**Reason:** This directly exposes the open-inventory coverage limitation and prevents misleading generalization claims.

## D012 — Do not promote the coarse PU model as superior

**Date:** 2026-11-10
**Decision:** Report histogram gradient boosting as the stronger coarse pilot model and retain PU bagging as an evaluated, currently underperforming variant.
**Evidence:** After rerunning with final 225-km blocks, across 20 paired state/seed runs mean PR-AUC was 0.01502 for calibrated PU bagging and 0.03136 for histogram gradient boosting; paired Wilcoxon p=0.26110.
**Reason:** The project rules prohibit cherry-picking. PU assumptions and calibration are especially fragile under strong survey bias and sparse positives.

## D013 — Final coarse spatial block size

**Date:** 2026-11-10
**Decision:** Use 225-km spatial blocks for block-dependent coarse experiments.
**Evidence:** Sampled empirical 95%-sill ranges were 87.5 km for dry-season NDVI, 112.5 km for elevation, 137.5 km for rainfall, and 212.5 km for built probability.
**Reason:** Rounding the largest sampled range upward reduces leakage risk. It also exposes instability from very few calibration blocks, which is reported rather than hidden.

## D014 — Provisional threat proxy, not quarry detection

**Date:** 2026-11-10
**Decision:** Rank coarse conservation risk with a transparent proxy combining Dynamic World built probability, WorldCover cropland and bare-ground indicators. Label every output provisional.
**Reason:** The required multi-year quarry-growth classifier and 100-cell visual validation have not been completed. Calling the proxy a quarry layer or heritage-loss rate would overstate the evidence.

## D015 — Time-Machine pilots and source scope

**Date:** 2026-11-10
**Decision:** Pilot southern Chennai, Tirupati–Srikalahasti and the Thrissur belt. Use Landsat Collection 2 immediately; use CORONA only after authenticated frame inspection and georeferencing; do not download historical maps until item-specific reuse rights are verified.
**Reason:** These areas coincide with the strongest coarse provisional risk concentrations near documented megalithic records and represent contrasting development, dry-interior and humid-canopy conditions.

## D016 — Atlas evidence independence

**Date:** 2026-11-10
**Decision:** Assign only Evidence Level 1 to current Atlas zones and do not run a convergence randomization test.
**Reason:** Probability and settlement-scale satellite features share model inputs and are not independent. No verified historical-map/CORONA feature, paleo-route reconstruction, unlocated-place layer, expert review, or field verification is available.

## D017 — Forecast scope and release

**Date:** 2026-11-10
**Decision:** Release only generalized construction-pressure trends and label the forecast weak; do not call the score a probability of site damage.
**Evidence:** The all-state 2016–2020 to 2020–2025 backtest produced Spearman correlation 0.2140, with a negative result in Andhra Pradesh and near-zero result in Tamil Nadu.
**Reason:** Built-probability trends omit actual damage outcomes, planned development, protection, permits and quarry validation. Weak backtesting does not support a stronger claim.

## D018 — Skip optional tank and cluster-size models

**Date:** 2026-11-10
**Decision:** Do not train a separate ancient-water-system model from 18 tank records, and do not model burial cluster size.
**Reason:** The tank sample is too small for the required spatial evaluation and the inventory has no reliable cluster-size label.

