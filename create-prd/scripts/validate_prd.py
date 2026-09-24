#!/usr/bin/env python3
"""Validate the canonical product PRD using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = [
    (1, "Introduction & Goals"),
    (2, "Domain, Audience & SEO"),
    (3, "Project Type & Scope"),
    (4, "User Scenarios"),
    (5, "Page Structure"),
    (6, "Interaction Flows"),
    (7, "Functional Requirements"),
    (8, "API, Data, Auth, Storage & Payment"),
    (9, "Mobile & Responsive"),
    (10, "Error States, Security & Privacy"),
    (11, "UI Copy & Localization"),
    (12, "Design & Technical Constraints"),
    (13, "Non-Goals"),
    (14, "Open Questions"),
]
REQUIRED_SCOPE_SUBSECTIONS = [
    "Project Type",
    "Current Scope",
    "Existing Baseline",
    "Confirmed Next Phase",
    "Possible Later",
    "Explicitly Overridden",
    "Infrastructure Decisions",
]

ROLE_NOTE_RE = re.compile(r"(?:文档角色|document role)", re.I)
LANG_NOTE_RE = re.compile(r"(?:语言说明|language)", re.I)

ID_PREFIX = r"(?:PAGE|FLOW|FR|DATA|API|PAY|COPY|ERR|NFR)"
ID_RE = re.compile(rf"\b{ID_PREFIX}-\d{{3}}\b")
MALFORMED_ID_RE = re.compile(rf"\b{ID_PREFIX}-(\d+)\b")
DEFINITION_START_RE = re.compile(
    rf"^(?:#{{3,6}}\s+|[-*]\s+|\d+[.)]\s+|\|\s*)"
    rf"[*_\x60]*({ID_PREFIX}-\d{{3}})[\x60*_]*(?=\s|[—–:：|])"
)
MAIN_HEADING_RE = re.compile(
    r"(?m)^##[ \t]+(?P<number>\d+)\.[ \t]+(?P<title>.*\S)[ \t]*$"
)

SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}\b")),
    ("OpenAI-style key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}\b")),
    ("live/test credential", re.compile(r"\b(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]{12,}\b", re.I)),
    ("webhook secret", re.compile(r"\bwhsec_[A-Za-z0-9]{12,}\b", re.I)),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", re.I)),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b", re.I)),
    ("Resend-style key", re.compile(r"\bre_[A-Za-z0-9_-]{20,}\b")),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{20,}=*", re.I)),
    (
        "credential-bearing database URL",
        re.compile(r"(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s:@/]+:[^\s@/]+@", re.I),
    ),
    (
        "credential-bearing URL",
        re.compile(r"https?://[^\s/:@]+:[^\s/@]+@[^\s]+", re.I),
    ),
]
GENERIC_CREDENTIAL_RE = re.compile(
    r"(?i)\b(?:api[_ -]?key|secret|token|password|passwd|client[_ -]?secret|"
    r"private[_ -]?key|access[_ -]?key)\b\s*[:=：]\s*[\x60\"']?"
    r"(?P<value>[A-Za-z0-9._~+/\-=]{12,})"
)
QUERY_CREDENTIAL_RE = re.compile(
    r"(?i)[?&](?:api[_-]?key|access[_-]?token|token|secret|password)="
    r"(?P<value>[A-Za-z0-9._~+/\-=]{12,})"
)
MOJIBAKE = ("ï»¿", "â€™", "â€œ", "â€", "Ã", "�")
ACTIVE_INFRA_DECISIONS = {"reuse", "configure", "extend"}
ALL_INFRA_DECISIONS = ACTIVE_INFRA_DECISIONS | {
    "defer",
    "not required",
    "blocked",
}
CORE_INFRA_CAPABILITIES = {"database", "auth", "storage", "payment"}

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
    """Normalize supported locale labels to the canonical English structure."""
    if not CANONICAL_LOCALE:
        return text

    # Backward compatibility for the previous canonical English heading.
    text = re.sub(
        r"(?m)^##[ \t]+11\.[ \t]+UI Copy & i18n[ \t]*$",
        "## 11. UI Copy & Localization",
        text,
    )

    for key, canonical in CANONICAL_LOCALE.items():
        aliases = {
            strings.get(key)
            for strings in LOCALE_STRINGS.values()
            if strings.get(key)
        }
        aliases.discard(canonical)

        for alias in sorted(aliases, key=len, reverse=True):
            escaped = re.escape(alias)

            if key.startswith("section."):
                number = key.split(".", 1)[1]
                text = re.sub(
                    rf"(?m)^##[ \t]+{re.escape(number)}\.[ \t]+{escaped}[ \t]*$",
                    f"## {number}. {canonical}",
                    text,
                )
            elif key.startswith("scope."):
                text = re.sub(
                    rf"(?m)^###[ \t]+{escaped}[ \t]*$",
                    f"### {canonical}",
                    text,
                )
            elif key == "heading.mobile_acceptance":
                text = re.sub(
                    rf"(?m)^###[ \t]+{escaped}[ \t]*$",
                    f"### {canonical}",
                    text,
                )
            elif key.startswith("field."):
                text = re.sub(
                    rf"(?m)^(\s*[-*]\s*){escaped}\s*[:：]",
                    rf"\1{canonical}:",
                    text,
                )

    return text


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


def section_body(text: str, number: int, title: str) -> str:
    pattern = re.compile(
        rf"(?ms)^##[ \t]+{number}\.[ \t]+{re.escape(title)}[ \t]*\n"
        rf"(.*?)(?=^##[ \t]+|\Z)"
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def subsection_body(text: str, title: str) -> str:
    pattern = re.compile(
        rf"(?ms)^###[ \t]+{re.escape(title)}[ \t]*\n"
        rf"(.*?)(?=^###[ \t]+|^##[ \t]+|\Z)"
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def is_none_statement(body: str) -> bool:
    compact = re.sub(r"[\s。.;；\x60*_>-]", "", body).lower()
    return compact in {"无", "none", "noopenquestions"}


def looks_like_placeholder_secret(value: str) -> bool:
    normalized = value.strip().strip("\"'\x60")
    lowered = normalized.lower()
    if re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", normalized):
        return True
    if any(
        token in lowered
        for token in (
            "placeholder",
            "example",
            "redacted",
            "replace",
            "your_",
            "your-",
            "changeme",
            "dummy",
            "sample",
        )
    ):
        return True
    if re.fullmatch(r"(?:x+|\*+|0+)", lowered):
        return True
    return False


def definition_lines(text: str) -> dict[str, list[int]]:
    definitions: dict[str, list[int]] = {}
    current_section: int | None = None

    for lineno, line in enumerate(text.splitlines(), start=1):
        main = re.match(r"^##[ \t]+(\d+)\.", line)
        if main:
            current_section = int(main.group(1))

        match = DEFINITION_START_RE.match(line.strip())
        if not match:
            continue

        # Section 3 is the classification/index. IDs there are cross-references,
        # not full definitions.
        if current_section == 3:
            continue

        token = match.group(1)
        definitions.setdefault(token, []).append(lineno)

    return definitions


def count_mobile_acceptance_items(body: str) -> tuple[bool, int]:
    marker = re.search(
        r"(?im)^###[ \t]+.*(?:Mobile acceptance|移动端验收).*$",
        body,
    )
    if not marker:
        return False, 0

    target = body[marker.end() :]
    next_heading = re.search(r"(?m)^###[ \t]+", target)
    if next_heading:
        target = target[: next_heading.start()]

    numbered = re.findall(r"(?m)^\s*\d+[.)]\s+\S", target)
    bullets = re.findall(r"(?m)^\s*[-*]\s+\S", target)
    return True, max(len(numbered), len(bullets))


def validate_main_sections(text: str, findings: list[Finding]) -> dict[int, str]:
    expected = {number: title for number, title in REQUIRED_SECTIONS}
    found: dict[tuple[int, str], list[int]] = {}

    for match in re.finditer(r"(?m)^##(?!#)[^\n]*$", text):
        parsed = MAIN_HEADING_RE.fullmatch(match.group(0))
        lineno = line_number(text, match.start())
        if not parsed:
            findings.append(
                Finding(
                    "ERROR",
                    f"Main section heading at line {lineno} must use '## N. Exact Title'.",
                )
            )
            continue

        number = int(parsed.group("number"))
        title = parsed.group("title").strip()
        found.setdefault((number, title), []).append(lineno)
        if expected.get(number) != title:
            findings.append(
                Finding(
                    "ERROR",
                    f"Unexpected main section at line {lineno}: {number}. {title}",
                )
            )

    positions: list[int] = []
    bodies: dict[int, str] = {}
    for number, title in REQUIRED_SECTIONS:
        lines = found.get((number, title), [])
        if not lines:
            findings.append(Finding("ERROR", f"Missing required section: {number}. {title}"))
            continue
        if len(lines) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    f"Required section {number}. {title} appears multiple times at lines {lines}.",
                )
            )
            continue
        positions.append(lines[0])
        bodies[number] = section_body(text, number, title)

    if len(positions) == len(REQUIRED_SECTIONS) and positions != sorted(positions):
        findings.append(Finding("ERROR", "The 14 main PRD sections are not in the required order."))

    return bodies


def validate_scope(
    scope_body: str,
    current_ids: set[str],
    findings: list[Finding],
) -> None:
    positions: list[int] = []
    for title in REQUIRED_SCOPE_SUBSECTIONS:
        matches = list(re.finditer(rf"(?m)^###[ \t]+{re.escape(title)}[ \t]*$", scope_body))
        if not matches:
            findings.append(Finding("ERROR", f"Project Type & Scope is missing subsection: {title}"))
            continue
        if len(matches) > 1:
            findings.append(
                Finding("ERROR", f"Project Type & Scope repeats subsection: {title}")
            )
            continue
        positions.append(matches[0].start())

    if len(positions) == len(REQUIRED_SCOPE_SUBSECTIONS) and positions != sorted(positions):
        findings.append(
            Finding("ERROR", "Project Type & Scope subsections are not in the required order.")
        )

    if not current_ids:
        findings.append(Finding("ERROR", "Current Scope must contain at least one stable PRD ID."))

    infra_body = subsection_body(scope_body, "Infrastructure Decisions")
    table_rows: list[list[str]] = []
    for line in infra_body.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0].lower() == "capability" or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        table_rows.append(cells)

    if not table_rows:
        findings.append(
            Finding("ERROR", "Infrastructure Decisions must contain a capability decision table.")
        )
        return

    seen_capabilities: set[str] = set()
    for cells in table_rows:
        capability = cells[0].strip()
        decision = cells[1].strip().lower()
        basis = cells[2].strip()
        capability_key = capability.lower()
        seen_capabilities.add(capability_key)

        if decision not in ALL_INFRA_DECISIONS:
            findings.append(
                Finding(
                    "ERROR",
                    f"Infrastructure decision for {capability!r} is not an allowed value.",
                )
            )
            continue

        basis_ids = set(ID_RE.findall(basis))
        if decision in ACTIVE_INFRA_DECISIONS:
            if not basis_ids:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Active infrastructure decision for {capability!r} must cite Current Scope IDs.",
                    )
                )
            elif not basis_ids.issubset(current_ids):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Infrastructure decision for {capability!r} cites IDs outside Current Scope.",
                    )
                )
            if re.search(
                r"Existing Baseline|Confirmed Next Phase|Possible Later|template|reference|playbook|module doc",
                basis,
                re.I,
            ):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Active infrastructure decision for {capability!r} uses a non-current scope source.",
                    )
                )
        elif not basis_ids and not re.search(r"No Current Scope trigger", basis, re.I):
            findings.append(
                Finding(
                    "ERROR",
                    f"Inactive infrastructure decision for {capability!r} must cite Current Scope IDs or state 'No Current Scope trigger'.",
                )
            )

    missing_core = CORE_INFRA_CAPABILITIES - seen_capabilities
    for capability in sorted(missing_core):
        findings.append(
            Finding(
                "ERROR",
                f"Infrastructure Decisions is missing core capability: {capability.title()}",
            )
        )


def validate_implementation_content(text: str, findings: list[Finding]) -> None:
    checks = [
        (
            r"(?m)^\s*[-*]\s*\[[ xX]\]",
            "PRD contains task checkboxes; implementation tasks belong outside the PRD.",
        ),
        (
            r"\bTASK-\d+\b",
            "PRD contains TASK IDs; task generation is outside this skill.",
        ),
        (
            r"(?i)Execution Prompt|执行[ \t]*Prompt|父任务包|Task Package|docs/project/tasks\.md",
            "PRD contains task-generation or execution-prompt content.",
        ),
        (
            r"(?im)^#{2,6}\s+(?:\d+\.\s*)?(?:Implementation|Execution|Delivery|Rollout)[ \t]+(?:Plan|Tasks|Steps|Checklist)\b|"
            r"^#{2,6}\s+(?:\d+\.\s*)?(?:实现任务|实现计划|实施步骤|执行计划|任务清单|交付计划|修改文件)",
            "PRD contains an implementation/task-plan section.",
        ),
        (
            r"(?i)\bgit[ \t]+commit\b|commit[ \t]+message|Conventional Commit|提交代码|创建提交|提交信息",
            "PRD contains a commit instruction.",
        ),
        (
            r"(?i)\bFiles?[ \t]+to[ \t]+(?:change|modify|create|delete)\b|修改文件(?:清单)?|文件改动清单",
            "PRD contains a file-change list.",
        ),
        (
            r"(?im)^\s*(?:[-*]|\d+[.)])\s+"
            r"(?:实现|修改|创建|新增|删除|重构|编写|安装|运行|执行|迁移|部署)"
            r"(?:代码|组件|文件|脚本|测试|数据库|依赖|构建|应用|服务|到|[ \t])|"
            r"^\s*(?:[-*]|\d+[.)])\s+"
            r"(?:add|edit|create|delete|refactor|implement|write|install|run|execute|migrate|deploy)"
            r"\b",
            "PRD contains an imperative implementation work item.",
        ),
        (
            r"(?im)(?:^|[\x60$])[ \t]*(?:pnpm|npm|yarn|bun|git|docker|wrangler|npx|pytest|python3?|cargo|go)[ \t]+[A-Za-z0-9:_-]+",
            "PRD appears to contain an implementation command.",
        ),
        (
            r"(?m)^\s*(?:[-*]|\d+[.)])\s+(?:修改|创建|删除|重构|新增|编辑|安装|运行|执行|迁移|部署)"
            r".*(?:\b(?:src|app|components|scripts|tests|public|config)/[^\s\x60]+|"
            r"\b[\w.-]+\.(?:tsx?|jsx?|py|sql|ya?ml|json|css|scss)\b)",
            "PRD contains a file-level implementation instruction.",
        ),
        (
            r"(?im)^\s*(?:[-*]|\d+[.)])\s+(?:edit|create|delete|refactor|implement|install|run|execute|migrate|deploy)"
            r"\b.*(?:\b(?:src|app|components|scripts|tests|public|config)/[^\s\x60]+|"
            r"\b[\w.-]+\.(?:tsx?|jsx?|py|sql|ya?ml|json|css|scss)\b)",
            "PRD contains a file-level implementation instruction.",
        ),
    ]

    for pattern, message in checks:
        if re.search(pattern, text):
            findings.append(Finding("ERROR", message))

    if re.search(r"\x60{3}", text):
        findings.append(
            Finding("ERROR", "PRD contains a fenced code block; code and command blocks are out of scope.")
        )


def validate_secrets(text: str, findings: list[Finding]) -> None:
    detected_labels: set[str] = set()

    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            detected_labels.add(label)

    for pattern, label in (
        (GENERIC_CREDENTIAL_RE, "assigned credential value"),
        (QUERY_CREDENTIAL_RE, "credential value in URL query"),
    ):
        for match in pattern.finditer(text):
            if not looks_like_placeholder_secret(match.group("value")):
                detected_labels.add(label)
                break

    for label in sorted(detected_labels):
        findings.append(
            Finding(
                "ERROR",
                f"Possible {label} detected; secret values are not allowed and were not echoed.",
            )
        )


def validate_reference_paths(path: Path, text: str, findings: list[Finding]) -> None:
    normalized = path.resolve()
    suffix = Path("docs/project/PRD.md")
    if normalized.parts[-len(suffix.parts) :] != suffix.parts:
        findings.append(Finding("WARNING", "Expected output path is docs/project/PRD.md."))
        return

    repo_root = normalized.parents[2]
    cited_paths = sorted(set(re.findall(r"(?<![\w/])docs/[A-Za-z0-9_./-]+\.md\b", text)))
    for cited in cited_paths:
        if not (repo_root / cited).is_file():
            findings.append(
                Finding("ERROR", f"Cited project document does not exist: {cited}")
            )


def validate(path: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not path.exists():
        return [Finding("ERROR", f"File does not exist: {path}")]
    if not path.is_file():
        return [Finding("ERROR", f"Path is not a file: {path}")]

    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        findings.append(Finding("ERROR", "File contains a UTF-8 BOM."))

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return [Finding("ERROR", f"File is not valid UTF-8: {exc}")]

    text = normalize_localized_structure(text)

    for token in MOJIBAKE:
        if token in text:
            findings.append(Finding("ERROR", f"Possible mojibake detected: {token!r}"))

    validate_reference_paths(path, text, findings)

    h1_matches = list(re.finditer(r"(?m)^#(?!#)\s+\S.*$", text))
    if len(h1_matches) != 1:
        findings.append(
            Finding("ERROR", f"Expected exactly one H1 title; found {len(h1_matches)}.")
        )
    else:
        after_title = text[h1_matches[0].end() :].splitlines()
        first_nonempty = [line.strip() for line in after_title if line.strip()][:2]
        if (
            len(first_nonempty) < 1
            or not first_nonempty[0].startswith(">")
            or not ROLE_NOTE_RE.search(first_nonempty[0])
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "A document-role note must appear immediately below the title.",
                )
            )
        if (
            len(first_nonempty) < 2
            or not first_nonempty[1].startswith(">")
            or not LANG_NOTE_RE.search(first_nonempty[1])
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "A language/localization note must appear immediately below the role note.",
                )
            )

    bodies = validate_main_sections(text, findings)
    scope_body = bodies.get(3, "")
    current_scope_body = subsection_body(scope_body, "Current Scope")
    current_ids = set(ID_RE.findall(current_scope_body))
    validate_scope(scope_body, current_ids, findings)

    definitions = definition_lines(text)
    for token, lines in sorted(definitions.items()):
        if len(lines) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    f"ID {token} is defined multiple times at lines {lines}.",
                )
            )

    for match in MALFORMED_ID_RE.finditer(text):
        digits = match.group(1)
        if len(digits) != 3:
            findings.append(
                Finding(
                    "ERROR",
                    f"Malformed stable ID at line {line_number(text, match.start())}; use exactly three digits.",
                )
            )

    all_ids = set(ID_RE.findall(text))
    overridden_ids = set(
        ID_RE.findall(subsection_body(scope_body, "Explicitly Overridden"))
    )
    for token in sorted(all_ids):
        if token not in definitions and token not in overridden_ids:
            findings.append(Finding("ERROR", f"ID {token} is referenced but never defined."))

    for token in sorted(current_ids):
        if token not in definitions:
            findings.append(
                Finding("ERROR", f"Current Scope ID {token} lacks one formal definition.")
            )

    flow_body = bodies.get(6, "")
    flow_definitions = {
        match.group(1)
        for line in flow_body.splitlines()
        if (match := DEFINITION_START_RE.match(line.strip()))
        and match.group(1).startswith("FLOW-")
    }
    if not flow_definitions:
        findings.append(Finding("ERROR", "Interaction Flows must define at least one FLOW-xxx ID."))

    nong_body = bodies.get(13, "")
    nong_bullets = re.findall(r"(?m)^\s*[-*]\s+(.+\S)\s*$", nong_body)
    if not nong_bullets:
        findings.append(Finding("ERROR", "Non-Goals must contain at least one explicit exclusion."))
    else:
        for item in nong_bullets:
            if not re.search(r"原因|理由|because|reason|out of scope", item, re.I):
                findings.append(
                    Finding("ERROR", "Every Non-Goal must state an exclusion reason.")
                )
                break

    mobile_body = bodies.get(9, "")
    mobile_not_applicable = bool(
        re.search(r"\b(?:N/?A|Not applicable)\b|不适用", mobile_body, re.I)
    )
    if not mobile_not_applicable:
        if not re.search(
            r"页面级.{0,12}(?:不得|无).{0,8}横向滚动|no page-level horizontal",
            mobile_body,
            re.I,
        ):
            findings.append(
                Finding("ERROR", "Mobile section must prohibit page-level horizontal scrolling.")
            )
        has_mobile_acceptance, mobile_items = count_mobile_acceptance_items(mobile_body)
        if not has_mobile_acceptance:
            findings.append(
                Finding("ERROR", "Mobile section is missing a Mobile acceptance subsection.")
            )
        elif mobile_items < 3:
            findings.append(
                Finding(
                    "ERROR",
                    f"Mobile section needs at least 3 testable acceptance items; found {mobile_items}.",
                )
            )

    open_body = bodies.get(14, "")
    if not open_body.strip():
        findings.append(
            Finding(
                "ERROR",
                "Open Questions is empty; write genuine questions or explicitly state none.",
            )
        )
    elif not is_none_statement(open_body):
        question_blocks = list(
            re.finditer(
                r"(?ms)^###[ \t]+OQ-\d{3}\b.*?\n(.*?)(?=^###[ \t]+|\Z)",
                open_body,
            )
        )
        if not question_blocks:
            findings.append(
                Finding(
                    "ERROR",
                    "Open Questions must use OQ-xxx entries or explicitly state none.",
                )
            )
        for block in question_blocks:
            content = block.group(1)
            for field in (
                "Question",
                "Impact area",
                "Options",
                "Recommended",
                "Reason",
                "Blocking",
                "Current implementation impact",
                "Owner",
                "Needed by",
                "Temporary assumption",
            ):
                if not re.search(rf"(?im)^\s*[-*]\s*{re.escape(field)}\s*[:：]", content):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Open Question entry is missing field: {field}",
                        )
                    )

            options_match = re.search(
                r"(?ims)^\s*[-*]\s*Options\s*[:：]\s*$"
                r"(?P<body>.*?)(?=^\s*[-*]\s*(?:Recommended|Reason|Blocking|Current implementation impact|Owner|Needed by|Temporary assumption)\s*[:：])",
                content,
            )
            if options_match:
                option_labels = re.findall(
                    r"(?im)^\s*[-*]\s*([A-D])\s*[:：]\s*(\S.*)$",
                    options_match.group("body"),
                )
                labels = [label for label, _ in option_labels]
                if labels != ["A", "B", "C"]:
                    findings.append(
                        Finding(
                            "ERROR",
                            "Open Question Options must contain exactly A, B, and C in order.",
                        )
                    )

            recommended_match = re.search(
                r"(?im)^\s*[-*]\s*Recommended\s*[:：]\s*([A-C])\s*$",
                content,
            )
            if re.search(r"(?im)^\s*[-*]\s*Recommended\s*[:：]", content) and not recommended_match:
                findings.append(
                    Finding(
                        "ERROR",
                        "Open Question Recommended must select A, B, or C.",
                    )
                )

            reason_match = re.search(
                r"(?im)^\s*[-*]\s*Reason\s*[:：]\s*\S.+$",
                content,
            )
            if re.search(r"(?im)^\s*[-*]\s*Reason\s*[:：]", content) and not reason_match:
                findings.append(
                    Finding(
                        "ERROR",
                        "Open Question Reason must contain one concise line.",
                    )
                )

            blocking_match = re.search(
                r"(?im)^\s*[-*]\s*Blocking\s*[:：]\s*(?P<value>[^\n]+)",
                content,
            )
            if blocking_match and not re.match(
                r"^(?:🔴Yes|No)(?:\s|[（(。.;；]|$)",
                blocking_match.group("value").strip(),
            ):
                findings.append(
                    Finding(
                        "ERROR",
                        "Open Question Blocking must use '🔴Yes' or 'No'.",
                    )
                )

    validate_implementation_content(text, findings)
    validate_secrets(text, findings)

    placeholder_matches = [
        match
        for match in re.finditer(r"<([^>\n]+)>", text)
        if not re.fullmatch(r"(?:https?://|mailto:).+", match.group(1), re.I)
        and not re.fullmatch(r"[^@\s]+@[^@\s]+", match.group(1))
    ]
    if placeholder_matches:
        findings.append(
            Finding(
                "ERROR",
                f"Unresolved angle-bracket placeholder found at line {line_number(text, placeholder_matches[0].start())}.",
            )
        )
    if re.search(r"\bDraft\s*/\s*Confirmed\s*/\s*Partially Blocked\b", text):
        findings.append(Finding("ERROR", "Template status choices were not resolved."))
    if "YYYY-MM-DD" in text:
        findings.append(Finding("ERROR", "Template date placeholder was not resolved."))

    current_pay_ids = {token for token in current_ids if token.startswith("PAY-")}
    payment_scope_trigger = re.search(
        r"支付|订阅|一次性购买|付费|结账|账单|额度|权益|"
        r"\bpayment\b|\bcheckout\b|\bsubscription\b|\bone-time\b|"
        r"\bcredits?\b|\bbilling\b|\bentitlement\b",
        current_scope_body,
        re.I,
    )
    if payment_scope_trigger and not current_pay_ids:
        findings.append(
            Finding(
                "ERROR",
                "Current Scope mentions payment or entitlement but has no PAY-xxx ID.",
            )
        )
    if current_pay_ids:
        payment_body = bodies.get(8, "")
        payment_definitions = {
            match.group(1)
            for line in payment_body.splitlines()
            if (match := DEFINITION_START_RE.match(line.strip()))
            and match.group(1).startswith("PAY-")
        }
        missing_payment_defs = current_pay_ids - payment_definitions
        for token in sorted(missing_payment_defs):
            findings.append(
                Finding("ERROR", f"Current payment ID {token} must be defined in section 8.")
            )

        payment_terms = {
            "payment mode": r"subscription|credits?|one-time|mixed|订阅|一次性|积分|额度",
            "product mapping": r"product|price|商品|价格映射",
            "checkout return": r"checkout.{0,80}(?:success|cancel)|成功.{0,40}取消|回跳",
            "webhook verification": r"webhook.{0,80}(?:verify|signature|验签)|验签",
            "idempotency": r"幂等|idempot",
            "entitlement": r"权益|entitlement|credits?",
            "failure compensation": r"补偿|refund|退款|retry|重试",
        }
        for label, pattern in payment_terms.items():
            if not re.search(pattern, payment_body, re.I | re.S):
                findings.append(
                    Finding("ERROR", f"Current PAY requirements are missing {label} coverage.")
                )

    copy_body = bodies.get(11, "")
    current_copy_ids = {token for token in current_ids if token.startswith("COPY-")}
    if current_copy_ids and not re.search(
        r"copy|文案|label|message|localization|i18n|key",
        copy_body,
        re.I,
    ):
        findings.append(
            Finding(
                "ERROR",
                "Current COPY requirements must define user-facing copy or the project's existing localization/content handling.",
            )
        )

    vague_terms = re.findall(r"体验良好|功能正常|正常工作|用户友好|美观大方", text)
    if vague_terms:
        findings.append(
            Finding(
                "WARNING",
                "Potentially vague acceptance wording found: "
                + ", ".join(sorted(set(vague_terms))),
            )
        )

    # Keep output deterministic when one defect triggers the same message twice.
    return list(dict.fromkeys(findings))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a docs/project/PRD.md product requirements document."
    )
    parser.add_argument("path", type=Path, help="Path to docs/project/PRD.md")
    args = parser.parse_args()

    findings = validate(args.path)
    errors = [finding for finding in findings if finding.level == "ERROR"]
    warnings = [finding for finding in findings if finding.level == "WARNING"]

    for finding in findings:
        print(f"{finding.level}: {finding.message}")

    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    text = args.path.read_text(encoding="utf-8-sig")
    ids = sorted(set(ID_RE.findall(text)))
    print(f"\nVALIDATION PASSED: {len(ids)} unique PRD ID(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
