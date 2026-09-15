#!/usr/bin/env python3
"""Audit Material→Evidence→Claim→Report/Topic traceability and usage status."""
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
from layout import detect_layout,rel

VALID={"core-argument","method","result","limitation","background","reproduction","context-only","unused-with-reason","unavailable","needs-review"}
REQUIRED_USED={"core-argument","method","result","limitation","reproduction","background"}
ID_RE=re.compile(r"\b(?:E|MAT|CLM|R|Evidence|Material|Claim)[-_][A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*\b",re.I)

def split_ids(value:str)->list[str]:
    return [x.strip() for x in re.split(r"[;,]",value or "") if x.strip()]

def split_paths(value:str)->list[str]:
    return [x.strip() for x in re.split(r"[;,]",value or "") if x.strip()]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root)
    ledger=root/("09-质量审计/材料使用审计.csv" if layout=="v3" else "01-批次与审计/材料使用审计.csv")
    result={"schema_version":4,"passed":False,"ledger":str(ledger),"material_count":0,"missing":[],"invalid":[],"orphan_ids":[],"context_or_unusable":[]}
    if not ledger.exists():
        result["ledger_missing"]=True
    else:
        with ledger.open("r",encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
        result["material_count"]=len(rows); seen=set(); material_ids=set(); corpus=[]
        for p in root.rglob("*"):
            if not p.is_file() or p == ledger or "99-原始归档" in p.parts: continue
            if p.suffix.lower() in {".md",".html",".csv"}:
                corpus.append(p.read_text(encoding="utf-8-sig",errors="replace"))
        corpus_text="\n".join(corpus)
        for r in rows:
            mid=(r.get("material_id") or "").strip(); path=(r.get("material_path") or "").strip(); status=(r.get("usage_status") or "").strip(); consumer=(r.get("actual_consumer") or "").strip(); ev=split_ids(r.get("evidence_ids","")); claims=split_ids(r.get("claim_ids","")); fields=split_ids(r.get("matrix_field_ids","")); reason=(r.get("notes") or "").strip(); ref_role=(r.get("reference_role") or "").strip(); occ=(r.get("occurrence_locators") or "").strip()
            problems=[]
            if not mid: problems.append("missing-material-id")
            elif mid in seen: problems.append("duplicate-material-id")
            seen.add(mid); material_ids.add(mid)
            if status not in VALID: problems.append("invalid-usage-status")
            p=(root/path).resolve() if path else None
            if status not in {"unavailable"} and (not p or not p.is_file()): result["missing"].append({"material_id":mid,"path":path,"status":status})
            if status=="unavailable" and not reason: problems.append("unavailable-needs-reason")
            if status=="unused-with-reason" and not reason: problems.append("unused-needs-reason")
            if status=="context-only": result["context_or_unusable"].append(mid)
            if status in REQUIRED_USED:
                consumers=split_paths(consumer)
                if not consumers: problems.append("used-material-missing-consumer")
                for c in consumers:
                    cp=(root/c).resolve()
                    if not cp.is_file(): problems.append("consumer-missing:"+c)
                if not (ev or claims or fields): problems.append("used-material-missing-provenance")
            if (r.get("kind") or "").strip()=="reference" and status not in {"unavailable"} and not (ref_role and occ): problems.append("reference-missing-role-or-occurrence")
            if status in {"core-argument","method","result","limitation"} and not (r.get("report_sections") or "").strip(): problems.append("core-material-missing-report-section")
            if status in {"result","method"} and (r.get("render_status") or "").strip() not in {"passed","not-applicable","not-run"}: problems.append("invalid-render-status")
            for eid in ev:
                if eid not in corpus_text: result["orphan_ids"].append({"material_id":mid,"id":eid,"kind":"evidence"})
            for cid in claims:
                if cid not in corpus_text: result["orphan_ids"].append({"material_id":mid,"id":cid,"kind":"claim"})
            if problems: result["invalid"].append({"material_id":mid,"problems":problems})
        # Every non-ledger Material ID in the batch must be represented in the ledger.
        for mid in sorted(set(x for x in ID_RE.findall(corpus_text) if x.upper().startswith("MAT-"))):
            if mid not in material_ids: result["orphan_ids"].append({"material_id":mid,"kind":"ledger"})
        result["passed"]=not result["missing"] and not result["invalid"] and not result["orphan_ids"]
    out=Path(args.out).resolve() if args.out else root/("09-质量审计/材料使用验收.json" if layout=="v3" else "01-批次与审计/材料使用验收.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"material_count":result.get("material_count",0),"missing":len(result.get("missing",[])),"invalid":len(result.get("invalid",[])),"orphan_ids":len(result.get("orphan_ids",[]))},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
