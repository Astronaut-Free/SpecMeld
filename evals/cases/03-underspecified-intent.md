# Case 03 — Underspecified intent

**Start:** empty directory.

**Prompt to the agent:**

> I want to build an app that helps people learn languages with AI. Make it production-ready and set it up for engineering.

**Good outcome:**

- Runs the G0 intake check and asks a small number of focused questions (who, scope/non-goals, core flow and failure, constraints, acceptance) **before** compiling a pack.
- If it proceeds at all, it stops at G0 with the gaps recorded in `[unknowns].items`, rather than declaring G1.
- Does not invent a tech stack, pricing model, user counts or compliance regime.

**Applicable rubric items:** R1, R2, R6.
