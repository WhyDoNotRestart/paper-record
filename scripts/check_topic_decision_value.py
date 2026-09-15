#!/usr/bin/env python3
"""Check that topic packages are research-decision artifacts, not tutorials."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from layout import detect_layout,paper_dirs

ID_RE=re.compile(r"\b(?:E|MAT|CLM|R|Evidence|Material|Claim)[-_][A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*\b",re.I)
REQUIRED={
    "00-主题入口.md":("主题边界","总研究问题","研究决策"),
    "01-问题树.md":("总研究问题","未解决","Evidence"),
    "02-理论与方法谱系.md":("机制","关键假设","失败模式"),
    "03-论文关系与可比性.md":("可比","不可比","关系类型"),
    "04-证据差异与结果对照.md":("证据","指标","可信范围"),
    "05-失败模式与边界.md":("失败模式","外推边界","不能推出"),
    "06-可检验研究机会.md":("可检验研究问题","自变量","因变量","基线","成功判据"),
}
ALTERNATIVES={
    "00-主题入口.md":["00-主题入口.md","00-topic-entry.md"],
    "01-问题树.md":["01-问题树.md","01-problem-tree.md"],
    "02-理论与方法谱系.md":["02-理论与方法谱系.md","02-theory-method-lineage.md"],
    "03-论文关系与可比性.md":["03-论文关系与可比性.md","03-paper-relations-comparability.md"],
    "04-证据差异与结果对照.md":["04-证据差异与结果对照.md","04-evidence-differences.md"],
    "05-失败模式与边界.md":["05-失败模式与边界.md","05-failure-boundaries.md"],
    "06-可检验研究机会.md":["06-可检验研究机会.md","06-testable-opportunities.md"],
}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out"); args=ap.parse_args(); root=Path(args.root).resolve(); topic_root=root/"05-主题研究图谱"; topics=sorted(p for p in topic_root.iterdir() if p.is_dir()) if topic_root.exists() else []; rows=[]
    if not topics:
        result={"schema_version":4,"topic_count":0,"status":"not-applicable","passed":len(paper_dirs(root,detect_layout(root)))<2,"rows":[]}
    else:
        for topic in topics:
            issues=[]; all_text=[]
            for canonical, names in ALTERNATIVES.items():
                p=next((topic/n for n in names if (topic/n).is_file()),None)
                if not p: issues.append("missing:"+canonical); continue
                text=p.read_text(encoding="utf-8-sig",errors="replace"); all_text.append(text)
                if len(re.sub(r"\s+","",text))<120: issues.append("too-short:"+canonical)
                for term in REQUIRED[canonical]:
                    if term not in text: issues.append(f"missing-term:{canonical}:{term}")
            combined="\n".join(all_text); ids=set(ID_RE.findall(combined))
            if len(ids)<3: issues.append(f"evidence-or-claim-ids<3:{len(ids)}")
            if re.search(r"(?m)^#{1,6}.*(?:入门|进阶|高级)|^\s*[-*]\s*(?:入门|进阶|高级)",combined): issues.append("tutorial-structure-detected")
            rows.append({"topic_id":topic.name.split("--",1)[0],"path":topic.as_posix(),"id_count":len(ids),"issues":issues,"passed":not issues})
        result={"schema_version":4,"topic_count":len(rows),"status":"checked","passed":all(x["passed"] for x in rows),"rows":rows}
    out=Path(args.out).resolve() if args.out else root/"09-质量审计/主题研究决策验收.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"passed":result["passed"],"topic_count":result["topic_count"],"status":result["status"],"failed":sum(not x["passed"] for x in result["rows"])},ensure_ascii=False)); return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
