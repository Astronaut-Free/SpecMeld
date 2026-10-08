<!-- sps:readiness=READY -->
# System Current Truth — Legal Consult Mini App

## Architecture Drivers
Privacy boundary, advisory-only AI semantics, mini-program platform review, weak-network behavior, and provider outage isolation drive the design.

## Solution Strategy
Use a mini-program client, a small API service, relational authoritative session storage, and an asynchronous AI Q&A module. Keep payment outside V1 until business scope, compliance, refund, and reconciliation rules are approved.

## Building Blocks
- Mini-program client: consent, question, result, callback request, history.
- API: session creation/read and callback request.
- AI Q&A module: bounded answer generation and fallback classification.
- Security boundary: authenticated user access, role-scoped operations, audit metadata.

## Data / Integration
`contracts/openapi.yaml` is the API contract. AI behavior is governed by `docs/engineering/specs/AI_QA.md`. Platform lifecycle constraints are in `MOBILE_MINI_PROGRAM.md`.

## Conditional Domains
Compliance is applicable now: consent, privacy, retention, auditability, and non-lawyer AI positioning are design inputs. Payments are DEFERRED with Product Owner ownership; trigger is payment collection entering scope; target is a dedicated payment/compliance design gate before implementation.

## Failure Behavior
Model or network failure must not discard a created consult session. Retry is idempotent by client request id. Unsupported AI output becomes a human-follow-up state.
