#!/usr/bin/env python3
"""Verify that every paper has a source-grounded independent review sign-off."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from layout import detect_layout, frontmatter, paper_dirs, paper_id, rel

PASSED = {"passed", "approved", "通过", "已通过", "已签收"}
TRUE_VALUES = {"true", "yes", "1", "是", "已打开", "已核对"}
EVIDENCE_RE = re.compile(r"\b(?:E|Evidence)(?:[-_][A-Za-z0-9]+)+\b", re.I)
REQUIRED_REVIEW_TERMS = ("关键结果", "理论", "图表", "综合推论", "复现")


def latest_task(root: Path, pid: str) -> Path | None:
    tasks = sorted((root / "09-质量审计/reading-tasks").glob(f"READ-{pid}-v*.md"))
    return tasks[-1] if tasks else None


def latest_review(root: Path, pid: str) -> Path | None:
    reviews = sorted((root / "09-质量审计/independent-reviews").glob(f"REVIEW-{pid}-v*.md"))
    return reviews[-1] if reviews else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    layout = detect_layout(root)
    rows = []
    corpus = "\n".join(
        p.read_text(encoding="utf-8-sig", errors="replace")
        for p in root.rglob("*.md")
        if "99-原始归档" not in p.parts
    )

    for paper in paper_dirs(root, layout):
        pid = paper_id(paper)
        review = latest_review(root, pid)
        task = latest_task(root, pid)
        issues: list[str] = []
        sampled: list[str] = []
        reviewer = ""
        integrator = ""
        if task:
            task_text = task.read_text(encoding="utf-8-sig", errors="replace")
            integrator = str(frontmatter(task_text).get("integrator", "")).strip().strip('"\'')
        if not review:
            issues.append("missing-independent-review")
        else:
            text = review.read_text(encoding="utf-8-sig", errors="replace")
            fm = frontmatter(text)
            reviewer = str(fm.get("reviewer", "")).strip().strip('"\'')
            status = str(fm.get("review_status", "")).strip().lower()
            reopened = str(fm.get("source_pdf_reopened", "")).strip().lower()
            boundary = str(fm.get("conclusion_boundary_ok", "")).strip().lower()
            reviewed_at = str(fm.get("reviewed_at", "")).strip().strip('"\'')
            sampled = sorted(set(EVIDENCE_RE.findall(text)))
            if not reviewer or reviewer.lower() in {"pending", "待分配"}:
                issues.append("missing-reviewer")
            if reviewer and integrator and reviewer == integrator:
                issues.append("reviewer-equals-integrator")
            if reopened not in TRUE_VALUES:
                issues.append("source-pdf-not-reopened")
            if status not in PASSED:
                issues.append("review-status-not-passed")
            if boundary not in TRUE_VALUES:
                issues.append("conclusion-boundary-not-approved")
            if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", reviewed_at):
                issues.append("invalid-reviewed-at")
            if len(sampled) < 3:
                issues.append(f"sampled-evidence-ids<3:{len(sampled)}")
            for eid in sampled:
                if eid not in corpus:
                    issues.append("unresolved-sampled-evidence:" + eid)
            for term in REQUIRED_REVIEW_TERMS:
                if term not in text:
                    issues.append("missing-review-term:" + term)
        rows.append({
            "paper_id": pid,
            "review_path": rel(review, root) if review else None,
            "reviewer": reviewer or None,
            "integrator": integrator or None,
            "sampled_evidence_ids": sampled,
            "issues": issues,
            "passed": not issues,
        })

    result = {
        "schema_version": 4,
        "layout": layout,
        "paper_count": len(rows),
        "passed": bool(rows) and all(row["passed"] for row in rows),
        "rows": rows,
    }
    out = Path(args.out).resolve() if args.out else root / "09-质量审计/独立复核验收.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": result["passed"],
        "paper_count": len(rows),
        "failed": sum(not row["passed"] for row in rows),
    }, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
