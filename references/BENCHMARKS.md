# Benchmark Synthesis

本 Skill 不是复制下列项目，而是吸收其成熟原则，并刻意避免它们在当前目标下的复杂度。研究基线：2026-10-03 前可见 main HEAD。

| 项目 | 研究 SHA | 吸收 | 不照搬 |
|---|---|---|---|
| microsoft/code-with-engineering-playbook | `016770e43d8a75be87b98c000c049f07c4a6e6f8` | Engineering Fundamentals、DoR/DoD、WIP、Design/Code Review、CI/CD、DevEx、Security、Observability、版本策略 | 大量独立指南不直接映射成项目文档 |
| github/spec-kit | `acf43471bd0fba70420c6d801fb3b29c6a96b043` | Constitution、Specify→Plan→Tasks→Implement→Converge、living/flow-forward/flow-back | 小改动不强制走完整 SDD 仪式 |
| Fission-AI/OpenSpec | `bfa670eda91c6cd998d42248ceab2b565db932ff` | Proposal/Specs/Design/Tasks/Apply/Archive、Brownfield、shared spec store | 不为每次变化生成多文件目录 |
| bmad-code-org/BMAD-METHOD | `4f61d4e769e50bc11d0d5d724f48942aac699679` | right-sized planning、readiness、independent review、evidence-based retro | 不暴露大量角色/agent 给用户 |
| obra/superpowers | `8ca22dba9a94f28898bbce59f2537ff4d87c747d` | isolated work、clean baseline、TDD/verification、safe branch finish、two-stage review | 不绑定某一 harness |
| arc42/arc42-template | `32fd461c91b184777e14f7d66b4e46db936fd3e5` | goals/constraints/context/strategy/building blocks/runtime/deployment/decisions/quality/risks | 不生成 12 份架构文档；收敛到 SYSTEM spine |
| OAI/OpenAPI-Specification | `447c479c9c7136918e80a57a258fd6c84f369c7c` | machine-readable API contract | Markdown 不重复 endpoint truth |
| compose-spec/compose-spec | `914ec15d1fa498969c0df5c1d672306db3256089` | multi-container service/network/volume/config/secrets model | local Compose 不等于 production topology |
| design-tokens/community-group | `882ebd6716abef9a46d8ef5fb12e82009d6cee2e` | design tokens 作为可共享设计真值 | 不把 UI style 只写成 prose |
| buildermethods/agent-os | `475b0cac4c7c5cf2336ad5a663b691a6d3415e05` | discover existing standards、按任务注入相关标准、lightweight spec shaping | 不维护一大套重复 standards 文件 |
| garrytan/gstack | `7fca42ad8b6c707b8a38f579f72bf3c4f7de6d85` | product/design/eng/DX/security/release review lenses、QA/canary/ship | 不暴露 20+ commands；自动选择 lenses |
| jmagly/aiwg | `f91d42ed166db704020281505e1eb765b29c4a15` | provider-agnostic、preserve existing work、install/repair/verify、specialist workflows | 不引入庞大 framework graph |
| backstage/backstage | `bcf7fb1a5fa500501d3d2f64ae7983959d607cc2` | Golden Paths、Software Templates、Docs-as-Code、catalog thinking | 不要求部署 Developer Portal |
| adr/madr | `ba75bb1b20d42af5746b246ad348c202419ae681` | ADR 最小结构、状态/上下文/决策/后果 | 不为普通小决定写 ADR |

## 关键综合原则

1. **Agent OS + Brownfield** → 先发现项目自己的标准，再应用通用标准。
2. **Backstage Golden Path + BMAD right-sizing** → 开箱即用，但按风险自动变深，不让用户手动选几十个流程。
3. **Spec Kit/OpenSpec + MADR** → Current Truth、Change History、Decision History 分开。
4. **OpenAPI/Compose/Design Tokens + Docs-as-Code** → 机器事实不重复写 prose。
5. **Superpowers/gstack** → 隔离、验证、独立 Review、QA、Canary，但收敛成一个统一执行闭环。
6. **Microsoft/arc42** → 全生命周期和架构覆盖完整，但产物收敛到 3 个 Current Docs。

目标不是“功能数量超过所有项目”，而是：**在通用软件项目标准化这个单一目标上，用更少的表面复杂度覆盖更多必要控制点。**
