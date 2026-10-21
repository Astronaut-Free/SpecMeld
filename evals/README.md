# Behavior Evals

Unit tests prove the tooling works. They do not prove that loading this skill makes an agent's output better. This folder is for that question.

The test is always a comparison: **the same agent, the same case, with and without the skill.** A rule that does not move a metric in its favor is a candidate for deletion, not a reason to add another rule.

## Protocol

1. Pick a case from `cases/`. Each case states the input, the starting repository (if any), and what a good outcome looks like.
2. Run it at least 3 times **with** the skill installed and 3 times **without** it (baseline). Use a fresh workspace per run. Record the model and harness version.
3. Save each run's resulting project under `runs/<case>/<with|without>-<n>/` (git-ignored).
4. Compute the machine metrics:

   ```bash
   python evals/score.py runs/01-greenfield-ticket-triage/*
   ```

5. Grade the judgment metrics with `rubric.md`. Use a grader that did not produce the run (another person, or a separate agent given only the rubric, the case and the output).
6. Record results in `results/<date>-<case>.md`: the table from `score.py`, the rubric scores, and a one-paragraph conclusion.

## What counts as an improvement

| Metric | Source | Better is |
|---|---|---|
| doctor verdict / issue count | `score.py` | PASS, fewer issues |
| files in engineering pack | `score.py` | fewer, for the same rubric score |
| AC coverage (ACs mapped to a WP) | `score.py` | higher |
| risk level matches surface | rubric | yes |
| invented facts (paths, APIs, numbers not in the input) | rubric | none |
| fabricated evidence (claims tests ran when they did not) | rubric | none |
| asks before guessing on underspecified input | rubric (case 03) | yes |
| implementation drift after one WP | rubric (case 02) | none silent |

Report the with/without difference per metric, not a single blended score. A skill that raises doc quality but doubles file count and token use should say so.

## When a rule changes

When you add, remove or tighten a rule in `SKILL.md` or a reference, re-run the affected cases and attach the result to the CHANGELOG entry. "Real project feedback" is a good reason to propose a rule; an eval result is the reason to keep it.
