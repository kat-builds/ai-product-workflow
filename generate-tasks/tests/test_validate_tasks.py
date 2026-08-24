from __future__ import annotations

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
- 这次：Codex 会把填写、提交、成功结果和失败提示连接起来。
- 完成后：用户可以完成提交，成功时看到结果，失败时知道发生了什么。"""
    return f"""## Task {task_id} — {title}

- 依赖：{dependency}

{explanation}

**发给 Codex 的 Prompt**

```text
{opener} docs/project/tasks.md 中的 Task {task_id}，先读取完整任务并检查当前实现，按任务要求完成实现和验证。{extra_prompt}完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 {task_id} 开头的 commit。
```
"""


def prompt_document(
    *entries: str,
    completed_ids: tuple[str, ...] = (),
) -> str:
    completed = ""
    if completed_ids:
        completed = "## 已完成\n" + "、".join(completed_ids) + "\n\n"
    return f"""# Task Execution Prompts

Last updated: 2026-08-14

> 文档角色说明：本文件是给用户复制 Prompt 的派生执行入口，不是任务定义。任务范围以 docs/project/tasks.md 为准。

{completed}{''.join(entries)}"""


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
            "**发给 Codex 的 Prompt**",
            "### 发给 Codex 的 Prompt",
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
        self.assertTrue(any("must contain only IDs" in error for error in errors))

    def test_rejects_vague_engineering_explanation(self) -> None:
        parents = {"1.0": make_parent("1.0", title="Example")}
        text = prompt_document(
            task_prompt_entry(
                "1.0",
                "Example",
                explanation="""- 现在：这部分能力还没有形成完整结果。
- 这次：Codex 会补齐功能并完成客观验证。
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


class CanonicalTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tasks_template = Path("assets/tasks-template.md").read_text(
            encoding="utf-8"
        )
        cls.prompt_template = Path("assets/task-prompt-template.md").read_text(
            encoding="utf-8"
        )

    def test_tasks_template_does_not_embed_execution_prompts(self) -> None:
        self.assertNotIn("- 执行 Prompt：", self.tasks_template)
        self.assertNotIn("- Stop Condition：", self.tasks_template)
        self.assertNotIn("## Execution Plan", self.tasks_template)

    def test_prompt_template_has_required_user_entry_structure(self) -> None:
        self.assertNotIn("Next task:", self.prompt_template)
        self.assertNotIn("Execution mode:", self.prompt_template)
        self.assertNotIn("使用方法：", self.prompt_template)
        self.assertIn("## Task 1.0 —", self.prompt_template)
        self.assertNotIn("当前是否可以开始：", self.prompt_template)
        self.assertIn("依赖：", self.prompt_template)
        self.assertIn("- 依赖：1.0", self.prompt_template)
        self.assertNotIn("### 这项任务是做什么的", self.prompt_template)
        self.assertNotIn("### 发给 Codex 的 Prompt", self.prompt_template)
        self.assertIn("**发给 Codex 的 Prompt**", self.prompt_template)
        self.assertIn("先读取完整任务并检查当前实现", self.prompt_template)


if __name__ == "__main__":
    unittest.main()
