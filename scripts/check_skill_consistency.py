#!/usr/bin/env python3
"""Self-check the skill's own contracts, templates, scripts, and layout declarations."""
from __future__ import annotations
import argparse, json, py_compile
from pathlib import Path
from layout import V3_DIRS,V3_PAPER_FILES,V3_STARTERS

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(Path(__file__).resolve().parent.parent)); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); errors=[]
 skill=(root/"SKILL.md").read_text(encoding="utf-8",errors="replace")
 for token in ["layout_version: 3","02-深度说理报告.md","03-12字段证据矩阵.md","Material → Evidence → Claim","completed"]:
  if token not in skill: errors.append("SKILL.md missing:"+token)
 for rel in ["README.md","FILE_CLASSIFICATION.md","references/skill-improvement-plan-20260914.md","references/full-paper-reading-contract.md","references/matrix-12-fields-contract.md","templates/paper-report.md","templates/matrix-12-fields.md","templates/figure-evidence-card.md"]:
  if not (root/rel).is_file(): errors.append("missing:"+rel)
 init=(root/"scripts/init_paper_record.py").read_text(encoding="utf-8",errors="replace")
 for d in V3_DIRS:
  if f'"{d}"' not in init and "'"+d+"'" not in init and not any(x.startswith(d+"/") for x in ["09-质量审计/reading-tasks","09-质量审计/audits"]): errors.append("init-missing-dir:"+d)
 for py in (root/"scripts").glob("*.py"):
  try: py_compile.compile(str(py),doraise=True)
  except Exception as exc: errors.append(f"syntax:{py.name}:{exc}")
 result={"passed":not errors,"skill_root":str(root),"errors":errors,"checked_layout_dirs":len(V3_DIRS),"checked_paper_files":len(V3_PAPER_FILES),"checked_starters":len(V3_STARTERS)}
 if args.out:
  out=Path(args.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"passed":result["passed"],"error_count":len(errors)},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
