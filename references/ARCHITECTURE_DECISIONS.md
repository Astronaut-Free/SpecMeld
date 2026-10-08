# Architecture Decision & Trade-off Engine

目标：把业务目标、功能需求、非功能性需求（NFR）、现有系统约束、预算/时间/团队能力，转换成**有理由、有边界、可演进的 Solution Strategy**。这里关注的不是“技术能不能做”，而是“在当前约束下，哪种做法最合理”。

本机制用于高影响架构决策；不要求为每个 npm 包、helper、UI 库做正式选型文档。

---

## 1. 基本原则

1. **Architecture before technology**：先明确业务目标、Quality Attributes 和约束，再选技术。
2. **Simplest sufficient architecture**：默认选择满足已知需求的最简单方案，不因“看起来高级”引入微服务、Kafka、Kubernetes、NoSQL 等复杂度。
3. **Trade-off, not best practice absolutism**：没有脱离场景的“最佳技术”，只有在具体约束下更合适的方案。
4. **Reversible decisions stay light**：容易替换、低影响的选择轻量记录；高成本、强锁定、跨系统、数据不可逆的选择必须更严谨。
5. **Build differentiation, reuse commodity where sensible**：核心差异化能力优先掌控；成熟通用能力优先评估采购、托管或集成，而不是默认全部自研。
6. **NFR must drive architecture**：规模、延迟、可用性、安全、权限、兼容、部署、RPO/RTO、成本等不是附录，而是 Architecture Drivers。
7. **Design for evolution, not hypothetical infinity**：为合理增长留边界，但不要提前为“未来一亿用户”建设当前不需要的复杂系统。
8. **Every lock-in needs an exit view**：高供应商锁定、专有 API、专有数据格式、不可迁移平台需要明确退出/迁移成本与触发条件。
9. **Existing reality matters**：Brownfield / Client 项目必须把既有 ERP、OA、身份系统、部署环境、团队技能和运维能力作为硬约束，而不是从零设计理想架构。
10. **Decision evidence over taste**：技术偏好、流行度、个人熟悉度可以是输入，但不能单独成为关键架构决策理由。

---

## 2. Architecture Driver Extraction

在技术选型前，至少检查以下输入；只有真正影响设计的项才需要量化到工程级别。

### Business / Product

- 核心业务能力和差异化能力是什么？
- Time-to-market / deadline？
- 标准产品可覆盖多少，必须定制多少？
- 哪些能力是 commodity，哪些是核心竞争力？
- 业务失败的代价是什么？

### Scale / Performance

- 用户规模、并发、QPS、任务吞吐？
- 数据规模、文件规模、增长速度？
- P50/P95/P99 latency 或用户可接受等待时间？
- 实时、近实时还是小时/天级 freshness？

### Reliability / Recovery

- Availability/SLO？
- 单点故障允许吗？
- Degraded mode 是什么？
- RPO / RTO？
- Provider/region/network outage 怎么办？

### Security / Privacy / Permission

- 数据敏感等级？
- 用户、员工、主管、管理员、租户权限边界？
- 数据驻留/合规/审计要求？
- 客户是否要求私有化、专网或本地部署？

### Integration / Compatibility

- 必须连接哪些 ERP/OA/CRM/微信/企微/第三方？
- 对方支持 API、Webhook、MQ、CDC、Batch file 中哪些能力？
- Legacy protocol / network / auth 限制？
- 是否需要双写、对账、重放、补偿？

### Delivery / Operations

- 团队规模和技能？
- 是否有 SRE/DBA/安全团队？
- 发布频率？
- 客户能否运维 Kubernetes/消息系统/模型服务？
- 云资源/客户机房/混合云限制？

### Cost / Commercial

- 开发预算和持续运维预算？
- 单用户/单任务/单推理可接受成本？
- License / cloud / API / network egress / GPU 成本？
- 自研的人力 TCO 是否高于采购/托管？

---

## 3. NFR → Quality Attribute Scenario

对会改变架构的 NFR，优先写成可验证场景，而不是“高性能、高可用、可扩展”这类形容词。

推荐格式：

```text
在 <条件/负载> 下，
当 <刺激/事件> 发生时，
系统应 <响应>，
并满足 <可测量目标>，
通过 <测试/监控/演练> 验证。
```

典型维度：

- Performance：并发/QPS/任务量/latency/throughput
- Availability：SLO、故障恢复、degraded mode
- Security：访问控制、隔离、审计、加密
- Scalability：预期增长、扩容触发点、扩容方式
- Compatibility：旧系统、API/version、客户端兼容
- Deployability：Cloud / private / hybrid / on-prem / air-gapped
- Recoverability：backup、restore、RPO/RTO、replay
- Maintainability：deploy frequency、change isolation、operational complexity
- Cost：月成本、单请求/单任务/单客户成本边界

如果关键 NFR 仍然完全未知且会导致架构分叉，不能宣告 G1 Build Ready。

---

## 4. Mandatory High-impact Decision Families

按适用性判断，不是每个项目都必须逐项生成文档。

### 4.1 Build / Buy / Integrate

候选：
- Build：自研
- Buy：采购商业产品
- Adopt：采用成熟开源产品
- Managed：使用托管服务
- Integrate：复用客户已有系统
- Hybrid：组合

重点比较：差异化价值、产品成熟度、集成成本、License/TCO、可定制性、数据控制、供应商锁定、交付速度、团队运维能力、退出成本。

### 4.2 Standard Product / Customization

候选：
- 标准产品优先
- 80% 标准 + 20% 定制
- Plugin/Extension 模式
- Full custom

优先避免把客户个性化需求硬编码进核心通用模型；必要时定义 extension boundary。

### 4.3 Architecture Style

候选：
- Modular Monolith
- Microservices
- Serverless / Functions
- Event-driven / Worker-based
- Hybrid

判断依据：Bounded Context、独立发布、故障隔离、扩缩容差异、组织边界、运维成熟度、事务复杂度、可观测性和调试成本。

默认不要因为“未来可能扩张”直接选择微服务。明确何时需要拆分的 Evolution Trigger。

### 4.4 Communication / Integration Style

候选：
- REST/HTTP
- RPC/gRPC
- Event / Message Queue
- Webhook
- CDC
- Batch/File/ETL
- Streaming
- Hybrid

判断依据：同步响应需求、延迟、吞吐、解耦、顺序、幂等、重试、回放、最终一致性、对方能力和故障传播。

### 4.5 Data / Storage

候选包括但不限于：
- PostgreSQL/MySQL
- Document/NoSQL
- Redis
- Object Storage
- Search Engine
- Vector Store
- Data Warehouse/Lake

必须先定义 authoritative source of truth，再说明辅助存储的职责。Polyglot persistence 需要实际收益，不因“不同数据类型”自动引入多个数据库。

Redis 必须说明具体用途（如 cache/session/rate-limit/ephemeral state/lock），默认不作为核心业务长期 Source of Truth。

### 4.6 Real-time / Near-real-time / Batch

判断依据：业务 freshness、用户等待时间、数据量、成本、重算能力、故障恢复、对账需求。能用批处理满足的，不因为技术偏好强行实时化。

### 4.7 Deployment Model

候选：
- Public SaaS
- Dedicated SaaS
- Private cloud
- On-prem / customer datacenter
- Hybrid
- Edge / disconnected

同时比较 managed vs self-hosted。判断：数据驻留、网络边界、客户安全要求、升级方式、运维责任、可观测性、支持成本、平台锁定、可移植性。

### 4.8 AI / Model Sourcing

候选：
- Hosted Model API
- Multi-provider routing
- Open-source self-hosted model
- Fine-tuned model
- Custom-trained model
- Hybrid

判断：quality/eval、latency、cost、privacy、data residency、throughput、GPU/ops、vendor lock-in、fallback、model/version lifecycle。

不要把“自己训练模型”当成默认高级方案；只有数据、效果、成本或控制边界证明必要时才选择。

### 4.9 Existing Enterprise System Integration

对 ERP/OA/CRM/Identity/微信/企微等，除了“能接 API”还要决定：
- system of record 在哪边
- data ownership
- anti-corruption/adapter boundary 是否需要
- sync direction
- retry/idempotency
- reconciliation
- outage/degraded behavior
- version/credential/network constraints

---

## 5. Trade-off Procedure

对于高影响或明显存在多个合理候选的决策：

1. **State the decision**：到底要决定什么。
2. **List hard constraints**：不满足就淘汰的约束。
3. **Generate 2–4 credible candidates**：不要列十个无意义方案。
4. **Compare against drivers**：至少考虑功能适配、NFR、成本、复杂度、团队、风险、锁定、迁移/恢复。
5. **Choose and explain**：明确为什么当前选择更合理。
6. **Record consequences**：得到什么、牺牲什么。
7. **Classify reversibility**：easy / moderate / hard-to-reverse。
8. **Define evolution trigger**：什么事实变化时重新评估。
9. **Define evidence**：PoC/benchmark/load test/security review/cost estimate/vendor capability 等。
10. **Persist appropriately**：当前结论进入 SYSTEM/Spec；长期重大决定进入 ADR。

可使用矩阵，但禁止用伪精确评分掩盖不确定性。分数只能辅助，关键约束和理由必须用文字说明。

---

## 6. Decision Recording Rules

### 直接写入 SYSTEM / Engineering Spec

适合：
- 当前 Solution Strategy
- Architecture Drivers
- 边界/层次/运行方式
- 组件职责
- 当前技术组合及角色
- Evolution Trigger

### 创建 ADR

当任一成立：
- 难以逆转或迁移成本高
- 跨多个模块/团队/Agent
- 会影响公共 Contract / 数据模型 / 部署拓扑
- Build/Buy/Vendor/Cloud/Database/Architecture Style 等长期重要选择
- 存在多个合理方案且未来需要知道“为什么当时这么选”

### 不需要 ADR

- 易替换的小库
- 局部实现细节
- 低风险 UI/helper 选择
- 由现有工程标准已明确规定的选择

---

## 7. Architecture Views

复杂项目的 `SYSTEM_ARCHITECTURE` 应按实际需要提供多个 View，而不是只画一张“盒子图”。常见 View：

- Context：用户/外部系统与系统边界
- Capability / Logical：业务能力、平台能力、AI 能力、数据能力、集成能力之间的关系
- Building Block / Service：模块、服务、worker、client 的职责和 ownership
- Runtime / Sequence：关键请求/任务如何流动
- Data：Source of Truth、读写路径、缓存/搜索/对象存储
- Integration：外部系统、协议、direction、failure handling
- Deployment：进程/容器/网络/环境/区域/客户机房
- Security/Trust Boundary：身份、权限、租户、敏感数据边界

不是每个项目都需要全部 View。图必须服务于工程决策，而不是为了看起来像架构文档。

---

## 8. Evolution Triggers

关键架构选择应定义“什么时候需要重新评估”，例如：

- Modular Monolith → Service split：某 bounded context 出现独立扩缩容/发布/故障隔离需求
- Direct HTTP → Queue：同步链路已造成 timeout/峰值/故障传播问题
- DB-only search → Search engine：查询能力或索引规模超出现有数据库合理边界
- Single provider AI → Multi-provider：SLA/成本/地域/效果需要故障转移
- Managed service → Self-hosted：成本、数据驻留或供应商限制达到明确阈值
- Batch → Near-real-time：业务 freshness 的收益被真实需求证明

Evolution Trigger 是未来变化的门槛，不是提前建设复杂度的理由。

---

## 9. G1 Architecture Decision Exit Criteria

在宣告 `G1 Build Ready` 前，适用时至少满足：

- 关键 Architecture Drivers 已识别，影响架构的 NFR 有边界或验证方式
- System boundary / main building blocks / ownership 明确
- 高影响 Build/Buy/Integrate 与技术组合已做 trade-off
- 关键数据 Source of Truth 明确
- 同步/异步、实时/批处理等关键运行语义明确
- 部署模型和外部集成约束明确到不会让 Coding Agent 实现分叉
- 高锁定/难逆转选择有 ADR/exit view
- 重大 UNKNOWN 已解决，或以 Owner + Trigger + Evidence 方式明确 Deferred
- 关键选择已经映射到 Spec/Contract/LLD/WP，而不是只留在聊天里

---

## 10. Anti-patterns

禁止以下默认行为：

- “大系统就微服务”
- “有异步就 Kafka”
- “有缓存就 Redis”
- “JSON 多就 MongoDB”
- “AI 产品就自训练模型”
- “企业项目就 Kubernetes”
- “客户要求定制就全部重写”
- “私有化一定比 SaaS 安全”
- “采购一定比自研便宜”
- “实时一定比批处理高级”
- 用“高性能/高可用/高扩展”替代可验证目标
- 只画架构图，不记录为什么这样组合
- 为了避免未来迁移成本，提前引入当前完全不需要的抽象层
