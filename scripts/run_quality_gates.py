#!/usr/bin/env python3
"""Run the Paper Record 3.1 gates as one auditable command."""
from __future__ import annotations
import argparse,json,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path

def run_check(name:str, script_root:Path, root:Path, extra:list[str]|None=None)->dict:
    cmd=[sys.executable,"-X","utf8",str(script_root/name),"--root",str(root)] + (extra or [])
    p=subprocess.run(cmd,cwd=str(root),text=True,encoding="utf-8",errors="replace",capture_output=True)
    return {"script":name,"returncode":p.returncode,"passed":p.returncode==0,"stdout":p.stdout.strip(),"stderr":p.stderr.strip()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True)
    ap.add_argument("--skill-root")
    ap.add_argument("--out")
    args=ap.parse_args()
    root = Path(args.root).resolve()
    skill = (
        Path(args.skill_root).resolve()
        if args.skill_root
        else Path(__file__).resolve().parents[1]
    )
    script_dir = skill / "scripts"
    results=[]
    scripts=["validate_paper_record.py","check_reading_task_completion.py","check_semantic_evidence.py","check_matrix_field_richness.py","check_material_traceability.py","check_topic_decision_value.py","check_filename_policy.py","check_links.py","check_independent_review.py"]
    for name in scripts: results.append(run_check(name,script_dir,root))
    navigation=root/"00-开始/00-阅读导航.md"
    if navigation.is_file():
        for renderer in ("markdown","obsidian","html"):
            with tempfile.NamedTemporaryFile(prefix="paper-record-preview-",suffix=".html",delete=False) as preview, tempfile.NamedTemporaryFile(prefix="paper-record-render-",suffix=".json",delete=False) as report:
                preview_path,report_path=preview.name,report.name
            results.append(run_check("render_markdown_preview.py",script_dir,root,["--source","00-开始/00-阅读导航.md","--renderer",renderer,"--out",preview_path,"--report",report_path]))
    with tempfile.NamedTemporaryFile(prefix="paper-record-classification-",suffix=".json",delete=False) as report:
        classification_out=report.name
    results.append(run_check("check_file_classification.py",script_dir,skill,["--out",classification_out]))
    result={"schema_version":4,"timestamp":datetime.now(timezone.utc).isoformat(),"root":str(root),"skill_root":str(skill),"passed":all(x["passed"] for x in results),"checks":results}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/总门禁结果.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"failed":[x["script"] for x in results if not x["passed"]]},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
