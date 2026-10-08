# Artifact Architecture

## 1. Truth Layers

默认遵循：

- **Current Truth**：现在系统是什么；持续更新。
- **Decision Record**：为什么做了重要长期选择；被替代时 Superseded，不重写历史。
- **Execution Record**：一次 Change/WP/Migration/Release 怎么执行。
- **Evidence Record**：测试、评审、发布、事故等证明发生过什么。
- **Machine Truth**：OpenAPI、Schema/Migration、CI、Docker/IaC、Tokens、Lockfiles/SBOM、Tests/Evals 等。

## 2. 默认 1 + 3 + N（nano 例外）

### PROJECT.toml
机器可读控制面：project classification、owners、coverage、stage、Current Truth、Native Truth、artifact paths、exceptions/unknowns、collaboration、engineering pack state。

### Nano: docs/PROJECT.md
`profile=nano` 的唯一合并 Current Truth；nano 不要求 PRODUCT/SYSTEM/DELIVERY 或 Engineering Pack。

### PRODUCT.md / SYSTEM.md / DELIVERY.md
非 nano 项目的长期摘要型 Current Truth。

### changes/<id>.md
一次改变的历史。Closed 后只允许勘误或引用后续 Change，不重写过去。

### decisions/ADR-xxxx.md
长期重要、非显然且存在真实 trade-off 的决定。

### HANDOVER.md
仅 client mode、团队移交或 EOL 时生成。

## 3. Artifact Path Registry

`PROJECT.toml [artifact_paths]` 是默认目录约定。Compiler 实例化任何模板后，必须把实际路径写进 `ENGINEERING_INDEX.md` 或对应 Current Truth，禁止只写 Artifact 名不写路径。

| Template | Default destination | Create when |
|---|---|---|
| `CHANGE.md` | `changes/<change-id>.md` | L1/L2/L3 change 需要历史记录 |
| `ADR.md` | `decisions/ADR-xxxx.md` | 高影响、长期、真实 trade-off |
| `ENGINEERING_SPEC.md` | `docs/engineering/specs/<name>.md` | 独立 Owner/高风险/复杂到主文档难 Review |
| `LLD.md` | `docs/engineering/lld/<name>.md` | 跨多文件/状态/接口的可施工模块设计 |
| `WORK_PACKET.md` | `docs/engineering/work/WP-xxx.md` | G1 前拆出的实施单元 |
| `ACCEPTANCE.md` | `docs/engineering/acceptance/ACCEPTANCE.md` | Engineering Pack 核心控制文件 |
| `SOLUTION_OVERVIEW.md` | `docs/SOLUTION_OVERVIEW.md` | Client/FDE/政企/管理层需要双层表达 |
| `HANDOVER.md` | `docs/HANDOVER.md` | Client/G4/EOL/团队移交 |
| `PULL_REQUEST.md` | `.github/pull_request_template.md` | GitHub 多 actor 或需要统一 PR evidence；其他 provider 使用等价模板路径 |

未实例化的模板不算缺失。

## 4. Status Namespaces

不同 Artifact 可以有不同 lifecycle，但不得把不同概念都叫一个裸 `status` 后假装是同一回事。

### Project Gate
`PROJECT.toml.stage`：`G0_INTENT_STABLE | G1_BUILD_READY | G2_INTEGRATION_READY | G3_RELEASE_READY | G4_OPERABLE_HANDOVER_READY`

### Engineering Pack State
唯一权威在 `PROJECT.toml [engineering_pack].status`：
`NOT_COMPILED | DRAFT | DEVELOPMENT_READY | STALE | CONVERGED`

`ENGINEERING_INDEX.md` 不再复制一份 pack status。

### Core Artifact Readiness
核心 Markdown 顶部使用语言无关标记：

`<!-- sps:readiness=DRAFT -->`

进入 G1 前必须改为：

`<!-- sps:readiness=READY -->`

Doctor 只读该机器标记，不依赖中文/英文标题。

### Implementation Entry State
`entry_state: NOT_READY | READY | BLOCKED`

这是当前施工入口是否可用，不等于 Engineering Pack State。

### Work Packet Lifecycle
`PLANNED | READY | IN_PROGRESS | BUILT | VERIFIED | INTEGRATION_READY | INTEGRATED | DONE | BLOCKED`

## 5. Machine-readable Truth First

优先引用而不是复制：OpenAPI/AsyncAPI/protobuf/GraphQL、DB migration/schema/constraints/seeds、Docker/Compose/K8s/Helm、Terraform/Pulumi/CloudFormation、CI/CD YAML、manifest+lockfile+SBOM、design tokens/component library、typed config schema、executable tests/eval datasets。

## 6. Version Rules

- Current Truth 文件名稳定，不加 `final/updated/copy`。
- Git history/tag 保存版本快照。
- ADR/Change/Release/Incident 等记录 append-only 或 immutable-after-close。
- 已执行 DB migration 不修改，新增 migration。
- Breaking contracts 使用 compatibility/deprecation window。
- 代际/EOL 才 archive baseline。

## 7. Collaboration Native Controls

优先使用 provider 已验证可用的 ownership、protected branch/ruleset、required checks、PR/MR review、merge queue/train、CI workflow 等机器约束。`DELIVERY.md` 解释 policy、Owner、例外和集成顺序，不复制 provider 已经能强制的配置。

## 8. Solution Architecture Outputs

Business Capability Decomposition 与 Architecture Decision Engine 默认不新增固定项目文档。业务能力/流程保留在 PRODUCT；capability→system responsibility、Solution Strategy 与关键 trade-off 写入 SYSTEM/SYSTEM_ARCHITECTURE；高影响长期决定写 ADR。

只有业务/管理层需要独立交付时才生成 `SOLUTION_OVERVIEW.md`；大量 vendor/build-buy 决策时才生成独立 tech-selection spec。


## Archive Snapshot Is Not Current Truth

ZIP、release bundle、milestone snapshot 归类为 **Evidence/Archive Record**。它们可以证明某个时点发生过什么，但不能因为“包里有文件”就覆盖 current repository 的 Truth / ADR / LLD / machine artifacts。恢复历史设计时必须重新验证 authority 与 reality。
