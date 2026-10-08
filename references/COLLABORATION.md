# Collaboration & Provider Integration Standard

## Purpose

多人或多 Agent 开发最危险的不是单个任务写错，而是多个“局部正确”改动在集成后变成全局错误。本规范把并行、所有权、PR、Required Checks、Merge Queue/Integrator 和集成验证作为工程设计的一部分。


## Provider Abstraction

`PROJECT.toml [collaboration].provider` 决定平台术语和可用机器机制；流程语义保持一致：review、ownership、required checks、integration ordering、post-merge verification。

| Provider | Change review | Ownership | Protected integration | Queue / serialization | Typical native mechanism |
|---|---|---|---|---|---|
| GitHub | Pull Request | CODEOWNERS / rulesets | protected branch + required checks | Merge Queue or Integrator | Actions / Rulesets |
| GitLab | Merge Request | CODEOWNERS / approval rules | protected branch + pipelines | Merge Trains or Integrator | CI/CD / approval rules |
| Gitee | Pull Request | reviewer/path ownership policy or project rule | protected branch + CI when available | provider queue if verified, otherwise Integrator | Gitee CI / repo protection as actually available |
| local | branch/worktree handoff | explicit WP owner | designated Integrator | serialized by DAG | local tests + signed-off handoff; no platform claims |

只有在实际验证 provider 能力后才能声称某项机器门禁已启用；否则记录为 `NOT_VERIFIED` 并使用等价人工/CI 机制。

## 1. Roles

- **Work Owner / Implementer**：只负责一个 WP 的实现与证据。
- **Reviewer**：独立检查 Spec/Contract compliance 与 code quality；可以多人/多 lens。
- **Integrator**：人类或指定 Integration Agent；负责依赖顺序、合并、冲突跨边界判断、post-merge verification。
- **Release Owner**：负责 release gate；不等同于 Integrator，除非项目明确合并角色。

实现者默认不自合并。小型单人项目可在 `DELIVERY.md` 明确合并角色，但仍需保留“实现完成”和“集成验证”两个不同状态。

## 2. Parallelism Algorithm

1. Build WP Dependency DAG.
2. Build expected write-set overlap graph.
3. Mark shared contracts/schema/migrations/common libraries/design tokens as hotspots.
4. Create parallel groups only for WPs with no dependency edge and no unresolved ownership collision.
5. For collisions: extract/stabilize boundary, serialize, or assign one owner and downstream consumers.
6. Record exact integration order.

`no dependency != parallel safe`.

## 3. Isolation

Default: one WP → one isolated branch/worktree.

Never:
- two agents writing in the same worktree;
- two WPs owning the same DB migration or public contract simultaneously;
- one agent silently modifying another WP's files to “make it work”.

Each WP records `base_branch`, `baseline_sha`, `branch_or_worktree`, `owner`, `integrator`.

## 4. Shared Hotspots

Typical hotspots:
- API/Event schemas
- DB schema/migrations
- shared types/SDKs
- auth/permission model
- common libraries
- root package manifests/lockfiles
- global config
- design tokens/component primitives
- CI/release workflows

Preferred strategy: smallest stable foundational change first, merge it, then fan out dependent WPs.

## 5. Pull Request Contract

PR must navigate to authoritative artifacts, not duplicate them. It should expose:
- Change/WP ID
- target/base
- dependency PRs
- final SHA
- contract/schema/migration impact
- evidence/tests/evals
- truth/spec/lld sync
- release/rollback impact
- unresolved risk/debt

## 6. Integration Gate

Integration eligible only when applicable:
- dependencies satisfied;
- correct target;
- current integration candidate passes Required Checks;
- independent review complete;
- ownership approvals complete;
- no unresolved blocking discussion;
- contracts/schema/migrations compatible or migration approved;
- docs/native truth synchronized;
- release-impacting rollback/recovery known;
- post-merge verification ready.

## 7. Provider Machine Enforcement

When the selected provider exposes equivalent capabilities, prefer enforcing policy with:
- default-branch protection / repository rulesets;
- required status checks;
- required PR reviews;
- CODEOWNERS (GitHub/GitLab where supported) or equivalent ownership rules;
- merge queue / merge train / designated Integrator when concurrency or staleness warrants it;
- CI workflows for integration/e2e/contracts/security/migrations.

Do not claim a rule is enforced unless repository settings or workflow state were actually verified.

## 8. Provider Queue/Train vs Serialized Integrator

Use the provider-native queue/train only when verified and useful for high change concurrency/high churn. Otherwise a designated Integrator serializes according to DAG.

The standard does not require rebasing for aesthetics. It requires the exact integration candidate to be verified against current target state.

## 9. Conflict Handling

Mechanical conflict inside one WP's ownership → implementer can resolve after baseline refresh.

Conflict crossing ownership/contract/schema/architecture/security/acceptance → Integrator stops merge and treats it as a design/change event. Update Spec/ADR/Change first.

Force-push is never an automatic conflict strategy; follow explicit project policy and approval.

## 10. Handoff Contract

Before handoff, Work Owner records in WP:
- final SHA/PR;
- exact commands/results;
- dependency SHAs used;
- changed contract/schema/migrations;
- Current Truth/Spec/LLD sync;
- unresolved risk/drift;
- next Integrator action.

Chat memory is not the authoritative handoff channel.

## 11. Post-Merge Gate

After integration:
1. verify default branch CI/integration suite;
2. verify generated/native contracts consistency;
3. update downstream WP baselines;
4. run Convergence for merged increment;
5. if failed, stop downstream merges and select revert/rollback/forward-fix based on risk.

## 12. Completion States

`BUILT` → implementation done.

`VERIFIED` → WP tests/review passed.

`INTEGRATION_READY` → PR meets integration gate.

`INTEGRATED` → merged/queued result landed and post-merge checks pass.

`DONE` → Current Truth / evidence / dependent-state reconciliation completed.
