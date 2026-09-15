# Paper Record 3.1 鲁班优化日志

> 分支：`codex/luban-paper-record-3.1`  
> 基线：`origin/main` / `b7fc868`  
> 规则：每轮只处理一个主要问题面；每轮完成后先验收、再提交、再推送；不自动 merge。

## 阶段状态

| 阶段 | 目标 | 状态 | commit | push | 精简报告 |
|---|---|---|---|---|---|
| 0 | 验料、基线、隔离 fixture 与访行 | passed | pending | pending | 已复现三类基线失败，待提交 |
| 1 | 图表、PDF、引用路径真实展示 | queued | - | - | - |
| 2 | 逐篇深度报告与语义门禁 | queued | - | - | - |
| 3 | Material→Evidence→Claim 闭环 | queued | - | - | - |
| 4 | 主题图谱与跨论文研究决策 | queued | - | - | - |
| 5 | 总门禁、真实回放、独立复核 | queued | - | - | - |
| 6 | 回炉、文档和最终验收 | queued | - | - | - |

## 阶段报告记录

### 阶段 0

- 目标：建立可回滚基线并复现至少三类失败。
- 已完成：创建新分支；新增 3.1 优化计划；新增隔离 fixture、五类访行记录和基线失败复现。
- 验证：`check_links.py` 和 `render_markdown_preview.py` 对无效 PNG 均误报通过；`audit_material_usage.py` 明确报告台账缺失。
- 未解决：阶段 1 需要修复媒体格式和真实渲染检查；阶段 3 需要修复材料闭环。
- Git：分支已创建；阶段 0 commit 待验收。
- 下一步：进入阶段 1，修复图表、PDF 和引用路径展示。

