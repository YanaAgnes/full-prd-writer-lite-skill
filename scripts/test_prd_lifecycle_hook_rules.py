#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
DISCOVERY = ROOT / "references" / "prd-discovery-workflow.md"


class PrdLifecycleHookRulesTest(unittest.TestCase):
    def read_all(self) -> str:
        return "\n".join(
            [
                SKILL.read_text(encoding="utf-8"),
                DISCOVERY.read_text(encoding="utf-8"),
            ]
        )

    def test_skill_requires_engineering_hook_for_loop_and_release_gates(self) -> None:
        text = self.read_all()
        missing = [
            term
            for term in [
                "scripts/prd_lifecycle_hook.py",
                "init-workspace",
                "validate-function-coverage",
                "init-leaf-queue",
                "complete-task",
                "validate-release-ready",
                "--require-packs",
                "TO-CHECK-FUNCTIONS.md",
                "Hook 不生成 PRD 正文",
            ]
            if term not in text
        ]
        self.assertEqual(missing, [], f"missing lifecycle hook rules: {missing}")

    def test_coverage_gate_is_a_hard_stop_before_leaf_loop(self) -> None:
        text = self.read_all()
        missing = [
            term
            for term in [
                "没有通过 coverage gate，不得进入 leaf loop",
                "没有通过 init-leaf-queue，不得声称叶子功能循环已建立",
                "没有通过 complete-task --require-packs，不得把叶子功能置为 To Check / 已生成",
                "没有清空 To Generate / To Check，不得发布",
                "工程 Hook 负责阻断",
            ]
            if term not in text
        ]
        self.assertEqual(missing, [], f"missing hard-stop rules: {missing}")


if __name__ == "__main__":
    unittest.main()
