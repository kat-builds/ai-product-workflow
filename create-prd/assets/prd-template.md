# <产品或功能名称> 产品需求文档（PRD）

> 文档角色说明：本文件定义产品的当前范围、功能逻辑、交互流程、业务规则、页面结构与验收标准；视觉落地遵循当前工程的 design token、组件体系与 i18n 规范。

> 语言说明：本文档使用中文；面向用户的站点文案默认使用英文并通过 i18n 资源读取，代码命名、路由、字段名和内部术语使用英文。

- Last updated: YYYY-MM-DD
- Status: Draft / Confirmed / Partially Blocked
- Product decision priority: 最新用户确认 > 未被覆盖的已确认上游规格 > 仍有效的既有 PRD 决策 > 当前仓库事实 > 设计、playbook 与模板参考
- Output boundary: 本文档只定义产品需求；不得包含 tasks、实现步骤、命令、迁移、部署或 commit 指令

## 1. Introduction & Goals

### 产品概述

<产品是什么，以及本次 PRD 覆盖什么。>

### 用户问题与目标用户

- 用户问题：<具体问题>
- 目标用户：<具体人群>
- 核心价值：<可观察价值>

### 当前目标与成功标准

- `NFR-001` — <可衡量目标或验收结果>

### 已采用假设

- <仅记录不会改变核心范围的 P1 假设；没有时写“无”。>

## 2. Domain, Audience & SEO

- Domain：<域名或 TBD>
- Target region：<地区>
- Site language：<语言>
- Primary audience：<受众>
- SEO handling：<当前相关策略；不相关时简述原因>

## 3. Project Type & Scope

### Project Type

- 类型：<Simple frontend tool / Content site / API tool / AI tool / Account product / Paid product>
- PRD 展开深度：<为什么需要或不需要专项章节>

### Current Scope

- `FR-001` — <本次明确实现或改造的能力；详细定义见对应正式需求>

### Existing Baseline

- `PAGE-001` — <已有能力及 Reuse / Preserve / Hide / Redirect / Noindex / Do not touch / Delete 处理>

### Confirmed Next Phase

- <已明确承诺的下一阶段及未来影响；没有时写“无”。不得据此创建当前需求或激活当前基础设施。>

### Possible Later

- <尚未承诺的未来事项；没有时写“无”。>

### Explicitly Overridden

- <被最新用户决定覆盖的旧规格及新结论；没有时写“无”。>

### Infrastructure Decisions

| Capability | Decision | Scope basis | Notes |
|---|---|---|---|
| Database | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID 或 No Current Scope trigger> | <说明> |
| Auth | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID 或 No Current Scope trigger> | <说明> |
| Storage | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID 或 No Current Scope trigger> | <说明> |
| Payment | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID 或 No Current Scope trigger> | <说明> |
| Analytics | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID 或 No Current Scope trigger> | <说明> |

仅 `Reuse / Configure / Extend` 表示当前激活；它们的 Scope basis 必须列出 Current Scope ID。参考文档、模板能力、Existing Baseline、Confirmed Next Phase 或 Possible Later 不能单独作为当前激活依据。

## 4. User Scenarios

### 场景 1：<名称>

- 用户：<角色>
- 触发：<何时进入>
- 目标：<希望完成什么>
- 预期结果：<用户能观察到的结果>

## 5. Page Structure

### `PAGE-001` — <页面或入口名称>

- Route：`/example`
- Page role：<页面职责>
- Handling：New / Reuse / Adapt / Hide / Preserve / Do not touch / Redirect / Noindex / Delete
- Section order：<区块顺序>
- Key states：initial / empty / loading / error / success
- Primary CTA：<实际用户文案或 COPY ID>
- Navigation / footer handling：<明确处理>

## 6. Interaction Flows

### `FLOW-001` — <完整流程名称>

1. 用户从 <入口> 进入。
2. 用户执行 <操作>。
3. 系统显示 <即时反馈>。
4. 成功时显示 <结果>，并允许 <下一步>。
5. 失败时进入 `ERR-001`，用户可以 <恢复或重试>。

## 7. Functional Requirements

### `FR-001` — <单一、可判断的需求标题>

- Trigger：<用户动作或条件>
- System behavior：<系统行为和业务规则>
- User-visible result：<用户能看到什么>
- Boundaries：<不做什么或限制>
- Acceptance criteria：<可直接验证的结果>

## 8. API, Data, Auth, Storage & Payment

最终 PRD 仅保留 Current Scope 实际触发的子节并删除其余示例。简单项目直接说明所有专项能力均为 `Not required`，不得保留未触发的 ID 或占位子节。

### API / Provider（按需）

- `API-001` — <用途、输入、输出、失败/超时/限流、服务端边界、变量名>

### Data / Auth / Storage（按需）

- `DATA-001` — <账号、权限、保存内容、owner、生命周期、刷新恢复、删除和失败处理>

### Payment / Entitlement（按需）

- `PAY-001` — <模式、产品映射、checkout 回跳、webhook、幂等、权益、补偿和变量名>

### Analytics（按需）

- Event：`<event_name>`
- Trigger：<触发条件>
- Properties：<必要且非敏感属性>
- Privacy boundary：<不采集什么>
- Success metric：<如何衡量>

## 9. Mobile & Responsive

### Breakpoints

覆盖：`320 / 375 / 390 / 412 / 768 / 1024`。

### Rules

- 页面级不得横向滚动。
- 宽表格、图表、代码块、tabs 或列表只在组件内部滚动。
- 输入区域可收缩，关键按钮、单位和操作不得被挤出。
- 窄屏导航和工具栏使用明确的折行、堆叠或横滑策略。

### Mobile acceptance criteria

1. `320px` 下可以完成 `FLOW-001` 的核心路径，无页面级横向滚动。
2. `375px` 下主要输入、CTA 和结果不会重叠、截断或移出视口。
3. `390px` 下长标题、错误文案和用户输入可以换行且不遮挡操作。
4. `412px` 下宽内容仅在所属组件内部滚动。
5. `768px` 与 `1024px` 下页面从移动布局过渡后，区块顺序和关键操作保持一致。

## 10. Error States, Security & Privacy

### Error States

#### `ERR-001` — <错误名称>

- Trigger：<错误条件>
- User message：<实际英文站点文案或 COPY ID>
- System behavior：<系统如何处理>
- Retry：<是否和如何重试>
- Next step：<用户下一步>

### Security & Privacy

- Data storage：<保存什么或不保存>
- Third-party transfer：<发送什么或不发送>
- Logging：不得记录用户输入全文、结果全文、凭据或敏感个人信息。
- Secrets：仅记录环境变量名和用途，值只能位于服务端 secret 配置。
- Legal update：<Privacy / Terms / Cookie / disclosure 是否需要更新及原因>

## 11. UI Copy & i18n

| ID | Context | English copy | Namespace / Key | Decision |
|---|---|---|---|---|
| `COPY-001` | Primary CTA | `<English copy>` | `<namespace.key>` | Reuse / New / Preserve |

用户已经定制的文案、标签和 placeholder 必须保留，除非本 PRD 明确要求修改。

## 12. Design & Technical Constraints

### Design priority

1. 本 PRD 的功能、状态和业务规则；
2. 当前工程组件体系、design token 和全局样式；
3. 截图、STITCH 或参考代码的布局与视觉比例。

### Applicable project references

仅列出实际读取且由已分类范围触发的真实路径；没有时写“无”。文档存在本身不构成 Current Scope 依据。

| Reference | Why applicable | Allowed effect | Scope effect |
|---|---|---|---|
| `<verified/path.md>` | <由哪个 Current Scope、Confirmed Next Phase 或明确 baseline 决策触发> | <约束或复用边界> | Does not create Current Scope |

### Reuse and ownership

- <页面区块、组件职责、状态 owner、Reuse / Adapt / New / Do not touch 结论>

### Product-relevant technical constraints

- <例如 Next.js App Router、next-intl、服务端边界或部署限制；不写实现命令和未验证路径>

## 13. Non-Goals

- <明确不做的内容> — 原因：<范围外、下一阶段或用户明确排除>。

## 14. Open Questions

### OQ-001 — <未决问题；若没有真实未决项，写“无”并删除本示例>

- Question：<问题>
- Impact area：<范围、页面、支付、数据等>
- Options：
  - A：<当前合理方案 A>
  - B：<当前合理方案 B>
  - C：<当前合理方案 C>
- Recommended: <A / B / C>
- Reason: <一句简短推荐理由>
- Blocking：🔴Yes / No
- Current implementation impact：<当前影响>
- Owner：<负责人>
- Needed by：<阶段或日期>
- Temporary assumption：<已采用的临时假设；没有时写“无”>
