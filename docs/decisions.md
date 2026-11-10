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

