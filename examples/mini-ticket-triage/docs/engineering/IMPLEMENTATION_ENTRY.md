<!-- sps:readiness=READY -->
# Coding Agent Implementation Entry

entry_state: READY
baseline_sha: greenfield
base_branch: main
current_wp: `docs/engineering/work/WP-001.md`
agent_model_tier: standard

## Mission
Build the minimum ticket persistence/API first, then the async AI triage path without changing the advisory-only product rule.

## Read First
1. `docs/engineering/work/WP-001.md`
2. `docs/SYSTEM.md`
3. `contracts/openapi.yaml`
4. `schemas/001_create_ticket.sql`

## Execution Order
`WP-001 → WP-002`

## Stop & Escalate
Stop if implementation requires synchronous model calls on ticket creation, changes final human authority, breaks the API contract, or requires destructive schema changes.

## Required Evidence
Run unit/integration/contract tests for the current WP and record command/result/PR/SHA before moving on.
