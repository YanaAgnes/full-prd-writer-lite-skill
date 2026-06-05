#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

MANIFEST_START = "<!-- ASSEMBLY-MANIFEST:START -->"
MANIFEST_END = "<!-- ASSEMBLY-MANIFEST:END -->"
ALLOWED_STATES = {"已冻结", "基线继承"}
BLOCK_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
BLOCK_SCAN_RE = re.compile(r"<!-- PRD-BLOCK:([A-Za-z0-9._-]+) START -->")


class AssemblyError(RuntimeError):
    pass


@dataclass(frozen=True)
class Entry:
    block_id: str
    requirement_unit: str
    source_file: str
    state: str
    order: int
    sha256: str
    final_location: str


def parse_manifest(path: Path) -> list[Entry]:
    text = path.read_text(encoding="utf-8")
    if MANIFEST_START not in text or MANIFEST_END not in text:
        raise AssemblyError("manifest markers are missing")
    body = text.split(MANIFEST_START, 1)[1].split(MANIFEST_END, 1)[0]
    rows = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        raise AssemblyError("manifest table has no data rows")

    header = [cell.strip() for cell in rows[0].strip("|").split("|")]
    expected = [
        "block_id",
        "requirement_unit",
        "source_file",
        "state",
        "order",
        "sha256",
        "final_location",
    ]
    if header != expected:
        raise AssemblyError(f"manifest header must be: {expected}")

    entries: list[Entry] = []
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) != len(expected):
            raise AssemblyError(f"invalid manifest row: {row}")
        block_id, unit, source, state, order, digest_value, location = cells
        if not BLOCK_ID_RE.fullmatch(block_id):
            raise AssemblyError(f"invalid block id: {block_id}")
        if state not in ALLOWED_STATES:
            raise AssemblyError(f"block {block_id} has illegal state: {state}")
        if not re.fullmatch(r"[0-9a-f]{64}", digest_value):
            raise AssemblyError(f"block {block_id} has invalid sha256")
        entries.append(
            Entry(
                block_id,
                unit,
                source,
                state,
                int(order),
                digest_value,
                location,
            )
        )

    ids = [entry.block_id for entry in entries]
    orders = [entry.order for entry in entries]
    if len(ids) != len(set(ids)):
        raise AssemblyError("manifest contains duplicate block IDs")
    if len(orders) != len(set(orders)):
        raise AssemblyError("manifest contains duplicate order values")
    return sorted(entries, key=lambda entry: entry.order)


def source_path(workspace: Path, relative: str) -> Path:
    candidate = (workspace / relative).resolve()
    chapters = (workspace / "chapters").resolve()
    if chapters != candidate and chapters not in candidate.parents:
        raise AssemblyError(f"source is outside chapters/: {relative}")
    if not candidate.is_file():
        raise AssemblyError(f"source file does not exist: {relative}")
    return candidate


def extract_block(text: str, block_id: str) -> tuple[str, str]:
    start = f"<!-- PRD-BLOCK:{block_id} START -->"
    end = f"<!-- PRD-BLOCK:{block_id} END -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise AssemblyError(f"block {block_id} must have exactly one start and end")
    before, remainder = text.split(start, 1)
    content, after = remainder.split(end, 1)
    if end in before or start in after:
        raise AssemblyError(f"block {block_id} markers are malformed")
    if content.startswith("\n"):
        content = content[1:]
    if content.endswith("\n"):
        content = content[:-1]
    complete = f"{start}\n{content}\n{end}"
    return content, complete


def digest(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def expected_blocks(workspace: Path, entries: list[Entry]) -> list[str]:
    blocks: list[str] = []
    for entry in entries:
        text = source_path(workspace, entry.source_file).read_text(encoding="utf-8")
        content, complete = extract_block(text, entry.block_id)
        actual = digest(content)
        if actual != entry.sha256:
            raise AssemblyError(
                f"hash mismatch for {entry.block_id}: "
                f"expected {entry.sha256}, got {actual}"
            )
        blocks.append(complete)
    return blocks


def verify_final(text: str, entries: list[Entry]) -> None:
    registered = [entry.block_id for entry in entries]
    scanned = BLOCK_SCAN_RE.findall(text)
    if scanned != registered:
        raise AssemblyError(
            f"final block order/content mismatch: expected {registered}, got {scanned}"
        )
    if len(scanned) != len(set(scanned)):
        raise AssemblyError("final document contains duplicate blocks")
    remaining = text
    for entry in entries:
        content, complete = extract_block(text, entry.block_id)
        if digest(content) != entry.sha256:
            raise AssemblyError(f"final hash mismatch for {entry.block_id}")
        remaining = remaining.replace(complete, "", 1)
    if remaining.strip():
        raise AssemblyError("final document contains unregistered body text")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-existing", action="store_true")
    args = parser.parse_args()

    try:
        workspace = args.workspace.resolve()
        entries = parse_manifest(args.manifest.resolve())
        if args.check_existing:
            verify_final(args.output.read_text(encoding="utf-8"), entries)
        else:
            blocks = expected_blocks(workspace, entries)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
            verify_final(args.output.read_text(encoding="utf-8"), entries)
    except (AssemblyError, OSError, ValueError) as exc:
        print(f"ASSEMBLY_FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"ASSEMBLY_PASSED: {len(entries)} blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
