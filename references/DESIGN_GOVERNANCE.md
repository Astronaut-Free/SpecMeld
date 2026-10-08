# Design Governance & Physical Reality Audit

## 1. 目标

Brownfield 设计不能先追求“方案完整”，而要先确认**不可违反的事实**。本规则解决：Frozen Design、Migration、DB Constraint/Grant、Runtime、Machine Contract、Test、Draft 文档互相冲突时，Agent 谁都不能自行折中。

## 2. Two-axis authority model

不要使用简单的“代码永远高于文档”或“Frozen 文档永远高于代码”。必须区分：

### Intent Authority
说明系统**被批准应该是什么**：Approved/Frozen Design、有效 ADR/Change、产品/安全批准。

### Reality Evidence
说明系统**当前实际上能做什么**：Physical Schema、Constraints、DB Grants、deployed/accepted Runtime、Machine Contracts、Tests、配置与运行证据。

Historical Draft、旧 ZIP、archive 只能提供背景，不能覆盖 Current Truth。

当 Intent Authority 与 Reality Evidence 不一致时，进入 conflict classification，而不是自动选边。

## 3. Brownfield pre-design audit order

对 L2/L3 governance surface，在提出新设计前按顺序核验：

1. Approved/Frozen Authority 与 current Change/ADR；
2. Physical Schema；
3. DB Constraints / indexes / uniqueness / FK；
4. DB Grants / runtime identities；
5. Accepted / deployed Runtime；
6. Machine-readable API/Event/Schema contracts；
7. Existing tests/evals；
8. Transaction boundaries / failure persistence；
9. Idempotency carrier；
10. Audit / Outbox / side-effect boundary；
11. Cross-document consistency；
12. 只在剩余空白处 `PROPOSE`。

无法验证就标记 `UNKNOWN / NOT_RUN / BLOCKED_TOOLING`，不得猜测。

## 4. Conflict classification

发现不一致时使用：

- `IMPLEMENTATION_DRIFT`：实现偏离仍有效的批准设计；
- `DOCUMENT_DRIFT`：Current/Living 文档落后于已批准且已实现事实；
- `DRAFT_DRIFT`：旧 Draft 与当前 Authority/Reality 不一致；
- `CONTRACT_GAP`：machine contract 未覆盖已存在的必要语义；
- `AUTHORITY_CONFLICT`：两个有效 Authority 对同一语义互相冲突；
- `CONTROLLED_AMENDMENT_REQUIRED`：现实证明现有批准设计需受控修改；
- `PHYSICAL_REALITY_BLOCKED`：缺少/冲突的 schema/grant/constraint/transaction 使设计无法安全冻结。

`AUTHORITY_CONFLICT / CONTROLLED_AMENDMENT_REQUIRED / PHYSICAL_REALITY_BLOCKED / UNKNOWN` 在相关 L2/L3 surface 解除前不得 Freeze。

## 5. Physical Reality Matrix

Brownfield critical LLD 按适用范围记录：

| Object | Logical owner | Physical object | PK/UNIQUE/FK | Mutable? | Runtime actor / DB role | Allowed operations | Runtime exists? | Evidence |
|---|---|---|---|---|---|---|---|---|

这张表的目的不是复制 schema，而是把设计假设与可执行事实对齐。

## 6. Permission Matrix

当 runtime 会访问受保护数据时：

| Runtime actor | DB/service identity | Object | SELECT | INSERT | UPDATE | DELETE | Reason / evidence |
|---|---|---|---|---|---|---|---|

“逻辑上应该能写”不是权限证据。

## 7. Transaction Matrix

当一次业务动作跨多个持久化/side effect：

| Operation | TX / boundary | Persisted before failure? | Rollback behavior | Failure record | Outbox / external effect | Evidence |
|---|---|---|---|---|---|---|

尤其检查：rollback 后谁保存 FAILED、重复执行由什么幂等键承载、external side effect 是否需要 compensation。

## 8. Design lifecycle

适用的设计资产按以下链条收敛：

`DRAFT → PHYSICAL_AUDIT → AUTHORITY_CHECK → CONSISTENCY_CHECK → SCENARIO_VALIDATION → INDEPENDENT_REVIEW → FREEZE_CANDIDATE → EXACT_SHA → FROZEN`

不要求为每一步生成独立文档；证据可以存在 Change、LLD、PR/MR、test 或 machine artifact 中。

## 9. Archive / ZIP rule

ZIP、release bundle、milestone snapshot 是历史快照，不承担 Current Truth。Current Truth 和 active Design Authority 应存在版本库/当前受控系统中，并有可验证 SHA/版本。
