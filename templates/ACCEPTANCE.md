<!-- sps:readiness=DRAFT -->
# Acceptance / Traceability

status: DRAFT | ACTIVE | CONVERGED
owner:

每条验收项使用稳定 ID（`AC-01`、`AC-02` …）。WP 通过 `acceptance_refs` 引用；doctor 会报告未知引用和未被任何 WP 覆盖的验收项。ID 一经发布不重用。

| ID | Requirement / Acceptance | Source | Spec / Contract | Work Packet | Test / Eval | Evidence | Status |
|---|---|---|---|---|---|---|---|

## Golden / Critical Flows

## Negative / Failure Cases

## Security / Privacy Cases

## Architecture Driver / NFR Cases

关键 scale/latency/availability/security/compatibility/deployment/recovery/cost 假设应映射到可执行测试、benchmark、review、演练或监控证据。

## Cross-Module Propagation Cases (if applicable)

| Affected consumer / path | Required target state | Migration / compatibility evidence | Test / runtime evidence | Status |
|---|---|---|---|---|

No cross-module Change is accepted while a material consumer remains silently unclassified or on an obsolete baseline without compatibility protection.

## Performance / Reliability Cases

## AI Eval Cases (if applicable)

## Remaining Gaps
