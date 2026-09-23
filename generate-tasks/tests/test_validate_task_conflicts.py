#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_task_conflicts.py"
SPEC = importlib.util.spec_from_file_location("validate_task_conflicts", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def prompt(task_1_conflicts: str, task_2_conflicts: str) -> str:
    return f"""# demo — Task Execution Prompts

## 未完成

1.0、2.0

## Task 1.0 — First

- 依赖：无
- 冲突：{task_1_conflicts}

- 现在：x
- 这次：x
- 完成后：x

**发给 Codex 的 Prompt**

```text
x
```

## Task 2.0 — Second

- 依赖：无
- 冲突：{task_2_conflicts}

- 现在：x
- 这次：x
- 完成后：x

**发给 Codex 的 Prompt**

```text
x
```
"""


class ValidateTaskConflictsTests(unittest.TestCase):
    def test_accepts_no_conflicts(self) -> None:
        self.assertEqual(MODULE.validate(prompt("无", "无")), [])

    def test_accepts_symmetric_conflict(self) -> None:
        self.assertEqual(MODULE.validate(prompt("2.0", "1.0")), [])

    def test_rejects_missing_conflict_field(self) -> None:
        text = prompt("无", "无").replace("- 冲突：无\n", "", 1)
        errors = MODULE.validate(text)
        self.assertTrue(any("exactly one" in error for error in errors))

    def test_rejects_unknown_task(self) -> None:
        errors = MODULE.validate(prompt("3.0", "无"))
        self.assertTrue(any("non-current Task IDs" in error for error in errors))

    def test_rejects_asymmetric_conflict(self) -> None:
        errors = MODULE.validate(prompt("2.0", "无"))
        self.assertTrue(any("Conflict must be symmetric" in error for error in errors))

    def test_rejects_self_conflict(self) -> None:
        errors = MODULE.validate(prompt("1.0", "无"))
        self.assertTrue(any("must not conflict with itself" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
