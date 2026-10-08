# Contributing to SpecMeld

SpecMeld（构序）欢迎 issue、文档改进、规则修复、doctor 检查、golden example 与可复现的工程反馈。

## 原则

1. **Evidence over claims**：缺陷请尽量附最小复现、命令、输出或具体文件位置。
2. **Do not add rules without a failure mode**：新增规则需要说明它解决过什么真实问题。
3. **Machine enforcement when deterministic**：能稳定机器检查的规则，优先 doctor + test；不能稳定机器化的，保持为按需 reference。
4. **Progressive disclosure**：不要把所有细节塞进 `SKILL.md`。
5. **No fixed document count**：不要引入“每个项目固定 N 份文档”的要求。
6. **Right-sized governance**：规则必须说明适用的 stage / risk / surface，不把高风险治理扩散到普通 feature。

## 变更流程

- Fork / branch；
- 修改实现和对应测试；
- 运行：

```bash
python -m py_compile scripts/*.py
python -m unittest discover -s tests -v
python scripts/doctor.py examples/mini-ticket-triage
python scripts/doctor.py examples/legal-consult-mini-app
python scripts/doctor.py examples/knowledge-graph-atlas
```

- 更新 `CHANGELOG.md`；
- 若改变机器行为，必须增加回归测试；
- 若改变方法论，优先更新既有 reference，只有职责明显独立时才新增 reference。

## Pull Request 最低信息

说明：问题、证据、改动、测试、兼容性影响、是否改变 Gate / template / doctor 行为。
