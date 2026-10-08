<!-- sps:readiness=READY -->
# Acceptance / Traceability

owner: Product Owner

| Requirement | Spec / Contract | WP | Verification | Evidence |
|---|---|---|---|---|
| Cross-user read is denied | SECURITY_PRIVACY | WP-001 | authorization integration test | required before Done |
| AI outage preserves consult | AI_QA | WP-001 | provider-failure test | required before Done |
| Weak-network retry is idempotent | MOBILE_MINI_PROGRAM + OpenAPI | WP-001 | duplicate-submit test | required before Done |
| Payment is not reachable in V1 | PRODUCT | WP-001 | route/surface review | required before Done |
