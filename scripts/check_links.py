#!/usr/bin/env python3
"""Audit Markdown, Obsidian, HTML links and image targets against real files."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import resolve_local_link,rel
WIKILINK=re.compile(r'!?\[\[([^]#|]+)(?:#[^]|]+)?(?:\|[^]]+)?\]\]')
MDLINK=re.compile(r'(?<!\!)\[([^]]*)\]\(([^)]+)\)')
IMAGE=re.compile(r'!\[([^]]*)\]\(([^)]+)\)')
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); rows=[]
 for src in root.rglob("*"):
  if not src.is_file() or src.suffix.lower() not in {".md",".html"} or "99-原始归档" in src.parts: continue
  text=src.read_text(encoding="utf-8",errors="replace")
  for m in WIKILINK.finditer(text):
   target=m.group(1).strip(); p=resolve_local_link(src,target,root); rows.append({"source":rel(src,root),"syntax":"wikilink","target":target,"resolved":rel(p,root) if p and p.is_relative_to(root) else str(p) if p else "","exists":bool(p and p.is_file()),"is_directory":bool(p and p.is_dir())})
  for m in MDLINK.finditer(text):
   target=m.group(2).strip(); p=resolve_local_link(src,target,root); rows.append({"source":rel(src,root),"syntax":"markdown","target":target,"resolved":rel(p,root) if p and p.is_relative_to(root) else str(p) if p else "","exists":bool(p and p.is_file()),"is_directory":bool(p and p.is_dir())})
  for m in IMAGE.finditer(text):
   target=m.group(2).strip(); p=resolve_local_link(src,target,root); rows.append({"source":rel(src,root),"syntax":"image","target":target,"resolved":rel(p,root) if p and p.is_relative_to(root) else str(p) if p else "","exists":bool(p and p.is_file()),"is_directory":bool(p and p.is_dir())})
 bad=[r for r in rows if not r["exists"] or r["is_directory"]]; result={"root":str(root),"link_count":len(rows),"broken":bad,"directory_targets":[r for r in rows if r["is_directory"]],"rows":rows}; out=Path(args.out).resolve() if args.out else root/"09-质量审计/链接审计.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":not bad,"link_count":len(rows),"broken_count":len(bad),"directory_targets":len(result["directory_targets"])},ensure_ascii=False)); return 0 if not bad else 1
if __name__=="__main__": raise SystemExit(main())
