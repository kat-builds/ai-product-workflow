---
name: generate-tasks
description: 从 docs/project/PRD.md 的已确认需求和仓库事实生成、增量更新或只读审查 docs/project/tasks.md，并同步生成面向用户的 docs/project/task-prompt.md。用于把稳定 PRD ID 转换为分阶段、可追踪、可验证的任务包，计算依赖与推荐实际执行顺序，分离 canonical 任务定义和可复制 Codex Prompt，校验两份文档并盘点 User Actions。该 Skill 不生成 PRD、不实现业务代码、不部署且不 commit。
---

# generate-tasks

根据 `docs/project/PRD.md` 和仓库事实生成、更新或审查：

- `docs/project/tasks.md`：唯一 canonical task source of truth，只定义任务范围、要求、依赖、状态和验收。
- `docs/project/task-prompt.md`：从 `tasks.md` 派生的用户执行入口，只提供推荐实际顺序、通俗说明和可复制 Prompt，不重新定义任务合同。

## 必须执行的流程

1. 完整读取适用的 `AGENTS.md`、`docs/project/PRD.md` 和 `references/task-generation-rules.md`。
2. 以 PRD 的 Current Scope、业务规则和 stable IDs 作为唯一产品范围依据；拆分任务前逐项核对相关 stable ID。
3. 若 `docs/project/tasks.md` 已存在，默认增量更新；只有用户明确要求重建时才整体重写。`task-prompt.md` 始终按更新后的 canonical tasks 重新计算，不保留过期顺序或 Prompt。
4. 用户只要求 review / audit 时，只读运行 validator 和语义复检；除非明确要求修复，否则不修改两个项目文档。
5. 只读检查与当前 PRD 范围相关的 repository code、config、tests、scripts 和项目文档。仓库只决定实现事实，不产生新需求。
6. 完成 dependency graph、critical path 和 conflict 分析后判断 Single-Agent 或 Multi-Agent。若启用 Multi-Agent，完整读取并遵守 `references/multi-agent-execution-rules.md`；执行模式只通过必要的 Main Manager、batch 和 Worker 内容体现，不在文档顶部单独声明或解释。
7. 完整读取 `assets/tasks-template.md` 和 `assets/task-prompt-template.md`，先组装 `tasks.md`，再从最终任务状态和 dependency graph 派生 `task-prompt.md`。
8. 本 Skill 只做任务规划，不执行实现、部署或其他会改变项目运行状态的操作，也不创建 branch/worktree、启动 Worker/Subagent 或 commit。
9. 写入后运行：

   ```bash
   python3 <skill-directory>/scripts/validate_tasks.py docs/project/tasks.md docs/project/task-prompt.md
   ```

   修复所有 error，并处理有实质影响的 warning。
10. 最后按 PRD stable IDs 做语义覆盖复检，并复核 `task-prompt.md` 的解释没有扩展或曲解任务范围。
11. 盘点本轮新增或修改任务需要的 User Actions，报告可复用指南的已有与缺失情况；缺少指南时统一询问是否在 Skill 中生成，得到明确同意前不创建。

## 核心判断

* AI 能执行并客观判断的检查写入父任务的 `AI 验证` 和 `Verification Plan`，不单独创建 AI 验证任务或关卡。
* AI 可以独立完成验收时使用 `验收方式：AI 验证`；验证通过后进入 `✅ Approved`。
* 只有 AI 完成全部可执行验证后仍需用户作不可替代的判断、批准或不可逆操作时，才使用 `验收方式：AI 验证后人工复查`；AI 验证后进入 `🟡 Ready for review`，对应 `G-*` 通过后进入 `✅ Approved`。
* 登录、授权、CAPTCHA、2FA、secret、测试账号或测试环境等属于 `人工前置`，不是 `G-*`。
* User Action 的具体步骤保留在 `tasks.md`；`task-prompt.md` 只解释其对当前启动顺序的影响，不复制完整操作指南。
* 每个正式任务或 Confirmation Task 必须引用至少一个 stable PRD ID；不得编造需求、仓库事实或验证证据。
* 缺失决定会改变产品范围、业务规则或实现方向时，生成 Confirmation Task 或 Blocked Task，不得伪装成人工前置。
* Task 编号是稳定引用，不是执行顺序。`task-prompt.md` 必须按 dependency、critical path、blocker、底层影响面、当前状态和冲突面排列未完成 parent。
* `tasks.md` 中不得生成 `执行 Prompt`、`Stop Condition`、Main Manager Kickoff Prompt、Worker Launch Prompt 或 Handoff Prompt；全部可复制 Prompt 只进入 `task-prompt.md`。
* `task-prompt.md` 不复制完整 Task Package，不新增 scope、dependency、acceptance、文件或验证要求；发生冲突时始终以 `tasks.md` 为准。
* 每个执行 chat/session 一次只处理一个 runnable parent Task Package。用户复制某 Task 的 Prompt 或回复 `k` 启动它，即明确授权创建该 Prompt 要求的 task commit。
* 当前 Task 完成后，Single-Agent executor 必须更新 canonical `tasks.md` 并同步 `task-prompt.md`；Multi-Agent Worker 只交付 commit 和证据，由 Main Manager merge 后同步两份文档。任何模式都不得自动实现下一 parent。

## `task-prompt.md` 要求

* 不生成 `Next task`、`Execution mode`、`Execution mode rationale` 或使用方法等顶部调度提示；未完成列表的第一个 Task 就是当前推荐任务。
* 只为未完成 parent 生成 `## Task X.X — <标题>`。存在 `✅ Approved` parent 时，在任务列表前生成 `## 已完成`，下面只写一行 Task ID，按实际完成时间用中文顿号连接，例如 `1.0、2.0、5.0`；最新完成的追加在最后，不得按 Task ID 或 canonical 文档顺序重排。没有已完成任务时省略该区块。
* 每个 Task 标题后只显示一行简短依赖：没有依赖时写 `依赖：无`；否则只列 Task ID，例如 `依赖：1.0`，多个 ID 用 `、` 分隔。存在 canonical blocker 时只追加 blocker ID，不写标题、完成状态或解释。
* `依赖` 后直接列出约 3–6 行通俗说明，并明确写成 `现在：`、`这次：`、`完成后：`。必须使用当前产品的真实页面、用户动作和可见结果；禁止使用“这部分能力”“核心流程”“补齐功能”“形成完整结果”“客观验证”等空泛工程话。
* 使用粗体 `**发给 Codex 的 Prompt**` 引出可复制 Prompt。
* Single-Agent Prompt 使用一句简短启动指令：执行指定 Task、读取完整任务、检查当前实现、按任务要求完成工作和验证、更新两份任务文档，并创建以 Task ID 开头的 commit。具体范围、依赖、边界、人工前置和验证要求不在 Prompt 重复。
* Multi-Agent Worker Prompt 仍需包含 Worker 执行和交接所必需的信息，由 Main Manager 更新两份任务文档。
* Single-Agent 使用完整线性推荐顺序。Multi-Agent 使用按先后排列的 batches；同批任务可并行，但文件中的稳定展示顺序不得暗示虚假 dependency。
* Confirmation、blocked dependency、human prerequisite 和 external dependency 放在实际需要的位置，并写清 unlock condition；不得假设 blocker 已解除。

## 完成前复检

* Current Scope、需要收口的 Existing Baseline ID 和 stable PRD IDs 均可追踪到对应 Task Package。
* Requirement Traceability 每行包含 `PRD ID | Requirement Summary | Task Package | Coverage | Status` 五个非空字段。
* 父任务、`T-*`、`G-*`、验收方式、checkbox 和状态流一致。
* `人工前置`、dependency、真实联调和人工复查使用正确字段，不互相代替。
* Task dependency graph 与父任务 `依赖` 一致；推荐顺序不会把未满足 direct dependency 的任务放在其解锁任务之前。
* `tasks.md` 不含任何可复制执行 Prompt 或模式专属终止字段。
* `task-prompt.md` 已完成 ID 集合与 canonical Approved parents 一致且按实际完成时间排列；未完成 parent 覆盖、标题、依赖 ID、推荐顺序和 Prompt 均与 canonical tasks 一致。
* mock、静态检查或父任务 `✅ Approved` 不得把真实联调误写为 `Verified`。
* 增量更新保留 `tasks.md` 有效历史；发现已有任务失效时，按规则重开相关任务和 `G-*`。
* 输出只包含任务规划，不包含实现结果、部署结果、真实 secret 或敏感值。

完成后简要报告结果和实际 blocker，并分别给出：

* `Structural validator: PASSED/FAILED`
* `PRD semantic review: PASSED/FAILED`
* `Prompt sequence review: PASSED/FAILED`
* `User Actions: NONE`，或列出本轮所需事项及对应指南的 `Available/Missing/Not needed`

只有存在 `Missing` 时才询问是否生成中央指南。
