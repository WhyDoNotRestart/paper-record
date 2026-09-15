# Paper Record 3.1 鲁班式优化报告

- 日期：2026-09-15
- 目标分支：`codex/luban-paper-record-3.1`
- 基线：`origin/main` / `b7fc868`
- 发布边界：不修改 `main`，不 merge、tag、release 或外部发布。

## 一、打磨前后的关键差距

| 问题 | 打磨前 | Paper Record 3.1 |
|---|---|---|
| 图表、PDF 和引用路径 | 只检查路径，伪 PNG 也可能通过，入口可能不可展示 | 统一解析器 + 文件头/MIME/解码/页数检查 + Markdown/Obsidian/HTML renderer 回放 |
| 逐篇论文报告 | 容易停在摘要、模板句或孤立笔记 | 固定“背景→瓶颈→问题→理论→观察→设计→方法→实验→证据→结论→边界”主叙事 |
| 理论和作者思路 | 没有回答理论如何使用、假设失效会怎样、为什么选择方法 | 强制记录“是什么—如何使用—不成立后果”和“观察—瓶颈—假设—设计—预期机制” |
| 材料使用 | 登记路径不代表真正使用 | `Material→Evidence→Claim→Matrix→Report/Topic/Opportunity` 双向追踪，支持 occurrence 和受控未使用 |
| 研究主题 | 02/03 文件夹容易退化为入门/进阶/高级教程 | 问题树、机制谱系、论文可比性、证据差异、失败边界和可检验机会 |
| 质量验收 | 规范、模板、脚本可能脱节 | 统一总门禁、真实小批次回放、文件分类检查和独立复核门禁 |

## 二、阶段结果和提交

| 阶段 | 结果 | commit |
|---|---|---|
| 0 验料、基线、访行 | 通过；隔离 fixture 和对标记录完成 | `fb73338` |
| 1 媒体、PDF、路径展示 | 通过；无效媒体拒绝，三种 renderer 回放 | `958646c` |
| 2 逐篇深度报告 | 通过；语义门禁拒绝空洞/泛化报告 | `7f95e8c` |
| 3 材料证据闭环 | 通过；6 类材料和反向 ID 审计 | `5f69a63` |
| 4 主题研究图谱 | 通过；教程化主题拒绝，研究机会结构化 | `7fc4c5c` |
| 5 总门禁与真实回放 | 通过；完整 v3 fixture 全绿，独立复核门禁已接入 | `da9c6d9` |
| 6 回炉与最终交付 | 通过；SKILL、README、最终报告、分类清单和最终门禁已完成 | `a494490` |

## 三、阶段 5 全绿回放证据

回放批次：`tests/fixtures/phase5-valid/batch`

- 论文：1 篇；主题包：1 个；材料：6 条；核心图表/公式卡：3 条。
- 逐篇语义：唯一全文锚点 8 个；解析出的 Evidence/Claim ID 21 个；原文证据 6 处；结构化转述 3 处；综合推论 1 处。
- 材料追踪：6/6 有用途状态；missing 0；invalid 0；orphan IDs 0。
- 通读任务：1/1 通过；8 个阶段均已完成并有产物。
- 主题决策：问题树、理论与方法谱系、论文关系、证据差异、失败边界和研究机会均通过。
- 实际展示：Markdown、Obsidian、HTML 三种离线 renderer 均 `broken_count=0`；图片真实解码、PDF 头和页数检查通过。
- 文件分类：Skill 仓库 `119/119`（阶段 5 提交后仓库跟踪文件为 161/161）已登记。
- 独立复核：第二遍静态抽查通过；抽查了 PDF、Figure 1、Table 1、Eq. 1、数据、代码、参考文献 occurrence、SI 缺失和 G01 研究机会。

统一命令：

```powershell
python -m py_compile <scripts/*.py>
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_quality_gates.py --root tests/fixtures/phase5-valid/batch --skill-root .
```

结果：8 项单元测试通过；`check_skill_consistency.py` 通过；完整回放总门禁 `passed=true`，9 个脚本检查和 3 种 renderer 均通过。

## 四、仍然明确保留的边界

1. CUA 浏览器环境在本轮返回 `Codex auth token is unavailable`，因此没有 GUI 浏览器/Obsidian 人工点击记录；当前通过的是离线 HTML 解析、媒体真实性检查和第二遍静态复核。
2. 回放是受控单论文 fixture，不代表多论文、大批次、真实 Zotero 权限、插件主题或复杂路径的全部行为。
3. 自动门禁和静态复核不能替代研究者对论文语义、实验统计、密码学安全性或机器学习因果解释的最终判断。
4. 旧批次不原地迁移；生产批次必须以新 revision 运行，并在真实材料上完成独立复核后才可标记 `completed`。

## 五、下一轮真实反馈观察点

- 真实用户是否能在 Obsidian 和独立 HTML 中打开带中文、空格、括号、锚点的 PDF/图片入口；
- 多论文主题中“可比性”是否足以阻止错误合并；
- occurrence 级参考文献角色是否能减少“登记但未论证”的材料；
- 深度报告是否仍出现“有锚点但无因果解释”的伪深度；
- 独立复核者是否能用证据卡在不看摘要的情况下快速定位结论边界。
