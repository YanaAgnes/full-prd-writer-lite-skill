#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
DISCOVERY = ROOT / "references" / "prd-discovery-workflow.md"
CHAPTER_RULES = ROOT / "references" / "full-prd-chapter-rules.md"


class FunctionInventoryCoverageRulesTest(unittest.TestCase):
    def read_all(self) -> str:
        return "\n".join(
            [
                SKILL.read_text(encoding="utf-8"),
                DISCOVERY.read_text(encoding="utf-8"),
                CHAPTER_RULES.read_text(encoding="utf-8"),
            ]
        )

    def assert_has_terms(self, text: str, terms: list[str]) -> None:
        missing = [term for term in terms if term not in text]
        self.assertEqual(missing, [], f"missing function inventory coverage rules: {missing}")

    def test_function_inventory_cross_source_gate_is_mandatory(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "function-inventory-coverage-gate",
                "function-inventory-ledger",
                "功能架构",
                "功能汇总",
                "目录 / TOC",
                "角色权限",
                "OCR",
            ],
        )

    def test_tentative_and_no_detail_functions_must_not_disappear(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "待定",
                "正文缺失",
                "To Generate",
                "明确排除",
                "PEND-",
                "不得因为缺少详细正文",
            ],
        )

    def test_overview_and_chapter_7_must_be_reconciled(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "Function 总览检查表",
                "Chapter 7 功能结构总览",
                "source-location",
                "coverage disposition",
            ],
        )


if __name__ == "__main__":
    unittest.main()
