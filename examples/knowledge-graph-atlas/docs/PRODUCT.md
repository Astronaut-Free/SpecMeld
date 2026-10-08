<!-- sps:readiness=READY -->
# Product Current Truth — Knowledge Graph Atlas

## Problem & Users
Researchers need to navigate historical people, institutions, events, and claims while preserving where each claim came from and how entity merges were decided.

## Scope
Ingest selected public sources, preserve source/raw/evidence lineage, resolve entities with reviewable decisions, and project canonical relationships into a queryable graph. No claim is promoted solely because it appears in multiple low-quality copies.

## Core Flow
Register source → capture raw item → parse observation → attach evidence → resolve entity → promote canonical fact → project graph → inspect provenance.

## NFR / Architecture Drivers
Every canonical assertion must trace to evidence. Projection rebuild must be deterministic from canonical truth. Entity merge/split must be reversible through recorded decisions. Initial dataset target is millions, not billions, of edges.

## Acceptance Criteria
A researcher can trace any displayed relationship back to source evidence; a corrected entity decision propagates to the graph projection without rewriting original raw evidence; a full projection rebuild yields equivalent canonical identities and edge semantics.
