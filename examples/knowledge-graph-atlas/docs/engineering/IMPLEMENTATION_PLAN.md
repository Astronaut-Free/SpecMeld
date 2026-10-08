<!-- sps:readiness=READY -->
# Implementation Plan

owner: Data Engineering Owner
baseline: greenfield

## Target State
A reproducible ingestion and canonicalization core with query projection clearly separated from truth.

## Dependency DAG
`WP-001`

## Delivery Strategy
Implement source registry, immutable raw/evidence lineage, canonical identity decisions and migration-safe schema first; graph projection follows the ADR boundary and remains rebuildable.
