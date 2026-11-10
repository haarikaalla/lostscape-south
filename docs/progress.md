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

