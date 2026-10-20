# WP-XXX: <title>

status: PLANNED | READY | IN_PROGRESS | BUILT | VERIFIED | INTEGRATION_READY | INTEGRATED | DONE | BLOCKED
owner:
timebox:
issue_ref:
governance_level: L1 | L2 | L3
affected_surface:
scope_kind: behavior | scaffold | design | investigation
verification_contract: v1 # enabled by default for new WPs; old packs are compatible
integration_required: true | false # true for critical cross-layer business flows
integrator:
change:
branch_or_worktree:
base_branch:
baseline_sha:
final_sha:
pr:

## Goal

## Done Condition

## Dependencies / Blockers

- prerequisite WPs/PRs:
- merge-before / merge-after constraints:

## Change Propagation (if applicable)

- propagation_from / changed truth:
- affected_consumers:
- propagation_state:
- migration_wave:
- target_contract/schema/version/baseline:
- stale downstream baseline handling:

## Parallelism / Integration

- parallel_safe_with:
- write-set overlap / shared hotspots:
- owned contracts/schema/migrations:
- integration order:
- handoff target:

## Read Set

- Specs:
- LLDs:
- Contracts/Schemas:
- Existing code/patterns:

## Expected Write Set

- modules/files:
- contracts/schema/migrations:
- tests/evals:
- docs/specs to synchronize:

## Invariants / Forbidden Changes

## Existing Capability & Asset Audit

- Repo/commit, real module/API/producer/consumer/schema authority and tested behavior:
- Capability gap (implemented / partial / missing / out-of-scope):
- Reuse/adopt/build decision + concrete library/source, rationale, adaptation, owner:

## Behavioral Acceptance

One row per critical behavior. Use stable case IDs (e.g. `CASE-001`). Expectations MUST come from the owning product/contract authority, not the output of the code being developed.

| Case ID | Preconditions / Input | Action | Expected Observable Result | Verification Seam / Command | Owner | Boundary (REAL/MOCKED/MIXED) |
|---|---|---|---|---|---|---|
| CASE-001 | ... | ... | ... | ... | ... | REAL |

## Execution Evidence

Required to claim `VERIFIED`, `INTEGRATION_READY`, `INTEGRATED` or `DONE`; never at `READY`. Evidence paths/URLs are locators, not proof that assertions are correct.

| Case ID | Command | Result (PASS/FAIL/NOT_RUN/BLOCKED) | Evidence Path / URL | Code SHA | Environment | Boundary (REAL/MOCKED/MIXED) |
|---|---|---|---|---|---|---|

## Implementation Obligations

## Test / Eval Commands

## Review Lenses

## Rollback / Recovery Notes

## Evidence

- commands run:
- results:
- PR/SHA:
- dependency SHAs/PRs used:
- base/current-target verification:
- reviewer/integrator verdict:
- screenshots/runtime evidence if applicable:

## Convergence

- Current Truth updated:
- Spec/LLD updated:
- Native Truth updated:
- Drift remaining:
- verdict: PASS | CONCERNS | FAIL
