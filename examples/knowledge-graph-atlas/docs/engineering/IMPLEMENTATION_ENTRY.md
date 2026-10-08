<!-- sps:readiness=READY -->
# Coding Agent Implementation Entry

entry_state: READY
baseline_sha: greenfield
base_branch: main
current_wp: `docs/engineering/work/WP-001.md`
agent_model_tier: strong

## Mission
Implement the canonical evidence/provenance core before any graph-specific optimization becomes authoritative.

## Read First
1. `docs/engineering/work/WP-001.md`
2. `docs/engineering/specs/SOURCE_PROVENANCE_ENTITY_RESOLUTION.md`
3. `decisions/ADR-0001_GRAPH_STORAGE.md`
4. `schemas/001_graph_core.sql`

## Stop Conditions
Stop for any design that makes projection state authoritative, destroys raw evidence, or performs unreviewable fuzzy entity merges.
