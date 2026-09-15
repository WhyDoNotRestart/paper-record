#!/usr/bin/env python3
"""Render a Markdown smoke preview and validate every local target."""
from __future__ import annotations
import argparse,html,json,re
from pathlib import Path
from layout import resolve_local_link,rel,target_type,validate_media

TOKEN=re.compile(r'!\[([^\]]*)\]\((<[^>]+>|[^)]+)\)|(?<!\!)\[([^\]]*)\]\((<[^>]+>|[^)]+)\)|!?\[\[([^]#|]+)(?:#[^]|]+)?(?:\|([^]]+))?\]\]')
HEADING=re.compile(r'^(#{1,6})\s+(.+?)\s*$')
EXTERNAL_PREFIX=("http://","https://","mailto:","data:","zotero:")

def clean(raw:str)->str:
    return raw.strip().strip("<>")

def file_uri(path:Path)->str:
    return path.as_uri()

def make_target(src:Path, raw:str, syntax:str, root:Path, renderer:str)->tuple[str,dict]:
    raw=clean(raw)
    if raw.startswith(EXTERNAL_PREFIX):
        row={"kind":syntax,"target":raw,"target_type":"external","resolved":raw,"exists":True,"format_valid":True,"render_status":"passed","renderer":renderer,"reason":"external-target"}
        return raw,row
    p=resolve_local_link(src,raw,root)
    exists=bool(p and p.is_file())
    directory=bool(p and p.is_dir())
    kind=target_type(p,syntax)
    media=validate_media(p) if kind in {"image","pdf"} else {"format_valid":exists and not directory,"reason":"file-ok" if exists and not directory else "missing-file"}
    valid=exists and not directory and bool(media.get("format_valid"))
    status="passed" if valid else "failed"
    row={"kind":syntax,"target":raw,"target_type":kind,"resolved":str(p) if p else "","exists":exists,"is_directory":directory,"format_valid":bool(media.get("format_valid")),"render_status":status,"renderer":renderer,"media":media}
    return (file_uri(p) if valid and p else raw),row

def inline(text:str,src:Path,root:Path,stats:list[dict],renderer:str)->str:
    chunks=[]; pos=0
    for m in TOKEN.finditer(text):
        chunks.append(html.escape(text[pos:m.start()]))
        if m.group(1) is not None:
            alt,raw=m.group(1),m.group(2); href,row=make_target(src,raw,"image",root,renderer); stats.append(row)
            state="OK" if row["render_status"]=="passed" else "BROKEN"
            chunks.append(f'<figure><img src="{html.escape(href,quote=True)}" alt="{html.escape(alt,quote=True)}"><figcaption>{html.escape(alt)} — {state}</figcaption></figure>')
        elif m.group(3) is not None:
            label,raw=m.group(3),m.group(4); href,row=make_target(src,raw,"link",root,renderer); stats.append(row)
            state="OK" if row["render_status"]=="passed" else "BROKEN"
            chunks.append(f'<a href="{html.escape(href,quote=True)}">{html.escape(label)}</a> <small>— {state}</small>')
        else:
            raw=m.group(5).strip(); label=(m.group(6) or Path(raw).stem).strip(); href,row=make_target(src,raw,"wikilink",root,renderer); stats.append(row)
            state="OK" if row["render_status"]=="passed" else "BROKEN"
            chunks.append(f'<a href="{html.escape(href,quote=True)}">{html.escape(label)}</a> <small>— {state}</small>')
        pos=m.end()
    chunks.append(html.escape(text[pos:])); return ''.join(chunks)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--source",required=True); ap.add_argument("--out"); ap.add_argument("--report"); ap.add_argument("--renderer",choices=("markdown","obsidian","html"),default="html"); args=ap.parse_args()
    root=Path(args.root).resolve(); src=(root/args.source).resolve() if not Path(args.source).is_absolute() else Path(args.source).resolve()
    if not src.is_file(): raise SystemExit(f"source not found: {src}")
    text=src.read_text(encoding="utf-8-sig",errors="replace"); stats=[]; blocks=[]
    for line in text.splitlines():
        h=HEADING.match(line)
        if h: blocks.append(f'<h{len(h.group(1))}>{inline(h.group(2),src,root,stats,args.renderer)}</h{len(h.group(1))}>')
        elif line.strip(): blocks.append(f'<p>{inline(line,src,root,stats,args.renderer)}</p>')
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/preview.html"; out.parent.mkdir(parents=True,exist_ok=True)
    body='<!doctype html><meta charset="utf-8"><title>'+html.escape(src.name)+'</title><style>body{font:14px sans-serif;max-width:1000px;margin:2rem auto;line-height:1.65}img{max-width:100%;max-height:520px;object-fit:contain}figure{margin:1rem 0;padding:1rem;background:#f7f7f7}small{color:#666}</style><h1>Preview: '+html.escape(rel(src,root))+'</h1>'+''.join(blocks)
    out.write_text(body,encoding="utf-8")
    bad=[x for x in stats if x["render_status"]!="passed"]
    result={"schema_version":4,"source":rel(src,root),"preview":rel(out,root) if out.is_relative_to(root) else str(out),"renderer":args.renderer,"target_count":len(stats),"broken_count":len(bad),"passed":not bad,"targets":stats}
    if args.report:
        rp=Path(args.report).resolve(); rp.parent.mkdir(parents=True,exist_ok=True); rp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"source":result["source"],"preview":result["preview"],"renderer":args.renderer,"target_count":len(stats),"broken_count":len(bad),"passed":result["passed"]},ensure_ascii=False)); return 0 if not bad else 1
if __name__=="__main__": raise SystemExit(main())
