# Security Policy

## Scope

安全问题包括但不限于：doctor / initializer 的路径处理、命令执行边界、secret 泄漏检测绕过、归档或模板导致的敏感信息暴露、CI 权限配置缺陷。

## Reporting

公开仓库启用 GitHub Private Vulnerability Reporting 后，请优先通过私密安全报告提交。若私密报告尚未启用，请只创建**不包含漏洞细节或 secret**的公开 issue，请维护者提供私密沟通渠道。

不要在 issue、PR、example 或测试 fixture 中提交真实 token、private key、password、客户数据或生产凭据。

## Supported versions

开源初期只保证当前最新 minor release 的安全修复。旧版本如存在高风险问题，CHANGELOG 会说明受影响范围与升级建议。
