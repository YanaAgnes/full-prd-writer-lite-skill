#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_WEAK_TERMS = [
    "支持相关操作",
    "查询条件保持一致",
    "按权限控制",
    "系统按规则处理",
    "查看详情",
]


@dataclass(frozen=True)
class Finding:
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.kind}: {self.detail}"


@dataclass(frozen=True)
class ContractRow:
    anchor_id: str
    anchor: str
    required_terms: list[list[str]]
    weak_terms: list[str]


@dataclass(frozen=True)
class ConsumptionRow:
    anchor_id: str
    chapter_section: str
    evidence_refs: str
    ledger_refs: str


def split_cell(value: str) -> list[str]:
    return [item.strip() for item in value.split("/") if item.strip()]


def split_required_terms(value: str) -> list[list[str]]:
    groups: list[list[str]] = []
    for item in split_cell(value):
        aliases = [alias.strip() for alias in re.split(r"\s+or\s+", item) if alias.strip()]
        if aliases:
            groups.append(aliases)
    return groups


def extract_table_block(text: str) -> list[str]:
    lines = text.splitlines()
    tables: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            current.append(stripped)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    for table in tables:
        if len(table) >= 2:
            return table
    raise ValueError("missing markdown table")


def parse_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_contract(path: Path) -> list[ContractRow]:
    table = extract_table_block(path.read_text(encoding="utf-8"))
    header = parse_row(table[0])
    indexes = {name: idx for idx, name in enumerate(header)}
    required_columns = ["anchor_id", "anchor", "required_terms"]
    missing = [column for column in required_columns if column not in indexes]
    if missing:
        raise ValueError(f"contract missing columns: {missing}")
    weak_index = indexes.get("weak_terms")

    rows: list[ContractRow] = []
    for line in table[2:]:
        cells = parse_row(line)
        if len(cells) != len(header):
            raise ValueError(f"contract row has wrong column count: {line}")
        required_terms = split_required_terms(cells[indexes["required_terms"]])
        if not required_terms:
            raise ValueError(f"contract row has no required_terms: {line}")
        weak_terms = split_cell(cells[weak_index]) if weak_index is not None else []
        rows.append(
            ContractRow(
                anchor_id=cells[indexes["anchor_id"]],
                anchor=cells[indexes["anchor"]],
                required_terms=required_terms,
                weak_terms=weak_terms,
            )
        )
    if not rows:
        raise ValueError("contract has no data rows")
    return rows


def parse_consumption_map(path: Path) -> dict[str, list[ConsumptionRow]]:
    table = extract_table_block(path.read_text(encoding="utf-8"))
    header = parse_row(table[0])
    indexes = {name: idx for idx, name in enumerate(header)}
    required_columns = ["anchor_id", "chapter_section", "evidence_refs", "ledger_refs"]
    missing = [column for column in required_columns if column not in indexes]
    if missing:
        raise ValueError(f"consumption-map missing columns: {missing}")

    rows: dict[str, list[ConsumptionRow]] = {}
    for line in table[2:]:
        cells = parse_row(line)
        if len(cells) != len(header):
            raise ValueError(f"consumption-map row has wrong column count: {line}")
        row = ConsumptionRow(
            anchor_id=cells[indexes["anchor_id"]],
            chapter_section=cells[indexes["chapter_section"]],
            evidence_refs=cells[indexes["evidence_refs"]],
            ledger_refs=cells[indexes["ledger_refs"]],
        )
        rows.setdefault(row.anchor_id, []).append(row)
    return rows


def find_first_match(text: str, terms: list[str]) -> str | None:
    for term in terms:
        if term and term in text:
            return term
    return None


def find_group_matches(text: str, groups: list[list[str]]) -> tuple[bool, list[str]]:
    matches: list[str] = []
    for group in groups:
        match = find_first_match(text, group)
        if not match:
            return False, matches
        matches.append(match)
    return True, matches


def check_paths(
    *,
    contract_path: Path,
    block_path: Path,
    consumption_map_path: Path,
    evidence_path: Path,
    full_prd_path: Path | None = None,
) -> list[Finding]:
    contract_rows = parse_contract(contract_path)
    consumption_rows = parse_consumption_map(consumption_map_path)
    block_text = block_path.read_text(encoding="utf-8")
    full_text = full_prd_path.read_text(encoding="utf-8") if full_prd_path else ""
    evidence_text = evidence_path.read_text(encoding="utf-8")

    findings: list[Finding] = []
    if not evidence_text.strip():
        findings.append(Finding("missing evidence", "source-evidence is empty"))

    for row in contract_rows:
        block_match, _block_terms = find_group_matches(block_text, row.required_terms)
        full_match, full_terms = (
            find_group_matches(full_text, row.required_terms) if full_text else (False, [])
        )
        weak_match = find_first_match(block_text, row.weak_terms + DEFAULT_WEAK_TERMS)

        if not block_match:
            if full_match:
                findings.append(
                    Finding(
                        "global-only anchor",
                        f"{row.anchor_id} {row.anchor}: required groups appear only outside local block ({' / '.join(full_terms)})",
                    )
                )
            elif weak_match:
                findings.append(
                    Finding(
                        "weak anchor",
                        f"{row.anchor_id} {row.anchor}: weak substitute found in local block ({weak_match})",
                    )
                )
            else:
                findings.append(
                    Finding(
                        "missing anchor",
                        f"{row.anchor_id} {row.anchor}: missing required groups {' / '.join(' or '.join(group) for group in row.required_terms)}",
                    )
                )

        mapped_rows = consumption_rows.get(row.anchor_id, [])
        if not mapped_rows:
            findings.append(
                Finding(
                    "missing consumption",
                    f"{row.anchor_id} {row.anchor}: anchor is absent from consumption-map",
                )
            )
            continue

        if not any(
            mapped_row.chapter_section
            and (mapped_row.evidence_refs.strip() or mapped_row.ledger_refs.strip())
            for mapped_row in mapped_rows
        ):
            findings.append(
                Finding(
                    "missing consumption",
                    f"{row.anchor_id} {row.anchor}: consumption-map lacks chapter section or evidence/ledger refs",
                )
            )

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one high-risk requirement unit against its local anchor contract."
    )
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--block", type=Path, required=True)
    parser.add_argument("--consumption-map", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--full-prd", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        findings = check_paths(
            contract_path=args.contract,
            block_path=args.block,
            consumption_map_path=args.consumption_map,
            evidence_path=args.evidence,
            full_prd_path=args.full_prd,
        )
    except (OSError, ValueError) as exc:
        print(f"LOCAL_GATE_FAILED: {exc}", file=sys.stderr)
        return 1

    if findings:
        for finding in findings:
            print(finding, file=sys.stderr)
        return 1

    print(f"LOCAL_GATE_PASSED: {args.block}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
