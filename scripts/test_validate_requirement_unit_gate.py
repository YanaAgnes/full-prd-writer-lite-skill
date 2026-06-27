#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_requirement_unit_gate as validator


class ValidateRequirementUnitGateTest(unittest.TestCase):
    def write_temp(self, text: str) -> Path:
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
        with temp:
            temp.write(text)
        return Path(temp.name)

    def test_detects_missing_anchor(self) -> None:
        contract = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | anchor | required_terms | weak_terms |",
                    "| --- | --- | --- | --- |",
                    "| AUD-001 | 审批编号 | 审批编号 / SP | 支持相关操作 / 查看详情 |",
                ]
            )
        )
        block = self.write_temp("这里只写了审核入口和详情页。")
        consumption = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | chapter_section | evidence_refs | ledger_refs |",
                    "| --- | --- | --- | --- |",
                    "| AUD-001 | 7.3.2 审核详情 | SRC-001 | requirement-ledger:AUD-001 |",
                ]
            )
        )
        evidence = self.write_temp("SRC-001: 原文写明审批编号由需求编号 + SP + 日期 + 顺序号组成。")

        findings = validator.check_paths(
            contract_path=contract,
            block_path=block,
            consumption_map_path=consumption,
            evidence_path=evidence,
        )

        self.assertEqual(findings[0].kind, "missing anchor")

    def test_detects_global_only_anchor(self) -> None:
        contract = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | anchor | required_terms | weak_terms |",
                    "| --- | --- | --- | --- |",
                    "| AUD-002 | 审核超期状态 | 审核超期状态 | 查询条件保持一致 / 支持筛选 |",
                ]
            )
        )
        block = self.write_temp("已处理需求的查询条件与待处理需求保持一致。")
        full_prd = self.write_temp("第 7.3.2 节之外，通知章节中提到了审核超期状态。")
        consumption = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | chapter_section | evidence_refs | ledger_refs |",
                    "| --- | --- | --- | --- |",
                    "| AUD-002 | 7.3.1 已处理需求 | SRC-002 | requirement-ledger:AUD-002 |",
                ]
            )
        )
        evidence = self.write_temp("SRC-002: 已处理需求筛选条件包含审核超期状态。")

        findings = validator.check_paths(
            contract_path=contract,
            block_path=block,
            consumption_map_path=consumption,
            evidence_path=evidence,
            full_prd_path=full_prd,
        )

        self.assertEqual(findings[0].kind, "global-only anchor")

    def test_detects_weak_anchor_and_missing_consumption(self) -> None:
        contract = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | anchor | required_terms | weak_terms |",
                    "| --- | --- | --- | --- |",
                    "| AUD-003 | 同意意见非必填 | 同意意见 / 非必填 / 200 字 | 支持相关操作 / 填写审批意见 |",
                ]
            )
        )
        block = self.write_temp("审核人填写审批意见后支持相关操作。")
        consumption = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | chapter_section | evidence_refs | ledger_refs |",
                    "| --- | --- | --- | --- |",
                ]
            )
        )
        evidence = self.write_temp("SRC-003: 同意意见非必填，长度上限 200 字。")

        findings = validator.check_paths(
            contract_path=contract,
            block_path=block,
            consumption_map_path=consumption,
            evidence_path=evidence,
        )

        self.assertEqual(findings[0].kind, "weak anchor")
        self.assertTrue(any(finding.kind == "missing consumption" for finding in findings))

    def test_passes_when_contract_block_and_consumption_close_the_loop(self) -> None:
        contract = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | anchor | required_terms | weak_terms |",
                    "| --- | --- | --- | --- |",
                    "| AUD-004 | 驳回意见必填 | 驳回意见 / 必填 or 必须填写 / 200 字 | 支持相关操作 / 填写审批意见 |",
                ]
            )
        )
        block = self.write_temp("驳回时审核人必须填写驳回意见，长度上限 200 字。")
        consumption = self.write_temp(
            "\n".join(
                [
                    "| anchor_id | chapter_section | evidence_refs | ledger_refs |",
                    "| --- | --- | --- | --- |",
                    "| AUD-004 | 7.3.2 审核按钮 | SRC-004 | requirement-ledger:AUD-004 |",
                ]
            )
        )
        evidence = self.write_temp("SRC-004: 驳回意见必填，长度上限 200 字。")

        findings = validator.check_paths(
            contract_path=contract,
            block_path=block,
            consumption_map_path=consumption,
            evidence_path=evidence,
        )

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
