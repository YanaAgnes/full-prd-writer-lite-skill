#!/usr/bin/env python3
"""Engineering hook for full-PRD generation lifecycle control.

The hook enforces deterministic workflow constraints. It does not interpret
requirements or generate PRD prose.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path


OVERVIEW_CANDIDATES = [
    "Function 总览检查表.md",
    "TO-CHECK-FUNCTIONS.md",
]
OPEN_STATES = {"To Generate", "To Check", "待生成", "待检查", "to generate", "to check"}
DONE_STATE = "已生成"


@dataclass
class Table:
    header: list[str]
    row_indexes: list[int]
    rows: list[list[str]]


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def is_separator_row(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def find_table(lines: list[str], required_headers: set[str]) -> Table:
    for idx, line in enumerate(lines):
        header = split_row(line)
        if not header or not required_headers.issubset(set(header)):
            continue
        if idx + 1 >= len(lines) or not is_separator_row(lines[idx + 1]):
            continue
        row_indexes: list[int] = []
        rows: list[list[str]] = []
        cursor = idx + 2
        while cursor < len(lines):
            if not lines[cursor].lstrip().startswith("|"):
                break
            if not is_separator_row(lines[cursor]):
                cells = split_row(lines[cursor])
                if len(cells) == len(header):
                    row_indexes.append(cursor)
                    rows.append(cells)
            cursor += 1
        return Table(header, row_indexes, rows)
    raise ValueError(f"markdown table not found for headers: {sorted(required_headers)}")


def row_dict(table: Table, row: list[str]) -> dict[str, str]:
    return dict(zip(table.header, row))


def render_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |\n"


def default_overview(workspace: Path) -> Path:
    for name in OVERVIEW_CANDIDATES:
        candidate = workspace / name
        if candidate.exists():
            return candidate
    return workspace / OVERVIEW_CANDIDATES[0]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_text("".join(lines), encoding="utf-8")


def ensure_file(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")


def cmd_init_workspace(args: argparse.Namespace) -> int:
    workspace = args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    for relative in [
        "source-ledger/extracts",
        "function-packs",
        "global-packs",
        "chapters/06-user-stories",
        "chapters/07-functions",
        "chapters/08-collaboration",
    ]:
        (workspace / relative).mkdir(parents=True, exist_ok=True)

    ensure_file(
        workspace / "PRD-CONTROL.md",
        f"""
        # PRD-CONTROL

        | 项目 | 内容 |
        | --- | --- |
        | 系统名称 | {args.system_name} |
        | 目标版本 | {args.target_version} |
        | 主源文档 | {args.source} |
        | 当前阶段 | source-inventory |
        | 下一动作 | 建立 function-inventory-ledger 并执行 function-inventory-coverage-gate |
        """,
    )
    ensure_file(
        workspace / "source-ledger" / "source-inventory.md",
        f"""
        # Source Inventory

        | Source ID | File/material | Material type | Version/date | User-declared role | Discovered role | Include? | Exclusion or risk | Readability |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        | SRC-001 | {args.source} | formal baseline |  | primary source | pending scan | yes |  | pending |
        """,
    )
    ensure_file(
        workspace / "source-ledger" / "function-inventory-ledger.md",
        """
        # Function Inventory Ledger

        | Candidate ID | Normalized function | Source-location | Source type | Evidence | Coverage disposition | Function ID | Target section | Pending ID | Notes |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        """,
    )
    ensure_file(
        workspace / "source-ledger" / "coverage-matrix.md",
        """
        # Coverage Matrix

        | Function ID | Function | Source requirements | Roles | Stories | Flow/state | Chapter 7 | Chapter 8 | Acceptance | State |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        """,
    )
    print(f"PRD_WORKSPACE_INITIALIZED: {workspace}")
    return 0


def overview_table(path: Path) -> tuple[list[str], Table]:
    lines = read_lines(path)
    table = find_table(lines, {"功能编号", "状态"})
    return lines, table


def overview_ids(path: Path) -> set[str]:
    _lines, table = overview_table(path)
    return {
        row_dict(table, row).get("功能编号", "")
        for row in table.rows
        if row_dict(table, row).get("功能编号", "")
    }


def coverage_findings(workspace: Path, overview: Path) -> list[str]:
    ledger = workspace / "source-ledger" / "function-inventory-ledger.md"
    if not ledger.exists():
        return [f"missing function-inventory-ledger: {ledger}"]

    ledger_lines = read_lines(ledger)
    ledger_table = find_table(ledger_lines, {"Candidate ID", "Coverage disposition"})
    ids = overview_ids(overview)
    findings: list[str] = []

    for row in ledger_table.rows:
        item = row_dict(ledger_table, row)
        candidate = item.get("Candidate ID", "")
        disposition = item.get("Coverage disposition", "")
        function_id = item.get("Function ID", "")
        pending_id = item.get("Pending ID", "")

        for required in ["Source-location", "Source type", "Evidence"]:
            if not item.get(required, "").strip():
                findings.append(f"{candidate}: missing {required}")

        if disposition == "include-in-overview":
            if not function_id:
                findings.append(f"{candidate}: include-in-overview requires Function ID")
            elif function_id not in ids:
                findings.append(f"{candidate}: {function_id} missing from Function 总览检查表")
        elif disposition == "pending-for-product-confirmation":
            if not pending_id.startswith("PEND-"):
                findings.append(f"{candidate}: pending disposition requires PEND- item")
        elif disposition == "merge-into-existing-function":
            if function_id and function_id not in ids:
                findings.append(f"{candidate}: merged target {function_id} missing from overview")
        elif disposition == "explicit-exclusion":
            if not item.get("Notes", "").strip():
                findings.append(f"{candidate}: explicit exclusion requires Notes reason")
        else:
            findings.append(f"{candidate}: invalid Coverage disposition {disposition!r}")

    return findings


def cmd_validate_function_coverage(args: argparse.Namespace) -> int:
    workspace = args.workspace.resolve()
    overview = (args.overview or default_overview(workspace)).resolve()
    findings = coverage_findings(workspace, overview)
    if findings:
        for finding in findings:
            print(f"FUNCTION_COVERAGE_FAILED: {finding}", file=sys.stderr)
        return 1
    print("FUNCTION_COVERAGE_PASSED")
    return 0


def update_pointer(lines: list[str], title: str, status: str, note: str) -> None:
    replacements = {
        "当前叶子功能": title,
        "当前状态": status,
        "本轮处理内容": note,
    }
    for key, value in replacements.items():
        pattern = re.compile(rf"^\| {re.escape(key)} \| .* \|$")
        for idx, line in enumerate(lines):
            if pattern.match(line.strip()):
                lines[idx] = f"| {key} | {value} |\n"
                break


def upsert_review(lines: list[str], function_id: str, result: str, note: str) -> None:
    record = f"| {function_id} | Hook | {result} | {note} |\n"
    try:
        table = find_table(lines, {"功能编号", "检查人", "检查结果", "备注"})
    except ValueError:
        lines.extend(
            [
                "\n## 产品检查记录\n\n",
                "| 功能编号 | 检查人 | 检查结果 | 备注 |\n",
                "| --- | --- | --- | --- |\n",
                record,
            ]
        )
        return

    id_col = table.header.index("功能编号")
    for idx, row in zip(table.row_indexes, table.rows):
        if row[id_col] == function_id:
            lines[idx] = record
            return
    insert_at = table.row_indexes[-1] + 1 if table.row_indexes else None
    if insert_at is None:
        header_line = next(
            idx
            for idx, line in enumerate(lines)
            if split_row(line) == table.header
        )
        insert_at = header_line + 2
    lines.insert(insert_at, record)


def cmd_complete_task(args: argparse.Namespace) -> int:
    workspace = args.workspace.resolve()
    overview = (args.overview or default_overview(workspace)).resolve()
    lines, table = overview_table(overview)
    id_col = table.header.index("功能编号")
    status_col = table.header.index("状态")
    name_col = table.header.index("功能名称") if "功能名称" in table.header else None
    result_col = table.header.index("产品检查结果") if "产品检查结果" in table.header else None

    target_position: int | None = None
    next_title = ""
    for position, row in enumerate(table.rows):
        if row[id_col] == args.function_id:
            target_position = position
            if row[status_col] == DONE_STATE and not args.force:
                print(f"{args.function_id} already {DONE_STATE}", file=sys.stderr)
                return 2
            row[status_col] = "To Check"
            if result_col is not None:
                row[result_col] = "待检查"
            lines[table.row_indexes[position]] = render_row(row)
            title = f"{row[id_col]} {row[name_col]}" if name_col is not None else row[id_col]
            update_pointer(lines, title, "To Check", args.note or "已完成原文对照和 PRD 正文更新。")
            break

    if target_position is None:
        print(f"unknown function id: {args.function_id}", file=sys.stderr)
        return 2

    if args.stop_at and args.function_id == args.stop_at:
        write_lines(overview, lines)
        print(f"PRD_LOOP_STOPPED_FOR_PRODUCT_CHECK: {args.function_id}")
        return 20

    if args.auto_approve:
        row = table.rows[target_position]
        row[status_col] = DONE_STATE
        if result_col is not None:
            row[result_col] = "默认检查通过"
        lines[table.row_indexes[target_position]] = render_row(row)
        upsert_review(
            lines,
            args.function_id,
            "默认检查通过",
            f"用户授权默认通过，{_dt.date.today().isoformat()}",
        )

        for row in table.rows[target_position + 1 :]:
            if row[status_col] in {"To Generate", "待生成", "to generate"}:
                next_title = f"{row[id_col]} {row[name_col]}" if name_col is not None else row[id_col]
                update_pointer(lines, next_title, "To Generate", "等待执行原文读取、细节补充和正文生成。")
                break
        if not next_title:
            update_pointer(lines, "无", DONE_STATE, "全部叶子功能已完成，等待发布前校验。")

    write_lines(overview, lines)
    print(f"PRD_TASK_COMPLETED: {args.function_id}")
    return 0


def release_findings(workspace: Path, overview: Path) -> list[str]:
    _lines, table = overview_table(overview)
    findings: list[str] = []
    status_col = table.header.index("状态")
    id_col = table.header.index("功能编号")
    for row in table.rows:
        if row[status_col] in OPEN_STATES:
            findings.append(f"{row[id_col]} remains {row[status_col]}")
    ledger = workspace / "source-ledger" / "function-inventory-ledger.md"
    if ledger.exists():
        findings.extend(coverage_findings(workspace, overview))
    return findings


def cmd_validate_release_ready(args: argparse.Namespace) -> int:
    workspace = args.workspace.resolve()
    overview = (args.overview or default_overview(workspace)).resolve()
    findings = release_findings(workspace, overview)
    if findings:
        for finding in findings:
            print(f"RELEASE_NOT_READY: {finding}", file=sys.stderr)
        return 1
    print("RELEASE_READY_PASSED")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init-workspace")
    init.add_argument("--workspace", type=Path, required=True)
    init.add_argument("--source", required=True)
    init.add_argument("--system-name", required=True)
    init.add_argument("--target-version", required=True)
    init.set_defaults(func=cmd_init_workspace)

    coverage = sub.add_parser("validate-function-coverage")
    coverage.add_argument("--workspace", type=Path, required=True)
    coverage.add_argument("--overview", type=Path)
    coverage.set_defaults(func=cmd_validate_function_coverage)

    complete = sub.add_parser("complete-task")
    complete.add_argument("--workspace", type=Path, required=True)
    complete.add_argument("--overview", type=Path)
    complete.add_argument("--function-id", required=True)
    complete.add_argument("--note")
    complete.add_argument("--auto-approve", action="store_true")
    complete.add_argument("--stop-at")
    complete.add_argument("--force", action="store_true")
    complete.set_defaults(func=cmd_complete_task)

    release = sub.add_parser("validate-release-ready")
    release.add_argument("--workspace", type=Path, required=True)
    release.add_argument("--overview", type=Path)
    release.set_defaults(func=cmd_validate_release_ready)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"PRD_HOOK_FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
