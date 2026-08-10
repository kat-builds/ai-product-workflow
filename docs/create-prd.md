# 规则：生成产品需求文档（PRD）

更新日期：2026-07-16

> 一句话目标：根据用户需求、上游规格和当前仓库事实，生成清晰、可执行、可验证的 `docs/project/PRD.md`，定义“做什么、为什么做、如何运作”，但不开始实现。

## 一、输出边界

- 只生成或更新 `docs/project/PRD.md`。
- 不写业务代码，不生成 `docs/project/tasks.md`，不执行构建、迁移、部署或外部服务调用。
- PRD 定义产品范围、页面结构、业务规则、交互、文案、风险与验收标准。
- 具体文件改动、实现步骤、任务依赖、执行工具和命令留给 `docs/playbooks/generate-task.md`。
- 默认使用中文编写 PRD；面向用户的实际站点文案默认使用英文，并通过 i18n 资源读取。
- 用户已经定制的 UI 文案、标签和 placeholder 不得擅自改写。
- 输出路径固定为项目专属文档目录下的 `docs/project/PRD.md`；若用户要求其他路径，先确认后再写。

PRD 标题下方必须包含：

> 文档角色说明：本文件定义产品的当前范围、功能逻辑、交互流程、业务规则、页面结构与验收标准；视觉落地遵循当前工程的 design token、组件体系与 i18n 规范。

> 语言说明：本文档使用中文；面向用户的站点文案默认使用英文并通过 i18n 资源读取，代码命名、路由、字段名和内部术语使用英文。

## 二、核心分类规则

### 2.1 范围分类

所有重要需求必须归入以下一种分类：

| 分类 | 含义 | PRD 与后续任务处理 |
|---|---|---|
| `Current Scope` | 本次明确实现或改造 | 写入正式需求并分配稳定 ID |
| `Existing Baseline` | 仓库已有，本次只复用、保留、隐藏或不触碰 | 说明处理方式，不写成新增能力 |
| `Confirmed Next Phase` | 用户明确承诺下一阶段实现 | 仅记录阶段与基础设施影响，不进入当前功能 |
| `Possible Later` | 未来可能考虑，尚未承诺 | 仅记录，不触发当前基础设施或任务 |
| `Non-Goals` | 当前明确不做 | 写明排除内容和原因，不生成当前需求 |

规则：

- 最新用户明确确认优先于上游规格和模板现状。
- `Existing Baseline`、`Confirmed Next Phase`、`Possible Later` 和 `Non-Goals` 不得自动升级为 `Current Scope`。
- Coming Soon、模板已有入口或仓库已有 provider 都不能单独证明它们属于当前范围。
- 被用户明确覆盖的上游内容应记录为 `Explicitly Overridden`，不得悄悄恢复。

### 2.2 问题优先级

| 级别 | 定义 | 处理方式 |
|---|---|---|
| P0 | 会改变当前范围、核心流程、页面结构、支付、登录、数据或核心 provider 可行性 | 生成 PRD 前询问；无法安全默认时推荐“阻塞或暂缓” |
| P1 | 有合理默认值，不改变核心范围 | 使用推荐值，并在 PRD 中记录假设 |
| P2 | 不影响当前实现 | 写入 `Open Questions`，标记 `Blocking: No` |

### 2.3 项目复杂度

先判断项目属于简单前端工具、内容站、API 工具、AI 工具、账号型产品或付费产品。只有当前范围实际触发以下能力时，才展开对应专项要求：

- 第三方 API、AI API、provider SDK 或 webhook；
- 登录、权限、数据库、用户资产或历史记录；
- 文件上传、本地处理、对象存储或云端结果；
- 支付、订阅、一次性购买、credits、额度或权益；
- Analytics、转化追踪、SEO 索引面或合规要求。

## 三、执行流程

### 第一步：读取输入并映射范围

读取用户需求、已有 PRD、idea/spec、design brief、STITCH、截图或其他上游资料。若有上游规格，按以下方式映射：

若 `Current Scope` 或 `Confirmed Next Phase` 触发 AI 图片生成、参考图、生成历史、图片存储、模型路由或 credits，必须读取 `docs/playbooks/ai-image-architecture.md`。该文档只用于识别模板已有契约和复用边界，不能单独把任何能力升级为 `Current Scope`。PRD 应把相关能力分别判断为 `Reuse / Configure / Extend / Defer / Not required`，避免重新设计已有 Provider、扣费、持久化和删除流程。

| 上游内容 | PRD 去向 |
|---|---|
| 当前实现要求 | `Current Scope`、页面、流程和正式需求 |
| 已有能力 | `Existing Baseline` |
| 明确下一阶段 | `Confirmed Next Phase` |
| 可能以后做、Coming Soon | `Possible Later` |
| 明确排除 | `Non-Goals` |
| Need Decision | 按 P0/P1/P2 处理 |
| 设计说明或参考代码 | 仅用于布局、视觉和复用判断 |
| Do Not Include in UI | Design constraints 或 `Non-Goals` |

设计稿、截图、STITCH 和模板代码不得作为新增功能、文案、状态、登录或付费入口的需求来源。

### 第二步：扫描关键缺口

检查以下内容能否从输入和仓库事实中确定：

- 用户问题、目标用户和成功标准；
- 当前范围、明确不做内容和主要用户路径；
- 页面、入口、导航及模板已有能力的处理方式；
- API、数据、登录、存储、支付、Analytics 是否属于当前范围；
- 域名、目标地区、语言、SEO 或内容要求；
- 设计参考、核心文案、错误状态和移动端要求。

不要要求用户决定底层技术细节；仓库结构、移动端默认值、design token、i18n 和常规错误处理应由规则合理推断。

### 第三步：提出必要问题

- 只问确实影响 PRD 的问题，每轮最多 3 题；若仍有未解决 P0，可在下一轮继续询问。
- 优先合并相关问题，选项必须互斥且能直接决定范围。
- 用户少回复字母时，其余题目采用各题推荐选项，除非用户明确拒绝默认。
- 推荐项不得编造价格、真实 API endpoint、法律承诺、第三方限制或敏感数据策略；不确定时推荐暂缓或记录阻塞。

提问格式必须符合：

```text
Reply with letters in order, e.g. ACB = 1A 2C 3B.
If fewer letters are provided, recommended options will be used for the rest unless you say otherwise.

1. 问题内容
   A. 选项 A
   B. 选项 B
   C. 选项 C

   Recommended: A
   Reason: 一句简短理由。
```

要求：

- 每个问题编号；
- 每题提供 2–4 个 A/B/C/D 选项；
- 每题包含 `Recommended: X` 和 `Reason: ...`；
- 同时接受 `ACB` 和 `1A, 2C, 3B`；
- 用户说“按推荐”时直接继续，不重复确认。

### 第四步：生成 PRD

把用户回答和推荐假设写成已经收敛的需求，不把选择题原文写入 PRD。所有需要后续实现或验证的 `Current Scope` 内容必须使用稳定 ID。

推荐 ID：

| 类型 | ID 示例 |
|---|---|
| 页面或入口 | `PAGE-001` |
| 用户流程 | `FLOW-001` |
| 功能需求 | `FR-001` |
| 数据、登录或存储 | `DATA-001` |
| API 或集成 | `API-001` |
| 支付或权益 | `PAY-001` |
| UI 文案 | `COPY-001` |
| 错误状态 | `ERR-001` |
| 非功能与验收要求 | `NFR-001` |

规则：

- ID 在一份 PRD 内唯一且稳定；更新 PRD 时不得无原因重排或复用旧 ID。
- 一个需求只表达一个可判断结果；复杂需求拆成多个 ID。
- 后续 `generate-task.md` 只能继承这些 ID，不得自行创造产品需求 ID。
- 若某项不需要实现但需要保留、隐藏、redirect、noindex 或验证，也应有可追踪 ID。

### 第五步：自检并保存

按第六章检查并修正后，将文件以 UTF-8 保存为 `docs/project/PRD.md`。不得写入 BOM、乱码、真实 secret 或真实凭据。

## 四、PRD 结构

以下 14 个主章节保持顺序。标记“按需”的章节或子节在未触发时可以省略，不机械输出大量 `Not applicable`。

### 1. Introduction & Goals

- 产品或功能概述、用户问题、目标用户和价值；
- 可衡量目标及 Current Scope 验收标准；
- 明确假设，避免使用“体验良好”“功能正常”等模糊描述。

### 2. Domain, Audience & SEO

- 域名、目标地区、站点语言和主要受众；
- 关键词、搜索意图、title/description 或内容策略，仅在相关时展开；
- 只引用仓库实际存在且适用于当前项目的 SEO 文档，不编造路径。

### 3. Project Type & Scope

必须包含：

- 项目类型和本 PRD 的展开深度；
- `Current Scope`、`Existing Baseline`、`Confirmed Next Phase`、`Possible Later`；
- Database、Auth、Storage、Payment 等基础设施结论：`Configure / Reuse / Defer / Not required`；
- 结论只由 Current Scope 和明确的 Confirmed Next Phase 支撑。

### 4. User Scenarios

列出主要用户、触发场景、用户目标和预期结果。复杂权限角色按角色拆分；简单工具不需要堆砌重复 User Stories。

### 5. Page Structure

每个相关页面或入口写明：

- 路由或页面角色；
- 处理方式：新增、复用、改造、隐藏、保留、不触碰或删除；
- 页面区块顺序、关键状态和主要 CTA；
- Dashboard、Pricing、Login、Blog、Legal、导航和 footer 是否属于范围。

不得因为模板存在页面就自动加入当前范围；删除已有页面必须有用户要求或明确必要性。

### 6. Interaction Flows

使用 `FLOW-xxx` 描述用户视角的完整流程：入口、操作、系统反馈、成功结果和下一步。涉及登录、额度、支付、上传或异步生成时，必须写条件分支和失败路径。

### 7. Functional Requirements

使用稳定 ID 编写可实现、可验证的正式需求。每条至少说明：

- 触发条件或用户动作；
- 系统行为和业务规则；
- 用户可见结果；
- 关键边界或验收标准。

被阻塞的需求标记 `⛔ Blocked`，并在 `Open Questions` 中给出解除条件；不得写成已经确认可实现。

### 8. API, Data, Auth, Storage & Payment（按需）

只展开当前范围实际触发的子节。

API / provider 至少写明：服务用途、请求输入、响应结果、超时/失败/限流、服务端边界和所需环境变量名。

Data / Auth / Storage 至少写明：是否登录、角色权限、保存哪些数据、数据 owner、生命周期、刷新恢复、删除策略、本地或云端存储及失败处理。

Payment 至少写明：

- `subscription / credits / one-time / mixed`；
- 内部商品与 provider product/price 的映射；
- checkout success/cancel 回跳和状态确认；
- webhook 验签、幂等键和重复通知处理；
- 权益入账、失败补偿、退款或重试边界；
- 所需环境变量名，不写真实值。

支付细节优先引用仓库已有且适用的 `docs/modules/PAYMENT.md`、`docs/modules/STRIPE.md` 或其他现有模块文档。本规则不要求创建新附录。

Analytics 仅在触发时写事件名、触发条件、必要属性、隐私边界和成功指标；不得默认采集用户输入原文或敏感信息。

### 9. Mobile & Responsive

除非用户明确要求仅桌面端，否则默认 mobile-first，并至少覆盖 `320 / 375 / 390 / 412 / 768 / 1024`。

必须写明：

- 页面级不得横向滚动；
- 宽表格、图表、代码块、tabs 或列表使用组件内滚动；
- 输入区域可收缩，关键按钮、单位和操作不得被挤出；
- 导航和工具栏在窄屏下的折行、堆叠或横滑策略；
- 至少 5 条可直接测试的移动端验收项，覆盖 320px 主流程、溢出、关键操作、宽内容和长文本。

### 10. Error States, Security & Privacy

错误项使用 `ERR-xxx`，写明用户看到什么、系统如何处理、能否重试和下一步。按适用情况覆盖：

- 空输入、格式错误、空结果、网络失败、复制或下载失败；
- API 超时、限流、provider 失败或无效响应；
- 未登录、权限不足、保存失败、刷新恢复；
- 上传失败、文件类型/大小限制、处理超时；
- 支付取消、失败、webhook 延迟/重复、权益未到账；
- credits 是否扣除、耗尽提示和升级路径。

安全与隐私必须说明：

- 用户输入、结果、文件和历史是否保存或发送给第三方；
- 日志不得记录用户输入全文、生成结果全文、凭据或敏感个人信息；
- API key、secret、token、OAuth secret、webhook secret 和数据库 URL 只能位于服务端 secret 配置；
- 是否需要更新 Privacy、Terms、Cookie 或风险提示；
- 成人、医疗、金融、版权或用户上传内容的限制（若适用）。

### 11. UI Copy & i18n

- 用户可见文案集中记录，关键文案使用 `COPY-xxx`；
- 为页面标题、CTA、表单、状态、toast、warning、error 和 FAQ 提供实际站点语言文案；
- 每条关键文案给出使用场景、i18n namespace/key 和复用或新增判断；
- 最终文案不得硬编码在业务组件中；
- 用户已定制文案不得擅自覆盖；设计稿文案仅作占位，除非用户确认。

术语较多或存在冲突时增加 Glossary 子节，包含内部英文术语、中文解释和 UI 文案。

### 12. Design & Technical Constraints

有设计资料时列出真实文件及用途，并明确优先级：

1. PRD 的功能、状态和业务规则；
2. 当前工程的组件体系、design token 和全局样式；
3. 截图、STITCH 或参考代码的布局与视觉比例。

说明页面区块、组件职责、状态 owner、复用/改造/新增原则及禁止事项。PRD 不写死未验证的目标文件路径、具体命令或逐步实现方案。

技术约束只写会影响产品实现的条件，例如 Next.js App Router、next-intl、服务端边界、部署环境、provider 限制和配置变量名。Secret 只列变量名和用途。

### 13. Non-Goals

每条明确“不做什么”和原因，例如范围外、下一阶段或明确排除。`Confirmed Next Phase` 和 `Possible Later` 不应重复伪装成当前 Non-Goal 实现说明。

### 14. Open Questions

只保留真正未决的问题，每项包含：

- `Question`
- `Impact area`
- `Blocking: Yes / No`
- `Current implementation impact`
- `Owner`
- `Needed by`
- 已采用的临时假设（如有）

`Blocking: Yes` 不得同时写成已确认需求；`Blocking: No` 不得阻止后续生成不受影响的任务。

## 五、条件专项规则

### 5.1 外部服务与配置

只在当前范围触发时记录 provider 名称、能力、复用或新增、缺失配置影响和环境变量名。Provider 未确认且影响核心功能时标记阻塞；若仅阻塞真实联调，可先定义 mock/UI 边界。

AI 图片项目必须同时引用 `docs/playbooks/ai-image-architecture.md` 并说明模型注册表、套餐权益、Provider adapter、生成执行服务、私有访问和删除生命周期分别采用 `Reuse / Configure / Extend / Defer / Not required` 中的哪一种处理。不得因为模板已经存在这些能力，就默认本项目必须启用登录、历史、支付或私有存储。

### 5.2 Existing Baseline 处理

对于模板已有但当前不启用的 Login、Dashboard、Pricing、Billing、Blog、Admin、Newsletter 或 Analytics，明确选择保留、隐藏入口、redirect、noindex、不触碰或删除。不得仅因当前不用就删除代码。

### 5.3 简单项目

简单前端工具仍必须写目标、范围、页面、流程、功能需求、移动端、基本错误、安全/隐私结论、Non-Goals 和 Open Questions；不需要用空章节模拟复杂 SaaS。

## 六、PRD Self-Check

保存前逐项检查并修正：

1. 当前范围、已有能力、下一阶段、可能以后和 Non-Goals 没有混淆。
2. 上游重要内容都有明确去向或 `Explicitly Overridden` 记录。
3. P0 已收敛；P1 假设已回写；P2 为 non-blocking。
4. 没有要求用户决定可由仓库或默认规则确定的底层技术细节。
5. 每个需要实现或验证的 Current Scope 项都有稳定 ID。
6. ID 唯一、稳定，且没有因更新文档而无故重排。
7. 至少有一条从入口到结果的完整 Interaction Flow。
8. 正式需求可实现、可验证，不使用模糊措辞。
9. Blocked 需求和 `Blocking: Yes` 问题一致。
10. 页面、路由、导航和模板入口都有明确处理方式。
11. 模板已有能力没有被自动加入 Current Scope。
12. API、Data、Auth、Storage、Payment 和 Analytics 只在触发时展开。
13. 当前基础设施结论没有被 Possible Later 或模板能力推动。
14. 外部 provider 的用途、配置缺失影响和变量名清楚。
15. 没有真实 key、secret、token、URL 凭据或敏感值。
16. 支付触发时覆盖 checkout、webhook、幂等、权益和失败补偿。
17. 数据或上传触发时说明保存、第三方传输、生命周期和删除策略。
18. 错误状态说明用户反馈、系统行为、重试和下一步。
19. 安全、隐私、日志和 Legal 更新判断与实际能力一致。
20. 默认 mobile-first，并覆盖指定断点和页面级无横向滚动。
21. 至少 5 条移动端验收项可直接测试。
22. UI 文案有场景和 i18n key，且未覆盖用户定制文案。
23. 设计参考没有被当作新增功能或最终文案来源。
24. Non-Goals 每条包含排除内容和原因。
25. Open Questions 只保留真实未决项，并正确标记 Blocking。
26. PRD 没有实现步骤、命令、代码或 tasks 清单。
27. 文件路径为 `docs/project/PRD.md`，标题下有角色和语言说明。
28. 文件为 UTF-8，无 BOM、乱码或 mojibake。
29. AI 图片项目已读取 `docs/playbooks/ai-image-architecture.md`，并明确现有生图能力的复用、配置、扩展或暂缓边界。

## 七、最终约束

1. 只生成或更新 `docs/project/PRD.md`，不得开始实现。
2. 不得为了填满模板展开未触发能力。
3. 不得自行扩大用户确认的范围或恢复 Non-Goals。
4. 不得编造文件路径、provider、价格、业务规则、法律承诺或 secret。
5. 后续任务必须以 PRD 的稳定 ID 和范围分类为准。
