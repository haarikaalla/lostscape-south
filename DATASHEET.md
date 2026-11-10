# Datasheet

## Dataset purpose

Support reproducible archaeological survey-prioritization research while protecting sensitive locations.

## Composition

Private precise inventory; public 10 km aggregates; open remote-sensing/context features; model-ready labeled and unlabeled samples; evaluation and risk outputs. Current public inventory has no exact coordinates.

## Collection and provenance

Every source, identifier, access date, license, and transformation is recorded in `docs/DATA_SOURCES.md`. Missing discovery years and protection status remain missing; they are never inferred.

## Preprocessing

State-boundary validation, 250 m proximity deduplication, deterministic class mapping, coarse public aggregation, cloud masking, seasonal composites, and spatial blocking. Coordinate-quality and source fields must survive transformations.

## Biases

Documentation reflects survey history, accessibility, settlement/road proximity, institutional priorities, language and digitization. Absence from the inventory is not evidence of archaeological absence.

## Distribution

Only coarse cells and derived non-sensitive products may be public. Precise locations, raw API responses, imagery chips revealing vulnerable sites, and private review materials remain excluded.

## Current sample sizes

The coarse feature pilot contains 21,732 cells and 140 observed-positive cells. State positive-cell counts are 6 Andhra Pradesh, 6 Karnataka, 8 Kerala, and 120 Tamil Nadu. These imbalances must accompany all transfer claims.

The verified inventory contains 18 ancient-tank records, which is insufficient for the requested separate water-system model. It has no reliable burial cluster-size field. Annual 2016–2025 built-probability histories cover 1,465 documented sites for construction-pressure benchmarking; these are exposure proxies, not damage labels.

