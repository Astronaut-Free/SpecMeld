<!-- sps:readiness=READY -->
# Delivery Current Truth — Mini Ticket Triage

## Source Control
One work packet per branch. Pull request required before main merge. No force push to main.

## Definition of Done
Implementation, unit/integration tests, contract validation, AI golden-set eval, and affected truth/spec updates are complete.

## Test Strategy
Unit tests for rules, integration tests for DB/API, contract validation for OpenAPI, deterministic fixtures for provider failure, and golden examples for triage output.

## Release
Build one versioned application artifact and worker artifact from the same SHA. Apply additive DB migration before enabling worker. Verify create → pending → suggestion → confirm flow after deploy.

## Rollback
Application artifact can roll back while additive schema remains. Disable AI worker/provider route to fall back to manual review if model behavior regresses.
