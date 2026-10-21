# Contributing to SpecMeld

SpecMeld（构序）欢迎 issue、文档改进、规则修复、doctor 检查、golden example 与可复现的工程反馈。

## 原则

1. **Evidence over claims**：缺陷请尽量附最小复现、命令、输出或具体文件位置。
2. **Do not add rules without a failure mode**：新增规则需要说明它解决过什么真实问题。
3. **Machine enforcement when deterministic**：能稳定机器检查的规则，优先 doctor + test；不能稳定机器化的，保持为按需 reference。
4. **Test behavior, not wording**：doctor 的测试构造一个“只错一处”的项目并断言稳定的 issue `code`；不要写断言某段文案存在的测试，它们会把措辞固化，却证明不了行为。
5. **Keep a rule only if it moves an eval**：新增或收紧方法论规则时，用 `evals/` 跑受影响案例并在 CHANGELOG 附结果。
6. **Progressive disclosure**：不要把所有细节塞进 `SKILL.md`。
7. **No fixed document count**：不要引入“每个项目固定 N 份文档”的要求。
8. **Right-sized governance**：规则必须说明适用的 stage / risk / surface，不把高风险治理扩散到普通 feature。

## 变更流程

- Fork / branch；
- 修改实现和对应测试；
- 运行：

```bash
python -m unittest discover -s tests -v
python scripts/doctor.py --strict examples/mini-ticket-triage
python scripts/doctor.py --strict examples/legal-consult-mini-app
python scripts/doctor.py --strict examples/knowledge-graph-atlas
```

- 更新 `CHANGELOG.md`；
- 若改变机器行为，必须增加回归测试；新增阻断型检查需同时加入 `NEW_IN_x_y_BLOCKING`，让 compat 模式能平滑过渡；
- 若改变方法论，优先更新既有 reference，只有职责明显独立时才新增 reference。

## Pull Request 最低信息

说明：问题、证据、改动、测试、兼容性影响、是否改变 Gate / template / doctor 行为。
