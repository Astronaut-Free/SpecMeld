<!-- sps:readiness=DRAFT -->
# System Current Truth

> 描述当前系统如何工作。能由 machine-readable artifact 表达的事实只链接，不重复抄写。

## Context & Boundaries

## Architecture Drivers / Quality Attributes

> 只记录真正改变架构的业务约束/NFR。优先给出可测量边界或验证方式，而不是“高性能/高可用”。

- Scale / concurrency / data growth:
- Latency / throughput / freshness:
- Availability / degraded mode:
- Security / privacy / permission / data residency:
- Compatibility / external systems:
- Deployment / operating constraints:
- RPO / RTO / recovery:
- Cost / time-to-market / team capability:

## Solution Strategy & Key Trade-offs

- Build / Buy / Integrate / Managed strategy:
- Standard vs custom/extension boundary:
- Architecture style and why:
- Sync/async + realtime/batch strategy:
- Data/storage strategy and source(s) of truth:
- Deployment model and why:
- AI/model sourcing strategy (if applicable):

| Decision | Chosen option | Credible alternatives | Why now | Reversibility / exit | Evolution trigger | ADR |
|---|---|---|---|---|---|---|

## Business Capability → System Responsibility Mapping

> 先说明业务能力如何映射到系统责任，再决定模块/服务。不要把 capability、domain、module、service 当成同一个东西。

| Business capability / process | Existing system / source of truth | Target system responsibility | Build / Buy / Integrate / Extend | Owner | Main dependencies |
|---|---|---|---|---|---|

## Architecture Views

> 只保留对当前项目有价值的 View：Context / Capability / Building Block / Runtime / Data / Integration / Deployment / Security。图必须解释边界和 flow，不为“看起来像架构”而画。

## Building Blocks / Ownership Boundaries

## Runtime & Key Flows

## Data & Storage

- Core entities/state:
- Database/schema authoritative files:
- Transactions/constraints/indexing:
- Migration/backfill:
- Object/file storage:
- Persistent volumes:
- Cache/search/index:
- Retention/deletion:
- Backup/restore/RPO/RTO:

## API / Event / Webhook / External Integrations

- Contract authoritative files:
- Auth/version/error/idempotency/timeout/retry/rate limit:
- External provider limits/fallback:

## Runtime / Containers / Infrastructure

- Processes/services/workers/jobs:
- Docker/Compose/multi-container authoritative files:
- Network/ports/volumes/health/readiness:
- Production orchestrator/deployment topology:
- Infra/IaC/DNS/TLS/CDN/LB/WAF:
- Environments/config/secrets boundaries:

## Security / Privacy / Supply Chain

## Observability / Reliability / Failure & Recovery

## AI / Analytics / Other Conditional Architecture

## Authority / Physical Reality Index

> Brownfield 项目只记录 material conflicts / verified authority paths；不要复制所有 machine artifacts。

| Surface | Approved intent authority | Reality evidence | Status | Amendment / drift action |
|---|---|---|---|---|

## Native Truth Index

| Domain | Authoritative file/system | Owner |
|---|---|---|

## Architecture Decisions

- Linked ADRs:

## Stakeholder Translation

> 对 Client/FDE/企业级或多干系人项目，把同一架构事实转换为非技术表达。不能把风险、成本或限制“翻译没了”。

| Technical decision | Business problem solved | Business/operational benefit | Cost / trade-off | Risk / limitation | What changes later |
|---|---|---|---|---|---|

## Evolution Triggers

- 哪些真实条件变化时需要重新评估当前架构（例如 service split、queue/search engine、multi-provider、self-hosting、realtime processing）？

## Risks / Technical Debt / Unknowns
