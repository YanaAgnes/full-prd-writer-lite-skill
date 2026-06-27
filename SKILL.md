---
name: full-prd-writer-lite
description: Use when a product manager needs to generate, consolidate, migrate, complete, or incrementally update a full PRD from one or more historical PRDs, iteration documents, meeting notes, screenshots, prototypes, or scattered product materials.
version: 0.3.0-alpha.1
---

# Full PRD Writer Lite

## Target Outcome

Produce a product-confirmed, review-ready, development-ready full PRD baseline from imperfect source materials.

The formal output uses the fixed Chapter 0-10 numbering model: Chapters 0-9
are required, and Chapter 10 appears only when appendix admission conditions
are met. The Skill optimizes for requirement preservation, product closure,
complete user paths, detailed product behavior, and reproducible assembly
rather than fast one-shot generation.

## Version Record

Current Skill process version: `v0.3.0-alpha.2`.

This version introduces an engineering lifecycle hook for the failure pattern
observed in single-source full PRD generation: function candidates visible only
in OCR, architecture, role-permission material, or appendix indexes can be
missed if coverage checking is left to memory or conversation state.

`v0.3.0-alpha.2` tightens the hook-driven leaf loop: after function coverage
passes, every full PRD generation or baseline incremental upgrade must create
a canonical `TO-CHECK-FUNCTIONS.md` queue and function-pack skeletons through
the lifecycle hook before any leaf-function prose is treated as generated.
The hook now blocks task completion when source evidence, local anchors, or
consumption maps remain placeholders.

Version preservation rules:

- Previous trace-driven fidelity snapshot: `v0.2.0-alpha.3`.
- New Hook-driven lifecycle branch: `feature/hook-driven-prd-v0.3`.
- Do not overwrite prior Skill versions when making process changes; create a
  branch or tag before changing workflow, scripts, gates, or regression tests.

## Hard Invariants

- 固定使用第 0-10 章编号体系，不因输入材料结构改变章节职责；第 0-9 章必需，第 10 章按附录准入条件生成。
- 格式转换不得删除、概括或压缩有效需求。
- 第 6 章覆盖全部范围内用户故事与使用路径，不按核心、重点或辅助抽样。
- 第 7 章完整描述全部当前有效功能，不因篇幅迁往第 10 章。
- Function 总览检查表和 Chapter 7 功能结构总览必须先通过 `function-inventory-coverage-gate`：从目录 / TOC、功能架构（含 OCR）、功能汇总、角色权限/菜单权限、正文标题、截图文字和附件索引交叉抽取候选功能；候选功能不得因为待定、正文缺失、只有 OCR/角色权限来源或缺少详细正文而消失，必须进入 To Generate、明确排除或 `PEND-` 待确认。
- 没有通过 coverage gate，不得进入 leaf loop；没有清空 To Generate / To Check，不得发布；工程 Hook 负责阻断这些状态错误。
- 可执行环境允许时，必须用 `scripts/prd_lifecycle_hook.py` 执行工作区初始化、功能覆盖门禁、`TO-CHECK-FUNCTIONS.md` 叶子队列初始化、function-pack 初始化、叶子功能状态推进和发布前阻断；不得只在对话中口头声明这些状态。
- Function coverage gate 通过后、进入任何 leaf loop 前，必须运行 `scripts/prd_lifecycle_hook.py init-leaf-queue`，从 Function 总览检查表生成 canonical `TO-CHECK-FUNCTIONS.md`，并将待处理叶子功能初始化为 `To Generate`。一次性脚本合并、批量生成草稿或模型口头说明不得替代该队列。
- 叶子功能从 `To Generate` 推进到 `To Check` 时，必须运行 `scripts/prd_lifecycle_hook.py complete-task --require-packs`；若对应 `function-packs/<F-ID>/source-evidence.md`、`local-anchor-contract.md` 或 `consumption-map.md` 缺失、为空、仍含 `待填写` 或没有有效表格行，Hook 必须阻断。
- 发布前必须运行 `scripts/prd_lifecycle_hook.py validate-release-ready --require-packs`；任何 `To Generate`、`To Check`、空证据包、空锚点或空消费映射都不得发布。
- 第 7 章叶子功能执行要素检查，但不强制统一表格模板；缺少稳定原文风格或多轮拼接时采用正式 PRD 产品说明风格。
- 第 7 章不把优先级、时间要求作为完整版 PRD 功能必查要素；只有转化为产品可见约束时才写入对应功能规则。
- 第 8 章按外部系统组织，但仍按协同场景和功能写详细产品需求。
- 涉及外部协同时，第 6、7、8 章的影响映射和正文必须重复同一组稳定 `US- / F- / EXT-` 编号并相互引用。
- 第 10 章是可选附录，不是第 7 章的压缩区。
- 每个需求单元的新增、修改或删除都必须检查第 0-10 章影响。
- 产品经理负责收口所有会改变当前产品基线的问题。
- 已确认正文写入章节分片后冻结；正式文件只从冻结或基线继承正文块原样装配。
- 最终拼装不得重新概括、扩写、补写或修改冻结正文。
- 正式 Full PRD 文件必须是干净产品正文，不得暴露 `PRD-BLOCK` 标记或其他内部装配标记。
- `chapters/` 只保存冻结正文唯一真源；正式输出写为工作区根部的产品命名 Full PRD 文件，不得输出到 `chapters/` 或覆盖清单/源分片。
- 正式 Full PRD 文件本身是可重装配的 canonical baseline；不得同时维护固定名基线与产品命名副本两套正式文件。
- 面向评审的正式 PRD 必须读起来像一份完整文档，不得把 `F-USER-001`、`F-KB-001` 等需求单元标题直接串成第 6、7、8、9 章二级目录。
- 正式 PRD 必须保持 `M- / US- / F- / EXT- / PEND-` 五类索引闭环，并在正文中能从模块追到用户故事、功能、外部协同和待确认项。
- 第 0-9 章不能只有标题或空壳；每章必须有可评审的正式正文。
- 产品确认授权只减少等待，不减少需求单元处理深度；不得把授权确认降级成批量迁移或一次性脚手架生成。
- 正式基线必须同时通过装配校验和正文质量校验；装配通过只证明文本一致，不证明 PRD 质量合格。
- 高风险需求单元必须先锁定 `source-evidence`，再生成规则和正文；没有 `source-evidence`，不得写入高风险功能正文。
- 高风险需求单元必须先生成 `local-anchor-contract`，再生成 `chapter-block`；没有 `local-anchor-contract`，不得写正文块。
- 高风险需求单元正文块必须提供 `consumption-map`，证明关键证据和 ledger 已被本地正文消费；没有 `consumption-map`，不得冻结。
- 高风险需求单元必须通过 requirement-unit local gate，才可进入 `chapters/` 冻结源；不得只靠整篇 PRD 的全文级关键词检查放行。
- 最终装配只能拼接 `chapters/` 中已冻结或基线继承的正文块；不得在装配阶段重新概括、合并或润色第 7 章正文。
- 对命中 Gold Set v0.1 或同类高风险模式的需求单元，默认先用 `scripts/init_requirement_unit_pack.py` 建立 pack 骨架，再填写 `source-evidence`、`local-anchor-contract`、`chapter-block`、`consumption-map`；不得跳过骨架直接写第 7 章正文。

### Trace-Driven Fidelity Invariants

- 多材料任务必须先建立 `source-inventory`，确认主基线、迭代材料、附件、Excel、消息模板、移动端材料、外部系统说明和排除范围；不得因为文件名最新就默认其为主基线。
- 建立功能清单时必须维护 `function-inventory-ledger`，逐条记录候选功能的 `source-location`、source type、evidence、coverage disposition、目标章节和处置理由；不得只从详细正文标题生成叶子功能清单。
- 后续版本修改必须进入 `applicability-matrix`，逐条标注适用的资源类型 / 对象类型、平台端、角色、流程节点、页面、操作和外部系统；不得把局部资源或局部页面规则扩散为全系统规则。
- 权限必须进入 `permission-ledger`，区分菜单权限、页面/列表按钮权限、流程节点按钮权限、数据权限、外部平台控制权限；不得把工作流引擎控制按钮写成普通页面按钮。
- 第 6、7、8 章展开前必须记录 `structure-decision-record`，说明正文按生命周期、页面、业务对象、角色、资源类型或流程组织的理由；不得在未确认结构维度时把资源类型拆成独立模块。
- 跨页面、跨流程、跨外部系统的规则必须进入 `cross-cutting-rule-ledger`，并回填到实际页面、功能、详情页、消息或协同场景；不得把横切规则写成孤立的迭代说明。
- 对已接受详细内容做结构迁移时必须执行 `migration-preservation-check`；结构迁移不得重新摘要，不得把已接受详细内容压缩成概述。
- 正式正文必须遵守 `function-code-policy`：只有真实功能、页面、详情页、列表、关键业务动作或全局产品规则获得 `F-`；父级分类和普通子规则不滥用 `F-`。
- 每次基于用户 Trace 修订 Skill 时必须维护 `trace-issue-taxonomy`，把用户可见失败映射到控制修复和回归检查。
- 对命中 Gold Set v0.1 或同类高风险模式的需求单元，必须建立 `source-evidence`、`local-anchor-contract`、`consumption-map`、`local-gate-report`；不得用单个摘要段落替代这些中间产物。
- `source-extract` 可以是工作提炼物，但对高风险需求单元不得替代 `source-evidence`；正文保真以 `source-evidence` 为准。
- `local-anchor-contract` 必须来自固定 profile 锚点与本单元证据的交集，不得完全依赖模型自由归纳。
- requirement-unit local gate 必须区分 `missing anchor`、`weak anchor`、`global-only anchor`；`支持相关操作`、`查询条件保持一致`、`按权限控制` 一类弱表达不得充当高风险需求单元正文。

### Gold Slice Regression Gates

Gold Set v0.1 is a regression lens, not source material. 不要求逐字复制 Gold Slice，但必须覆盖每个 slice 的保真锚点。

- `form-detail gate`: create/edit/detail functions must preserve 入口、按钮、嵌套表单、字段、展示规则、填写规则, validation, state/data changes, and acceptance.
- `workflow-permission-message gate`: stateful workflow units must preserve flow-node buttons, permission layers, detail operations, status changes, message triggers, external jumps, and logs.
- `object-lifecycle gate`: business-object lifecycle units must preserve object states, resource/object types, association/withdrawal rules, external consistency, and detail sections.
- `derived-list-time-rule gate`: derived operational lists must preserve list-generation rules, time thresholds, calculation type, task IDs, feedback records, reminders, and anti-duplicate behavior.

When a requirement unit matches one of these gates, add the matching specialized ledger if the standard ledgers cannot keep the anchors visible: `form-detail-ledger`, `message-notification-ledger`, `object-lifecycle-ledger`, or `derived-list-time-rule-ledger`.

### Evidence-Locked Unit Loop

For any requirement unit that matches a Gold Slice gate or otherwise carries high compression risk, use this closed loop:

```text
source-evidence
-> applicability / permission / cross-cutting ledgers
-> local-anchor-contract
-> chapter-block
-> consumption-map
-> requirement-unit local gate
-> confirmation
-> freeze into chapters/
```

Control rules:

- `source-evidence` stores verbatim or table-preserving evidence with stable source IDs and locations. It is not a prose summary.
- `local-anchor-contract` lists the local anchors the final Chapter 7 or 8 prose must cover. Missing-source anchors become pending items; they do not disappear silently.
- `local-anchor-contract` for tooling uses a machine-readable table with `anchor_id | anchor | required_terms | weak_terms`; use `/` for required sub-anchors and ` or ` for acceptable aliases inside one sub-anchor.
- `consumption-map` records which evidence and ledger rows are consumed by which local prose section.
- `consumption-map` for tooling uses a machine-readable table with `anchor_id | chapter_section | evidence_refs | ledger_refs`.
- The requirement-unit local gate is authoritative for local fidelity. The full-document `gold-slice-regression-check` remains useful, but it cannot override a failed local gate.

## Capability Gate

深度处理前检查：

```text
材料是否均可读取
是否能够持久化中间结果
是否能够精确拼装正文
是否能够执行文本或哈希校验
```

如果存在无法读取的附件、不能落盘的环境或不能执行确定性装配校验的环境：

1. 先向用户说明限制和受影响范围。
2. 不得声称已经完成可恢复、无损的正式基线。
3. 只能输出分段结果或 `未确认版完整 PRD 草案`。
4. 不得用模型推断替代缺失材料。

## Processing Modes

先识别处理模式，再独立判断处理深度。

处理模式：

```text
多材料基线重建
单文档重构
基线增量升级
```

- **多材料基线重建**：从多份历史、迭代、会议、原型或碎片材料恢复当前系统全貌。
- **单文档重构**：对一份 PRD 进行模板迁移、规范化、局部补齐或重构。
- **基线增量升级**：在用户指定的正式完整版基线上合入新迭代，另建新版本。

模式成立前先检查材料是否足以恢复目标范围。单独一份局部迭代 PRD
不等于当前系统完整版，也不能仅因它是唯一输入就归为单文档重构。
缺少可信完整版或足够历史材料时，先要求补充材料或缩小目标范围；
用户坚持继续时只能生成明确限定范围的未确认草案。

处理深度：

```text
仅检查
局部调整
部分重构
完整重建
```

不要使用“合规/不合规”代替模式和深度判断。

## Default Interaction

默认先分析、确认，再生成。用户说“生成完整 PRD”不表示允许跳过确认。

默认路径：

```text
轻量扫描
-> 确认系统、范围、排除范围、模式、初步目标版本
-> 建立 source-inventory 并确认主基线、附件和排除材料
-> 建立 function-inventory-ledger 并执行 function-inventory-coverage-gate
-> 用 scripts/prd_lifecycle_hook.py validate-function-coverage 阻断漏项
-> 用 scripts/prd_lifecycle_hook.py init-leaf-queue 生成 TO-CHECK-FUNCTIONS.md 和 function-packs
-> 建立 structure-decision-record 并确认正文组织维度
-> 建立当前模式必要的中间产物
-> 建立 applicability-matrix、permission-ledger、cross-cutting-rule-ledger
-> 为高风险需求单元锁定 source-evidence
-> 为高风险需求单元建立 local-anchor-contract
-> 确认系统能力地图和全局规则
-> 生成 chapter-block 与 consumption-map
-> 执行 requirement-unit local gate
-> 用 scripts/prd_lifecycle_hook.py complete-task --require-packs 推进 To Check / 已生成
-> 按需求单元分轮确认并冻结正文块
-> 对结构迁移或已接受内容执行 migration-preservation-check
-> 再次确认最终文档身份
-> 确认正式 Full PRD 文件名
-> 确定性装配和校验
-> 用 scripts/prd_lifecycle_hook.py validate-release-ready --require-packs 阻断未处理队列
-> 正文质量校验
```

交互要求：

- 大型系统按需求单元分轮推进，不要求用户一次确认全部系统。
- 每轮先确认会改变产品行为的阻断问题，再补充当前需求单元的字段、规则、异常和验收。
- 一个需求单元可以跨越多个章节；确认时必须展示其完整跨章表达。
- 用户修改已确认内容时，按需求单元成组检查和解冻，不按单章孤立修改。
- 输入越规范，越应复用原文并减少中间产物。

### Product-Facing Confirmation Contract

产品经理只确认产品结论，不确认内部工程状态。

对用户展示确认问题时：

- 说“本轮处理的产品范围、准备写入的产品口径、需要确认的差异点”。
- 不要求用户理解或判断 `候选正文块`、`章节分片`、`哈希`、`冻结`、`manifest`、`全局规则单元`、`能力域`、`写入 chapters`。
- 不让用户打开多个过程文件自行找重点；如需落盘过程文件，也必须在对话里给出本轮需要确认的完整产品口径。
- 内部文件状态、哈希、清单、装配动作只作为简短进度或最终校验结果汇报。

推荐确认格式：

```text
本轮处理：<产品范围>

准备写入 PRD 的产品口径：
1. ...
2. ...

需要确认的差异点：
1. ...
2. ...

可以回复：确认；或说明第几条怎么改。
```

### Authorized Confirmation Mode

当用户明确表示“后续默认确认”“涉及产品确认都按确认处理”“持续进行直到生成完整版”时，进入授权确认模式。

授权确认模式只改变等待策略：

- 不再逐轮停下来等用户回复。
- 仍必须按需求单元逐个提取来源、生成确认口径、记录“按用户授权默认确认”、写入跨章正文、冻结、更新追踪。
- 仍必须处理字段、规则、异常、失败、外部协同和验收，不得只生成模块摘要。
- 不得生成 `scaffold.md`、`ALL-FUNCTIONS` 或单个大块冒充全部功能需求单元。
- 不得跳过 `TO-CHECK-FUNCTIONS.md` 队列和 `complete-task --require-packs`。授权确认只允许 Hook 自动把已经完成证据包和正文更新的单元从 `To Check` 推进到 `已生成`，不允许把未逐项处理的功能批量标记完成。
- 如果来源不足或质量校验失败，只能继续补齐或标记为未确认草案，不能标记正式基线。

### Final Document Presentation Contract

最终只生成一个正式 Full PRD 文件：

```text
<prd-workspace>/产品名PRD-版本_完整版_状态_基线YYYYMMDD_生成YYYYMMDD.md
```

- 该文件是唯一正式 Full PRD，也是 canonical baseline，用于装配校验、哈希追踪、评审阅读和后续增量升级。
- 不额外生成固定名基线文件，也不生成产品命名副本。
- 后续版本合入该正式 Full PRD 对应的 `chapters/` 与清单体系，不从另一个副本合入。
- 文件状态优先使用 `待产品确认版`、`产品确认版`、`正式基线候选`；只有产品明确确认且无阻断项时才使用 `正式版`。
- 最终装配前必须确认系统名称、版本号、状态、基线日期、生成日期和正式 Full PRD 文件名。
- 如果中文正式文件名在当前运行环境中无法稳定落盘、展示或下载，必须生成一个可追踪的 ASCII fallback filename 副本，并执行文件可读取性校验；该副本只是交付可达性保障，不替代 canonical baseline 身份。

正式正文的阅读结构：

- 第 6 章按角色、功能域或用户目标组织用户故事；`US-` 是故事 ID，不直接作为二级目录批量铺开。
- 第 7 章按功能域组织，再展开叶子功能；`F-` 叶子功能应出现在三级或更低层标题、功能定位表和索引表中。
- 第 8 章按外部系统组织，再展开协同场景；`EXT-` 是协同 ID，不按内部功能块逐段拼接。
- 第 9 章使用统一待确认表，不按需求单元生成大量互不一致的小表。

索引闭环：

```text
M- module -> US- story -> F- function -> EXT- collaboration -> PEND- pending item
```

- 第 3 章定义 `M-` 模块索引。
- 第 6 章定义 `US-` 并引用关联 `F-` 和 `EXT-`。
- 第 7 章定义 `F-` 并引用关联 `M-`、`US-`、`EXT-` 和 `PEND-`。
- 第 8 章定义 `EXT-` 并引用关联 `US-` 和 `F-`。
- 第 9 章定义 `PEND-` 并引用关联 `M-`、`F-` 或 `EXT-`，说明当前基线结论和为什么不阻断。

跨功能关系单元可以独立保留，例如“综合检索中的知识问答展示关系”。但最终正文应采用引用式去重：主功能只保留入口性说明和引用，关系单元详细承接返回结构、展示关系、异常降级和验收。

## Main Workflow

1. 执行 Capability Gate。
2. 轻量扫描材料，识别来源版本、现有基线、材料关系和范围。
3. 判断材料是否足以恢复目标范围；不足时先补材料或缩小目标，不承诺正式完整版。
4. 向用户确认系统名称、范围、排除范围、模式和初步目标版本。
5. 加载 `references/prd-discovery-workflow.md`，按模式建立必要工作区。
6. 可执行环境允许时，运行 `scripts/prd_lifecycle_hook.py init-workspace` 初始化可恢复工作区。
7. 建立 `source-inventory`、`structure-decision-record` 和必要的 trace-control ledgers。
8. 建立 `function-inventory-ledger`，从目录 / TOC、功能架构（含 OCR）、功能汇总、角色权限/菜单权限、正文标题、截图文字和附件索引交叉抽取候选功能，并执行 `function-inventory-coverage-gate`。
9. 运行 `scripts/prd_lifecycle_hook.py validate-function-coverage`；没有通过 coverage gate，不得进入 leaf loop。
10. 恢复并确认当前系统能力地图、全局规则、角色、流程、状态和外部边界。
11. 按需求单元提取当前有效需求，处理冲突、适用范围、权限、横切规则和待确认问题。
12. 对高风险需求单元先执行 `scripts/init_requirement_unit_pack.py` 或手工建立等价骨架，再锁定 `source-evidence`，并从固定 profile 生成 `local-anchor-contract`。
13. 基于证据和 ledgers 生成该需求单元对第 0-10 章的候选 `chapter-block` 与 `consumption-map`。
14. 执行 requirement-unit local gate，识别 `missing anchor`、`weak anchor`、`global-only anchor`，未通过则补齐后再进入确认。
15. 将确认文本原样写入章节分片，执行文本或哈希比对并冻结。
16. 运行 `scripts/prd_lifecycle_hook.py complete-task`，把本轮叶子功能推进到 `To Check`；授权确认模式下可使用 `--auto-approve` 推进到 `已生成` 并指向下一项。
17. 完成全部计划内需求单元后，执行完整性、结构迁移保真、local gate 汇总和内容质量闸门。
18. 再次确认系统名称、版本号、基线日期、正式标记、生成日期和正式 Full PRD 文件名。
19. 运行 `scripts/prd_lifecycle_hook.py validate-release-ready`；没有清空 To Generate / To Check，不得发布。
20. 使用 `scripts/assemble_prd.py` 从 `chapters/` 唯一真源装配干净正式文件。
21. 使用 `scripts/assemble_prd.py --check-existing` 和 `scripts/validate_prd_quality.py` 检查正式文件一致性与正文质量。
22. 装配、质量、覆盖、可读取性、local gate 和跨章节检查全部通过后，才可标记为正式基线。

## Requirement Units And Content Blocks

需求单元是生成、修改和影响分析的基本单位：

```text
功能需求单元
全局规则单元
```

全局规则包括角色权限、导航、公共交互、上传下载、搜索、错误反馈、数据权限、审计及其他影响多个功能的产品规则。

对命中 Gold Set v0.1 或同类高风险模式的功能需求单元，需求单元包至少还必须包含：

```text
source-evidence
local-anchor-contract
chapter-block
consumption-map
local-gate-report
```

高风险需求单元正文最少要证明：

```text
source-evidence -> ledger row -> local-anchor-contract -> chapter-block -> consumption-map
```

任意链路缺口都不能冻结正文。

正文块是确认和冻结单位。合法状态：

```text
草稿 -> 待确认 -> 已确认 -> 已冻结
基线继承 -> 待确认（受到变更影响时）
已冻结 -> 待确认（必须存在变更记录）
待确认 -> 草稿（产品要求重新整理时）
```

新生成或发生语义变化的正文块不得跳过确认直接冻结。`chapters/` 中的正文块是冻结正文唯一真源；需求单元包只保存来源、映射、影响、确认记录和哈希。

对高风险需求单元，`chapter-block` 进入 `chapters/` 前必须满足：

```text
source-evidence complete
local-anchor-contract complete
consumption-map complete
requirement-unit local gate passed
```

每个需求单元必须对第 0-10 章记录：

```text
受影响并修改
已检查无影响
不适用（原因）
```

## Formal Baseline Gate

正式基线必须同时满足：

- 目标系统、范围、排除范围和目标版本已经确认。
- 所有计划内材料均已处理或明确排除。
- 材料足以证明目标范围的当前系统基线；局部迭代材料未被冒充为系统全量。
- `source-inventory` 已确认主基线、迭代材料、附件、外部来源、未纳入材料和无法读取材料。
- `function-inventory-coverage-gate` 已证明 Function 总览检查表、Chapter 7 功能结构总览和 `function-inventory-ledger` 一致；所有来自目录 / TOC、功能架构（含 OCR）、功能汇总、角色权限/菜单权限、正文标题、截图文字或附件索引的候选功能均有 `source-location` 和 coverage disposition。
- `applicability-matrix` 已证明每条迭代规则的资源类型 / 对象类型、平台端、角色、流程节点、页面、操作和外部系统适用范围。
- `permission-ledger` 已区分菜单权限、页面/列表按钮权限、流程节点按钮权限、数据权限和外部平台控制权限。
- `structure-decision-record` 已确认正文组织维度，且第 6、7、8 章没有因错误组织维度丢失业务生命周期细节。
- `cross-cutting-rule-ledger` 已将横切规则回填到受影响页面、功能、详情页、消息和外部协同。
- 涉及已接受详细内容或章节迁移时，`migration-preservation-check` 证明结构迁移不得重新摘要且没有压缩已接受详细内容。
- 有效需求均进入正文、明确排除或经产品确认删除。
- 当前系统能力地图、全局规则和角色权限已经确认。
- 第 6 章覆盖全部适用用户故事和使用路径。
- 第 7 章覆盖全部当前有效叶子功能并达到可评审、可开发深度。
- 第 8 章完整描述涉及的外部系统协同场景。
- 变更集中的全部需求单元均完成第 0-10 章影响检查。
- 会改变当前基线的阻断事项已经由产品收口。
- 所有待装配正文块均为 `已冻结` 或 `基线继承`。
- 每个正式正文块都来自具体需求单元或全局规则单元，不得使用 `ALL-FUNCTIONS`、`scaffold.md` 或单个大块代替逐功能正文。
- `ASSEMBLY-MANIFEST.md` 与章节唯一真源一致。
- `scripts/assemble_prd.py` 返回通过结果。
- `scripts/assemble_prd.py --check-existing` 返回通过结果。
- `scripts/validate_prd_quality.py` 返回通过结果。
- 对命中 Gold Set v0.1 或同类高风险模式的需求单元，`scripts/validate_requirement_unit_gate.py` 返回通过结果。
- 对 Gold Set v0.1 覆盖的功能域执行 `gold-slice-regression-check`；不要求逐字复制 Gold Slice，但必须覆盖每个 slice 的保真锚点。
- 对命中 Gold Set v0.1 或同类高风险模式的每个需求单元执行 requirement-unit local gate；不得只跑整篇 PRD 的全文级检查。
- 每个高风险需求单元都存在 `source-evidence`、`local-anchor-contract`、`consumption-map` 和 `local-gate-report`，且 local gate 结果为通过。
- 高风险需求单元正文不存在 `支持相关操作`、`查询条件保持一致`、`按权限控制`、`系统按规则处理`、`查看详情` 一类弱表达替代关键规则。
- 正式 Full PRD 文件位于 PRD 工作区根部，不污染 `chapters/` 冻结源目录。
- 正式 Full PRD 文件不包含 `PRD-BLOCK` 或其他内部装配标记。
- 正式文档使用清晰的产品命名文件名，并且只存在一个正式 Full PRD 输出。
- 第 6、7、8、9 章的二级目录是阅读结构，不是需求单元文件名列表。
- `M- / US- / F- / EXT- / PEND-` 索引能相互追踪，且待确认项不会与正文确定性规则冲突。
- 第 0-9 章均包含正式正文；不能以空章节、占位章节或待补说明占位。
- 产品明确同意生成正式完整版。

任何一项未满足，都不能标记为正式产品基线。

## Direct-Generation Degradation

只有用户明确说出类似以下指令时才跳过确认：

```text
跳过确认，直接生成
不要提问，直接输出
基于现有材料直接生成
```

此时：

1. 标记为 `未确认版完整 PRD 草案`。
2. 在第 0 章前说明材料限制、冲突、阻断项和推断风险。
3. 不把推断写成已确认事实。
4. 不把草案称为研发、测试或正式产品基线。
5. 可以使用模板生成草案，但不得伪造冻结状态或装配通过结果。

## Reference Loading

- 每个完整 PRD 任务都加载 `references/prd-discovery-workflow.md`。
- 起草或修改章节正文前加载 `references/full-prd-chapter-rules.md`。
- 对 Gold Set-like 或高风险需求单元，起草 pack 前加载 `references/requirement-unit-pack-templates.md`。
- 最终装配或生成明确要求的未确认草案时加载 `references/full-prd-template.md`。
- 多材料任务只加载当前材料分片、相关需求单元和必要全局规则，不反复载入全部材料。

## Runtime Boundaries

- 不建立 Schema、Jinja、Normalizer、数据库式追踪或多代理编排。
- 确定性脚本只用于初始化、状态推进、校验和装配：`scripts/prd_lifecycle_hook.py` 控制生命周期状态、`TO-CHECK-FUNCTIONS.md` 队列和门禁，`scripts/assemble_prd.py` 校验并拼接正文块，`scripts/validate_prd_quality.py` 校验正式正文质量；这些脚本都不得解释需求或生成产品内容。
- Hook 不生成 PRD 正文，不补写功能细节，不替代产品确认；模型负责语义整理和正文生成，产品负责业务口径确认，工程 Hook 负责阻断状态错误、漏项和未完成队列。
- `scripts/prd_lifecycle_hook.py init-workspace` 只创建可恢复目录和基础控制文件。
- `scripts/prd_lifecycle_hook.py validate-function-coverage` 只校验 `function-inventory-ledger`、Function 总览检查表和覆盖处置是否闭环。
- `scripts/prd_lifecycle_hook.py init-leaf-queue` 只从已通过覆盖门禁的 Function 总览检查表生成 canonical `TO-CHECK-FUNCTIONS.md` 和 function-pack 骨架，不得生成 PRD 正文。
- `scripts/prd_lifecycle_hook.py complete-task --require-packs` 只在证据包、锚点合同和消费映射非空且无占位符时推进 `To Generate -> To Check -> 已生成` 状态和当前指针。
- `scripts/prd_lifecycle_hook.py validate-release-ready --require-packs` 只在发布前确认没有未处理状态、覆盖门禁仍通过且证据包门禁已满足。
- `scripts/validate_requirement_unit_gate.py` 只负责校验 `source-evidence`、`local-anchor-contract`、`chapter-block`、`consumption-map` 的闭环完整性，不负责发明缺失需求。
- 一次性部署、环境、中间件、技术重构和研发交付任务不进入完整产品基线。
- 产品可见、可验证的限制仍应写入第 7 或第 8 章。
- 第 9 章问题必须来自输入缺失、材料冲突或产品提需未写清，不得为了填满章节而制造问题。
