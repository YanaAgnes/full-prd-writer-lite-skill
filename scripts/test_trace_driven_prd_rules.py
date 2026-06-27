#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
DISCOVERY = ROOT / "references" / "prd-discovery-workflow.md"
CHAPTER_RULES = ROOT / "references" / "full-prd-chapter-rules.md"


class TraceDrivenPrdRulesTest(unittest.TestCase):
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
        self.assertEqual(missing, [], f"missing required trace-driven rules: {missing}")

    def test_trace_failure_categories_are_mandatory_rules(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "source-inventory",
                "applicability-matrix",
                "permission-ledger",
                "structure-decision-record",
                "cross-cutting-rule-ledger",
                "migration-preservation-check",
                "function-code-policy",
                "trace-issue-taxonomy",
            ],
        )

    def test_applicability_and_permission_dimensions_are_explicit(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "资源类型 / 对象类型",
                "平台端",
                "菜单权限",
                "页面/列表按钮权限",
                "流程节点按钮权限",
                "数据权限",
                "外部平台控制权限",
            ],
        )

    def test_preservation_rules_cover_accepted_content_and_final_files(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "已接受详细内容",
                "结构迁移不得重新摘要",
                "ASCII fallback filename",
                "文件可读取性校验",
            ],
        )

    def test_high_risk_units_require_scaffold_and_template_reference(self) -> None:
        text = self.read_all()
        self.assert_has_terms(
            text,
            [
                "scripts/init_requirement_unit_pack.py",
                "references/requirement-unit-pack-templates.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
