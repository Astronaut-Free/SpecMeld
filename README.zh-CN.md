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

## 安装

仓库根目录本身就是 skill。按 v1.x Skill ID 克隆到 skills 目录：

```bash
git clone https://github.com/Astronaut-Free/SpecMeld.git ~/.claude/skills/software-project-standardizer
```

Windows（PowerShell）：

```powershell
git clone https://github.com/Astronaut-Free/SpecMeld.git "$env:USERPROFILE\.claude\skills\software-project-standardizer"
```

需要 Python 3.11+，无第三方依赖。

## Quick Start

脚本在 skill 目录里（下文记作 `$SKILL`），不在你的项目里：

```bash
SKILL=~/.claude/skills/software-project-standardizer
python $SKILL/scripts/init_project.py ./my-project --name my-project --mode greenfield --profile standard --archetype web
python $SKILL/scripts/init_engineering_pack.py ./my-project
python $SKILL/scripts/doctor.py ./my-project
```

调用时可以说：

> 使用 software-project-standardizer（SpecMeld）对当前项目做标准化，按项目规模和风险生成最小充分 Engineering Pack。

## Nano profile

单人短期小项目：

```bash
python $SKILL/scripts/init_project.py ./weekend-tool --name weekend-tool --profile nano --archetype internal
python $SKILL/scripts/doctor.py ./weekend-tool
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

对 Brownfield 的 R2/R3 critical surface，设计前必须先核对 Physical Schema、Constraints、Grants、Runtime、Machine Contracts、Tests、Transaction / Idempotency / Audit 边界。遇到冲突时不得自行“综合一个合理方案”，而要进入 Drift / Authority Conflict / Controlled Amendment 流程。

详见 `references/DESIGN_GOVERNANCE.md`。

## Progressive Governance

控制强度按 Change/WP 的 `risk_level` 设置，不是全局固定值：

```text
R1 Development
普通 feature / bug
→ branch + review + CI + tests

R2 Critical Surface
schema / migration / shared contract / core runtime / canonical
→ R1 + 独立批准人 + compatibility + migration + integration gate

R3 Production / Security
identity / permission / canonical authority / release control plane
→ R2 + 人类批准 + audit + release controls
```

`risk_level`（控制强度）与 Change Class L1–L3（变更规模）正交：改一行权限表依然是 R3。

一个高风险 Gate 被阻塞，只冻结依赖它或写同一受保护 surface 的工作；无依赖 workstream 可以继续。

详见 `references/GOVERNANCE.md`。

## Doctor 的边界

`doctor.py` 是声明阶段的**确定性 Gate**。`PASS` 不等于业务正确、生产可用或发布成功。

G1 会阻断：

- Work Packet DAG 有环或依赖了不存在的 WP；
- `read_set` 路径既不存在、也不由依赖产出；
- 声明 `parallel_safe_with` 的 WP 之间 `write_set` 重叠；
- 活跃 WP 的 `[done]` 没有可执行命令或可验证产物；
- 引用了不存在的验收项 `AC-xx`；
- R2/R3 WP 没有独立于作者的批准人；
- 声明的 native truth（contract、schema 等）缺失；
- 以及原有控制面检查：coverage、owner、exception、readiness 标记、secret、Brownfield baseline 与 design-reality audit。

另外对以下情况给 warning：风险等级疑似低报、无序 WP 共享 write set、验收项无 WP 覆盖、ADR 无备选、收敛过期。

```bash
python $SKILL/scripts/doctor.py <project> --strict              # warning 也阻断
python $SKILL/scripts/doctor.py <project> --format json         # 带稳定 code，给 Agent/CI 用
python $SKILL/scripts/doctor.py <project> --changed-since main  # drift guard，适合 pre-commit / PR check
```

业务正确性仍由真实 tests/evals/review/runtime evidence 证明。

## 从 1.1 升级

1.2 的 G1 更严格，1.1 下通过的项目升级后可能失败。这正是目的：新出现的失败是原本就存在的缺口。

```bash
python $SKILL/scripts/migrate_wp.py ./my-project/docs/engineering/work                       # 预演
python $SKILL/scripts/migrate_wp.py ./my-project/docs/engineering/work --write --authored-by "agent:compiler"
python $SKILL/scripts/doctor.py ./my-project
```

迁移只搬运能找到的内容，不编造命令、路径或批准人。如需先升级、再按计划补齐，可在 `PROJECT.toml` 设定有期限的过渡：

```toml
[governance]
doctor_compat = "1.1"
doctor_compat_until = "2026-12-31"
```

`governance_level = L1/L2/L3` 仍作为 `risk_level = R1/R2/R3` 的弃用别名被接受。

## Self-test

```bash
python -m unittest discover -s tests -v
python scripts/doctor.py --strict examples/mini-ticket-triage
python scripts/doctor.py --strict examples/legal-consult-mini-app
python scripts/doctor.py --strict examples/knowledge-graph-atlas
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
