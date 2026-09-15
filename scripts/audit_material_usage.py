#!/usr/bin/env python3
"""Audit the material ledger for paths, controlled statuses, consumers and provenance."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from layout import detect_layout
VALID={"core-argument","method","result","limitation","background","reproduction","context-only","unused-with-reason","unavailable","needs-review"}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root); ledger=root/("09-质量审计/材料使用审计.csv" if layout=="v3" else "01-批次与审计/材料使用审计.csv"); missing=[]; invalid=[]; unused=[]
 if not ledger.exists(): result={"passed":False,"ledger_missing":True,"material_count":0,"missing":[],"invalid":[]}
 else:
  with ledger.open("r",encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
  for r in rows:
   rel=r.get("material_path","").strip(); p=root/rel if rel else None; status=r.get("usage_status","").strip(); consumer=r.get("actual_consumer","").strip(); ev=r.get("evidence_ids","").strip(); claims=r.get("claim_ids","").strip(); fields=r.get("matrix_field_ids","").strip()
   if not p or not p.is_file(): missing.append({"material_id":r.get("material_id"),"path":rel})
   if status not in VALID: invalid.append({"material_id":r.get("material_id"),"reason":"invalid usage_status"})
   if status in {"unused-with-reason","unavailable","needs-review","context-only"}: unused.append(r.get("material_id"))
   elif not consumer or not (ev or claims or fields): invalid.append({"material_id":r.get("material_id"),"reason":"used material lacks consumer and provenance"})
  result={"passed":not missing and not invalid,"ledger":str(ledger),"material_count":len(rows),"missing":missing,"invalid":invalid,"context_or_unusable":unused}
 out=Path(args.out).resolve() if args.out else root/("09-质量审计/材料使用验收.json" if layout=="v3" else "01-批次与审计/材料使用验收.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"material_count":result.get("material_count",0),"missing":len(result.get("missing",[])),"invalid":len(result.get("invalid",[]))},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
