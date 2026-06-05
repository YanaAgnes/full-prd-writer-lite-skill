# Full PRD Chapter Rules

## Overall Skeleton

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

## Chapter Responsibilities

| Chapter | Controls | Must Not Become |
| --- | --- | --- |
| 0 修订记录 | Version evolution of the full PRD | Detailed feature rules or duplicate final version history |
| 1 文档信息 | Current document identity, version, status, applicability | Business background or scope narrative |
| 2 系统概述 | What the system is, who uses it, core scenarios, boundaries | `当前问题 / 产品目标 / 成功指标` filler |
| 3 文档覆盖范围 | What this PRD expands, does not expand, and excludes | Detailed functional requirements |
| 4 用户角色与权限 | Roles, menu permission, button permission, data permission | Full technical permission design |
| 5 业务流程 | Business-object flows and state transitions | Page navigation map or feature list |
| 6 用户故事与使用路径 | User goals, paths, system responses, results | Page field specification or one-shot story dump |
| 7 功能需求说明 | Functional tree, operation rules, data, states, exceptions, acceptance | Vague module list or technical solution |
| 8 外部系统协同需求说明 | Product scenarios involving external systems | Pure API/interface documentation |
| 9 待确认事项 | Product requirement questions product must close | Technical task list or generic backlog |
| 10 附录 | Confirmed long materials referenced by body chapters | Dumping ground |

## Key Cross-Chapter Rules

- Chapter 0 is the only version evolution record.
- Chapter 1 describes only the current document.
- Chapter 2 defines boundary overview; Chapter 8 expands external collaboration details.
- Chapter 3 defines coverage; Chapter 7 expands the functional tree.
- Chapter 4 summarizes permissions; Chapter 7 shows permission behavior in functions.
- Chapter 5 describes system/business-object flows; Chapter 6 describes user paths.
- Chapter 7 is the main body; Chapter 10 only stores confirmed long materials that would overload Chapter 7.
- Chapter 9 contains only product requirement questions.
- A retained Chapter 6 scenario must map to a Chapter 7 or Chapter 8 requirement.
- An unresolved product decision must not appear elsewhere as a definitive rule.
- Product-visible and testable constraints stay with their related Chapter 7 or Chapter 8 requirement.

## Chapter 2 Rules

Use:

```text
2.1 背景说明
2.2 产品定位
2.3 目标用户
2.4 核心使用场景
2.5 名词解释
2.6 系统边界与上下游依赖概览
```

Do not generate fixed `当前问题 / 产品目标 / 成功指标` sections.

## Chapter 3 Rules

Use:

```text
3.1 本文档覆盖的系统模块
3.2 本文档不覆盖的系统模块 / 能力
3.3 不纳入完整版 PRD 的事项
```

3.1 is global scope only. List first-level functions/modules only. Do not write details here.

The chapter must represent the confirmed current baseline. Keep future plans, superseded functions, external-system responsibilities, and engineering delivery tasks out of the covered scope.

## Chapter 4 Rules

Use:

```text
4.1 角色说明
4.2 菜单权限
4.3 按钮权限
4.4 数据权限
```

Keep this a permission summary. External system roles do not enter this system's role table.

## Chapter 5 Rules

Use:

```text
5.1 系统主流程
5.2 核心功能流程
5.3 关键状态流转
```

Do not require every function to have a flow diagram. Generate module/function flows only when there are multiple steps, roles, states, approvals, synchronization, callbacks, external collaboration, or important branches.

## Chapter 6 Rules

Discover scenarios progressively:

```text
candidate discovery
batch screening
scenario classification
selective completion
final story generation
```

Classify scenarios:

```text
core scenario
key scenario
supporting scenario
out of scope
```

Fully describe core scenarios. Describe key scenarios to implementation/test depth. Summarize supporting scenarios. Do not force identical detail on every story.

Final core stories need role, premise, goal, entry, main path, system response, result, important branches, related function, and acceptance points.

Chapter 6 describes the user's goal and path. Do not repeat Chapter 7's complete field, component, or rule specification.

## Chapter 7 Rules

Organize by functional tree:

```text
功能域
→ 业务对象 / 业务事项 / 流程阶段 / 能力分组
→ 页面 / 清单 / 表单 / 操作单元
→ 规则块
```

Prefer business objects, business processes, and user operation paths over frontend/backend technical boundaries.

Keep relevant product-visible constraints in the function where they apply, including response expectations, file limits, batch limits, permission isolation, operation traces, user-facing errors, compatibility, and failure compensation.

Exclude one-time environment deployment, middleware changes, technical refactoring, infrastructure work, and engineering delivery tasks.

## Chapter 8 Rules

Organize by external system, then collaboration scenario/function.

For each scenario, describe user goal, system trigger point, external carrying capability, user path, system response, permission boundary, data display/transfer, exception handling, and acceptance points.

Do not write pure API docs.

Include product-visible timeout, failure, retry, manual compensation, status display, and record/audit behavior where these affect user experience or acceptance.

## Chapter 9 Rules

Only include unclear product requirement points from missing, conflicting, vague, or inconsistent input materials.

Every item must be specific, answerable, and closable by product.

Classify items as:

```text
blocking
non-blocking
future
```

- Blocking items must be resolved before a formal baseline is generated.
- Non-blocking items may remain when they do not invalidate the body; the related body text must not pretend the decision is confirmed.
- Future items are outside the current baseline and should be moved to future scope or removed.

Chapter 9 is not permission to continue writing a contradictory or structurally invalid body.

## Chapter 10 Rules

Default: do not generate appendix.

Generate only when material is confirmed, necessary, referenced by the body, and too long or complex for Chapter 7.

## Final Chain Rules

Before delivery, verify:

```text
role -> permission
scenario -> Chapter 7 or Chapter 8 requirement
flow -> state trigger and outcome
function -> acceptance point
external collaboration -> product-visible result and failure handling
critical data -> applicable source/display/edit/validation/transition rule
pending item -> no contradictory definitive statement in the body
```
