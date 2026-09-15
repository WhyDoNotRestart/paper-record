#!/usr/bin/env python3
"""Check that every v3 paper has a synchronized full-reading task."""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
from layout import detect_layout, paper_dirs, paper_id, rel

STAGES = ["结构","理论","作者思路","方法","实验","图表与公式","结论与局限","综合整合"]
DONE = {"done","completed","complete","finished","已完成","完成","通过","已签收"}

def cells(line): return [c.strip() for c in line.strip().strip("|").split("|")]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); task_dir=root/"09-质量审计/reading-tasks" if layout=="v3" else root/"01-批次与审计/reading-tasks"; rows=[]
 for d in paper_dirs(root,layout):
  pid=paper_id(d); candidates=sorted(task_dir.glob(f"READ-{pid}-v*.md")) if task_dir.exists() else []; issues=[]
  if not candidates: issues.append("missing-task")
  task=candidates[-1] if candidates else None
  if task:
   text=task.read_text(encoding="utf-8",errors="replace")
   for stage in STAGES:
    line=next((x for x in text.splitlines() if x.startswith("| "+stage+" |")),"")
    if not line: issues.append("missing-stage:"+stage); continue
    c=cells(line); status=c[1] if len(c)>1 else ""; artifact=c[2] if len(c)>2 else ""
    if status.lower() not in DONE: issues.append(f"stage-not-complete:{stage}:{status or 'blank'}")
    if not artifact or artifact in {"—","-","待补"}: issues.append("stage-missing-output:"+stage)
   if not re.search(r"全文整合负责人：\s*(?!$|pending|待分配)",text,re.I|re.M): issues.append("missing-integrator")
   if not re.search(r"PDF\s*(?:p\.?|page)|第\s*\d+\s*页|全文证据|Figure|Table",text,re.I): issues.append("missing-evidence-log")
   if not re.search(r"覆盖|coverage|页码/章节范围",text,re.I): issues.append("missing-coverage-log")
  rows.append({"paper_id":pid,"task_path":rel(task,root) if task else None,"issues":issues,"passed":not issues})
 result={"layout":layout,"paper_count":len(rows),"passed":all(x["passed"] for x in rows) and bool(rows),"rows":rows}
 out=Path(args.out).resolve() if args.out else root/("09-质量审计/通读任务验收.json" if layout=="v3" else "01-批次与审计/通读任务验收.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"paper_count":len(rows),"failed":sum(not x["passed"] for x in rows)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
