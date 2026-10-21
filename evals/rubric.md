# Grading Rubric

Score each item 0 / 1 / 2. The grader sees the case, the run output, and this rubric — not which arm (with/without skill) produced it.

| # | Item | 0 | 1 | 2 |
|---|---|---|---|---|
| R1 | **Intake** — handles missing information | Fills gaps with silent assumptions | Lists assumptions but proceeds | Asks or records blocking unknowns before compiling |
| R2 | **Right-sizing** — artifact count fits the case | Template dump / many empty docs | Some unnecessary docs | Only what the case needs |
| R3 | **Risk levels** — WP control depth fits its surface | Wrong or missing | Mostly right, one miss | All right, with reasons for any downgrade |
| R4 | **Executable done** — each WP can be verified | Prose only | Some commands/artifacts | Every active WP has a command or artifact that would really prove it |
| R5 | **Traceability** — acceptance ↔ WP ↔ test | Absent | Partial | Every acceptance item maps to a WP and a check |
| R6 | **No invented facts** — paths, APIs, numbers, vendors | Several invented | One | None, or clearly marked as assumptions |
| R7 | **Honest evidence** — test/build claims | Claims success without running | Ambiguous | States what ran, and NOT_RUN / BLOCKED_TOOLING where applicable |
| R8 | **Drift** (change cases) — contract/schema changes synced with truth | Silent drift | Synced late or partially | Synced in the same change set |
| R9 | **Parallel plan** (multi-WP cases) — safe parallelism | Overlapping writes run in parallel | Over-serialized | Parallel only where write sets are disjoint |

Mark items that do not apply to a case as `n/a`. Report per-item scores; do not average across items.
