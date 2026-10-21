# Case 02 — Brownfield: contract change across modules

**Start:** a copy of `examples/mini-ticket-triage/` initialised as a git repository (`git init && git add . && git commit -m base`).

**Prompt to the agent:**

> Product wants agents to be able to archive a ticket. Archived tickets are hidden from the default list but still readable by ID. Plan and prepare the change; don't implement it yet.

**Good outcome:**

- Recognises a shared contract (OpenAPI) and schema change → a Change record and an R2 WP.
- New migration file, not an edit to `001_create_ticket.sql`.
- `docs/SYSTEM.md` / acceptance updated in the same change set; `doctor.py --changed-since HEAD` passes.
- Consumers of the list endpoint are identified, with a compatibility note for the default-list behavior change.
- No implementation code written.

**Applicable rubric items:** R2–R8.
