# Paper Record 3.1 独立复核记录

- 复核日期：2026-09-15
- 复核对象：`tests/fixtures/phase5-valid/batch`
- 复核方式：脱离实现修改的第二遍静态抽查；先看材料和证据卡，再回看主报告、矩阵、主题包和总门禁结果。
- 复核范围：1 篇论文、6 条材料、3 张图表/公式证据卡、1 个主题包、1 个研究机会。
- 复核结论：通过（静态证据链和门禁回放一致）。

## 抽查结果

| 抽查项 | 原始材料/入口 | 回链位置 | 结果 |
|---|---|---|---|
| PDF 版本、页码和结论边界 | `04-证据仓/P001--2024--valid-paper/source/P001--2024--valid-paper.pdf` | `03-逐篇精读/P001--2024--valid-paper/02-深度说理报告.md` 第 2、8、9 节 | 通过 |
| Figure 1 是否支持机制而非性能结论 | `04-证据仓/P001--2024--valid-paper/figures/P001--FIG-01--method.png` 与证据卡 | 主报告第 7 节、`CLM-P001-001` | 通过；报告明确不能单独推出性能提升 |
| Table 1 / 结果 Claim 是否带条件 | 图表证据卡与结果材料 | 主报告第 6、8 节、矩阵 F08 | 通过；限定在 D、C 和指标 Y |
| 公式 Eq. 1 是否被过度解释 | `P001--EQ-01--evidence.md` | 主报告第 7、8 节、`CLM-P001-001` | 通过；未把公式当作完整证明 |
| 数据和代码是否有实际消费者 | DATA-01、CODE-01 | 主报告第 6、10 节；材料台账 | 通过 |
| 参考文献 occurrence 角色 | `references/reference-usage.md` | 主报告第 2 节；台账 `MAT-P001-REF-01` | 通过；标为 background，未强行支持结论 |
| SI 缺失是否诚实登记 | `MAT-P001-SI-01` | 主报告第 9、10 节；台账 | 通过；状态为 unavailable |
| 主题包是否支持研究决策 | T01 七个主题文件 | 问题树、证据差异、失败边界、G01 | 通过；不是入门/进阶/高级教程 |

## 门禁复核

- `python scripts/run_quality_gates.py --root tests/fixtures/phase5-valid/batch --skill-root .`：通过，全部检查项 `passed=true`。
- `python -m unittest discover -s tests -p "test_*.py" -v`：通过，8 项测试。
- `python -m py_compile`：通过，全部 Python 脚本可编译。
- 未进行 GUI Obsidian/浏览器人工点击；当前 renderer 检查为离线 HTML 解析和媒体真实性检查，后续仍需活体浏览器验证。

## 未解决边界

1. 当前批次为受控单论文 fixture，不代表多论文、大体量或真实 Zotero 数据回放。
2. PDF/HTML 的离线解析通过不等于所有客户端主题、插件和权限设置下都能显示。
3. `completed` 仍需真实使用者以其论文材料完成一次独立复核后才能对生产批次签收。
