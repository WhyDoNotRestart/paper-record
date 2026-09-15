#!/usr/bin/env python3
"""Initialize a non-destructive Paper Record workspace/Vault structure.

Creates only missing folders and starter templates. It never overwrites existing
files. Every created file is immediately registered in 文件分类清单.md and
manifest.json with one business classification.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Dict, List

DEFAULT_CATEGORIES = [
    "后量子密码学",
    "零知识证明与递归证明",
    "隐私增强计算",
    "实现安全与侧信道",
    "区块链与分布式密码学",
]

DIRS = [
    "00-系统说明/批次日志",
    "01-精华论文",
    "02-研究主题",
    "99-佐证资料/完整论文笔记",
    "99-佐证资料/图表与证据卡",
    "03-研究空白与可复用资产/概念与术语",
    "03-研究空白与可复用资产/研究空白",
    "03-研究空白与可复用资产/可复用科研资产",
    "99-佐证资料/参考文献",
    "09-模板",
    "99-佐证资料/原始论文",
    "99-待人工复核",
]

TEMPLATES: Dict[str, str] = {
    "09-模板/论文笔记模板.md": """---\nrecord_type: paper\ntitle: \"原文题名\"\nzotero_item_id: \"未提及\"\ncategory: \"未分类\"\nreading_status: \"已收录\"\nfulltext_status: \"未获取\"\nevidence_status: \"未核验\"\nrecord_batch: \"{batch_id}\"\nlast_reviewed: \"{today}\"\n---\n\n# 原文题名\n\n## 三分钟速读\n\n- 研究问题：\n- 核心方法：\n- 最重要结果：\n- 最大局限：\n- 与当前研究的关系：\n\n## 论文导航\n\n- [[#研究问题]]\n- [[#论文论证链]]\n- [[#方法与技术路线]]\n- [[#实验设计与数据]]\n- [[#关键图表]]\n- [[#主要发现与结论]]\n- [[#局限与适用边界]]\n- [[#与其他论文关系]]\n- [[#参考文献溯源]]\n\n## 研究问题\n\n- 原文表述：\n- 原文位置：\n- 结构化理解：\n\n## 论文论证链\n\n| 环节 | 内容 | 原文位置 | 证据编号 |\n|---|---|---|---|\n| 研究缺口 |  |  |  |\n| 研究问题 |  |  |  |\n| 方法 |  |  |  |\n| 数据/实验 |  |  |  |\n| 图表证据 |  |  |  |\n| 结果 |  |  |  |\n| 结论 |  |  |  |\n| 局限 |  |  |  |\n\n## 方法与技术路线\n\n## 实验设计与数据\n\n## 关键图表\n\n## 主要发现与结论\n\n## 局限与适用边界\n\n## 研究者速查\n\n- 可引用结论：\n- 可复用方法：\n- 可复用指标：\n- 可复用数据/代码：\n- 需要重新核验：\n\n## 与其他论文关系\n\n## 参考文献溯源\n\n## 客观证据与个人推论分离\n\n> [!quote] 原文证据\n> \n\n> [!summary] 结构化转述\n> \n\n> [!insight] 个人推论\n> \n\n> [!question] 待核查问题\n> \n""",
    "09-模板/图表证据卡模板.md": """---\nrecord_type: figure-evidence\npaper_item_id: \"未提及\"\nfigure_id: \"Figure/Table X\"\ntitle: \"原文标题\"\nfigure_type: \"未核验\"\nsource_page: \"未提及\"\nsource_section: \"未提及\"\nimage: \"未获取\"\nverification_status: \"未核验\"\nrecord_batch: \"{batch_id}\"\n---\n\n# Figure/Table X：原文标题\n\n![[图表文件名.png]]\n\n## 图表展示内容\n\n- 横轴/列：\n- 纵轴/行：\n- 变量：\n- 比较对象：\n- 固定条件：\n\n## 关键观察\n\n## 正文对应关系\n\n- 原文位置：\n- 对应段落主张：\n- 支持程度：完全支持 / 部分支持 / 无法判断\n\n## 研究问题与结论对应\n\n- 支撑问题：\n- 支撑子结论：\n- 证据强度：直接证据 / 间接证据 / 作者推导 / 合理外推\n\n## 边界与可复现性\n\n- 样本、硬件、软件、参数：\n- 未测试场景：\n- 不宜外推到：\n\n## 跨论文关系\n\n- 关系：支持 / 补充 / 拓展 / 对比 / 评估 / 应用 / 重复 / 冲突\n- 目标论文：\n""",
    "09-模板/分类小结模板.md": """---\nrecord_type: category-summary\ncategory: \"未分类\"\nrecord_batch: \"{batch_id}\"\nlast_reviewed: \"{today}\"\n---\n\n# 分类小结：未分类\n\n## 收录范围\n\n## 论文列表\n\n## 主题分布\n\n## 方法趋势\n\n## 数据和实验条件对比\n\n## 主要结论与冲突\n\n## 研究空白\n\n## 可复用科研资产\n\n## 阅读建议\n""",
    "00-系统说明/文件分类清单.md": """# 文件分类清单\n\n本清单记录Paper Record生成或修改的每个文件。一个文件只归入一个主业务分类；无法确认的文件进入`99-待人工复核/`。\n\n| 相对路径 | 业务分类 | 文件用途 | 关联论文/分类 | 状态 | 批次ID |\n|---|---|---|---|---|---|\n""",
    "00-系统说明/论文知识库说明.md": """# 论文知识库说明\n\n- Excel：批量索引、分类统计、横向比较。\n- Zotero：条目、集合、标签、PDF和SI。\n- Obsidian：深度笔记、图表证据、研究空白和双向链接。\n- 图表资产：只保留单个图/表本体，不使用整页PDF截图。\n- 阶段门禁：每阶段完成后必须等待用户验收。\n\n## 当前状态\n\n- 初始化时间：{today}\n- 最近批次：{batch_id}\n- 处理状态：未开始\n""",
}


def classify(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if rel.startswith("00-系统说明/"):
        return "系统说明与批次审计"
    if rel.startswith("01-精华论文/"):
        return "论文索引与横向比较"
    if rel.startswith("02-研究主题/"):
        return "领域入门与学习路径"
    if rel.startswith("99-佐证资料/完整论文笔记/"):
        return "单篇论文深度笔记"
    if rel.startswith("99-佐证资料/图表与证据卡/"):
        return "图表证据卡与裁剪图表"
    if rel.startswith("03-研究空白与可复用资产/概念与术语/"):
        return "概念、术语与方法卡"
    if rel.startswith("03-研究空白与可复用资产/研究空白/"):
        return "研究空白与机会"
    if rel.startswith("03-研究空白与可复用资产/可复用科研资产/"):
        return "可复用科研资产"
    if rel.startswith("99-佐证资料/参考文献/"):
        return "参考文献与引用溯源"
    if rel.startswith("09-模板/"):
        return "模板与标准化输入"
    if rel.startswith("99-佐证资料/原始论文/"):
        return "原始附件与只读素材"
    if rel.startswith("99-待人工复核/"):
        return "待人工复核"
    return "待人工复核"


def write_if_missing(root: Path, rel: str, content: str, batch_id: str, today: str) -> bool:
    path = root / rel
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.format(batch_id=batch_id, today=today), encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化Paper Record论文知识库目录与模板")
    parser.add_argument("--root", required=True, help="目标Vault或工作目录")
    parser.add_argument("--batch-id", default=None, help="批次ID，例如PR-20260914-001")
    parser.add_argument("--categories", nargs="*", default=DEFAULT_CATEGORIES, help="需要预建的论文分类")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    categories = [str(c).strip() for c in args.categories if str(c).strip()]
    if any(Path(c).is_absolute() or ".." in Path(c).parts or "/" in c or "\\" in c for c in categories):
        parser.error("categories 只能是单一目录名，不能包含绝对路径、.. 或路径分隔符")
    today = date.today().isoformat()
    batch_id = args.batch_id or f"PR-{today.replace('-', '')}-001"
    created: List[str] = []

    for rel_dir in DIRS:
        (root / rel_dir).mkdir(parents=True, exist_ok=True)

    for category in categories:
        for base in ("99-佐证资料/完整论文笔记", "99-佐证资料/图表与证据卡", "99-佐证资料/原始论文"):
            (root / base / category).mkdir(parents=True, exist_ok=True)

    for rel, content in TEMPLATES.items():
        if write_if_missing(root, rel, content, batch_id, today):
            created.append(rel)

    # Add one category-summary starter per category only if absent.
    for category in categories:
        rel = f"01-精华论文/{category}--论文索引.md"
        content = (
            f"<!-- paper-record:starter -->\n# {category}：论文索引\n\n"
            "| 论文题名 | 年份 | 研究类型 | 研究主题 | 阅读状态 | 深度笔记 | 图表证据 |\n"
            "|---|---:|---|---|---|---|---|\n"
        )
        if write_if_missing(root, rel, content, batch_id, today):
            created.append(rel)
        rel = f"02-研究主题/{category}--入门路径.md"
        content = f"# {category}：入门路径\n\n## 先修知识\n\n## 核心术语\n\n## 推荐阅读顺序\n\n## 代表论文\n\n"
        if write_if_missing(root, rel, content, batch_id, today):
            created.append(rel)

    manifest_json = root / "00-系统说明" / "paper-record-manifest.json"
    manifest_json_rel = "00-系统说明/paper-record-manifest.json"
    manifest_will_be_created = not manifest_json.exists()
    if manifest_will_be_created:
        created.append(manifest_json_rel)

    # Keep an append-only batch history so reruns cannot silently diverge from
    # the Markdown classification ledger. Migrate the original single-batch
    # shape when an older manifest is encountered.
    if manifest_json.exists():
        try:
            existing = json.loads(manifest_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}
    else:
        existing = {}
    if isinstance(existing.get("batches"), list):
        batches = existing["batches"]
    else:
        batches = []
        if existing.get("batch_id"):
            batches.append({
                "batch_id": existing.get("batch_id"),
                "date": existing.get("date"),
                "status": "migrated",
                "files": existing.get("created_files", []),
            })
    batch_record = {
        "batch_id": batch_id,
        "date": today,
        "status": "initialized",
        "files": [
            {"path": rel, "business_category": classify(rel), "event": "created"}
            for rel in created
        ],
        "existing_files_preserved": True,
    }
    batches = [b for b in batches if b.get("batch_id") != batch_id]
    batches.append(batch_record)
    data = {
        "schema_version": 1,
        "skill": "papaer-record",
        "root": str(root),
        "batches": batches,
    }
    manifest_json.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="paper-record-manifest-", suffix=".tmp", dir=str(manifest_json.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp_name, manifest_json)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)

    manifest_path = root / "00-系统说明" / "文件分类清单.md"
    lines = [
        f"| {rel} | {classify(rel)} | 自动初始化文件 | 未绑定 | 已创建 | {batch_id} |"
        for rel in created
    ]
    if lines:
        with manifest_path.open("a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    print(json.dumps({"root": str(root), "batch_id": batch_id, "created": created, "count": len(created)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

