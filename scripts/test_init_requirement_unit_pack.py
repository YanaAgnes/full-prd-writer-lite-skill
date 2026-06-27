#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import init_requirement_unit_pack as scaffold


class InitRequirementUnitPackTest(unittest.TestCase):
    def run_main(self, argv: list[str]) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return scaffold.main(argv)

    def test_creates_workflow_permission_message_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            exit_code = self.run_main(
                [
                    "--root",
                    str(root),
                    "--unit",
                    "data-demand-approval",
                    "--gate",
                    "workflow-permission-message",
                ]
            )

            self.assertEqual(exit_code, 0)

            pack_root = root / "function-packs" / "data-demand-approval"
            self.assertTrue((pack_root / "source-evidence.md").exists())
            self.assertTrue((pack_root / "source-extract.md").exists())
            self.assertTrue((pack_root / "local-anchor-contract.md").exists())
            self.assertTrue((pack_root / "chapter-block.md").exists())
            self.assertTrue((pack_root / "consumption-map.md").exists())
            self.assertTrue((pack_root / "local-gate-report.md").exists())

            contract_text = (pack_root / "local-anchor-contract.md").read_text(encoding="utf-8")
            self.assertIn("| anchor_id | anchor | required_terms | weak_terms |", contract_text)
            self.assertIn("流程节点按钮", contract_text)
            self.assertIn("消息通知", contract_text)

            block_text = (pack_root / "chapter-block.md").read_text(encoding="utf-8")
            self.assertIn("局部保真检查清单", block_text)
            self.assertIn("详情操作", block_text)
            self.assertIn("状态变化", block_text)

            consumption_text = (pack_root / "consumption-map.md").read_text(encoding="utf-8")
            self.assertIn("| anchor_id | chapter_section | evidence_refs | ledger_refs |", consumption_text)

    def test_refuses_to_overwrite_existing_pack_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pack_root = root / "function-packs" / "data-demand-approval"
            pack_root.mkdir(parents=True)
            (pack_root / "chapter-block.md").write_text("existing", encoding="utf-8")

            exit_code = self.run_main(
                [
                    "--root",
                    str(root),
                    "--unit",
                    "data-demand-approval",
                    "--gate",
                    "workflow-permission-message",
                ]
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(
                (pack_root / "chapter-block.md").read_text(encoding="utf-8"),
                "existing",
            )


if __name__ == "__main__":
    unittest.main()
