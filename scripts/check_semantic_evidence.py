#!/usr/bin/env python3
"""Lint the v3 main report for argument-chain and evidence markers."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id,rel
REQUIRED=["00-论文入口.md","01-全文通读轨迹.md","02-深度说理报告.md","03-12字段证据矩阵.md","04-图表公式证据册.md","05-实验数据与复现.md","06-参考文献脉络.md","07-主张证据与边界.md"]
MARKERS=["从零理解","研究目的与核心问题","理论","作者观察","设计选择","方法执行链","实验","图表","结论","局限","外推边界","原文证据","结构化转述","本次综合推论"]
BANNED=["采用某算法，效果较好","具有理论、方法和实践意义","见论文","详见实验部分","输入/模型/工具/指标/结论"]
ANCHOR=re.compile(r"PDF\s*(?:p\.?|page)|第\s*\d+\s*页|Sec\.|Figure|Fig\.?|Table|图\s*\d+|表\s*\d+|Eq\.?",re.I)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); rows=[]
 for d in paper_dirs(root,layout):
  issues=[]; files={p.name:p for p in d.glob("*.md")}; missing=[x for x in REQUIRED if x not in files]; issues += ["missing:"+x for x in missing]
  report=files.get("02-深度说理报告.md"); text=report.read_text(encoding="utf-8",errors="replace") if report else ""
  for m in MARKERS:
   if m not in text: issues.append("report-missing:"+m)
  if any(x in text for x in BANNED): issues.append("banned-template-phrase")
  anchors=len(ANCHOR.findall(text)); ids=len(set(re.findall(r"(?:CLM|Claim|E|Evidence|MAT|Material)[-_]?[A-Za-z0-9]+",text,re.I)))
  if anchors<3: issues.append(f"anchors<3:{anchors}")
  if ids<5: issues.append(f"evidence-ids<5:{ids}")
  if len(text)<5000: issues.append(f"report-chars<5000:{len(text)}")
  rows.append({"paper_id":paper_id(d),"report_chars":len(text),"anchors":anchors,"evidence_ids":ids,"issues":issues,"passed":not issues})
 result={"layout":layout,"paper_count":len(rows),"passed":all(x["passed"] for x in rows) and bool(rows),"rows":rows}; out=Path(args.out).resolve() if args.out else root/("09-质量审计/语义证据验收.json" if layout=="v3" else "01-批次与审计/语义证据验收.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"paper_count":len(rows),"failed":sum(not x["passed"] for x in rows)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
