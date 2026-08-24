# Task Execution Prompts

Last updated: YYYY-MM-DD

> 文档角色说明：本文件是给用户复制 Prompt 的派生执行入口，不是任务定义或第二份 source of truth。任务范围、依赖、状态和验收始终以 `docs/project/tasks.md` 为准；两者冲突时先重新运行 `$generate-tasks`。

<!-- 若存在 Approved parent，在第一个 Task 小节前输出“已完成”二级标题，下面只写一行 Task ID，按实际完成时间用中文顿号连接，新完成的追加在最后；没有时省略。 -->

<!-- 只列未完成 parent。按推荐实际执行顺序排列，不按 Task ID 排序。Single-Agent 使用线性顺序；Multi-Agent 可在 Task 标题下增加 `Execution batch` 和 Worker 元数据。 -->

## Task 1.0 — 完成可客观验证的结果

- 依赖：无

- 现在：用户还不能从页面完整提交这项操作，提交后也看不到明确结果。
- 这次：Codex 会把填写内容、提交操作、成功结果和失败提示连接起来。
- 完成后：用户可以完成提交；成功时能看到结果，失败时也知道发生了什么。

**发给 Codex 的 Prompt**

```text
执行 docs/project/tasks.md 中的 Task 1.0，先读取完整任务并检查当前实现，按任务要求完成实现和验证。完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 1.0 开头的 commit。
```

## Task 2.0 — 完成需要人工前置但可由 AI 验收的结果

- 依赖：1.0

- 现在：页面还没有连上实际使用的外部服务，所以用户暂时拿不到真实结果。
- 这次：Codex 会连接该服务；需要登录或授权时，会明确告诉你去哪里完成操作。
- 完成后：用户使用页面功能时会得到外部服务返回的真实结果，而不是测试数据。

**发给 Codex 的 Prompt**

```text
执行 docs/project/tasks.md 中的 Task 2.0，先读取完整任务并检查当前实现，按任务要求完成实现和验证。完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 2.0 开头的 commit。
```

## Task 3.0 — 完成仍需用户判断的结果

- 依赖：无

- 现在：页面是否好看、操作是否顺手，还需要你亲自体验后才能确定。
- 这次：Codex 会先完成页面和可以自动检查的内容，再整理出只需要你判断的部分。
- 完成后：你只需按清单体验一次页面，就能决定它是否可以发布。

**发给 Codex 的 Prompt**

```text
执行 docs/project/tasks.md 中的 Task 3.0，先读取完整任务并检查当前实现，按任务要求完成实现和验证。完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 3.0 开头的 commit。
```

<!-- 生成器必须把上方示例替换为当前产品的真实页面、用户动作和结果，不得保留泛化描述。若 parent 已是 Ready for review，改为只协助对应 G-* 复查与状态收口，不重复实现。所有 parent 完成时省略全部 Task 小节。 -->
