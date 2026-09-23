#!/usr/bin/env python3
"""Lightweight structural validator for project Design System documents."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_CONCEPTS = {
    "authority": (r"(?im)^##\s+.*authority", r"(?im)^##\s+.*scope"),
    "foundations": (r"(?im)^##\s+.*foundation", r"(?im)^##\s+.*token"),
    "responsive": (r"(?im)^##\s+.*responsive", r"(?im)^##\s+.*layout"),
    "components": (r"(?im)^##\s+.*component",),
    "interaction": (r"(?im)^##\s+.*interaction",),
    "reuse": (r"(?im)^##\s+.*reuse", r"(?im)^##\s+.*ownership"),
    "accessibility": (r"(?im)^##\s+.*accessib",),
    "governance": (r"(?im)^##\s+.*governance", r"(?im)^##\s+.*change process"),
}

PLACEHOLDER_PATTERNS = (
    r"\{\{[^}]+\}\}",
    r"<PROJECT(?:_|\b)",
    r"<DESIGN(?:_|\b)",
)


def has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_design_system.py <path-to-DESIGN_SYSTEM.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    if not re.search(r"(?im)^#\s+.+design system\s*$", text):
        errors.append("Missing top-level '# … Design System' heading.")

    for concept, patterns in REQUIRED_CONCEPTS.items():
        if not has_any(text, patterns):
            errors.append(f"Missing required design-system concept/section: {concept}.")

    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, text)
        if match:
            errors.append(f"Unresolved template placeholder: {match.group(0)}")

    if "PRD" not in text:
        warnings.append("Document does not mention PRD/source-of-truth separation.")

    if not re.search(r"(?i)(canonical|source of truth)", text):
        warnings.append("Document does not clearly identify canonical ownership/source of truth.")

    headings = re.findall(r"(?m)^#{2,4}\s+(.+?)\s*$", text)
    normalized: dict[str, int] = {}
    for heading in headings:
        key = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", heading).strip().lower()
        normalized[key] = normalized.get(key, 0) + 1
    duplicates = sorted(key for key, count in normalized.items() if count > 1)
    if duplicates:
        warnings.append("Repeated section headings: " + ", ".join(duplicates))

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print("Design System validator: FAILED")
        return 1

    print("Design System validator: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
