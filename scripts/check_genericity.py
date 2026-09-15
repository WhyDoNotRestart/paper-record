#!/usr/bin/env python3
"""Find repeated long prose across paper reports; repetition is a review signal."""
from __future__ import annotations
import argparse,collections,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs
IGNORE=("[原文证据]","[结构化转述]","[本次综合推论]","Evidence","Material")
def norm(line):
 s=re.sub(r"\s+"," ",line.strip()); return s if 60<=len(s)<=320 and not s.startswith(("#","|","- [","```")) and not any(x in s for x in IGNORE) else None
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); docs=[]
 for d in paper_dirs(root,detect_layout(root)):
  for name in ["02-深度说理报告.md","11-深度说理报告.md","01-从零理解.md","03-作者思路与方法.md"]:
   p=d/name
   if p.exists(): docs.append(p)
 counts=collections.defaultdict(set)
 for p in docs:
  for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
   s=norm(line)
   if s: counts[s].add(p.parent.name)
 repeated=[{"text":s,"documents":sorted(ds),"document_count":len(ds)} for s,ds in counts.items() if len(ds)>=4]; repeated.sort(key=lambda x:(-x["document_count"],x["text"]))
 result={"document_count":len(docs),"repeated_boilerplate":repeated,"passed":len(repeated)<10}; out=Path(args.out).resolve() if args.out else root/"09-质量审计/模板化风险审计.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"repeated_count":len(repeated)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
