from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts import validate_tasks as validator


def make_parent(
    task_id: str,
    *,
    title: str | None = None,
    state: str = validator.PENDING_STATE,
    dependencies: tuple[str, ...] = (),
    acceptance: str = "AI 验证",
    prerequisite: str = "None",
    prerequisite_state: str = "Not required",
    gate_ref: str | None = None,
) -> validator.Parent:
    return validator.Parent(
        task_id=task_id,
        title=title or f"Task {task_id}",
        checkbox="x" if state == validator.APPROVED_STATE else " ",
        state=state,
        acceptance=acceptance,
        prerequisite=prerequisite,
        prerequisite_state=prerequisite_state,
        real_integration="Not required",
        dependencies=dependencies,
        test_refs=("T-001",),
        gate_ref=gate_ref,
        block="",
    )


def parent_block(extra: str = "") -> str:
    return f"""- 任务类型：`Formal Task Package`
- 状态：`⬜ Pending`
- 验收方式：`AI 验证`
- 人工前置：`None`
- 前置状态：`Not required`
- 真实联调：`Not required`
- 来源：`FR-001`
- 目标：完成当前任务。
- 边界 / 不做：不处理其他任务。
- 依赖：`None`
- 子项：
  - 1.1 完成工作
- 涉及文件：
  - `path/a`
- AI 验证：`T-001`
{extra}"""


def task_prompt_entry(
    task_id: str,
    title: str,
    *,
    opener: str = "执行",
    extra_prompt: str = "",
    dependency: str = "无",
    explanation: str | None = None,
) -> str:
    explanation = explanation or """- 现在：用户还不能从页面完整提交操作，也看不到明确结果。
- 这次：coding agent 会把填写、提交、成功结果和失败提示连接起来。
- 完成后：用户可以完成提交，成功时看到结果，失败时知道发生了什么。"""
    return f"""## Task {task_id} — {title}

- 依赖：{dependency}

{explanation}

**发给 coding agent 的 Prompt**

```text
{opener} docs/project/tasks.md 中的 Task {task_id}，先读取完整任务并检查当前实现，按任务要求完成实现和验证。{extra_prompt}完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 {task_id} 开头的 commit。
```
"""


def prompt_document(
    *entries: str,
    completed_ids: tuple[str, ...] = (),
    unfinished_ids: tuple[str, ...] | None = None,
    important_ids: tuple[str, ...] = (),
    title: str = "Example Project — Task Execution Prompts",
) -> str:
    completed = ""
    if completed_ids:
        completed = "## 已完成\n" + "、".join(completed_ids) + "\n\n"
    if unfinished_ids is None:
        unfinished_ids = tuple(
            match.group(1)
            for entry in entries
            if (match := re.search(r"^## Task (\d+\.0) —", entry))
        )
    unfinished = ""
    if unfinished_ids:
        unfinished = (
            "## 未完成\n"
            + "、".join(
                f"❗{task_id}" if task_id in important_ids else task_id
                for task_id in unfinished_ids
            )
            + "\n\n"
        )
        if not important_ids:
            unfinished = unfinished.replace(
                unfinished_ids[0],
                f"❗{unfinished_ids[0]}",
                1,
            )
    return f"""# {title}

Last updated: 2026-08-14

> 本文件仅供复制 Prompt；任务定义以 docs/project/tasks.md 为准。

{completed}{unfinished}{''.join(entries)}"""


class ParentContractTests(unittest.TestCase):
    def validate(self, block: str) -> list[str]:
        errors: list[str] = []
        warnings: list[str] = []
        validator.validate_parent(
            validator.Heading(3, "[ ] 1.0 Example", 0, 0),
            block,
            errors,
            warnings,
        )
        return errors

    def test_accepts_parent_without_operational_field(self) -> None:
        self.assertEqual(self.validate(parent_block()), [])

    def test_rejects_execution_prompt_in_tasks_parent(self) -> None:
        errors = self.validate(
            parent_block(
                "- 执行 Prompt：\n  ```text\n开始 Task 1.0。\n  ```"
            )
        )
        self.assertTrue(any("must not contain '执行 Prompt'" in error for error in errors))

    def test_rejects_stop_condition_in_tasks_parent(self) -> None:
        errors = self.validate(parent_block("- Stop Condition：完成后交接。"))
        self.assertTrue(any("must not contain 'Stop Condition'" in error for error in errors))


class TaskPromptValidationTests(unittest.TestCase):
    def validate(
        self,
        text: str,
        parents: dict[str, validator.Parent],
    ) -> list[str]:
        errors: list[str] = []
        warnings: list[str] = []
        validator.validate_task_prompt(text, parents, errors, warnings)
        return errors

    def test_accepts_complete_single_agent_prompt_document(self) -> None:
        parents = {"1.0": make_parent("1.0", title="Example")}
        text = prompt_document(
            task_prompt_entry("1.0", "Example"),
        )
        self.assertEqual(self.validate(text, parents), [])

    def test_rejects_obsolete_top_guidance(self) -> None:
        parents = {"1.0": make_parent("1.0", title="First")}
        text = prompt_document(
            task_prompt_entry("1.0", "First"),
        ).replace(
            "Last updated: 2026-08-14",
            "Last updated: 2026-08-14\n\nNext task: Task 1.0 — First",
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("must not contain Next task" in error for error in errors))

    def test_rejects_title_without_project_name_or_domain(self) -> None:
        parents = {"1.0": make_parent("1.0", title="First")}
        text = prompt_document(
            task_prompt_entry("1.0", "First"),
            title="Task Execution Prompts",
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("Project name or domain" in error for error in errors))

    def test_accepts_unfinished_summary_in_prompt_order_with_critical_mark(self) -> None:
        parents = {
            "1.0": make_parent("1.0", title="First"),
            "2.0": make_parent("2.0", title="Second"),
        }
        text = prompt_document(
            task_prompt_entry("2.0", "Second"),
            task_prompt_entry("1.0", "First"),
            important_ids=("2.0",),
        )
        self.assertEqual(self.validate(text, parents), [])

    def test_rejects_unfinished_summary_out_of_prompt_order(self) -> None:
        parents = {
            "1.0": make_parent("1.0", title="First"),
            "2.0": make_parent("2.0", title="Second"),
        }
        text = prompt_document(
            task_prompt_entry("2.0", "Second"),
            task_prompt_entry("1.0", "First"),
            unfinished_ids=("1.0", "2.0"),
            important_ids=("2.0",),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("IDs and order must match" in error for error in errors))

    def test_rejects_unfinished_summary_without_critical_mark(self) -> None:
        parents = {"1.0": make_parent("1.0", title="First")}
        text = prompt_document(
            task_prompt_entry("1.0", "First"),
        ).replace("❗1.0", "1.0", 1)
        errors = self.validate(text, parents)
        self.assertTrue(any("critical-path Task" in error for error in errors))

    def test_rejects_missing_unfinished_summary(self) -> None:
        parents = {"1.0": make_parent("1.0", title="First")}
        text = prompt_document(
            task_prompt_entry("1.0", "First"),
        ).replace("## 未完成\n❗1.0\n\n", "", 1)
        errors = self.validate(text, parents)
        self.assertTrue(any("exactly one '## 未完成'" in error for error in errors))

    def test_rejects_dependent_before_unfinished_dependency(self) -> None:
        parents = {
            "1.0": make_parent("1.0", title="Foundation"),
            "2.0": make_parent(
                "2.0",
                title="Feature",
                dependencies=("1.0",),
            ),
        }
        text = prompt_document(
            task_prompt_entry(
                "2.0",
                "Feature",
                dependency="1.0",
            ),
            task_prompt_entry("1.0", "Foundation"),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("first Task 2.0" in error for error in errors))
        self.assertTrue(any("before unfinished dependency" in error for error in errors))

    def test_accepts_dependency_id_only(self) -> None:
        parents = {
            "1.0": make_parent("1.0", title="Foundation"),
            "2.0": make_parent(
                "2.0",
                title="Feature",
                dependencies=("1.0",),
            ),
        }
        text = prompt_document(
            task_prompt_entry("1.0", "Foundation"),
            task_prompt_entry(
                "2.0",
                "Feature",
                dependency="1.0",
            ),
        )
        self.assertEqual(self.validate(text, parents), [])

    def test_accepts_legacy_prompt_headings_during_incremental_refresh(self) -> None:
        parents = {"1.0": make_parent("1.0", title="Example")}
        entry = task_prompt_entry("1.0", "Example").replace(
            "- 现在：",
            "### 这项任务是做什么的\n\n- 现在：",
        ).replace(
            "**发给 coding agent 的 Prompt**",
            "### 发给 coding agent 的 Prompt",
        )
        text = prompt_document(entry)
        self.assertEqual(self.validate(text, parents), [])

    def test_rejects_incorrect_dependency_display(self) -> None:
        parents = {
            "1.0": make_parent("1.0", title="Foundation"),
            "2.0": make_parent(
                "2.0",
                title="Feature",
                dependencies=("1.0",),
            ),
        }
        text = prompt_document(
            task_prompt_entry("1.0", "Foundation"),
            task_prompt_entry("2.0", "Feature"),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("dependency display does not match" in error for error in errors))

    def test_rejects_dependency_explanation(self) -> None:
        parents = {
            "1.0": make_parent("1.0", title="Foundation"),
            "2.0": make_parent(
                "2.0",
                title="Feature",
                dependencies=("1.0",),
            ),
        }
        text = prompt_document(
            task_prompt_entry("1.0", "Foundation"),
            task_prompt_entry(
                "2.0",
                "Feature",
                dependency="Task 1.0 — Foundation — 未完成",
            ),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("must contain only" in error for error in errors))

    def test_rejects_vague_engineering_explanation(self) -> None:
        parents = {"1.0": make_parent("1.0", title="Example")}
        text = prompt_document(
            task_prompt_entry(
                "1.0",
                "Example",
                explanation="""- 现在：这部分能力还没有形成完整结果。
- 这次：coding agent 会补齐功能并完成客观验证。
- 完成后：用户会看到可核对的验证结果。""",
            ),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("vague engineering language" in error for error in errors))

    def test_rejects_completed_parent_in_prompt_list(self) -> None:
        parents = {
            "1.0": make_parent(
                "1.0",
                title="Done",
                state=validator.APPROVED_STATE,
            )
        }
        text = prompt_document(
            task_prompt_entry("1.0", "Done"),
            completed_ids=("1.0",),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("omit all Task sections" in error for error in errors))
        self.assertTrue(any("completed or unknown" in error for error in errors))

    def test_accepts_all_complete_document_without_task_sections(self) -> None:
        parents = {
            "1.0": make_parent(
                "1.0",
                title="Done",
                state=validator.APPROVED_STATE,
            )
        }
        text = prompt_document(
            completed_ids=("1.0",),
        )
        self.assertEqual(self.validate(text, parents), [])

    def test_accepts_completed_ids_in_actual_completion_order(self) -> None:
        parents = {
            "1.0": make_parent("1.0", state=validator.APPROVED_STATE),
            "2.0": make_parent("2.0", state=validator.APPROVED_STATE),
        }
        text = prompt_document(completed_ids=("2.0", "1.0"))
        self.assertEqual(self.validate(text, parents), [])

    def test_rejects_completed_ids_on_separate_lines(self) -> None:
        parents = {
            "1.0": make_parent("1.0", state=validator.APPROVED_STATE),
            "2.0": make_parent("2.0", state=validator.APPROVED_STATE),
        }
        text = prompt_document(completed_ids=("1.0", "2.0")).replace(
            "1.0、2.0",
            "1.0\n2.0",
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("exactly one non-empty line" in error for error in errors))

    def test_rejects_completed_section_that_does_not_match_tasks(self) -> None:
        parents = {
            "1.0": make_parent(
                "1.0",
                title="Done",
                state=validator.APPROVED_STATE,
            )
        }
        text = prompt_document(
            completed_ids=("2.0",),
        )
        errors = self.validate(text, parents)
        self.assertTrue(any("does not match Approved parents" in error for error in errors))

    def test_accepts_short_prompt_for_in_progress_parent(self) -> None:
        parents = {
            "1.0": make_parent(
                "1.0",
                title="Resume",
                state=validator.IN_PROGRESS_STATE,
            )
        }
        text = prompt_document(
            task_prompt_entry("1.0", "Resume"),
        )
        self.assertEqual(self.validate(text, parents), [])


class LocaleNormalizationTests(unittest.TestCase):
    def test_normalizes_english_parent_fields(self) -> None:
        text = """- Task Type: `Formal Task Package`
- Status: `⬜ Pending`
- Acceptance: `AI verification`
- Human Prerequisite: `None`
- Prerequisite Status: `Not required`
- Real Integration: `Not required`
- Source: `FR-001`
- Goal: Example
- Boundary / Non-goals: Example
- Dependencies: `None`
- Subtasks:
  - 1.1 Example
- Files:
  - `path/a`
- AI Verification: `T-001`
"""
        normalized = validator.normalize_localized_task_text(text)
        self.assertRegex(normalized, r"- 任务类型：\s*`Formal Task Package`")
        self.assertRegex(normalized, r"- 验收方式：\s*`AI 验证`")
        self.assertRegex(normalized, r"- 依赖：\s*`无`")

    def test_normalizes_english_prompt_labels(self) -> None:
        text = """## Unfinished

❗1.0

## Task 1.0 — Example

- Dependencies: None
- Conflicts: None

- Now: the user cannot finish the action.
- This task: the coding agent connects the action.
- After: the user can finish the action.

**Prompt for coding agent**
"""
        normalized = validator.normalize_localized_task_text(text)
        self.assertIn("## 未完成", normalized)
        self.assertRegex(normalized, r"- 依赖：\s*无")
        self.assertRegex(normalized, r"- 冲突：\s*无")
        self.assertRegex(normalized, r"- 现在：\s*")
        self.assertIn("**发给 coding agent 的 Prompt**", normalized)


class CanonicalTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tasks_template = Path("assets/tasks-template.md").read_text(
            encoding="utf-8"
        )
        cls.prompt_template = Path("assets/task-prompt-template.md").read_text(
            encoding="utf-8"
        )

    def test_templates_are_english_source_documents(self) -> None:
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", self.tasks_template))
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", self.prompt_template))

    def test_tasks_template_does_not_embed_execution_prompts(self) -> None:
        self.assertNotIn("- Execution Prompt:", self.tasks_template)
        self.assertNotIn("- Stop Condition：", self.tasks_template)
        self.assertNotIn("## Execution Plan", self.tasks_template)

    def test_prompt_template_has_required_user_entry_structure(self) -> None:
        self.assertNotIn("Next task:", self.prompt_template)
        self.assertNotIn("Execution mode:", self.prompt_template)
        self.assertNotIn("使用方法：", self.prompt_template)
        self.assertIn("# <Project name or domain> — Task Execution Prompts", self.prompt_template)
        self.assertIn("## Completed", self.prompt_template)
        self.assertIn("## Unfinished", self.prompt_template)
        self.assertIn("❗2.0, 3.0", self.prompt_template)
        self.assertIn("## Task 2.0 —", self.prompt_template)
        self.assertNotIn("当前是否可以开始：", self.prompt_template)
        self.assertIn("Dependencies:", self.prompt_template)
        self.assertIn("- Dependencies: 2.0", self.prompt_template)
        self.assertNotIn("### 这项任务是做什么的", self.prompt_template)
        self.assertNotIn("### Prompt for coding agent", self.prompt_template)
        self.assertIn("**Prompt for coding agent**", self.prompt_template)
        self.assertIn("Read the complete parent task and inspect the current implementation first", self.prompt_template)


if __name__ == "__main__":
    unittest.main()
