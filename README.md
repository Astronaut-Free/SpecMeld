# SpecMeld

**English** | [简体中文](README.zh-CN.md)

> **Software Engineering Toolkit · From intent to reliable delivery.**

SpecMeld connects intent, product design, architecture, contracts, Coding Agent implementation, verification, release, and continuous evolution into one traceable engineering loop.

The project is currently released first as a **Claude Code / Coding Agent Skill**. Over time it can evolve into a CLI, engineering checker, and broader developer-tooling platform. For compatibility with existing installations and projects, the technical Skill ID remains `software-project-standardizer` throughout v1.x.

## What it solves

SpecMeld is not a template library for mass-producing engineering documents. It focuses on five things:

1. **Right-sized engineering** — choose engineering depth based on project scale, risk, and lifecycle stage;
2. **Execution-ready compilation** — turn sufficiently clarified requirements into an Engineering Pack that Coding Agents can execute directly;
3. **Evidence-driven gates** — keep “implemented”, “tested”, “integrated”, and “release-ready” as distinct evidence states;
4. **Continuous convergence** — keep Product / Design / Contracts / Code / Tests / Runtime aligned;
5. **Governance without bureaucracy** — apply strict controls to high-risk surfaces without forcing every feature through production-grade ceremony.

## Core capabilities

- Product / PRD / UX / Acceptance
- Business Capability Decomposition
- Solution Architecture / NFR / Technology Trade-off
- Data / API / Event / AI / Runtime / Infra / Security
- LLD / Contract / Schema / Migration
- Work Packet / Dependency DAG / Multi-Agent integration
- CI/CD / Release / Rollback / Operations / Handover
- Cross-Module Change Propagation
- Brownfield Reality Scan / Drift Repair
- **Design Authority & Physical Reality Audit**
- **Progressive Governance / Governance Right-Sizing**
- Version / Compatibility / Deprecation / Retirement

## Brand & compatibility

| Layer | Name |
|---|---|
| Project brand | **SpecMeld** |
| Chinese name | **构序** |
| Current Skill ID (v1.x) | `software-project-standardizer` |
| Recommended repo name | `specmeld` |
| Future CLI | `specmeld` |

The v1.x Skill ID is intentionally stable so existing installations, `PROJECT.toml` files, and automations do not break. Brand and technical identifier are decoupled in v1.x; changing the invocation ID later would be treated as a breaking change.

## Quick Start

```bash
python scripts/init_project.py ./my-project --name my-project --mode greenfield --profile standard --archetype web
python scripts/init_engineering_pack.py ./my-project
python scripts/doctor.py ./my-project
```

For Claude Code, place the `software-project-standardizer/` directory under:

```text
~/.claude/skills/software-project-standardizer/
```

On Windows this is typically:

```text
C:\Users\<you>\.claude\skills\software-project-standardizer\
```

A typical invocation is:

> Use software-project-standardizer (SpecMeld) to standardize the current project. Generate the smallest sufficient Engineering Pack based on its actual scale and risk.

## Nano profile

For a solo short-lived project:

```bash
python scripts/init_project.py ./weekend-tool --name weekend-tool --profile nano --archetype internal
python scripts/doctor.py ./weekend-tool
```

Nano keeps only `PROJECT.toml + docs/PROJECT.md` and skips the full Engineering Pack.

## Mature Brownfield / already-shipped projects

For a V1.0+ project already in production, do not re-template the whole repository. Use this sequence instead:

```text
Production / Repository Reality
→ Authority & Truth Audit
→ Drift / Gap Analysis
→ G0–G4 Lifecycle Assessment
→ Right-sized Engineering Compilation
→ Evolution Plan
→ READY Work Packets
```

For Brownfield L2/L3 critical surfaces, design work must first verify Physical Schema, Constraints, Grants, Runtime, Machine Contracts, Tests, and Transaction / Idempotency / Audit boundaries. When evidence conflicts, the Agent must not synthesize a convenient compromise; it must enter Drift / Authority Conflict / Controlled Amendment handling.

See `references/DESIGN_GOVERNANCE.md`.

## Progressive Governance

Governance strength is not globally fixed:

```text
L1 Development
ordinary feature / bug
→ branch + review + CI + tests

L2 Critical Surface
schema / migration / shared contract / core runtime / canonical
→ L1 + compatibility + migration + integration gate

L3 Production / Security
identity / permission / canonical authority / release control plane
→ L2 + explicit ownership + approval + audit + release controls
```

A blocked high-risk Gate should freeze only work that depends on it or writes to the same protected surface. Independent workstreams may continue.

See `references/GOVERNANCE.md`.

## What `doctor.py` proves — and what it does not

`doctor.py` is a **deterministic structural, stage, and governance checker**. A `PASS` does not prove business correctness, production readiness, or successful deployment.

It can check:

- PROJECT control plane / Coverage / owner / exception;
- Engineering Pack readiness;
- Brownfield baseline;
- secret leakage;
- Spec / WP owner fields;
- heuristic issues such as empty acceptance criteria, unverifiable Done Conditions, and ADRs without alternatives;
- documentation convergence drift;
- governance level and Brownfield L2/L3 design-reality audit state.

Business correctness still requires real tests, evals, reviews, and runtime evidence.

## Self-test

```bash
python -m py_compile scripts/*.py
python -m unittest discover -s tests -v
python scripts/doctor.py examples/mini-ticket-triage
python scripts/doctor.py examples/legal-consult-mini-app
python scripts/doctor.py examples/knowledge-graph-atlas
```

CI covers Linux / Windows and Python 3.11 / 3.13.

## Golden examples

- `examples/mini-ticket-triage/` — AI ticket triage;
- `examples/legal-consult-mini-app/` — legal consultation mini program;
- `examples/knowledge-graph-atlas/` — source provenance, lineage, entity resolution, and graph projection.

Examples constrain output quality. They do **not** imply a fixed number of files for every project.

## Project feedback loop

After a real project ends, only three classes of reusable learning should flow back into SpecMeld:

- **Repeatable Spec Pattern** — a pattern observed across multiple projects;
- **Blind Spot / Failure Mode** — a real cause of rework, incorrect behavior, or governance mismatch;
- **Invalid Rule** — an existing rule shown by evidence to be too heavy, redundant, or wrong.

If a finding can be checked deterministically, prefer `doctor.py + tests`. Otherwise capture it through the smallest appropriate reference or golden example. Do not create new global MUST rules from a single anecdote.

## Open source

SpecMeld uses the **MIT License**. See `CONTRIBUTING.md` for contribution guidance and `SECURITY.md` for security reporting.

The recommended public repository name is `specmeld`. Before publishing packages or registering a trademark, verify GitHub/npm/PyPI/name availability separately; repository-name availability, package-name availability, and trademark availability are different questions.
