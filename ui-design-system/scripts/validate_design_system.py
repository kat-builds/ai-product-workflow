#!/usr/bin/env python3
"""Lightweight structural validator for project Design System documents."""

from __future__ import annotations

import json
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

LOCALE_DIR = Path(__file__).resolve().parents[1] / "locales"


def load_locale_strings() -> dict[str, dict[str, str]]:
    locales: dict[str, dict[str, str]] = {}
    if not LOCALE_DIR.is_dir():
        return locales

    for locale_path in sorted(LOCALE_DIR.glob("*.json")):
        try:
            payload = json.loads(locale_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        strings = payload.get("strings")
        code = payload.get("code") or locale_path.stem
        if isinstance(strings, dict) and all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in strings.items()
        ):
            locales[str(code)] = strings

    return locales


LOCALE_STRINGS = load_locale_strings()
CANONICAL_LOCALE = LOCALE_STRINGS.get("en", {})


def normalize_localized_structure(text: str) -> str:
    """Normalize supported locale section headings to the English canonical form."""
    if not CANONICAL_LOCALE:
        return text

    for key, canonical in CANONICAL_LOCALE.items():
        if not key.startswith("section."):
            continue

        number = key.split(".", 1)[1]
        aliases = {
            strings.get(key)
            for strings in LOCALE_STRINGS.values()
            if strings.get(key)
        }
        aliases.discard(canonical)

        for alias in aliases:
            text = re.sub(
                rf"(?m)^##\s+{re.escape(number)}\.\s+{re.escape(alias)}\s*$",
                f"## {number}. {canonical}",
                text,
            )

    return text


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

    text = normalize_localized_structure(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if not re.search(r"(?im)^#\s+.+(?:design system|设计系统)\s*$", text):
        errors.append("Missing top-level Design System heading.")

    for concept, patterns in REQUIRED_CONCEPTS.items():
        if not has_any(text, patterns):
            errors.append(f"Missing required design-system concept/section: {concept}.")

    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, text)
        if match:
            errors.append(f"Unresolved template placeholder: {match.group(0)}")

    if "PRD" not in text:
        warnings.append("Document does not mention PRD/source-of-truth separation.")

    if not re.search(r"(?i)(canonical|source of truth|权威|事实来源)", text):
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
