# ADR-0001: Canonical Store and Graph Projection

status: Accepted
owner: Data Engineering Owner

## Context
The product needs evidence-heavy writes and provenance joins plus graph traversal for research views.

## Options Considered
| Option | Strengths | Costs / Risks | Exit |
|---|---|---|---|
| PostgreSQL only | one truth store, simple ops | recursive traversal may become expensive | add projection later |
| Graph DB as canonical | natural traversal | weaker fit for evidence/history ownership and higher lock-in | costly migration |
| PostgreSQL canonical + graph projection | strong evidence truth plus graph read model | two-store reconciliation | projection is rebuildable |

## Decision
Use PostgreSQL as canonical source of truth and a graph projection behind an adapter. The projection must be rebuildable from canonical/evidence state.

## Consequences / Trade-offs
We accept projection rebuild and consistency work to keep provenance semantics independent from graph-vendor storage choices.

## Reversibility
The graph provider can be replaced by rebuilding from canonical ids and relationships; application queries use an adapter boundary.
