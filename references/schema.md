# Paper Record 3.1 数据模式

## 核心实体

```text
Batch → Paper → ReadingTask → Material → Evidence → Claim
                              ├→ Figure/Table/Formula
                              ├→ Dataset/Code
                              └→ ReferenceOccurrence
Claim → MatrixField → Report/Topic/Gap/Asset
```

## Paper frontmatter

```yaml
record_type: paper
layout_version: 3
paper_id: P001
zotero_item_id: ITEMKEY
title: "full title"
short_slug: short-slug
year: 2024
version: published-v1
source_quality: peer-reviewed | preprint | report
relevance: direct-LLM-crypto | AI-assisted-cryptanalysis | cryptography-for-LLM | crypto-adjacent | out-of-scope
source_pdf: ../../04-证据仓/P001--2024--short-slug/source/P001--2024--short-slug.pdf
fulltext_status: verified | partial | unavailable
reading_status: queued | reading | read | independently-reviewed | completed
evidence_status: pending | partial | evidence-rich | needs-review
```

## Material 字段

```yaml
material_id: MAT-P001-004
material_path: 04-证据仓/P001--2024--short-slug/figures/P001--FIG-02--method.png
kind: pdf | figure | table | formula | dataset | code | reference | supplementary
source_version: v1
sha256: "..."
usage_status: core-argument | method | result | limitation | background | reproduction | context-only | unused-with-reason | unavailable | needs-review
actual_consumer: 03-逐篇精读/P001--2024--short-slug/02-深度说理报告.md
report_sections: "4;7"
topic_sections: ""
occurrence_locators: "PDF p.5, Fig. 2"
render_status: passed | failed | not-applicable | not-run
notes: ""
```

## Evidence 字段

```yaml
evidence_id: E-P001-004
material_id: MAT-P001-004
kind: text | figure | table | formula | dataset | code | reference
locator: "PDF p.5, Sec. 3.1, Fig. 2"
observation: "可核验事实"
strength: direct | partial | contextual | conflicting | unverified
supports: [CLM-P001-003]
boundary: "不能推出的内容"
```

## Claim 字段

```yaml
claim_id: CLM-P001-003
owner: author | structured-restatement | synthesis
text: "主张文本"
evidence_ids: [E-P001-004]
field_ids: [F06, F08]
report_sections: ["4", "8"]
confidence: high | medium | low
```

## ReferenceOccurrence 字段

```yaml
reference_occurrence_id: R-P001-003
bibliography_key: "[3]"
locator: "PDF p.2, Introduction"
role: theory | method | dataset | baseline | related-work | background | context-only | conflicting | needs-review
supports: [CLM-P001-001]
consumer: 02-深度说理报告.md
```

## 追踪规则

所有核心材料必须沿以下方向可追踪：

```text
Material → Evidence → Claim → Matrix Field → Report/Topic/Opportunity
```

同时支持反向检查：

```text
Report/Matrix/Topic 中的关键 ID
→ 是否存在 Claim/Evidence
→ 是否存在 Material
→ Material 是否真实可用或有受控缺失状态
```

缺失信息使用受控状态，不填猜测值。保存但未进入论证的材料必须标记 `context-only` 或 `unused-with-reason`，不能计为已使用。
