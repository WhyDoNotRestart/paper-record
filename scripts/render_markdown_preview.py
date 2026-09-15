#!/usr/bin/env python3
"""Render a Markdown smoke preview with local images and note links resolved."""
from __future__ import annotations
import argparse,html,json,re
from pathlib import Path
from urllib.parse import unquote
from layout import resolve_local_link
IMAGE=re.compile(r'!\[([^\]]*)\]\((<[^>]+>|[^)]+)\)')
LINK=re.compile(r'(?<!\!)\[([^\]]*)\]\((<[^>]+>|[^)]+)\)')
WIKI=re.compile(r'!?\[\[([^]#|]+)(?:#[^]|]+)?(?:\|[^]]+)?\]\]')
HEADING=re.compile(r'^(#{1,6})\s+(.+?)\s*$')
def clean(raw): return raw.strip().strip("<>")
def uri(p): return p.as_uri() if p else ""
def inline(s,src,stats):
 chunks=[]; pos=0; token=re.compile(r'!\[([^\]]*)\]\((<[^>]+>|[^)]+)\)|(?<!\!)\[([^\]]*)\]\((<[^>]+>|[^)]+)\)|!?\[\[([^]#|]+)(?:#[^]|]+)?(?:\|([^]]+))?\]\]')
 for m in token.finditer(s):
  chunks.append(html.escape(s[pos:m.start()]))
  if m.group(1) is not None:
   alt,raw=m.group(1),clean(m.group(2)); p=resolve_local_link(src,raw,src.parents[0]); ok=bool(p and p.is_file()) or raw.startswith(("http://","https://","data:")); stats.append({"kind":"image","target":raw,"resolved":str(p) if p else raw,"exists":ok}); chunks.append(f'<figure><img src="{html.escape(uri(p) if ok else raw,quote=True)}" alt="{html.escape(alt,quote=True)}"><figcaption>{html.escape(alt)} — {"OK" if ok else "BROKEN"}</figcaption></figure>')
  elif m.group(3) is not None:
   label,raw=m.group(3),clean(m.group(4)); p=resolve_local_link(src,raw,src.parents[0]); ok=bool(p and p.is_file()) or raw.startswith(("http://","https://","mailto:")); stats.append({"kind":"link","target":raw,"resolved":str(p) if p else raw,"exists":ok}); chunks.append(f'<a href="{html.escape(uri(p) if ok else raw,quote=True)}">{html.escape(label)}</a> <small>— {"OK" if ok else "BROKEN"}</small>')
  else:
   raw=m.group(5).strip(); label=(m.group(6) or Path(raw).stem).strip(); p=resolve_local_link(src,raw,src.parents[0]); ok=bool(p and p.is_file()); stats.append({"kind":"wikilink","target":raw,"resolved":str(p) if p else raw,"exists":ok}); chunks.append(f'<a href="{html.escape(uri(p) if ok else raw,quote=True)}">{html.escape(label)}</a> <small>— {"OK" if ok else "BROKEN"}</small>')
  pos=m.end()
 chunks.append(html.escape(s[pos:])); return ''.join(chunks)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--source",required=True); ap.add_argument("--out"); ap.add_argument("--report"); args=ap.parse_args(); root=Path(args.root).resolve(); src=(root/args.source).resolve() if not Path(args.source).is_absolute() else Path(args.source).resolve()
 if not src.is_file(): raise SystemExit(f"source not found: {src}")
 text=src.read_text(encoding="utf-8",errors="replace"); stats=[]; blocks=[]
 for line in text.splitlines():
  h=HEADING.match(line)
  if h: blocks.append(f'<h{len(h.group(1))}>{inline(h.group(2),src,stats)}</h{len(h.group(1))}>')
  elif line.strip(): blocks.append(f'<p>{inline(line,src,stats)}</p>')
 out=Path(args.out).resolve() if args.out else root/"09-质量审计/preview.html"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(f'<!doctype html><meta charset="utf-8"><title>{html.escape(src.name)}</title><style>body{{font:14px sans-serif;max-width:1000px;margin:2rem auto;line-height:1.65}}img{{max-width:100%;max-height:520px;object-fit:contain}}figure{{margin:1rem 0;padding:1rem;background:#f7f7f7}}</style><h1>Preview: {html.escape(src.relative_to(root).as_posix())}</h1>'+''.join(blocks),encoding="utf-8")
 bad=[x for x in stats if not x["exists"]]; result={"schema_version":3,"source":src.relative_to(root).as_posix(),"preview":out.relative_to(root).as_posix() if out.is_relative_to(root) else str(out),"target_count":len(stats),"broken_count":len(bad),"passed":not bad,"targets":stats}
 if args.report: rp=Path(args.report).resolve(); rp.parent.mkdir(parents=True,exist_ok=True); rp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"source":result["source"],"preview":result["preview"],"target_count":len(stats),"broken_count":len(bad),"passed":result["passed"]},ensure_ascii=False)); return 0 if not bad else 1
if __name__=="__main__": raise SystemExit(main())
