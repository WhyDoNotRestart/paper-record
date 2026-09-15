# Paper Record数据规范

## 1. 论文主笔记YAML

```yaml
---
title: "原文题名"
title_cn: "未提及"
authors: []
year: 2024
category: "后量子密码学"
subcategory: "格密码-密钥封装"
paper_type: "实验研究; 方法改进"
zotero_item_id: "123"
doi: "未提及"
url: "未提及"
source_type: "期刊论文"
version: "未提及"

reading_status: "已收录"
difficulty: "未核验"
importance: "未核验"
relevance: "未核验"
recommended_order: null
fulltext_status: "未获取"
figure_status: "未核验"
evidence_status: "未核验"
reproducibility_status: "未核验"

research_questions: []
supports: []
extends: []
compares_with: []
conflicts_with: []

source_verified: false
last_reviewed: "2026-09-14"
record_batch: "PR-YYYYMMDD-001"
tags:
  - "#domain/"
  - "#topic/"
---
```

空值含义：信息没有在当前证据范围内出现时使用`未提及`；文件/全文尚未拿到使用`未获取`；已有线索但还没核验使用`未核验`；字段对该论文不适用使用`不适用`。

## 2. 论文矩阵最小字段

矩阵保留以下列，长文本下沉至笔记：

```text
论文题名
分类
研究类型
研究主题
研究问题
研究目的与核心问题
研究对象与应用场景
研究方法/技术路径
数据与材料来源
主要发现/关键结果
创新点/贡献
结论摘录
实际意义/应用价值
关键词标签
文献图表
图表说明解析论证
图表数量
DOI
原文链接
Zotero Item ID
阅读状态
全文状态
证据完整度
深度笔记链接
图表解析汇总链接
批次ID
最后核验日期
```

用户明确要求14字段时，表头必须使用其原始字段名，不得用内部字段名替代；内部字段可以放在附加列或YAML中。

## 3. 证据对象

```yaml
id: "E-123-07"
paper_item_id: "123"
source_location:
  section: "Results 4.2"
  page: "8"
  paragraph: "未提及"
  figure_table: "Figure 3"
evidence_type: "实验结果"
claim: "原文主张或准确转述"
supports_question: "RQ1"
supports_conclusion: "C2"
evidence_strength: "直接证据"
interpretation_level: "原文摘录"
externality_boundary: "仅在该数据集、硬件和参数下验证"
reproduction:
  hardware: "未提及"
  software: "未提及"
  parameters: "未提及"
  dataset: "未提及"
  code: "未提及"
relation:
  type: "补充"
  targets: []
verification_status: "已核验"
```

## 4. 图表证据卡

每张图表卡遵循以下结构：

```markdown
---
record_type: figure-evidence
paper_item_id: "123"
figure_id: "Figure 3"
title: "原文标题"
figure_type: "性能曲线/参数表/流程图/框架图"
source_page: "8"
source_section: "Results 4.2"
image: "./Figure-03-性能比较.png"
verification_status: "已核验"
---

# Figure 3：原文标题

![[Figure-03-性能比较.png]]

## 图表展示内容

- 横轴：
- 纵轴：
- 变量：
- 比较对象：
- 固定条件：

## 关键观察

- 只写图表实际展示的观察，不把作者推论直接写成数据事实。

## 正文对应关系

- 原文位置：
- 对应段落主张：
- 支持程度：完全支持 / 部分支持 / 无法判断

## 研究问题与结论对应

- 支撑问题：
- 支撑子结论：
- 证据强度：

## 边界与可复现性

- 样本、硬件、软件、参数：
- 未测试场景：
- 不宜外推到：

## 跨论文关系

- 关系：支持 / 补充 / 冲突 / 重复 / 拓展 / 对比
- 目标论文：
```

图片本身只保留图表区域。图注和解释写在Markdown，不把整页截图或无关正文拼到图片内。

## 5. 参考文献溯源

建议使用两类记录：

### reference_master

```text
reference_key
normalized_title
authors
year
venue
volume
issue
pages
doi
url
bibtex
verification_status
```

### reference_occurrence

```text
source_paper_item_id
source_paper_title
reference_number
raw_reference_text
reference_key
source_location
cited_in_section
citation_context
match_confidence
verification_status
```

这样既能生成去重后的`references.bib`，又能保留“哪篇论文引用了该文献”的来源关系。

## 6. Excel工作簿建议

- `总览`：所有论文和状态；
- 每个分类一个Sheet：APA引用和矩阵简表；
- `待下载PDF`：无法获取的全文；
- `待人工复核`：错配、冲突、未核验；
- `参考文献总表`：去重后的参考文献；
- `参考文献来源关系`：来源论文和出现位置；
- `标签字典`：标签命名空间、含义和来源；
- `文件清单`：每个生成文件的业务分类、关联论文和状态。

## 7. 关系类型字典

只使用有限关系词，避免同义词泛滥：

```text
支持、补充、拓展、对比、评估、应用、重复、冲突、替代、依赖
```

关系写在论文YAML和正文中，并尽量双向链接；一侧声明后，另一侧若未同步应列入待修复清单。
