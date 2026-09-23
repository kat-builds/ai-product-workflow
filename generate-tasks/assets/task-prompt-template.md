# <项目名或域名> — Task Execution Prompts

Last updated: YYYY-MM-DD

> 本文件仅供复制 Prompt；任务定义以 `docs/project/tasks.md` 为准。

<!-- 优先使用 PRD 已确认的用户可见项目名；没有明确项目名时使用仓库事实中已确认的主域名。替换标题占位符，不得猜测。 -->

<!-- 若存在 Approved parent，输出“已完成”及一行 Task ID，按实际完成时间排列，新完成的追加在最后；没有时省略。 -->

## 已完成

1.0

<!-- 若存在未完成 parent，输出“未完成”及一行 Task ID，顺序与下方 Task 小节完全一致；当前 critical path 上的 ID 加 `❗` 前缀。所有 parent 均已完成时省略。 -->

## 未完成

❗2.0、3.0

<!-- 只为未完成 parent 生成 Task 小节。按推荐实际执行顺序排列，不按 Task ID 排序。Single-Agent 使用线性顺序；Multi-Agent 可在 Task 标题下增加 `Execution batch` 和 Worker 元数据。`冲突` 只列当前未完成且不能安全并行的 parent Task ID，关系必须双向一致。 -->

## Task 2.0 — 完成需要人工前置但可由 AI 验收的结果

- 依赖：无
- 冲突：3.0

- 现在：用户还不能从页面完整提交这项操作，提交后也看不到明确结果。
- 这次：Codex 会把填写内容、提交操作、成功结果和失败提示连接起来。
- 完成后：用户可以完成提交；成功时能看到结果，失败时也知道发生了什么。

**发给 Codex 的 Prompt**

```text
执行 docs/project/tasks.md 中的 Task 2.0，先读取完整任务并检查当前实现，按任务要求完成实现和验证。完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 2.0 开头的 commit。
```

## Task 3.0 — 完成仍需用户判断的结果

- 依赖：2.0
- 冲突：2.0

- 现在：页面还没有连上实际使用的外部服务，所以用户暂时拿不到真实结果。
- 这次：Codex 会连接该服务；需要登录或授权时，会明确告诉你去哪里完成操作。
- 完成后：用户使用页面功能时会得到外部服务返回的真实结果，而不是测试数据。

**发给 Codex 的 Prompt**

```text
执行 docs/project/tasks.md 中的 Task 3.0，先读取完整任务并检查当前实现，按任务要求完成实现和验证。完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 3.0 开头的 commit。
```

<!-- 生成器必须把上方示例替换为当前产品的真实页面、用户动作和结果，不得保留泛化描述。没有冲突时必须写 `冲突：无`。若 parent 已是 Ready for review，改为只协助对应 G-* 复查与状态收口，不重复实现。所有 parent 完成时省略全部 Task 小节。 -->
