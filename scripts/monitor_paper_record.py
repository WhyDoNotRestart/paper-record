#!/usr/bin/env python3
"""Observe Paper Record gates; never upgrade a batch to completed."""
from __future__ import annotations
import argparse,json,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--interval",type=int,default=30); ap.add_argument("--max-cycles",type=int,default=0); ap.add_argument("--once",action="store_true"); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); skill=Path(__file__).resolve().parent; out=Path(args.out).resolve() if args.out else root/"09-质量审计/monitor-status.jsonl"; out.parent.mkdir(parents=True,exist_ok=True); cycle=0
 while True:
  cycle+=1; cmd=[sys.executable,"-X","utf8",str(skill/"run_quality_gates.py"),"--root",str(root)]; p=subprocess.run(cmd,cwd=str(root),text=True,encoding="utf-8",errors="replace",capture_output=True); status={"timestamp":datetime.now(timezone.utc).isoformat(),"cycle":cycle,"root":str(root),"passed":p.returncode==0,"stdout":p.stdout.strip(),"stderr":p.stderr.strip()}
  with out.open("a",encoding="utf-8") as f:f.write(json.dumps(status,ensure_ascii=False)+"\n")
  print(json.dumps({"cycle":cycle,"passed":status["passed"]},ensure_ascii=False),flush=True)
  if status["passed"] or args.once or (args.max_cycles and cycle>=args.max_cycles): return 0 if status["passed"] else 1
  time.sleep(max(1,args.interval))
if __name__=="__main__": raise SystemExit(main())
