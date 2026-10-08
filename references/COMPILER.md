# Engineering Documentation Compiler

## 1. 目标

把稳定到足够开发的 Product Intent 编译成 Coding Agent 可执行的工程包，而不是固定生成一套目录。

## 2. 编译阶段

1. Build Coverage Map
2. Decompose business goals/processes into Business Capabilities and responsibility boundaries
3. Map capabilities to existing/target systems, ownership and Build/Buy/Integrate/Extend candidates
4. Extract Architecture Drivers from Product/NFR/current reality/constraints
5. Run high-impact Architecture Decision & Trade-off Pass
6. Establish Solution Strategy + key ADRs/evolution triggers
7. Build Artifact Plan
8. Establish Current Truth summaries
9. Select Engineering Spec modules
10. Generate/attach Native Truth contracts
11. Compile LLDs
12. Build Dependency DAG + write-set overlap graph
13. If shared truth changes, build Change Impact Graph + Migration Waves
14. Derive parallel-safe groups, shared-hotspot owners and integration order
15. Compile Work Packets
16. Build Acceptance/Test/Eval mapping
17. Generate Implementation Entry + Integration Plan
18. Generate stakeholder/executive view when the project has client/business audiences
19. Run G1 consistency audit

## 2.1 Business Capability Decomposition（先拆业务，再拆系统）

在 Architecture Decision Pass 前，先把业务语言转换为稳定的能力/责任模型。尤其适用于 enterprise、Client/FDE、跨部门平台和复杂业务系统。

执行顺序：

1. 从用户/客户目标识别 key business outcomes；
2. 还原端到端 business process / value stream，而不是只收集功能按钮；
3. 提取 Business Capabilities（例如 Supplier Management、Procurement、Contract、Inventory、Settlement）；
4. 区分 capability、domain/bounded context、application/module/service，禁止一一等同；
5. 标记现有系统与 Source of Truth：KEEP / EXTEND / REPLACE / BUY / INTEGRATE / NEW；
6. 确定 capability owner、data owner、主要 handoff、external dependency；
7. 形成 capability → system responsibility mapping，再进入技术组合与 trade-off。

默认优先复用成熟已有能力。只有业务差异化、集成约束、NFR、所有权或成本证明值得时，才新增独立系统/服务。

详细规则见 `SOLUTION_ARCHITECTURE.md`。

## 2.2 Architecture Decision Pass（G1 前）

在 Artifact Plan 之前执行。目标不是生成更多文档，而是避免“功能聊清楚了，但技术组合仍靠拍脑袋”。

按适用性处理高影响决策：

- Build / Buy / Adopt Open Source / Managed / Integrate / Hybrid
- Standard product / Extension / Plugin / Full custom
- Modular Monolith / Microservices / Serverless / Event-driven / Hybrid
- REST/RPC / Event/Queue / Webhook / CDC / Batch/Streaming
- Real-time / Near-real-time / Batch
- SQL/NoSQL/Search/Vector/Object/Cache 的职责与 Source of Truth
- Public/Dedicated SaaS / Private cloud / On-prem / Hybrid；Managed / Self-hosted
- Hosted Model API / Multi-provider / Self-hosted / Fine-tuned / Custom-trained
- Existing ERP/OA/CRM/Identity 的 system-of-record、adapter、sync、reconciliation 和 outage strategy

选择依据来自 Architecture Drivers：业务差异化、time-to-market、scale、latency/freshness、availability、security/privacy/permissions、consistency、compatibility、deployment/data residency、RPO/RTO、cost/TCO、team/ops capability、vendor lock-in、reversibility。

高影响选择必须记录 alternatives + consequences + reversibility + evolution trigger；难逆转或长期重要的结论创建 ADR。详细见 `ARCHITECTURE_DECISIONS.md`。

## 2.3 Governance Right-Sizing Pass

在 Artifact Plan 前判断每个 Change/WP 的治理等级，而不是全项目统一拉满：

- `L1`：普通 feature/bug/local compatible change；
- `L2`：schema/migration/shared contract/core runtime/canonical；
- `L3`：identity/permission/canonical authority/release control plane/high-risk production effect。

判断因子：`Stage + Risk + Affected Surface + Blast Radius`。项目 `[governance].default_level = auto` 时由 compiler 决定；Change/WP 可以显式记录更高或更低但必须给出理由。

Brownfield L2/L3 设计在生成/冻结 LLD 前必须先走 `DESIGN_GOVERNANCE.md` 的 Physical Reality Audit。

## 3. Artifact Plan 规则

一个主题只有在以下任一条件成立时才拆成独立 Spec：

- 有独立 Owner
- 有独立生命周期或版本
- 有多个 Coding Agent/团队并行依赖
- 有高风险/强 review 要求
- 有多个 machine contracts 需要解释
- 主文档该章节已无法一次可靠 review

否则保留为 PRODUCT/SYSTEM/DELIVERY 的章节。

### 反碎片规则

- 两份文档有 >50% 相同事实：合并或改成链接 authoritative truth。
- machine-readable artifact 已能准确表达的字段：Markdown 不复制。
- 单纯因为“模板里有”不能成为建文档理由。
- 一个 Spec 只负责一个稳定的关注点，不按团队会议/聊天主题拆。

## 4. Spec Module Catalog

### UX_UI_SPEC
适用：有 GUI/交互且 Core Flow/State/Design System 对实现有约束。
应包含：IA、Flows、screen/state matrix、interaction rules、responsive、accessibility、i18n、tokens/components authority、design QA。

### SYSTEM_ARCHITECTURE
适用：多模块/服务/复杂 runtime，或存在重要技术组合/部署/集成选择。
应包含：Business Capability → System Responsibility mapping、Architecture Drivers、Solution Strategy、context、按需的 Context/Capability/Building Block/Runtime/Data/Integration/Deployment/Security views、boundaries、building blocks、runtime flows、deployment mapping、quality/risk、Build/Buy/Integrate 与关键技术 trade-offs、reversibility、Evolution Triggers、linked ADRs。

### SOLUTION_OVERVIEW
适用：Client/FDE、政企、跨部门平台、售前/方案评审，或同一方案需要同时被业务领导和研发团队理解。普通纯内部工程项目不单独创建。
应包含：business outcome、capability map、existing-vs-target fit-gap、logical solution view、关键 integration/deployment、安全/可靠性约束、技术选择的业务解释、cost/risk/assumptions、phasing/80-20 boundary。它是 stakeholder view，不得创造与 SYSTEM/ADR 不一致的新事实。

### SOLUTION_STRATEGY_TECH_SELECTION
适用：Client/FDE、采购/供应商评估、标准产品 + 定制边界复杂，或跨多个域存在大量 Build/Buy/Integrate/Managed/Vendor 选择，已无法在 SYSTEM_ARCHITECTURE 中一次可靠 Review。
应包含：Architecture Drivers、candidate options、fit-gap、TCO、delivery/ops impact、security/data residency、vendor lock-in/exit、customization boundary、recommendation、linked ADRs。普通产品项目不要单独创建。


### MOBILE_MINI_PROGRAM
适用：iOS/Android/跨端 App 或微信/支付宝等小程序，存在平台生命周期、审核、设备能力或弱网约束。
应包含：设备权限、应用签名/小程序主体与审核、商店/小店审核、灰度发布、版本兼容、分包策略、离线/弱网行为、平台 API/SDK 兼容边界。

### FRONTEND_ARCHITECTURE
适用：客户端复杂、状态/导航/缓存/离线/多端逻辑显著。

### BACKEND_SERVICE_ARCHITECTURE
适用：多服务/worker/job/domain boundaries/transaction boundaries 显著。

### DOMAIN_MODEL
适用：核心业务实体、状态机、规则较复杂。

### DATA_DATABASE_STORAGE
适用：持久化、复杂 schema、migration/backfill、object storage、volume、cache/search、retention/backup 重要。

### API_EVENT_INTEGRATION
适用：多个 consumer/provider、公共 contract、事件/Webhook/第三方依赖。

### AI_ML_INFERENCE_EVAL
适用：Model/Prompt/RAG/Tool/Agent/Eval 是产品能力。

### RUNTIME_CONTAINER_INFRA
适用：Docker/Compose/多容器/Cloud/IaC/多环境/网络拓扑复杂。

### SECURITY_PRIVACY
适用：敏感数据、AuthZ、租户隔离、支付、合规、外部暴露面较高。

### TEST_QUALITY_EVAL
适用：测试矩阵复杂、跨层、AI Eval、性能、安全、UAT 需要独立管理。

### CI_CD_RELEASE_OPERATIONS
适用：多环境、artifact promotion、migration、canary、rollback、SLO/operations 复杂。

### SOURCE_PROVENANCE_ENTITY_RESOLUTION
适用：采集、情报、知识库、知识图谱、ETL，存在来源/证据/实体消解/数据血缘。

### CLIENT_HANDOVER_SPEC
适用：FDE/外包/客户交付。

## 5. LLD 触发规则

**Design Governance trigger**：Brownfield + governance L2/L3 的 LLD 必须在 Freeze 前记录 `authority_status` 与 `physical_reality_audit`；不得先写“合理设计”再回头找证据。

生成 LLD，当任一成立：

- 一项工作跨 ≥3 个模块/文件群且存在顺序/状态耦合
- 有明确 state machine / transaction / concurrency / retry semantics
- 一个服务/模块会被多个 WP 共同修改
- 多 Agent 并行需要稳定边界
- Contract 已确定但内部实现仍有明显设计空间
- 失败模式/恢复逻辑复杂

不要为单文件 helper、小 CSS 调整、简单 CRUD 自动生成 LLD。

## 6. LLD 最低内容

- Purpose / responsibility
- Inputs / outputs
- Internal components / exact touchpoints
- State / data structures
- Control flow / sequence
- Invariants / validation rules
- Transaction / idempotency / concurrency / retry
- Failure & recovery
- Config/dependencies
- Observability
- Security implications
- Tests/fixtures
- Migration/compatibility
- Out of scope
- Native truth links

## 7. Work Packet 编译

每个 WP 必须足够小到可以独立验证，足够大到形成有意义的工程增量。

### WP 字段

- id / title / owner / status / timebox / issue_ref
- goal / done condition
- dependencies
- prerequisite baseline
- read set
- write set
- invariants / forbidden changes
- implementation obligations
- native contract/schema changes
- test/eval commands
- review lenses
- evidence requirements
- truth/spec/lld sync targets
- rollback notes if applicable

### WP Timebox Guidance

时间盒是规划参考，不是硬性限制，也不能为了“按时”牺牲 Gate：

- L1：通常半天级；
- L2：通常 1–3 天；
- L3：通常按周拆分并设置中间验证点。

超过参考量级时优先重新检查范围、依赖和是否应该拆 WP，而不是机械延长。

### Change Impact Graph / Migration Waves

当本次工作修改共享 API/Event/Schema、Canonical/Domain 语义、权限、共享库、Projection、外部集成或平台基础时，Compiler 必须在普通 Dependency DAG 之外再构建 **Change Impact Graph**：

- changed authoritative truth / owner
- direct consumers
- material indirect consumers
- affected tests/evals/docs/runtime/release paths
- propagation state for each consumer
- migration wave / compatibility window / retirement condition

典型迁移顺序是 `expand → dual-compatible → backfill/rebuild → switch → observe → retire`，但只实例化项目真正需要的阶段。任何 material consumer 不得保持 silent/unclassified。详细见 `PROPAGATION.md`。

### Dependency DAG / Parallelism

Dependency DAG 之外必须再检查 write-set overlap。`无依赖` 不等于 `可并行`。如果多个 WP 修改同一 contract/schema/migration/shared hotspot，应先抽稳定边界、指定单一 owner 或串行执行。

为多人/多 Agent 项目，Compiler 还必须输出：

- parallel-safe WP groups
- serialized/shared-hotspot WPs
- contract/schema-first WPs
- per-WP owner + integrator
- branch/worktree isolation plan
- PR dependency / merge order
- merge queue or serialized integration policy
- post-merge integration gate

优先顺序通常：

1. foundational contracts/schema/scaffold
2. core domain/data
3. services/backend
4. clients/UI
5. integration
6. quality/e2e/eval
7. release/ops/handover

但必须以实际依赖为准，不机械套顺序。

## 8. Typical output size — 不是硬指标

- Lite：通常 5–8 份工程说明/计划类文档 + 少量 WP
- Standard：通常 8–16 份 + LLD/WP
- Critical/Complex：通常 12–30 份 + 更多 LLD/WP

数量不是质量指标。目标是“Coding Agent 无关键歧义 + 人类可维护”。

## 8.1 G1 Architecture Decision Exit

`DEVELOPMENT_READY` 不只意味着“有架构图”。在适用时必须确认：

- Architecture Drivers 已识别，关键 NFR 有目标/边界/验证方式；
- System boundary、主要 building blocks、source-of-truth/data ownership 清楚；
- 高影响 Build/Buy/Integrate、deployment、communication、data、AI sourcing 等选择已完成必要 trade-off；
- 高锁定/难逆转选择有 ADR 或明确 exit/evolution trigger；
- 没有会让两个 Coding Agent 设计出不同系统的关键架构 UNKNOWN；
- 关键结论已经落到 SYSTEM/Spec/Contract/LLD/WP，而不是只存在聊天记录。

## 9. Implementation Entry

Implementation Entry 必须能回答：

- 我现在在哪个 baseline 上？
- 我第一步读什么？
- 我不需要读什么？
- 当前第一个 WP 是哪个？
- 下一步取决于什么？
- build/test/eval 命令是什么？
- 什么情况下必须停下来更新设计？
- 谁能批准 merge/release/destructive change？
- 完成后证据写到哪里？

## 10. Brownfield Compilation

先生成 Current Reality + Drift Map，再编译目标 Delta。对现有技术栈先问“是否阻碍目标/NFR”，而不是“有没有更现代的选择”；除非收益能覆盖迁移、回归、培训和运维成本，否则不要为架构审美做技术替换。

不要把整个既有系统重写成新文档；优先：

- 记录当前真实边界
- 对目标改动涉及的区域生成/补强 Spec/LLD
- 复用已有命名/模式/工具
- 把 legacy inconsistency 显式标记为 debt，而不是偷偷“规范化”导致大范围无关改动

## 11. Provider-native Collaboration Outputs（按需）

当 `collaboration.mode != single` 时，Compiler 根据 `collaboration.provider` 和已有 repo 现实判断并按需生成/更新：

- provider 的 ownership 机制（GitHub/GitLab 可用 CODEOWNERS；其他平台使用经验证的等价机制）
- provider 的 PR/MR/change template（GitHub 可基于 `templates/PULL_REQUEST.md`）
- CI/Required Checks workflows（必须绑定真实 build/test/eval 命令，禁止空壳）
- `DELIVERY.md` 中的 branch/ruleset/review/merge queue policy

Ruleset / protected branch / Merge Queue / Merge Train 等 provider 设置不是 Markdown 事实。若工具有权限，应读取/配置/验证；若无权限，只输出待配置项并标 `NOT_VERIFIED`，不得声称已经生效。

---

## Artifact Routing / Index Discipline

Compiler 实例化模板时遵循 `references/ARTIFACTS.md` 与 `PROJECT.toml [artifact_paths]`：

- Spec → `artifact_paths.engineering_specs`
- LLD → `artifact_paths.lld`
- WP → `artifact_paths.work`
- Acceptance → `artifact_paths.acceptance`
- Contract → `artifact_paths.contracts`
- Schema → `artifact_paths.schemas`
- ADR → `artifact_paths.decisions`
- Change → `artifact_paths.changes`

每个实例化 Artifact 必须把**实际 Path**登记进 `ENGINEERING_INDEX.md` 或对应 Current Truth；未登记路径的“文档名清单”不算完成编译。

核心控制文件由 `<!-- sps:readiness=... -->` 标记机器 readiness。模板初始为 `DRAFT`；只有内容、Owner、依赖、Acceptance 和当前 Truth 已经足够执行时才能改为 `READY`。不要为了让 doctor 通过而机械改标记。
