# Cross-Module Change Propagation

## 1. Purpose

Prevent partial migrations where one module/contract moves to the new design while dependent consumers, tests, projections, docs or runtime paths remain on the old semantics.

This is a **lightweight event-driven mechanism**, not a mandatory new document set. Activate it only when a change crosses a module boundary or changes shared truth.

## 2. Activation triggers

Run propagation analysis when any change touches one or more of:

- public/shared API, event, webhook, protobuf or schema
- database schema or canonical/domain semantics used by multiple modules
- shared types/SDK/common libraries
- auth/permission/tenant boundary
- shared design/component contract
- queue/event topic semantics or workflow state
- search/vector/graph/read-model projection inputs
- external integration contract
- runtime/config/platform foundation used by downstream modules
- feature/path replacement, compatibility window, deprecation or retirement

Do not activate for a local implementation detail with no downstream consumer.

## 3. Change Impact Graph

Start from the changed authoritative truth and identify:

```text
Changed Truth / Contract
        ↓
Direct Consumers
        ↓
Indirect Consumers
        ↓
Affected Tests / Evals / Docs / Ops / Release Paths
```

For each node record:

- owner
- dependency edge / why affected
- current baseline/version
- target baseline/version
- compatibility mode
- required migration/work packet
- verification evidence

Dependency sources should prefer executable/native truth where possible: imports, API schemas, event subscriptions, DB ownership, code references, CI/test dependencies, deployment manifests and generated client bindings.

## 4. Propagation states

Every affected consumer must end in exactly one explicit state:

- `AFFECTED` — impact known, action not yet classified
- `MIGRATION_REQUIRED` — code/data/config/contract change required
- `COMPATIBLE_NO_CHANGE` — verified compatible; no implementation change needed
- `DEFERRED` — intentionally postponed with owner + trigger/deadline + compatibility protection
- `NOT_APPLICABLE` — examined and not actually dependent
- `WAIVED` — accepted exception with owner/risk/expiry/compensating control

Silence is not a state.

## 5. Migration Wave

Do not dispatch downstream work randomly. Build the minimum safe wave order from dependencies and compatibility. Typical pattern:

```text
0. Freeze/approve target semantics
1. Expand contract/schema/foundation
2. Make producer and consumers dual-compatible
3. Backfill / rebuild / replay / migrate data or projections
4. Switch reads/writes/traffic to the new path
5. Observe and verify
6. Deprecate old path
7. Contract/remove old path after Retirement Gate
```

Not every change needs every wave. Use the smallest sequence that preserves correctness and reversibility.

## 6. Work Packet compilation

When propagation is active, the Compiler must:

- create or update the impacted WP DAG
- make shared contract/schema/foundation work explicit and merge it before dependent WPs when required
- record `propagation_from`, `affected_consumers`, `migration_wave`, `target_version/baseline` in relevant WPs
- prevent parallel WPs from independently redefining the same shared truth
- mark old-baseline downstream WPs `BLOCKED` or `STALE` until refreshed

Do not create one WP per consumer if multiple low-risk consumers can be safely migrated together.

## 7. Cross-Module Convergence Gate

A propagation-aware Change cannot close until:

1. all direct and material indirect consumers are classified;
2. every `MIGRATION_REQUIRED` item is implemented or intentionally `DEFERRED/WAIVED`;
3. shared contracts/schema/migrations are on the approved target version;
4. affected unit/contract/integration/E2E/eval tests pass;
5. projections/caches/search/vector/graph/read models are rebuilt or proven compatible where applicable;
6. Current Truth / Specs / LLD / Native Truth are synchronized;
7. release/rollback/retirement sequencing is executable;
8. no dependent WP remains on an obsolete baseline without explicit compatibility protection.

Verdict: `PASS | CONCERNS | FAIL`.

## 8. GitHub / Multi-Agent interaction

- Contract/schema/foundation PRs are shared hotspots and have a single owner/integration order.
- Downstream Agents must refresh to the integrated target baseline before claiming `INTEGRATION_READY`.
- A merge conflict that changes public semantics is a design/propagation event, not a mechanical conflict.
- Post-merge integration checks must cover the combined dependency chain, not only each PR in isolation.

## 9. Brownfield / retirement

For existing systems, preserve legacy behavior until dependencies are known. Prefer additive migration:

`expand → compatible transition → switch → observe → retire`

Old paths are not removed merely because the new path works. Retirement requires proof that callers/data/jobs/config/clients no longer depend on the old path or have an accepted migration/waiver.
