# papaer-record Skill打磨报告（2026-09-14，全文通读与证据矩阵专项）

## 1. 验料结论

**好料，继续打磨。** 用户问题成立且具有明确痛点：下载PDF后如果没有强制阅读队列和证据门禁，矩阵会退化成摘要搬运，论文笔记和分类目录也会变成空模板。当前Skill的独特性不在“能总结论文”，而在于把 Zotero、全文通读责任、Obsidian证据链、图表卡和可验收矩阵串成一个可回滚流程。

本轮只打磨一个面：**全文通读之后的证据化总结与矩阵/笔记交付质量**。未扩展真实Zotero/Obsidian连接器，也未承诺自动替代人工阅读。

## 2. 访行记录

| 同类项目 | 链接 | 类型 | 可学的手艺 | 本Skill的取舍 |
|---|---|---|---|---|
| Awesome Academic Skills | [GitHub](https://github.com/O0000-code/awesome-academic-skills) | 间接/生态索引 | 按研究生命周期组织技能，并展示许可证、网络权限和运行方式 | 保留本Skill的单一流程定位，不做大而全技能目录 |
| Academic Research Agent Skill | [GitHub](https://github.com/ngtiendong/Academic-Research-Agent-Skill) | 直接/工作流 | 用角色、Reality Gate、可见Artifacts、人工批准和claim verification组织研究流程 | 借鉴“任务/产物/验收”，落到论文12字段和阅读队列 |
| K-Dense Scientific Skills | [AgenticSkills目录](https://agenticskills.io/skills/claude-scientific-skills) | 间接/技能套件 | 通过大量可触发的专业子技能覆盖PDF、论文检索、同行评审和科学工具 | 不把本Skill拆成143个子Skill，先把全文阅读主链做扎实 |
| Deep Research Skill | [SkillsLLM](https://skillsllm.com/skill/deep-research-skill) | 间接/证据方法 | 记录检索hop、证据ID、来源图、反证和不确定性，并用ledger lint | 借鉴可审计证据和独立验证，采用字段证据覆盖率 |
| Research Literature Review | [MCP Market](https://mcpmarket.com/tools/skills/research-literature-review-1) | 直接/产品形态 | 把本地PDF、Zotero、Obsidian和学术API放在同一研究入口 | 不虚构连接状态；仍按本地可用工具和失败清单降级 |

同行观察：成熟项目普遍强调“可见产物、角色/阶段、证据追踪、人工门禁”，但很少把“下载后立即分配全文通读 + 12字段逐项证据回链 + 预备矩阵/证据丰富矩阵分层”写成硬合同。这是本Skill本轮应打穿的差异化。

## 3. 生态位判断

> **一句话新定位：** 下载论文后，自动把每篇论文放入可追踪的全文通读队列，并把通读结果沉淀为12字段证据化矩阵、详细Obsidian论文笔记和可回链图表卡，而不是生成一张空泛的摘要表。

目标用户：需要处理多篇论文、希望把Zotero附件转化为长期研究资产的研究生、科研人员和技术调研者。

安装理由：临时问Agent只能得到一次性摘要；本Skill交付队列、主笔记、证据清单、矩阵、图表卡、失败清单和验收状态，下一次可以恢复、复核、比较和重跑。

## 4. 过尺结果

### 当前结构评分（实测/证据）

| 维度 | 打磨前 | 本轮后 | 证据 |
|---|---:|---:|---|
| 定位清晰度 | 3/5 | 4/5 | SKILL新增“一句话新定位”和两级矩阵定义 |
| 触发与入口 | 4/5 | 4/5 | 命令覆盖第0—7阶段和优化/重跑 |
| 工作流可执行性 | 3/5 | 5/5 | `references/workflow.md`新增下载后立即生成通读队列和三遍通读 |
| 输出可见性 | 3/5 | 5/5 | 主笔记、字段证据清单、阅读任务分配表和证据丰富矩阵 |
| 证据边界 | 4/5 | 5/5 | 每字段锚点、直接证据、摘录/转述/推论分区 |
| 失败与降级 | 4/5 | 5/5 | `needs-review`、未获取/未提及/未核验和队列阻塞原因 |
| 可验证性 | 3/5 | 5/5 | validator检查12字段、证据覆盖率、矩阵14字段和图表卡合同 |
| 安装/运行摩擦 | 3/5 | 4/5 | 仍为本地工具无连接器；初始化自动生成队列模板 |
| 跨runtime中性 | 4/5 | 4/5 | 不写死Claude/Codex连接状态，保留工具降级 |

“打磨后”是结构实测分，不代表真实论文内容已自动核验；实际论文质量仍取决于全文可读性和人工验收。

### 活体/回归验证

- `py -m py_compile scripts/init_paper_record.py scripts/validate_paper_record.py`：通过。
- 初始化脚本仍为非覆盖式：只创建缺失文件，保留旧批次和人工修改。
- Validator已改为与当前阶段语义一致：Stage 2检查阅读队列；Stage 3检查预备矩阵14字段；Stage 4检查参考文献；Stage 5检查全文主笔记和字段证据；Stage 6检查图表卡。
- 本轮未拉取真实Zotero库或18篇论文回放，因此没有虚构“全文总结质量提升”的数字；真实回放列为下一轮活体任务。

## 5. 差距清单

### P0

- 真实Zotero/Obsidian连接器仍未实现；
- 当前没有自动从PDF解析正文并生成页码锚点；
- 现有旧Vault需要重新初始化或手工补上通读队列和12字段证据表；
- 任何全文不可读、版本冲突或字段证据不足的论文仍需人工复核。

### P1

- 增加从Zotero导出CSV/JSON生成阅读队列的脚本；
- 增加真实样例论文回放，测量预备矩阵到证据丰富矩阵的翻转率和缺字段率；
- 为矩阵HTML报告展示“字段证据覆盖率”和`provisional/evidence-rich`状态。

### P2

- 增加阅读进度图和分类热力图；
- 自动建议P0/P1/P2优先级；
- 增加跨论文字段差异视图。

## 6. 三个打磨方向

- **A（推荐，已执行）细修工作流**：下载后立即分配通读任务；定义三遍通读、12字段最低内容和证据覆盖率；更新模板和验证器。
- **B 精雕可见产物**：下一轮增加真实论文示例、矩阵HTML对比页、证据覆盖率图表和before/after截图。
- **C 开套件**：拆分Zotero附件治理、PDF全文解析、深读、图表和跨论文比较为多个可组合Skill；当前不做，避免过早扩大维护面。

## 7. 本轮候选改写与实际变更

| 文件 | 操作 | 结果 |
|---|---|---|
| `SKILL.md` | 重构总入口、阶段顺序、两级矩阵、12字段和队列规则 | 已完成 |
| `references/workflow.md` | 增加下载后阅读队列、Stage 5三遍通读和矩阵回填规则 | 已完成 |
| `references/schema.md` | 增加12字段最低内容、字段证据对象、矩阵状态和阅读元数据 | 已完成 |
| `references/deep-reading-protocol.md` | 新增结构/证据/综合三遍通读操作协议 | 已完成 |
| `references/acceptance-gates.md` | 增加队列、12字段100%覆盖和证据丰富矩阵门禁 | 已完成 |
| `scripts/init_paper_record.py` | 初始化时新增全文队列；大幅扩充论文笔记模板和字段证据表 | 已完成 |
| `scripts/validate_paper_record.py` | 重写为当前v3阶段语义，检查队列、14字段、12字段和图表卡 | 已完成 |
| `references/skill-polish-report-20260914.md` | 更新本轮鲁班报告和回炉清单 | 已完成 |

## 8. README/Showcase建议

当前目录没有独立README；建议公开发布时增加首屏：

- 一句话钩子：“下载论文后先排通读队列，再生成带原文锚点的12字段矩阵。”
- 3个场景：论文库整理、组会/开题前批量深读、方法选型与研究空白比较；
- 可见产物：`全文通读任务分配.md`、一篇详细论文主笔记、证据丰富矩阵行、Figure证据卡和验收报告；
- 快速开始：初始化Vault → Stage 2下载/匹配 → 查看队列 → Stage 5通读 → Stage 6图表；
- 明确“不会做什么”：不把摘要冒充全文、不在未核验时生成结论、不覆盖原始附件、不把整页截图计为图表本体。

## 9. 执行计划

### 24小时内必须完成

- [x] 合并全文通读协议、12字段合同和两级矩阵规则；
- [x] 初始化模板新增通读任务分配表和详细论文笔记；
- [x] 更新validator并完成Python语法检查。

### 3天内完成

- [ ] 用至少3篇真实PDF回放三遍通读和12字段证据覆盖；
- [ ] 记录每字段缺失/未提及/未核验比例；
- [ ] 验证预备矩阵不会被误标成证据丰富矩阵。

### 7天内完成

- [ ] 连接真实Zotero只读盘点；
- [ ] 生成矩阵HTML中的证据状态和阅读进度视图；
- [ ] 再决定是否增加CSV/JSON阅读队列生成器。

### 本轮不做

- 不实现真实Zotero/Obsidian写入适配器；
- 不承诺自动完成PDF全文理解；
- 不批量处理现有18篇论文；
- 不发布、merge或部署到真实用户环境。

## 10. 出师证书

```text
┌────────────────────────────────────────┐
│          出师证书 · 鲁班工坊            │
│                                        │
│  作品：papaer-record                   │
│  过尺：打磨前 30/45 → 打磨后 41/45（实测结构分）│
│  定位：下载后先分配全文通读，再产出证据丰富矩阵 │
│  绝活：12字段逐项回链 + 队列化三遍通读 + 两级矩阵 │
│  下一步：用真实PDF回放并统计字段证据覆盖率       │
│                                        │
│  验收师傅：鲁班                         │
└────────────────────────────────────────┘
```

## 11. 回炉清单

- 对标观察：继续关注学术研究Skill是否提供PDF-to-Markdown、证据ledger、claim verification和可见Artifacts；
- 迭代纪律：每轮只改一个主题；先冻结基线，再用真实PDF/队列/矩阵回放验证；
- 下一轮入口：3篇真实PDF回放、队列状态恢复、12字段覆盖率、矩阵HTML证据状态；
- 已知边界：自动生成的结构不等于真实通读，OCR和页码解析错误必须进入`needs-review`。

## 12. 需要用户确认的问题

1. 下一轮是否允许我用现有Vault中的真实PDF做3篇回放，并生成可对账的字段覆盖率报告？
2. 你希望`reader_lane`按“论文分类”分配，还是按“章节/任务类型（方法、实验、图表）”分配？
3. 是否需要我下一轮同时补写独立README和矩阵HTML Showcase？

## 13. 附录：参考来源

- https://github.com/O0000-code/awesome-academic-skills
- https://github.com/ngtiendong/Academic-Research-Agent-Skill
- https://agenticskills.io/skills/claude-scientific-skills
- https://skillsllm.com/skill/deep-research-skill
- https://mcpmarket.com/tools/skills/research-literature-review-1
