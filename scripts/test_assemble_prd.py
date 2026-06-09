#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("assemble_prd.py")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class AssemblePrdTest(unittest.TestCase):
    def make_workspace(self, root: Path) -> tuple[Path, Path, Path]:
        workspace = root / "workspace"
        chapters = workspace / "chapters"
        chapters.mkdir(parents=True)

        body_a = "# 0. 修订记录\n\n| 版本 | 内容 |\n| --- | --- |\n| V1 | 初始化 |"
        body_b = "# 1. 文档信息\n\n| 项目 | 内容 |\n| --- | --- |\n| 名称 | 示例 |"
        (chapters / "00.md").write_text(
            f"<!-- PRD-BLOCK:B-0001 START -->\n{body_a}\n<!-- PRD-BLOCK:B-0001 END -->\n",
            encoding="utf-8",
        )
        (chapters / "01.md").write_text(
            f"<!-- PRD-BLOCK:B-0002 START -->\n{body_b}\n<!-- PRD-BLOCK:B-0002 END -->\n",
            encoding="utf-8",
        )

        manifest = workspace / "ASSEMBLY-MANIFEST.md"
        manifest.write_text(
            "\n".join(
                [
                    "<!-- ASSEMBLY-MANIFEST:START -->",
                    "| block_id | requirement_unit | source_file | state | order | sha256 | final_location |",
                    "| --- | --- | --- | --- | --- | --- | --- |",
                    f"| B-0001 | F-A | chapters/00.md | 已冻结 | 1 | {digest(body_a)} | 0 |",
                    f"| B-0002 | F-B | chapters/01.md | 已冻结 | 2 | {digest(body_b)} | 1 |",
                    "<!-- ASSEMBLY-MANIFEST:END -->",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return workspace, manifest, workspace / "FULL-PRD.md"

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_assembly_outputs_clean_final_and_check_existing_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace, manifest, output = self.make_workspace(Path(tmp))

            result = self.run_script(
                "--workspace",
                str(workspace),
                "--manifest",
                str(manifest),
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            final_text = output.read_text(encoding="utf-8")
            self.assertNotIn("PRD-BLOCK", final_text)
            self.assertIn("# 0. 修订记录", final_text)
            self.assertIn("# 1. 文档信息", final_text)

            check = self.run_script(
                "--workspace",
                str(workspace),
                "--manifest",
                str(manifest),
                "--output",
                str(output),
                "--check-existing",
            )
            self.assertEqual(check.returncode, 0, check.stderr)

    def test_check_existing_rejects_modified_final(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace, manifest, output = self.make_workspace(Path(tmp))
            result = self.run_script(
                "--workspace",
                str(workspace),
                "--manifest",
                str(manifest),
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output.write_text(
                output.read_text(encoding="utf-8") + "\n未登记正文\n",
                encoding="utf-8",
            )

            check = self.run_script(
                "--workspace",
                str(workspace),
                "--manifest",
                str(manifest),
                "--output",
                str(output),
                "--check-existing",
            )
            self.assertNotEqual(check.returncode, 0)
            self.assertIn("content differs", check.stderr)


if __name__ == "__main__":
    unittest.main()
