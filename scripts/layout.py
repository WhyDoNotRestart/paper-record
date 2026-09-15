#!/usr/bin/env python3
"""Shared layout, metadata, and local-link helpers for Paper Record validators."""
from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import unquote
V3_DIRS=["00-开始","01-批次控制","02-论文台账","03-逐篇精读","04-证据仓","05-主题研究图谱","06-跨论文比较","07-研究机会","08-复现与科研资产","09-质量审计","99-原始归档"]
V3_PAPER_FILES=["00-论文入口.md","01-全文通读轨迹.md","02-深度说理报告.md","03-12字段证据矩阵.md","04-图表公式证据册.md","05-实验数据与复现.md","06-参考文献脉络.md","07-主张证据与边界.md"]
V3_STARTERS=["00-开始/00-阅读导航.md","00-开始/01-材料入口.md","01-批次控制/批次范围与纳入标准.md","01-批次控制/版本与变更记录.md","02-论文台账/论文主索引.md","05-主题研究图谱/研究主题总览.md","06-跨论文比较/跨论文比较报告.md","07-研究机会/研究机会总览.md","08-复现与科研资产/资产总览.md","09-质量审计/文件分类清单.md","09-质量审计/材料使用审计.csv","09-质量审计/批次状态.json"]
def detect_layout(root:Path)->str:
 if (root/"layout-version.json").exists() or (root/"03-逐篇精读").exists(): return "v3"
 if (root/"04-论文深度阅读").exists() or (root/"00-入口").exists(): return "v2"
 if (root/"04-论文笔记").exists() or (root/"00-系统说明").exists(): return "legacy"
 return "unknown"
def paper_dirs(root:Path,layout:str|None=None)->list[Path]:
 layout=layout or detect_layout(root); dirname={"v3":"03-逐篇精读","v2":"04-论文深度阅读","legacy":"04-论文笔记"}.get(layout)
 return sorted(p for p in (root/dirname).iterdir() if p.is_dir()) if dirname and (root/dirname).exists() else []
def paper_id(path:Path)->str: return path.name.split("--",1)[0]
def rel(path:Path,root:Path)->str: return path.relative_to(root).as_posix()
def frontmatter(text:str)->dict[str,str]:
 if not text.startswith("---"): return {}
 end=text.find("\n---",3)
 if end<0:return {}
 result={}
 for line in text[4:end].splitlines():
  if ":" not in line or line.lstrip().startswith("#"): continue
  key,value=line.split(":",1); result[key.strip()]=value.strip().strip('"\'')
 return result
def strip_frontmatter(text:str)->str:
 if text.startswith("---"):
  end=text.find("\n---",3)
  if end>=0:return text[end+4:]
 return text
def is_placeholder(text:str)->bool: return bool(re.search(r"<(?:paper|title|fill|待填写)|short-slug|ITEMKEY|pN|\{\{.*?\}\}",text,re.I))
def resolve_local_link(src:Path,target:str,root:Path)->Path|None:
 target=unquote(target.strip().strip("<>").split("#",1)[0].split("?",1)[0])
 if not target or target.startswith(("http://","https://","mailto:","data:","zotero:")): return None
 if target.startswith("file:///"): target=target[8:]
 base=Path(target) if target.startswith("/") or (len(target)>2 and target[1]==":") else (src.parent/target)
 candidates=[base]
 if base.suffix=="": candidates += [base.with_suffix(".md"),base/"index.md"]
 return next((p.resolve() for p in candidates if p.is_file() or p.is_dir()),base.resolve())
