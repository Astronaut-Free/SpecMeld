# LLD-001: Triage Flow

status: APPROVED
owner: Engineering Owner
governance_level: L2
authority_status: ALIGNED
physical_reality_audit: NOT_APPLICABLE

## Responsibility
Persist ticket first, enqueue triage, execute one idempotent analysis per ticket/version, store suggestion, allow human confirmation/override.

## State
`NEW → TRIAGE_PENDING → SUGGESTED | NEEDS_REVIEW → CONFIRMED`.

## Transactions
Ticket create transaction does not include model call. Suggestion write uses ticket id + analysis version uniqueness.

## Tests
Create succeeds during provider outage; duplicate job does not duplicate suggestion; low confidence routes to manual review; override records actor.
