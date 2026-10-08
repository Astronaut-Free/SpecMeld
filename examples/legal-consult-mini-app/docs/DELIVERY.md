<!-- sps:readiness=READY -->
# Delivery Current Truth — Legal Consult Mini App

## Source Control
One WP per branch/worktree. Review is required before integration. Provider is GitHub in this example; equivalent mechanisms may be used elsewhere.

## Quality Gates
Run API contract tests, authorization tests, AI golden-set eval, duplicate-submit/weak-network tests, and mini-program device/review checklist before release candidate.

## Release
Use a mini-program gray release where supported and verify compatibility with the minimum supported client/runtime version. Backend changes stay backward compatible for the previous client during rollout.

## Rollback
Disable the AI route to human-review fallback if model quality regresses. Client rollback follows platform-supported version/release mechanisms; additive server schema remains compatible.
