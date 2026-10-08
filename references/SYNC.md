# Continuous Synchronization & Convergence

## 1. 目标

工程文档在 Coding 开始后仍然可信。任何人或 Coding Agent 都能知道：当前真值在哪里、为什么变化、代码与文档是否一致。

## 2. Truth 层次

- Product Intent / Acceptance → `PRODUCT.md` + feature Change
- System semantics / boundaries → `SYSTEM.md` + Engineering Specs / LLD
- API/Event/Data contracts → machine-readable contract/schema/migration
- Delivery/Release/Ops policy → `DELIVERY.md` + pipeline/config
- Historical why → ADR/RFC/Change
- Actual runtime evidence → tests, deploy receipts, dashboards, logs, release records

冲突时不能自动假设 Markdown 或代码必然正确；必须判断哪个代表被批准的新意图。

## 3. Update Trigger Matrix

| Change | 必须同步 |
|---|---|
| 用户可见行为/业务规则 | PRODUCT + Acceptance + affected Spec |
| UX flow/state | PRODUCT + UX spec/design truth |
| API/Event | contract + API spec/consumers + tests |
| DB schema/data semantics | migration/schema + data/domain spec + tests |
| service/module boundary | SYSTEM + architecture/LLD + ADR if durable decision |
| runtime/container/infra | native config + SYSTEM/runtime spec + DELIVERY if release behavior changes |
| security/privacy | security spec/current truth + tests/gates |
| CI/CD/release behavior | pipeline config + DELIVERY + ops/release spec |
| AI model/prompt/RAG/tool semantics | AI spec + version registry + evals |
| rollback/recovery semantics | DELIVERY + relevant runtime/data spec + runbook/evidence |

## 4. During Implementation

### Implementation Detail
若不改变外部 Contract/用户行为/系统边界：更新 LLD/native truth 即可。

### Design Delta
若改变业务语义、接口、数据结构、状态流、失败行为：先更新 Change + affected Spec/Contract，再继续实现。

### Architecture / Breaking Delta
若改变核心架构、公共 Contract、核心数据模型、兼容性/迁移：暂停实现，先做 RFC/ADR + Migration/Compatibility/Rollback。

## 5. Cross-Module Change Propagation

当 Design/Breaking Delta 改变共享 Contract/Schema、Canonical/Domain 语义、公共权限、Event/Workflow、Projection 输入、外部集成或平台基础时，运行 `references/PROPAGATION.md`：

1. 建立 Change Impact Graph；
2. 识别 direct / material indirect consumers；
3. 标记每个消费者的 propagation state；
4. 编排最小安全 Migration Wave；
5. 把 affected WP / tests / docs / release steps 接入同一 Change；
6. 在所有受影响项收敛前，不允许把 Change 标记 Closed。

局部 Implementation Detail 且无下游消费者时不启用。

## 6. WP Completion Convergence

每个 WP 完成前验证：

1. WP Done Condition 满足
2. required tests/evals 实际运行
3. code/config/native truth 已提交
4. linked Spec/LLD 与最终实现一致
5. affected Current Truth 已同步
6. evidence 可追溯到 SHA/PR/artifact
7. 没有未解释的设计漂移

结果：`PASS | CONCERNS | FAIL`。

## 7. Feature Convergence

Feature/L2+ 完成时检查：

`Requirement → Acceptance → Spec → LLD/Contract → WP → Code → Test/Eval → Runtime Evidence`

每个关键 Requirement 至少有实现和验证路径。

## 8. Release Convergence

Release Candidate 前：

- current docs represent candidate behavior
- contract/schema versions match candidate
- tested artifact identity = deploy candidate identity
- migration/rollback config corresponds to candidate
- dashboards/alerts/runbooks cover new operational surface
- known release blockers are closed or explicitly accepted
- release notes/handover updates are prepared where applicable

## 9. Drift Handling

发现文档与代码不一致：

1. 标记 `DRIFT`
2. 找最近 Change/ADR/PR 判断 approved intent
3. 决定修 code 或修 docs
4. 在同一 Change 中收敛
5. 无法判断则升为 open decision，不得悄悄选一边


## Truth Document Change Governance

Current Truth 不是仓库里的例外文件；每次修改都走与代码相同的 Git 审计路径：

1. 在对应 Change/WP/issue 上说明为什么要改 truth；
2. 通过 branch/worktree + review/merge（单人项目至少保留 commit history）；
3. 推荐 commit message：`docs(truth): <scope> - <reason>`，或在同一实现提交中显式注明 `truth-sync`；
4. 与代码/contract 同一语义变更时优先同一 PR/MR/Change 收敛，避免“先改代码以后补文档”；
5. truth 改错时使用 Git revert 或受控 forward-fix；不要改写已共享历史来隐藏错误；
6. 回滚 truth 时同时判断对应 code/config/contract 是否也需要回滚，防止文档与 runtime 再次分叉。

`engineering_pack.last_converged_sha` 记录最近一次完成全局文档/代码收敛的 Git SHA。doctor 在可读取 Git 历史时会对明显长期漂移（>50 commits）给 warning；这只是启发式提醒，不等同于“50 个提交必然过期”。

## 10. Stable filenames

Current docs 与长期 Specs 文件名稳定。不要用 `final-final-copy` 管历史；Git history/tag + Change/ADR 管历史。

## 11. Review cadence

不设固定“每周为了更新而更新”的文档会议。更新由事件触发：

- Change approved
- Contract/Schema changed
- WP completed
- Release candidate
- Incident/Postmortem action
- Major dependency/platform change
- Handover/EOL


## Authority Conflict Handling

Brownfield 中不能用“代码永远正确”或“Frozen 文档永远正确”自动裁决。先区分：

- **Intent Authority**：Approved/Frozen Design、有效 ADR/Change；
- **Reality Evidence**：Physical Schema/Constraints/Grants、accepted runtime、machine contracts、tests/config/runtime evidence。

出现冲突时使用 `IMPLEMENTATION_DRIFT / DOCUMENT_DRIFT / DRAFT_DRIFT / CONTRACT_GAP / AUTHORITY_CONFLICT / CONTROLLED_AMENDMENT_REQUIRED / PHYSICAL_REALITY_BLOCKED`，并在同一 Change 中收敛。

## Archive / Snapshot Boundary

ZIP、milestone bundle、release archive 只做历史快照，不承担 Current Truth。当前 active truth/design 必须能在受控 repository/system 中定位到 exact version/SHA。Archive 中存在而 repository 中缺失的 Draft，默认是 historical input，不自动升级为当前 authority。
