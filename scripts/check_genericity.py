#!/usr/bin/env python3
"""Find repeated prose and unfilled template residue across paper reports."""
from __future__ import annotations
import argparse,collections,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs,strip_frontmatter

IGNORE=("[原文证据]","[结构化转述]","[本次综合推论]","Evidence","Material")
PLACEHOLDER=re.compile(r"(?:^|\s)(?:待填写|待补充|暂无|TBD|TODO|short-slug|ITEMKEY|pN|\{\{.*?\}\})(?:\s|$)",re.I)
GENERIC=re.compile(r"(?:效果较好|具有理论、方法和实践意义|采用(?:了)?某|值得进一步研究|提升了性能|取得了良好结果)")

def norm(line):
    s=re.sub(r"\s+"," ",line.strip())
    return s if 60<=len(s)<=320 and not s.startswith(("#","|","- [","```")) and not any(x in s for x in IGNORE) else None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); docs=[]; rows=[]
    for d in paper_dirs(root,detect_layout(root)):
        p=d/("02-深度说理报告.md" if (d/"02-深度说理报告.md").exists() else "11-深度说理报告.md")
        if p.exists(): docs.append(p)
    counts=collections.defaultdict(set)
    for p in docs:
        text=strip_frontmatter(p.read_text(encoding="utf-8-sig",errors="replace"))
        placeholders=[line.strip() for line in text.splitlines() if PLACEHOLDER.search(line)]
        generic=[line.strip() for line in text.splitlines() if GENERIC.search(line)]
        for line in text.splitlines():
            s=norm(line)
            if s: counts[s].add(p.parent.name)
        rows.append({"paper_id":p.parent.name.split("--",1)[0],"path":p.as_posix(),"placeholder_lines":placeholders,"generic_lines":generic})
    repeated=[{"text":s,"documents":sorted(ds),"document_count":len(ds)} for s,ds in counts.items() if len(ds)>=2]; repeated.sort(key=lambda x:(-x["document_count"],x["text"]))
    problem_reports=[r for r in rows if r["placeholder_lines"] or r["generic_lines"]]
    result={"schema_version":4,"document_count":len(docs),"repeated_boilerplate":repeated,"reports_with_genericity":problem_reports,"passed":bool(docs) and not repeated and not problem_reports}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/模板化风险审计.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"document_count":len(docs),"repeated_count":len(repeated),"generic_reports":len(problem_reports)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
