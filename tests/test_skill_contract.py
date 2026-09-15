#!/usr/bin/env python3
"""Isolated smoke tests for Paper Record 3.0 skill contracts."""
from __future__ import annotations
import base64, json, subprocess, sys, tempfile, unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
INIT = SKILL / "scripts/init_paper_record.py"
VALIDATE = SKILL / "scripts/validate_paper_record.py"
TASKS = SKILL / "scripts/create_reading_tasks.py"
RENDER = SKILL / "scripts/render_markdown_preview.py"
SEMANTIC = SKILL / "scripts/check_semantic_evidence.py"

class PaperRecordSkillSmokeTest(unittest.TestCase):
    def run_py(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "-X", "utf8", str(script), *args], text=True, encoding="utf-8", capture_output=True)

    def test_init_creates_v3_and_validator_accepts(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"
            created = self.run_py(INIT, "--root", str(root), "--batch-id", "TEST-001")
            self.assertEqual(created.returncode, 0, created.stderr)
            self.assertEqual(json.loads((root / "layout-version.json").read_text(encoding="utf-8"))["layout_version"], 3)
            checked = self.run_py(VALIDATE, "--root", str(root))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)


    def test_render_resolves_obsidian_stem_and_image_file(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"; root.mkdir(parents=True)
            source = root / "00-开始/source.md"; target = root / "03-逐篇精读/P001--2024--demo/02-深度说理报告.md"; image = root / "04-证据仓/P001--2024--demo/figures/fig.png"
            target.parent.mkdir(parents=True); image.parent.mkdir(parents=True); target.write_text("# report\n", encoding="utf-8")
            image.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="))
            source.parent.mkdir(parents=True); source.write_text("# nav\n[[../03-逐篇精读/P001--2024--demo/02-深度说理报告]]\n![fig](../04-证据仓/P001--2024--demo/figures/fig.png)\n", encoding="utf-8")
            result = self.run_py(RENDER, "--root", str(root), "--source", "00-开始/source.md")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"broken_count": 0', result.stdout)

    def test_render_rejects_invalid_image_content(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"; root.mkdir(parents=True)
            source = root / "entry.md"; image = root / "broken.png"
            image.write_bytes(b"not-a-real-png")
            source.write_text("![broken](broken.png)\n", encoding="utf-8")
            result = self.run_py(RENDER, "--root", str(root), "--source", "entry.md")
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"broken_count": 1', result.stdout)

    def test_semantic_gate_rejects_hollow_report(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"
            paper = root / "03-逐篇精读/P001--2024--hollow"
            paper.mkdir(parents=True)
            (root / "layout-version.json").write_text('{"layout_version":3}\n', encoding="utf-8")
            required = ["00-论文入口.md", "01-全文通读轨迹.md", "03-12字段证据矩阵.md", "04-图表公式证据册.md", "05-实验数据与复现.md", "06-参考文献脉络.md", "07-主张证据与边界.md"]
            for name in required:
                (paper / name).write_text("# placeholder\n", encoding="utf-8")
            (paper / "02-深度说理报告.md").write_text("# P001\n\n## 理论\n采用某算法，效果较好。\n", encoding="utf-8")
            result = self.run_py(SEMANTIC, "--root", str(root))
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"passed": false', result.stdout)

    def test_task_generator_preserves_existing_status(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"
            self.assertEqual(self.run_py(INIT, "--root", str(root)).returncode, 0)
            paper = root / "03-逐篇精读/P001--2024--demo-paper"
            paper.mkdir(parents=True)
            (paper / "00-论文入口.md").write_text("---\npaper_id: P001\nsource_pdf: 04-证据仓/P001--2024--demo-paper/source/p001.pdf\nversion: v1\n---\n", encoding="utf-8")
            pdf = root / "04-证据仓/P001--2024--demo-paper/source/p001.pdf"
            pdf.parent.mkdir(parents=True); pdf.write_bytes(b"test-pdf")
            task_dir = root / "09-质量审计/reading-tasks"; task_dir.mkdir(parents=True, exist_ok=True)
            task = task_dir / "READ-P001-v1.md"; task.write_text("status: done\n", encoding="utf-8")
            result = self.run_py(TASKS, "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("status: done", task.read_text(encoding="utf-8"))
            self.assertIn("P001", (root / "09-质量审计/全文通读任务队列.csv").read_text(encoding="utf-8-sig"))

if __name__ == "__main__":
    unittest.main()
