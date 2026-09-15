#!/usr/bin/env python3
"""Check v3 paper output presence and basic evidence-bearing report depth."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id
REQUIRED=["00-论文入口.md","01-全文通读轨迹.md","02-深度说理报告.md","03-12字段证据矩阵.md","04-图表公式证据册.md","05-实验数据与复现.md","06-参考文献脉络.md","07-主张证据与边界.md"]
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); rows=[]
 for d in paper_dirs(root,layout):
  report=d/("02-深度说理报告.md" if layout=="v3" else "11-深度说理报告.md"); text=report.read_text(encoding="utf-8",errors="replace") if report.exists() else ""; missing=[f for f in REQUIRED if layout=="v3" and not (d/f).is_file()]; anchors=len(re.findall(r"PDF\s*(?:p\.?|page)|第\s*\d+\s*页|Sec\.|Figure|Table|图\s*\d+|表\s*\d+",text,re.I)); rows.append({"paper_id":paper_id(d),"report_chars":len(text),"anchors":anchors,"missing":missing,"passed":not missing and len(text)>=5000 and anchors>=3})
 result={"layout":layout,"paper_count":len(rows),"passed":all(r["passed"] for r in rows) and bool(rows),"rows":rows}; out=Path(args.out).resolve() if args.out else root/"09-质量审计/逐篇深度验收.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"paper_count":len(rows),"failed":sum(not r["passed"] for r in rows)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
