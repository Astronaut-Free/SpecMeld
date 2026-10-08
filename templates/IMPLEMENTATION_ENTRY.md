<!-- sps:readiness=DRAFT -->
# Coding Agent Implementation Entry

entry_state: NOT_READY | READY | BLOCKED
baseline_sha:
base_branch:
engineering_pack:
current_wp:
governance_level: L1 | L2 | L3
agent_model_tier: auto # economy | standard | strong | auto

## Mission

一句话说明当前工程目标和完成边界。

## Read First — 最小必读

1. `<WP path>`
2. `<linked spec/lld>`
3. `<contract/schema if needed>`

不要默认读取整个 `docs/`。

## Current Baseline

- Build command:
- Test command:
- Known baseline failures:
- Runtime/dev command:

## Execution Order / Dependency DAG

```text
WP-001 -> WP-002 -> {WP-003, WP-004} -> WP-005
```

### Cross-Module Propagation Plan (if applicable)

- changed shared truth / contract:
- active migration wave:
- stale/blocked downstream WPs:
- consumers allowed to continue under compatibility:
- propagation convergence condition:

### Parallel Execution Plan

- parallel-safe groups:
- serialized/shared-hotspot WPs:
- contract/schema-first WPs:
- designated Integrator:
- merge order / queue policy:

## Agent Model Tier Guidance

- mechanical/local WP: economy or standard model is acceptable when tests/contracts are strong.
- architecture, security, migration, cross-module/shared-contract WP: prefer strong model.
- `auto` means the orchestrator selects based on risk; model tier never relaxes the WP acceptance gate.

## Current Work Packet

- Path:
- Goal:
- Dependencies satisfied:

## Non-negotiable Constraints

- Contracts/invariants:
- Security/privacy:
- Compatibility:
- No-scope areas:

## Stop & Escalate When

停止 Coding 并先更新设计/决策，如果出现：

- approved requirement 无法按当前 design 实现
- public API/Event/Schema breaking change
- core data model / architecture boundary change
- implementation evidence invalidates an approved Architecture Driver / NFR / technology trade-off assumption
- migration becomes irreversible or rollback assumptions fail
- security/privacy boundary changes
- two specs/contracts contradict each other
- a shared-contract/schema/domain change reveals an unclassified downstream consumer or invalid migration order

## Review / Merge Rules

- Required tests/evals:
- Required review lenses:
- PR must link current WP/change:
- Dependency PRs must be integrated first:
- Required checks must be green against the current integration candidate:
- CODEOWNERS/ownership approvals where applicable:
- Merge authority: human or designated Integrator; implementer does not self-merge by default
- Merge queue / serialized integration rule:
- Post-merge integration verification:
- Force-push/destructive actions requiring approval:

## Evidence Destination

完成后把：commands/results/SHA/PR/eval/deploy evidence 写入当前 WP，并运行 Convergence。
