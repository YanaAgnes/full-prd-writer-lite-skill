#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_gold_slice_regression as validator


class ValidateGoldSliceRegressionTest(unittest.TestCase):
    def write_temp(self, text: str) -> Path:
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
        with temp:
            temp.write(text)
        return Path(temp.name)

    def test_finds_missing_profile_anchors(self) -> None:
        path = self.write_temp("只写支持相关操作，没有表单细节。")
        findings = validator.check_text(path.read_text(encoding="utf-8"), ["form-detail"])
        self.assertTrue(findings)
        self.assertIn("form-detail", findings[0].profile)

    def test_passes_when_profile_anchors_are_present(self) -> None:
        text = "入口 按钮 嵌套表单 字段 展示规则 填写规则 校验 状态变化 验收"
        path = self.write_temp(text)
        findings = validator.check_text(path.read_text(encoding="utf-8"), ["form-detail"])
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
