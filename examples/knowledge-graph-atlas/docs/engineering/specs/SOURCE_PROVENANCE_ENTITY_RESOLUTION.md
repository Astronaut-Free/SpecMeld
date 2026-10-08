# Source, Provenance & Entity Resolution Spec

status: APPROVED
owner: Data Engineering Owner

## Source Registry
Every source has stable id, source type, jurisdiction/context, fetch policy, observed timestamp semantics, and licensing/usage notes. Raw items never silently change source identity.

## Provenance / Lineage
Observation references raw item and parser version. Evidence references observation plus evidence span/location. Canonical assertions reference one or more evidence ids and the decision/version that promoted them. Graph edges reference canonical ids and projection version.

## Entity Resolution
Deterministic identifiers win when present. Fuzzy candidates are scored but not auto-merged above a business-risk threshold without review. Merge, split, alias and correction actions are append-only decisions with predecessor/successor links.

## Data Quality
Block orphan references, invalid source ids, impossible temporal intervals, duplicate canonical keys and unresolved high-risk merge collisions. Track completeness, duplicate rate, resolver precision/recall and projection-rebuild parity.

## Correction Propagation
A canonical correction marks affected projection rows stale, rebuilds them from current canonical truth, and preserves historical raw/evidence records unchanged.
