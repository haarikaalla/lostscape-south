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

