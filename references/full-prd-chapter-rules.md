# Full PRD Chapter Rules

Use these rules whenever drafting, migrating, reviewing, or changing full PRD chapter content.

## Contents

1. Overall Skeleton
2. Cross-Chapter Rules
3. Chapter 0-5 Rules
4. Chapter 6 Rules
5. Chapter 7 Rules
6. Chapter 8 Rules
7. Chapter 9 Rules
8. Chapter 10 Rules
9. Requirement-Unit Impact Rules
10. Final Quality Rules

## 1. Overall Skeleton

```text
0. 修订记录
1. 文档信息
2. 系统概述
3. 文档覆盖范围
4. 用户角色与权限
5. 业务流程
6. 用户故事与使用路径
7. 功能需求说明
8. 外部系统协同需求说明
9. 待确认事项
10. 附录
```

Chapters 0-9 are required for a formal baseline. Chapter 10 is optional and appears only when appendix admission conditions are met.

The final assembled PRD must contain one coherent Chapter 0-9 sequence, with
Chapter 10 only when appendix admission conditions are met. Do not leave
repeated `## 2.`, `## 3.`, `## 5.`, `## 6.`, `## 7.`, or `## 8.` sections
from intermediate rounds. Do not add formal Chapters 11+; iteration risks,
test cases, delivery boundaries, and confirmation conclusions must either fit
Chapter 0-10 responsibilities or be excluded from the full PRD baseline.
Requirement-unit fragments are internal assembly inputs; the formal output
reads as one document. A required chapter is not complete merely because its
heading exists; Chapters 0-9 must each contain formal, reviewable body content.

## 2. Cross-Chapter Rules

| Chapter | Controls | Must Not Become |
| --- | --- | --- |
| 0 修订记录 | Full PRD version evolution and product-change summary | Detailed feature rules or duplicate final version history |
| 1 文档信息 | Current document identity, status, version, date, scope | Business narrative or version-change details |
| 2 系统概述 | System identity, positioning, users, scenarios, terms, boundary overview | Generic `当前问题 / 产品目标 / 成功指标` filler |
| 3 文档覆盖范围 | Covered first-level domains, uncovered capabilities, excluded artifact types | Detailed requirements |
| 4 用户角色与权限 | Role description, menu, button/action, and data permission | Technical authorization design or external-system role table |
| 5 业务流程 | Main business flow, necessary function flows, key states | Page navigation list or operation manual |
| 6 用户故事与使用路径 | Complete user goals, paths, system responses, branches, outcomes | Field/component specification or selected-story sample |
| 7 功能需求说明 | Complete current functional tree and detailed product behavior | Vague module list, technical solution, or compressed summary |
| 8 外部系统协同需求说明 | Detailed product collaboration grouped by external system | Pure API documentation or external internal-function design |
| 9 待确认事项 | Traceable non-blocking product tracking items in a formal baseline | Generic backlog, technical questions, or unresolved blockers |
| 10 附录 | Confirmed, body-referenced, independently useful long material | Chapter 7 overflow or unconfirmed dumping ground |

Hard relations:

- Use stable index families consistently:

  ```text
  M- module -> US- story -> F- function -> EXT- collaboration -> PEND- pending item
  ```

- Chapter 0 is the only version evolution record.
- Chapter 1 describes only the current document identity.
- Chapter 2 gives boundary overview; Chapter 8 gives detailed collaboration behavior.
- Chapter 3 lists first-level coverage; Chapter 7 expands the complete current functional tree.
- Chapter 4 summarizes permissions; Chapters 6-8 show their behavior in paths and functions.
- Chapter 5 describes business-object/process/state flows; Chapter 6 describes complete user paths.
- Every Chapter 6 story maps to Chapter 7 and, when applicable, Chapter 8.
- A Chapter 6/7/8 relationship uses stable IDs in every direction, for example
  `US-001 <-> F-SEAL-001 <-> EXT-SEAL-001`; a descriptive label is not an ID.
- Chapter 7 remains the primary body even when it becomes very long.
- Product-visible limits and failure behavior stay with their Chapter 7 or 8 requirement.
- An unresolved product decision must not appear elsewhere as a definitive rule.
- Requirement-unit files are assembly inputs. The final PRD must not read as a
  list of `F-USER-001`, `F-KB-001`, or similar file names at Chapter 6/7/8/9
  second level. Use product reading structure first, stable IDs second.

### 2.1 Final file identity

Every formal workspace produces exactly one formal Full PRD file:

```text
<prd-workspace>/产品名PRD-版本_完整版_状态_基线YYYYMMDD_生成YYYYMMDD.md
```

- This product-named file is the canonical baseline for assembly checks, human
  review, and future incremental upgrades.
- Do not generate a separate fixed-name baseline plus a product-named copy.
- Future incremental work merges into this formal Full PRD's `chapters/` and
  manifest structure, not into a second copy.
- Use `待产品确认版`, `产品确认版`, or `正式基线候选` unless product explicitly
  confirms a true `正式版`.

Chapter 1 should make the document identity clear enough that readers know
which version, status, baseline date, generation date, and material scope they
are reading. Process-only details such as hashes and manifests stay out of the
final body.

### 2.2 Index model

Use these index families:

| Prefix | Meaning | Primary chapter | Must link to |
| --- | --- | --- | --- |
| `M-` | Module / first-level functional domain | 3 | `US-`, `F-` |
| `US-` | User story / usage path | 6 | `M-`, `F-`, optional `EXT-` |
| `F-` | Leaf function or global product rule | 7 | `M-`, `US-`, optional `EXT-`, optional `PEND-` |
| `EXT-` | External collaboration scenario | 8 | `US-`, `F-` |
| `PEND-` | Non-blocking pending item | 9 | `M-`, `F-` or `EXT-` |

The final document should provide enough overview tables for a reviewer to trace
from a module to its stories, detailed functions, external collaborations, and
remaining pending items without opening internal work files.

### 2.3 Function code policy

Formal PRDs must follow the `function-code-policy`:

- Give `F-` IDs to real functions, list pages, detail pages, create/edit pages,
  key business actions, or global product rules that need cross-chapter
  traceability.
- Do not give `F-` IDs to parent categories, ordinary field rows, validation
  rows, prompt text, status labels, or acceptance points.
- A parent category can own several `F-` children, but it is not itself a
  function unless the product exposes it as an independently operable
  capability.
- Child rules inherit the owning `F-`; use local rule numbers inside the
  function when a rule needs to be referenced.
- All `US- / F- / EXT- / PEND-` codes used in Chapters 6-9 must match exactly.
- `F-` candidates must be reconciled with `function-inventory-ledger`; a
  function seen only in 目录 / TOC, 功能架构, OCR, 功能汇总, 角色权限, 菜单权限,
  screenshots, or appendix indexes cannot be dropped merely because the source
  lacks a detailed body section.

## 3. Chapter 0-5 Rules

### 3.1 Chapter 0: 修订记录

Use:

| 需求评审时间 | 文档版本 | 内容提要 | 作者 |
| --- | --- | --- | --- |

Rules:

- Preserve known historical full-PRD version records at product-change summary level.
- If no historical record exists, write only the current version row.
- Incremental upgrade records additions, modifications, deletions, and affected scope.
- Do not include engineering logs, deployment records, field rules, or page interactions.
- Do not create another version-history chapter at the end.
- Do not leave placeholder numbering such as `0.x`, `2.x`, `4.x`, `5.x`, or
  `7.x` in a formal baseline.

### 3.2 Chapter 1: 文档信息

Include:

```text
product/system name
document name
document version
document type
document status
product baseline version
product baseline date
creation/update/generation dates
review time
author
applicable scope
related materials
```

Keep source latest version, existing baseline version, iteration version, and target output version distinct in working artifacts. Chapter 1 records the confirmed current document identity.

Recommended additional rows when delivering a formal baseline:

```text
正式文件
文件身份说明
```

Use them to state that the product-named Full PRD is the only formal output and
canonical baseline when the document is generated in a persistent PRD workspace.

### 3.3 Chapter 2: 系统概述

Use:

```text
2.1 背景说明
2.2 产品定位
2.3 目标用户
2.4 核心使用场景
2.5 名词解释
2.6 系统边界与上下游依赖概览
```

Rules:

- Describe what the system is and where it sits in the product landscape.
- Describe user groups, not detailed permission matrices.
- Core use scenarios are a system-level overview, not a replacement for Chapter 6.
- Name external systems and responsibility boundaries at overview level.
- Do not generate fixed `当前问题`, `产品目标`, or `成功指标` sections.
- Do not invent names for unknown systems or modules; use confirmed examples such as the intelligent-search system when illustration is necessary.

### 3.4 Chapter 3: 文档覆盖范围

Use:

```text
3.1 本文档覆盖的系统模块
3.2 本文档不覆盖的系统模块 / 能力
3.3 不纳入完整版 PRD 的事项
```

Rules:

- 3.1 lists first-level functional domains only.
- 3.2 records system modules/capabilities deliberately outside this document.
- 3.3 records items inappropriate for a complete product baseline, such as one-time deployment, environment, middleware, technical refactoring, and engineering delivery tasks.
- Do not place detailed function rules here.
- External-system internal capabilities do not enter covered system modules.

### 3.5 Chapter 4: 用户角色与权限

Use only:

```text
4.1 角色说明
4.2 菜单权限
4.3 按钮权限
4.4 数据权限
```

Rules:

- Role description explains what the role does, its responsibility, and purpose.
- Menu permission states visibility/access.
- Button permission states visible, enabled, and executable operations.
- Data permission states accessible object/data scope.
- Keep this chapter as a global permission summary.
- Do not include external-system roles in this system's role table.
- When a global role/permission changes, identify every constrained function and update related Chapters 6-8 behavior.
- Use the `permission-ledger` dimensions when the source distinguishes them:
  菜单权限、页面/列表按钮权限、流程节点按钮权限、数据权限、外部平台控制权限.
- Do not mix workflow/APaaS/BPM node buttons into page/list button permission.
  Workflow-node availability belongs with the flow/state behavior and the
  affected Chapter 7 operation.
- Do not infer data permission from menu permission. Data permission requires
  a source statement or product confirmation.

### 3.6 Chapter 5: 业务流程

Use:

```text
5.1 系统主流程
5.2 核心功能流程
5.3 关键状态流转
```

Rules:

- Always include the system main flow when a meaningful system process exists.
- Include function-level flows only for multi-role, multi-step, stateful, approval, callback, synchronization, external collaboration, or important branch behavior.
- Every state flow defines state, trigger, allowed actor, result, visible response, rollback/withdraw/reject/resubmit behavior when applicable.
- Do not force a diagram for simple CRUD.
- Do not put page field and button details in flow diagrams.

## 4. Chapter 6 Rules

Chapter 6 must cover the complete set of current in-scope user stories and usage paths.

Recommended reading structure:

```text
6.1 用户故事总览
6.x 按角色、功能域或用户目标展开
6.x.x US-xxx 用户故事名称
```

Do not use unnumbered `## F-xxx` or `## US-xxx` headings as the second-level
structure of Chapter 6. Stable IDs belong in story titles, summary tables, and
mapping fields.

### 4.1 Coverage source

Generate stories from:

```text
confirmed current system map
current user-operable leaf functions
roles and permissions
business flow and state
external collaboration
current effective requirements
```

Do not randomly extract selected stories from source prose.

### 4.2 Coverage requirement

- Every current user-operable leaf function maps to at least one story or complete path.
- One story may cover several continuous leaf functions only when the coverage matrix explicitly records all relationships.
- A non-user-operated capability must state why a story is not applicable and where its behavior is described.
- Story detail may vary with complexity, but no story may be omitted, truncated, or reduced to a label.
- Do not use story classification to justify summarizing or excluding requirements.

### 4.3 Story completeness

Every story states:

```text
stable story ID
related function IDs
related external-collaboration IDs
role
business premise
user goal
entry
key path
system response
important branches and exceptions
completion result
acceptance points
```

Split stories when role/permission, goal, premise, entry, main state path, external collaboration path, or acceptance result is substantively different.

Do not split ordinary clicks or fields into separate stories when they do not produce an independent user goal or result.

### 4.4 Boundary with Chapter 7

Chapter 6 explains:

```text
why the user enters
what goal is completed
where the path starts
what key steps and system responses occur
which branches matter
what result is obtained
```

Chapter 7 explains complete page areas, elements, product fields, operation rules, state/data behavior, exceptions, and acceptance detail.

Use the operation-manual principle of covering every function, but do not write Chapter 6 as button-by-button training instructions.

## 5. Chapter 7 Rules

Chapter 7 is the main product-requirement body. Completeness has priority over page count.

Before drafting or updating Chapter 7, pass `function-inventory-coverage-gate`.
The Function 总览检查表, Chapter 7 功能结构总览, `function-inventory-ledger`, and
`function-code-policy` must agree on every candidate function's source-location
and coverage disposition. Candidates marked 待定, 正文缺失, OCR-only, role-only,
or menu-only are still visible product signals: they must enter the overview as
To Generate, merge into an existing `F-` with reason, become 明确排除, or become a
`PEND-` item. They must not disappear because they lack detail; specifically,
不得因为缺少详细正文而 omit a candidate from the function inventory.

### 5.1 Required structure

```text
7.1 功能结构总览
7.x 按功能域展开的详细需求
```

Organize the detailed tree:

```text
functional domain
-> business object / capability group / user matter
-> page / task / operation unit
-> leaf function and rule
```

Recommended reading structure:

```text
7.1 功能结构总览
7.x 功能域
7.x.x 业务对象 / 能力分组 / 用户事项
7.x.x F-xxx 叶子功能名称
```

Do not generate Chapter 7 as a flat sequence of `## F-...` requirement-unit
headings. The reader should first see product domains and business objects, then
leaf function IDs.

Prefer one consistent second-level dimension inside a functional domain. Do not mix menu, role, page type, and iteration version arbitrarily.

Before drafting Chapter 7, use the confirmed `structure-decision-record`.
If the product lifecycle is shared across resource types, write lifecycle
modules first and place resource-type differences inside the affected
functions. Do not promote a resource type / object type into a standalone
module merely because a later iteration source focuses on it.

The final split level is the smallest unit that can be explained and accepted independently.

The leaf-function structure is flexible. Preserve a clear source-document
style when it is coherent and product-friendly. When the source is assembled
from multiple iterations or has no stable narrative logic, use an official PRD
product-description style: natural-language sections, short lists where useful,
and tables only when structure improves clarity.

### 5.2 Leaf-function completeness

Each current leaf function states, when applicable:

```text
stable function ID
related module ID
functional-tree location
role and permission
entry and prerequisite
page/task name and relation
page regions, elements, and ordering
available operations
product fields
business rules
data and state changes
normal system response
branches and exceptions
failure, retry, and compensation
internal-function relation
external collaboration
pending item IDs
testable acceptance
```

Product-field rules include:

```text
field name
location
display/input behavior
data source
required/optional
validation
default value
linkage
visibility/editability by role/state
```

These are product fields, not database columns, API parameters, or table schemas.

When a rule comes from a later version, preserve its applicability boundary
from `applicability-matrix` in the function text whenever it affects behavior:

```text
资源类型 / 对象类型
平台端
role
flow/state node
page/location
operation
external system
```

Do not generalize a rule to all resources, all roles, or all platforms unless
the source or product confirmation explicitly does so.

For Gold Set-like or otherwise high-risk units, Chapter 7 local prose is
controlled by this locked chain:

```text
source-evidence -> local-anchor-contract -> chapter-block -> consumption-map
```

The local prose cannot freeze until `scripts/validate_requirement_unit_gate.py`
reports no `missing anchor`, `weak anchor`, or `global-only anchor`. Whole-PRD
keyword presence does not satisfy this local requirement.

### 5.2.1 Leaf-function element check

Leaf-function generation is based on element checking, not on a mandatory
display template. For every `F-` leaf function, check whether each element
exists, applies, and should enter the formal product baseline:

| Element | Check |
| --- | --- |
| 需求内容 | Whether the function states what it is and what product problem it solves. |
| 需求背景 | Whether there is business context, trigger reason, or change reason worth preserving. |
| 页面路径 / 入口 | Whether there is a menu path, page entry, route, redirect, trigger, or non-page entry. |
| 功能说明 | Whether core interaction, input/output, business rule, and system response are clear. |
| 页面布局 / 区域元素 | Whether page regions, visible elements, ordering, and operation locations are clear. |
| 交互图 / 流程关系 | If diagrams exist, whether actors, steps, responses, and results are transcribed into text. |
| 外部依赖 | Whether the function depends on external systems, other modules, interfaces, manual work, or upstream/downstream capabilities. |
| 功能权限 | Whether role visibility, availability, and executable operations are clear. |
| 数据权限 | Whether viewable, operable, exportable, or manageable data scope is clear. |
| 历史数据 | Whether legacy data, history records, compatibility, backfill, migration, or echo behavior is involved. |
| 异常说明 | Whether no-permission, no-data, validation failure, timeout, external failure, duplicate submission, retry, or compensation behavior is clear. |
| 原型图信息 | If prototypes exist, whether page regions, elements, fields, operations, and states are extracted. |
| 补充说明 | Whether boundaries, limits, special terms, compatibility rules, or not-applicable conclusions are needed. |
| 验收口径 | Whether the function has testable acceptance points. |

If an element is not involved, has no source, or is unchanged in the current
iteration, the function may use `-`, an empty value, `不涉及`, `本次不变`, or
`沿用现有规则`. Do not use vague substitutes such as `按需展示`,
`支持相关操作`, or `按具体功能判断`.

For high-risk units, the element check must be materialized in
`local-anchor-contract` before prose is written. The contract uses a
machine-readable table with `anchor_id | anchor | required_terms | weak_terms`.
Use `/` for required sub-anchors and ` or ` for aliases inside one sub-anchor.
`consumption-map` must point every `anchor_id` to a concrete Chapter 7 section
plus evidence or ledger refs.

Do not make priority or delivery timing mandatory Chapter 7 elements in a full
PRD baseline. If source materials contain `P0/P1/P2`, launch dates, delivery
dates, or schedule constraints, keep them out of the stable function body unless
they create product-visible behavior, scope, availability, or compatibility
rules. When they are only planning metadata, keep them in working notes,
revision context, or delivery planning artifacts instead.

### 5.2.2 Official product-description style

Use this style when original function material has been stitched together over
multiple iterations or lacks a coherent authorial structure:

- Natural language is the default for 需求内容, 需求背景, 页面路径与入口,
  页面整体说明, 交互说明, 异常说明, and 补充说明.
- Write interaction as user action -> system judgment/response -> result,
  including limits and states when applicable.
- Write page layout from whole to part, commonly left to right and top to
  bottom, so readers can reconstruct the product behavior without a prototype.
- Use lists for short rule sets or acceptance points.
- Use tables only for naturally structured information such as product fields,
  resource types, role permissions, data permissions, state transitions,
  exception matrices, compatibility mappings, and acceptance matrices.
- Do not force background, requirement content, or ordinary interaction prose
  into a table merely for uniformity.

### 5.3 Page and operation granularity

- A menu with different list, detail, create, edit, delete, approval, import, export, or special-operation rules must expand those differences.
- Do not summarize ten different submenus in ten one-line rows when their fields and behaviors differ.
- A page containing operations with different permissions, states, or acceptance results must split them into leaf functions or explicit rule blocks.
- One task spanning several pages may be organized by the user matter if page relations are clear.
- Do not merge distinct behavior merely to shorten the table of contents.
- Do not create empty layers for visual symmetry.

### 5.3.1 Cross-cutting rule placement

For rules tracked in `cross-cutting-rule-ledger`, Chapter 7 must do both:

1. Keep or reference the global/cross-cutting rule once when it has a shared
   product meaning.
2. State the local effect inside each affected function, page, detail section,
   message, or operation.

Typical cross-cutting rules include attachments, evaluation/report fields,
message notifications, shared status display, external jumps, resource-instance
display, common navigation, and audit records. Do not leave these as isolated
iteration notes without local page destinations.

### 5.3.2 Gold Slice Regression Gates

Gold Set v0.1 defines four Chapter 7 preservation gates. 不要求逐字复制 Gold Slice, but the final PRD must preserve the product anchors.

| Gate | Chapter 7 placement rule |
| --- | --- |
| form-detail gate | For create/edit/detail pages, keep 入口、按钮、嵌套表单、字段、展示规则、填写规则 with role/state visibility, validation, save/submit state changes, exceptions, and acceptance. Use `form-detail-ledger` when the page spans multiple nested forms or source fragments. |
| workflow-permission-message gate | For workflow and message-heavy units, write the local workflow state and buttons inside the business function, then place 模板、触发矩阵、接收对象内容表、变量字典、日志开关 in the message function, and external jump boundaries in Chapter 8. Use `message-notification-ledger` when message rules span multiple functions. |
| object-lifecycle gate | For object/resource lifecycle units, organize around lifecycle states before resource-type differences. Preserve 库表、文件、接口、归集状态、确认完成归集、资源已注销, cancellation rules, and external name/state sync. Use `object-lifecycle-ledger` when object states are spread across pages. |
| derived-list-time-rule gate | For derived operational lists, preserve 即将超期任务清单、超期任务清单、催办反馈清单、督办编号、催办编号, generation rules, thresholds, calculation type, reminders, feedback records, and anti-duplicate behavior. Use `derived-list-time-rule-ledger` when list rows are generated from process state and time rules. |

If a unit matches a gate and Chapter 7 only says `支持管理`, `支持查询`, `支持提醒`, `相关操作`, or another summary phrase, the draft fails the gate.
If the local block omits a required anchor while the same anchor appears only
elsewhere in the full PRD, treat it as `global-only anchor` and fail the local
gate.

### 5.4 Product-visible constraints

Keep with the function where applicable:

```text
response expectation
file type/size/count limit
batch limit
permission/data isolation
operation/audit trace
compatibility visible to users
user-facing error
retry or manual compensation
```

Exclude pure technical implementation such as database design, cache replacement, infrastructure, deployment environment, or code refactoring.

### 5.5 Chapter 10 boundary

Normal function content remains in Chapter 7:

```text
page behavior
interaction rule
permission
state
exception
ordinary field table
short matrix
short enum
```

Do not move content to Chapter 10 because Chapter 7 is long.

## 6. Chapter 8 Rules

Chapter 8 is detailed product design for collaboration with external systems.

### 6.1 Organization

```text
external system
-> collaboration scenario / function
-> detailed product behavior
```

Recommended reading structure:

```text
8.1 外部系统协同总览
8.x 外部系统名称
8.x.x EXT-xxx 协同场景名称
```

Do not organize Chapter 8 primarily by internal function blocks. Internal
functions are referenced from external-system sections through `F-` IDs.

### 6.2 Scenario completeness

For every collaboration scenario, state:

```text
stable collaboration ID
related function IDs
related story IDs
user goal
trigger and entry
this system responsibility
external system responsibility
user path
identity and permission ownership
data direction and visible fields
system response
status and result display
exception and failure behavior
retry and manual compensation
record and audit behavior
acceptance points
```

### 6.3 Boundaries

- Describe what the product must do before, during, and after collaboration.
- Do not write pure API endpoints, request schemas, authentication protocols, or technical retry architecture.
- Do not place external-system internal menus, roles, approval pages, or implementation rules into this system's Chapter 7.
- If the user is redirected, embedded, or returned, describe the visible path and result.
- If data moves, describe product meaning, direction, display, ownership, and failure result.
- Keep product-visible timeout, status, failure, retry, compensation, and audit requirements.

## 7. Chapter 9 Rules

Chapter 9 must not be generated merely to look complete.

### 7.1 Source

Every item traces to:

```text
missing input
applicable-source conflict
vague or inconsistent requirement
product request missing a necessary decision
```

### 7.2 Formal baseline rule

A formal baseline cannot retain an unresolved item that changes current:

```text
scope
role or permission
flow or state
data meaning
functional behavior
external boundary
acceptance result
```

Product must close these blockers before formal assembly.

Chapter 9 may retain only non-blocking tracking items that record:

```text
related requirement unit
source
current baseline conclusion
why it does not affect the current baseline
responsible confirmer
future processing condition
state
```

Use one consistent table shape:

| 待确认编号 | 关联模块 | 关联需求 | 问题类型 | 来源依据 | 当前基线处理 | 是否阻断 | 后续处理条件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Do not generate many small Chapter 9 tables with different headers. Grouping by
module is acceptable only if the table schema stays the same.

An unconfirmed draft may temporarily list blockers, but they must not conflict with definitive body text.

### 7.3 Relationship units

A relationship unit describes behavior between two or more functions, such as
how a comprehensive-search result displays knowledge-answer content. Keep it as
an independent requirement unit when splitting it would leave no clear owner for
the acceptance boundary.

Final-body rule:

- Primary functions keep short references to the relationship unit.
- The relationship unit owns the detailed return structure, display relation,
  degradation behavior, and acceptance points.
- Do not duplicate the same detailed rules across every related function.

## 8. Chapter 10 Rules

Default: do not generate Chapter 10.

Generate an appendix only when all conditions hold:

1. The material is product-confirmed.
2. A body chapter explicitly references it.
3. It has independent reuse value.
4. It is genuinely long, structurally special, or repeatedly needed.
5. Moving it does not remove necessary local context from Chapter 7 or 8.

Typical appendix material:

```text
very long field dictionary
complete complex enum set
large permission/rule matrix
confirmed compatibility/mapping specification
confirmed source material that must remain verbatim
```

Each appendix states:

```text
applicable scope
body reference location
content owner/source
confirmed state
```

## 9. Requirement-Unit Impact Rules

A requirement-unit change is never a single-chapter edit.

For every function or global-rule unit, record its conclusions for 第 0-10 章:

```text
受影响并修改
已检查无影响
不适用（原因）
```

At minimum check:

```text
0 revision summary
1 version/status/scope identity
2 users/scenarios/terms/boundaries
3 covered and excluded scope
4 roles and permissions
5 flow and state
6 stories and paths
7 detailed functions
8 external collaboration
9 pending tracking items
10 appendix references
```

When a confirmed or frozen unit changes:

1. Create a change record.
2. Locate all related blocks through the impact index.
3. Return only actually affected blocks to `待确认`.
4. Keep checked-unaffected blocks frozen.
5. Modify the complete cross-chapter set.
6. Re-run preservation, coverage, and consistency checks.
7. Product reconfirms the whole changed set.
8. Freeze and reassemble.

## 10. Final Quality Rules

### 10.1 Forbidden substitutes for detail

Do not use these as requirements without an explicit referenced definition:

```text
支持相关操作
按需展示
进行优化
提供管理能力
异常时进行提示
其他规则同上
按功能权限配置
按具体功能判断
相关业务操作
源文档依据
```

Do not leave internal process wording in formal PRD body text:

```text
候选正文块
章节分片
哈希
manifest
本轮确认
本轮不覆盖
本轮不展开
后续确认
后续需求单元
待写入
```

If the phrase is needed for process recovery, keep it in `PRD-CONTROL.md`,
requirement-unit packs, or validation logs, not in the assembled PRD.

### 10.2 Final chains

Verify:

```text
source-inventory -> included/excluded/readability conclusion
function-inventory-ledger -> function-inventory-coverage-gate -> Function 总览检查表 / Chapter 7 功能结构总览 -> source-location and coverage disposition retained
source requirement -> disposition and body destination
applicability-matrix -> correct resource type / object type, platform side, role, flow node, page, operation, and external system boundary
role -> menu/action/data permission
permission-ledger -> menu permission, page/list button permission, flow-node button permission, data permission, external platform control permission
structure-decision-record -> Chapter 6/7/8 reading structure
cross-cutting-rule-ledger -> every local function/detail/message/external destination
current leaf function -> Chapter 6 story or justified not-applicable
story -> Chapter 7 requirement
external story -> Chapter 7 and Chapter 8
flow -> trigger, actor, state, response, result
product field -> display/input/source/required/validation/linkage rule
function -> testable acceptance
pending item -> no contradictory definitive body statement
requirement-unit change -> complete Chapter 0-10 impact row
已接受详细内容 -> migration-preservation-check -> target chapter without compression
frozen/inherited block -> manifest -> final file exact text
final file -> quality validator -> no empty required chapters, duplicate chapters, placeholder numbering, process wording, or vague substitutes
canonical filename -> file exists -> 文件可读取性校验 -> optional ASCII fallback filename when needed
Gold Set v0.1 -> gold-slice-regression-check -> 不要求逐字复制 Gold Slice -> 必须覆盖每个 slice 的保真锚点
source-evidence -> local-anchor-contract -> chapter-block -> consumption-map -> scripts/validate_requirement_unit_gate.py -> no missing anchor / weak anchor / global-only anchor
```

### 10.3 Review scope by mode

| Mode | Function semantic review | Global-rule semantic review |
| --- | --- | --- |
| 多材料基线重建 | All current effective functions | All current effective global rules |
| 单文档重构 | All rewritten/completed functions; consistency check for direct migration | All rewritten/completed rules; consistency check for direct migration |
| 基线增量升级 | All changed functions; association regression for inherited functions | All changed global rules; association regression for inherited rules |

Random sampling cannot replace the required semantic-review scope.
