#!/usr/bin/env python3
"""Check active batch names for stable IDs, short slugs, and safe extensions."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
ACTIVE={"02-论文台账","03-逐篇精读","04-证据仓","05-主题研究图谱","06-跨论文比较","07-研究机会","08-复现与科研资产"}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); args=ap.parse_args(); root=Path(args.root).resolve(); bad=[]
 for p in root.rglob("*"):
  if not p.is_file() or "99-原始归档" in p.parts: continue
  parts=p.relative_to(root).parts; human=any(x in ACTIVE for x in parts); name=p.name
  if human and len(name)>140: bad.append(f"{p.relative_to(root).as_posix()}:name-too-long")
  if len(name)>180: bad.append(f"{p.relative_to(root).as_posix()}:name-too-long")
  if human and p.suffix.lower() not in {".md",".html",".json",".jsonl",".csv",".tsv",".xlsx",".png",".jpg",".jpeg",".svg",".pdf",".txt",".py"}: bad.append(f"{p.relative_to(root).as_posix()}:unsupported-extension")
 print(json.dumps({"passed":not bad,"bad_count":len(bad),"bad":bad[:100]},ensure_ascii=False)); return 0 if not bad else 1
if __name__=="__main__": raise SystemExit(main())
