#!/usr/bin/env python3
"""Run the Paper Record 3.0 technical gates as one auditable command."""
from __future__ import annotations
import argparse,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--skill-root"); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); skill=Path(args.skill_root).resolve() if args.skill_root else Path(__file__).resolve().parent
 scripts=["validate_paper_record.py","check_reading_task_completion.py","check_semantic_evidence.py","check_matrix_field_richness.py","audit_material_usage.py","check_filename_policy.py","check_links.py"]
 results=[]
 for name in scripts:
  cmd=[sys.executable,"-X","utf8",str(skill/name),"--root",str(root)]
  p=subprocess.run(cmd,cwd=str(root),text=True,encoding="utf-8",errors="replace",capture_output=True)
  results.append({"script":name,"returncode":p.returncode,"passed":p.returncode==0,"stdout":p.stdout.strip(),"stderr":p.stderr.strip()})
 result={"timestamp":datetime.now(timezone.utc).isoformat(),"root":str(root),"skill_root":str(skill),"passed":all(x["passed"] for x in results),"checks":results}
 out=Path(args.out).resolve() if args.out else root/"09-质量审计/总门禁结果.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"failed":[x["script"] for x in results if not x["passed"]]},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
