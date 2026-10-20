# Behavior-first Agent Evaluations (V1.2)

These are *evaluation scenarios*, not test evidence. Suite status: **NOT_RUN**. Do not report PASS without actual transcripts, exact repo snapshot and independent grading.

## Protocol

1. For each case, prepare a controlled, read-only or sandboxed repository snapshot reflecting the prompt. Fix model, budget, tool permissions and acceptance oracle in advance; use a fresh session and comparable context.
2. Run a baseline coding agent **without** SpecMeld, and another with SpecMeld, on the same task. Randomize order where practical; avoid telling the agent which failure to find.
3. Collect artifact outputs, commands, run evidence, code/contract references, blocking decisions, transcript and evaluator verdict. Track `NOT_RUN`, `BLOCKED_TOOLING`, `PASS`, `FAIL` and unknowns separately.
4. Have an independent reviewer verify each *expected observable behavior* and each *failure signal* from `scenarios.json`. A prompt-only answer is not proof of runtime correctness.
5. Compare omitted decisions/acceptance cases, false readiness/verified claims, unnecessary blocking, user follow-ups required, first-pass acceptance and rework rounds. Repeat noisy tasks before concluding effectiveness.

Do not leak customer or project information into public fixtures. For real applications use separately authorized anonymized repository snapshots. CI can only check fixture schema; real agent behavior evaluation must be run separately.
