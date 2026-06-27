#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("prd_lifecycle_hook.py")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


class PrdLifecycleHookTest(unittest.TestCase):
    def run_hook(self, *args: str, cwd: Path | None = None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
        )

    def test_init_workspace_creates_control_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "prd-workspace"
            result = self.run_hook(
                "init-workspace",
                "--workspace",
                str(workspace),
                "--source",
                "source.md",
                "--system-name",
                "示例系统",
                "--target-version",
                "V1.0",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            for relative in [
                "PRD-CONTROL.md",
                "source-ledger/source-inventory.md",
                "source-ledger/function-inventory-ledger.md",
                "source-ledger/coverage-matrix.md",
                "chapters",
            ]:
                self.assertTrue((workspace / relative).exists(), relative)
            self.assertIn("示例系统", (workspace / "PRD-CONTROL.md").read_text(encoding="utf-8"))

    def test_coverage_gate_blocks_missing_overview_function(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            ledger = workspace / "source-ledger" / "function-inventory-ledger.md"
            overview = workspace / "Function 总览检查表.md"
            write(
                ledger,
                """
                | Candidate ID | Normalized function | Source-location | Source type | Evidence | Coverage disposition | Function ID | Target section | Pending ID | Notes |
                | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
                | C-001 | 账户列表 | 1.1 | 正文标题 | 账户列表 | include-in-overview | F-ACCOUNT-001 | 7.1 |  |  |
                | C-002 | 日志管理 | OCR-2 | 功能架构 OCR | 日志管理 | include-in-overview | F-LOG-001 | 7.2 |  |  |
                """,
            )
            write(
                overview,
                """
                | 功能编号 | 功能名称 | 状态 |
                | --- | --- | --- |
                | F-ACCOUNT-001 | 账户列表 | 已生成 |
                """,
            )

            result = self.run_hook(
                "validate-function-coverage",
                "--workspace",
                str(workspace),
                "--overview",
                str(overview),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("F-LOG-001", result.stderr)

    def test_complete_auto_approve_advances_to_next_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            overview = workspace / "Function 总览检查表.md"
            write(
                overview,
                """
                # Function 总览检查表

                ## 当前处理指针

                | 项目 | 内容 |
                | --- | --- |
                | 当前叶子功能 | F-A 账户列表 |
                | 当前状态 | To Generate |
                | 本轮处理内容 | 准备处理 |

                ## 功能总览

                | 功能编号 | 功能名称 | 状态 | 产品检查结果 |
                | --- | --- | --- | --- |
                | F-A | 账户列表 | To Generate |  |
                | F-B | 日志管理 | To Generate |  |

                ## 产品检查记录

                | 功能编号 | 检查人 | 检查结果 | 备注 |
                | --- | --- | --- | --- |
                """,
            )

            result = self.run_hook(
                "complete-task",
                "--workspace",
                str(workspace),
                "--overview",
                str(overview),
                "--function-id",
                "F-A",
                "--auto-approve",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = overview.read_text(encoding="utf-8")
            self.assertIn("| F-A | 账户列表 | 已生成 | 默认检查通过 |", text)
            self.assertIn("| 当前叶子功能 | F-B 日志管理 |", text)
            self.assertIn("| 当前状态 | To Generate |", text)

    def test_init_leaf_queue_creates_to_check_queue_and_packs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            overview = workspace / "Function 总览检查表.md"
            write(
                overview,
                """
                | 功能编号 | 功能名称 | 状态 | 产品检查结果 | 源文档位置 | 详述位置 |
                | --- | --- | --- | --- | --- | --- |
                | F-A | 账户列表 | To Check | 待检查 | 1.1 账户列表 | 7.1 |
                | F-B | 日志管理 | To Check | 待检查 | OCR-2 日志管理 | 7.2 |
                """,
            )

            result = self.run_hook(
                "init-leaf-queue",
                "--workspace",
                str(workspace),
                "--overview",
                str(overview),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            queue = workspace / "TO-CHECK-FUNCTIONS.md"
            self.assertTrue(queue.exists())
            text = queue.read_text(encoding="utf-8")
            self.assertIn("| 当前叶子功能 | F-A 账户列表 |", text)
            self.assertIn("| F-A | 叶子功能 | 账户列表 |", text)
            self.assertIn("| F-A | 叶子功能 | 账户列表 |  |  |  | 7.1 | To Generate | 待生成 | 1.1 账户列表 |", text)
            for relative in [
                "function-packs/F-A/source-evidence.md",
                "function-packs/F-A/local-anchor-contract.md",
                "function-packs/F-A/consumption-map.md",
            ]:
                self.assertTrue((workspace / relative).exists(), relative)

    def test_complete_task_with_pack_gate_blocks_placeholder_packs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            overview = workspace / "Function 总览检查表.md"
            write(
                overview,
                """
                | 功能编号 | 功能名称 | 状态 | 源文档位置 | 详述位置 |
                | --- | --- | --- | --- | --- |
                | F-A | 账户列表 | To Generate | 1.1 账户列表 | 7.1 |
                """,
            )
            init_result = self.run_hook(
                "init-leaf-queue",
                "--workspace",
                str(workspace),
                "--overview",
                str(overview),
            )
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            result = self.run_hook(
                "complete-task",
                "--workspace",
                str(workspace),
                "--overview",
                str(workspace / "TO-CHECK-FUNCTIONS.md"),
                "--function-id",
                "F-A",
                "--require-packs",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("placeholder remains", result.stderr)
            self.assertIn("no data rows", result.stderr)

    def test_complete_task_with_pack_gate_passes_after_pack_is_filled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            overview = workspace / "Function 总览检查表.md"
            write(
                overview,
                """
                | 功能编号 | 功能名称 | 状态 | 源文档位置 | 详述位置 |
                | --- | --- | --- | --- | --- |
                | F-A | 账户列表 | To Generate | 1.1 账户列表 | 7.1 |
                """,
            )
            init_result = self.run_hook(
                "init-leaf-queue",
                "--workspace",
                str(workspace),
                "--overview",
                str(overview),
            )
            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            pack = workspace / "function-packs" / "F-A"
            write(
                pack / "source-evidence.md",
                """
                | evidence_id | source_id | location | evidence_type | content |
                | --- | --- | --- | --- | --- |
                | E-001 | SRC-001 | 1.1 | text | 账户列表原文 |
                """,
            )
            write(
                pack / "local-anchor-contract.md",
                """
                | anchor_id | anchor | required_terms | weak_terms |
                | --- | --- | --- | --- |
                | A-001 | 列表入口 | 账户列表 | 支持相关操作 |
                """,
            )
            write(
                pack / "consumption-map.md",
                """
                | anchor_id | chapter_section | evidence_refs | ledger_refs |
                | --- | --- | --- | --- |
                | A-001 | 7.1 | E-001 | function-inventory-ledger:C-001 |
                """,
            )

            result = self.run_hook(
                "complete-task",
                "--workspace",
                str(workspace),
                "--overview",
                str(workspace / "TO-CHECK-FUNCTIONS.md"),
                "--function-id",
                "F-A",
                "--require-packs",
                "--auto-approve",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = (workspace / "TO-CHECK-FUNCTIONS.md").read_text(encoding="utf-8")
            self.assertIn("| F-A | 叶子功能 | 账户列表 |  |  |  | 7.1 | 已生成 | 默认检查通过 | 1.1 账户列表 |", text)

    def test_release_ready_blocks_unprocessed_and_uncovered_functions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            overview = workspace / "Function 总览检查表.md"
            write(
                overview,
                """
                | 功能编号 | 功能名称 | 状态 |
                | --- | --- | --- |
                | F-A | 账户列表 | 已生成 |
                | F-B | 日志管理 | To Generate |
                """,
            )

            result = self.run_hook(
                "validate-release-ready",
                "--workspace",
                str(workspace),
                "--overview",
                str(overview),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("To Generate", result.stderr)


if __name__ == "__main__":
    unittest.main()
