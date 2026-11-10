# Data sources

Access date for Phase 1 sources: **2026-11-10**.

| Dataset | Exact source | Coverage/date range | License / terms | Use |
|---|---|---|---|---|
| OpenStreetMap | Overpass API, `https://overpass-api.de/api/interpreter` | Current database snapshot at access time | ODbL 1.0; attribution required | Archaeological sites, megaliths, tombs, ruins, forts, quarries |
| Wikidata | SPARQL endpoint, `https://query.wikidata.org/sparql` | Current statements at access time | CC0 1.0 | Archaeological/heritage items with coordinates and metadata |
| geoBoundaries | API and `gbOpen` India ADM1 | Current release returned by API | CC BY 4.0 | State boundaries and spatial validation |
| ASI/Bhuvan monument coordinate compilation | `prachatos/asi-wikidata`, `monuments_min.csv`, derived from ASI WLM 2018 and Bhuvan | 2018 compilation; accessed 2026-11-10 | Repository MIT license; upstream ASI/Bhuvan attribution retained | Centrally protected monument inventory and coordinate enrichment |
| ASI centrally protected monuments list | `https://asi.nic.in/pdf/CPM_List.pdf` | Published 2025; accessed 2026-11-10 | Government information; source attribution retained | Official names, localities, districts and protection status validation |
| Tamil Nadu Department of Archaeology | Excavation and district-wise monument pages at `tnarch.gov.in` | Page contents available 2026-11-10 | Government information; source attribution retained | Cross-check of excavation type/year and state-protected sites |
| Kerala Department of Archaeology | 2023 centrally protected monuments PDF | 2023; accessed 2026-11-10 | Government information; source attribution retained | Cross-check of prehistoric umbrella stones and burial caves |

Raw API responses and exact queries are cached locally. Precise point data are placed only in gitignored `data/private/`. Public releases use aggregated 10 km cells.

