#!/usr/bin/env python3
"""Validate Paper Record structure, layout consistency, links, and completion honesty."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from layout import V3_DIRS, V3_PAPER_FILES, V3_STARTERS, detect_layout, paper_dirs, paper_id, rel, frontmatter, resolve_local_link, target_type, validate_media

LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)|!?\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^]]+)?\]\]')
GENERATED_AUDIT_FILES = {
    "结构验收.json", "通读任务验收.json", "语义证据验收.json",
    "矩阵字段验收.json", "材料使用验收.json", "主题研究决策验收.json",
    "链接审计.json", "总门禁结果.json",
}

def check_links(root: Path) -> list[dict]:
    bad=[]
    for src in root.rglob("*"):
        if not src.is_file() or src.suffix.lower() not in {".md", ".html"} or "99-原始归档" in src.parts: continue
        text=src.read_text(encoding="utf-8-sig",errors="replace")
        for match in LINK_RE.finditer(text):
            target=(match.group(1) or match.group(2) or "").strip().strip("<>").split("#",1)[0]
            if not target or target.startswith(("http://","https://","mailto:","data:","zotero:")): continue
            p=resolve_local_link(src,target,root); kind=target_type(p,"image" if match.group(0).startswith("!") else "link")
            media=validate_media(p) if kind in {"image","pdf"} else {"format_valid":bool(p and p.is_file() and not p.is_dir())}
            if not p or not p.is_file() or p.is_dir() or not media.get("format_valid"):
                bad.append({"source":rel(src,root),"target":target,"resolved":rel(p,root) if p and p.is_relative_to(root) else str(p) if p else "","target_type":kind,"format_valid":bool(media.get("format_valid")),"media":media})
    return bad

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--layout",choices=["auto","v3","v2","legacy"],default="auto"); ap.add_argument("--out"); args=ap.parse_args()
    root=Path(args.root).expanduser().resolve(); layout=detect_layout(root) if args.layout=="auto" else args.layout; errors=[]; warnings=[]; info={"layout":layout}
    if layout=="v3":
        for d in V3_DIRS:
            if not (root/d).is_dir(): errors.append(f"missing-dir:{d}")
        for f in V3_STARTERS:
            if not (root/f).is_file(): errors.append(f"missing-starter:{f}")
        papers=paper_dirs(root,"v3"); info["paper_count"]=len(papers)
        for d in papers:
            if not re.fullmatch(r"P\d{3,}--\d{4}--[a-z0-9-]+",d.name): errors.append(f"bad-paper-dir:{rel(d,root)}")
            for f in V3_PAPER_FILES:
                if not (d/f).is_file(): errors.append(f"{paper_id(d)}:missing:{f}")
            entry=d/"00-论文入口.md"
            if entry.exists() and frontmatter(entry.read_text(encoding="utf-8",errors="replace")).get("paper_id") not in {None,paper_id(d)}:
                errors.append(f"{paper_id(d)}:paper-id-mismatch")
        ledger=root/"09-质量审计/文件分类清单.md"
        if ledger.exists():
            lt=ledger.read_text(encoding="utf-8",errors="replace")
            for p in root.rglob("*"):
                if (
                    p.is_file()
                    and p.name not in {"文件分类清单.md", *GENERATED_AUDIT_FILES}
                    and not (p.parent == root / "09-质量审计" and p.suffix.lower() == ".json")
                    and "99-原始归档" not in p.parts
                    and "__pycache__" not in p.parts
                ):
                    if f"`{rel(p,root)}`" not in lt: errors.append(f"unclassified:{rel(p,root)}")
        state=root/"09-质量审计/批次状态.json"
        if state.exists():
            try:
                data=json.loads(state.read_text(encoding="utf-8"))
                if data.get("status")=="completed" and (errors or not papers): errors.append("completed-with-structural-errors")
            except Exception as exc: errors.append(f"invalid-state:{exc}")
        bad_links=check_links(root); info["broken_links"]=len(bad_links); errors.extend([f"broken-link:{x['source']}->{x['target']}" for x in bad_links[:50]])
    else:
        warnings.append(f"legacy-layout:{layout}; v3 validation is recommended for new batches")
        info["paper_count"]=len(paper_dirs(root,layout))
    result={"passed":not errors,"layout":layout,"errors":errors,"warnings":warnings,"info":info}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/结构验收.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"passed":result["passed"],"layout":layout,"error_count":len(errors),"warning_count":len(warnings)},ensure_ascii=False)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
