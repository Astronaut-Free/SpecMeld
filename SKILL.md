---
name: software-project-standardizer
description: SpecMeld turns a sufficiently discussed software product, client need, or change into a right-sized, execution-ready engineering package that Coding Agents can implement and keep synchronized with reality. Use for greenfield, mature brownfield, feature work, upgrades, AI/Web/App/Mini Program/SaaS/API/data/platform/library/internal/client delivery. It performs business/solution decomposition, architecture trade-offs, design-authority and physical-reality audits, progressive governance, evidence-backed gates, provider-neutral multi-agent integration, and continuous Product/Design/Contracts/Code/Test/Runtime convergence.
---

# SpecMeld（构序） · Software Project Standardizer V1.1.1

## 0. Mission

把已经聊清楚到足够程度的**产品方向、需求、功能、约束**，编译成一套 **Execution-ready Engineering Pack**，让 Coding Agent 从明确入口施工，而不是重新发明产品或架构。

目标始终是：

`Intent ↔ Product ↔ Architecture ↔ Contracts ↔ Code ↔ Tests/Evals ↔ Runtime`

保持收敛。

这不是固定模板库，也不是瀑布式“先写完所有文档再编码”。对外使用流程应简单，内部方法论可以完整；复杂度通过 progressive disclosure 和 risk-sized rigor 控制。

---

## 1. Non-negotiable Rules

1. **Coverage before confidence**：完整性来自主动 Coverage Audit，不来自固定文档数量。
2. **Compile, do not dump templates**：只生成真实需要的工程资产。
3. **Reality wins**：Brownfield 以代码、Schema、配置、部署、测试和运行事实为基线。
4. **Machine truth first**：OpenAPI、Schema/Migration、CI YAML、Docker/IaC、Tokens、Lockfile/SBOM、Tests/Evals 优先作为事实源。
5. **Business before system decomposition**：先业务结果/流程/Capability，再 Domain/模块/服务。
6. **Architecture before technology**：先 Architecture Drivers / NFR / 约束，再选技术。
7. **Trade-off before commitment**：高影响选择必须比较合理候选、成本、风险、可逆性和演进触发条件。
8. **No silent drift**：Code/Contract/Schema/Runtime/安全语义发生变化时，对应 Truth/Spec/Decision 必须同步。
9. **Evidence over claims**：coded、tested、reviewed、integrated、release-ready、deployed、production-verified、accepted 是不同状态。
10. **Parallelism is earned**：多人/多 Agent 并行由 Dependency DAG + write-set overlap + shared-contract ownership 决定。
11. **Implementation ≠ Integration**：实现者默认不自合并；由人类或指定 Integrator 负责集成 Gate。
12. **Change must propagate**：共享 Contract/Schema/Domain 语义/事件/权限/平台基础变化时，必须计算影响消费者、迁移波次和收敛条件。
13. **Context economy**：Coding Agent 默认只加载当前 WP 及链接依赖。
14. **Handover by design**：Client/FDE/长期维护项目必须可由新团队独立接管。
15. **Do not fake tooling**：无法执行命令、测试、部署或验证时，报告 `NOT_RUN / BLOCKED_TOOLING / UNKNOWN`，不得伪造通过证据。
16. **Authority before proposal**：Brownfield critical design 先核 Approved Intent 与 Physical Reality；冲突必须分类，不得由 Agent 自行折中。
17. **Governance is progressive**：控制强度由 Stage + Risk + Surface + Blast Radius 决定；高风险 Gate 不得无条件冻结无依赖 workstream。

---

## 2. Standard Workflow

### A. Reality / Intent Scan

**Greenfield**：提炼 Problem、Users、Jobs/Scenarios、Scope/Non-goals、核心功能/流程、业务规则、平台、NFR/约束、Acceptance、已知/未知。

**Brownfield**：先验证 repo/module、build/test baseline、DB/migration、constraints/grants、API/event、accepted runtime、CI/CD、UX/design system、observability、现有文档漂移和已有工程惯例。对 L2/L3 critical surface，先执行 Design Authority / Physical Reality Audit；旧 Draft、ZIP、archive 不得覆盖 current repository/runtime truth。冲突不得静默综合，按 `IMPLEMENTATION_DRIFT / DOCUMENT_DRIFT / DRAFT_DRIFT / CONTRACT_GAP / AUTHORITY_CONFLICT / CONTROLLED_AMENDMENT_REQUIRED / PHYSICAL_REALITY_BLOCKED` 分类。

### B. Project Classification

写入 `PROJECT.toml`：mode、profile、archetype、lifecycle、owners、coverage、stage、truth paths、native truth、engineering pack status、collaboration、governance default。每个 Change/WP 再按实际 surface 指定 `governance_level`，不要把项目级默认误当成所有改动的最高强度。`profile=nano` 是单人短期小项目的独立轻量路径：只维护 `PROJECT.toml + docs/PROJECT.md`，不编译完整 Engineering Pack。

### C. Coverage Audit

所有项目都扫描 10 个域：Product & UX、Architecture & Code、Data & Storage、API & Integration、Runtime & Infrastructure、Security & Supply Chain、Quality & Delivery、Reliability & Operations、Organization & Change、Conditional Domains。

状态只能是：`APPLICABLE | NOT_APPLICABLE | DEFERRED | UNKNOWN`。

详细判定标准见 `references/COVERAGE.md`。

### D. Establish Current Truth

非 nano 项目的长期摘要真值默认只有：

- `docs/PRODUCT.md`
- `docs/SYSTEM.md`
- `docs/DELIVERY.md`

Nano 项目只使用 `docs/PROJECT.md` 合并真值。

它们描述“当前系统是什么”，不是把所有 LLD/Contract 复制进去。

### E. Solution Architecture Pass

复杂业务、Client/FDE、政企、平台项目先做：

`Business Outcome → Process/Value Stream → Business Capability → Domain/Responsibility → Existing/Target System Mapping → Technology`

高影响技术选择必须基于 Architecture Drivers 比较候选，例如：Build/Buy/Integrate、Monolith/Microservices、Sync/Async、Realtime/Batch、SQL/NoSQL/Search/Vector/Object、SaaS/Private/On-prem、Managed/Self-hosted、Model API/Self-hosted/Fine-tune、ERP/OA/CRM 集成方式。

规则见：

- `references/SOLUTION_ARCHITECTURE.md`
- `references/ARCHITECTURE_DECISIONS.md`

### F. Engineering Documentation Compilation

先生成 **Artifact Plan**，再实例化文件。根据真实复杂度自动选择：

- Engineering Specs（常用模块包括 UX/UI、`MOBILE_MINI_PROGRAM`、System Architecture、Frontend/Backend、Domain、Data/Storage、API/Event/Integration、AI/ML/Eval、Runtime/Infra、Security/Privacy、Quality、CI/CD/Ops、Source/Provenance/Entity Resolution、Client Handover）
- LLDs
- machine-readable Contracts/Schemas
- Work Packets
- Acceptance/Test/Eval Pack
- GitHub/Integration controls
- Client/Executive view（按需）

禁止固定生成“14 份标准文档”。

Compiler 规则见 `references/COMPILER.md`。

### G. G1 Development Ready

只有在以下条件成立时才允许 Coding Agent 正式施工：

- Scope / Acceptance 可执行；
- 核心 UX Flow/State（适用时）明确；
- Architecture boundary / domain / data ownership 明确；
- 并行开发依赖的 API/Event/Schema Contract 明确；
- persistence/migration/runtime/security/test baseline 明确；
- WP DAG 可执行；
- `IMPLEMENTATION_ENTRY.md` 可直接作为施工入口；
- 不存在会让两个实现者造出不同系统的关键 UNKNOWN；
- Brownfield L2/L3 design 不存在未解除的 Authority Conflict / Amendment Required / Physical Reality Block；
- 当前 governance controls 与 Change/WP 的风险和 surface 相匹配；
- 核心控制文档 `sps:readiness` 已从 `DRAFT` 更新为 `READY`；
- `doctor.py` 对声明阶段通过。

达到后：

```toml
stage = "G1_BUILD_READY"
[engineering_pack]
status = "DEVELOPMENT_READY"
```

### H. Build → Review → Integration → Convergence

Coding Agent：

1. 读取 `IMPLEMENTATION_ENTRY.md`；
2. 读取当前 `WP-xxx.md`；
3. 只读 WP 链接的 Spec/LLD/Contract；
4. 在隔离 branch/worktree 上实现；
5. 执行指定 tests/evals；
6. 独立 Review；
7. 更新 Evidence；
8. 同步受影响 Truth/Spec/LLD/Native Truth；
9. 通过 Integration/Convergence Gate 后再进入下一个 WP。

执行、协作与发布规则见 `references/EXECUTION.md`、`references/COLLABORATION.md`。

---

## 3. Cross-Module Change Propagation

当公共 Contract/Schema/Canonical/Domain 语义、权限、事件、Projection、外部集成或平台基础发生变化时：

1. 构建 **Change Impact Graph**；
2. 找 direct consumers 与 material indirect consumers；
3. 标记 `AFFECTED | MIGRATION_REQUIRED | COMPATIBLE_NO_CHANGE | DEFERRED | NOT_APPLICABLE | WAIVED`；
4. 编排 Migration Waves，典型顺序：`expand → dual-compatible → backfill/rebuild → switch → observe → retire`；
5. 共享基础先集成，下游 WP 刷新 baseline；
6. 所有影响项收敛前 Change 不得 Closed。

简单局部改动不启用此机制。详见 `references/PROPAGATION.md`。

---

## 4. Design Authority & Progressive Governance

Brownfield critical design 先做 `Intent Authority ↔ Reality Evidence` 对齐，再允许 PROPOSE。Physical Schema/Constraint/Grant、accepted runtime、machine contract、tests、transaction/idempotency/audit boundary 是设计输入，不是事后补充。适用规则见 `references/DESIGN_GOVERNANCE.md`。

治理按需分级：普通 feature 用 L1；schema/migration/shared contract/core runtime/canonical 通常进入 L2；identity/permission/canonical authority/release control plane 等高风险面才进入 L3。Stage 只增加必要控制，不把所有工作全局升级。详见 `references/GOVERNANCE.md`。

---

## 5. Continuous Synchronization

开发中发现设计与现实不一致时先分类：

- **Implementation detail**：只影响内部实现 → 更新 LLD/native truth；
- **Design delta**：改变模块职责、数据、API、UX flow、failure semantics → 先更新 Spec/Change；
- **Architecture / Breaking delta**：改变核心边界、公共 Contract、核心数据模型、迁移策略 → 先 RFC/ADR + compatibility/migration/rollback。

相关 Docs/Contract/Schema/Test 理想默认与代码在同一 PR/Change 中同步。

每个 WP/Feature 完成时检查：

`Requirement ↔ Spec/LLD ↔ Contract/Schema ↔ Code/Config ↔ Test/Eval ↔ Runtime Evidence`

详细规则见 `references/SYNC.md`。

---

## 6. Version / Change / Retirement

- L1 小改：Change + WP；
- L2 Feature：Impact + Spec delta + WP + Acceptance；
- L3 Breaking/高风险：RFC/ADR + Compatibility/Migration/Rollback + 强 Review；
- Current Truth 文件名稳定，不创建 `final_v2_最终版`；
- ADR 被替代时 `Superseded`，不重写历史；
- 已执行 DB migration 不修改，只新增 migration；
- Breaking Contract 必须有 version / migration path / deprecation window；
- Deprecated ≠ Removed；旧路径满足 Retirement Gate 后才真正删除；
- 发布快照由 Git Tag/Release 保存。

详见 `references/LIFECYCLE.md`、`references/ARTIFACTS.md`。

---

## 7. Artifact Model

### Project Operating Layer

Nano：`PROJECT.toml + docs/PROJECT.md`。

非 nano：

```text
PROJECT.toml

docs/
├─ PRODUCT.md
├─ SYSTEM.md
└─ DELIVERY.md

changes/
decisions/
```

### Engineering Pack

```text
docs/engineering/
├─ ENGINEERING_INDEX.md
├─ IMPLEMENTATION_ENTRY.md
├─ IMPLEMENTATION_PLAN.md
├─ specs/
├─ lld/
├─ work/
└─ acceptance/

contracts/
schemas/
```

默认路径、模板路由、状态命名空间和 Source-of-Truth 规则见 `references/ARTIFACTS.md`。

---

## 8. Machine Truth

优先使用机器可读事实：OpenAPI/AsyncAPI/protobuf、DB migration/schema、Docker/Compose/K8s/Helm、IaC、CI/CD YAML、Design Tokens、package manifest/lockfile/SBOM、typed config schema、tests/evals。

Markdown 主要解释目的、语义、边界、责任、失败模式、变更规则和权威路径。

---

## 9. Progressive Disclosure — 何时加载哪个 Reference

不要一次加载全部 references。

| Trigger | Load |
|---|---|
| 做 Coverage / G1 前查漏 | `references/COVERAGE.md` |
| 决定生成哪些工程资产、LLD/WP | `references/COMPILER.md` |
| Business Capability / Client / Solution Architecture | `references/SOLUTION_ARCHITECTURE.md` |
| 高影响技术选型 / Build-vs-Buy / NFR trade-off | `references/ARCHITECTURE_DECISIONS.md` |
| Artifact 类型、路径、状态、版本 | `references/ARTIFACTS.md` |
| 多人/多 Agent / GitHub/GitLab/Gitee/local integration | `references/COLLABORATION.md` |
| Build/Test/CI/CD/Release/Ops | `references/EXECUTION.md` |
| Change Class / Rollback / Deprecation / Handover | `references/LIFECYCLE.md` |
| 跨模块共享 truth 变化 | `references/PROPAGATION.md` |
| 文档/代码持续同步与收敛 | `references/SYNC.md` |
| Brownfield Design Authority / Physical Reality / Freeze | `references/DESIGN_GOVERNANCE.md` |
| 治理强度分级 / Applicability / Right-Sizing | `references/GOVERNANCE.md` |
| 需要理解方法来源和取舍 | `references/BENCHMARKS.md` |

---

## 10. Tooling Contract

### Bootstrap

```bash
python scripts/init_project.py <project> --name <name> --mode <greenfield|brownfield|client> --profile <nano|lite|standard|critical>
python scripts/init_engineering_pack.py <project>
```

`init_project.py` 只创建最小控制面；`profile=nano` 只创建 `PROJECT.toml + docs/PROJECT.md`，`init_engineering_pack.py` 对 nano 直接跳过。`--mode brownfield` 不会为了“看起来不同”而批量生成空 Reality Scan 文件。Brownfield 差异发生在后续 compiler/reality-scan 行为和 G1 验证上。

### Doctor

```bash
python scripts/doctor.py <project>
```

`doctor.py` 是**结构与声明阶段 readiness checker**，不是业务正确性证明。`PASS` 只表示当前声明 Gate 的可机器验证约束通过；功能正确性仍必须由 tests/evals/review/runtime evidence 证明。

工具无法运行时，不修改 ACL/安全策略来“让它能跑”；报告 `BLOCKED_TOOLING` 并说明未观测证据。

### Skill Self-test

```bash
python -m unittest discover -s tests -v
python -m py_compile scripts/*.py
```

仓库内 `.github/workflows/selftest.yml` 可用于 CI 验证 skill 自身。

---

## 11. Output Contract

### 首次标准化后

Nano 只交付 `PROJECT.toml + docs/PROJECT.md` 并运行轻量 doctor。非 nano 必须交付：

1. Project Classification / Tailoring
2. Coverage Summary
3. Current Truth (`PROJECT.toml`, `PRODUCT.md`, `SYSTEM.md`, `DELIVERY.md`)
4. `ENGINEERING_INDEX.md`
5. 按需 Engineering Specs / LLDs / Contracts
6. WP DAG + `WP-xxx`
7. Acceptance/Test/Eval Pack
8. Native Truth inventory
9. `IMPLEMENTATION_ENTRY.md`
10. G1 verdict: `PASS | CONCERNS | FAIL`

### 每个 WP/Feature 完成后

交付：actual diff/SHA/PR、test/eval/review evidence、Truth/Spec/LLD/Native Truth updates、migration/rollback 状态、remaining risk/debt、convergence verdict。

---

## 12. Complete Reference Index

- `references/COVERAGE.md`
- `references/COMPILER.md`
- `references/SOLUTION_ARCHITECTURE.md`
- `references/ARCHITECTURE_DECISIONS.md`
- `references/ARTIFACTS.md`
- `references/COLLABORATION.md`
- `references/EXECUTION.md`
- `references/LIFECYCLE.md`
- `references/PROPAGATION.md`
- `references/SYNC.md`
- `references/DESIGN_GOVERNANCE.md`
- `references/GOVERNANCE.md`
- `references/BENCHMARKS.md`

模板位于 `templates/`；工具位于 `scripts/`；可运行测试位于 `tests/`；golden examples 位于 `examples/`。
