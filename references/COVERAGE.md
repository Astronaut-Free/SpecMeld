# Coverage Audit — 10 Domains

目标：用少量维度覆盖完整软件生命周期。每个域都必须回答四个问题：

1. 是否适用？
2. 权威事实在哪里？
3. 谁负责？
4. 通过什么 Gate / Evidence 证明完成？

允许状态：`APPLICABLE | NOT_APPLICABLE | DEFERRED | UNKNOWN`。

- `APPLICABLE`：必须有 Truth/Native Truth + Owner + Gate/Evidence。
- `NOT_APPLICABLE`：必须写明为什么不适用。
- `DEFERRED`：必须写明 `owner=...; trigger=...; target=...`。
- `UNKNOWN`：必须写验证方式；如果会影响 G1，则不得进入 G1。

---

## 1. Product & UX

### 判断问题
- 谁使用、解决什么问题、核心 Jobs/Scenarios 是什么？
- Scope / Non-goals / Business Rules 是否清楚？
- IA、User Flow、Screen/State、empty/loading/error/disabled/success 是否闭合？
- 是否涉及 responsive、accessibility、i18n/l10n、Design System/Tokens？
- Mobile/小程序是否引用 `MOBILE_MINI_PROGRAM` spec，并覆盖设备权限、应用签名/小程序主体、商店/小店审核、灰度发布、版本兼容、分包策略、离线与弱网？
- 哪些产品级 NFR 会改变架构？

### 可判 NOT_APPLICABLE 的典型情况
纯 backend/library 且没有用户交互面；但 Product Intent / Acceptance 仍不能缺失。

### G1 最低证据
`PRODUCT.md` 已达到 `sps:readiness=READY`；核心 flow / acceptance 足以让实现者不自行发明产品行为。

---

## 2. Architecture & Code

Brownfield critical surface 追加：**Design Authority / Physical Reality** 是否核对 approved intent、schema/constraints/grants、accepted runtime、machine contracts、tests 与 transaction/idempotency/audit 边界；如冲突是否进入受控分类而不是 Agent 自行折中。

### 判断问题
- 复杂业务是否先完成 Business Process / Capability decomposition？
- capability → domain → system responsibility 映射是否清楚？
- Architecture Drivers / Quality Attributes 是什么？
- Build/Buy/Integrate、standard/custom、Monolith/Microservices/Serverless 等关键选择为什么成立？
- system/module/service boundary、state ownership、dependency direction、runtime flow 是否稳定？
- sync/async、realtime/batch、concurrency、failure behavior 是否明确？
- 是否定义 evolution trigger，而不是为假想未来过度设计？

### 可判 NOT_APPLICABLE 的典型情况
几乎不存在；即使是小脚本也至少要有最小 responsibility boundary 与 runtime assumption。

### G1 最低证据
`SYSTEM.md` READY；会影响多人/多 Agent 的关键架构选择有明确记录，长期/难逆转决定有 ADR。

---

## 3. Data & Storage

### 判断问题
- 核心 entities/state 和 Source of Truth 是什么？
- SQL/NoSQL/Search/Vector/Object/Cache 各自承担什么职责，是否真的需要 polyglot persistence？
- schema/constraints/transactions/index/query/migration/backfill 是否明确？
- retention/deletion/provenance/data quality 是否需要治理？
- files/object storage、persistent volume、backup/restore、RPO/RTO、encryption/capacity 是否适用？

### 可判 NOT_APPLICABLE 的典型情况
完全无持久化、无文件、无外部状态的纯计算库/一次性工具。

### G1 最低证据
关键 state ownership 与 persistence strategy 已明确；需要并行开发的 schema/contract 已冻结到足够程度。

---

## 4. API & Integration

### 判断问题
- provider/consumer 是谁？
- REST/RPC/Event/Queue/Webhook/CDC/Batch/Streaming 为什么这样选？
- version/auth/error/idempotency/pagination/timeout/retry/rate limit 是否明确？
- 外部 ERP/OA/CRM/Identity/Provider 的 System of Record、adapter、reconciliation、quota/SLA/fallback 是什么？
- 是否需要 OpenAPI/AsyncAPI/protobuf/GraphQL/Event schema 和 contract tests？

### 可判 NOT_APPLICABLE 的典型情况
真正无外部/跨模块接口的单进程封闭工具。

### G1 最低证据
并行开发依赖的接口有 machine-readable contract 或等价精确 Contract。

---

## 5. Runtime & Infrastructure

### 判断问题
- SaaS/Dedicated/Private Cloud/On-prem/Hybrid/Edge 怎么选？Managed 还是 Self-hosted？
- processes/services/workers/jobs、container/network/port/volume/health/readiness 如何运行？
- dev/test/staging/prod、config/secrets/service account 如何隔离？
- cloud/VPC/DNS/TLS/CDN/LB/WAF/IaC 是否适用？
- data residency、portability、vendor lock-in 是否影响方案？

### 可判 NOT_APPLICABLE 的典型情况
纯 library；但 build/runtime baseline 仍要记录。

### G1 最低证据
实现者知道本地如何运行、生产目标拓扑是什么、哪些运行约束不能自行改变。

---

## 6. Security & Supply Chain

### 判断问题
- authentication / authorization / tenant isolation / sensitive data / privacy 边界是什么？
- 是否需要 threat model / abuse case / audit log？
- secrets 生命周期如何管理？
- dependency pinning、lockfile、license、SBOM、provenance/signing、vulnerability/patch policy 是否适用？

### 可判 NOT_APPLICABLE 的典型情况
安全域几乎从不完全 N/A；可降低深度，但不能默认跳过 dependency/secrets 基线。

### G1 最低证据
权限和敏感数据边界不会留给 Coding Agent 临场决定。

---

## 7. Quality & Delivery

### 判断问题
- unit/integration/contract/E2E/performance/security/AI eval 哪些适用？
- test data / flaky policy / review / CI gates 是否明确？
- artifact identity / registry / CD promotion / RC / feature flag / rollout / migration / rollback test 怎么做？

### 可判 NOT_APPLICABLE 的典型情况
几乎不存在；prototype 可降低 Gate 深度，但至少要有可执行验证。

### G1 最低证据
每个 WP 有 test/evidence 路径；关键 Contract 能被自动验证。

---

## 8. Reliability & Operations

### 判断问题
- logs/metrics/traces/audit/correlation ID 哪些需要？
- SLI/SLO、alert、runbook、support/on-call、incident/postmortem 是否适用？
- backup restore drill / DR / capacity / degraded mode / provider outage 怎么处理？

### 可判 NOT_APPLICABLE 的典型情况
短期 prototype 或不运营的 library；production/maintained 系统通常应适用。

### G3/G4 最低证据
发布后能 Observe / Diagnose / Recover；生产项目恢复策略有验证证据。

---

## 9. Organization & Change

追加检查：**Governance Right-Sizing**。当前 controls 是否与 Stage + Risk + Surface + Blast Radius 匹配；普通 feature 是否被错误套用 L3 控制；某一阻塞是否不必要地冻结无依赖 workstream。

### 判断问题
- Owner/DRI/RACI 或等价责任是否清楚？
- CODEOWNERS / decision rights / branch/worktree / PR / Required Checks / Merge Queue / Integrator 是否需要？
- Dependency DAG、write-set overlap、shared hotspots 是否决定并行度？
- versioning、RFC/ADR trigger、compatibility/deprecation、exceptions/expiry、docs lifecycle、archive/EOL 怎么管理？

### 可判 NOT_APPLICABLE 的典型情况
单人极小项目可把协作机制降到最低，但 version/change/history 仍不能完全消失。

### G1 最低证据
多人/多 Agent 项目必须有明确 merge authority、integration strategy、work isolation。

---

## 10. Conditional Domains

按项目实际启用，不要求全部生成独立文档。

### AI/ML
Hosted API vs self-hosted/fine-tuned/custom/hybrid、model/prompt/routing/retrieval/tool schema、eval/golden set、latency/cost/privacy/data residency、fallback/human approval/provider failover/model lifecycle。

### Analytics / Experiment
Event taxonomy、metric definition、A/B guardrails、data quality。

### FinOps
Infra/API/AI/storage/network/license/support cost、Build-vs-Buy TCO、budget、unit economics/capacity。

### Compliance
Jurisdiction、retention、consent、auditability、regulated deployment/data handling。

### Client / FDE
Business capability map、standard-vs-custom boundary、existing systems、fit-gap、stakeholder translation、IP/cloud/account/domain/cert ownership、credential transfer、support/SLA、handover/EOL。

### G1 判定
Conditional domain 若会改变核心架构、数据边界或交付方式，则必须在 G1 前从 UNKNOWN 变为明确状态；否则可以 DEFERRED，但必须记录 owner/trigger/target。
