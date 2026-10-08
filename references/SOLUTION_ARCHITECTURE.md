# Solution Architecture — Business Capability Decomposition & Stakeholder Translation

## 1. Purpose

把“客户/产品说想做什么”转换成可工程化的系统责任模型，并保证同一架构既能指导研发，也能被业务/客户/管理层理解。

这不是要求 AI 像数据库内核/JVM/分布式框架专家一样深入所有底层，而是要求具备 Solution Architecture 的核心判断：**拆系统、组合技术、解释 trade-off、识别成本与风险、把方案讲清楚。**

---

## 2. Business-to-System Decomposition

不要从“功能清单”直接跳到技术栈。按以下顺序：

`Business Outcome → Value Stream / Process → Business Capability → Domain / Responsibility → Existing/Target System → Module/Service/Contract → Technology`

### 2.1 Business Outcome

先回答：客户/用户想改变什么结果？例如减少审批周期、统一客户视图、提高采购可追踪性，而不是“要一个看板”。

### 2.2 Process / Value Stream

恢复端到端流程和关键 handoff。例：

`Supplier → Procurement → Contract → Order → Inventory → Logistics → Settlement → BI`

### 2.3 Business Capability

能力是业务“能做什么”的稳定描述，例如 Supplier Management、Approval、Customer 360、Knowledge Retrieval。

规则：
- capability 不等于页面；
- capability 不等于数据库表；
- capability 不等于 microservice；
- capability 通常比当前组织结构更稳定。

### 2.4 Existing / Target Fit-Gap

对每个 capability 标记：
- KEEP：现有能力足够，继续作为责任方；
- EXTEND：在现有产品/平台扩展；
- REPLACE：现有能力阻碍目标/NFR；
- BUY：成熟商品能力更划算；
- INTEGRATE：外部系统继续作为 Source of Truth；
- NEW：确有差异化/能力缺口，需要新建。

同时明确：business owner、data owner、system of record、主要接口、SLA/约束。

### 2.5 System Responsibility Mapping

把 capability 映射到 system/application/module responsibility。只有在这些驱动存在时才进一步拆独立服务：
- 独立 scaling profile；
- 独立 release cadence；
- failure isolation；
- security/trust boundary；
- data ownership / transaction boundary；
- team ownership；
- technology/runtime constraint。

没有这些驱动时，优先更简单的模块化架构。

---

## 3. Solution Architecture Views

复杂项目按需建立不同 View：

1. **Context View**：用户、外部系统、系统边界；
2. **Business Capability View**：业务能力与依赖；
3. **Logical/System View**：能力如何落到应用/模块/平台；
4. **Integration View**：ERP/OA/CRM/微信/第三方如何连接；
5. **Data View**：Source of Truth、读写、缓存/搜索/对象存储；
6. **Runtime View**：关键同步/异步/批处理/AI调用如何流动；
7. **Deployment View**：SaaS/私有云/客户机房/区域/网络；
8. **Security/Reliability View**：身份权限、敏感边界、监控、备份、DR。

不是每个项目都需要 8 张图；只产出能消除关键歧义的 View。

---

## 4. Stakeholder Translation

同一事实支持至少两种表达。

### Engineering View

面向研发，准确表达：
- protocol / contract；
- state/data ownership；
- consistency / transaction；
- latency / SLO；
- failure / retry / idempotency；
- topology / deployment；
- migration / rollback。

### Business / Executive View

面向客户/管理层，回答：
- 解决什么业务问题？
- 为什么不是另一种做法？
- 带来什么业务/运营收益？
- 需要付出什么成本与复杂度？
- 风险/限制在哪里？
- 对现有系统/组织有什么影响？
- 以后扩展时哪些地方可以不重做？

### Translation rule

例如工程事实：

`Queue-based asynchronous integration isolates downstream failures.`

客户表达可以是：

`把业务模块解耦后，某个下游系统短时不可用时不会直接拖垮前台流程，后续新增系统也更少改动核心业务。`

但不能把它翻译成“系统永远不会故障”。

---

## 5. Cost / Risk / Delivery Framing

Solution Architecture 不是只画图。关键方案至少说明：
- delivery time / migration effort；
- build vs buy TCO；
- cloud/API/GPU/storage/network/license/support cost；
- operational complexity；
- vendor lock-in / exit；
- security/privacy/compliance risk；
- legacy integration risk；
- skill/team dependency；
- phased delivery / 80-20 boundary。

无法可靠量化时给出估算方式和 UNKNOWN，不伪造精确数字。

---

## 6. G1 Exit Criteria

适用时，G1 前应满足：
- 复杂业务已从功能清单提升为 process/capability model；
- capability → system responsibility / Source of Truth 清楚；
- existing-vs-target fit-gap 清楚；
- 核心 Build/Buy/Integrate/Custom 边界有理由；
- Architecture Drivers / NFR 能解释主要技术组合；
- 客户/管理层版本与工程版本基于同一事实；
- Coding Agent 不需要重新猜“这个模块到底负责什么”。
