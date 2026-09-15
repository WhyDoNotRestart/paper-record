#!/usr/bin/env python3
"""Lint Paper Record reports for an evidence-bearing argument chain."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id,strip_frontmatter

REQUIRED=["00-论文入口.md","01-全文通读轨迹.md","02-深度说理报告.md","03-12字段证据矩阵.md","04-图表公式证据册.md","05-实验数据与复现.md","06-参考文献脉络.md","07-主张证据与边界.md"]
MARKERS=["从零理解问题","研究目的与核心问题","理论、假设与威胁模型","作者观察与思路重建","方法执行链","实验、证明或评测逻辑","图表、公式与结果证据","从结果到结论","局限、未报告信息与外推边界","复现与复用","原文证据","结构化转述","本次综合推论"]
BANNED=["采用某算法，效果较好","具有理论、方法和实践意义","见论文","详见实验部分","输入/模型/工具/指标/结论"]
ANCHOR=re.compile(r"PDF\s*(?:p\.?|page)\s*\d+|第\s*\d+\s*页|Sec\.?\s*[\w.-]+|(?:Figure|Fig\.?|Table|Eq\.?)\s*\(?\d+\)?|(?:图|表|公式)\s*\d+",re.I)
ID_RE=re.compile(r"\b(?:CLM|Claim|E|Evidence|MAT|Material)(?:[-_][A-Za-z0-9]+)+\b",re.I)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); rows=[]
    for d in paper_dirs(root,layout):
        issues=[]; files={p.name:p for p in d.glob("*.md")}; missing=[x for x in REQUIRED if x not in files]; issues += ["missing:"+x for x in missing]
        report=files.get("02-深度说理报告.md") or files.get("11-深度说理报告.md"); raw=report.read_text(encoding="utf-8-sig",errors="replace") if report else ""; text=strip_frontmatter(raw)
        for marker in MARKERS:
            if marker not in text: issues.append("report-missing:"+marker)
        if any(x in text for x in BANNED): issues.append("banned-template-phrase")
        anchors=len(set(ANCHOR.findall(text))); ids=len(set(ID_RE.findall(text))); original=len(re.findall(r"\[原文证据\]",text)); structured=len(re.findall(r"\[结构化转述\]",text)); inferred=len(re.findall(r"\[本次综合推论\]",text))
        if anchors<8: issues.append(f"unique-anchors<8:{anchors}")
        if ids<6: issues.append(f"evidence-ids<6:{ids}")
        if original<4: issues.append(f"original-evidence<4:{original}")
        if structured<2: issues.append(f"structured-restatement<2:{structured}")
        if inferred<1: issues.append("missing-inference-marker")
        if not all(x in text for x in ["是什么","如何使用","不成立"]): issues.append("missing-theory-use-failure-chain")
        if not all(x in text for x in ["作者观察","瓶颈","假设","设计选择","预期机制"]): issues.append("missing-observation-to-design-chain")
        if not all(x in text for x in ["输入","中间状态","输出","失败分支"]): issues.append("missing-method-state-fields")
        if not all(x in text for x in ["基线","变量","指标","成功判据"]): issues.append("missing-experiment-fields")
        rows.append({"paper_id":paper_id(d),"report_chars":len(raw),"unique_anchors":anchors,"evidence_ids":ids,"original_evidence":original,"structured_restatements":structured,"inferences":inferred,"issues":issues,"passed":not issues})
    result={"schema_version":4,"layout":layout,"paper_count":len(rows),"passed":all(x["passed"] for x in rows) and bool(rows),"rows":rows}; out=Path(args.out).resolve() if args.out else root/"09-质量审计/语义证据验收.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"paper_count":len(rows),"failed":sum(not x["passed"] for x in rows)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
