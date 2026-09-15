#!/usr/bin/env python3
"""Audit local Markdown/Obsidian links and validate image/PDF content."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import resolve_local_link,rel,target_type,validate_media

WIKILINK=re.compile(r'!?\[\[([^]#|]+)(?:#[^]|]+)?(?:\|[^]]+)?\]\]')
MDLINK=re.compile(r'(?<!\!)\[([^]]*)\]\(([^)]+)\)')
IMAGE=re.compile(r'!\[([^]]*)\]\(([^)]+)\)')
EXTERNAL_PREFIX=("http://","https://","mailto:","data:","zotero:")

def audit(src:Path, raw:str, syntax:str, root:Path) -> dict|None:
    target=raw.strip().strip("<>")
    if not target or target.startswith(EXTERNAL_PREFIX):
        return None
    p=resolve_local_link(src,target,root)
    exists=bool(p and p.is_file())
    directory=bool(p and p.is_dir())
    kind=target_type(p,syntax)
    media=validate_media(p) if kind in {"image","pdf"} else {"format_valid": exists and not directory, "reason":"file-ok" if exists and not directory else "missing-file"}
    return {"source":rel(src,root),"syntax":syntax,"target":target,"target_type":kind,"resolved":rel(p,root) if p and p.is_relative_to(root) else str(p) if p else "","exists":exists,"is_directory":directory,"format_valid":bool(media.get("format_valid")),"media":media,"render_status":"not-run","renderer":"html"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); rows=[]
    for src in root.rglob("*"):
        if not src.is_file() or src.suffix.lower() not in {".md",".html"} or "99-原始归档" in src.parts: continue
        text=src.read_text(encoding="utf-8-sig",errors="replace")
        for m in WIKILINK.finditer(text):
            row=audit(src,m.group(0)[2:-2].split("#",1)[0].split("|",1)[0],"wikilink",root)
            if row: rows.append(row)
        for m in IMAGE.finditer(text):
            row=audit(src,m.group(2),"image",root)
            if row: rows.append(row)
        for m in MDLINK.finditer(text):
            row=audit(src,m.group(2),"markdown",root)
            if row: rows.append(row)
    bad=[r for r in rows if not r["exists"] or r["is_directory"] or not r["format_valid"]]
    result={"schema_version":4,"root":str(root),"link_count":len(rows),"broken":bad,"directory_targets":[r for r in rows if r["is_directory"]],"invalid_media":[r for r in rows if not r["format_valid"] and r["target_type"] in {"image","pdf"}],"rows":rows}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/链接审计.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"passed":not bad,"link_count":len(rows),"broken_count":len(bad),"invalid_media":len(result["invalid_media"])},ensure_ascii=False)); return 0 if not bad else 1
if __name__=="__main__": raise SystemExit(main())
