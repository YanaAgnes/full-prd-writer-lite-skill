#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
DISCOVERY = ROOT / "references" / "prd-discovery-workflow.md"
CHAPTER_RULES = ROOT / "references" / "full-prd-chapter-rules.md"


class RequirementUnitLocalGateRulesTest(unittest.TestCase):
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def assert_has_terms(self, text: str, terms: list[str]) -> None:
        missing = [term for term in terms if term not in text]
        self.assertEqual(missing, [], f"missing requirement-unit local gate terms: {missing}")

    def test_skill_and_workflow_name_the_local_gate_script(self) -> None:
        combined = "\n".join([self.read(SKILL), self.read(DISCOVERY)])
        self.assert_has_terms(
            combined,
            [
                "scripts/validate_requirement_unit_gate.py",
                "local-anchor-contract",
                "consumption-map",
                "local-gate-report",
            ],
        )

    def test_chapter_rules_require_local_contract_and_failure_taxonomy(self) -> None:
        text = self.read(CHAPTER_RULES)
        self.assert_has_terms(
            text,
            [
                "source-evidence",
                "local-anchor-contract",
                "consumption-map",
                "missing anchor",
                "weak anchor",
                "global-only anchor",
            ],
        )


if __name__ == "__main__":
    unittest.main()
