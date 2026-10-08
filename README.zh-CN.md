# SpecMeld（构序）

[English](README.md) | **简体中文**

> **Software Engineering Toolkit · From intent to reliable delivery.**

SpecMeld 把需求、产品设计、架构、Contract、Coding Agent 实施、测试验证、发布和持续演进连接成一套可追溯的工程闭环。

当前仓库首先以 **Claude Code / Coding Agent Skill** 形态发布；长期可以扩展为 CLI、工程检查器和开发者工具。为了兼容已有安装与项目，v1.x 的技术 Skill ID 仍保留为 `software-project-standardizer`。

## 它解决什么

SpecMeld 不是“批量生成工程文档”的模板库。它主要解决五件事：

1. **Right-sized engineering**：按项目规模、风险和阶段决定需要多少工程资产；
2. **Execution-ready compilation**：把已讨论清楚的需求编译成 Coding Agent 可直接执行的 Engineering Pack；
3. **Evidence-driven gates**：把“写完了 / 测过了 / 集成了 / 可发布”分成不同证据状态；
4. **Continuous convergence**：保持 Product / Design / Contracts / Code / Tests / Runtime 同步；
5. **Governance without bureaucracy**：高风险 surface 严格治理，普通 feature 不套核电站级流程。

## 核心能力

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
| 中文名 | **构序** |
| Current Skill ID (v1.x) | `software-project-standardizer` |
| Recommended repo name | `specmeld` |
| Future CLI | `specmeld` |

保留旧 Skill ID 是为了避免 v1.x 用户、`PROJECT.toml` 和既有安装突然失效。品牌与技术标识在 v1.x 解耦；如果未来更改 invocation ID，会按 breaking change 处理。

## Quick Start

```bash
python scripts/init_project.py ./my-project --name my-project --mode greenfield --profile standard --archetype web
python scripts/init_engineering_pack.py ./my-project
python scripts/doctor.py ./my-project
```

Claude Code 安装示例：把仓库中的 `software-project-standardizer/` 目录放到：

```text
~/.claude/skills/software-project-standardizer/
```

Windows 通常对应：

```text
C:\Users\<you>\.claude\skills\software-project-standardizer\
```

调用时可以说：

> 使用 software-project-standardizer（SpecMeld）对当前项目做标准化，按项目规模和风险生成最小充分 Engineering Pack。

## Nano profile

单人短期小项目：

```bash
python scripts/init_project.py ./weekend-tool --name weekend-tool --profile nano --archetype internal
python scripts/doctor.py ./weekend-tool
```

Nano 只维护 `PROJECT.toml + docs/PROJECT.md`，不编译完整 Engineering Pack。

## Mature Brownfield / 已上线项目

V1.0+ 已上线项目不要重新套模板。推荐顺序：

```text
Production / Repository Reality
→ Authority & Truth Audit
→ Drift / Gap Analysis
→ G0–G4 Lifecycle Assessment
→ Right-sized Engineering Compilation
→ Evolution Plan
→ READY Work Packets
```

对 Brownfield 的 L2/L3 critical surface，设计前必须先核对 Physical Schema、Constraints、Grants、Runtime、Machine Contracts、Tests、Transaction / Idempotency / Audit 边界。遇到冲突时不得自行“综合一个合理方案”，而要进入 Drift / Authority Conflict / Controlled Amendment 流程。

详见 `references/DESIGN_GOVERNANCE.md`。

## Progressive Governance

治理强度不是全局固定值：

```text
L1 Development
普通 feature / bug
→ branch + review + CI + tests

L2 Critical Surface
schema / migration / shared contract / core runtime / canonical
→ L1 + compatibility + migration + integration gate

L3 Production / Security
identity / permission / canonical authority / release control plane
→ L2 + explicit ownership + approval + audit + release controls
```

一个高风险 Gate 被阻塞，只冻结依赖它或写同一受保护 surface 的工作；无依赖 workstream 可以继续。

详见 `references/GOVERNANCE.md`。

## Doctor 的边界

`doctor.py` 是**结构、声明阶段与确定性治理检查器**。`PASS` 不等于业务正确、生产可用或发布成功。

它可以检查：

- PROJECT control plane / Coverage / owner / exception；
- Engineering Pack readiness；
- Brownfield baseline；
- secret 泄漏；
- Spec / WP owner；
- 空验收、不可验证 Done Condition、ADR 无备选等启发式问题；
- 文档 convergence 漂移；
- governance level / Brownfield L2-L3 design reality audit 状态。

业务正确性仍由真实 tests/evals/review/runtime evidence 证明。

## Self-test

```bash
python -m py_compile scripts/*.py
python -m unittest discover -s tests -v
python scripts/doctor.py examples/mini-ticket-triage
python scripts/doctor.py examples/legal-consult-mini-app
python scripts/doctor.py examples/knowledge-graph-atlas
```

CI 同时覆盖 Linux / Windows 与 Python 3.11 / 3.13。

## Golden examples

- `examples/mini-ticket-triage/`：AI 工单分流；
- `examples/legal-consult-mini-app/`：法律咨询类小程序；
- `examples/knowledge-graph-atlas/`：来源、血缘、实体消解、图投影数据项目。

示例用于约束输出质量，不代表每个项目都必须生成同样数量的文件。

## 项目复盘反哺

真实项目结束后只沉淀三类东西：

- **Repeatable Spec Pattern**：跨多个项目重复出现；
- **Blind Spot / Failure Mode**：真实导致返工、错误或治理失配；
- **Invalid Rule**：被证据证明过重、重复或错误的旧规则。

能确定性检测的优先进入 doctor + tests；其余通过最小 reference / golden example 沉淀。不要因为一次个案就扩写全局 MUST。

## Open source

本项目使用 **MIT License**。贡献规则见 `CONTRIBUTING.md`，安全报告见 `SECURITY.md`。

首个公开仓库建议命名为 `specmeld`。发布前仍建议自行做 GitHub/npm/PyPI/商标等正式名称核验；仓库名可用、包名可用和商标可用是三件不同的事。
