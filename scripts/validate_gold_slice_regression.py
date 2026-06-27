#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


GOLD_SET_VERSION = "Gold Set v0.1"

PROFILES: dict[str, list[list[str]]] = {
    "form-detail": [
        ["入口"],
        ["按钮"],
        ["嵌套表单", "表单页面", "子表单", "需求明细", "弹窗"],
        ["字段"],
        ["展示规则"],
        ["填写规则", "校验"],
        ["状态变化", "数据变化", "提交状态"],
        ["验收", "AC-"],
    ],
    "workflow-permission-message": [
        ["流程节点", "节点按钮"],
        ["菜单权限", "页面/列表按钮权限", "流程节点按钮权限", "数据权限"],
        ["详情操作", "详情底部"],
        ["状态流", "状态变更"],
        ["模板", "消息标题"],
        ["触发矩阵", "通知触发"],
        ["接收对象", "通知对象"],
        ["变量字典", "变量"],
        ["日志开关", "消息通知日志"],
        ["外部协同", "EXT-"],
    ],
    "object-lifecycle": [
        ["库表"],
        ["文件"],
        ["接口"],
        ["归集状态"],
        ["确认完成归集"],
        ["资源已注销"],
        ["取消关联"],
        ["资源供给信息"],
        ["最新名称", "名称同步"],
        ["EXT-CATALOG", "EXT-COLLECT", "外部协同"],
    ],
    "derived-list-time-rule": [
        ["即将超期任务清单"],
        ["超期任务清单"],
        ["催办反馈清单"],
        ["督办编号"],
        ["催办编号"],
        ["超期时长"],
        ["工作日", "自然日", "计算类型"],
        ["催办"],
        ["反馈记录"],
        ["防重复提交"],
    ],
}


@dataclass(frozen=True)
class Finding:
    profile: str
    detail: str

    def __str__(self) -> str:
        return f"{self.profile}: {self.detail}"


def check_text(text: str, profiles: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for profile in profiles:
        anchor_groups = PROFILES[profile]
        for group in anchor_groups:
            if not any(anchor in text for anchor in group):
                findings.append(
                    Finding(profile, f"missing anchor group: {' / '.join(group)}")
                )
    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Run gold-slice-regression-check for {GOLD_SET_VERSION} anchors."
    )
    parser.add_argument("prd_file", type=Path)
    parser.add_argument(
        "--profile",
        action="append",
        choices=sorted(PROFILES),
        help="Profile to check. May be repeated. Defaults to all profiles.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    text = args.prd_file.read_text(encoding="utf-8")
    profiles = args.profile or sorted(PROFILES)
    findings = check_text(text, profiles)
    if findings:
        for finding in findings:
            print(finding, file=sys.stderr)
        return 1
    print(f"gold-slice-regression-check passed for {GOLD_SET_VERSION}: {args.prd_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
