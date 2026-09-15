# Papaer Record Skill 文件分类清单

> 本清单仅登记 Skill 本体文件，不登记或修改任何既有论文批次产物。

| 相对路径 | 业务分类 | 用途 | 处理状态 | 处理日期 |
|---|---|---|---|---|
| `FILE_CLASSIFICATION.md` | Skill治理 | Skill内部文件分类与变更追踪 | 已创建并自登记 | 2026-09-14 |
| `baseline-20260914-pre-v3.zip` | 基线与回滚 | Paper Record 3.0 修改前的 Skill 完整快照 | 已冻结 | 2026-09-14 |
| `SKILL.md` | Skill核心说明 | Paper Record 3.0 主入口与执行纪律 | 已修改/新增 | 2026-09-14 |
| `README.md` | Skill说明与传播 | 供安装者快速理解能力、触发方式和输出 | 已修改/新增 | 2026-09-14 |
| `agents/openai.yaml` | Skill元数据 | 更新Skill在界面中的定位和默认提示 | 已修改/新增 | 2026-09-14 |
| `references/skill-improvement-plan-20260914.md` | Skill治理 | 记录本轮完善计划、缺陷根因和完成标准 | 已修改/新增 | 2026-09-14 |
| `references/naming-and-folder-policy.md` | 目录与命名规范 | 定义未来批次目录、文件名和链接规则 | 已修改/新增 | 2026-09-14 |
| `references/full-paper-reading-contract.md` | 全文通读规范 | 定义从零通读、覆盖记录、论文类型适配和签收条件 | 已修改/新增 | 2026-09-14 |
| `references/matrix-12-fields-contract.md` | 12字段矩阵规范 | 把矩阵从摘要表升级为逐字段证据索引 | 已修改/新增 | 2026-09-14 |
| `references/paper-report-contract.md` | 论文报告规范 | 定义主报告结构、深度和论文特异性要求 | 已修改/新增 | 2026-09-14 |
| `references/topic-synthesis-protocol.md` | 主题综合规范 | 将主题文件改造成问题导向的研究图谱 | 已修改/新增 | 2026-09-14 |
| `references/research-gap-protocol.md` | 研究机会规范 | 让研究空白和复用资产可转成实验设计 | 已修改/新增 | 2026-09-14 |
| `references/material-usage-contract.md` | 证据与材料规范 | 确保所有佐证材料有实际用途、状态和回链 | 已修改/新增 | 2026-09-14 |
| `references/rendering-compatibility.md` | 渲染兼容规范 | 规定 Markdown/Obsidian/HTML 三种验收、媒体解码和图表双入口 | 已修改 | 2026-09-15 |
| `references/acceptance-gates.md` | 验收规范 | 定义结构、语义、证据和渲染四类完成门禁 | 已修改/新增 | 2026-09-14 |
| `references/workflow.md` | 工作流规范 | 统一从检索到深读、综合和验收的阶段顺序 | 已修改/新增 | 2026-09-14 |
| `references/schema.md` | 数据模式 | 定义未来批次的Paper、Evidence、Claim和矩阵实体 | 已修改/新增 | 2026-09-14 |
| `references/reading-task-contract.md` | 通读任务规范 | 规范下载后立即分配、阶段产物和整合签收 | 已修改/新增 | 2026-09-14 |
| `references/semantic-quality-gates.md` | 语义质量规范 | 定义从零解释、论证链、反空洞规则和人工复核边界 | 已修改/新增 | 2026-09-14 |
| `references/integration.md` | 集成规范 | 消除旧目录矛盾并明确Zotero/Obsidian同步边界 | 已修改/新增 | 2026-09-14 |
| `templates/README.md` | 模板说明 | 说明模板与生成位置，防止占位符直接交付 | 已修改/新增 | 2026-09-14 |
| `templates/reading-task.md` | 通读任务模板 | 提供下载后立即分配、阶段、覆盖日志和复核字段 | 已修改/新增 | 2026-09-14 |
| `templates/paper-report.md` | 主报告模板 | 提供从零理解、作者思路、方法、实验、图表和边界的完整叙事骨架 | 已修改/新增 | 2026-09-14 |
| `templates/matrix-12-fields.md` | 矩阵模板 | 确保12字段逐项有判断、证据、边界和材料回链 | 已修改/新增 | 2026-09-14 |
| `templates/figure-evidence-card.md` | 图表证据模板 | 保证每张图表/公式都有变量、条件、主张和外推边界 | 已修改/新增 | 2026-09-14 |
| `templates/material-usage-ledger.csv` | 材料台账模板 | 提供PDF、图表、数据、代码和参考文献的实际用途字段 | 已修改/新增 | 2026-09-14 |
| `scripts/layout.py` | 验证基础库 | 统一Paper Record 3.0目录、论文文件、frontmatter和布局识别；3.1新增媒体类型与内容校验 | 已修改 | 2026-09-15 |
| `scripts/init_paper_record.py` | 初始化工具 | 创建不覆盖旧批次的 Paper Record 3.0 新批次 | 已修改/新增 | 2026-09-14 |
| `scripts/validate_paper_record.py` | 验证工具 | 统一初始化与验证的目录规范并诚实检查布局、文件和链接 | 已修改/新增 | 2026-09-14 |
| `scripts/check_reading_task_completion.py` | 质量门禁脚本 | 检查全文任务、阶段产物、整合负责人和覆盖日志是否同步 | 已修改/新增 | 2026-09-14 |
| `scripts/check_matrix_field_richness.py` | 质量门禁脚本 | 按12字段逐项检查结论、依据、锚点、边界和证据材料ID | 已修改/新增 | 2026-09-14 |
| `scripts/check_semantic_evidence.py` | 质量门禁脚本 | 检查主报告是否有完整论证链、论文特异性锚点和证据标记 | 已修改/新增 | 2026-09-14 |
| `scripts/audit_material_usage.py` | 质量门禁脚本 | 审计材料是否存在、状态受控、实际被消费者和证据链使用 | 已修改/新增 | 2026-09-14 |
| `scripts/run_quality_gates.py` | 质量门禁编排 | 将结构、任务、语义、矩阵、材料、命名和链接检查统一为一个入口 | 已修改/新增 | 2026-09-14 |
| `scripts/check_skill_consistency.py` | Skill自检 | 检查Skill内部规范、模板、初始化目录和脚本语法是否一致 | 已修改/新增 | 2026-09-14 |
| `scripts/monitor_paper_record.py` | 质量监视器 | 周期记录所有技术门禁但禁止自动篡改完成状态 | 已修改/新增 | 2026-09-14 |
| `scripts/build_reading_nav.py` | 导航生成工具 | 为新布局生成指向主报告文件的可读导航 | 已修改/新增 | 2026-09-14 |
| `scripts/check_links.py` | 链接与渲染门禁 | 解析 Markdown/Obsidian/图片/PDF 链接并校验目标文件格式和媒体内容 | 已修改 | 2026-09-15 |
| `scripts/check_filename_policy.py` | 质量门禁脚本 | 适配新布局的稳定命名、短slug和安全扩展名检查 | 已修改 | 2026-09-14 |
| `scripts/render_markdown_preview.py` | 渲染工具 | 生成 Markdown/Obsidian/HTML 预览并进行真实媒体格式与目标加载状态检查 | 已修改 | 2026-09-15 |
| `references/independent-review-protocol.md` | 复核规范 | 定义自动门禁之后的独立语义复核抽样和签收 | 已修改/新增 | 2026-09-14 |
| `scripts/create_reading_tasks.py` | 任务生成工具 | 让PDF核验后立即生成可追踪的全文通读任务并保留已有状态 | 已修改/新增 | 2026-09-14 |
| `scripts/check_genericity.py` | 质量门禁脚本 | 检测跨论文复制段落，防止用统一模板制造伪深度 | 已修改/新增 | 2026-09-14 |
| `scripts/check_paper_reading_depth.py` | 质量门禁脚本 | 提供兼容入口检查新布局逐篇产物和基础证据深度 | 已修改/新增 | 2026-09-14 |
| `tests/test_skill_contract.py` | Skill测试 | 隔离验证初始化、有效媒体渲染、无效媒体拒绝和通读任务状态保留 | 已修改 | 2026-09-15 |
| `references/deep-reading-protocol.md` | 全文通读规范 | 清除旧版碎片文件要求，统一到Paper Record 3.0主报告结构 | 已修改 | 2026-09-14 |
| `references/hot-paper-selection-policy.md` | 筛选规范 | 修正当前日期并明确热门度、直接性和版本治理 | 已修改 | 2026-09-14 |
| `references/evidence-claim-model.md` | 证据模型 | 与3.0材料台账、Claim链和矩阵字段保持一致 | 已修改 | 2026-09-14 |
| `references/skill-improvement-plan-20260915.md` | Skill治理 | Paper Record 3.1 分阶段优化计划与完成标准 | 已创建 | 2026-09-15 |
| `references/optimization-log-20260915.md` | Skill治理 | 逐阶段优化目标、门禁、commit、push和精简报告记录 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/README.md` | 测试夹具 | 阶段 0 隔离回放说明 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/layout-version.json` | 测试夹具 | 隔离批次布局版本 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/00-开始/entry.md` | 测试夹具 | 复现 Markdown、Obsidian、图片和 PDF 链接问题 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/03-逐篇精读/P001--2024--fixture/02-深度说理报告.md` | 测试夹具 | 提供真实渲染和证据链最小样例 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/data/data.csv` | 测试夹具 | 材料使用审计的数据样例 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/code/README.md` | 测试夹具 | 材料使用审计的代码样例 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/references/reference-usage.md` | 测试夹具 | 材料使用审计的参考文献 occurrence 样例 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/材料状态样例.md` | 测试夹具 | 材料状态和受控缺失样例 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/figures/valid.png` | 测试夹具 | 阶段 0 有效/无效媒体回放资产 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/figures/invalid.png` | 测试夹具 | 阶段 0 有效/无效媒体回放资产 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/04-证据仓/P001--2024--fixture/source/P001--2024--fixture.pdf` | 测试夹具 | 阶段 0 有效/无效媒体回放资产 | 已创建 | 2026-09-15 |
| `references/peer-benchmark-20260915.md` | 生态访行 | 记录五类同类工具/工作流的公开来源与可借鉴设计点 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/baseline-observations.md` | 测试证据 | 记录阶段 0 三类基线失败及命令输出 | 已创建 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-before.html` | 测试产物 | 阶段 0 基线命令生成的审计/预览证据 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-before.json` | 测试产物 | 阶段 0 基线命令生成的审计/预览证据 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/09-质量审计/链接审计.json` | 测试产物 | 阶段 0 基线命令生成的审计/预览证据 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/09-质量审计/材料使用验收.json` | 测试产物 | 阶段 0 基线命令生成的审计/预览证据 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-after.html` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-after2.html` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-obsidian.html` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-report.html` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-after.json` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-after2.json` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-obsidian.json` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
| `tests/fixtures/phase0/batch/preview-report.json` | 测试产物 | 阶段 1 多渲染器预览和媒体校验输出 | 已生成 | 2026-09-15 |
