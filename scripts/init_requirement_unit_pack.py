#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GateProfile:
    title: str
    seed_anchors: list[str]
    specialized_ledger: str | None


GATE_PROFILES = {
    "form-detail": GateProfile(
        title="form-detail gate",
        seed_anchors=[
            "入口",
            "按钮",
            "嵌套表单",
            "字段",
            "展示规则",
            "填写规则",
            "校验规则",
            "状态变化",
            "验收",
        ],
        specialized_ledger="form-detail-ledger",
    ),
    "workflow-permission-message": GateProfile(
        title="workflow-permission-message gate",
        seed_anchors=[
            "流程节点按钮",
            "菜单权限",
            "页面/列表按钮权限",
            "数据权限",
            "外部平台控制权限",
            "详情操作",
            "状态变化",
            "消息通知",
            "外部跳转",
            "日志/审批记录",
        ],
        specialized_ledger="message-notification-ledger",
    ),
    "object-lifecycle": GateProfile(
        title="object-lifecycle gate",
        seed_anchors=[
            "业务对象状态",
            "资源/对象类型",
            "关联规则",
            "撤销/取消规则",
            "外部状态一致性",
            "详情区块",
            "异常分支",
            "验收",
        ],
        specialized_ledger="object-lifecycle-ledger",
    ),
    "derived-list-time-rule": GateProfile(
        title="derived-list-time-rule gate",
        seed_anchors=[
            "列表生成规则",
            "时间阈值",
            "计算口径",
            "任务 ID",
            "提醒/催办",
            "反馈记录",
            "防重处理",
            "验收",
        ],
        specialized_ledger="derived-list-time-rule-ledger",
    ),
}


def source_evidence_template(unit: str, gate: str) -> str:
    return "\n".join(
        [
            f"# {unit} source-evidence",
            "",
            "## 使用规则",
            "- 这里只记录原文保真或表格保真证据，不写摘要句。",
            "- 每条证据必须保留 `source_id` 和来源定位；后续正文保真以这里为准。",
            f"- 当前 gate: `{gate}`。",
            "",
            "## Evidence Table",
            "| evidence_id | source_id | location | evidence_type | content |",
            "| --- | --- | --- | --- | --- |",
        ]
    )


def source_extract_template(unit: str) -> str:
    return "\n".join(
        [
            f"# {unit} source-extract",
            "",
            "## 说明",
            "- 这里可以按页面、对象、流程或角色重组证据。",
            "- `source-extract` 只是工作提炼物，不能覆盖 `source-evidence`。",
            "",
            "## Suggested Groups",
            "### 页面 / 入口",
            "",
            "### 字段 / 按钮 / 状态",
            "",
            "### 权限 / 消息 / 外部协同",
            "",
            "### 异常 / 兜底 / 待确认",
            "",
        ]
    )


def local_anchor_contract_template(unit: str, profile: GateProfile) -> str:
    lines = [
        f"# {unit} local-anchor-contract",
        "",
        "## Gate Profile Seed",
        f"- gate: `{profile.title}`",
        f"- specialized ledger hint: `{profile.specialized_ledger or 'none'}`",
        "- 先用下列 seed anchors 扫描证据，再把有证据支撑的锚点写入合同表。",
        "- 证据不足的 seed anchor 不得静默消失，应转入待确认项或显式标记 `不涉及`。",
        "",
    ]
    lines.extend([f"- {anchor}" for anchor in profile.seed_anchors])
    lines.extend(
        [
            "",
            "## Contract Rows",
            "| anchor_id | anchor | required_terms | weak_terms |",
            "| --- | --- | --- | --- |",
        ]
    )
    return "\n".join(lines)


def chapter_block_template(unit: str, profile: GateProfile) -> str:
    checklist = [f"- [ ] {anchor}" for anchor in profile.seed_anchors]
    return "\n".join(
        [
            f"# {unit} chapter-block",
            "",
            "## 元信息",
            f"- gate: `{profile.title}`",
            "- target chapter section: <填写，例如 7.3 需求审核>",
            "- source scope: <填写本轮纳入的 source_id>",
            "",
            "## 局部保真检查清单",
            *checklist,
            "",
            "## 正文草稿",
            "### <待填写章节标题>",
            "",
        ]
    )


def consumption_map_template(unit: str) -> str:
    return "\n".join(
        [
            f"# {unit} consumption-map",
            "",
            "## 使用规则",
            "- 每个 `anchor_id` 都要回填到具体正文位置。",
            "- `evidence_refs` 填 `E-...`；`ledger_refs` 填 `permission-ledger:...` / `message-notification-ledger:...` 等。",
            "",
            "| anchor_id | chapter_section | evidence_refs | ledger_refs |",
            "| --- | --- | --- | --- |",
        ]
    )


def local_gate_report_template(unit: str) -> str:
    return "\n".join(
        [
            f"# {unit} local-gate-report",
            "",
            "## Latest Run",
            "- status: not-run",
            "- validator: `scripts/validate_requirement_unit_gate.py`",
            "- result: 未执行",
            "- notes:",
            "",
        ]
    )


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a high-risk requirement-unit pack with local fidelity artifacts."
    )
    parser.add_argument("--root", type=Path, required=True, help="PRD workspace root")
    parser.add_argument("--unit", required=True, help="requirement-unit folder name")
    parser.add_argument(
        "--gate",
        required=True,
        choices=sorted(GATE_PROFILES.keys()),
        help="Gold gate or matching high-risk profile",
    )
    parser.add_argument(
        "--pack-type",
        choices=["function", "global"],
        default="function",
        help="choose function-packs or global-packs",
    )
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    profile = GATE_PROFILES[args.gate]
    pack_root = args.root / ("function-packs" if args.pack_type == "function" else "global-packs") / args.unit

    files = {
        pack_root / "source-evidence.md": source_evidence_template(args.unit, args.gate),
        pack_root / "source-extract.md": source_extract_template(args.unit),
        pack_root / "local-anchor-contract.md": local_anchor_contract_template(args.unit, profile),
        pack_root / "chapter-block.md": chapter_block_template(args.unit, profile),
        pack_root / "consumption-map.md": consumption_map_template(args.unit),
        pack_root / "local-gate-report.md": local_gate_report_template(args.unit),
    }

    try:
        for path, content in files.items():
            write_file(path, content, args.force)
    except FileExistsError as exc:
        print(f"SCAFFOLD_FAILED: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"SCAFFOLD_FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"SCAFFOLD_CREATED: {pack_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
