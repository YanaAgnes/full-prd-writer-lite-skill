#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


MANIFEST_START = "<!-- ASSEMBLY-MANIFEST:START -->"
MANIFEST_END = "<!-- ASSEMBLY-MANIFEST:END -->"


PLACEHOLDER_HEADING_RE = re.compile(r"^#{1,6}\s+\d+(?:\.\d+)*\.x(?:\.|\s|$)", re.M)
CHAPTER_RE = re.compile(r"^#{1,2}\s+(10|[0-9])\.\s+(.+)$", re.M)
ANY_NUMBERED_CHAPTER_RE = re.compile(r"^#{1,2}\s+([0-9]+)\.\s+(.+)$", re.M)
TOP_LEVEL_CHAPTER_RE = re.compile(r"^#\s+(10|[0-9])\.\s+(.+)$", re.M)
BLOCK_MARKER_RE = re.compile(r"^<!-- PRD-BLOCK:[A-Za-z0-9._-]+ (?:START|END) -->$", re.M)
UNIT_HEADING_RE = re.compile(r"^##\s+(?:F|US|EXT|PEND)-[A-Za-z0-9_-]+", re.M)

EXPECTED_CHAPTER_TITLES = {
    "0": "修订记录",
    "1": "文档信息",
    "2": "系统概述",
    "3": "文档覆盖范围",
    "4": "用户角色与权限",
    "5": "业务流程",
    "6": "用户故事与使用路径",
    "7": "功能需求说明",
    "8": "外部系统协同需求说明",
    "9": "待确认事项",
    "10": "附录",
}

PROCESS_PATTERNS = [
    "候选正文块",
    "候选块",
    "章节分片",
    "哈希",
    "manifest",
    "ASSEMBLY",
    "写入 chapters",
    "本轮确认",
    "本轮不覆盖",
    "本轮不展开",
    "后续确认",
    "后续需求单元",
    "待写入",
    "源文档依据",
]

VAGUE_PATTERNS = [
    "支持相关操作",
    "按需展示",
    "进行优化",
    "提供管理能力",
    "异常时进行提示",
    "其他规则同上",
    "按功能权限配置",
    "按具体功能判断",
    "相关业务操作",
    "待补充",
    "TODO",
    "同上",
]


@dataclass(frozen=True)
class Finding:
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.kind}: {self.detail}"


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def body_without_block_markers(text: str) -> str:
    return BLOCK_MARKER_RE.sub("", text)


def check_block_markers(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in BLOCK_MARKER_RE.finditer(text):
        findings.append(
            Finding(
                "internal marker",
                f"line {line_number(text, match.start())}: final output exposes PRD-BLOCK marker",
            )
        )
    return findings


def check_required_chapters(text: str) -> list[Finding]:
    findings: list[Finding] = []
    chapters: dict[str, list[int]] = {}
    for match in CHAPTER_RE.finditer(text):
        chapter = match.group(1)
        title = match.group(2).strip()
        chapters.setdefault(chapter, []).append(line_number(text, match.start()))
        expected_title = EXPECTED_CHAPTER_TITLES[chapter]
        if title != expected_title:
            findings.append(
                Finding(
                    "chapter title",
                    f"line {line_number(text, match.start())}: chapter {chapter} title must be {expected_title}, got {title}",
                )
            )
    for match in ANY_NUMBERED_CHAPTER_RE.finditer(text):
        chapter_number = int(match.group(1))
        if chapter_number > 10:
            findings.append(
                Finding(
                    "extra chapter",
                    f"line {line_number(text, match.start())}: chapter {chapter_number} is outside 0-10",
                )
            )

    for chapter in [str(i) for i in range(10)]:
        if chapter not in chapters:
            findings.append(Finding("missing chapter", f"chapter {chapter} is absent"))
    for chapter, lines in chapters.items():
        if len(lines) > 1:
            findings.append(
                Finding("duplicate chapter", f"chapter {chapter} appears at lines {lines}")
            )
    return findings


def has_substantive_body(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        return True
    return False


def check_required_chapter_bodies(text: str) -> list[Finding]:
    findings: list[Finding] = []
    matches = list(CHAPTER_RE.finditer(text))
    chapter_spans: dict[str, tuple[int, int]] = {}
    for index, match in enumerate(matches):
        chapter = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chapter_spans.setdefault(chapter, (start, end))

    for chapter in [str(i) for i in range(10)]:
        if chapter not in chapter_spans:
            continue
        start, end = chapter_spans[chapter]
        if not has_substantive_body(text[start:end]):
            findings.append(Finding("empty chapter", f"chapter {chapter} has no body content"))

    if "10" in chapter_spans:
        start, end = chapter_spans["10"]
        if not has_substantive_body(text[start:end]):
            findings.append(Finding("empty chapter", "chapter 10 has no body content"))

    return findings


def check_placeholder_numbering(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in PLACEHOLDER_HEADING_RE.finditer(text):
        line = line_number(text, match.start())
        findings.append(
            Finding("placeholder numbering", f"line {line}: {match.group(0).strip()}")
        )
    return findings


def check_forbidden_terms(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for term in PROCESS_PATTERNS:
        index = text.find(term)
        if index != -1:
            findings.append(
                Finding("process wording", f"line {line_number(text, index)} contains {term}")
            )
    for term in VAGUE_PATTERNS:
        index = text.find(term)
        if index != -1:
            findings.append(
                Finding("vague substitute", f"line {line_number(text, index)} contains {term}")
            )
    return findings


def split_top_level_chapters(text: str) -> dict[str, str]:
    matches = list(TOP_LEVEL_CHAPTER_RE.finditer(text))
    chapters: dict[str, str] = {}
    for index, match in enumerate(matches):
        chapter = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chapters[chapter] = text[start:end]
    return chapters


def check_requirement_depth(text: str) -> list[Finding]:
    findings: list[Finding] = []
    chapters = split_top_level_chapters(text)
    chapter_6 = chapters.get("6", "")
    chapter_7 = chapters.get("7", "")
    chapter_8 = chapters.get("8", "")

    if "US-" not in chapter_6:
        findings.append(
            Finding("requirement depth", "chapter 6 must contain stable US- user story IDs")
        )
    if "F-" not in chapter_6:
        findings.append(
            Finding("requirement depth", "chapter 6 must reference related F- function IDs")
        )

    if "F-" not in chapter_7:
        findings.append(
            Finding("requirement depth", "chapter 7 must contain stable F- function IDs")
        )
    required_chapter_7_anchors = {
        "功能定位": ["功能定位", "所属功能域"],
        "入口与前置条件": ["入口", "前置条件"],
        "页面/字段": ["页面", "区域", "字段", "元素"],
        "功能与交互规则": ["功能与交互规则", "交互规则", "规则编号"],
        "异常与补偿": ["异常", "失败", "补偿"],
        "验收口径": ["验收", "AC-"],
    }
    for label, terms in required_chapter_7_anchors.items():
        if not any(term in chapter_7 for term in terms):
            findings.append(
                Finding("requirement depth", f"chapter 7 lacks {label} detail")
            )

    no_external = "无外部" in chapter_8 or "不涉及外部" in chapter_8
    if not no_external:
        if "EXT-" not in chapter_8:
            findings.append(
                Finding(
                    "requirement depth",
                    "chapter 8 must contain stable EXT- external collaboration IDs",
                )
            )
        for term in ["本系统职责", "外部系统职责"]:
            if term not in chapter_8:
                findings.append(
                    Finding("requirement depth", f"chapter 8 lacks {term}")
                )
    return findings


def check_presentation_structure(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in UNIT_HEADING_RE.finditer(text):
        findings.append(
            Finding(
                "presentation structure",
                f"line {line_number(text, match.start())}: second-level heading is a raw requirement-unit ID",
            )
        )

    chapters = split_top_level_chapters(text)
    chapter_6 = chapters.get("6", "")
    chapter_7 = chapters.get("7", "")
    chapter_8 = chapters.get("8", "")
    chapter_9 = chapters.get("9", "")

    if chapter_6 and "用户故事总览" not in chapter_6:
        findings.append(
            Finding("presentation structure", "chapter 6 must include 用户故事总览")
        )
    if chapter_7 and "功能结构总览" not in chapter_7:
        findings.append(
            Finding("presentation structure", "chapter 7 must include 功能结构总览")
        )
    collaboration_overview_terms = ["外部系统协同总览", "外部协同总览"]
    if (
        chapter_8
        and "EXT-" in chapter_8
        and not any(term in chapter_8 for term in collaboration_overview_terms)
    ):
        findings.append(
            Finding("presentation structure", "chapter 8 must include 外部系统协同总览")
        )
    if "PEND-" in chapter_9:
        pending_header_groups = {
            "待确认编号": ["待确认编号", "编号"],
            "关联需求": ["关联需求", "归属需求单元", "相关需求单元"],
            "当前基线处理": ["当前基线处理", "当前基线结论", "当前处理"],
            "阻断性说明": ["是否阻断", "不影响当前基线的原因", "不影响当前基线原因"],
            "后续处理条件": ["后续处理条件", "建议处理"],
        }
        for label, aliases in pending_header_groups.items():
            if not any(alias in chapter_9 for alias in aliases):
                findings.append(
                    Finding(
                        "presentation structure",
                        f"chapter 9 pending table lacks {label}",
                    )
                )
    return findings


def parse_manifest_rows(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    if MANIFEST_START not in text or MANIFEST_END not in text:
        raise ValueError("manifest markers are missing")
    body = text.split(MANIFEST_START, 1)[1].split(MANIFEST_END, 1)[0]
    rows = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return []
    header = [cell.strip() for cell in rows[0].strip("|").split("|")]
    parsed: list[dict[str, str]] = []
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) == len(header):
            parsed.append(dict(zip(header, cells)))
    return parsed


def check_manifest(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        rows = parse_manifest_rows(path)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return [Finding("manifest", str(exc))]

    for index, row in enumerate(rows, start=1):
        source = row.get("source_file", "")
        unit = row.get("requirement_unit", "")
        block_id = row.get("block_id", f"row {index}")
        if source == "chapters/scaffold.md" or source.endswith("/scaffold.md"):
            findings.append(Finding("scaffold source", f"{block_id} uses {source}"))
        if unit == "ALL-FUNCTIONS":
            findings.append(Finding("ALL-FUNCTIONS", f"{block_id} uses ALL-FUNCTIONS"))
    return findings


def validate(final_path: Path, manifest_path: Path | None) -> list[Finding]:
    text = final_path.read_text(encoding="utf-8")
    body = body_without_block_markers(text)
    findings: list[Finding] = []
    findings.extend(check_block_markers(text))
    findings.extend(check_required_chapters(body))
    findings.extend(check_required_chapter_bodies(body))
    findings.extend(check_placeholder_numbering(body))
    findings.extend(check_forbidden_terms(body))
    findings.extend(check_requirement_depth(body))
    findings.extend(check_presentation_structure(body))
    if manifest_path is not None:
        findings.extend(check_manifest(manifest_path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    try:
        findings = validate(args.final, args.manifest)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"QUALITY_FAILED: {exc}", file=sys.stderr)
        return 1

    if findings:
        print(f"QUALITY_FAILED: {len(findings)} finding(s)", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1

    print("QUALITY_PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
