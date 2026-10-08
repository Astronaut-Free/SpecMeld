<!-- sps:readiness=READY -->
# System Current Truth — Knowledge Graph Atlas

## Architecture Drivers
Provenance, reversible entity resolution, deterministic rebuild, moderate graph traversal, and separation of canonical truth from read-optimized projection drive the architecture.

## Solution Strategy
Use PostgreSQL as authoritative evidence/canonical store and a graph projection behind an adapter for relationship traversal. Do not make the graph database the only truth source. `ADR-0001` records the trade-off.

## Data Pipeline
`Source → Raw → Observation → Evidence → Canonical → Graph Projection`.

## Data Lineage
Each downstream record keeps stable upstream identifiers. Raw payloads are immutable; observation parsing is versioned; canonical promotion records evidence ids and resolver decision ids; projection edges record canonical ids and projection version.

## Data Quality
Reject orphan evidence, unknown source ids, invalid temporal intervals, duplicate canonical identifiers, and graph edges pointing to retired canonical ids. Entity resolution reports precision/recall on a reviewed fixture set before promotion changes.

## Native Truth
Relational schema: `schemas/001_graph_core.sql`. Source/provenance/entity rules: `docs/engineering/specs/SOURCE_PROVENANCE_ENTITY_RESOLUTION.md`.
