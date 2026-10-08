# Security & Privacy Spec

status: APPROVED
owner: Engineering Owner

## Scope
Protect consult sessions, user identity, callback contact data, consent records, and operations access.

## Rules
Every session is user-scoped. Operations access is role-gated and auditable. Logs must exclude question text and callback contact values by default. Retention and deletion actions preserve minimum audit evidence required by policy.

## Verification
Authorization tests cover cross-user reads/writes, privileged operations, and audit events. Synthetic fixtures are used outside production.
