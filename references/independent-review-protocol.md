# 独立复核协议

自动门禁只证明文件和部分合同，不证明密码学、机器学习或实验解释正确。每篇论文至少安排一名不负责原始撰写的复核者，使用原始PDF和证据册重新抽查。

## 复核抽样

- 研究类型、核心问题和研究目的各1项；
- 关键结果至少2项，核对页码、图表、条件和单位；
- 贡献至少1项，确认不是把已有工作重述为创新；
- 理论/威胁模型至少1项，检查假设和边界；
- 图表至少2项，核对正文、图注和数字；
- 至少1条综合推论，检查是否由多条直接证据支持；
- 复现清单中的环境、数据、参数和代码状态。

## 签收字段

```yaml
reviewer: ""
source_pdf_reopened: true
sampled_evidence_ids: []
corrections: []
semantic_risks: []
conclusion_boundary_ok: true
review_status: passed | needs-revision
reviewed_at: "YYYY-MM-DD"
```

复核者不能只看主报告或摘要；发现越界时，任务退回 `needs-optimization` 并记录具体句子和原文定位。
