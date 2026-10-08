<!-- sps:readiness=DRAFT -->
# Delivery Current Truth

## Ownership & Decision Rights

- Product owner:
- Engineering owner:
- Release owner:
- Operations owner:
- Approval boundaries:

## Working Agreement

- Communication / issue tracking:
- WIP / dependency rules:
- Escalation:

## Definition of Ready

## Definition of Done

## Source Control / Branch / Review

- Collaboration mode: single | multi-human | multi-agent | hybrid
- Branch/integration model:
- One-WP/one-branch-or-worktree rule:
- Branch naming:
- Required reviews/checks:
- CODEOWNERS / ownership boundaries (GitHub 专属，其他平台使用等价机制):
- Merge authority (human or designated Integrator):
- Merge queue policy (GitHub 专属，其他平台使用等价机制):
- Base-update policy before integration:
- Force-push policy:
- Destructive-action rules:

## Progressive Governance

- Project default governance: auto | L1 | L2 | L3
- L1 surface controls:
- L2 critical-surface controls:
- L3 production/security controls:
- Rules that are stage-gated rather than globally mandatory:
- How unrelated work continues when one protected surface is blocked:

## Parallel Work / Provider Integration

- Dependency DAG authority:
- Parallel-safe criteria:
- Shared-hotspot policy:
- Contract/schema ownership:
- Change/MR/PR dependency / merge-order rule:
- Integrator handoff contract:
- Post-merge integration checks:
- Main/default branch releasability rule:

## Issue Tracker Mapping

- WP `issue_ref` points to the provider issue/ticket when one exists; no tracker means leave it empty, do not invent an ID.
- Issue/ticket status never overrides WP evidence or Gate state.

## Test Strategy

## CI / Build / Artifact

- CI authoritative config:
- Required gates:
- Artifact identity/registry:

## CD / Environments / Promotion

- Environments:
- Promotion path:
- Config/secrets ownership:

## Cross-Module Change Propagation

- Impact-graph trigger:
- Shared truth / contract ownership:
- Migration-wave policy:
- Downstream baseline refresh rule:
- Propagation convergence / retirement gate:

## Release / Migration / Rollout

- Versioning:
- Release candidate:
- Migration sequencing:
- Feature flags / canary / blue-green:
- Post-deploy verification:

## Rollback / Recovery / Compensation

- Code/artifact:
- Config/flags:
- Schema/data:
- Infrastructure:
- External side effects:
- Kill switch:

## Operations / Support

- Monitoring/alerts:
- Runbook/on-call/support:
- Incident/postmortem:
- DR/restore drills:

## Documentation / Change Lifecycle

- Current Truth update trigger:
- Change/ADR trigger:
- Archive/EOL:

## Client Handover / Support Boundary

## Known Delivery Risks / Exceptions
