# Implementation Tasks

Last updated: YYYY-MM-DD

> 文档角色说明：本文件是当前项目唯一 canonical task source of truth，只定义任务范围、要求、依赖、状态和验收。需求与业务规则以 `docs/project/PRD.md` 为准；用户实际复制给 Codex 的 Prompt 位于 `docs/project/task-prompt.md`。若两份任务文档冲突，以本文件为准并重新生成 `task-prompt.md`。

> 任务状态：⬜ Pending · 🔵 In progress · 🟡 Ready for review · ✅ Approved · ⛔ Blocked

## Scope Freeze

### In Scope

- `FR-001` — ...

### Existing Baseline

- `PAGE-001` — 保留、复用、隐藏或不触碰的方式。

### Out of Scope

- ...

### Follow-up / Later

#### Confirmed Next Phase

- ...

#### Possible Later

- ...

#### 执行中发现的范围外事项

- ...

## Traceability & Reuse

### Requirement Traceability

| PRD ID | Requirement Summary | Task Package | Coverage | Status |
|---|---|---|---|---|
| `FR-001` | ... | `1.0` | ... | Planned |
| `FR-002` | ... | `2.0` | ... | Planned |
| `FR-003` | ... | `3.0` | ... | Planned |

### Component Reuse Summary

| Section / Component | Decision | Existing Source | Target | Allowed Changes | Must Not Change |
|---|---|---|---|---|---|
| ... | Reuse / Adapt / New / Hide / Do not touch | ... | ... | ... | ... |

## Dependencies & Blockers

### Task Dependency Graph

| Task Package | Direct Dependencies | Unlocks | Start Condition |
|---|---|---|---|
| `1.0` | `None` | `2.0` | PRD 与 repository facts 已足够 |
| `2.0` | `1.0` | `None` | `1.0` ✅ Approved；所需人工前置在真实 provider 验证前提供 |
| `3.0` | `None` | `None` | PRD 与 repository facts 已足够；不因编号等待 `1.0` |

### External Dependencies & Blockers

| Capability | PRD IDs | Decision | Provider / Dependency | Required Config | Impact if Missing |
|---|---|---|---|---|---|
| ... | `FR-002` | Reuse / Configure / Defer | ... | `VARIABLE_NAME` | ... |

<!-- 只有真实 blocker 时输出下列结构。 -->

### BLOCKED-001: 标题

- 状态：`⛔ Blocked`
- 受影响 PRD ID：`FR-001`
- 用户介入：`🔴 P1 User Decision Required`
- 阻塞来源：...
- 原因：...
- 解除条件：...
- 解除前允许做：...
- 禁止做：...

## Relevant Files

### 核心必改

- `path` — 操作和边界。

### 可能涉及

- `path` — 触发条件。

### 新增文件

- `path` — 用途，或明确写为 `TBD — verify actual file path in repo before implementation.`。

## Task Packages

<!-- 人工前置、前置状态和真实联调都是单行精确枚举字段。父任务不得包含执行 Prompt、Stop Condition 或 Worker 启动信息。 -->

### [ ] 1.0 完成可客观验证的结果

- 任务类型：`Formal Task Package`
- 状态：`⬜ Pending`
- 验收方式：`AI 验证`
- 人工前置：`None`
- 前置状态：`Not required`
- 真实联调：`Not required`
- 来源：`FR-001`
- 目标：...
- 边界 / 不做：...
- 依赖：`None`
- 子项：
  - 1.1 ...
  - 1.2 ...
- 涉及文件：
  - `path` — ...
- AI 验证：`T-001`, `T-002`

### [ ] 2.0 完成需要人工前置但可由 AI 验收的结果

- 任务类型：`Formal Task Package`
- 状态：`⬜ Pending`
- 验收方式：`AI 验证`
- 人工前置：`Required`
- 前置状态：`Pending`
- 用户介入：`🔴 P1 User Action Required`
- 用户需完成：
  1. 前往明确的 provider test mode 配置入口。
  2. 按本任务列出的名称完成所需授权或配置，不在文档中记录 secret value。
  3. 确认测试环境可以使用该配置。
- 需要时间：`执行到 provider test mode 验证时`
- 完成后：AI 从阻塞步骤继续实现和验证，不再要求用户参与本任务验收。
- 真实联调：`Pending`
- 来源：`FR-002`
- 目标：...
- 边界 / 不做：一般访问权限不授权真实扣款、正式发布、生产删除或其他不可逆动作。
- 依赖：`1.0`
- 子项：
  - 2.1 ...
- 涉及文件：
  - `path` — ...
- AI 验证：`T-003`

### [ ] 3.0 完成仍需用户判断的结果

- 任务类型：`Formal Task Package`
- 状态：`⬜ Pending`
- 验收方式：`AI 验证后人工复查`
- 人工前置：`None`
- 前置状态：`Not required`
- 真实联调：`Not required`
- 来源：`FR-003`
- 目标：...
- 边界 / 不做：...
- 依赖：`None`
- 子项：
  - 3.1 ...
- 涉及文件：
  - `path` — ...
- AI 验证：`T-004`
- 人工验收关卡：`G-01` — 正式发布前

<!-- 收集所有 parent 的人工验收关卡引用，并为每个唯一 G-* ID 输出且只输出一个正式 checkpoint。 -->

### [ ] G-01 人工复查 — 正式发布前

- 覆盖任务：`3.0`
- 用户介入：`🔴 P2 User Decision Required`
- 设置原因：最终体验需要用户作不可替代的主观判断，失败会影响发布决定。
- 用户需检查：
  1. 前往已通过 AI 验证的目标页面。
  2. 按已确认的核心流程完成一次操作。
  3. 判断整体体验是否符合产品目标，并记录任何需要修改的具体问题。
- 通过标准：页面体验符合已确认目标，没有需要修改的主观体验问题。
- 未通过：记录具体问题，把 `3.0` 重开为 🔵 In progress；修复并重新完成 AI 验证后，再重复本次人工复查。
- 通过后：把 `G-01` 更新为 [x]，把 `3.0` 更新为 ✅ Approved 和 [x]，提交状态更新后再继续。

## Verification Plan

| ID | Stage | Scenario | Executor | Page / Entry | Steps or Command | Expected Result | Status |
|---|---|---|---|---|---|---|---|
| `T-001` | `1.0` | Type checking | AI | Repository root | `pnpm typecheck` | 命令成功且没有 TypeScript error | Not tested |
| `T-002` | `1.0` | Core user flow | AI | `/path` | 使用浏览器或仓库已有 E2E 流程执行主要操作 | 状态正确保存并展示 | Not tested |
| `T-003` | `2.0` | Provider test mode | AI | Test environment | 在所需人工前置完成后调用 provider test mode | 返回有效结果且没有认证错误 | Pending |
| `T-004` | `3.0` | Objective UI states | AI | `/path` | 检查相关 initial、loading、error、success 和响应式状态 | 所有客观状态符合 PRD 且页面无横向溢出 | Not tested |

## Development Rules & Task Management

* 严格按 PRD、Scope Freeze 和父任务边界执行；范围外内容进入 Follow-up / Later。
* 用户可见最终文案通过 i18n；不得覆盖用户已定制文案。
* 优先复用现有组件和语义 token；新增组件遵循 Component Reuse Summary。
* 未经 PRD 或父任务明确要求，不删除现有文件、路由、组件或能力，也不用占位内容替换。
* Secret 只存在服务端或部署平台 secret storage，不进入代码、Markdown、日志或截图。
* 真实 provider 或外部依赖未实际联调时，`真实联调` 保持 `Pending`。
* 最终复检发现缺陷时，将受影响的 `✅ Approved` 任务重开为 `🔵 In progress`，并重置失效的 `G-*`；修复后重新走对应状态流。
* `docs/project/task-prompt.md` 只是派生执行入口；任何冲突都以本文件为准并重新同步。
