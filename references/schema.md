# Paper Record 3.0 数据模式

## 核心实体

```text
Batch → Paper → ReadingTask → Material → Evidence → Claim
                              ├→ Figure/Table/Formula
                              ├→ Dataset/Code
                              └→ ReferenceUsage
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

## Evidence字段

```yaml
evidence_id: E-P001-004
material_id: MAT-P001-PDF
kind: text | figure | table | formula | dataset | code | reference
locator: "PDF p.5, Sec. 3.1, Fig. 2"
observation: "可核验事实"
strength: direct | partial | contextual | conflicting | unverified
supports: [CLM-P001-003]
boundary: "不能推出的内容"
```

## Claim字段

```yaml
claim_id: CLM-P001-003
owner: author | structured-restatement | synthesis
text: "主张文本"
evidence_ids: [E-P001-004]
field_ids: [F06, F08]
confidence: high | medium | low
```

所有ID必须稳定、可回链、不可用文件行号代替。缺失信息使用受控状态，不填猜测值。
