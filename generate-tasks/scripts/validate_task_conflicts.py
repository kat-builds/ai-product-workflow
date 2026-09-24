#!/usr/bin/env python3
"""Validate conflict metadata in generated task-prompt.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TASK_HEADING = re.compile(r"^## Task (\d+\.0) — .+$", re.M)
CONFLICT_FIELD = re.compile(r"^- (?:冲突|Conflicts)\s*[:：][ \t]*(.+?)\s*$", re.M | re.I)
TASK_ID = re.compile(r"\d+\.0")


def task_blocks(text: str) -> dict[str, str]:
    matches = list(TASK_HEADING.finditer(text))
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        task_id = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[task_id] = text[match.start():end]
    return blocks


def parse_conflicts(value: str) -> tuple[list[str], str | None]:
    value = value.strip().strip("`").strip()
    if value.casefold() == "none" or value == "无":
        return [], None
    if not value:
        return [], "must be None/无 or a list of Task IDs"
    tokens = [
        token.strip()
        for token in re.split(r"\s*(?:、|,)\s*", value)
        if token.strip()
    ]
    if any(not TASK_ID.fullmatch(token) for token in tokens):
        return [], "must contain only Task IDs separated by commas or 、"
    if len(tokens) != len(set(tokens)):
        return [], "must not repeat Task IDs"
    return tokens, None


def validate(text: str) -> list[str]:
    errors: list[str] = []
    blocks = task_blocks(text)
    conflicts: dict[str, list[str]] = {}

    for task_id, block in blocks.items():
        fields = CONFLICT_FIELD.findall(block)
        if len(fields) != 1:
            errors.append(
                f"Task {task_id} must contain exactly one Conflicts/冲突 metadata line."
            )
            continue

        refs, error = parse_conflicts(fields[0])
        if error:
            errors.append(f"Task {task_id} conflict display {error}.")
            continue
        if task_id in refs:
            errors.append(f"Task {task_id} must not conflict with itself.")
        unknown = [ref for ref in refs if ref not in blocks]
        if unknown:
            errors.append(
                f"Task {task_id} conflict display references non-current Task IDs: "
                + "、".join(unknown)
                + "."
            )
        conflicts[task_id] = refs

    for task_id, refs in conflicts.items():
        for ref in refs:
            if ref not in conflicts:
                continue
            if task_id not in conflicts[ref]:
                errors.append(
                    f"Conflict must be symmetric: Task {task_id} lists {ref}, "
                    f"but Task {ref} does not list {task_id}."
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate conflict metadata in docs/project/task-prompt.md."
    )
    parser.add_argument("task_prompt", type=Path)
    args = parser.parse_args()

    text = args.task_prompt.read_text(encoding="utf-8")
    errors = validate(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Task conflict validator: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
