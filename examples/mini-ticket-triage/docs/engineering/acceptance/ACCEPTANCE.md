<!-- sps:readiness=READY -->
# Acceptance / Traceability

owner: Product Owner

| ID | Requirement | Spec / Contract | Work Packet | Test / Eval | Evidence |
|---|---|---|---|---|---|
| AC-01 | Ticket creation survives AI outage | `docs/SYSTEM.md` | WP-001, WP-002 | provider-failure integration | required before Done |
| AC-02 | API request/response stable | `contracts/openapi.yaml` | WP-001 | contract test | required before Done |
| AC-03 | Low confidence routes to review | `docs/engineering/specs/AI_TRIAGE.md` | WP-002 | golden eval | required before Done |
| AC-04 | Human override is authoritative/audited | `docs/PRODUCT.md` | WP-002 | integration test | required before Done |
