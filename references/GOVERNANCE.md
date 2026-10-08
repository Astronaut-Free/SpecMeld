# Progressive Governance & Right-Sizing

## 1. 目标

治理是护栏，不是主工程。控制强度由 **Project Stage + Change Risk + Affected Surface + Blast Radius** 决定，而不是所有改动统一套最高等级。

## 2. Governance Levels

| Level | Typical surface | Minimum controls | Extra controls |
|---|---|---|---|
| L1 Development | 普通 feature、bug、局部兼容改动 | branch/worktree、review、基础 CI、tests、必要 contract check | 无默认双签/重型审批 |
| L2 Critical Surface | schema、migration、shared contract、core runtime、canonical state | L1 + compatibility/migration + contract/integration gate + rollback/forward-fix | shared ownership、baseline refresh、propagation convergence |
| L3 Production / Security | identity、permission、canonical authority、release control plane、高风险生产 side effect | L2 + explicit owner/approval + audit + release/rollback controls | provider-native CODEOWNERS/approval/queue 等仅在适用且已验证时启用 |

`L1/L2/L3` 是治理强度，不替代 `Change Class L1/L2/L3`；二者名称相同但维度不同。为了避免混淆，项目文件中统一字段名为 `governance_level`。

## 3. Applicability Matrix

每条治理规则都应能回答：

- **Stage**：G0/G1/G2/G3/G4 哪个阶段开始必须？
- **Risk**：普通 / critical / security-production？
- **Surface**：feature、schema、migration、contract、identity、permission、release 等？
- **Evidence**：靠什么证明已满足？

不能回答这四项的全局 `MUST`，优先视为过度治理候选。

## 4. Stage modifiers

- G0/G1：只建立安全施工所需控制。
- G2：加强 integration / cross-module convergence。
- G3：增加 release、migration、rollback、UAT。
- G4：增加 operability、recovery、handover。

项目较早阶段也可以提前进入 L2/L3，但必须由高返工/高风险 surface 触发，例如 identity、permission、canonical truth、不可逆 migration。

## 5. Non-blocking parallel work

一个 L2/L3 change 被 Gate 阻塞时，只冻结：

- 与它有 dependency edge 的 WP；
- 写入相同 protected surface 的 WP；
- 依赖尚未冻结 contract/schema 的 downstream WP。

无依赖、无 write-set overlap 的工作可以继续。治理红灯不得自动升级成全项目停工。

## 6. Controls must match implementation

调整治理强度时必须同步检查：

`Docs Rule ↔ CI/Workflow ↔ Repository Settings ↔ CODEOWNERS/Ownership ↔ Doctor/Gate`

只改 Markdown 而机器 Gate 仍按旧规则拦截，属于治理漂移。

## 7. Review trigger

当出现以下信号时执行 Governance Right-Sizing Review：

- 普通 feature 频繁触发高风险审批；
- 一处 Gate 导致无依赖 workstream 停摆；
- 多个 Gate 重复证明同一事实；
- 维护治理的时间持续高于产品能力建设；
- 项目进入 G3/G4，需要把之前后置的生产控制正式启用。
