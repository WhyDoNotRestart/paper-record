#!/usr/bin/env python3
"""Create a new Paper Record 3.0 batch without touching existing batches."""
from __future__ import annotations
import argparse, json
from datetime import date
from pathlib import Path

DIRS = [
    "00-开始", "01-批次控制", "02-论文台账", "03-逐篇精读", "04-证据仓",
    "05-主题研究图谱", "06-跨论文比较", "07-研究机会", "08-复现与科研资产",
    "09-质量审计/reading-tasks", "09-质量审计/audits", "04-证据仓/_索引",
    "99-原始归档",
]
STARTERS = {
    "00-开始/00-阅读导航.md": "# 论文阅读导航\n\n> 只链接真实文件，不链接目录。\n\n## 逐篇精读\n\n## 主题研究图谱\n\n## 研究机会\n",
    "00-开始/01-材料入口.md": "# 材料入口\n\n## 原始论文与全文\n\n## 图表、公式、数据与代码\n\n## 参考文献\n",
    "01-批次控制/批次范围与纳入标准.md": "# 批次范围与纳入标准\n\n- 主题：\n- 时间窗口（绝对日期）：\n- 纳入标准：\n- 排除标准：\n- 直接性分类：\n- 旧批次（只读）：\n",
    "01-批次控制/版本与变更记录.md": "# 版本与变更记录\n\n| 日期 | 版本 | 变更 | 原因 | 验证 |\n|---|---|---|---|---|\n",
    "02-论文台账/论文主索引.md": "# 论文主索引\n\n| Paper ID | 题名 | 年份/版本 | 直接性 | 全文状态 | 阅读状态 | 证据状态 |\n|---|---|---|---|---|---|---|\n",
    "05-主题研究图谱/研究主题总览.md": "# 研究主题总览\n\n> 由逐篇深读证据生成，不写成入门教程。\n",
    "06-跨论文比较/跨论文比较报告.md": "# 跨论文比较报告\n\n> 只比较可比的对象、条件、威胁模型和指标。\n",
    "07-研究机会/研究机会总览.md": "# 研究机会总览\n\n> 每个机会必须包含来源证据、可检验问题和实验设计。\n",
    "08-复现与科研资产/资产总览.md": "# 复现与科研资产总览\n\n> 只登记可以实际复用的变量、数据、基线、脚本和环境。\n",
    "09-质量审计/文件分类清单.md": "# 文件分类清单\n\n| 相对路径 | 业务分类 | 用途 | 状态 | 批次ID |\n|---|---|---|---|---|\n",
    "09-质量审计/材料使用审计.csv": "material_id,material_path,kind,source_version,sha256,usage_status,actual_consumer,evidence_ids,claim_ids,matrix_field_ids,notes\n",
}

def register(root: Path, path: Path, category: str, purpose: str, batch_id: str) -> None:
    ledger = root / "09-质量审计/文件分类清单.md"
    if not ledger.exists() or path == ledger:
        return
    rel = path.relative_to(root).as_posix()
    text = ledger.read_text(encoding="utf-8")
    if f"`{rel}`" not in text:
        with ledger.open("a", encoding="utf-8") as fh:
            fh.write(f"| `{rel}` | {category} | {purpose} | 已生成 | {batch_id} |\n")

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--batch-id", default="PR-UNKNOWN")
    args = ap.parse_args(); root = Path(args.root).expanduser().resolve(); root.mkdir(parents=True, exist_ok=True)
    for directory in DIRS: (root / directory).mkdir(parents=True, exist_ok=True)
    for rel, body in STARTERS.items():
        path = root / rel
        if not path.exists():
            path.write_text(body, encoding="utf-8")
    # The classification ledger is created among the starters; register every
    # earlier starter only after the ledger exists, so no generated file is lost.
    ledger = root / "09-质量审计/文件分类清单.md"
    ledger_text = ledger.read_text(encoding="utf-8") if ledger.exists() else ""
    with ledger.open("a", encoding="utf-8") as fh:
        for rel in STARTERS:
            if rel == "09-质量审计/文件分类清单.md":
                continue
            if f"`{rel}`" not in ledger_text:
                fh.write(f"| `{rel}` | 批次入口与审计 | Paper Record 3.0 starter | 已生成 | {args.batch_id} |\n")
                ledger_text += f"`{rel}`"
    state = {"layout_version": 3, "skill": "papaer-record", "batch_id": args.batch_id, "status": "not-started", "stage": 0, "created_at": date.today().isoformat(), "updated_at": date.today().isoformat()}
    state_path = root / "09-质量审计/批次状态.json"; state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); register(root, state_path, "批次控制", "阶段状态", args.batch_id)
    layout = root / "layout-version.json"; layout.write_text(json.dumps({"layout_version": 3, "skill_revision": "3.0"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); register(root, layout, "批次控制", "布局版本声明", args.batch_id)
    print(root); return 0
if __name__ == "__main__": raise SystemExit(main())
