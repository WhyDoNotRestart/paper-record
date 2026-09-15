#!/usr/bin/env python3
"""Isolated smoke tests for Paper Record 3.0 skill contracts."""
from __future__ import annotations
import base64, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
INIT = SKILL / "scripts/init_paper_record.py"
VALIDATE = SKILL / "scripts/validate_paper_record.py"
TASKS = SKILL / "scripts/create_reading_tasks.py"
RENDER = SKILL / "scripts/render_markdown_preview.py"
SEMANTIC = SKILL / "scripts/check_semantic_evidence.py"
MATERIAL_AUDIT = SKILL / "scripts/audit_material_usage.py"
TOPIC_CHECK = SKILL / "scripts/check_topic_decision_value.py"
QUALITY_GATES = SKILL / "scripts/run_quality_gates.py"

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

    def test_material_audit_accepts_used_and_controlled_unavailable_materials(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"
            report = root / "03-逐篇精读/P001--2024--material/02-深度说理报告.md"
            report.parent.mkdir(parents=True)
            report.write_text("E-P001-001 CLM-P001-001 MAT-P001-PDF\n", encoding="utf-8")
            source = root / "04-证据仓/P001--2024--material/source.txt"
            source.parent.mkdir(parents=True); source.write_text("fixture\n", encoding="utf-8")
            ledger = root / "09-质量审计/材料使用审计.csv"
            ledger.parent.mkdir(parents=True)
            ledger.write_text("material_id,material_path,kind,source_version,sha256,usage_status,actual_consumer,evidence_ids,claim_ids,matrix_field_ids,reference_role,report_sections,topic_sections,occurrence_locators,render_status,notes\n" +
                "MAT-P001-PDF,04-证据仓/P001--2024--material/source.txt,pdf,v1,,core-argument,03-逐篇精读/P001--2024--material/02-深度说理报告.md,E-P001-001,CLM-P001-001,F02,,2,,,passed,\n" +
                "MAT-P001-SI,04-证据仓/P001--2024--material/missing-si.pdf,supplementary,v1,,unavailable,,,,,,,,,not-applicable,not obtained\n", encoding="utf-8")
            result = self.run_py(MATERIAL_AUDIT, "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"orphan_ids": 0', result.stdout)

    def test_topic_gate_rejects_tutorial_structure(self):
        with tempfile.TemporaryDirectory(prefix="paper-record-") as td:
            root = Path(td) / "batch"
            topic = root / "05-主题研究图谱/T01--demo"; topic.mkdir(parents=True)
            bodies = {
                "00-主题入口.md": "主题边界 总研究问题 研究决策 E-P001-001 CLM-P001-001",
                "01-问题树.md": "总研究问题 未解决 Evidence E-P001-001 CLM-P001-001",
                "02-理论与方法谱系.md": "机制 关键假设 失败模式 E-P001-001 CLM-P001-001",
                "03-论文关系与可比性.md": "可比 不可比 关系类型 E-P001-001 CLM-P001-001",
                "04-证据差异与结果对照.md": "证据 指标 可信范围 E-P001-001 CLM-P001-001",
                "05-失败模式与边界.md": "失败模式 外推边界 不能推出 E-P001-001 CLM-P001-001",
                "06-可检验研究机会.md": "可检验研究问题 自变量 因变量 基线 成功判据 E-P001-001 CLM-P001-001",
            }
            for name, body in bodies.items():
                (topic / name).write_text(body + "\n# 入门\n", encoding="utf-8")
            result = self.run_py(TOPIC_CHECK, "--root", str(root))
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"passed": false', result.stdout)

    def test_integrated_fixture_passes_all_quality_gates(self):
        fixture = SKILL / "tests/fixtures/phase5-valid/batch"
        with tempfile.TemporaryDirectory(prefix="paper-record-integrated-") as td:
            root = Path(td) / "batch"
            shutil.copytree(fixture, root)
            result = self.run_py(QUALITY_GATES, "--root", str(root), "--skill-root", str(SKILL))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            audit = json.loads((root / "09-质量审计/总门禁结果.json").read_text(encoding="utf-8"))
            self.assertTrue(audit["passed"])
            self.assertTrue(all(check["passed"] for check in audit["checks"]))

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
