<!-- sps:readiness=READY -->
# System Current Truth — Mini Ticket Triage

## Architecture Drivers
Small team, low concurrency, fast time-to-market, provider AI latency/failure isolation, and auditability of human override.

## Solution Strategy
Use a modular monolith API plus an async inference worker. PostgreSQL is the ticket source of truth. HTTP is used for user-facing commands/queries; a job boundary isolates model latency. No microservice split until independent scaling or ownership becomes real.

## Building Blocks
- API: ticket create/read/confirm endpoints.
- Worker: model request, validation, confidence threshold, fallback state.
- PostgreSQL: authoritative ticket and triage state.
- External model API: advisory classifier only.

## Data & Contract Truth
API contract: `contracts/openapi.yaml`. Database change: `schemas/001_create_ticket.sql`. AI behavior spec: `docs/engineering/specs/AI_TRIAGE.md`.

## Failure Behavior
Model timeout/error never rolls back ticket creation. Worker records `NEEDS_REVIEW`. Duplicate job execution must be idempotent by ticket id + analysis version.

## Security
Internal authenticated users only. Human override and final state changes must record actor and timestamp.
