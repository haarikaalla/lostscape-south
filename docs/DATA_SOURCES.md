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
| USGS Landsat Collection 2 | `https://www.usgs.gov/landsat-missions/landsat-collections` | Level-2 surface reflectance from 1982 onward; accessed 2026-11-10 | USGS no-cost open data | Approved historical-change source for pilot areas |
| USGS Declassified Satellite Imagery 1 (CORONA/ARGON/LANYARD) | `https://doi.org/10.5066/F78P5XZM` | 1960–1972; availability must be checked per frame in EarthExplorer | Public domain; existing digital files free, on-demand scans may cost money | Approved availability check; no frames downloaded yet |
| Stanford South Asian Studies map guide | `https://guides.library.stanford.edu/c.php?g=1325856&p=11218656` | Describes 1980s–1990s India 1:50,000 map scans; accessed 2026-11-10 | Item-specific rights must be checked before download/release | Historical-map discovery only; no map downloaded |
| UNESCO World Heritage Centre — Hampi | `https://whc.unesco.org/en/list/241/` | Authoritative property description; accessed 2026-11-10 | UNESCO web terms; attribution retained | Historical context and interpretation of the known-city holdout only |
| UNESCO World Heritage Centre — Great Living Chola Temples | `https://whc.unesco.org/en/list/250/` | Authoritative property description; accessed 2026-11-10 | UNESCO web terms; attribution retained | Historical context only; never used to assign candidate identity |
| Archaeological Survey of India — Amaravati Circle | `https://asi.nic.in/pages/Amaravati-Circle` | Official ASI institutional/site context; accessed 2026-11-10 | Government information; attribution retained | Historical context only |
| Government of Kerala — Muziris Heritage Project | `https://www.keralatourism.org/muziris/muziris-project` | Official heritage-project description; accessed 2026-11-10 | Government information; attribution retained | Historical context only; never used to localize or classify candidates |

Raw API responses and exact queries are cached locally. Precise point data are placed only in gitignored `data/private/`. Public releases use aggregated 10 km cells.

