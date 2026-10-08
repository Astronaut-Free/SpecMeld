<!-- sps:readiness=READY -->
# Delivery Current Truth — Knowledge Graph Atlas

## Source Control
Local worktrees are acceptable; changes still use isolated branches and an explicit integration review before main.

## Verification
Run schema checks, fixture ingestion, lineage assertions, entity-resolution regression, and deterministic projection rebuild. Projection performance tests are separate from canonical correctness tests.

## Migration
Canonical schema changes use additive migrations first. Projection changes build a new projection version, compare counts/lineage samples, then switch readers and retire the old projection.

## Recovery
Raw/evidence/canonical stores are backed up and restorable. Graph projection is rebuildable and is not a backup authority.
