#!/usr/bin/env python3
"""Check that each paper has an evidence-bearing, paper-specific main report."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id,strip_frontmatter

REQUIRED=["00-论文入口.md","01-全文通读轨迹.md","02-深度说理报告.md","03-12字段证据矩阵.md","04-图表公式证据册.md","05-实验数据与复现.md","06-参考文献脉络.md","07-主张证据与边界.md"]
ANCHOR=re.compile(r"PDF\s*(?:p\.?|page)\s*\d+|第\s*\d+\s*页|Sec\.?\s*[\w.-]+|(?:Figure|Fig\.?|Table|Eq\.?)\s*\d+|(?:图|表|公式)\s*\d+",re.I)
EVIDENCE=re.compile(r"\b(?:E|MAT|CLM|Evidence|Material|Claim)[-_][A-Za-z0-9]+\b",re.I)

def section_has_content(text:str, heading:str)->bool:
    match=re.search(rf"(?ms)^##\s+{re.escape(heading)}.*?(?=^##\s+|\Z)",text)
    if not match: return False
    block=match.group(0)
    block=re.sub(r"^#{1,6}[^\n]*$", "", block, flags=re.M)
    block=re.sub(r"\[[^\]]+\]", "", block)
    block=re.sub(r"[`|_\- ]+", "", block)
    return len(block.strip()) >= 40

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); rows=[]
    for d in paper_dirs(root,layout):
        report=d/("02-深度说理报告.md" if layout=="v3" else "11-深度说理报告.md")
        raw=report.read_text(encoding="utf-8-sig",errors="replace") if report.exists() else ""
        text=strip_frontmatter(raw)
        missing=[f for f in REQUIRED if layout=="v3" and not (d/f).is_file()]
        required_sections=["从零理解问题","研究目的与核心问题","理论、假设与威胁模型","作者观察与思路重建","方法执行链","实验、证明或评测逻辑","图表、公式与结果证据","从结果到结论","局限、未报告信息与外推边界","复现与复用"]
        missing_sections=[s for s in required_sections if not section_has_content(text,s)]
        anchors=len(set(ANCHOR.findall(text)))
        evidence_ids=len(set(EVIDENCE.findall(text)))
        evidence_facts=len(re.findall(r"\[原文证据\]",text))
        structured=len(re.findall(r"\[结构化转述\]",text))
        inferences=len(re.findall(r"\[本次综合推论\]",text))
        theory_triplet=all(x in text for x in ["是什么","如何使用","不成立"])
        method_fields=all(x in text for x in ["输入","中间状态","输出","失败分支"])
        experiment_fields=all(x in text for x in ["基线","变量","指标","成功判据"])
        issues=[]
        if missing: issues += ["missing:"+x for x in missing]
        if missing_sections: issues += ["section-empty:"+x for x in missing_sections]
        if anchors<8: issues.append(f"unique-anchors<8:{anchors}")
        if evidence_ids<6: issues.append(f"evidence-ids<6:{evidence_ids}")
        if evidence_facts<4: issues.append(f"original-evidence<4:{evidence_facts}")
        if structured<2: issues.append(f"structured-restatement<2:{structured}")
        if inferences<1: issues.append("missing-inference-marker")
        if not theory_triplet: issues.append("missing-theory-use-failure-chain")
        if not method_fields: issues.append("missing-method-state-fields")
        if not experiment_fields: issues.append("missing-experiment-fields")
        rows.append({"paper_id":paper_id(d),"report_chars":len(raw),"unique_anchors":anchors,"evidence_ids":evidence_ids,"original_evidence":evidence_facts,"structured_restatements":structured,"inferences":inferences,"missing":missing,"missing_sections":missing_sections,"issues":issues,"passed":not issues})
    result={"schema_version":4,"layout":layout,"paper_count":len(rows),"passed":all(r["passed"] for r in rows) and bool(rows),"rows":rows}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/逐篇深度验收.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"paper_count":len(rows),"failed":sum(not r["passed"] for r in rows)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
