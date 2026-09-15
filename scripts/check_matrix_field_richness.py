#!/usr/bin/env python3
"""Check every matrix field has conclusion, basis, anchor, boundary and IDs."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id,rel
FIELDS=["研究类型","研究问题","研究主题","研究目的与核心问题","研究对象与应用场景","研究方法/技术路径","数据与材料来源","主要发现/关键结果","创新点/贡献","结论摘录","实际意义/应用价值","关键词标签"]
SECTIONS=["字段结论","判断依据","全文锚点","适用条件与不确定性","Evidence / Material"]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); rows=[]
 for d in paper_dirs(root,layout):
  p=d/"03-12字段证据矩阵.md" if layout=="v3" else d/"09-12字段证据矩阵.md"; t=p.read_text(encoding="utf-8",errors="replace") if p.exists() else ""; issues=[]
  for i,name in enumerate(FIELDS,1):
   start=re.search(rf"(?m)^##\s+F{i:02d}\s+{re.escape(name)}\s*$",t)
   if not start: issues.append(f"F{i:02d}:missing-section"); continue
   nxt=re.search(r"(?m)^##\s+F\d{2}\s+",t[start.end():]); block=t[start.end():start.end()+nxt.start() if nxt else len(t)]
   for s in SECTIONS:
    if not re.search(rf"(?m)^###\s+{re.escape(s)}\s*$",block): issues.append(f"F{i:02d}:missing:{s}")
   if not re.search(r"PDF\s*(?:p\.?|page)|第\s*\d+\s*页|Sec\.|Figure|Table|图\s*\d+|表\s*\d+",block,re.I): issues.append(f"F{i:02d}:missing-anchor")
   if not re.search(r"E[-_]|MAT[-_]|证据ID|材料ID",block,re.I): issues.append(f"F{i:02d}:missing-id")
  result_chars=len(t); rows.append({"paper_id":paper_id(d),"matrix_path":rel(p,root),"chars":result_chars,"issues":issues,"passed":not issues})
 result={"layout":layout,"paper_count":len(rows),"passed":all(x["passed"] for x in rows) and bool(rows),"rows":rows}; out=Path(args.out).resolve() if args.out else root/("09-质量审计/矩阵字段验收.json" if layout=="v3" else "01-批次与审计/矩阵字段验收.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"paper_count":len(rows),"failed":sum(not x["passed"] for x in rows)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
