#!/usr/bin/env python3
"""Build a simple v3 reading navigation from paper entry notes."""
from __future__ import annotations
import argparse, os, re
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id

def value(text,label):
 m=re.search(rf"(?m)^[-*]\s*{re.escape(label)}\s*[：:]\s*(.+)$",text); return m.group(1).strip() if m else "未填写"
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); out=root/"00-开始/00-阅读导航.md" if layout=="v3" else root/"00-论文阅读导航.md"; rows=[]
 for d in paper_dirs(root,layout):
  entry=d/"00-论文入口.md"; t=entry.read_text(encoding="utf-8",errors="replace") if entry.exists() else ""; target=d/"02-深度说理报告.md"; href=Path(os.path.relpath(target,out.parent)).as_posix(); rows.append(f"- [{paper_id(d)} {value(t,'题名')}]({href})")
 body="# 论文阅读导航\n\n> 只链接实际文件。\n\n"+"\n".join(rows)+"\n"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(body,encoding="utf-8"); print(f"updated {out} ({len(rows)} papers)"); return 0
if __name__=="__main__": raise SystemExit(main())
