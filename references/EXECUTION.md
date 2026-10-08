# Execution Playbook

## Brownfield First

1. 找 deployable/current SHA。
2. 识别 build/test commands。
3. 识别 DB/schema/migrations。
4. 识别 API/contracts。
5. 识别 Docker/containers/infra/env。
6. 识别 CI/CD、observability、release path。
7. 发现 coding/testing/review conventions。
8. 对比 docs，输出 drift。
9. 只把验证后的事实写入 Current Truth。

## Work Planning

每个任务要有：goal、inputs、affected truth/contracts、dependencies、tests、rollback/repair expectation、done evidence。

跨模块/shared-truth Change 还必须先建立 Change Impact Graph，并把受影响消费者编排成 Migration Waves；不要让各 Agent 各自猜“自己是否受影响”。

不要把整个项目上下文塞给每个 Agent；只给相关 Current Truth + Change + interfaces。

## Isolation & Baseline

优先使用 harness 原生隔离；否则遵循 repo 的 branch/worktree 方式。开始前记录 clean baseline build/test 状态。

## Review

先看 spec/contract compliance，再看 code quality。根据 Change 自动选择 Product / UX / Engineering / Security-Quality / Release-Ops lenses。

实现者不能仅凭自己的检查宣布 Accepted。

## Convergence

完成前逐项核对：

`Intent → PRODUCT → SYSTEM/Contracts → Code/Config → Tests → Runtime Evidence`

任何不一致必须：修实现、更新 Current Truth、创建 ADR/Change，三者择一明确处理；禁止静默漂移。

## Multi-human / Multi-Agent Collaboration & Provider Integration

### Core model

- **One Work Packet = one isolated branch/worktree by default.** Never let multiple agents share the same writable worktree.
- **Implementer owns implementation; Integrator owns integration.** The Integrator may be a human or a specifically designated Integration Agent.
- **No self-merge by default.** An implementer may prepare/push a PR, but merge authority is separate unless the project explicitly says otherwise.
- **Dependency DAG is authoritative.** Parallelism is derived from dependencies and write-set overlap, not from the number of available agents.
- **Main/default branch stays releasable.** Integration must not knowingly land a broken combined state.

### Before parallel dispatch

For every ready WP, record:

- `base_branch` and `baseline_sha`
- isolated `branch_or_worktree`
- `owner` and `integrator`
- prerequisite WPs/PRs
- read-set / expected write-set
- owned contracts/schema/migrations
- shared hotspots
- test/eval commands
- merge prerequisites

Build a **write-set overlap graph**. Two WPs are parallel-safe only when:

1. neither depends on the other;
2. they do not both own the same contract/schema/migration;
3. overlapping files are either read-only, generated, or have an explicit single owner/integration order;
4. each WP can be independently verified.

If two WPs touch the same shared hotspot, do one of: extract/stabilize the boundary first, serialize them, or assign one owner and make the other consume the merged result. Do not rely on "we will resolve conflicts later" as the normal plan.

### Contract-first integration

When multiple WPs depend on an interface, merge the smallest stable contract/schema/foundation WP first. Downstream WPs then update to that integrated baseline. This applies especially to:

- API/event schemas
- DB schema/migrations
- shared types/SDKs
- auth/permission contracts
- design tokens/component contracts
- common libraries

### Pull Request contract

Every integration PR should identify:

- WP / Change ID
- target branch
- baseline/final SHA
- dependencies / prerequisite PRs
- contracts/schema/migrations changed
- tests/evals run and evidence
- Current Truth / Spec / LLD updates
- rollout/rollback notes when applicable
- known risks or deferred items

PR text is a navigation/index layer, not a duplicate engineering spec. Link authoritative artifacts.

### Provider Integration Gate

A PR is integration-eligible only when applicable conditions are true:

1. correct target branch and dependency order;
2. prerequisite WPs/PRs are already integrated or the merge candidate includes their exact state;
3. required CI/tests/evals are green on the current integration candidate, not merely on an obsolete baseline;
4. independent review completed;
5. CODEOWNERS/ownership approvals completed where required;
6. unresolved review conversations / blockers are closed or explicitly waived;
7. Contract/Schema/Migration changes are compatible or have approved migration strategy;
8. affected Current Truth / Spec / LLD / Native Truth are synchronized in the same change where practical;
9. rollback/recovery implications are known for release-impacting changes;
10. post-merge integration checks are defined.

### Merge queue / serialized integration

Use a merge queue when the repository supports it and concurrency/churn makes stale-green PRs likely. Otherwise the designated Integrator serializes merges according to the DAG.

Do not require rebasing purely for aesthetics. What matters is that the exact candidate being integrated has passed the required checks against the current target state.

### Conflict protocol

- The Integrator coordinates conflicts that cross WP ownership boundaries.
- An implementer may resolve conflicts inside its owned write-set after refreshing the baseline.
- A conflict that changes a public contract, schema, architecture boundary, security rule, or acceptance behavior is a design/change event, not a mechanical Git conflict. Stop and reconcile the relevant Spec/ADR/Change first.
- Never use force-push to hide integration drift. Force-push is allowed only under the project policy and explicit approval.

### Agent handoff

An agent does not hand off via chat memory alone. Before handoff it updates the WP with:

- final SHA / PR
- exact commands and results
- dependencies actually used
- changed contracts/schema/migrations
- drift or unresolved risks
- Current Truth/Spec/LLD sync status
- next actor / Integrator action required

The next actor reads the WP and linked authoritative files.

### Post-merge integration

After merge/queue completion:

1. verify default branch CI / integration tests;
2. verify generated contracts/artifacts are consistent;
3. update dependent WPs to the new baseline;
4. if the merge changes shared truth, recompute propagation state / remaining migration waves;
5. run Convergence for the merged increment;
6. if integration fails, stop downstream merges and choose revert/rollback/forward-fix according to risk.

## CI/CD

CI 至少按适用场景运行 lint/build/unit/integration/contract/security/dependency/migration/container/IaC/AI-eval。

CD 区分 artifact build、registry、environment promotion、migration、deploy、smoke、progressive rollout、post-deploy verify。

`CI PASS != DEPLOYED != PRODUCTION VERIFIED`。

## Release

锁定最终 source SHA + artifact/image digest + migration set + contract versions + config/flag snapshot。测试通过的应是将要部署的 artifact，而不是同 commit 的另一次不可追踪构建。

## Operations

至少知道：谁看、看什么、怎么告警、怎么诊断、怎么止损、怎么恢复、怎么升级。生产 incident 的修复如果改变 requirement/constraint，反馈进 Current Truth/next Change。


## Brownfield Maintained Project Route

对已经上线或长期维护的项目，不重新从模板出发。默认顺序：

`Production/Repo Reality → Authority & Truth Audit → Drift/Gap Analysis → G0–G4 Assessment → Right-sized Compilation → Evolution Plan → READY WPs`

对 governance L2/L3 surface，在写 LLD/设计前加载 `DESIGN_GOVERNANCE.md`。对普通 L1 feature 不强制完整 Physical Reality Matrix。

如果一个高治理等级 WP 被阻塞，只阻塞 dependency/write-set 相关下游；无依赖 workstream 可继续。详见 `GOVERNANCE.md`。
