# `tasks.md` 与 `task-prompt.md` 生成规则

更新日期：2026-08-14

> 目标：把 `docs/project/PRD.md` 中已确认且有稳定 ID 的需求，转换为按验证阶段执行、可追踪、可验证的 canonical `docs/project/tasks.md`，并派生按推荐实际执行顺序排列的 `docs/project/task-prompt.md`。前者只定义任务，后者只帮助用户理解和复制 Prompt。

## 目录

1. 职责与写入边界
2. 权威来源、范围分类与条件引用
3. 任务类型
4. 父任务状态与重开
5. AI 验证、人工前置和人工复查
6. 真实联调
7. 五步生成流程
8. `tasks.md` 固定输出结构
9. 父任务包与 Prompt 分离
10. `G-*` 人工复查关卡
11. `Verification Plan`
12. 固定执行规则
13. Dependency、执行顺序、Multi-Agent 与增量更新
14. 两份文档的校验契约与 Self-Check

## 1. 职责与写入边界

生成或更新任务时：

- 任务生成阶段只允许创建或修改 `docs/project/tasks.md` 和 `docs/project/task-prompt.md`。只有完成两份任务文档并取得用户明确同意后，才可另行新增或更新第 5.5 节定义的 Skill 中央指南。
- `tasks.md` 是唯一 canonical task source of truth，保存 scope、dependency、task contract、status 和 acceptance。
- `task-prompt.md` 是可随任务状态重算的派生执行入口，保存推荐顺序、通俗说明和可复制 Prompt；不得被引用为产品范围或任务合同依据。
- 只读检查仓库；允许使用 `rg`、`rg --files`、`ls`、`sed`、`git diff --no-index` 等不改变项目状态的方式。
- 不得创建或更新 PRD，不得修改业务代码、配置或上述范围之外的其他文档。
- 不得安装依赖、启动服务、执行构建、迁移数据库、调用 provider、部署、开始实现或 commit。
- 当前轮只写未来执行指令；`task-prompt.md` 内的 future commit instruction 不授权当前任务生成阶段提交。
- 不得写入真实 API key、secret、token、password、OAuth secret、webhook secret、数据库 URL、验证码、私钥或测试账号凭据。
- 文件使用 UTF-8、无 BOM。

用户明确只要求 review / audit 时，默认只读运行 validator 和本文件的语义 Self-Check，并报告问题；除非用户明确要求修复，否则不得修改或创建两份任务文档。生成或更新任务时，不执行任务内容或其他项目写入。

## 2. 权威来源、范围分类与条件引用

### 2.1 权威层级

1. `docs/project/PRD.md` 是产品范围、业务规则和稳定需求 ID 的唯一权威。
2. 适用的 `AGENTS.md` 决定仓库操作、测试、格式和提问规则。
3. 实际代码、配置和脚本决定当前实现事实、真实路径、可复用边界和可执行命令。
4. 设计、架构、模块和 playbook 文档只提供被 PRD 触发后的实现约束、流程完整性检查或视觉参考。

不得从仓库、模板或参考文档反推新的产品需求。若 PRD 与实现事实无法同时满足，生成 Confirmation Task 或 Blocked Task，不能在 tasks 中自行改写产品规则。

### 2.2 范围分类

| PRD 分类或状态 | `tasks.md` 去向 | 当前可执行 |
|---|---|---|
| `Current Scope` 且无阻塞 | Formal Task Package | 是 |
| `Existing Baseline` 且 PRD 要求复用、保留、隐藏、redirect、noindex、验证或收口 | Formal Task Package 或明确任务边界 | 是，但不得写成新增能力 |
| `Confirmed Next Phase` | `Follow-up / Later` | 否，除非 PRD 已提升到 Current Scope |
| `Possible Later` | `Follow-up / Later` | 否 |
| `Non-Goals` | `Out of Scope` | 否 |
| `Blocking: Yes` 或 `⛔ Blocked` | Blocked Task | 否 |
| `Blocking: No` | 备注或 `Follow-up / Later` | 不得阻塞无关工作 |
| 无稳定 PRD ID 的新想法 | `Follow-up / Later` 或先更新 PRD | 否 |

这张表是范围去向的唯一完整定义。不得在后续章节用另一套分类重新解释。

### 2.3 项目参考文档的条件引用

先确认 PRD Current Scope 或适用 `AGENTS.md` 是否触发，再读取实际存在的对应文档：

| 参考文档 | 读取条件 | 只允许提供 |
|---|---|---|
| `docs/playbooks/ui-patterns.md` | Current Scope 涉及用户反馈、交互状态、错误/成功反馈或既有 UI pattern | 状态与交互实现模式；不得新增页面、功能、状态或文案 |
| `docs/playbooks/ai-image-architecture.md` | Current Scope 明确涉及 AI 图片生成、模型路由、credits、生成历史、私有访问或图片生命周期 | 模型注册、权益、adapter、执行服务、存储访问和删除生命周期的复用边界 |
| `docs/playbooks/payment-flow.md` | Current Scope 明确涉及 payment、checkout、webhook、一次性购买、subscription、credits 入账/扣除/退款或权益到期 | 入口、checkout、回跳、状态、webhook、入账、退款和异常路径的完整性检查 |
| `docs/modules/PAYMENT.md` | 上述 payment 条件触发且文件存在 | 当前支付模块事实和复用约束 |
| PRD 指定的设计文件、截图、模块文档或其他 playbook | PRD 稳定 ID 或适用 `AGENTS.md` 明确指向，或 Current Scope 能力确实需要该实现参考 | 布局、视觉、架构或模块事实 |

条件引用规则：

- 参考文档存在某项能力，不等于 PRD 要求实现该能力。
- 模板、依赖或代码已经支持某项能力，也不得自动生成相关任务、依赖、测试或配置。
- 只把与触发该文档的 PRD ID 有直接关系的约束带入父任务；其余内容不进入 Scope Freeze、Dependencies、Task Packages 或 Verification Plan。
- 参考路径不存在时，寻找仓库内真实等价文档或代码；无法确认时记录 `TBD — verify actual file path in repo before implementation.`，不得编造路径。
- 支付需求和业务规则始终来自 PRD 及其稳定 ID；payment playbook 只查流程完整性，module 文档和代码只确认实现事实。
- AI 图片任务优先复用现有模型注册表、套餐权益、provider adapter、生成执行服务、私有访问、存储和删除生命周期；只有 PRD ID 明确要求扩展时才能生成新增或改造任务。
- 设计资料只用于布局和视觉指导，不能产生 PRD 未确认的入口、状态、操作或文案。
- 不得修改用户已定制的 UI copy、label 或 placeholder，除非 PRD 明确要求。

## 3. 任务类型

### 3.1 Formal Task Package

实现一个连贯结果，并完成该结果的全部 AI 验证及适用的人工复查。人工前置不改变任务类型。

### 3.2 Confirmation Task

只产出决定、方案、影响分析、配置清单、验证结论或解除阻塞条件，不实现 production behavior。若任务允许修改业务代码、修复实际 implementation defect 或完成正式实现，必须使用 Formal Task Package。若结论改变产品范围或业务规则，必须先更新 PRD，再生成实现任务。

### 3.3 Blocked Task

记录阻塞来源、受影响 PRD ID、允许的准备工作、禁止工作和解除条件。不得包含尚未授权的 provider 接入、schema、生产配置或真实实现步骤。

### 3.4 Follow-up / Later

记录当前不执行的事项，不使用 checkbox，不生成 execution prompt。

每个 Formal Task Package 和 Confirmation Task 必须引用至少一个稳定 PRD ID。`BLOCKED-*`、`T-*` 或 `G-*` 不能替代 PRD ID。

## 4. 父任务状态与重开

### 4.1 允许状态

```text
⬜ Pending
🔵 In progress
🟡 Ready for review
✅ Approved
⛔ Blocked
```

前四项是父任务 `状态` 的精确枚举；`⛔ Blocked` 只用于独立 Blocked Task。`前置状态`、`真实联调` 和 Verification Plan `Status` 使用各自独立枚举，不添加这些任务状态符号。

### 4.2 状态流

仅需 AI 验证：

```text
⬜ Pending → 🔵 In progress → ✅ Approved
```

AI 验证后仍需人工复查：

```text
⬜ Pending → 🔵 In progress → 🟡 Ready for review → ✅ Approved
```

状态定义：

- `⬜ Pending`：尚未开始，标题 checkbox 为 `[ ]`。开始前缺少人工前置时仍保持此状态。
- `🔵 In progress`：实现或验证正在进行；开始后才发现人工前置缺失时保持此状态，并记录最小阻塞点。
- `🟡 Ready for review`：实现和全部 AI 可执行验证已通过，只剩已记录的人工复查；标题仍为 `[ ]`。
- `✅ Approved`：全部必需 AI 验证，以及适用的人工复查已通过；标题必须为 `[x]`。若 PRD 把真实联调列为本父任务验收条件，相关真实联调也必须已通过。
- `⛔ Blocked`：只用于无法开始的独立 Blocked Task；父任务因 dependency 或人工前置暂时无法继续时，仍按实际进度保持 `⬜ Pending` 或 `🔵 In progress`。

`验收方式：AI 验证` 不得使用 `🟡 Ready for review`。`验收方式：AI 验证后人工复查` 在关卡通过前不得进入 `✅ Approved`。

### 4.3 最终复检后的重开

最终复检或后续验证发现缺陷时：

1. 把受影响任务从 `[x] ✅ Approved` 改为 `[ ] 🔵 In progress`。
2. 把因该缺陷失效且已完成的 `G-*` 重置为 `[ ]`。
3. 修复缺陷并重新运行受影响的 AI 验证。
4. `AI 验证` 任务在验证通过后才恢复 `[x] ✅ Approved`。
5. `AI 验证后人工复查` 任务先回到 `🟡 Ready for review`，重新完成对应人工复查后才恢复 `[x] ✅ Approved`。

不得保留已知失效的批准状态或人工关卡结果。

## 5. AI 验证、人工前置和人工复查

三者是不同概念，字段、步骤、执行者和状态流不得混用。

### 5.1 AI 验证

AI 能执行且能依据客观证据判断结果时，必须由 AI 验证。例如：

- typecheck、lint、unit、integration、E2E；
- 浏览器交互、viewport 和 responsive 检查；
- API 请求与 response assertion；
- database query 与状态验证；
- provider test mode；
- mock、redirect、metadata、sitemap、robots 等确定性结果；
- repository diff、文件路径、删除边界和复用边界检查。

规则：

- 每个父任务通过 `AI 验证` 字段引用 `T-*`。
- 每个 `T-*` 只在固定 `Verification Plan` 定义一次。
- 技术命令、code、path、API、SQL、测试身份/环境和证据可写在父任务或 Verification Plan。
- 未来执行时必须实际运行，不能按计划、推测或静态描述标记通过。
- 不为 AI 验证创建独立父任务、独立门禁或 `G-*`。

### 5.2 人工前置

AI 仍能完成并客观验证任务，但需要用户先提供执行条件时，使用人工前置。例如：

- 批准 terminal、browser、tool 或 account permission；
- 登录用户自己的账号；
- 完成 CAPTCHA、verification code 或 2FA；
- 在部署平台配置命名的 secret 或 environment variable；
- 启用 API 或授权 integration；
- 提供 test account、test data 或 test environment；
- 完成 AI 无法代替的一次性 account setup。

父任务字段：

```text
人工前置：None | Required
前置状态：Not required | Pending | Provided
用户介入：🔴 P1/P2/P3 User Action Required    # 仅 Required
用户操作指南：$generate-tasks/references/user-actions/<name>.md    # 仅已有中央指南时
用户需完成：...    # 仅 Required
需要时间：开始任务前 | 执行到某一步时    # 仅 Required
完成后：AI 从阻塞步骤继续实现和验证。    # 仅 Required
```

规则：

- `人工前置` 和 `前置状态` 是单行精确枚举字段，不得写 `Ready`、`Waiting for ...`、解释性自然语言或在枚举值后追加条件。dependency 只写在 `依赖`，真实 provider/environment 验证进度只写在 `真实联调`。
- `None` 必须对应 `前置状态：Not required`，且不生成 `用户需完成 / 需要时间 / 完成后`。
- `Required` 必须对应 `前置状态：Pending` 或 `Provided`，并包含以上三个说明。
- `Required` 必须增加 `用户介入：🔴 Pn User Action Required`；`Pn` 按对 critical path 的影响选择。没有中央指南时，具体步骤放在 `用户需完成`；有指南时引用该文件，并只补充本项目参数。
- `None` 不得包含 `用户介入`；AI 能通过已有授权工具安全完成的事项不得伪装成人工前置或标红。
- 只记录权限或配置名称、目的和安全操作方式，不记录 secret value、credential 或 verification code。
- 尚未开始且前置缺失时保持 `⬜ Pending`；开始后缺失时保持 `🔵 In progress`，完成不依赖该前置的安全工作并记录精确阻塞步骤。
- 用户提供前置后继续同一个父任务，不新建替代任务。
- 人工前置不是验收结果，不生成 `G-*`，通常也不生成 `T-*`。
- 一般访问权限不授权真实扣款、production release、production deletion 或其他不可逆动作。
- 未确认的 provider 选择、价格/权益规则、商业决定或 architecture direction 属于 Confirmation Task 或 Blocked Task，不属于人工前置。
- 人工前置只保留当前 parent 局部需要的 `User Action Required`。若同一 parent 还需要 Decision 或 Approval，不得把它们一并塞入人工前置。
- 影响多个任务或改变产品/业务方向的未决 Decision，以一个 Blocked Task 或 Confirmation Task 作为 canonical source；跨任务、高影响或 production-sensitive Approval 以一个 Blocked Task 作为 canonical source，相关 parent 只引用该 blocker。
- AI 验证完成后仍不可替代的最终 Decision 或 Approval 才进入 `G-*`。同一事项不得在 parent、Blocked Task、`G-*` 和 `task-prompt.md` 重复建模。

### 5.3 人工复查

只有 AI 完成全部客观验证后仍存在不可替代的人类判断或明确批准时，才使用人工复查。例如：

- 主观视觉、interaction quality 或 brand judgment；
- Legal、commercial 或 final Go/No-Go approval；
- 对真实扣款、正式发布、生产删除等不可逆动作的具体确认；
- 用户明确不授权 AI 代做的 account-specific action。

规则：

- 父任务使用 `验收方式：AI 验证后人工复查`。
- AI 先完成所有可执行验证，并把任务更新为 `🟡 Ready for review`。
- 创建 `G-*`，其中只保留剩余人工步骤。
- `G-*` 必须增加 `用户介入：🔴 Pn User Decision Required` 或 `用户介入：🔴 Pn User Approval Required`，分别用于改变产品/业务结果的不可替代决定，或 destructive、high-impact、irreversible、hard-to-rollback、production-sensitive 操作的明确批准。
- `G-*` 不重复 AI tests、`T-*`、commands、technical evidence 或 source-code inspection。
- 用户步骤必须说明去哪里、做什么、观察什么、什么算通过、什么算失败以及失败后如何处理。

### 5.4 选择验收方式

每个父任务只使用以下一个值：

```text
验收方式：AI 验证
验收方式：AI 验证后人工复查
```

- 即使改动用户可见或风险高，只要已获得必要权限且结果可客观判断，仍使用 `AI 验证`；风险只增加验证覆盖，不自动产生人工复查。
- 只有验证后仍剩不可委托判断时，才使用 `AI 验证后人工复查`。

### 5.5 User Action Guide

User Action Guide 是 `$generate-tasks/references/user-actions/*.md` 中可跨项目复用的外部平台操作说明。项目专属参数和任务状态仍保留在 `tasks.md`。

任务生成与增量更新完成后，只盘点本轮新增或修改任务中的 `User Action / User Decision / User Approval`：

1. 一句话即可说明的事项标记为 `Not needed`，步骤直接保留在 `tasks.md`。
2. 对复杂事项检查 Skill 中是否已有准确适用的指南；已有时标记为 `Available` 并引用，不重复通用步骤。
3. 没有指南时标记为 `Missing`，在 `tasks.md` 保留完整步骤，不写不存在的引用。
4. 完成 validator 和 PRD semantic review 后，统一报告事项、关联 Task、时机及 `Available/Missing/Not needed`；只有存在 `Missing` 时才一次性询问是否生成。
5. 用户同意后才新增或更新中央指南，并只复检受影响任务；用户暂不生成时，现有 `tasks.md` 保持可执行并结束流程。

中央指南只收录稳定、重复且与具体项目无关的操作，并说明使用时机、入口、准备条件、完整步骤、参数来源、成功标准、失败处理和必要的安全限制；不适用的内容省略。项目名称、域名、环境变量名等差异作为参数留在 `tasks.md`。依赖未来 implementation 才能确定的步骤不得提前编造。实际执行到人工事项时，AI 仍先检查是否已经完成或可安全代办，再请求用户介入。

## 6. 真实联调

涉及外部服务的父任务独立记录：

```text
真实联调：Not required | Pending | Verified
```

- `Not required`：该父任务不需要真实 provider、webhook、storage 或 production dependency。
- `Pending`：实现、mock 或静态验证可以完成，但真实外部依赖尚未实际测试。
- `Verified`：未来执行时必须记录真实入口、环境、执行方式和结果证据。

规则：

- mock、typecheck、build、unit test 或计划中的调用不能替代真实联调。
- 父任务 `✅ Approved` 不会自动把真实联调 `Pending` 改为 `Verified`。
- 若 PRD 明确把真实联调作为该父任务的验收条件，相关 Verification Plan row 通过且 `真实联调` 更新为 `Verified` 前，父任务不得进入 `✅ Approved`。
- 若 PRD 明确允许真实联调作为后续非阻塞验证，父任务可以保持 `✅ Approved` 与 `真实联调：Pending`；该 Pending 不得被描述为已验证，也不得阻塞不依赖它的后续任务。
- PRD 要求真实联调时，对应 Verification Plan row 必须保持可见，直到实际执行并获得证据。
- 缺少人工前置时，真实联调和相关测试保持 `Pending`，不能按推测通过。

## 7. 五步生成流程

### 第一步：读取 PRD 并判断可用性

完整提取：

- Current Scope、Existing Baseline、Confirmed Next Phase、Possible Later、Non-Goals；
- page、flow、feature、copy、error 和 non-functional IDs；
- API、data、auth、storage、payment、analytics、mail、provider、SEO 和 legal requirements；
- design 与 technical constraints；
- Open Questions、`Blocking` 和 `⛔ Blocked`。

在拆分 Task Package 前，逐个核对每个 stable ID 在 PRD 中的原意、范围状态和 verification needs；未完成逐项核对前不得分组。

完整正式任务的最低条件：

- Current Scope 非空；
- 核心 flow 和 page scope 可判断；
- 可执行 Current Scope 需求有稳定 PRD ID；
- payment、auth、data 和核心 provider boundary 没有被错误当作已确认。

整体范围不可用时，不生成虚假的完整计划。局部阻塞只隔离受影响任务，不阻塞无关 Current Scope。必须提问时，遵守适用 `AGENTS.md` 的问题格式。

### 第二步：只读扫描相关仓库上下文

按 PRD 实际触发扫描：

- 适用 `AGENTS.md` 和 `package.json` scripts；
- routes、pages、layouts、navigation、footer；
- components、shared UI、styles、design tokens；
- i18n files、namespaces 和现有 keys；
- site config、content、metadata、sitemap、robots、redirect；
- API、database、auth、storage、payment、analytics、mail；
- `env.example`、deployment config 和 provider use；
- 第 2.3 节条件触发的项目参考文档。

路径规则：

- 先找实际等价位置，不假设模板默认路径一定存在。
- 只记录扫描得到的真实路径；实在无法确认时才写明确 TBD。
- 记录 reuse source、target、allowed changes 和 must-not-change。
- 新建 component 前先确认现有 component 不能复用或在明确边界内 adapt。
- 验证命令只能来自适用 `AGENTS.md`、实际 package scripts 或仓库工具。

### 第三步：冻结范围和依赖

生成：

- `In Scope`：当前要完成的内容，每项引用 PRD ID；
- `Existing Baseline`：PRD 要求复用、保留、隐藏、不触碰、验证或收口的现有能力；
- `Out of Scope`：Non-Goals 和当前明确不做内容；
- `Follow-up / Later`：Confirmed Next Phase、Possible Later 和执行中发现的范围外事项。

同时建立父任务 direct dependency graph、识别 critical path，并判断 API、database、auth、storage、payment、upload、analytics、SEO/legal、external provider、environment config、schema/migration、shared high-conflict files、blocker 和 human prerequisite。Task 编号、章节或阶段本身不是 dependency。

对 schema/migrations、auth、payment、package/dependencies、shared config、env、shared types、routes、global styles、messages、shared core modules 和 `tasks.md` 等 conflict surface 做初步 owner 分析；无法可靠隔离的任务降低并行度、合并给同一 Worker 或串行。

新站初始化、Cloudflare、Hyperdrive、database 或 provider setup 只有被 PRD ID 明确触发时才生成。模板已有配置不能成为生成理由。

### 第四步：按可验证结果拆父任务并判断执行模式

通常为 4–8 个包，但不得为了数量强拆。每个包必须：

- 形成连贯且可独立验收的结果；
- 有明确 boundary 和 dependency；
- 写真实文件或明确 TBD；
- 引用 AI verification；
- 记录 acceptance method、human prerequisite 和 real integration；
- 不把 Confirmation 或 Blocked 内容藏进 implementation subtasks。

UI 与真实 API 可分阶段，但不能提前宣称真实联调完成。人工关卡放在其失败会使后续任务返工的第一个下游任务之前；不受结论影响的安全任务可先执行。

任务拆分后，以 time-to-correct-completion 为目标评估 Multi-Agent Execution 的净收益。只有并行时间收益明显高于 context、branch/worktree、协调、conflict、merge、review、validation 和机器资源成本时才启用；否则保持 Single-Agent Mode。启用时必须完整读取 `multi-agent-execution-rules.md`，并把执行模式、batches、Worker 启动和交接 Prompt 只写入 `task-prompt.md`；不启动独立 Codex Worker chat/session、不创建内部 Subagent，也不创建 runtime 文件。

### 第五步：组装、派生、校验并保存

- 只读 review / audit 时运行 validator 和语义 Self-Check，报告结果后停止；除非用户明确要求修复，否则不执行以下写入步骤。
- 先按第 8 节顺序组装 canonical `tasks.md`；父任务不得包含模式专属 Prompt 或 `Stop Condition`。
- 再按第 9.3 和 14.3 节从最终 dependency graph、状态和执行模式派生 `task-prompt.md`。
- 运行 `scripts/validate_tasks.py docs/project/tasks.md docs/project/task-prompt.md`。
- 修复全部 error 和有实际影响的 warning。
- 对照 PRD ID 做 validator 无法完成的语义覆盖审计，并检查通俗说明没有扩展或曲解 task contract。
- 按第 5.5 节盘点本轮 User Actions。
- 完成报告分别给出 `Structural validator: PASSED/FAILED`、`PRD semantic review: PASSED/FAILED`、`Prompt sequence review: PASSED/FAILED` 和 `User Actions`，不得互相代替。
- 两份文件都保存为 UTF-8、无 BOM。
- 不执行已生成任务，不 commit。

## 8. `tasks.md` 固定输出结构

标题后首先包含文档角色说明：

> 文档角色说明：本文件是当前项目唯一 canonical task source of truth，只定义任务范围、要求、依赖、状态和验收。需求与业务规则以 `docs/project/PRD.md` 为准；用户实际复制给 Codex 的 Prompt 位于 `docs/project/task-prompt.md`。若两份任务文档冲突，以本文件为准并重新生成 `task-prompt.md`。

紧随其后输出固定图例：

> 任务状态：⬜ Pending · 🔵 In progress · 🟡 Ready for review · ✅ Approved · ⛔ Blocked

章节按以下顺序：

1. `Scope Freeze`
2. `Traceability & Reuse`
3. `Dependencies & Blockers`
4. `Relevant Files`
5. `Task Packages`
6. `Verification Plan`
7. `Development Rules & Task Management`

`Dependencies & Blockers` 和 `Verification Plan` 永远必需。`tasks.md` 不生成 `Execution Guide`、`Execution Plan` 或任何可复制 Prompt；执行模式和用户操作层只进入 `task-prompt.md`。

所有 Markdown table cell 若需包含 literal `|`，必须写成 `\|`；未转义的 `|` 只作为 column delimiter。

### 8.1 Scope Freeze

固定包含 `In Scope`、`Existing Baseline`、`Out of Scope` 和 `Follow-up / Later`；后者按需包含 `Confirmed Next Phase`、`Possible Later`、`执行中发现的范围外事项`。完整 Markdown 格式见 [tasks-template.md](../assets/tasks-template.md)。空的 Follow-up 子类可省略，但不能变成正式任务。

### 8.2 Traceability & Reuse

需求追踪表：

```md
| PRD ID | Requirement Summary | Task Package | Coverage | Status |
|---|---|---|---|---|
```

覆盖所有 Current Scope ID 和需要关闭、验证或收口的 Existing Baseline ID。无代码改动时写明 `Covered by existing implementation`、`Verification only` 或 `Documentation only`。

表头和每个 requirement row 都必须严格为五列且五列非空，顺序只能是 `PRD ID | Requirement Summary | Task Package | Coverage | Status`。不得省略 `Requirement Summary`，不得把 Task mapping、Coverage 或 Status 左移/右移到相邻字段；需要补充说明时写在对应 cell 内，不增加第六列。

只有含义、Task mapping 和 verification needs 实质一致的 IDs 才允许使用 range shorthand 合并；任一项不一致时必须逐项列出，range shorthand 不得替代逐个核对。

涉及页面或 component 时生成独立复用表：

```md
| Section / Component | Decision | Existing Source | Target | Allowed Changes | Must Not Change |
|---|---|---|---|---|---|
```

Decision 使用 `Reuse / Adapt / New / Hide / Do not touch`。新增 component 必须说明现有 component 不能复用的原因、单一职责和边界。任务生成阶段只记录 future execution constraint，不调用 component Skill 实现组件。

### 8.3 Dependencies & Blockers

始终先生成父任务 direct dependency graph：

```md
### Task Dependency Graph

| Task Package | Direct Dependencies | Unlocks | Start Condition |
|---|---|---|---|
| `1.0` | `None` | `2.0` | PRD 与 repository facts 已足够 |
```

- 每个 Formal/Confirmation parent 恰好一行；dependency 必须与父任务的 `依赖` 字段一致。
- 只记录 direct dependency，不用 task 编号、文档顺序或阶段名称制造串行关系。
- `Start Condition` 写 dependency、contract、人工前置或 blocker 解除条件；不能把计划状态写成已完成事实。
- 局部 blocker 只影响依赖它的任务；没有 dependency 的安全任务仍可开始。

API、data、auth、storage、payment、upload、analytics、SEO/legal、external provider、configuration 或 blocker 被 PRD 触发时，再生成：

```md
### External Dependencies & Blockers

| Capability | PRD IDs | Decision | Provider / Dependency | Required Config | Impact if Missing |
|---|---|---|---|---|---|
```

只列 environment variable name 和用途，不列值。未确认 provider 不得生成真实接入、webhook、entitlement、schema 或 production config。

Blocked Task：

```md
### BLOCKED-001: 标题
- 状态：`⛔ Blocked`
- 受影响 PRD ID：...
- 用户介入：`🔴 Pn User Action Required`、`🔴 Pn User Decision Required` 或 `🔴 Pn User Approval Required` — 仅当解除 blocker 确实需要用户介入时
- 阻塞来源：...
- 原因：...
- 解除条件：...
- 解除前允许做：...
- 禁止做：...
```

一个 blocker 是其共享 Action、Decision 或 Approval 的 canonical source；相关 parent 和 `task-prompt.md` 只引用它，不复制完整步骤。

### 8.4 Relevant Files

按 [tasks-template.md](../assets/tasks-template.md) 使用 `核心必改`、`可能涉及`、`新增文件` 三类；只列真实扫描路径或明确 TBD。增量更新不静默删除仍相关的历史文件。

### 8.5 Prompt 与执行信息禁区

`tasks.md` 只定义任务，不承担用户操作层。禁止写入：

- 父任务 `执行 Prompt` 或 `Stop Condition` 字段；
- `Execution Guide`、`Execution Plan`、`Main Manager Kickoff Prompt`、Worker Launch/Handoff Prompt；
- “复制下面 Prompt”“发送给 Codex”等用户启动步骤；
- 仅为某次调度快照存在的 Worker、branch、batch 或 reasoning level。

Dependency、critical path 判断所需的稳定事实保留在 `Task Dependency Graph`、parent `依赖`、边界和验证字段。所有派生执行信息进入 `task-prompt.md`。

## 9. 父任务包

### 9.1 固定格式

使用连续且稳定的 `### [ ] 1.0 ...`、`2.0 ...`；subtask 使用 `1.1`、`1.2`，不使用 checkbox。

````md
### [ ] 1.0 结果导向标题

- 任务类型：`Formal Task Package` 或 `Confirmation Task`
- 状态：`⬜ Pending`
- 验收方式：`AI 验证` 或 `AI 验证后人工复查`
- 人工前置：`None` 或 `Required`
- 前置状态：`Not required`、`Pending` 或 `Provided`
- 用户介入：`🔴 P1/P2/P3 User Action Required` — 仅在人工前置 Required 时
- 用户需完成：仅 Required
- 需要时间：仅 Required
- 完成后：仅 Required
- 真实联调：`Not required`、`Pending` 或 `Verified`
- 来源：稳定 PRD IDs
- 目标：可独立验证的结果
- 边界 / 不做：明确排除内容
- 依赖：task、config、dependency 或 `None`
- 子项：
  - 1.1 ...
  - 1.2 ...
- 涉及文件：真实 path 和 intended operation
- AI 验证：`T-001`, `T-002`
- 人工验收关卡：`G-01` — 仅在验收方式需要人工复查时
````

父任务以 `AI 验证` 或适用的 `人工验收关卡` 结束，不追加模式专属执行字段。具体用户 Prompt 见第 9.3 节并只写入 `task-prompt.md`。

### 9.2 一致性规则

- `任务类型`、state、acceptance method、human prerequisite、real integration、source、goal、boundary、dependency、subtasks 和 files、AI verification 均为必填。
- `任务类型`、`状态`、`验收方式`、`人工前置`、`前置状态` 和 `真实联调` 都是单行精确枚举，不得把 dependency、blocker、联调对象或进度说明附加到枚举字段；这些事实分别写入 `依赖`、对应 `BLOCKED-*` 或 `真实联调`。
- `来源` 至少包含一个真实稳定 PRD ID，不得只写“参考 PRD”。
- title 具体且以结果或动作表达，不用“处理一些问题”等模糊名称。
- `边界 / 不做` 阻止 UI、API、payment、auth 或 scope-out 内容顺手混入。
- subtask 只说明覆盖内容，不独立执行、提交或生成 prompt。
- 父任务不得包含 `执行 Prompt`、`Stop Condition`、Worker、branch、worktree 或 Completion Report 元数据。
- `AI 验证` 任务不引用 `G-*`，验证通过后更新为 `[x] ✅ Approved`。
- `AI 验证后人工复查` 任务必须引用一个实际 `G-*`，AI 验证后只更新为 `[ ] 🟡 Ready for review`。
- human prerequisite 可用于任一验收方式；它不改变 acceptance method 或最终状态流。
- Confirmation Task 不修改 production behavior；若确认结果会改变 PRD，future execution 必须先更新 PRD 并停止，等待重新生成 tasks。
- env/config 改动涉及执行时，文件清单包含实际 `env.example`；schema 改动按 PRD 和仓库规则判断 migration/fixture。
- payment/credits 父任务继承相关 PRD IDs 和条件读取到的流程/模块约束，但不能从参考文档创造产品规则。
- i18n 任务记录 resource file 和 key，不硬编码最终文案，不改写用户定制 copy。
- UI/content 类任务不默认加入 full build；只有用户、适用 `AGENTS.md` 或实际仓库规则要求时才加入。
- Single-Agent 执行者一次只完成一个父任务；Multi-Agent Worker 只完成被分配的 Task Package，后续调度只由 Main Manager / Integration Owner 决定。
- Multi-Agent Worker 不更新共享 `docs/project/tasks.md`。它提交自己的实现与验证证据；Main Manager review/merge 通过后统一更新任务状态。

### 9.3 在 `task-prompt.md` 生成用户 Prompt

使用 [task-prompt-template.md](../assets/task-prompt-template.md) 的固定结构。只为未完成 parent 生成一个 `## Task X.X — <标题>`，并按顺序包含：

1. `依赖`：没有依赖时写 `无`；否则只列 Task ID，例如 `1.0`，多个 ID 用 `、` 分隔。存在 canonical blocker 时只追加 blocker ID。不得添加标题、完成状态或解释。
2. 约 3–6 行通俗说明，直接放在 `依赖` 后，并至少包含以下三句：
   - `现在：`说明用户目前在哪个页面、做什么操作时遇到什么问题或缺少什么结果；
   - `这次：`说明 Codex 会改动哪一段用户过程或系统行为；
   - `完成后：`说明用户能完成什么动作、会看到什么，或系统会怎样运行。
3. 粗体 `**发给 Codex 的 Prompt**` 和一个完整 `text` code fence。Prompt 只引用 canonical parent，不重写 Task Package。

若存在 `✅ Approved` parent，在第一个未完成 Task 前生成：

```md
## 已完成
1.0、2.0、5.0
```

标题下只写一行，用中文顿号连接真实 Approved Task ID，并按实际完成时间从早到晚排列；没有 Approved parent 时省略整个区块。已完成任务不再生成 Prompt 小节。

增量更新时保留现有已完成 ID 的先后顺序，将新进入 `✅ Approved` 的 Task 追加到最后。需要重建列表时，按 `tasks.md` 的最终验证证据时间或 Git 中该 Task 最后一次完成 commit 的时间排列；已重开后重新批准的 Task 以最后一次批准时间为准。不得按 Task ID 或 canonical 文档顺序代替完成时间。

通俗说明必须使用 PRD 和 repository 中真实的产品名词。不得复制 parent 的 `目标`、`子项`、`涉及文件` 或 Verification Plan 行；不得出现 Task/T/G ID、验证状态、文件路径或内部代码标识。禁止使用“这部分能力”“核心流程”“补齐功能/工作”“形成完整结果”“客观验证/确认”“可核对的验证结果”“按已确认流程”等不能让非程序员理解实际变化的空话。必要技术术语首次出现时用人话解释并补充英文。

不生成 `Next task`、`Execution mode`、`Execution mode rationale` 或使用方法等顶部调度提示。未完成列表仍按推荐实际执行顺序排列，第一个 `## Task` 就是当前推荐任务；其他 Task 是否需要等待，直接由其 `依赖` ID 和 canonical `tasks.md` 判断。

Single-Agent Prompt 使用一句启动指令：

```text
执行 docs/project/tasks.md 中的 Task X.X，先读取完整任务并检查当前实现，按任务要求完成工作和验证。完成后更新 docs/project/tasks.md 和 docs/project/task-prompt.md，并创建以 X.X 开头的 commit。
```

Prompt 不重复 Task Package。实现类任务可把“工作”写成“实现”，Confirmation Task 可写成“核查”，`🟡 Ready for review` 可写成“复查”；其他要求仍以 canonical parent 和适用 `AGENTS.md` 为准。`✅ Approved` 不生成 Task Prompt。

Single-Agent Prompt 直接用于 Local chat。Multi-Agent Prompt 的额外 Worker、branch/worktree、allowed boundary、focused validation、commit 和 Completion Report 信息按 `multi-agent-execution-rules.md` 加入同一个 Task 的 Prompt，不复制任务合同；Worker 不更新两份任务文档，由 Main Manager merge 后统一同步。

这些 future commit instruction 只在用户实际发送该 Task Prompt 或回复 `k` 时授权执行；不授权当前 task generation 阶段 commit。

## 10. `G-*` 人工复查关卡

只有确实剩余人工判断时创建 `G-*`。

```md
### [ ] G-01 人工复查 — 开始 3.0 前

- 覆盖任务：`1.0`, `2.0`
- 用户介入：`🔴 P1 User Decision Required`
- 设置原因：为什么必须在此处取得用户判断
- 用户需检查：
  1. 前往明确页面或环境。
  2. 完成明确用户操作。
  3. 观察并判断明确结果。
- 通过标准：用户可理解的通过条件
- 未通过：记录问题，把受影响任务重开为 🔵 In progress；修复并重新完成 AI 验证后重复本次复查
- 通过后：把关卡更新为 [x]，把覆盖任务更新为 ✅ Approved 和 [x]，提交状态更新后继续
```

规则：

- `G-*` 不是 implementation task，不生成 execution prompt。
- checkbox 只表示关卡是否通过；`[x] G-*` 覆盖的任务必须为 `[x] ✅ Approved`。
- 未通过或最终复检使结果失效时，关卡保持或重置为 `[ ]`，受影响任务重开。
- 每个需要人工复查的父任务必须由它引用的 `G-*` 覆盖；`G-*` 不得覆盖仅需 AI 验证的任务或未知任务。
- 收集所有 parent `人工验收关卡` 的唯一 ID 集合，并在同一次生成中为每个 ID 输出且只输出一个正式 `### [ ] G-*` checkpoint；parent 引用集合与 checkpoint 定义集合必须完全相等，不得留下只引用未定义或定义未引用的关卡。
- 一个关卡可覆盖多个逻辑相关且都需要人工复查的 `🟡 Ready for review` 任务。
- `未通过` 和 `通过后` 必须逐一写出所有 `覆盖任务` ID，并分别说明重开为 `🔵 In progress` 后重跑 AI 验证，以及 checkpoint `[x]` 后把覆盖任务更新为 `✅ Approved` / `[x]`。
- 关卡安排在第一个会受人工结论影响或失败后会返工的任务之前。
- 用户步骤必须使用自然语言，明确入口、动作、观察、通过和失败。
- 禁止把 command、code fence、`T-*`、`Verification Plan`、source-code inspection、database query、API call 或未解释的技术证据交给用户。
- AI 能通过 browser/E2E/API/database/provider test mode 客观完成的部分，必须留在父任务和 Verification Plan，不得复制到 `G-*`。
- 登录、CAPTCHA、2FA、secret config、test account 和 tool permission 按人工前置处理，不创建 `G-*`。
- `用户介入` 只能使用 `🔴 P1/P2/P3 User Decision Required` 或 `🔴 P1/P2/P3 User Approval Required`；普通技术判断、AI 可完成操作和纯执行前置不得放入 `G-*`。
- 已有准确适用的中央指南时可以引用；否则把用户可执行的步骤直接写在 `G-*`。
- grouped checkpoint 在并行计划中只由 integration owner 执行并更新共享状态。

## 11. `Verification Plan`

固定包含一张中央表。每个 test 只定义一次，父任务的 `AI 验证` 只引用 ID：

```md
| ID | Stage | Scenario | Executor | Page / Entry | Steps or Command | Expected Result | Status |
|---|---|---|---|---|---|---|---|
| `T-001` | `1.0` | ... | AI | ... | ... | ... | Not tested |
```

规则：

- 新生成的 `T-*` executor 使用 `AI`；人工前置留在父任务，人工复查留在 `G-*`，不复制成技术测试。
- browser action、responsive check、E2E、API、database、provider test mode 和客观 visual assertion 在权限具备时都由 AI 执行。
- 每个父任务至少引用一个 `T-*`；每个引用必须有且只有一个定义。
- 每个定义必须被父任务引用，且 row 的 `Stage` 必须包含该父任务编号。
- 每个核心 flow 至少一个 normal test。
- 每个被 PRD 触发的高风险 capability 至少一个 critical error、duplicate 或 idempotency test。
- UI 工作按 PRD 覆盖 relevant initial、empty、invalid、loading、error、success 和 result-action states。
- responsive 只在 UI scope 触发时检查相关 viewport；通常包含 `320 / 768 / 1024` 和无 page-level horizontal overflow。
- real integration row 保持 `Pending`，直到实际执行并记录证据。
- 不为 PRD 未触发的 capability 生成 test。
- 不得按 planned behavior 或 inference 标记 passed。

## 12. 固定执行规则

`Development Rules & Task Management` 至少包含：

- 严格按 PRD、Scope Freeze 和 parent boundary 执行；scope-out 进入 Follow-up / Later。
- 用户可见最终 copy 通过 i18n；不覆盖用户已定制 copy。
- 优先 reuse existing components 和 semantic tokens。
- 未经 PRD 和父任务明确授权，不得删除 file、section、component call、route 或 existing capability，也不得用 placeholder 替换。
- secret 只进入 server-side 或 platform secret storage，不进入 code、Markdown、log 或 screenshot。
- human prerequisite 只保存当前 parent 局部的 User Action 执行条件；共享 Decision/Approval 引用 canonical blocker，完成后 AI 从 blocked step 继续。
- 请求用户前先检查现状并自行完成安全可执行部分。
- AI 可执行且可客观判断的 verification 由 AI 完成并留实际 evidence。
- `G-*` 只包含不可替代的剩余 human judgment。
- real provider 未联调时保持 `真实联调：Pending`。
- final recheck 发现 defect 时重开 affected task，并 reset invalidated `G-*`。
- Single-Agent executor 一次只完成一个 parent package；Multi-Agent Worker 只完成分配的 Task Package。

更新到 `🟡 Ready for review` 前，future executor 必须检查当前 diff；若发现父任务未明确授权的 file deletion、section removal、component-call removal 或 whole-capability replacement，必须恢复或暂停请求确认。

## 13. Dependency、执行顺序、Multi-Agent 与增量更新

### 13.1 Dependency 与 Multi-Agent 判断

- Task number 和 stage 不构成 dependency；局部 blocker 只暂停受影响任务。
- AI 根据 direct dependency、critical path、conflict surface、协调/整合成本和机器资源判断并行净收益；不按任务数量配置 Worker，也不为并行强拆任务。
- 只有净收益明显为正时才在 `task-prompt.md` 使用 Multi-Agent batches，并完整遵守 `multi-agent-execution-rules.md`；否则使用 Single-Agent 线性顺序。
- 选择 Single-Agent 时必须记录当前 repository 的具体证据，说明实际 conflict、coordination/integration 与 resource 成本为何高于并行收益；执行顺序始终从 runnable dependency graph 和 critical path 重新选择，不得写成按 task 编号推进。

### 13.2 增量更新

若 `docs/project/tasks.md` 已存在，默认增量更新：

- 保留有效的 `[x]`、`✅ Approved`、`🟡 Ready for review` 和 `🔵 In progress` 历史。
- 只有已知 defect 按第 4.3 节重开受影响任务和失效关卡。
- 不静默删除、改写、renumber 或 reorder 历史任务。
- PRD 变化使任务失效时，将其从可执行父任务区移入 `Follow-up / Later` 的历史/归档记录，保留原 task ID 和最后合法状态，并注明失效原因及替代任务（如有）；不得把 `Superseded` 写入父任务 `状态` 字段。
- 新 parent package 使用后续稳定编号。
- 更新 traceability、relevant files、verification rows 和 `tasks.md` 实际 Last updated 日期。
- 每次都从更新后的 canonical 状态重算 `task-prompt.md`；已完成 parent 只进入 `## 已完成` ID 清单，保留原有完成顺序并在最后追加新 Approved Task，不保留其 Task 小节、旧 blocker 顺序、旧 Worker assignment 或旧 Prompt。
- 含旧验收字段、旧人工复核等级或无状态符号枚举的历史 package 必须在本次文档更新中迁移到当前字段；迁移只规范结构，必须保留真实 title、scope、evidence、checkbox 和 completion state，不得把未完成工作写成完成。已经使用当前字段且未受 PRD 变化影响的历史内容原样保留。

## 14. 两份文档的校验契约与 Self-Check

### 14.1 Validator 必须确定性检查

`scripts/validate_tasks.py` 至少检查：

- UTF-8/BOM、required section、code fence 外的父任务顶层字段、枚举、checkbox/state 和结构化 legacy field；
- Markdown table 的 `\|` literal pipe、Requirement Traceability 表头、分隔行及每个数据行严格为五个非空列；
- dependency graph 与父任务依赖一致、引用存在且无 cycle；
- prerequisite 精确枚举、acceptance、正式 `G-*` 定义、`T-*`、真实联调和状态流互相一致；
- `tasks.md` 不含 `执行 Prompt`、`Stop Condition`、Execution Guide/Plan 或 Main Manager/Worker 可复制 Prompt；
- `task-prompt.md` 的 UTF-8/BOM、Task 标题、未完成 parent 一一覆盖和 Approved 排除，且不含顶部调度提示；
- `## 已完成` 的 ID 集合与 canonical Approved parents 完全一致且无重复；完成时间顺序由语义复检核对；每个未完成 Task 包含简短 dependency/blocker ID、约 3–6 行通俗说明、粗体 Prompt 标识和唯一完整的短 text Prompt；
- 通俗说明包含 `现在 / 这次 / 完成后`，没有 Task/T/G ID、技术字段或已禁止的空泛工程话；
- Prompt 不得包含额外停止语句或否定已由用户发送 Prompt 给出的 commit 授权；
- 顺序至少满足 direct dependency：未完成 dependency 必须出现在 dependent 之前，列表第一项的 direct dependencies 必须已完成；
- Multi-Agent 时的 batch、唯一 Worker/branch、allowed boundary、focused validation 和 handoff 结构一致；
- 正式 `用户介入` 字段使用合法 `🔴` label，且相关说明字段非空；人工步骤不含技术委派或可能的 secret/credential 泄露。

Validator 只能检查结构、枚举、引用和可识别模式，不能代替 PRD semantic coverage、真实路径确认、主观判断必要性或实际 provider evidence 审查。
不要用复杂 regex 判断任务是否语义上属于 Confirmation Task、业务拆分是否合理，或 prompt 是否使用某句固定措辞；这些由 Self-Check 和 AI semantic review 负责。

### 14.2 Self-Check

保存前逐项确认：

1. PRD 分类、稳定 ID、Scope Freeze 和 traceability 一致；参考文档没有扩大范围。
2. repository facts、路径、命令、reuse 和 must-not-change boundary 均有依据或明确 TBD。
3. 父任务按可独立验收结果拆分；Confirmation Task 只产出决定、方案、影响分析、配置清单、验证结论或解除条件，任何允许修改业务代码、修复 implementation defect 或完成正式实现的任务均为 Formal Task Package；Blocked/Follow-up 没有混入未授权实现。
4. dependency graph、critical path、局部 blocker 和父任务 `依赖` 一致，没有按编号制造串行；若选择 Single-Agent，已用当前 repository 的 conflict、coordination/integration、resource 证据证明其成本高于并行收益，并按 runnable dependency / critical path 调度。
5. parent fields、checkbox/state、acceptance、prerequisite 精确枚举、real integration、`T-*` 和正式 `G-*` checkpoint 状态流一致；Traceability 每行严格对应五列表头。
6. AI 验证覆盖核心 flow、PRD 触发的高风险/error path 和必要 UI states；未真实联调的项目保持 `真实联调：Pending`。若真实联调是父任务验收条件，未通过前不得进入 `✅ Approved`；若只是 PRD 允许的后续非阻塞验证，可保持 `✅ Approved` 与 `真实联调：Pending`。
7. 人工前置只包含 parent 局部 Action；跨任务 Decision/Approval 由唯一 blocker 作为 canonical source，AI 验证后的最终判断才进入 `G-*`；所有 `🔴` 类型和优先级正确，用户步骤无需技术委派。
8. `tasks.md` 只定义任务，没有任何可复制 Prompt、Stop Condition、Worker assignment 或用户启动步骤。
9. `task-prompt.md` 明确声明自己是派生入口；已完成 ID 集合、完成时间顺序、未完成 parent 覆盖、标题、依赖 ID 和推荐执行顺序均已复核，通俗说明能让非程序员知道 Codex 实际在改什么。
10. 若启用 Multi-Agent，完整通过 `multi-agent-execution-rules.md` 的 Self-Check；否则不生成 batch、Worker、branch 或 handoff 空壳。
11. 增量更新保留有效历史，已知 defect 正确重开任务并重置失效 gate。
12. 本轮新增或修改任务的 User Actions 已按第 5.5 节盘点，未为缺少的指南写入虚假引用。
13. 两份文件只包含 planning，无当前阶段 implementation、deployment、commit、secret 或 credential。
14. 两份文件 UTF-8、无 BOM、无 mojibake，并一起通过 validator。

### 14.3 `task-prompt.md` 的推荐实际执行顺序

Task 编号是稳定引用，不是执行序号。生成或更新 canonical `tasks.md` 后，必须把当前顺序快照写入 `task-prompt.md`，但不得写回 `tasks.md`。任务状态、PRD、dependency 或 blocker 改变后必须重新计算。

顺序计算规则：

1. 排除所有 `✅ Approved` parent；只有已确认 defect 并按重开规则变为未完成时才重新进入列表。
2. 从未完成 parent 的真实 direct dependency graph 出发；先安排能解除 critical path 或多个 blocker 的 runnable task，再考虑风险、预计时间和 conflict surface。
3. `🔵 In progress` 仍须满足 dependency；若其依赖未完成，先列 unlock task，并明确该 In-progress task 暂不可继续。
4. Confirmation Task、Blocked Task、human prerequisite 和 external dependency 放在它实际阻塞后续工作的最早位置，并写明 unlock condition；不得假设用户决定、credential 或外部状态已经具备。
5. 用户明确把多个仓库纳入同一规划时，按领域选择已有实现、测试和证据更成熟的一边先做；另一边随后复核实际 commit、diff、tests 和 completion evidence，并只适配通用 contract。Provider、AI workflow、payment、storage、初始化脚本和产品范围差异必须保留。
6. Single-Agent 为全部未完成 parent 生成线性 Task 小节；第一个小节必须是真正可启动的 parent。
7. Multi-Agent 按先后排列 batches；同批 Task 小节可标注并行，不人为制造 dependency。首批中稳定展示的第一项放在最前，并在 batch 元数据中标明同批其他项可并行。
8. 若所有未完成 parent 都被外部 blocker 阻塞，仍按最早 unlock value 排列，并在顶部第一项说明 blocker；不得伪造已解除状态。
9. task 完成或状态改变时，执行者同步 `task-prompt.md`：移除 Approved Task 小节，把其 ID 追加到 `## 已完成` 末尾，并重算剩余顺序。结构性范围或 dependency 改变时必须重新运行 `$generate-tasks`。
