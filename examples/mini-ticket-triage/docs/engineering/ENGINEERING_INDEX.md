<!-- sps:readiness=READY -->
# Engineering Pack Index

owner: Engineering Owner

## Engineering Specs
| ID | Path | Purpose | Owner | Artifact Status | Native Truth / Contract |
|---|---|---|---|---|---|
| AI-TRIAGE | `docs/engineering/specs/AI_TRIAGE.md` | AI inference boundary | Engineering Owner | APPROVED | model output contract |

## LLDs
| ID | Path | Component/Boundary | Depends on | Artifact Status |
|---|---|---|---|---|
| LLD-001 | `docs/engineering/lld/LLD-001_TRIAGE_FLOW.md` | ticket triage flow | AI-TRIAGE | APPROVED |

## Work Packets
| WP | Path | Goal | Dependencies | WP Status | Evidence |
|---|---|---|---|---|---|
| WP-001 | `docs/engineering/work/WP-001.md` | persistence/API | none | READY | pending |
| WP-002 | `docs/engineering/work/WP-002.md` | async AI triage | WP-001 | PLANNED | pending |

## Acceptance / Quality
| Artifact | Path | Coverage |
|---|---|---|
| Acceptance | `docs/engineering/acceptance/ACCEPTANCE.md` | product, API, AI, failure |

## Native Truth Inventory
| Domain | Authoritative path/system | Owner |
|---|---|---|
| API | `contracts/openapi.yaml` | Engineering Owner |
| DB | `schemas/001_create_ticket.sql` | Engineering Owner |
