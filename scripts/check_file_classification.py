#!/usr/bin/env python3
"""Check that every tracked Paper Record Skill file is classified."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); ledger=root/"FILE_CLASSIFICATION.md"; errors=[]
    text=ledger.read_text(encoding="utf-8-sig",errors="replace") if ledger.exists() else ""
    try:
        tracked=subprocess.check_output(["git","-c","core.quotePath=false","-C",str(root),"ls-files"],text=True,encoding="utf-8",errors="replace").splitlines()
    except Exception:
        tracked=[p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts]
    for rel in tracked:
        if rel in {"FILE_CLASSIFICATION.md"} or rel.startswith(".git/") or "/__pycache__/" in f"/{rel}/": continue
        if f"`{rel}`" not in text: errors.append("unclassified:"+rel)
    result={"schema_version":4,"root":str(root),"classification_file":str(ledger),"tracked_count":len(tracked),"errors":errors,"passed":ledger.exists() and not errors}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/文件分类验收.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"tracked_count":len(tracked),"unclassified":len(errors)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
