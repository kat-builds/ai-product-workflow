# Multi-Agent Execution 规则

更新日期：2026-08-14

> 目标：在正确性和风险可控的前提下缩短 time-to-correct-completion。本文件只规定如何在 `docs/project/task-prompt.md` 表达并行 batches、Main Manager、Worker Prompt 和交接；canonical `docs/project/tasks.md` 始终只定义任务，不保存这些运行时调度信息。

## 目录

1. 适用范围与启用判断
2. Dependency、critical path 与 batches
3. Conflict Surface Analysis
4. Main Manager 与 Worker 隔离
5. `task-prompt.md` 结构
6. 每个 Task 的 Worker Prompt
7. Model / reasoning level 与资源
8. Worker ownership、merge 与 stale context
9. `🔴` 用户介入
10. Self-Check

## 0. 术语与文档边界

- `Worker`：用户按 `task-prompt.md` 启动的独立 Codex Worktree chat/session；每个 Worker 使用独立 branch 和 worktree，一次只执行一个 parent Task Package。
- `Main Manager`：唯一 Integration Owner，负责 `main`、review、merge、integration validation、canonical task status 和后续调度。
- `Subagent`：同一 Codex 会话内部由 parent 创建和管理的子 Agent，不等同于独立 Worker；不得混用两者。

文档职责：

- `tasks.md`：唯一 task source of truth。不得包含 Execution Plan、Worker assignment、branch、Launch/Handoff Prompt 或 Stop Condition。
- `task-prompt.md`：当前执行快照。可以包含 batches、Main Manager 启动 Prompt、每个未完成 Task 的 Worker metadata 和可复制 Prompt；不得重写 task contract，不生成顶部执行模式或使用说明。

生成 Multi-Agent 文档不等于启动 Worker/Subagent、创建 branch/worktree、merge 或 commit。

## 1. 适用范围与启用判断

完成 parent 拆分、direct dependency graph 和 conflict surface 后再判断。优化目标是更快达到正确完成，不是 Worker 数量最多。

综合评估：

- runnable tasks、critical path 和预计耗时；
- file/module/interface/schema/业务语义的 conflict surface；
- session startup、context loading、branch/worktree、协调、review、merge 和 integration 成本；
- CPU、RAM、disk/I/O、browser、build、test、typecheck、dev server 和当前重任务；
- stale context、返工概率及其对 critical path 的影响。

只有并行时间收益明显高于这些成本且风险可控时，才在 `task-prompt.md` 生成 Main Manager、Worker 和 batch 内容。否则使用普通线性 Task 列表，不得生成 Worker 或 batch 空壳。

## 2. Dependency、critical path 与 batches

一个 Task 进入某 batch 前必须满足：

1. direct dependencies 已 `✅ Approved`，或 Main Manager 根据 repository evidence 确认所需 contract 已锁定；首次静态生成不得从自由文字猜测 contract 已锁定；
2. 不依赖未解除的产品决定、用户前置或外部 blocker；
3. 与同批 Task 的写入边界可可靠隔离；
4. 共享资源足够，预计并发不会使总时间变长；
5. 实际时间收益高于启动、协调、merge 和验证成本。

调度优先级：

1. 先解除 blocking prerequisite；
2. 保持 critical path 持续推进；
3. 同批启动所有安全且有明显收益的独立任务；
4. 同等条件下先启动预计耗时较长或能解锁更多下游的任务；
5. 局部 blocker 只阻塞依赖它的 Task。

Task ID 不是执行顺序。同批在文件中使用稳定展示顺序，但必须标明可以并行，不能把展示顺序描述为 dependency。

不得为了增加 Worker 数强拆连贯 parent。Waiting/Blocked Task 仍保留自己的 `## Task X.X` 小节并按预计 unlock 位置排列，但 Prompt 必须写明启动条件；不得让用户误以为当前已 runnable。

## 3. Conflict Surface Analysis

逐项检查：

- database schema、migrations、seed、fixtures；
- auth、authorization、ownership、session；
- payment、credits、webhook、entitlement；
- package/dependencies、lockfile；
- shared config、environment、deployment；
- shared types、interfaces、API contracts、generated clients；
- routes、layouts、navigation、middleware；
- global styles、design tokens、shared UI primitives；
- messages、i18n namespaces、共享文案；
- shared core modules、central registries、cross-cutting utilities；
- `tasks.md`、`task-prompt.md` 和其他共享执行文档；
- 多个 Task 预计同时修改的实际文件。

对每个高冲突区域指定唯一 owner，其他 Worker 标为 read-only/prohibited，并写清 coordination point。无法可靠隔离时降低并发、交给同一 Worker 或串行。不同 worktree 不能自动解决 semantic/interface/integration conflict。

## 4. Main Manager 与 Worker 隔离

### 4.1 Main Manager

唯一 Main Manager / Integration Owner 负责：

- 维护 dependency graph 和 critical path；
- 根据真实 repository/Git 状态决定 Worker 调度；
- 管理 `main`、merge timing/order 和跨任务 conflict；
- review Worker diff、boundary 和 validation evidence；
- 运行必要 integration/final validation；
- merge 后更新 canonical `tasks.md` 状态，并同步 `task-prompt.md` 的已完成时间顺序、剩余 Task 和 batches。

Main Manager 只承担整合职责，不抢占可交给 Worker 的普通开发任务。

### 4.2 Worker

每个 Worker：

- 使用从 latest `main` 创建的独立 worktree 和唯一非 `main` branch；
- 只处理分配的一个 Task Package 和 allowed files/modules；
- 不操作、切换、修改、merge 或 push `main`；
- 不整合其他 Worker branch；
- 不修改 `docs/project/tasks.md` 或 `docs/project/task-prompt.md`；
- dependency 假设失效、需要越界或 shared contract 冲突时停止并报告 Main Manager；
- 完成后提交 commit 和完整 Completion Report，不自行 merge。

## 5. `task-prompt.md` 结构

文档顺序：

1. 文档角色说明；
2. 若存在 Approved parent，按实际完成时间排列的 `## 已完成`；
3. 一份完整 Main Manager Kickoff `text` Prompt；
4. 按 batch 顺序排列的所有未完成 `## Task X.X — <标题>`。

不输出 `Next task`、`Execution mode`、rationale 或使用方法。首个 batch 中稳定展示的第一项放在最前，batch 元数据说明同批还有哪些 Task 可并行。没有未完成 parent 时不输出 kickoff 或 Task 小节。

每个 Task 标题下、固定的两个小节前，可以增加以下短元数据：

```md
- 依赖：无
Execution batch: `Batch 1` — may run in parallel with Task 3.0
Worker: `Worker A`
Branch: `task/1-0-...`
Allowed Files / Modules: `path/a`, `path/b`
Focused Validation: `T-001`
```

只有真实高冲突例外时增加 `Do Not Touch`。默认 reasoning level 不重复写。元数据是当前调度快照，不得写入 `tasks.md`。

Main Manager Kickoff Prompt 必须要求：

- 读取 canonical `tasks.md` 和派生 `task-prompt.md`；
- 从 repository/Git 实际状态核对 `main`、working tree、dependencies、资源、batches、branch 和 boundary，不把计划状态当事实；
- kickoff 只报告用户现在应创建的 Worktree chats 和可启动 Workers，不创建 Worker/branch/worktree，不开始实现；
- 后续根据 branch、commit、diff、logs 和 validation evidence review/merge；
- merge 后更新 `tasks.md` 和 `task-prompt.md`，再返回下一批完整 Task Prompt。

## 6. 每个 Task 的 Worker Prompt

每个未完成 parent 仍严格使用：

````md
## Task X.X — <标题>

- 依赖：无，或只列 Task / blocker ID

约 3–6 行，直接以“现在 / 这次 / 完成后”说明真实用户问题、改动和结果。

**发给 Codex 的 Prompt**

```text
完整 Worker Prompt
```
````

Worker Prompt 在通用 parent Prompt 要求之外，必须包含：

- Worker、Task Package、branch、direct dependencies、allowed files/modules、focused validation；
- 仅在适用时包含 Do Not Touch 和偏离默认值的 reasoning level；
- 确认独立 worktree/branch，并读取适用 `AGENTS.md`、canonical parent 和必要 PRD 内容；
- 已正确实现的部分只验证，不重复修改；
- 只处理当前 Task，不操作 main，不修改两份任务文档；
- boundary/dependency 失效时报告 Main Manager；
- 创建符合仓库规则且以 Task ID 开头的 commit，不 merge；
- Completion Report 包含 Worker、Task、branch、commit hash、changed files/diff、dependency 假设、boundary、validation 命令与结果、风险/blocker 和建议 canonical 状态。

Worker 不负责同步 `task-prompt.md`；该同步由 Main Manager merge 后完成。因此 Multi-Agent Worker Prompt 不要求 Worker 更新任务状态文件。

Waiting/Blocked Task 的 Prompt 必须首先核对 unlock condition。若仍未满足，只报告 blocker，不创建 branch、不开始实现、不 commit。

## 7. Model / reasoning level 与资源

- Main Manager：至少 `High`。
- Worker 默认：`Middle`。
- `Low`：只用于机械、低风险、边界清晰且易客观验证的任务。
- `High`：用于复杂、高风险、critical-path、跨模块、auth、payment、migration、debugging 或 integration。
- 不确定时使用 `Middle`；不得指定具体模型名称。

Worker 只运行 focused validation。full build、full test suite、Playwright/browser/E2E 和大型 integration tests 由 Main Manager 按资源限流。不要让多个 Worker 同时争用 browser、port 或大型 build/test。

## 8. Worker ownership、merge 与 stale context

Task 实质开始后默认由原 Worker持续完成。只有 blocked、不收敛、假设失效、latest main 使实现过时，或预计返工成本明显高于重新规划时才重新分配。

Main Manager merge 前必须：

1. review diff、commit 和 changed files；
2. 核对 Task boundary、allowed files、Do Not Touch 和 dependency 假设；
3. 核对 validation evidence；
4. 按风险追加 targeted review/validation；
5. 根据在途 branches、shared files、dependency 和 critical path 决定 merge timing/order；
6. merge 后运行适当 integration validation，再更新两份任务文档。

不要机械要求每个 branch 每次都 rebase，也不要因 Worker 完成就自动 merge。

## 9. `🔴` 用户介入

- parent 人工前置、`G-*`、Confirmation Task、Blocked Task 和 User Action Guide 仍以 `tasks.md` 为 canonical source。
- `task-prompt.md` 只简短解释 blocker 对启动顺序的影响，不复制完整用户步骤。
- `P1` 阻塞当前/近期 critical path，`P2` 是后续确定需要，`P3` 不影响主要进度。
- 不得记录真实 secret、credential 或 verification code。

## 10. Self-Check

1. 并行净收益与推荐并发数有 dependency、conflict 和资源依据；未为展示并行而强拆 Task。
2. 每个 batch 只含 runnable 或明确 contract-locked Task；Waiting/Blocked 有真实 unlock condition。
3. 唯一 Main Manager、merge gate、branch/worktree、file owner 和 shared contract 清楚。
4. `tasks.md` 没有任何 Execution Plan、Worker metadata、Prompt 或 Stop Condition。
5. `task-prompt.md` 的已完成时间顺序、batches、未完成 parent 和依赖与 canonical 状态一致，且没有顶部调度提示。
6. 每个 Task 保留简短依赖、通俗说明和粗体 Prompt 标识；通俗说明使用真实用户动作与结果，不复制技术合同或空泛工程话，Worker Prompt 不复制整个 PRD/Task Package。
7. 每个 Worker Prompt 包含唯一 Task/branch、边界、focused validation、main prohibition、commit 和 Completion Report；Worker 不修改两份任务文档。
8. Main Manager kickoff 完整可复制，并明确由用户创建 Worktree chats；生成 Skill 本身不启动 Worker/Subagent。
9. Reasoning 与重型验证按资源调度，不指定具体模型，不机械 rebase/merge。
10. genuine user blockers 只在 `tasks.md` 建模一次，`task-prompt.md` 仅引用且不泄露 secret。
