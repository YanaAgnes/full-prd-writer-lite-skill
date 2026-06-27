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
