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

- Chapter 0 is the only version evolution record.
- Chapter 1 describes only the current document identity.
- Chapter 2 gives boundary overview; Chapter 8 gives detailed collaboration behavior.
- Chapter 3 lists first-level coverage; Chapter 7 expands the complete current functional tree.
- Chapter 4 summarizes permissions; Chapters 6-8 show their behavior in paths and functions.
- Chapter 5 describes business-object/process/state flows; Chapter 6 describes complete user paths.
- Every Chapter 6 story maps to Chapter 7 and, when applicable, Chapter 8.
- Chapter 7 remains the primary body even when it becomes very long.
- Product-visible limits and failure behavior stay with their Chapter 7 or 8 requirement.
- An unresolved product decision must not appear elsewhere as a definitive rule.

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

Prefer one consistent second-level dimension inside a functional domain. Do not mix menu, role, page type, and iteration version arbitrarily.

The final split level is the smallest unit that can be explained and accepted independently.

### 5.2 Leaf-function completeness

Each current leaf function states, when applicable:

```text
stable function ID
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

### 5.3 Page and operation granularity

- A menu with different list, detail, create, edit, delete, approval, import, export, or special-operation rules must expand those differences.
- Do not summarize ten different submenus in ten one-line rows when their fields and behaviors differ.
- A page containing operations with different permissions, states, or acceptance results must split them into leaf functions or explicit rule blocks.
- One task spanning several pages may be organized by the user matter if page relations are clear.
- Do not merge distinct behavior merely to shorten the table of contents.
- Do not create empty layers for visual symmetry.

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

An unconfirmed draft may temporarily list blockers, but they must not conflict with definitive body text.

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
```

### 10.2 Final chains

Verify:

```text
source requirement -> disposition and body destination
role -> menu/action/data permission
current leaf function -> Chapter 6 story or justified not-applicable
story -> Chapter 7 requirement
external story -> Chapter 7 and Chapter 8
flow -> trigger, actor, state, response, result
product field -> display/input/source/required/validation/linkage rule
function -> testable acceptance
pending item -> no contradictory definitive body statement
requirement-unit change -> complete Chapter 0-10 impact row
frozen/inherited block -> manifest -> final file exact text
```

### 10.3 Review scope by mode

| Mode | Function semantic review | Global-rule semantic review |
| --- | --- | --- |
| 多材料基线重建 | All current effective functions | All current effective global rules |
| 单文档重构 | All rewritten/completed functions; consistency check for direct migration | All rewritten/completed rules; consistency check for direct migration |
| 基线增量升级 | All changed functions; association regression for inherited functions | All changed global rules; association regression for inherited rules |

Random sampling cannot replace the required semantic-review scope.
