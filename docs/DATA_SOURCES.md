# Data sources

Access date for Phase 1 sources: **2026-11-10**.

| Dataset | Exact source | Coverage/date range | License / terms | Use |
|---|---|---|---|---|
| OpenStreetMap | Overpass API, `https://overpass-api.de/api/interpreter` | Current database snapshot at access time | ODbL 1.0; attribution required | Archaeological sites, megaliths, tombs, ruins, forts, quarries |
| Wikidata | SPARQL endpoint, `https://query.wikidata.org/sparql` | Current statements at access time | CC0 1.0 | Archaeological/heritage items with coordinates and metadata |
| geoBoundaries | API and `gbOpen` India ADM1 | Current release returned by API | CC BY 4.0 | State boundaries and spatial validation |

Raw API responses and exact queries are cached locally. Precise point data are placed only in gitignored `data/private/`. Public releases use aggregated 10 km cells.

