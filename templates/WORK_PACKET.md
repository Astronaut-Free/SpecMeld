+++
# Machine-checked by scripts/doctor.py. Keep facts here; keep reasoning in the body below.
id = "WP-XXX"
title = ""
status = "PLANNED"        # PLANNED | READY | IN_PROGRESS | BUILT | VERIFIED | INTEGRATION_READY | INTEGRATED | DONE | BLOCKED
owner = ""
risk_level = "R1"         # R1 development | R2 critical surface | R3 production/security (references/GOVERNANCE.md)
affected_surface = []     # e.g. ["schema", "public api"]; doctor warns when the surface implies a higher risk_level
depends_on = []           # WP ids that must be integrated first; cycles and unknown ids fail G1
parallel_safe_with = []   # only when write_set is disjoint; overlap fails G1
read_set = []             # paths/globs that exist now or are written by a dependency
write_set = []            # paths/globs this WP may modify
acceptance_refs = []      # AC-xx ids from the acceptance artifact
checkpoints = []          # intermediate verifications; split the WP if unverified change would outgrow one review
issue_ref = ""
integrator = ""
change = ""

[done]
commands = []             # executable checks, e.g. "python -m pytest tests/contract -q"
artifacts = []            # verifiable outputs, e.g. "contracts/openapi.yaml"

[approval]
authored_by = ""          # who compiled this WP (agent or human)
approved_by = ""          # required for R2/R3 before READY; must differ from authored_by

[execution]
branch_or_worktree = ""
base_branch = ""
baseline_sha = ""
final_sha = ""
pr = ""
+++

# WP-XXX: <title>

## Goal

一到三句话：这个 WP 完成后系统多了什么能力、边界在哪里。

## Done Condition

解释 `[done]` 中命令/产物为什么足以证明完成；需要人工判断的部分写明由谁判断。

## Invariants / Forbidden Changes

## Implementation Obligations

## Change Propagation (only when shared truth changes)

- changed truth / contract:
- affected consumers and propagation state:
- migration wave:
- stale downstream baseline handling:

## Review Lenses

R1：self-check + CI；R2：独立 reviewer（不是作者）+ contract/migration review；R3：R2 + 人类批准与审计。

## Rollback / Recovery Notes

## Evidence

- commands run / results:
- PR / SHA:
- dependency SHAs/PRs used:
- reviewer / integrator verdict:
- runtime evidence (if applicable):
- NOT_RUN / BLOCKED_TOOLING (if any, with reason):

## Convergence

- Current Truth updated:
- Spec/LLD updated:
- Native Truth updated:
- Drift remaining:
- verdict: PASS | CONCERNS | FAIL
