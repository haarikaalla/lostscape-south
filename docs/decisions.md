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

