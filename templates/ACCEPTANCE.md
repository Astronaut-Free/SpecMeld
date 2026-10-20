<!-- sps:readiness=DRAFT -->
# Acceptance / Traceability

status: DRAFT | ACTIVE | CONVERGED
owner:

| Requirement / Acceptance | Source | Spec / Contract | Work Packet | Test / Eval | Evidence | Status |
|---|---|---|---|---|---|---|

## Executable Behavioral Cases (for applicable business work)

Each case must trace to an owner-approved requirement/contract, a WP, an observable expected result and a test seam. No test oracle may be inferred from the implementing code.

| Case ID | Authority / Source | WP | Preconditions / Input | Action | Expected Observable Result | Test Seam / Command | Boundary | Owner | Execution Evidence / SHA |
|---|---|---|---|---|---|---|---|---|---|

**READY:** plan and oracle available; tests may be scheduled for implementation. **VERIFIED:** required cases have actually run, with run environment, code SHA, test result, evidence locator and real/mock scope. **INTEGRATED:** required end-to-end path rerun against integrated SHA. Skeleton-only, async accepted vs completed, legitimate empty vs unexpected empty, and mock-only vs real wiring must not be conflated.

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
