# Case 01 — Greenfield: AI ticket triage

**Start:** empty directory.

**Prompt to the agent:**

> We're a 3-person support team. Customers submit tickets through a web form. We want an AI to suggest a category and priority, but a human agent always confirms or overrides it. If the AI provider is down, tickets must still be created. Postgres is fine. Internal users only, behind our SSO. Set this project up so a coding agent can start building.

**Good outcome (reference: `examples/mini-ticket-triage/`):**

- Persists the ticket before any model call; model failure → review state.
- Human confirmation is the only path to the final classification and is audited.
- A schema + public API WP is R2 with an independent approver, not R1.
- Every acceptance item maps to a WP; each active WP has an executable done check.
- Small: no separate microservice, no speculative specs.

**Applicable rubric items:** R1–R7, R9.
