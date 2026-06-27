#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
DISCOVERY = ROOT / "references" / "prd-discovery-workflow.md"
CHAPTER_RULES = ROOT / "references" / "full-prd-chapter-rules.md"


class GoldSliceRegressionRulesTest(unittest.TestCase):
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
        self.assertEqual(missing, [], f"missing gold-slice regression terms: {missing}")

    def test_gold_slice_failure_modes_are_named(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "Gold Slice Regression Gates",
                "form-detail gate",
                "workflow-permission-message gate",
                "object-lifecycle gate",
                "derived-list-time-rule gate",
            ],
        )

    def test_specialized_ledgers_are_available_for_complex_units(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "form-detail-ledger",
                "message-notification-ledger",
                "object-lifecycle-ledger",
                "derived-list-time-rule-ledger",
            ],
        )

    def test_chapter_7_rules_preserve_gold_slice_anchors(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "入口、按钮、嵌套表单、字段、展示规则、填写规则",
                "模板、触发矩阵、接收对象内容表、变量字典、日志开关",
                "库表、文件、接口、归集状态、确认完成归集、资源已注销",
                "即将超期任务清单、超期任务清单、催办反馈清单、督办编号、催办编号",
            ],
        )

    def test_quality_validation_mentions_gold_slice_regression(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "gold-slice-regression-check",
                "Gold Set v0.1",
                "不要求逐字复制 Gold Slice",
                "必须覆盖每个 slice 的保真锚点",
            ],
        )


if __name__ == "__main__":
    unittest.main()
