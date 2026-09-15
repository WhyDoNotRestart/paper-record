#!/usr/bin/env python3
"""Create v3 full-reading tasks immediately after paper PDFs are verified."""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import date
from pathlib import Path
from layout import detect_layout,paper_dirs,paper_id
STAGES=["结构","理论","作者思路","方法","实验","图表与公式","结论与局限","综合整合"]
def sha256(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--version",default="1"); ap.add_argument("--assigned-to",default="待分配"); ap.add_argument("--integrator",default="待分配"); ap.add_argument("--independent-reviewer",default="待分配"); args=ap.parse_args(); root=Path(args.root).resolve(); layout=detect_layout(root)
 if layout!="v3": raise SystemExit("create_reading_tasks.py只为layout v3新批次服务；旧批次不原地迁移")
 td=root/"09-质量审计/reading-tasks"; td.mkdir(parents=True,exist_ok=True); rows=[]
 for d in paper_dirs(root,"v3"):
  pid=paper_id(d); entry=d/"00-论文入口.md"; fm={}
  if entry.exists():
   for line in entry.read_text(encoding="utf-8",errors="replace").splitlines():
    if ":" in line and not line.startswith("#"): k,v=line.split(":",1); fm[k.strip()]=v.strip().strip('"\'')
  pdf=Path(fm.get("source_pdf", "")); pdf=(root/pdf).resolve() if not pdf.is_absolute() else pdf; task=td/f"READ-{pid}-v{args.version}.md"; old_status="queued"
  if task.exists():
   m=re.search(r"^status:\s*(.+)$",task.read_text(encoding="utf-8",errors="replace"),re.M); old_status=m.group(1).strip() if m else old_status
  digest=sha256(pdf) if pdf.is_file() else ""; source=pdf.relative_to(root).as_posix() if pdf.is_file() and pdf.is_relative_to(root) else fm.get("source_pdf","")
  body=f"""---
task_id: READ-{pid}-v{args.version}
paper_id: {pid}
source_pdf: {source}
pdf_sha256: \"{digest}\"
version: {fm.get('version','unknown')}
assigned_to: \"{args.assigned_to}\"
integrator: \"{args.integrator}\"
status: {old_status}
blocking_reason: null
review_status: pending
created_at: {date.today().isoformat()}
---

# 全文通读任务：{pid}

## 阶段记录

| 阶段 | 状态 | 产物 | 复核说明 |
|---|---|---|---|
"""
  for s in STAGES:
   output=f"../../03-逐篇精读/{d.name}/01-全文通读轨迹.md" if s=="结构" else f"../../03-逐篇精读/{d.name}/02-深度说理报告.md"
   body+=f"| {s} | queued | {output} | |\n"
  body+="""
## 全文覆盖日志

| 页码/章节范围 | 已读内容 | Evidence ID | 状态 | 未解决问题 |
|---|---|---|---|---|
| | | | queued | |

## 版本与材料核验

- PDF页数：
- PDF hash：
- SI/附录：
- 图表/公式：
- 数据/代码：
- 关键参考文献：
"""
  task.write_text(body,encoding="utf-8"); rows.append({"task_id":f"READ-{pid}-v{args.version}","paper_id":pid,"source_pdf":source,"pdf_sha256":digest,"assigned_to":args.assigned_to,"integrator":args.integrator,"independent_reviewer":args.independent_reviewer,"status":old_status})
 queue=root/"09-质量审计/全文通读任务队列.csv"; lines=["task_id,paper_id,source_pdf,pdf_sha256,assigned_to,integrator,independent_reviewer,status"]+[",".join(str(r[k]).replace(","," ") for k in ["task_id","paper_id","source_pdf","pdf_sha256","assigned_to","integrator","independent_reviewer","status"]) for r in rows]; queue.write_text("\ufeff"+"\n".join(lines)+"\n",encoding="utf-8-sig"); print(json.dumps({"layout":layout,"paper_count":len(rows),"queue":str(queue)},ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())
