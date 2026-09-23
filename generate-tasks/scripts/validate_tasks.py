#!/usr/bin/env python3
"""Validate canonical tasks.md and its derived task-prompt.md."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = (
    "Scope Freeze",
    "Traceability & Reuse",
    "Dependencies & Blockers",
    "Relevant Files",
    "Task Packages",
    "Verification Plan",
    "Development Rules & Task Management",
)

SECTION_ORDER = (
    "Scope Freeze",
    "Traceability & Reuse",
    "Dependencies & Blockers",
    "Relevant Files",
    "Task Packages",
    "Verification Plan",
    "Development Rules & Task Management",
)

REQUIRED_SCOPE_SUBSECTIONS = (
    "In Scope",
    "Existing Baseline",
    "Out of Scope",
    "Follow-up / Later",
)

REQUIRED_PARENT_FIELDS = (
    "任务类型",
    "状态",
    "验收方式",
    "人工前置",
    "前置状态",
    "真实联调",
    "来源",
    "目标",
    "边界 / 不做",
    "依赖",
    "子项",
    "涉及文件",
    "AI 验证",
)

REQUIRED_GATE_FIELDS = (
    "覆盖任务",
    "用户介入",
    "设置原因",
    "用户需检查",
    "通过标准",
    "未通过",
    "通过后",
)

ALLOWED_TASK_TYPES = {"Formal Task Package", "Confirmation Task"}
PENDING_STATE = "⬜ Pending"
IN_PROGRESS_STATE = "🔵 In progress"
READY_FOR_REVIEW_STATE = "🟡 Ready for review"
APPROVED_STATE = "✅ Approved"
BLOCKED_STATE = "⛔ Blocked"
ALLOWED_STATES = {
    PENDING_STATE,
    IN_PROGRESS_STATE,
    READY_FOR_REVIEW_STATE,
    APPROVED_STATE,
}
ALLOWED_ACCEPTANCE = {"AI 验证", "AI 验证后人工复查"}
ALLOWED_PREREQUISITES = {"None", "Required"}
ALLOWED_PREREQUISITE_STATES = {"Not required", "Pending", "Provided"}
ALLOWED_REAL_INTEGRATION = {"Not required", "Pending", "Verified"}
ALLOWED_TEST_STATUSES = {
    "Not tested",
    "Pending",
    "Passed",
    "Verified",
    "Failed",
    "Blocked",
}

LEGACY_FIELDS = ("验收门禁", "人工复核", "关卡验证")

PARENT_TITLE = re.compile(r"^\[([ xX])\] ((\d+)\.0) (.+)$")
GATE_TITLE = re.compile(r"^\[([ xX])\] (G-\d{2,}) (.+)$")
BLOCKED_TITLE = re.compile(r"^(BLOCKED-\d{3,}):\s+(.+)$")
FIELD_MARKER = re.compile(r"^- ([^：\n]+)：[ \t]*(.*)$", re.M)
CANONICAL_TEST_REF = re.compile(r"`(T-\d{3,})`")
ANY_TEST_TOKEN = re.compile(r"\bT-[A-Za-z0-9_-]+\b")
CANONICAL_GATE_REF = re.compile(r"`(G-\d{2,})`")
ANY_GATE_TOKEN = re.compile(r"\bG-[A-Za-z0-9_-]+\b")
CANONICAL_TASK_REF = re.compile(r"`(\d+\.0)`")
PRD_ID_REF = re.compile(r"`([A-Z][A-Z0-9_-]*-\d+)`")
USER_INTERVENTION = re.compile(
    r"^🔴 P([123]) (User Action Required|User Decision Required|User Approval Required)$"
)
VERIFICATION_HEADER = (
    "| ID | Stage | Scenario | Executor | Page / Entry | Steps or Command | "
    "Expected Result | Status |"
)

TRACEABILITY_HEADER = (
    "| PRD ID | Requirement Summary | Task Package | Coverage | Status |"
)

DEPENDENCY_HEADER = (
    "| Task Package | Direct Dependencies | Unlocks | Start Condition |"
)

FIRST_BATCH_HEADER = (
    "| Worker | Task Package | Dependencies | Critical Path | Branch | "
    "Allowed Files / Modules | Focused Validation |"
)

FIRST_BATCH_HEADER_WITH_DO_NOT_TOUCH = (
    "| Worker | Task Package | Dependencies | Critical Path | Branch | "
    "Allowed Files / Modules | Do Not Touch | Focused Validation |"
)

TASK_STATUS_LEGEND = (
    "任务状态：⬜ Pending · 🔵 In progress · 🟡 Ready for review · "
    "✅ Approved · ⛔ Blocked"
)

TASK_PROMPT_TITLE_SUFFIX = "Task Execution Prompts"
TASK_PROMPT_ROLE = "本文件仅供复制 Prompt"
TASK_PROMPT_COMPLETED_TITLE = "已完成"
TASK_PROMPT_UNFINISHED_TITLE = "未完成"
TASK_PROMPT_HEADING = re.compile(r"^Task (\d+\.0) — (.+)$")
TASK_PROMPT_OBSOLETE_TOP_GUIDANCE = re.compile(
    r"^(?:Next task:|Execution mode:|Execution mode rationale:|>?\s*使用方法：)",
    re.M,
)
TASK_PROMPT_VAGUE_EXPLANATION = re.compile(
    r"这部分能力|核心流程|补齐(?:功能|工作)|形成(?:一套)?(?:完整)?结果|"
    r"客观(?:验证|确认)|可核对的验证结果|按已确认流程"
)

COMMAND_PATTERN = re.compile(
    r"(?i)(?:"
    r"`?\b(?:pnpm|npm|yarn|bun|npx|node|python\d*|pytest|curl|wget|git|rg|"
    r"grep|sed|awk|bash|zsh|sh|powershell|pwsh|psql|mysql|sqlite3|wrangler|"
    r"drizzle-kit)\b[^`\n]*`?"
    r"|(?:^|\s)\$\s+\S+"
    r"|--[a-z][a-z0-9-]*"
    r"|运行.{0,8}命令"
    r"|执行.{0,8}命令"
    r"|查看.{0,8}源代码"
    r"|inspect.{0,8}source code"
    r")"
)

KNOWN_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\bpostgres(?:ql)?://[^\s`]+"),
    re.compile(r"(?i)\bmysql://[^\s`]+"),
    re.compile(r"\bsk-(?:live|test)?-?[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\b(?:ghp_|github_pat_|xox[baprs]-|whsec_|rk_live_|re_)[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?i)(?:验证码|verification[ _-]?code|2fa[ _-]?code)\s*[:=]\s*\d{6,8}\b"),
)

GENERIC_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_ -]?key|client[_ -]?secret|webhook[_ -]?secret|"
    r"secret|access[_ -]?token|refresh[_ -]?token|token|password|passwd)"
    r"\b\s*[:=]\s*[`\"']?([^\s`\"']{8,})"
)

PLACEHOLDER_VALUES = {
    "...",
    "example",
    "placeholder",
    "redacted",
    "masked",
    "changeme",
    "variable_name",
    "secret_name",
    "api_key",
    "token",
    "password",
}


@dataclass
class Heading:
    level: int
    title: str
    start: int
    end: int


@dataclass
class Parent:
    task_id: str
    title: str
    checkbox: str
    state: str
    acceptance: str
    prerequisite: str
    prerequisite_state: str
    real_integration: str
    dependencies: tuple[str, ...]
    test_refs: tuple[str, ...]
    gate_ref: str | None
    block: str


@dataclass
class Gate:
    gate_id: str
    title: str
    checkbox: str
    covered_tasks: tuple[str, ...]
    block: str


@dataclass
class TestRow:
    test_id: str
    stages: tuple[str, ...]
    executor: str
    status: str
    line_number: int


@dataclass
class BlockedTask:
    blocker_id: str
    title: str
    state: str
    block: str


@dataclass
class WorkerAssignment:
    worker: str
    task_id: str
    dependencies: str
    branch: str
    allowed: str
    do_not_touch: str | None
    focused_validation: str


def strip_ticks(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def markdown_headings(text: str) -> list[Heading]:
    """Return ATX headings outside fenced code blocks."""
    headings: list[Heading] = []
    offset = 0
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        fence_match = re.match(r"(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)
            marker_char = marker[0]
            if fence is None:
                fence = marker_char
            elif fence == marker_char:
                fence = None
            offset += len(line)
            continue
        if fence is None:
            match = re.match(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*(?:\r?\n)?$", line)
            if match:
                headings.append(
                    Heading(
                        level=len(match.group(1)),
                        title=match.group(2).strip(),
                        start=offset,
                        end=offset + len(line),
                    )
                )
        offset += len(line)
    return headings


def section_bounds(
    text: str, headings: list[Heading], title: str
) -> tuple[int, int] | None:
    matches = [heading for heading in headings if heading.level == 2 and heading.title == title]
    if len(matches) != 1:
        return None
    heading = matches[0]
    end = len(text)
    for candidate in headings:
        if candidate.level == 2 and candidate.start > heading.start:
            end = candidate.start
            break
    return heading.end, end


def section_text(text: str, headings: list[Heading], title: str) -> str:
    bounds = section_bounds(text, headings, title)
    if bounds is None:
        return ""
    return text[bounds[0] : bounds[1]]


def h3_blocks(section: str) -> list[tuple[Heading, str]]:
    headings = [heading for heading in markdown_headings(section) if heading.level == 3]
    blocks: list[tuple[Heading, str]] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start if index + 1 < len(headings) else len(section)
        blocks.append((heading, section[heading.start:end]))
    return blocks


def heading_block(section: str, level: int, title: str) -> str:
    headings = markdown_headings(section)
    matches = [
        heading
        for heading in headings
        if heading.level == level and heading.title == title
    ]
    if len(matches) != 1:
        return ""
    heading = matches[0]
    end = len(section)
    for candidate in headings:
        if candidate.start > heading.start and candidate.level <= level:
            end = candidate.start
            break
    return section[heading.start:end]


def child_blocks(section: str, level: int) -> list[tuple[Heading, str]]:
    headings = [
        heading for heading in markdown_headings(section) if heading.level == level
    ]
    blocks: list[tuple[Heading, str]] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start if index + 1 < len(headings) else len(section)
        blocks.append((heading, section[heading.start:end]))
    return blocks


def text_fences(block: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(
            r"```text[ \t]*\n(.*?)\n[ \t]*```",
            block,
            re.S,
        )
    ]


def normalize_markdown(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("`", "")).strip()


def prohibits_worker_main_operations(prompt: str) -> bool:
    """Return whether a Worker prompt clearly prohibits operations on main."""
    for clause in re.split(r"[\n。！？.!?]+", prompt):
        if not re.search(r"\bmain\b", clause, re.I):
            continue
        if not re.search(r"(?:不得|禁止|不要|must\s+not|do\s+not)", clause, re.I):
            continue
        if re.search(
            r"(?:操作|切换|修改|合并|推送|工作|operate|switch|modify|merge|push|work)",
            clause,
            re.I,
        ):
            return True
    return False


def field_markers_outside_fences(
    block: str,
) -> list[tuple[str, int, int, str]]:
    markers: list[tuple[str, int, int, str]] = []
    offset = 0
    fence_char: str | None = None
    fence_length = 0

    for line in block.splitlines(keepends=True):
        fence_match = re.match(r"^[ \t]*(`{3,}|~{3,})", line)
        if fence_match:
            fence = fence_match.group(1)
            if fence_char is None:
                fence_char = fence[0]
                fence_length = len(fence)
            elif fence[0] == fence_char and len(fence) >= fence_length:
                fence_char = None
                fence_length = 0
            offset += len(line)
            continue

        if fence_char is None:
            match = FIELD_MARKER.match(line)
            if match:
                markers.append(
                    (
                        match.group(1).strip(),
                        offset + match.start(),
                        offset + match.end(),
                        match.group(2).rstrip(),
                    )
                )
        offset += len(line)

    return markers


def parse_fields(block: str) -> tuple[dict[str, str], list[str]]:
    markers = field_markers_outside_fences(block)
    fields: dict[str, str] = {}
    duplicates: list[str] = []
    for index, (name, _, marker_end, first_line) in enumerate(markers):
        end = markers[index + 1][1] if index + 1 < len(markers) else len(block)
        tail = block[marker_end:end]
        content = first_line
        if tail:
            content = f"{first_line}{tail}".strip()
        if name in fields:
            duplicates.append(name)
        else:
            fields[name] = content
    return fields, duplicates


def parse_markdown_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if len(stripped) < 2 or not stripped.startswith("|") or not stripped.endswith("|"):
        return None

    trailing_backslashes = 0
    for char in reversed(stripped[:-1]):
        if char != "\\":
            break
        trailing_backslashes += 1
    if trailing_backslashes % 2:
        return None

    cells: list[str] = []
    current: list[str] = []
    for char in stripped[1:-1]:
        if char != "|":
            current.append(char)
            continue

        preceding_backslashes = 0
        for current_char in reversed(current):
            if current_char != "\\":
                break
            preceding_backslashes += 1
        if preceding_backslashes % 2:
            current.pop()
            current.append("|")
            continue

        cells.append("".join(current).strip())
        current = []

    cells.append("".join(current).strip())
    return cells


def scalar(fields: dict[str, str], name: str) -> str:
    value = fields.get(name, "")
    first = value.splitlines()[0].strip() if value else ""
    return strip_ticks(first)


def exact_scalar(fields: dict[str, str], name: str) -> str:
    """Return a scalar only when the whole field contains that scalar."""
    return strip_ticks(fields.get(name, "").strip())


def first_line(fields: dict[str, str], name: str) -> str:
    value = fields.get(name, "")
    return value.splitlines()[0].strip() if value else ""


def validate_intervention(
    value: str,
    label: str,
    errors: list[str],
    allowed_kinds: set[str],
) -> str | None:
    match = USER_INTERVENTION.fullmatch(strip_ticks(value))
    if not match:
        allowed = " or ".join(sorted(allowed_kinds))
        errors.append(
            f"{label}: 用户介入 must use `🔴 P1/P2/P3 {allowed}`."
        )
        return None
    kind = match.group(2)
    if kind not in allowed_kinds:
        allowed = " or ".join(sorted(allowed_kinds))
        errors.append(f"{label}: 用户介入 must be {allowed}, not {kind}.")
        return None
    return kind


def parse_exact_refs(
    value: str,
    canonical_pattern: re.Pattern[str],
    token_pattern: re.Pattern[str],
    separator_pattern: str,
) -> tuple[list[str], bool]:
    refs = canonical_pattern.findall(value)
    mentioned = token_pattern.findall(value)
    scrubbed = canonical_pattern.sub("", value)
    scrubbed = re.sub(separator_pattern, "", scrubbed)
    valid = bool(refs) and not scrubbed and sorted(refs) == sorted(mentioned)
    return refs, valid


def possible_secret_line(text: str) -> int | None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in KNOWN_SECRET_PATTERNS:
            if pattern.search(line):
                return line_number
        assignment = GENERIC_SECRET_ASSIGNMENT.search(line)
        if not assignment:
            continue
        value = assignment.group(1).strip().rstrip(".,;，；)")
        normalized = value.lower()
        if (
            normalized in PLACEHOLDER_VALUES
            or value.startswith(("<", "${", "$"))
            or re.fullmatch(r"[A-Z][A-Z0-9_]{5,}", value)
            or set(value) <= {"*", "x", "X", "•"}
        ):
            continue
        if len(value) >= 8:
            return line_number
    return None


def validate_sections(
    text: str, headings: list[Heading], errors: list[str]
) -> None:
    if TASK_STATUS_LEGEND not in text:
        errors.append("Task status legend is missing or differs from the canonical symbols.")

    h2_titles = [heading.title for heading in headings if heading.level == 2]
    for required in REQUIRED_SECTIONS:
        count = h2_titles.count(required)
        if count == 0:
            errors.append(f"Missing required section: ## {required}")
        elif count > 1:
            errors.append(f"Required section appears more than once: ## {required}")

    present_known = [title for title in h2_titles if title in SECTION_ORDER]
    order_indexes = [SECTION_ORDER.index(title) for title in present_known]
    if order_indexes != sorted(order_indexes):
        errors.append("Known sections are not in the required order.")

    for forbidden_section in ("Execution Guide", "Execution Plan", "Execution Prompts"):
        if forbidden_section in h2_titles:
            errors.append(
                f"tasks.md must not contain ## {forbidden_section}; "
                "operational guidance belongs in task-prompt.md."
            )

    scope = section_text(text, headings, "Scope Freeze")
    scope_h3 = [heading.title for heading in markdown_headings(scope) if heading.level == 3]
    for subsection in REQUIRED_SCOPE_SUBSECTIONS:
        if subsection not in scope_h3:
            errors.append(f"Scope Freeze is missing subsection: ### {subsection}")

    traceability = section_text(text, headings, "Traceability & Reuse")
    if traceability and TRACEABILITY_HEADER not in traceability:
        errors.append("Requirement Traceability table header is missing or invalid.")

    dependencies = section_text(text, headings, "Dependencies & Blockers")
    if dependencies and DEPENDENCY_HEADER not in dependencies:
        errors.append("Task Dependency Graph table header is missing or invalid.")

    if re.search(r"^- (?:执行 Prompt|Stop Condition)：", text, re.M):
        errors.append(
            "tasks.md must not contain 执行 Prompt or Stop Condition fields; "
            "copyable prompts belong in task-prompt.md."
        )
    for forbidden_heading in (
        "Main Manager Kickoff Prompt",
        "First Batch Worker Launch Prompts",
        "Worker Completion Handoff",
    ):
        if any(heading.title == forbidden_heading for heading in headings):
            errors.append(
                f"tasks.md must not contain {forbidden_heading}; "
                "operational prompts belong in task-prompt.md."
            )


def validate_traceability_table(
    text: str,
    headings: list[Heading],
    errors: list[str],
) -> None:
    traceability = section_text(text, headings, "Traceability & Reuse")
    if not traceability or TRACEABILITY_HEADER not in traceability:
        return

    lines = traceability.splitlines()
    header_index = next(
        (
            index
            for index, line in enumerate(lines)
            if line.strip() == TRACEABILITY_HEADER
        ),
        None,
    )
    if header_index is None:
        return
    if header_index + 1 >= len(lines) or not re.fullmatch(
        r"\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*){4}\|",
        lines[header_index + 1].strip(),
    ):
        errors.append("Requirement Traceability table separator is missing or invalid.")
        return

    row_count = 0
    saw_data_row = False
    column_names = (
        "PRD ID",
        "Requirement Summary",
        "Task Package",
        "Coverage",
        "Status",
    )
    for relative_index, line in enumerate(
        lines[header_index + 2 :], start=header_index + 3
    ):
        stripped = line.strip()
        if not stripped:
            if saw_data_row:
                break
            continue
        if not stripped.startswith("|"):
            if saw_data_row:
                break
            continue

        saw_data_row = True
        cells = parse_markdown_table_row(stripped)
        if cells is None:
            errors.append(
                f"Requirement Traceability line {relative_index}: invalid table row."
            )
            continue
        if len(cells) != 5:
            errors.append(
                f"Requirement Traceability line {relative_index}: expected exactly "
                "5 columns in PRD ID | Requirement Summary | Task Package | "
                "Coverage | Status order."
            )
            continue
        row_count += 1
        for column_name, cell in zip(column_names, cells):
            if not cell:
                errors.append(
                    f"Requirement Traceability line {relative_index}: "
                    f"{column_name} must not be empty."
                )

    if not saw_data_row:
        errors.append("Requirement Traceability table contains no requirement rows.")


def validate_single_agent_guide(
    text: str,
    headings: list[Heading],
    errors: list[str],
) -> None:
    guide = section_text(text, headings, "Execution Guide")
    single_agent = heading_block(guide, 3, "Single-Agent Start")
    if not single_agent:
        return

    fields, duplicates = parse_fields(single_agent)
    for name in duplicates:
        errors.append(f"Single-Agent Start: duplicate field '{name}'.")
    for name in ("当前模式", "判断依据", "调度规则"):
        if name not in fields or not first_line(fields, name):
            errors.append(f"Single-Agent Start is missing field '{name}'.")

    mode = strip_ticks(first_line(fields, "当前模式"))
    if mode and mode != "Single-Agent":
        errors.append("Single-Agent Start 当前模式 must be exactly `Single-Agent`.")

    rationale = normalize_markdown(first_line(fields, "判断依据"))
    required_rationale_patterns = {
        "actual conflict cost": r"(?:conflict|冲突|共享写入|shared[- ]file)",
        "coordination/integration cost": r"(?:coordination|协调|整合|integration|merge|review)",
        "resource cost": r"(?:resource|资源|CPU|RAM|browser|浏览器|build|test)",
        "parallel benefit": r"(?:并行收益|parallel benefit|parallel gain|净收益)",
        "cost-benefit comparison": r"(?:高于|超过|大于|不抵|不足以抵消|outweigh)",
    }
    for description, pattern in required_rationale_patterns.items():
        if rationale and not re.search(pattern, rationale, re.I):
            errors.append(
                "Single-Agent Start 判断依据 must explain repository-specific "
                f"{description}."
            )

    scheduling = normalize_markdown(first_line(fields, "调度规则"))
    for description, pattern in (
        ("runnable parents", r"\brunnable\b"),
        ("direct dependency", r"(?:direct dependency|直接依赖|依赖已满足)"),
        ("critical path", r"(?:critical path|关键路径)"),
    ):
        if scheduling and not re.search(pattern, scheduling, re.I):
            errors.append(
                f"Single-Agent Start 调度规则 must select by {description}."
            )
    if re.search(
        r"(?:按|依照)(?:任务)?编号(?:顺序)?(?:推进|执行|选择|开始)|"
        r"从\s*`?1\.0`?\s*(?:开始|推进)",
        scheduling,
        re.I,
    ):
        errors.append(
            "Single-Agent Start must not use task numbering as the serial schedule."
        )


def validate_parent(
    heading: Heading,
    block: str,
    errors: list[str],
    warnings: list[str],
) -> Parent | None:
    title_match = PARENT_TITLE.fullmatch(heading.title)
    if not title_match:
        return None

    checkbox, task_id, number, title = title_match.groups()
    label = f"{task_id} {title}"
    fields, duplicates = parse_fields(block)
    for name in duplicates:
        errors.append(f"{label}: duplicate field '{name}'.")
    for name in REQUIRED_PARENT_FIELDS:
        if name not in fields:
            errors.append(f"{label}: missing field '{name}'.")
    for forbidden in ("执行 Prompt", "Stop Condition"):
        if forbidden in fields:
            errors.append(
                f"{label}: tasks.md parent must not contain '{forbidden}'; "
                "operational prompts belong in task-prompt.md."
            )

    task_type = exact_scalar(fields, "任务类型")
    state = exact_scalar(fields, "状态")
    acceptance = exact_scalar(fields, "验收方式")
    prerequisite = exact_scalar(fields, "人工前置")
    prerequisite_state = exact_scalar(fields, "前置状态")
    real_integration = exact_scalar(fields, "真实联调")
    dependencies = tuple(CANONICAL_TASK_REF.findall(fields.get("依赖", "")))

    if task_type not in ALLOWED_TASK_TYPES:
        errors.append(f"{label}: invalid 任务类型 '{task_type}'.")
    if state not in ALLOWED_STATES:
        errors.append(f"{label}: invalid 状态 '{state}'.")
    if acceptance not in ALLOWED_ACCEPTANCE:
        errors.append(f"{label}: invalid 验收方式 '{acceptance}'.")
    if prerequisite not in ALLOWED_PREREQUISITES:
        errors.append(f"{label}: invalid 人工前置 '{prerequisite}'.")
    if prerequisite_state not in ALLOWED_PREREQUISITE_STATES:
        errors.append(f"{label}: invalid 前置状态 '{prerequisite_state}'.")
    if real_integration not in ALLOWED_REAL_INTEGRATION:
        errors.append(f"{label}: invalid 真实联调 '{real_integration}'.")

    checked = checkbox.lower() == "x"
    if checked != (state == APPROVED_STATE):
        errors.append(
            f"{label}: checkbox [x] must be equivalent to 状态 {APPROVED_STATE}."
        )

    if acceptance == "AI 验证" and state == READY_FOR_REVIEW_STATE:
        errors.append(f"{label}: AI 验证 cannot use {READY_FOR_REVIEW_STATE}.")

    source = fields.get("来源", "")
    prd_ids = {
        ref
        for ref in PRD_ID_REF.findall(source)
        if not ref.startswith(("T-", "G-", "BLOCKED-"))
    }
    if not prd_ids:
        errors.append(f"{label}: 来源 must contain at least one backticked stable PRD ID.")

    subtasks = fields.get("子项", "")
    subtask_matches = re.findall(r"^\s*-\s+(\d+)\.(\d+)\s+.+$", subtasks, re.M)
    if not subtask_matches:
        errors.append(f"{label}: 子项 must contain at least one numbered subtask.")
    for parent_number, _ in subtask_matches:
        if parent_number != number:
            errors.append(f"{label}: subtask number does not match parent {task_id}.")
    if re.search(r"^\s+-\s+\[[ xX]\]", subtasks, re.M):
        errors.append(f"{label}: subtasks must not use checkboxes.")

    if not fields.get("涉及文件", "").strip():
        errors.append(f"{label}: 涉及文件 must not be empty.")

    ai_value = first_line(fields, "AI 验证")
    test_refs, test_refs_valid = parse_exact_refs(
        ai_value,
        CANONICAL_TEST_REF,
        ANY_TEST_TOKEN,
        r"[\s,，、;；]+",
    )
    if not test_refs_valid:
        errors.append(
            f"{label}: AI 验证 must contain only canonical backticked T-xxx IDs."
        )
    if len(test_refs) != len(set(test_refs)):
        errors.append(f"{label}: AI 验证 contains duplicate T-* references.")

    gate_ref: str | None = None
    gate_field_present = "人工验收关卡" in fields
    if acceptance == "AI 验证后人工复查":
        if not gate_field_present:
            errors.append(f"{label}: human-review task must reference 人工验收关卡.")
        else:
            gate_value = first_line(fields, "人工验收关卡")
            gate_refs = CANONICAL_GATE_REF.findall(gate_value)
            mentioned_gates = ANY_GATE_TOKEN.findall(gate_value)
            if len(gate_refs) != 1 or gate_refs != mentioned_gates:
                errors.append(
                    f"{label}: 人工验收关卡 must reference exactly one canonical `G-xx`."
                )
            else:
                gate_ref = gate_refs[0]
    elif gate_field_present:
        errors.append(f"{label}: AI 验证 task must not reference 人工验收关卡.")

    mentioned_gate_refs = set(ANY_GATE_TOKEN.findall(block))
    expected_gate_refs = {gate_ref} if gate_ref else set()
    if mentioned_gate_refs != expected_gate_refs:
        unexpected = sorted(mentioned_gate_refs - expected_gate_refs)
        if unexpected:
            errors.append(
                f"{label}: parent mentions checkpoint(s) without a matching "
                f"人工验收关卡 field: {', '.join(unexpected)}."
            )

    if prerequisite == "Required":
        if prerequisite_state not in {"Pending", "Provided"}:
            errors.append(
                f"{label}: Required 人工前置 needs 前置状态 Pending or Provided."
            )
        for name in ("用户需完成", "需要时间", "完成后"):
            if name not in fields or not fields[name].strip():
                errors.append(f"{label}: Required 人工前置 is missing '{name}'.")
        if "用户介入" not in fields:
            errors.append(f"{label}: Required 人工前置 is missing '用户介入'.")
        else:
            validate_intervention(
                scalar(fields, "用户介入"),
                label,
                errors,
                {"User Action Required"},
            )
        timing = scalar(fields, "需要时间")
        if timing and not any(token in timing for token in ("开始任务前", "执行到")):
            errors.append(
                f"{label}: 需要时间 must say 开始任务前 or 执行到某一步时."
            )
        completion = fields.get("完成后", "")
        if completion and ("AI" not in completion or "继续" not in completion):
            warnings.append(f"{label}: 完成后 should say that AI continues from the blocker.")
        if prerequisite_state == "Pending" and state in {
            READY_FOR_REVIEW_STATE,
            APPROVED_STATE,
        }:
            errors.append(
                f"{label}: unresolved prerequisite cannot coexist with {state}."
            )
    elif prerequisite == "None":
        if prerequisite_state != "Not required":
            errors.append(
                f"{label}: 人工前置 None requires 前置状态 Not required."
            )
        for name in ("用户需完成", "需要时间", "完成后"):
            if name in fields:
                errors.append(
                    f"{label}: 人工前置 None must not include conflicting field '{name}'."
                )
        if "用户介入" in fields:
            errors.append(
                f"{label}: 人工前置 None must not include conflicting field '用户介入'."
            )

    return Parent(
        task_id=task_id,
        title=title,
        checkbox=checkbox.lower(),
        state=state,
        acceptance=acceptance,
        prerequisite=prerequisite,
        prerequisite_state=prerequisite_state,
        real_integration=real_integration,
        dependencies=dependencies,
        test_refs=tuple(test_refs),
        gate_ref=gate_ref,
        block=block,
    )


def validate_gate(
    heading: Heading,
    block: str,
    errors: list[str],
    warnings: list[str],
) -> Gate | None:
    title_match = GATE_TITLE.fullmatch(heading.title)
    if not title_match:
        return None
    checkbox, gate_id, title = title_match.groups()
    label = f"{gate_id} {title}"
    fields, duplicates = parse_fields(block)
    for name in duplicates:
        errors.append(f"{label}: duplicate field '{name}'.")
    for name in REQUIRED_GATE_FIELDS:
        if name not in fields or not fields[name].strip():
            errors.append(f"{label}: missing or empty field '{name}'.")

    coverage_value = first_line(fields, "覆盖任务")
    covered, coverage_valid = parse_exact_refs(
        coverage_value,
        CANONICAL_TASK_REF,
        re.compile(r"\b\d+\.0\b"),
        r"[\s,，、;；]+",
    )
    if not coverage_valid:
        errors.append(
            f"{label}: 覆盖任务 must contain only canonical backticked parent IDs."
        )
    if len(covered) != len(set(covered)):
        errors.append(f"{label}: 覆盖任务 contains duplicate parent IDs.")

    validate_intervention(
        scalar(fields, "用户介入"),
        label,
        errors,
        {"User Decision Required", "User Approval Required"},
    )

    user_steps = fields.get("用户需检查", "")

    if "```" in block or "~~~" in block:
        errors.append(f"{label}: human checkpoint must not contain a code fence.")
    if ANY_TEST_TOKEN.search(block):
        errors.append(f"{label}: human checkpoint must not contain T-* test IDs.")
    if re.search(r"(?i)Verification Plan", block):
        errors.append(f"{label}: human checkpoint must not delegate to Verification Plan.")
    if COMMAND_PATTERN.search(user_steps):
        errors.append(
            f"{label}: 用户需检查 contains a technical command or source-code task."
        )

    failure = fields.get("未通过", "")
    if failure and (
        IN_PROGRESS_STATE not in failure
        or not re.search(r"(?:重开|reopen)", failure, re.I)
        or "AI 验证" not in failure
    ):
        errors.append(
            f"{label}: 未通过 must reopen affected tasks to "
            f"{IN_PROGRESS_STATE} and rerun AI verification."
        )

    after = fields.get("通过后", "")
    if after and ("[x]" not in after or APPROVED_STATE not in after):
        errors.append(
            f"{label}: 通过后 must mark the gate [x] and covered tasks "
            f"{APPROVED_STATE}/[x]."
        )
    for task_id in covered:
        if failure and task_id not in failure:
            errors.append(
                f"{label}: 未通过 must name covered task {task_id} when reopening it."
            )
        if after and task_id not in after:
            errors.append(
                f"{label}: 通过后 must name covered task {task_id} when approving it."
            )

    for name in ("设置原因", "通过标准"):
        if name in fields and len(fields[name].strip()) < 4:
            warnings.append(f"{label}: '{name}' is too vague.")

    return Gate(
        gate_id=gate_id,
        title=title,
        checkbox=checkbox.lower(),
        covered_tasks=tuple(covered),
        block=block,
    )


def validate_blocked_task(
    heading: Heading,
    block: str,
    errors: list[str],
) -> BlockedTask | None:
    title_match = BLOCKED_TITLE.fullmatch(heading.title)
    if not title_match:
        return None
    blocker_id, title = title_match.groups()
    label = f"{blocker_id} {title}"
    fields, duplicates = parse_fields(block)
    for name in duplicates:
        errors.append(f"{label}: duplicate field '{name}'.")
    required = (
        "状态",
        "受影响 PRD ID",
        "阻塞来源",
        "原因",
        "解除条件",
        "解除前允许做",
        "禁止做",
    )
    for name in required:
        if name not in fields or not fields[name].strip():
            errors.append(f"{label}: missing or empty field '{name}'.")

    state = exact_scalar(fields, "状态")
    if state != BLOCKED_STATE:
        errors.append(f"{label}: 状态 must be exactly '{BLOCKED_STATE}'.")

    source_ids = {
        ref
        for ref in PRD_ID_REF.findall(fields.get("受影响 PRD ID", ""))
        if not ref.startswith(("T-", "G-", "BLOCKED-"))
    }
    if not source_ids:
        errors.append(
            f"{label}: 受影响 PRD ID must contain a backticked stable PRD ID."
        )
    for forbidden in ("执行 Prompt", "Stop Condition", "AI 验证", "人工验收关卡"):
        if forbidden in fields:
            errors.append(f"{label}: Blocked Task must not contain '{forbidden}'.")
    if re.search(r"^###\s+\[[ xX]\]", block, re.M):
        errors.append(f"{label}: Blocked Task must not use a checkbox.")
    if "用户介入" in fields:
        validate_intervention(
            scalar(fields, "用户介入"),
            label,
            errors,
            {
                "User Action Required",
                "User Decision Required",
                "User Approval Required",
            },
        )
    return BlockedTask(
        blocker_id=blocker_id,
        title=title,
        state=state,
        block=block,
    )


def parse_verification_rows(
    text: str,
    headings: list[Heading],
    errors: list[str],
    require_rows: bool,
) -> dict[str, TestRow]:
    verification = section_text(text, headings, "Verification Plan")
    if not verification:
        return {}
    lines = verification.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.strip() == VERIFICATION_HEADER),
        None,
    )
    if header_index is None:
        errors.append("Verification Plan table header is missing or differs from schema.")
        return {}
    if header_index + 1 >= len(lines) or not re.fullmatch(
        r"\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*){7}\|",
        lines[header_index + 1].strip(),
    ):
        errors.append("Verification Plan table separator is missing or invalid.")
        return {}

    rows: dict[str, TestRow] = {}
    row_lines = lines[header_index + 2 :]
    for relative_index, line in enumerate(row_lines, start=header_index + 3):
        stripped = line.strip()
        if not stripped:
            if rows:
                break
            continue
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = parse_markdown_table_row(stripped)
        if cells is None:
            errors.append(
                f"Verification Plan line {relative_index}: invalid table row."
            )
            continue
        if len(cells) != 8:
            errors.append(
                f"Verification Plan line {relative_index}: expected 8 table columns."
            )
            continue

        raw_id, raw_stage, _, executor, _, _, _, status = cells
        id_match = re.fullmatch(r"`(T-\d{3,})`", raw_id)
        if not id_match:
            errors.append(
                f"Verification Plan line {relative_index}: invalid canonical T-* ID."
            )
            continue
        test_id = id_match.group(1)
        if test_id in rows:
            errors.append(f"Verification test defined more than once: {test_id}")
            continue

        stages = tuple(CANONICAL_TASK_REF.findall(raw_stage))
        stage_tokens = re.findall(r"\b\d+\.0\b", raw_stage)
        if not stages or sorted(stages) != sorted(stage_tokens):
            errors.append(
                f"{test_id}: Stage must contain canonical backticked parent task IDs."
            )

        if executor != "AI":
            errors.append(
                f"{test_id}: new Verification Plan rows must use Executor AI; "
                "human prerequisites belong in parent fields and human review belongs in G-*."
            )
        if status not in ALLOWED_TEST_STATUSES:
            errors.append(f"{test_id}: invalid verification Status '{status}'.")

        rows[test_id] = TestRow(
            test_id=test_id,
            stages=stages,
            executor=executor,
            status=status,
            line_number=relative_index,
        )

    if require_rows and not rows:
        errors.append("Verification Plan contains no T-* rows.")
    return rows


def validate_cross_references(
    parents: dict[str, Parent],
    gates: dict[str, Gate],
    tests: dict[str, TestRow],
    errors: list[str],
    warnings: list[str],
) -> None:
    referenced_tests: dict[str, set[str]] = {}
    for parent in parents.values():
        for test_id in parent.test_refs:
            referenced_tests.setdefault(test_id, set()).add(parent.task_id)
            row = tests.get(test_id)
            if row is None:
                errors.append(
                    f"{parent.task_id}: referenced verification test is not defined: {test_id}"
                )
                continue
            if parent.task_id not in row.stages:
                errors.append(
                    f"{test_id}: Stage does not include referencing parent {parent.task_id}."
                )
            if parent.state in {READY_FOR_REVIEW_STATE, APPROVED_STATE}:
                if row.status in {"Not tested", "Failed", "Blocked"}:
                    errors.append(
                        f"{parent.task_id}: state {parent.state} conflicts with "
                        f"{test_id} status {row.status}."
                    )
                if row.status == "Pending" and parent.real_integration != "Pending":
                    errors.append(
                        f"{parent.task_id}: {test_id} may remain Pending after AI verification "
                        "only when 真实联调 is Pending."
                    )
                elif row.status == "Pending" and parent.state == APPROVED_STATE:
                    warnings.append(
                        f"{parent.task_id}: {APPROVED_STATE} with {test_id} and "
                        "真实联调 Pending "
                        "is valid only when PRD treats real integration as a non-blocking "
                        "follow-up rather than this parent's acceptance condition."
                    )

    for test_id in sorted(set(tests) - set(referenced_tests)):
        errors.append(f"Verification test is defined but never referenced: {test_id}")

    gate_references: dict[str, set[str]] = {}
    for parent in parents.values():
        if parent.gate_ref:
            gate_references.setdefault(parent.gate_ref, set()).add(parent.task_id)
            if parent.gate_ref not in gates:
                errors.append(
                    f"{parent.task_id}: referenced human checkpoint is not defined: "
                    f"{parent.gate_ref}"
                )

    covered_by: dict[str, set[str]] = {}
    for gate in gates.values():
        for task_id in gate.covered_tasks:
            covered_by.setdefault(task_id, set()).add(gate.gate_id)
            parent = parents.get(task_id)
            if parent is None:
                errors.append(
                    f"{gate.gate_id}: 覆盖任务 references unknown parent {task_id}."
                )
                continue
            if parent.acceptance != "AI 验证后人工复查":
                errors.append(
                    f"{gate.gate_id}: must not cover AI-only parent {task_id}."
                )
            if parent.gate_ref != gate.gate_id:
                errors.append(
                    f"{gate.gate_id}: coverage and {task_id} 人工验收关卡 do not match."
                )

            gate_checked = gate.checkbox == "x"
            parent_approved = (
                parent.checkbox == "x" and parent.state == APPROVED_STATE
            )
            if gate_checked != parent_approved:
                errors.append(
                    f"{gate.gate_id}: checkbox status conflicts with covered parent "
                    f"{task_id} state/checkbox."
                )

        if gate.gate_id not in gate_references:
            errors.append(f"{gate.gate_id}: checkpoint is not referenced by any parent.")

    for task_id, gate_ids in covered_by.items():
        if len(gate_ids) > 1:
            errors.append(
                f"{task_id}: covered by multiple human checkpoints: "
                f"{', '.join(sorted(gate_ids))}"
            )

    for parent in parents.values():
        if parent.acceptance != "AI 验证后人工复查":
            continue
        if parent.gate_ref and parent.task_id not in gates.get(
            parent.gate_ref,
            Gate("", "", " ", (), ""),
        ).covered_tasks:
            errors.append(
                f"{parent.task_id}: referenced {parent.gate_ref} does not cover this task."
            )
        if parent.state == READY_FOR_REVIEW_STATE and parent.gate_ref:
            gate = gates.get(parent.gate_ref)
            if gate and gate.checkbox == "x":
                errors.append(
                    f"{parent.task_id}: {READY_FOR_REVIEW_STATE} conflicts with completed "
                    f"{parent.gate_ref}."
                )

    for parent in parents.values():
        if parent.real_integration == "Verified":
            matching_rows = [
                tests[test_id]
                for test_id in parent.test_refs
                if test_id in tests
                and tests[test_id].status in {"Passed", "Verified"}
            ]
            if not matching_rows:
                warnings.append(
                    f"{parent.task_id}: 真实联调 Verified has no Passed/Verified test row."
                )


def validate_dependency_graph(
    text: str,
    headings: list[Heading],
    parents: dict[str, Parent],
    errors: list[str],
) -> None:
    dependencies = section_text(text, headings, "Dependencies & Blockers")
    if not dependencies or DEPENDENCY_HEADER not in dependencies:
        return

    lines = dependencies.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.strip() == DEPENDENCY_HEADER),
        None,
    )
    if header_index is None:
        return
    if header_index + 1 >= len(lines) or not re.fullmatch(
        r"\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*){3}\|",
        lines[header_index + 1].strip(),
    ):
        errors.append("Task Dependency Graph table separator is missing or invalid.")
        return

    rows: dict[str, set[str]] = {}
    for relative_index, line in enumerate(
        lines[header_index + 2 :], start=header_index + 3
    ):
        stripped = line.strip()
        if not stripped:
            if rows:
                break
            continue
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = parse_markdown_table_row(stripped)
        if cells is None:
            errors.append(
                f"Task Dependency Graph line {relative_index}: invalid table row."
            )
            continue
        if len(cells) != 4:
            errors.append(
                f"Task Dependency Graph line {relative_index}: expected 4 table columns."
            )
            continue
        task_match = re.fullmatch(r"`(\d+\.0)`", cells[0])
        if not task_match:
            errors.append(
                f"Task Dependency Graph line {relative_index}: invalid Task Package ID."
            )
            continue
        task_id = task_match.group(1)
        if task_id in rows:
            errors.append(f"Task Dependency Graph defines {task_id} more than once.")
            continue
        rows[task_id] = set(CANONICAL_TASK_REF.findall(cells[1]))

    for task_id in sorted(set(rows) - set(parents)):
        errors.append(f"Task Dependency Graph references unknown parent {task_id}.")
    for task_id, parent in parents.items():
        if task_id not in rows:
            errors.append(f"Task Dependency Graph is missing parent {task_id}.")
            continue
        graph_dependencies = rows[task_id]
        parent_dependencies = set(parent.dependencies)
        if graph_dependencies != parent_dependencies:
            errors.append(
                f"{task_id}: Task Dependency Graph dependencies do not match "
                "the parent 依赖 field."
            )
        if task_id in graph_dependencies:
            errors.append(f"{task_id}: task must not depend on itself.")
        for dependency in graph_dependencies:
            if dependency not in parents:
                errors.append(
                    f"{task_id}: dependency references unknown parent {dependency}."
                )

    state: dict[str, int] = {}

    def visit(task_id: str) -> bool:
        if state.get(task_id) == 1:
            return True
        if state.get(task_id) == 2:
            return False
        state[task_id] = 1
        for dependency in rows.get(task_id, set()):
            if dependency in parents and visit(dependency):
                return True
        state[task_id] = 2
        return False

    if any(visit(task_id) for task_id in parents if state.get(task_id) is None):
        errors.append("Task Dependency Graph contains a dependency cycle.")


def parse_first_batch_assignments(
    plan: str,
    parents: dict[str, Parent],
    errors: list[str],
) -> dict[str, WorkerAssignment]:
    lines = plan.splitlines()
    header_index = next(
        (
            index
            for index, line in enumerate(lines)
            if line.strip()
            in {FIRST_BATCH_HEADER, FIRST_BATCH_HEADER_WITH_DO_NOT_TOUCH}
        ),
        None,
    )
    if header_index is None:
        errors.append("First Batch Worker Assignment table header is missing or invalid.")
        return {}
    has_do_not_touch = (
        lines[header_index].strip() == FIRST_BATCH_HEADER_WITH_DO_NOT_TOUCH
    )
    column_count = 8 if has_do_not_touch else 7
    if header_index + 1 >= len(lines) or not re.fullmatch(
        rf"\|\s*:?-{{3,}}:?\s*(?:\|\s*:?-{{3,}}:?\s*){{{column_count - 1}}}\|",
        lines[header_index + 1].strip(),
    ):
        errors.append("First Batch Worker Assignment table separator is missing or invalid.")
        return {}

    assignments: dict[str, WorkerAssignment] = {}
    task_owners: dict[str, str] = {}
    branch_owners: dict[str, str] = {}
    for relative_index, line in enumerate(
        lines[header_index + 2 :], start=header_index + 3
    ):
        stripped = line.strip()
        if not stripped:
            if assignments:
                break
            continue
        if not stripped.startswith("|"):
            if assignments:
                break
            continue
        cells = parse_markdown_table_row(stripped)
        if cells is None:
            errors.append(f"First Batch line {relative_index}: invalid table row.")
            continue
        if len(cells) != column_count:
            errors.append(
                f"First Batch line {relative_index}: expected {column_count} table columns."
            )
            continue

        worker = strip_ticks(cells[0])
        task_match = re.fullmatch(r"`(\d+\.0)`", cells[1])
        if not worker:
            errors.append(f"First Batch line {relative_index}: Worker is empty.")
            continue
        if not task_match:
            errors.append(
                f"First Batch line {relative_index}: invalid canonical Task Package ID."
            )
            continue
        if worker in assignments:
            errors.append(f"First Batch assigns {worker} more than once.")
            continue

        task_id = task_match.group(1)
        dependencies = normalize_markdown(cells[2])
        critical_path = normalize_markdown(cells[3])
        branch = strip_ticks(cells[4])
        allowed = normalize_markdown(cells[5])
        do_not_touch = normalize_markdown(cells[6]) if has_do_not_touch else None
        focused_validation = normalize_markdown(cells[7 if has_do_not_touch else 6])

        prior_task_owner = task_owners.get(task_id)
        if prior_task_owner is not None:
            errors.append(
                f"First Batch assigns Task Package {task_id} to both "
                f"{prior_task_owner} and {worker}."
            )
        else:
            task_owners[task_id] = worker

        if branch:
            if branch.casefold() == "main":
                errors.append(
                    f"First Batch {worker}: Branch must be an independent non-main branch."
                )
            prior_branch_owner = branch_owners.get(branch)
            if prior_branch_owner is not None:
                errors.append(
                    f"First Batch reuses branch {branch} for both "
                    f"{prior_branch_owner} and {worker}."
                )
            else:
                branch_owners[branch] = worker

        if task_id not in parents:
            errors.append(f"First Batch references unknown parent task {task_id}.")
        if re.search(r"(?:Satisfied|已满足)\s*:", dependencies, re.I):
            errors.append(
                f"First Batch {worker}: Dependencies must list direct dependencies "
                "without a Satisfied prefix."
            )
        parent = parents.get(task_id)
        if parent is not None:
            listed_dependencies = set(CANONICAL_TASK_REF.findall(cells[2]))
            if listed_dependencies != set(parent.dependencies):
                errors.append(
                    f"First Batch {worker}: Dependencies do not match parent {task_id}."
                )
            if not parent.dependencies and dependencies != "None":
                errors.append(
                    f"First Batch {worker}: dependency-free task must use exactly None."
                )
            if parent.state in {READY_FOR_REVIEW_STATE, APPROVED_STATE}:
                errors.append(
                    f"First Batch {worker}: parent {task_id} is already "
                    f"{parent.state} and is not runnable implementation work."
                )
            if (
                parent.prerequisite == "Required"
                and parent.prerequisite_state != "Provided"
            ):
                errors.append(
                    f"First Batch {worker}: required human prerequisite for "
                    f"{task_id} is still {parent.prerequisite_state}."
                )
            for dependency in parent.dependencies:
                dependency_parent = parents.get(dependency)
                if (
                    dependency_parent is not None
                    and dependency_parent.state != APPROVED_STATE
                ):
                    errors.append(
                        f"First Batch {worker}: dependency {dependency} is "
                        f"{dependency_parent.state}, not {APPROVED_STATE}."
                    )
        if not critical_path:
            errors.append(f"First Batch {worker}: Critical Path must be non-empty.")
        if not branch:
            errors.append(f"First Batch {worker}: Branch must be non-empty.")
        if not allowed:
            errors.append(
                f"First Batch {worker}: Allowed Files / Modules must be non-empty."
            )
        if has_do_not_touch and not do_not_touch:
            errors.append(
                f"First Batch {worker}: Do Not Touch must be non-empty when the column exists."
            )
        if not focused_validation:
            errors.append(f"First Batch {worker}: Focused Validation must be non-empty.")

        assignments[worker] = WorkerAssignment(
            worker=worker,
            task_id=task_id,
            dependencies=dependencies,
            branch=branch,
            allowed=allowed,
            do_not_touch=do_not_touch,
            focused_validation=focused_validation,
        )

    if not assignments:
        errors.append("First Batch Worker Assignment contains no Worker rows.")
    elif has_do_not_touch and all(
        assignment.do_not_touch == "None" for assignment in assignments.values()
    ):
        errors.append(
            "First Batch Do Not Touch column must be omitted when every Worker is None."
        )
    return assignments


def validate_execution_plan(
    text: str,
    headings: list[Heading],
    parents: dict[str, Parent],
    errors: list[str],
    warnings: list[str],
) -> None:
    plan = section_text(text, headings, "Execution Plan")
    if not plan:
        return

    if not any(
        "Main Manager" in line and "High" in line for line in plan.splitlines()
    ):
        errors.append("Execution Plan must assign Main Manager reasoning level High.")
    if not re.search(r"独立\s+branch", plan, re.I) or not re.search(
        r"独立\s+worktree", plan, re.I
    ):
        errors.append("Execution Plan must declare independent branch/worktree isolation.")
    if not re.search(r"Main Manager[^\n]*(?:唯一|only)[^\n]*(?:merge gate|merge)", plan, re.I):
        errors.append("Execution Plan must make Main Manager the unique merge gate.")
    operation_titles = (
        "User Start Here",
        "Main Manager Kickoff Prompt",
        "First Batch Worker Launch Prompts",
        "Worker Completion Handoff",
    )
    plan_h3_titles = [
        heading.title
        for heading in markdown_headings(plan)
        if heading.level == 3
    ]
    for title in operation_titles:
        count = plan_h3_titles.count(title)
        if count == 0:
            errors.append(f"Execution Plan is missing operator section: ### {title}")
        elif count > 1:
            errors.append(f"Execution Plan repeats operator section: ### {title}")

    ordered_titles = (
        "User Start Here",
        "Main Manager Kickoff Prompt",
        "First Batch Worker Assignment",
        "First Batch Worker Launch Prompts",
        "Worker Completion Handoff",
    )
    if all(title in plan_h3_titles for title in ordered_titles):
        indexes = [plan_h3_titles.index(title) for title in ordered_titles]
        if indexes != sorted(indexes):
            errors.append(
                "Execution Plan operator sections must follow the startup-to-handoff order."
            )

    user_start = heading_block(plan, 3, "User Start Here")
    if user_start:
        if len(re.findall(r"点击|\bclick\b", user_start, re.I)) > 1:
            warnings.append(
                "User Start Here contains UI click instructions; keep it UI-agnostic."
            )

    manager_block = heading_block(plan, 3, "Main Manager Kickoff Prompt")
    if manager_block:
        manager_fences = text_fences(manager_block)
        if len(manager_fences) != 1:
            errors.append(
                "Main Manager Kickoff Prompt must contain exactly one complete text code fence."
            )

    assignments = parse_first_batch_assignments(plan, parents, errors)

    launch_section = heading_block(plan, 3, "First Batch Worker Launch Prompts")
    launch_prompts: dict[str, tuple[str, str]] = {}
    if launch_section:
        for heading, block in child_blocks(launch_section, 4):
            match = re.fullmatch(r"(.+?)\s+[—–-]\s+(\d+\.0)", heading.title)
            if not match:
                errors.append(
                    f"Invalid Worker Launch Prompt heading: #### {heading.title}"
                )
                continue
            worker = strip_ticks(match.group(1).strip())
            task_id = match.group(2)
            if worker in launch_prompts:
                errors.append(f"Worker Launch Prompt repeats {worker}.")
                continue
            fences = text_fences(block)
            if len(fences) != 1:
                errors.append(
                    f"Worker Launch Prompt for {worker} must contain exactly one text code fence."
                )
                continue
            launch_prompts[worker] = (task_id, fences[0])

    for worker in sorted(set(launch_prompts) - set(assignments)):
        errors.append(
            f"Worker Launch Prompt exists for {worker}, but it is not in First Batch."
        )
    for worker, assignment in assignments.items():
        launch = launch_prompts.get(worker)
        if launch is None:
            errors.append(f"First Batch {worker} is missing its Worker Launch Prompt.")
            continue
        task_id, prompt = launch
        if task_id != assignment.task_id:
            errors.append(
                f"Worker Launch Prompt for {worker} references {task_id}, "
                f"not assigned task {assignment.task_id}."
            )
        if not prohibits_worker_main_operations(prompt):
            errors.append(
                f"Worker Launch Prompt for {worker} must prohibit operating, "
                "switching, modifying, merging, or pushing main."
            )
        prompt_plain = normalize_markdown(prompt)
        for field_name, expected in (
            ("Worker", assignment.worker),
            ("Task Package", assignment.task_id),
            ("Branch", assignment.branch),
            ("Dependencies", assignment.dependencies),
            ("Allowed Files / Modules", assignment.allowed),
            ("Focused Validation", assignment.focused_validation),
        ):
            if normalize_markdown(expected) not in prompt_plain:
                errors.append(
                    f"Worker Launch Prompt for {worker} does not match First Batch "
                    f"field {field_name}."
                )
        if (
            assignment.do_not_touch
            and assignment.do_not_touch != "None"
            and normalize_markdown(assignment.do_not_touch) not in prompt_plain
        ):
            errors.append(
                f"Worker Launch Prompt for {worker} does not match First Batch "
                "field Do Not Touch."
            )

    handoff_section = heading_block(plan, 3, "Worker Completion Handoff")
    handoff_prompts: dict[str, str] = {}
    if handoff_section:
        for heading, block in child_blocks(handoff_section, 4):
            match = re.fullmatch(r"(.+?)\s+Handoff to Main Manager", heading.title)
            if not match:
                errors.append(
                    f"Invalid Worker handoff heading: #### {heading.title}"
                )
                continue
            worker = strip_ticks(match.group(1).strip())
            if worker in handoff_prompts:
                errors.append(f"Worker handoff prompt repeats {worker}.")
                continue
            fences = text_fences(block)
            if len(fences) != 1:
                errors.append(
                    f"Worker handoff for {worker} must contain exactly one text code fence."
                )
                continue
            handoff_prompts[worker] = fences[0]

    for worker in sorted(set(handoff_prompts) - set(assignments)):
        errors.append(
            f"Worker handoff exists for {worker}, but it is not in First Batch."
        )
    for worker in assignments:
        prompt = handoff_prompts.get(worker)
        if prompt is None:
            errors.append(f"First Batch {worker} is missing its Manager handoff prompt.")
            continue
        if worker not in prompt:
            errors.append(f"Manager handoff prompt does not name {worker}.")

    plan_tasks = set(CANONICAL_TASK_REF.findall(plan))
    for task_id in sorted(plan_tasks - set(parents)):
        errors.append(f"Execution Plan references unknown parent task {task_id}.")

    if re.search(
        r"(?im)^(?:\s*[-*|]\s*)?(?:Model|模型)\s*[:：][^\n]*"
        r"(?:gpt[- ]?\d|claude|gemini|o[134](?:-|\b))|"
        r"^(?:\s*[-*|]\s*)?(?:Main Manager|Worker)[^\n]{0,80}"
        r"(?:model|模型)[^\n]*(?:gpt[- ]?\d|claude|gemini|o[134](?:-|\b))",
        plan,
    ):
        warnings.append(
            "Execution Plan names a specific model; use only Low/Middle/High reasoning levels."
        )


def task_prompt_blocks(
    text: str,
    errors: list[str],
) -> list[tuple[str, str, str]]:
    """Return ordered (task_id, title, block) entries from task-prompt.md."""
    result: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for heading, block in child_blocks(text, 2):
        if heading.title in {
            TASK_PROMPT_COMPLETED_TITLE,
            TASK_PROMPT_UNFINISHED_TITLE,
        }:
            continue
        match = TASK_PROMPT_HEADING.fullmatch(heading.title)
        if not match:
            errors.append(
                f"task-prompt.md has invalid level-2 heading: ## {heading.title}; "
                "expected ## Task X.X — <标题>."
            )
            continue
        task_id, title = match.groups()
        if task_id in seen:
            errors.append(f"task-prompt.md repeats Task {task_id}.")
            continue
        seen.add(task_id)
        result.append((task_id, title, block))
    return result


def validate_task_prompt(
    text: str,
    parents: dict[str, Parent],
    errors: list[str],
    warnings: list[str],
) -> None:
    headings = markdown_headings(text)
    h1_titles = [heading.title for heading in headings if heading.level == 1]
    if (
        len(h1_titles) != 1
        or not re.fullmatch(
            rf".+ — {re.escape(TASK_PROMPT_TITLE_SUFFIX)}",
            h1_titles[0],
        )
        or h1_titles[0].startswith("<")
    ):
        errors.append(
            "task-prompt.md must contain exactly one "
            "'# <项目名或域名> — Task Execution Prompts' title with a resolved name."
        )
    if TASK_PROMPT_ROLE not in text:
        errors.append(
            "task-prompt.md must state that it is the derived user Prompt entry, "
            "not the canonical task source."
        )
    if "docs/project/tasks.md" not in text:
        errors.append("task-prompt.md must name canonical docs/project/tasks.md.")

    if TASK_PROMPT_OBSOLETE_TOP_GUIDANCE.search(text):
        errors.append(
            "task-prompt.md must not contain Next task, Execution mode, "
            "Execution mode rationale, or usage guidance at the top."
        )

    prefix = text.split("## Task ", 1)[0]
    mode = (
        "Multi-Agent"
        if "Main Manager" in prefix
        or re.search(r"(?m)^(?:Worker|Branch|Execution batch):", text)
        else "Single-Agent"
    )

    entries = task_prompt_blocks(text, errors)
    ordered_ids = [task_id for task_id, _, _ in entries]
    incomplete = {
        task_id: parent
        for task_id, parent in parents.items()
        if parent.state != APPROVED_STATE
    }
    approved_ids = [
        task_id
        for task_id, parent in parents.items()
        if parent.state == APPROVED_STATE
    ]
    completed_headings = [
        heading
        for heading in headings
        if heading.level == 2 and heading.title == TASK_PROMPT_COMPLETED_TITLE
    ]
    unfinished_headings = [
        heading
        for heading in headings
        if heading.level == 2 and heading.title == TASK_PROMPT_UNFINISHED_TITLE
    ]
    if approved_ids:
        if len(completed_headings) != 1:
            errors.append(
                "task-prompt.md must contain exactly one '## 已完成' section "
                "when Approved parents exist."
            )
        else:
            completed_block = heading_block(text, 2, TASK_PROMPT_COMPLETED_TITLE)
            completed_lines = [
                line.strip()
                for line in completed_block.splitlines()[1:]
                if line.strip() and not line.lstrip().startswith("<!--")
            ]
            if len(completed_lines) != 1:
                errors.append(
                    "task-prompt.md '## 已完成' must contain exactly one "
                    "non-empty line of Task IDs."
                )
                completed_ids: list[str] = []
            else:
                completed_ids = completed_lines[0].split("、")
            if any(not re.fullmatch(r"\d+\.0", task_id) for task_id in completed_ids):
                errors.append(
                    "task-prompt.md '## 已完成' must use plain Task IDs "
                    "joined by Chinese delimiter '、'."
                )
            if len(completed_ids) != len(set(completed_ids)):
                errors.append("task-prompt.md '## 已完成' repeats a Task ID.")
            if set(completed_ids) != set(approved_ids):
                errors.append(
                    "task-prompt.md '## 已完成' does not match Approved parents; "
                    f"expected: {', '.join(approved_ids)}."
                )
    elif completed_headings:
        errors.append(
            "task-prompt.md must omit '## 已完成' when no Approved parents exist."
        )

    if incomplete:
        if len(unfinished_headings) != 1:
            errors.append(
                "task-prompt.md must contain exactly one '## 未完成' section "
                "when unfinished parents exist."
            )
        else:
            unfinished_block = heading_block(text, 2, TASK_PROMPT_UNFINISHED_TITLE)
            unfinished_lines = [
                line.strip()
                for line in unfinished_block.splitlines()[1:]
                if line.strip() and not line.lstrip().startswith("<!--")
            ]
            if len(unfinished_lines) != 1:
                errors.append(
                    "task-prompt.md '## 未完成' must contain exactly one "
                    "non-empty line of Task IDs."
                )
            else:
                unfinished_tokens = unfinished_lines[0].split("、")
                if any(
                    not re.fullmatch(r"❗?\d+\.0", token)
                    for token in unfinished_tokens
                ):
                    errors.append(
                        "task-prompt.md '## 未完成' must use Task IDs, optionally "
                        "prefixed by ❗, joined by Chinese delimiter '、'."
                    )
                unfinished_ids = [
                    token.removeprefix("❗") for token in unfinished_tokens
                ]
                if len(unfinished_ids) != len(set(unfinished_ids)):
                    errors.append("task-prompt.md '## 未完成' repeats a Task ID.")
                if unfinished_ids != ordered_ids:
                    errors.append(
                        "task-prompt.md '## 未完成' IDs and order must match the "
                        "Task sections below."
                    )
                if not any(token.startswith("❗") for token in unfinished_tokens):
                    errors.append(
                        "task-prompt.md '## 未完成' must mark at least one current "
                        "critical-path Task with ❗."
                    )
    elif unfinished_headings:
        errors.append(
            "task-prompt.md must omit '## 未完成' when no unfinished parents exist."
        )

    summary_positions = {
        heading.title: heading.start
        for heading in headings
        if heading.level == 2
        and heading.title in {
            TASK_PROMPT_COMPLETED_TITLE,
            TASK_PROMPT_UNFINISHED_TITLE,
        }
    }
    first_task_position = min(
        (
            heading.start
            for heading in headings
            if TASK_PROMPT_HEADING.fullmatch(heading.title)
        ),
        default=len(text),
    )
    if any(position > first_task_position for position in summary_positions.values()):
        errors.append("task-prompt.md summary sections must appear before Task sections.")
    if (
        TASK_PROMPT_COMPLETED_TITLE in summary_positions
        and TASK_PROMPT_UNFINISHED_TITLE in summary_positions
        and summary_positions[TASK_PROMPT_COMPLETED_TITLE]
        > summary_positions[TASK_PROMPT_UNFINISHED_TITLE]
    ):
        errors.append("task-prompt.md '## 已完成' must appear before '## 未完成'.")

    if incomplete:
        if not entries:
            errors.append("task-prompt.md contains no Task sections for unfinished parents.")
        else:
            first_id, _, _ = entries[0]
            parent = parents.get(first_id)
            if parent is not None:
                unresolved = [
                    dependency
                    for dependency in parent.dependencies
                    if dependency in parents
                    and parents[dependency].state != APPROVED_STATE
                ]
                if unresolved:
                    errors.append(
                        f"task-prompt.md first Task {first_id} has unfinished direct "
                        f"dependencies: {', '.join(unresolved)}."
                    )
    else:
        if entries:
            errors.append(
                "task-prompt.md must omit all Task sections when all parents are complete."
            )

    entry_ids = set(ordered_ids)
    missing = sorted(set(incomplete) - entry_ids)
    extra = sorted(entry_ids - set(incomplete))
    if missing:
        errors.append(
            "task-prompt.md is missing unfinished parent(s): " + ", ".join(missing)
        )
    if extra:
        errors.append(
            "task-prompt.md includes completed or unknown parent(s): " + ", ".join(extra)
        )

    positions = {task_id: index for index, task_id in enumerate(ordered_ids)}
    for task_id, parent in incomplete.items():
        if task_id not in positions:
            continue
        for dependency in parent.dependencies:
            dependency_parent = parents.get(dependency)
            if (
                dependency_parent is not None
                and dependency_parent.state != APPROVED_STATE
                and dependency in positions
                and positions[dependency] > positions[task_id]
            ):
                errors.append(
                    f"task-prompt.md order places Task {task_id} before unfinished "
                    f"dependency {dependency}."
                )

    for task_id, title, block in entries:
        parent = parents.get(task_id)
        if parent is None:
            continue
        if title != parent.title:
            errors.append(
                f"task-prompt.md Task {task_id} title does not match tasks.md."
            )

        block_headings = markdown_headings(block)
        bold_prompt_marker = re.search(
            r"(?m)^\*\*发给 Codex 的 Prompt\*\*[ \t]*$",
            block,
        )
        legacy_prompt_heading = next(
            (
                heading
                for heading in block_headings
                if heading.level == 3 and heading.title == "发给 Codex 的 Prompt"
            ),
            None,
        )
        if bold_prompt_marker is not None:
            prompt_marker_start = bold_prompt_marker.start()
        elif legacy_prompt_heading is not None:
            prompt_marker_start = legacy_prompt_heading.start
        else:
            prompt_marker_start = len(block)
            errors.append(f"Task {task_id} is missing its Codex Prompt label.")

        pre_prompt_block = block[:prompt_marker_start]
        explanation_start = re.search(r"(?m)^[-*]\s*现在：", pre_prompt_block)
        legacy_explanation_heading = next(
            (
                heading
                for heading in block_headings
                if heading.level == 3 and heading.title == "这项任务是做什么的"
            ),
            None,
        )
        metadata_end_candidates = [
            position
            for position in (
                explanation_start.start() if explanation_start is not None else None,
                legacy_explanation_heading.start
                if legacy_explanation_heading is not None
                else None,
            )
            if position is not None
        ]
        metadata_end = min(metadata_end_candidates, default=len(pre_prompt_block))
        metadata_block = pre_prompt_block[:metadata_end]
        metadata, metadata_duplicates = parse_fields(metadata_block)
        for field_name in metadata_duplicates:
            errors.append(
                f"Task {task_id} repeats prompt metadata field '{field_name}'."
            )
        for field_name in ("依赖",):
            if field_name not in metadata or not metadata[field_name].strip():
                errors.append(
                    f"Task {task_id} is missing prompt metadata '{field_name}'."
                )

        dependency_display = metadata.get("依赖", "").strip()
        if "当前是否可以开始" in metadata:
            errors.append(
                f"Task {task_id} must not include '当前是否可以开始'; "
                "show only the dependency IDs."
            )

        parent_fields, _ = parse_fields(parent.block)
        blocker_refs = set(
            re.findall(r"\bBLOCKED-\d{3,}\b", parent_fields.get("依赖", ""))
        )
        displayed_dependencies = set(
            re.findall(r"(?<![\w.-])(\d+\.0)(?![\w.-])", dependency_display)
        )
        displayed_blockers = set(
            re.findall(r"\bBLOCKED-\d{3,}\b", dependency_display)
        )
        expected_dependencies = set(parent.dependencies)
        if displayed_dependencies != expected_dependencies:
            errors.append(
                f"Task {task_id} dependency display does not match tasks.md; "
                f"expected {', '.join(sorted(expected_dependencies)) or 'none'}."
            )
        if displayed_blockers != blocker_refs:
            errors.append(
                f"Task {task_id} blocker display does not match tasks.md; "
                f"expected {', '.join(sorted(blocker_refs)) or 'none'}."
            )
        if not expected_dependencies and not blocker_refs:
            if strip_ticks(dependency_display) != "无":
                errors.append(f"Task {task_id} without dependencies must display '依赖：无'.")
        else:
            allowed_text = "、".join(
                [*parent.dependencies, *sorted(blocker_refs)]
            )
            if strip_ticks(dependency_display) != allowed_text:
                errors.append(
                    f"Task {task_id} dependency display must contain only IDs "
                    f"separated by '、': {allowed_text}."
                )

        explanation_body = (
            pre_prompt_block[explanation_start.start() :].strip()
            if explanation_start is not None
            else ""
        )
        explanation_lines = [
            line.strip()
            for line in explanation_body.splitlines()
            if line.strip() and not line.lstrip().startswith("<!--")
        ]
        if not 3 <= len(explanation_lines) <= 6:
            errors.append(
                f"Task {task_id} plain-language explanation must be about 3-6 "
                "non-empty lines."
            )
        for label in ("现在：", "这次：", "完成后："):
            if not any(
                re.match(rf"^[-*]\s*{re.escape(label)}", line)
                for line in explanation_lines
            ):
                errors.append(
                    f"Task {task_id} plain-language explanation is missing '{label}'."
                )
        if re.search(
            r"(?m)^- (?:任务类型|状态|验收方式|来源|目标|边界 / 不做|"
            r"依赖|子项|涉及文件|AI 验证)：",
            explanation_body,
        ):
            errors.append(
                f"Task {task_id} explanation must not copy technical tasks.md fields."
            )
        if re.search(r"\b(?:Task\s+\d+\.0|T-\d+|G-\d+)\b|AI 验证", explanation_body):
            errors.append(
                f"Task {task_id} explanation must not expose Task/T/G IDs or "
                "verification terminology to the user."
            )
        if TASK_PROMPT_VAGUE_EXPLANATION.search(explanation_body):
            errors.append(
                f"Task {task_id} explanation uses vague engineering language; "
                "name the real page, user action, problem, and visible result."
            )
        if not re.search(r"用户|访客|客户|管理员|你|系统", explanation_body):
            errors.append(
                f"Task {task_id} explanation must name who sees the change or "
                "how the system behaves."
            )
        if "```" in explanation_body or "~~~" in explanation_body:
            errors.append(f"Task {task_id} explanation must not contain code fences.")

        prompt_section = block[prompt_marker_start:]
        prompts = text_fences(prompt_section)
        if len(prompts) != 1:
            errors.append(
                f"Task {task_id} must contain exactly one complete text Prompt fence."
            )
            continue
        prompt = prompts[0]
        prompt_issues: list[str] = []
        if task_id not in prompt:
            prompt_issues.append("task ID")
        if "docs/project/tasks.md" not in prompt:
            prompt_issues.append("canonical tasks.md path")
        for description, pattern in (
            ("read complete task", r"读取[^\n。]*完整(?:任务|范围)"),
            ("inspect current implementation", r"检查当前"),
            ("task verification", r"任务要求[^。\n]*验证|T-\*[^\n。]*验证"),
            ("commit instruction", r"提交|commit"),
            ("task-prefixed commit", rf"以\s*{re.escape(task_id)}\s*开头"),
        ):
            if not re.search(pattern, prompt, re.I):
                prompt_issues.append(description)

        if re.search(
            r"(?:然后|完成后)停止|不要开始下一个父任务包|"
            r"未经用户明确授权[^。；\n]*(?:不创建|不要创建|不提交|不要提交)[^。；\n]*commit",
            prompt,
            re.I,
        ):
            prompt_issues.append("unexpected stop or denied commit authorization")

        if mode == "Single-Agent":
            if "docs/project/task-prompt.md" not in prompt:
                prompt_issues.append("task-prompt.md synchronization")
        elif mode == "Multi-Agent":
            if not re.search(r"\bWorker\b", block):
                prompt_issues.append("Worker assignment")
            if not re.search(r"\bBranch\b", block):
                prompt_issues.append("branch assignment")
            if not prohibits_worker_main_operations(prompt):
                prompt_issues.append("main-operation prohibition")
            if not re.search(
                r"不得修改[^。\n]*docs/project/tasks\.md[^。\n]*"
                r"docs/project/task-prompt\.md|"
                r"不得修改[^。\n]*(?:两份任务文档|任务文档)",
                prompt,
            ):
                prompt_issues.append("shared task-document prohibition")
            if not re.search(r"Completion Report", prompt, re.I):
                prompt_issues.append("Completion Report")

        if prompt_issues:
            errors.append(
                f"Task {task_id} Prompt is incomplete or invalid; review "
                f"{', '.join(prompt_issues)}."
            )

    if mode == "Multi-Agent":
        if "Main Manager" not in prefix or len(text_fences(prefix)) != 1:
            errors.append(
                "Multi-Agent task-prompt.md must contain one complete Main Manager "
                "Kickoff Prompt before the first Task section."
            )
    elif mode == "Single-Agent" and re.search(
        r"(?m)^(?:Worker|Branch|Execution batch):", text
    ):
        errors.append(
            "Single-Agent task-prompt.md must not contain Worker, Branch, or batch metadata."
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate canonical docs/project/tasks.md and derived "
            "docs/project/task-prompt.md generated by $generate-tasks."
        )
    )
    parser.add_argument("tasks_file", type=Path)
    parser.add_argument(
        "task_prompt_file",
        type=Path,
        nargs="?",
        help=(
            "Derived task-prompt.md path. Defaults to a sibling of tasks_file."
        ),
    )
    args = parser.parse_args()
    task_prompt_file = args.task_prompt_file or args.tasks_file.with_name(
        "task-prompt.md"
    )

    errors: list[str] = []
    warnings: list[str] = []

    if not args.tasks_file.exists():
        print(f"ERROR: file not found: {args.tasks_file}")
        return 2
    if not args.tasks_file.is_file():
        print(f"ERROR: not a file: {args.tasks_file}")
        return 2
    if not task_prompt_file.exists():
        print(f"ERROR: file not found: {task_prompt_file}")
        return 2
    if not task_prompt_file.is_file():
        print(f"ERROR: not a file: {task_prompt_file}")
        return 2

    raw = args.tasks_file.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("File contains a UTF-8 BOM.")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"ERROR: file is not valid UTF-8: {exc}")
        return 2

    secret_line = possible_secret_line(text)
    if secret_line is not None:
        errors.append(
            f"Possible real secret, credential, private key, code, or database URL "
            f"detected near line {secret_line}; value is intentionally not echoed."
        )
    for field_name in LEGACY_FIELDS:
        if re.search(rf"^- {re.escape(field_name)}：", text, re.M):
            errors.append(f"Legacy/conflicting field remains: {field_name}")

    headings = markdown_headings(text)
    validate_sections(text, headings, errors)
    validate_traceability_table(text, headings, errors)

    task_section = section_text(text, headings, "Task Packages")
    parents: dict[str, Parent] = {}
    gates: dict[str, Gate] = {}
    blocked_tasks: dict[str, BlockedTask] = {}
    parent_numbers: list[int] = []

    blocker_section = section_text(text, headings, "Dependencies & Blockers")
    for heading, block in h3_blocks(blocker_section):
        blocked_task = validate_blocked_task(heading, block, errors)
        if blocked_task is not None:
            if blocked_task.blocker_id in blocked_tasks:
                errors.append(
                    f"Duplicate Blocked Task heading: {blocked_task.blocker_id}"
                )
            else:
                blocked_tasks[blocked_task.blocker_id] = blocked_task
        elif heading.title.startswith("BLOCKED-"):
            errors.append(
                f"Invalid Blocked Task heading: ### {heading.title}"
            )

    for heading, block in h3_blocks(task_section):
        parent = validate_parent(
            heading,
            block,
            errors,
            warnings,
        )
        if parent is not None:
            if parent.task_id in parents:
                errors.append(f"Duplicate parent task heading: {parent.task_id}")
            else:
                parents[parent.task_id] = parent
                parent_numbers.append(int(parent.task_id.split(".")[0]))
            continue

        gate = validate_gate(heading, block, errors, warnings)
        if gate is not None:
            if gate.gate_id in gates:
                errors.append(f"Duplicate human checkpoint heading: {gate.gate_id}")
            else:
                gates[gate.gate_id] = gate
            continue

        if heading.title.startswith("["):
            errors.append(
                f"Invalid task/checkpoint heading in Task Packages: ### {heading.title}"
            )
        elif heading.title.startswith("BLOCKED-"):
            errors.append(
                f"Blocked Task must be placed in Dependencies & Blockers: "
                f"### {heading.title}"
            )

    if not parents and not blocked_tasks:
        errors.append(
            "No canonical parent tasks or Blocked Tasks were found."
        )
    if parent_numbers != sorted(parent_numbers):
        errors.append("Parent task numbers must remain in ascending order.")
    if len(parent_numbers) != len(set(parent_numbers)):
        errors.append("Parent task numbers must be unique.")

    validate_dependency_graph(text, headings, parents, errors)

    tests = parse_verification_rows(
        text,
        headings,
        errors,
        require_rows=bool(parents),
    )
    validate_cross_references(parents, gates, tests, errors, warnings)

    prompt_raw = task_prompt_file.read_bytes()
    if prompt_raw.startswith(b"\xef\xbb\xbf"):
        errors.append("task-prompt.md contains a UTF-8 BOM.")
    try:
        prompt_text = prompt_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"ERROR: task-prompt.md is not valid UTF-8: {exc}")
        return 2
    prompt_secret_line = possible_secret_line(prompt_text)
    if prompt_secret_line is not None:
        errors.append(
            "Possible real secret, credential, private key, code, or database URL "
            f"detected in task-prompt.md near line {prompt_secret_line}; value is "
            "intentionally not echoed."
        )
    validate_task_prompt(prompt_text, parents, errors, warnings)

    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
        return 1

    print("VALIDATION PASSED")
    print(f"Parent tasks: {len(parents)}")
    print(f"Blocked tasks: {len(blocked_tasks)}")
    print(f"Human checkpoints: {len(gates)}")
    print(f"Verification tests: {len(tests)}")
    print(f"Prompt tasks: {sum(1 for parent in parents.values() if parent.state != APPROVED_STATE)}")
    for item in warnings:
        print(f"WARNING: {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
