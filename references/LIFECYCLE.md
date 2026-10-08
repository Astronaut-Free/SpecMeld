# Lifecycle, Gates & Change

## 5 Gates

### G0 — Intent Stable
问题、用户、方向、核心范围足够清楚，可以工程化。

### G1 — Build Ready
关键业务流程/Business Capabilities（适用时）、capability→system responsibility、Acceptance、Architecture Drivers/NFR、Solution Strategy、高影响 trade-offs、边界、数据/Contract、deployment/integration constraints、security、ownership、test/CI baseline 明确；没有会导致实现分叉的关键 UNKNOWN。技术选择必须能回溯到业务能力/需求/约束，而不是只记录最终 stack。

### G2 — Integration Ready
实现、相关 tests、contract/schema changes、independent review、Current Truth reconciliation 完成；多人/多 Agent 项目还必须满足依赖 PR 顺序、ownership approval、当前 integration candidate 的 required checks、冲突处理和 post-merge verification 计划。

若 Change 触及 shared truth，G2 还要求 Change Impact Graph 已分类所有 material consumers，当前 Migration Wave 已完成，依赖 WP 已刷新到正确 baseline，不存在无兼容保护的 obsolete consumer。

### G3 — Release Ready
最终 artifact、migration/config、observability、rollback/recovery、known blockers、release approval 就绪。对有可见用户/客户验收面的发布，必须记录人工 UAT 签字；统一字段为 `PROJECT.toml [release].uat_signed_by`，G3+ 不得为空。

### G4 — Operable / Handover Ready
生产验证通过；runbook/support/incident/recovery 可用；client/EOL 时独立接管通过。

## Change Classes

### L1 Small
低风险、局部、兼容。Change 只保留 Goal/Scope/Test/Result/Truth Update。

### L2 Feature
新能力、新 flow、新 API/schema/provider。需要 Impact/Design Delta/Contracts/Migration/Review/Release。若跨模块/shared truth 传播，增加 Change Impact Graph、Migration Waves 与 Propagation Convergence。

### L3 Breaking or High-risk
核心模型/架构/技术栈/公共 Contract breaking/高风险 side effect。需要 alternatives、RFC/ADR、compatibility、migration、rollback/recovery/compensation、strong review；跨模块消费者必须显式完成 propagation classification 和 retirement/compatibility gate。

## Rollback Vocabulary

- Revert：撤代码提交
- Rollback：回旧 artifact/config
- Restore：恢复数据/状态
- Forward-fix：无法倒退时向前修复
- Compensation：现实世界 side effect 的业务反向操作
- Kill Switch：立即停止危险能力

任何 release 需要按实际风险定义 trigger、owner、scope、verification。

## Exceptions

任何绕过 Gate 的 exception 必须有：reason、owner、risk、expiry/trigger、compensating control。永久 exception 视为治理失败。

## Sunset / Retirement

项目或重大能力进入 `lifecycle = "sunset"` 时，不只删除代码：

1. 冻结新功能并记录替代方案/迁移路径；
2. 更新 README / Current Truth，明确替代系统、最后支持窗口和数据导出方式；
3. 下架或撤销 native truth 对应的 runtime、route、job、credential、DNS/provider integration；
4. 按 retention/compliance 要求归档必要文档、release/evidence、schema/migration 历史；
5. 验证 consumer/tenant/client 已完成迁移，再执行最终 retirement；
6. 保留最小审计历史，禁止为了“干净”重写已发生事实。


## Design Asset Lifecycle

项目 G0–G4 不变，但重要设计资产还有自己的验证链：

`DRAFT → PHYSICAL_AUDIT → AUTHORITY_CHECK → CONSISTENCY_CHECK → SCENARIO_VALIDATION → INDEPENDENT_REVIEW → FREEZE_CANDIDATE → EXACT_SHA → FROZEN`

这些状态不要求分别生成文件。证据可以落在 LLD、Change、ADR、PR/MR、tests 或 machine artifact。Brownfield L2/L3 设计若 `authority_status` 为 `AMENDMENT_REQUIRED / CONFLICT / UNKNOWN`，或 `physical_reality_audit` 为 `REQUIRED / BLOCKED`，不得宣称 Freeze。

治理等级与 Change Class 是不同维度：Change Class 描述变更规模/破坏性，governance_level 描述该 surface 需要多强的控制。详见 `GOVERNANCE.md`。
