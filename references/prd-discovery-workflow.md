# PRD Discovery And Lossless Assembly Workflow

Use this workflow for every complete PRD task. It controls material ingestion, version inheritance, product confirmation, requirement-unit writing, persistence, recovery, and final assembly.

## Contents

1. Capability And Target Check
2. Mode And Processing-Depth Selection
3. Mode-Specific Workspace
4. Material And Version Governance
5. Current System Map
6. Requirement Units
7. Content Blocks And State Transitions
8. Staged Confirmation Workflow
9. Multi-Material Baseline Reconstruction
10. Single-Document Restructuring
11. Baseline Incremental Upgrade
12. Pending-Item Control
13. Context Recovery
14. Lossless Assembly
15. Quality Validation
16. Formal Baseline Gates
17. Trace-Driven Skill Iteration
18. Engineering Lifecycle Hook

## 1. Capability And Target Check

### 1.1 Runtime capability

Before deep processing, verify:

```text
all declared source materials can be read
intermediate files can be persisted
chapter fragments can be written without truncation
the deterministic assembler can run
text or SHA-256 verification can run
```

If any capability is missing:

- disclose the exact limitation and affected source or output;
- do not claim lossless, resumable, or formal-baseline completion;
- do not replace unreadable evidence with model inference;
- deliver only a bounded partial result or an unconfirmed draft.

### 1.2 Initial target confirmation

Perform a light scan, then ask product to confirm:

```text
system/product name
document scope
excluded scope
processing mode
preliminary target output version
```

Do not deeply atomize materials before these are confirmed. The scan may inspect headings, revision records, filenames, dates, and obvious material relationships.

### 1.3 Source-sufficiency gate

Before selecting a processing mode, decide whether the supplied evidence can
recover the user's intended target scope.

```text
trusted current full baseline
or
sufficient historical/iteration materials to reconstruct the full target scope
or
one document that itself claims and demonstrates full target-scope coverage
```

A local iteration PRD usually proves only its change scope. It does not prove
unchanged historical functions, roles, paths, fields, or rules.

If evidence is insufficient:

1. Identify the missing baseline or historical scope.
2. Ask product to provide it or explicitly reduce the target scope.
3. Do not select `单文档重构` merely because only one file was supplied.
4. Do not promise a formal full PRD from a local iteration document.
5. If product explicitly insists on continuing, produce only a bounded
   `未确认版完整 PRD 草案` and state that unchanged system behavior is not recovered.

### 1.4 Final identity confirmation

Before formal assembly, confirm again:

```text
system name
target version
product baseline date
formal version label
generation date
final filename
```

Suggested filename:

```text
<系统名称>PRD-<版本号>_完整版_<正式标记>_基线<YYYYMMDD>_生成<YYYYMMDD>.md
```

This product-named file is the only formal Full PRD output and the canonical
baseline for future incremental upgrades. Do not generate a separate fixed-name
baseline or a second product-named copy.

## 2. Mode And Processing-Depth Selection

Mode describes the relationship between inputs and the desired output. Depth describes how much content must be rebuilt.

### 2.1 Processing modes

| Input relationship | Mode |
| --- | --- |
| Multiple historical, iteration, meeting, prototype, or fragment sources without a trusted current full baseline | 多材料基线重建 |
| One PRD requiring template migration, normalization, or selective completion | 单文档重构 |
| One trusted full baseline plus new iteration or fragment requirements | 基线增量升级 |

Additional rules:

- A rough current PRD plus historical iteration materials is `多材料基线重建`.
- A document with a different chapter structure but complete content is `单文档重构`.
- A trusted full PRD plus a new iteration PRD is `基线增量升级`.
- One local iteration PRD without a trusted baseline is insufficient evidence,
  not automatically `单文档重构`.
- Do not label the input merely `合规` or `不合规`; state mode and depth.

### 2.2 Processing depths

```text
仅检查
局部调整
部分重构
完整重建
```

Assess depth using:

```text
template match
content completeness
functional structure clarity
cross-chapter consistency
requirement detail
version identity completeness
```

A structurally different but detailed document may need only migration. A correctly titled but shallow document may require partial or complete reconstruction.

## 3. Mode-Specific Workspace

The following is the logical maximum workspace. Create only what the selected mode and material complexity require.

```text
prd-workspace/
├── PRD-CONTROL.md
├── source-ledger/
│   ├── source-inventory.md
│   ├── material-index.md
│   ├── requirement-ledger.md
│   ├── migration-ledger.md
│   ├── applicability-matrix.md
│   ├── permission-ledger.md
│   ├── structure-decision-record.md
│   ├── cross-cutting-rule-ledger.md
│   ├── migration-preservation-check.md
│   ├── function-inventory-ledger.md
│   ├── function-code-policy.md
│   ├── trace-issue-taxonomy.md
│   ├── form-detail-ledger.md
│   ├── message-notification-ledger.md
│   ├── object-lifecycle-ledger.md
│   ├── derived-list-time-rule-ledger.md
│   ├── current-system-map.md
│   ├── coverage-matrix.md
│   └── extracts/
├── function-packs/
│   └── <requirement-unit>/
│       ├── source-evidence.md
│       ├── source-extract.md
│       ├── local-anchor-contract.md
│       ├── chapter-block.md
│       ├── consumption-map.md
│       └── local-gate-report.md
├── global-packs/
├── chapters/
│   ├── 00-05-global.md
│   ├── 06-user-stories/
│   ├── 07-functions/
│   ├── 08-collaboration/
│   ├── 09-pending.md
│   └── 10-appendix.md
├── ASSEMBLY-MANIFEST.md
└── <系统名称>PRD-<版本号>_完整版_<正式标记>_基线<YYYYMMDD>_生成<YYYYMMDD>.md
```

For Gold Set-like or otherwise high-risk units, scaffold the pack before
drafting local prose:

```bash
python3 scripts/init_requirement_unit_pack.py \
  --root prd-workspace \
  --unit <requirement-unit> \
  --gate <form-detail|workflow-permission-message|object-lifecycle|derived-list-time-rule>
```

If the runtime cannot execute the script, create the same files manually using
`references/requirement-unit-pack-templates.md`.

When a filesystem and Python runtime are available, initialize the workspace
through the lifecycle hook:

```bash
python3 scripts/prd_lifecycle_hook.py init-workspace \
  --workspace prd-workspace \
  --source <source-document> \
  --system-name <system-name> \
  --target-version <version>
```

The hook creates control files and ledgers only. Hook 不生成 PRD 正文.

### 3.1 Required artifacts by mode

| Mode | Required | Conditional |
| --- | --- | --- |
| 多材料基线重建 | source-inventory, material index, requirement ledger, structure-decision-record, function-inventory-ledger, applicability-matrix, permission-ledger, current system map, coverage matrix, needed requirement-unit packs, chapter fragments, assembly manifest | source extracts, migration ledger, cross-cutting-rule-ledger, migration-preservation-check, source-evidence, local-anchor-contract, chapter-block, consumption-map, local-gate-report |
| 单文档重构 | source-inventory, migration ledger, structure-decision-record, function-inventory-ledger, current system map, coverage matrix, chapter fragments, assembly manifest | requirement ledger, extracts, requirement-unit packs for rewritten/completed content and synthesized story/function/collaboration coverage, migration-preservation-check, source-evidence, local-anchor-contract, chapter-block, consumption-map, local-gate-report |
| 基线增量升级 | source-inventory, baseline registration, change set, function-inventory-ledger, applicability-matrix, permission-ledger, impact analysis, target-version working copy, chapter fragments, assembly manifest | affected requirement-unit packs, local ledger, version diff, cross-cutting-rule-ledger, migration-preservation-check, source-evidence, local-anchor-contract, chapter-block, consumption-map, local-gate-report |

Clean input must not be atomized merely to make every artifact exist.
Clean input also must not be collapsed into one catch-all artifact when the
target output requires complete user stories, function details, or external
collaboration. If Chapter 6, 7, or 8 text is newly synthesized, each covered
function or small related batch needs a requirement-unit record even when the
source was a single document.

### 3.2 `PRD-CONTROL.md`

This is the control compass and recovery entry point. It records:

```text
confirmed target and version identity
processing mode and depth
source list and processing state
current system map and global-rule list
current requirement unit
requirement-unit 0-10 impact index
confirmed/frozen/inherited content blocks
open conflicts and product decisions
last safe persistence point
next safe action
```

It is a process artifact and does not enter the final PRD.

### 3.3 Source inventory

`source-inventory` is the first material-control artifact. It exists to avoid
silent baseline mistakes and missing side-materials.

| Source ID | File/material | Material type | Version/date | User-declared role | Discovered role | Include? | Exclusion or risk | Readability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Material types include:

```text
formal baseline
iteration PRD
meeting note / chat trace
prototype / screenshot
attachment / appendix
Excel / message template
mobile material
external system specification
historical reference
unknown local candidate
```

Rules:

1. Ask product to confirm any source whose discovered role conflicts with the
   user-declared role, especially main baseline versus latest iteration.
2. Register local materials discovered near the declared source path when their
   names or headings match the target system, platform, message, mobile, or
   external-collaboration scope.
3. Do not ingest unknown local candidates silently. Mark them `pending
   confirmation` or explicitly excluded.
4. If a source cannot be read, record it as unreadable and state the affected
   requirement scope before continuing.

### 3.4 Material index

| Source ID | File/material | Type | Version/date | Applicable scope | Relationship | Part count | State |
| --- | --- | --- | --- | --- | --- | --- | --- |

Relationships:

```text
current baseline
incremental addition
local replacement
historical reference
explicitly obsolete
pending confirmation
```

A source may have different relationships for different functions. Do not assign one whole-document precedence when only a local section changed.

### 3.5 Requirement ledger

| Requirement ID | Requirement unit | Source/location | Version | Original requirement | Change type | Predecessor | Effective state | Conflict | Destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Change types:

```text
新增 / 修改 / 删除 / 替换 / 重申 / 冲突 / 无法判断
```

Effective states:

```text
有效 / 已修改 / 已删除 / 已替换 / 待确认
```

Keep enough original text and location information to recover meaning. The ledger is not a compressed summary.

### 3.6 Migration ledger

| Migration ID | Original location | Original content/block | Target chapter/unit | Treatment | State | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Treatments:

```text
原样迁移
低风险规范化
拆分迁移
合并迁移
经产品确认删除
排除范围
待确认
```

### 3.7 Structure decision record

Create `structure-decision-record` before drafting Chapters 6-8.

| Decision ID | Scope | Candidate structure | Chosen structure | Why | Rejected structures | Product confirmation | Impacted chapters |
| --- | --- | --- | --- | --- | --- | --- | --- |

Candidate structures:

```text
business lifecycle
page / menu
business object
role
resource type / object type
workflow state
external system
mixed with explicit ownership
```

Rules:

1. Pick the dimension that lets a reviewer reconstruct the product blueprint.
2. Resource type / object type can be a subdimension, but cannot become a
   standalone top-level module when the product lifecycle is shared.
3. If the user rejects a structure in a trace or review, update this record and
   migrate affected content through `migration-preservation-check`.

### 3.8 Applicability matrix

Use `applicability-matrix` for every new, modified, or version-overridden rule.

| Rule ID | Source requirement | Resource type / object type | Platform side | Role | Flow/state node | Page/location | Operation | External system | Applies to | Does not apply to | PRD destination |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

1. A later change applies only to the explicitly targeted object, page, role,
   platform side, operation, or external collaboration.
2. When applicability is unclear, preserve the older broader rule and mark the
   new rule as pending confirmation instead of silently generalizing it.
3. Chapter 7 and 8 prose must repeat the applicability boundary in product
   language when misapplication would change behavior.

### 3.9 Permission ledger

Use `permission-ledger` to separate permission types.

| Permission ID | Role | Menu permission | Page/list button permission | Flow-node button permission | Data permission | External platform control permission | Source | Affected functions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Definitions:

```text
菜单权限: whether a role can see or enter a menu/page.
页面/列表按钮权限: whether a role can see, enable, or execute a page operation.
流程节点按钮权限: workflow/APaaS/BPM-controlled action availability by node.
数据权限: object, organization, region, owner, or submitted-data scope.
外部平台控制权限: action ownership held by an external system or engine.
```

Rules:

1. Chapter 4 summarizes permissions globally; Chapter 7 repeats the concrete
   page and operation behavior where it affects visible elements.
2. Do not mix workflow-node buttons into ordinary page/list button permissions.
3. Do not infer data scope from menu access; data permission requires explicit
   source or product confirmation.

### 3.10 Cross-cutting rule ledger

Use `cross-cutting-rule-ledger` for rules that constrain multiple pages,
functions, detail sections, external collaborations, or messages.

| Rule ID | Rule name | Source | Rule type | Applies to functions/pages | Detail destinations | Message / external destinations | Local exceptions | Acceptance impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rule types include:

```text
attachment
message notification
evaluation / report
common navigation
shared field behavior
shared status display
external jump / return
resource-instance display
audit / record
```

The final PRD may keep a global rule unit, but each affected Chapter 7 or 8
function must still contain or reference the concrete local behavior.

### 3.11 Migration preservation check

Use `migration-preservation-check` whenever accepted prose, detailed content,
or an independent PRD is moved into another structure.

| Check ID | Accepted content source | Target location | Preservation unit | Required detail anchors | Result | Missing / changed details | Fix |
| --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

1. 已接受详细内容 is evidence. Do not re-summarize it during copy-into,
   renumbering, or chapter migration.
2. 结构迁移不得重新摘要. It may rename headings, move paragraphs, split tables,
   or add cross-references, but it must not reduce fields, buttons, prompts,
   validation, status, permissions, external paths, messages, or acceptance.
3. If the target document has a different structure, migrate detail anchors
   first, then polish wording.

### 3.12 Function code policy

Use `function-code-policy` to decide stable IDs.

| Candidate | Code? | Prefix | Reason | Parent / owner | Notes |
| --- | --- | --- | --- | --- | --- |

Rules:

1. Assign `F-` only to real functions, list pages, detail pages, create/edit
   pages, key business actions, or global product rules that need traceability.
2. Do not assign `F-` to parent categories, ordinary field rules, validation
   rows, prompts, or acceptance rows unless they are independently reusable
   global product rules.
3. Child rules inherit the owning `F-` and use local rule IDs when necessary.
4. Keep `US- / F- / EXT- / PEND-` references consistent across Chapters 6-9.

### 3.13 Function inventory coverage gate

Run `function-inventory-coverage-gate` before creating or updating the Function
总览检查表 and Chapter 7 功能结构总览. The gate exists to catch functions that
are visible in architecture, OCR, summary, role, or permission material but do
not have a rich detailed-function section yet.

Create `function-inventory-ledger.md`:

| Candidate ID | Normalized function | Source-location | Source type | Evidence | Coverage disposition | Function ID | Target section | Pending ID | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Candidate sources must include, where present:

```text
目录 / TOC
功能架构 diagrams or OCR text
功能汇总 tables
角色权限 / 菜单权限 descriptions
detailed body headings
screenshot text or prototype OCR
attachment and appendix indexes
```

Coverage disposition values:

```text
include-in-overview
merge-into-existing-function
explicit-exclusion
pending-for-product-confirmation
```

Rules:

1. Do not build the leaf-function list only from detailed body headings.
2. A candidate function must not disappear because it is marked 待定, has 正文缺失,
   comes only from OCR, or lacks a full detailed section. It must be listed in
   the Function 总览检查表 as To Generate, mapped to an existing `F-`, explicitly
   excluded with reason, or converted into a `PEND-` item.
3. When included, the Function 总览检查表 and Chapter 7 功能结构总览 must preserve
   its `source-location` and coverage disposition until product confirms or
   generation is complete.
4. Role-only, menu-only, or OCR-only candidates may still receive a stable `F-`
   if the product exposes them as leaf functions. If the product boundary is
   unclear, use pending-for-product-confirmation, not silent deletion.
5. Reconcile `function-inventory-ledger`, Function 总览检查表, Chapter 7 功能结构总览,
   `function-code-policy`, and `coverage-matrix` before declaring Chapter 7
   complete.
6. Run the engineering hook before the leaf loop:

```bash
python3 scripts/prd_lifecycle_hook.py validate-function-coverage \
  --workspace prd-workspace \
  --overview "prd-workspace/Function 总览检查表.md"
```

没有通过 coverage gate，不得进入 leaf loop. 工程 Hook 负责阻断 this class of
coverage failure so conversation state or context compression cannot silently
skip a candidate function.

### 3.14 Coverage matrix

| Function ID | Function | Source requirements | Roles | Stories | Flow/state | Chapter 7 | Chapter 8 | Acceptance | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

It proves:

```text
source requirement
-> current function
-> role/story/flow
-> Chapter 7/8
-> acceptance
```

It does not replace the 0-10 impact index or `function-inventory-ledger`.

### 3.15 Evidence-locked local fidelity loop

High-risk requirement units use an evidence-locked local loop before prose can
enter `chapters/`.

| Artifact | Purpose | Constraint |
| --- | --- | --- |
| `source-evidence.md` | Locked evidence set for one requirement unit | Preserve verbatim or table-preserving source content with stable source IDs and locations; do not replace with prose summary |
| `source-extract.md` | Working extraction and grouping | May reorganize evidence, but cannot override or replace `source-evidence` |
| `local-anchor-contract.md` | Required local prose anchors | Generated from fixed gate profile plus requirement-unit evidence; missing-source anchors become pending items, not silent omissions |
| `chapter-block.md` | Candidate prose for Chapter 6/7/8/9 | Must consume every required local anchor or state `不涉及` / pending explicitly |
| `consumption-map.md` | Trace from evidence and ledgers into local prose | Record `source-evidence -> ledger row -> local anchor -> chapter-block section` |
| `local-gate-report.md` | Local fidelity verdict | Record `pass / fail`, missing anchors, weak anchors, and global-only anchors |

Rules:

1. `source-evidence` is mandatory for Gold Set-like or otherwise high-risk
   requirement units. A later `source-extract` may compress for working
   convenience, but fidelity is judged against `source-evidence`.
2. `local-anchor-contract` is required before drafting local prose. Do not let
   the model decide coverage solely from free-form intuition.
3. `consumption-map` is required before freezing any high-risk local block.
4. A requirement-unit local gate failure blocks freeze even when the full PRD
   still passes global quality checks.
5. For tooling, `local-anchor-contract.md` uses a machine-readable table with
   the exact headers `anchor_id | anchor | required_terms | weak_terms`. Use
   `/` in `required_terms` for required sub-anchors, and ` or ` inside one
   sub-anchor for acceptable aliases. `weak_terms` may use `/` as a simple list.
6. For tooling, `consumption-map.md` uses a machine-readable table with the
   exact headers `anchor_id | chapter_section | evidence_refs | ledger_refs`.
7. `scripts/validate_requirement_unit_gate.py` is the default local gate
   implementation for high-risk requirement units.
8. `scripts/init_requirement_unit_pack.py` is the default scaffold for these
   artifacts, and `references/requirement-unit-pack-templates.md` is the
   manual fallback reference.

### 3.16 Gold Slice regression controls

Gold Set v0.1 contains four regression gates. 不要求逐字复制 Gold Slice，但必须覆盖每个 slice 的保真锚点。

| Gate | Trigger | Required anchors | Optional specialized ledger |
| --- | --- | --- | --- |
| form-detail gate | create/edit/detail page with many fields, nested forms, or validation rules | 入口、按钮、嵌套表单、字段、展示规则、填写规则 | form-detail-ledger |
| workflow-permission-message gate | multi-step workflow, approval, responsibility review, message, or external jump | flow-node buttons, menu/page/data/external permissions, detail operations, status changes, message template/trigger/log behavior | message-notification-ledger |
| object-lifecycle gate | business object or resource moves through association, cancellation, completion, or external state sync | object states, resource types, association rules, external consistency, detail sections | object-lifecycle-ledger |
| derived-list-time-rule gate | list is generated from state/time rules rather than direct CRUD | list generation, threshold, calculation type, task ID, reminder, feedback, anti-duplicate behavior | derived-list-time-rule-ledger |

Use specialized ledgers only when the normal ledgers would hide the anchors. They are not mandatory templates. They make high-risk details visible enough for confirmation, migration, and regression checks.

`gold-slice-regression-check` is a final review step for any document covering Gold Set v0.1-like behavior. It checks whether the generated PRD preserves the relevant anchors; it does not compare prose byte-for-byte.

## 4. Material And Version Governance

### 4.1 Source evidence

Use source evidence in this order as an investigation signal:

```text
current-session product decision
user-identified formal baseline
explicit product decision record
applicable iteration document
meeting note or chat record
prototype or screenshot
historical document
model inference
```

This order does not authorize silent resolution of product conflicts.

Screenshots and prototypes prove only visible labels, elements, layouts, states, and navigation. They do not prove hidden permissions, validation, data sources, business transitions, or backend behavior.

### 4.2 Version identities

Keep these separate:

```text
source latest version
existing formal baseline version
iteration material version
target output baseline version
```

Rules:

1. Read revision records and explicit version relations before filenames.
2. A filename is evidence, not authority over contradictory document content.
3. The user confirms the target output version.
4. If no version exists for a first formal baseline, suggest `V1.0.0` or ask the user to specify one.
5. If baseline is `V1.3.2` and an iteration is explicitly `V1.3.3`, recommend `V1.3.3` but do not silently adopt it.
6. If new material has no version, do not invent a patch or minor number.
7. Latest version does not mean the latest document replaces all historical requirements.

### 4.3 Large-source partitioning

Prefer the source's own structure:

```text
functional domain
-> subfunction
-> page/flow
-> rule/appendix
```

Only split further when a unit remains too large. Never split a table row set, field definition, flow sequence, or continuous rule block arbitrarily.

Every partition records:

```text
source and original location
partition ID and neighbor relation
related functions/global rules
extracted requirement IDs
processed state
cross-part continuation
```

Material ingestion is complete only when all planned headings, tables, image explanations, and attachments are processed or explicitly excluded.

## 5. Current System Map

Recover the current system from effective requirements, not by concatenating historical tables of contents.

### 5.1 Structure

```text
functional domain
-> business object / capability group / user matter
-> page / task / operation unit
-> leaf function and rule block
```

Every current leaf function receives a stable ID such as:

```text
F-SEARCH-001
F-KNOWLEDGE-003
```

Keep the ID when a function is renamed or moved. Create new IDs only for substantive split, merge, replacement, or a new capability, and record the relationship.

### 5.2 State

Distinguish:

```text
current effective
pending retention decision
explicitly deleted
future scope
external-system capability
```

Only current effective functions enter formal Chapter 7. Pending retention decisions are blocking if they change the current baseline.

### 5.3 Structure confirmation

Confirm:

```text
first-level functional domains
second-level grouping dimension
leaf-function split/merge/move/delete relations
roles and global permissions
main flow and key states
external-system boundary
```

Do not expand detailed Chapter 7 content until the current system map is confirmed.

## 6. Requirement Units

Requirement units are the boundary for generation, confirmation, modification, and impact analysis.

```text
功能需求单元
全局规则单元
```

### 6.1 Function requirement unit

The function pack records:

```text
stable function ID and tree position
source-evidence
source requirements and version changes
current effective requirement set
roles and permissions
complete user operations and stories
page/task/element structure
product fields and rules
business/data/state rules
exceptions, failure, retry, compensation
external collaboration
acceptance
0-10 impact conclusions
local-anchor-contract
candidate chapter blocks
consumption-map
local-gate-report
pending product questions
confirmation record
```

For Gold Set-like or otherwise high-risk units, `source-evidence`,
`local-anchor-contract`, `chapter-block`, `consumption-map`, and
`local-gate-report` are not optional working notes; they are the local
fidelity contract.

Minimum closure rule:

```text
one current leaf function or explicitly related small batch
-> one function pack or recorded direct-migration disposition
-> evidence-locked local loop completed when the unit is high risk
-> complete Chapter 6/7/8 coverage or justified not-applicable
-> quality-reviewed frozen body block
```

Do not replace function packs with a single `ALL-FUNCTIONS`, `scaffold`, or
chapter-sized migration block when any new story, product behavior, exception,
external collaboration, or acceptance text is synthesized.

### 6.2 Global rule unit

Use a global rule unit when a rule cannot reasonably belong to one function and constrains multiple functions or chapters.

Examples:

```text
roles and global permissions
navigation and common entries
common page and interaction behavior
upload/download/pagination/search/error feedback
global data permission and audit behavior
product-visible system constraints
```

Give each global rule a stable ID, for example:

```text
G-ROLE-PERMISSION
G-NAVIGATION
G-COMMON-INTERACTION
```

The global pack records:

```text
source and current effective rule
applicable functions
unified behavior
exceptions
conflict resolution
verifiable outcome
0-10 impact conclusions
candidate chapter blocks
confirmation record
```

### 6.3 Impact index

For every requirement unit and every 第 0-10 章 cell, record:

```text
受影响并修改
已检查无影响
不适用（原因）
```

Record related content-block IDs and chapter locations. A change does not require every chapter to change, but it requires every chapter to be checked.

When one requirement unit affects Chapters 6, 7, and 8, assign or preserve its
stable candidate `US-`, `F-`, and `EXT-` IDs during impact planning. Record the
cross-reference relation in every affected row before drafting prose. Do not
leave an external-collaboration impact as an unlinked narrative description.

Use an explicit relationship tuple such as:

```text
US-001 <-> F-SEAL-001 <-> EXT-SEAL-001
```

Repeat all IDs in each affected Chapter 6, 7, and 8 impact row. IDs use stable
ASCII slugs or numbers; labels such as `US-电子印章申请` are names, not stable IDs.

## 7. Content Blocks And State Transitions

Content blocks are the confirmation and freeze unit.

### 7.1 Stable boundary

Block markers are used only inside frozen source files under `chapters/`:

```html
<!-- PRD-BLOCK:<block-id> START -->
confirmed body content
<!-- PRD-BLOCK:<block-id> END -->
```

Block IDs do not change because a heading is renamed or moved.
The assembled formal Full PRD file must not contain these markers.

### 7.2 Legal states

```text
草稿 -> 待确认 -> 已确认 -> 已冻结
基线继承 -> 待确认（受到变更影响时）
已冻结 -> 待确认（必须存在变更记录）
待确认 -> 草稿（产品要求重新整理时）
```

New or semantically changed content cannot jump directly to `已冻结`.

### 7.3 Unique source of truth

During review, a requirement-unit pack may contain candidate blocks. After product confirmation:

1. Copy the exact confirmed text into `chapters/`.
2. Compare text or SHA-256.
3. Mark the chapter block frozen.
4. Keep only block ID, location, confirmation record, and confirmation hash in the requirement-unit pack.

`chapters/` becomes the only source of frozen prose. Do not maintain a separately editable frozen copy in a function or global pack.

For high-risk units, the block cannot enter `chapters/` until:

```text
source-evidence complete
local-anchor-contract complete
consumption-map complete
local-gate-report = pass
```

## 8. Staged Confirmation Workflow

Do not use a fixed number of confirmation rounds.

### 8.1 System-level confirmation

Confirm progressively:

```text
target and mode
-> current system map
-> roles/global rules
-> main flow/state/external boundaries
```

### 8.2 Requirement-unit loop

For one requirement unit or a small related batch:

```text
load related source and inherited blocks only
-> calculate current effective requirements
-> identify blockers and preliminary 0-10 impact
-> scaffold the requirement-unit pack for high-risk units
-> lock source-evidence for high-risk units
-> generate local-anchor-contract from gate profile + evidence
-> product closes behavior-changing blockers
-> generate complete cross-chapter candidate blocks
-> generate consumption-map
-> run `scripts/validate_requirement_unit_gate.py`
-> product reviews the complete requirement unit
-> copy confirmed text unchanged into chapter fragments
-> verify text/SHA-256
-> freeze blocks
-> update control compass, ledgers, coverage, and impact index
```

Start with structure and behavior-changing decisions. Ask finer field, interaction, exception, and acceptance questions only for the current unit.

Do not ask product to approve every sentence or ordinary editorial normalization. Do not postpone behavior-changing questions until after detailed writing.

If the local gate reports `missing anchor`, `weak anchor`, or `global-only
anchor`, fix the local unit before product confirmation unless the issue is
explicitly converted into a pending item.

### 8.3 Complete story coverage

For every current user-operable leaf function, identify:

```text
role
business premise
goal
entry
key path
system response
important branch/exception
result
related function
related external collaboration
acceptance
```

One story may cover several continuous leaf functions only when the coverage matrix records the relationship. A non-user-operated capability must state why a story is not applicable and where its behavior is specified.

Do not classify stories to justify omission or compression.

### 8.4 Product-facing confirmation

Ask product to confirm product conclusions only. Do not ask product to approve
internal state names such as candidate blocks, chapter fragments, hashes,
manifest rows, or freeze transitions.

Every product-facing confirmation round states:

```text
current product scope
effective product conclusions to write
behavior-changing differences or conflicts
questions that affect scope, role, flow, state, data, external boundary, or acceptance
```

Internal workflow terms stay in process files and progress updates. If a
confirmation pack is written to disk, the conversation still summarizes the
product decisions so the product manager does not have to inspect multiple
files to know what to confirm.

### 8.5 Authorized default confirmation

If product explicitly authorizes default confirmation for future questions:

1. Record the authorization in `PRD-CONTROL.md`.
2. Continue the same requirement-unit loop without waiting for each reply.
3. For every simulated confirmation, record the source, product conclusion,
   and `确认方式：按用户授权默认确认`.
4. Do not downgrade to direct generation, bulk migration, or a one-shot
   scaffold. The count of covered units must still close.
5. If the source has a behavior-changing ambiguity, choose the conservative
   interpretation supported by current source evidence and record it as an
   authorized default decision. If no source-backed interpretation exists,
   keep a blocking item and do not mark a formal baseline.

## 9. Multi-Material Baseline Reconstruction

Use this mode for historical and fragmented materials without a trusted current full baseline.

### 9.1 Incremental ingestion

Allowed:

```text
source 1 -> requirement ledger
ledger + source 2 requirements -> updated ledger
updated ledger + source 3 requirements -> updated ledger
```

Forbidden:

```text
source 1 + source 2 -> rewritten PRD A
PRD A + source 3 -> rewritten PRD B
PRD B + source 4 -> rewritten PRD C
```

The accumulated object is the traceable requirement ledger, not a repeatedly rewritten PRD.

### 9.2 Current effective requirement formula

```text
当前有效需求
= 历史版本中仍有效的需求
+ 后续明确新增
+ 后续明确修改或替换后的结果
- 后续明确删除
```

Rules:

1. A later version not mentioning an old requirement does not delete it.
2. `优化`, `调整`, or `升级` does not automatically replace an old rule.
3. A modification applies only to the function, page, field, or rule explicitly targeted.
4. Delete only with explicit deletion, deprecation, replacement, or product confirmation.
5. Identical content may be marked repeated; similar but different content must remain distinct.
6. Unresolvable conflicts preserve both sources and go to product confirmation.
7. Current-session product decisions have priority and must record time and impact.

### 9.3 Context loading

When processing a function unit, load only:

```text
its effective requirements and version history
directly related roles, flows, states, and external systems
necessary global rules
source passages needed for meaning
```

When processing a global rule, load its source, applicable-function index, and necessary impacted blocks, not every function's full prose.

## 10. Single-Document Restructuring

Template migration is classification and assembly, not requirement invention.

For every original content block, record one disposition:

```text
已迁移
重复保留
经产品确认删除
排除范围
待确认
```

Rules:

1. Register each heading, table, prose block, image explanation, and appendix item in the migration ledger.
2. Map by meaning, not old chapter number.
3. One original block may split across several target chapters.
4. Several blocks may merge under one function without losing differences.
5. Normalize title, numbering, table shape, and wording only when behavior is unchanged.
6. If original prose already meets target meaning and quality, copy it directly into the target chapter block.
7. For directly migrated prose, the requirement-unit pack records mapping and impact only; it must not paraphrase it.
8. Unclear ownership or meaning goes to product confirmation.
9. If Chapter 6 stories are generated from a function list, each story must be
   concrete enough to pass Chapter 6 completeness rules; placeholders such as
   `按具体功能判断` or `按权限完成...相关业务操作` are not migration.
10. If Chapter 7 keeps original prose for traceability, remove source-only
    scaffolding from the formal body or move it to a confirmed appendix; do not
    leave `源文档依据`, OCR notes, raw HTML styles, or source chapter labels as
    substitutes for product requirements.
11. A single catch-all block for all functions is allowed only for an
    unconfirmed migration draft. A formal baseline must split rewritten or
    synthesized behavior by function/global-rule unit.

Complete migration only when no valid original content remains without a destination or explicit disposition.

## 11. Baseline Incremental Upgrade

Use:

```text
existing formal baseline
+ confirmed change set
= target output baseline
```

Procedure:

1. Register the user-designated full PRD as the existing formal baseline.
2. Lightly adopt its Chapter 0-10 structure, function locations, version identity, and reusable links; do not atomize all prose.
3. Mark untouched blocks `基线继承`.
4. Preserve the original baseline file unchanged.
5. Create a separate target-version working copy and workspace.
6. Extract additions, modifications, deletions, replacements, and unclear changes from new materials.
7. Map changes to stable function/global-rule IDs and baseline block locations.
8. Run complete Chapter 0-10 impact analysis for every changed requirement unit.
9. Load and modify only affected packs and chapter blocks.
10. Keep unaffected inherited blocks byte-for-byte unchanged.
11. Perform full semantic review for all changed functions and global rules.
12. Perform association regression checks for inherited blocks.
13. Product confirms the complete change set and target output version.
14. Freeze changed blocks and assemble a new file.
15. Chapter 0 records additions, modifications, deletions, and impact from old to new baseline.

The counts must close:

```text
changed requirement-unit count
= units with complete 0-10 impact rows
= units whose affected blocks are confirmed/frozen
```

Do not sample one changed function as proof of complete impact closure.

## 12. Pending-Item Control

Pending items must originate from:

```text
missing source information
applicable-source conflict
vague or inconsistent source
product request that omitted a necessary decision
```

Do not invent pending questions merely to populate Chapter 9.

### 12.1 Blocking item

A blocking item changes:

```text
scope
role or permission
flow or state
data meaning
functional behavior
external boundary
acceptance result
```

Product must close it before formal baseline assembly.

### 12.2 Non-blocking tracking item

It does not change the confirmed current baseline, for example a future decision explicitly excluded from this version.

Chapter 9 may retain it only when it records:

```text
source
current baseline conclusion
why it does not affect the baseline
responsible confirmer
future processing condition
```

## 13. Context Recovery

The workflow must not depend on one conversation retaining all materials.

### 13.1 Persistence after every safe unit

After material ingestion or requirement-unit confirmation, update:

```text
PRD-CONTROL.md
relevant ledger
current system map/coverage when changed
chapter fragment
block state and hash
next safe action
```

### 13.2 Recovery

On a new session, load:

```text
PRD-CONTROL.md
only the relevant ledger/map entries
current requirement-unit pack
related source passages
related chapter blocks
```

Report:

```text
completed sources/partitions
pending sources/partitions
confirmed/frozen/inherited blocks
current requirement unit
open product decisions
next safe action
```

Do not re-summarize all completed materials.

### 13.3 Local recalculation

When a source, version order, or product decision changes:

1. Locate affected requirement IDs.
2. Recalculate related requirement units.
3. Use the impact index to locate chapter blocks.
4. Return only affected frozen/inherited blocks to `待确认`.
5. Re-run source preservation, version inheritance, coverage, and cross-chapter checks.

## 14. Lossless Assembly

### 14.1 Machine-readable manifest

Use:

```markdown
<!-- ASSEMBLY-MANIFEST:START -->
| block_id | requirement_unit | source_file | state | order | sha256 | final_location |
| --- | --- | --- | --- | --- | --- | --- |
| B-0001 | G-DOCUMENT | chapters/00-05-global.md | 已冻结 | 10 | <64-character SHA-256> | 0-5 |
<!-- ASSEMBLY-MANIFEST:END -->
```

Rules:

- `source_file` points inside `chapters/`.
- `state` is only `已冻结` or `基线继承`.
- `order` is a unique integer.
- `sha256` is computed from exact UTF-8 content between block markers, excluding marker lines.
- Every registered block appears once.
- Formal body text outside registered blocks is forbidden.
- If a table of contents is required, generate and register it as a derived block before assembly.
- The final `--output` path must be inside the PRD workspace but outside `chapters/`; it must not overwrite `ASSEMBLY-MANIFEST.md` or any registered source file.
- The final formal Full PRD file contains only clean product prose; `PRD-BLOCK` comments remain in `chapters/` for source verification and are stripped from formal output.

### 14.2 Formal assembly

Run:

```bash
python3 <skill-dir>/scripts/assemble_prd.py \
  --workspace <prd-workspace> \
  --manifest <prd-workspace>/ASSEMBLY-MANIFEST.md \
  --output <prd-workspace>/<系统名称>PRD-<版本号>_完整版_<正式标记>_基线<YYYYMMDD>_生成<YYYYMMDD>.md
```

Manual model concatenation is an unverified draft, not a formal baseline.
If a copy outside the workspace is needed, first assemble and verify the single
formal Full PRD file in the workspace, then copy that verified file separately
without treating the copy as a second baseline.

The assembler validates:

```text
manifest shape
legal states
source under chapters/
output inside workspace and outside chapters/
unique block IDs and order
exact markers
source hash
final order
final clean body equals registered source-block content after marker removal
no internal block markers in final output
no duplicate or unregistered body
```

It must not generate, summarize, renumber, or rewrite product prose.
After assembly, run the assembler again with `--check-existing` to verify the
persisted final file still matches the registered source blocks.

### 14.3 Final file accessibility

After assembly:

1. Verify the canonical product-named file exists.
2. Re-open it with UTF-8 and confirm the first and last non-empty lines are
   readable.
3. If the environment cannot display, persist, or transfer the Chinese
   product-named filename reliably, create an ASCII fallback filename copy in
   the same workspace, for example:

   ```text
   full-prd-v<version>-baseline-<YYYYMMDD>-generated-<YYYYMMDD>.md
   ```

4. Record the canonical path and ASCII fallback filename in `PRD-CONTROL.md`.
5. State clearly that the product-named file remains the canonical baseline and
   the fallback is only for delivery access.

## 15. Quality Validation

Run quality validation before marking a formal baseline:

```bash
python3 <skill-dir>/scripts/validate_prd_quality.py \
  --final <prd-workspace>/<系统名称>PRD-<版本号>_完整版_<正式标记>_基线<YYYYMMDD>_生成<YYYYMMDD>.md \
  --manifest <prd-workspace>/ASSEMBLY-MANIFEST.md
```

The validator is a guardrail, not a writer. It checks for formal-output
failures such as:

```text
missing or duplicate required chapters
empty required chapter bodies
chapter titles that do not match the fixed 0-10 model
extra formal chapters outside 0-10
placeholder numbering such as 4.x, 5.x, 7.x
process wording leaked into the final body
vague substitutes for real requirements
catch-all scaffold or ALL-FUNCTIONS manifest entries
Chapter 6 lacking stable US- stories or F- function references
Chapter 7 lacking F- function IDs, entry, fields/pages, rules, exceptions, and acceptance detail
Chapter 8 lacking EXT- collaboration IDs and responsibility split when external collaboration exists
```

If validation fails:

1. Treat the failing items as feedback on the controlled output.
2. Return only the affected requirement units or derived chapter shells to
   `待确认`.
3. Fix the underlying function/global-rule content or final chapter structure.
4. Re-freeze, reassemble, and rerun quality validation.

Do not silence the validator by deleting product requirements. Fix the prose,
structure, or requirement-unit coverage that caused the failure.

## 16. Formal Baseline Gates

Use mode-equivalent evidence; do not require identical intermediate artifacts.

### 16.1 Material completeness

- All declared sources are registered.
- All planned blocks, partitions, tables, image explanations, and attachments are processed or explicitly excluded.
- Unprocessed or excluded content has a reason.

### 16.2 Requirement completeness

- Every planned requirement/content block/change item has a stable ID and source location.
- Every item enters body content, explicit exclusion, confirmed deletion, or a non-blocking tracking state.
- No current effective requirement has no destination.

### 16.3 Version completeness

| Mode | Pass condition |
| --- | --- |
| 多材料基线重建 | Historical requirements are effective, changed, replaced, deleted, or explicitly excluded; silence in a later version did not delete them |
| 单文档重构 | Revision information and current prose do not conflict; unrecoverable history is not invented |
| 基线增量升级 | Existing baseline, iteration version, complete change set, and target version form a closed relation |

### 16.4 Structure completeness

- Product confirmed the current system map.
- Every current leaf function enters Chapter 7.
- Page, task, operation, and rule distinctions are not lost through directory merging.
- Function split, merge, move, and delete relations are traceable.

### 16.5 Story completeness

- Every user-operable current leaf function maps to a complete Chapter 6 story/path.
- Every story maps to Chapter 7.
- External collaboration stories also map to Chapter 8.
- Story-not-applicable capabilities state the reason and other specification location.

### 16.6 Cross-chapter completeness

- Every requirement unit has a complete Chapter 0-10 impact row.
- Role, scope, flow, state, story, function, external collaboration, and acceptance do not contradict.
- All planned changed blocks are confirmed and frozen.
- All untouched baseline blocks are marked inherited.

### 16.7 Content quality

Every new or changed leaf function states, when applicable:

```text
tree/page/task position and entry
role, permission, and premise
page regions, elements, ordering, and operations
product field display/edit/source/required/validation/linkage rules
business, data, and state behavior
normal response and important branches
exception, failure, retry, and compensation
internal/external relation
testable acceptance
```

Every new or changed global rule states:

```text
applicable scope
constrained functions
unified rule
exception
conflict handling
verifiable result
```

Do not use `支持相关操作`, `按需展示`, `进行优化`, `异常时提示`, or `其他规则同上` as substitutes for actual requirements.

For high-risk requirement units, content quality additionally requires:

```text
locked source-evidence
profile-derived local-anchor-contract
consumption-map proving local anchor coverage
no weak-summary substitutes in place of required local anchors
```

### 16.8 Assembly completeness

The deterministic assembler must return success. Any illegal state, outside source, duplicate ID/order, missing marker, hash mismatch, order mismatch, or unregistered body blocks formal delivery.

### 16.9 Assembly and quality completeness

- The deterministic assembler returns success.
- The quality validator returns success.
- `scripts/validate_requirement_unit_gate.py` returns success for every Gold
  Set-like or otherwise high-risk requirement unit.
- Every Gold Set-like or otherwise high-risk requirement unit passes its local
  gate. Full-document checks cannot override a failed local gate.
- Manifest rows do not use `ALL-FUNCTIONS`, `scaffold.md`, or chapter-sized
  catch-all blocks to represent synthesized Chapter 6/7/8 function behavior.
- The final file has one coherent Chapter 0-9 structure, not repeated chapter
  sequences from intermediate rounds.
- Every required Chapter 0-9 section contains formal body content, not only a
  heading, placeholder, or future-completion note.

## 17. Trace-Driven Skill Iteration

Use this section when reviewing product-manager usage traces to improve the
Skill. Treat traces as feedback about the Skill's control loop, not as isolated
conversation anecdotes.

### 17.1 Classify each trace signal

| Signal | Meaning | Likely control fix |
| --- | --- | --- |
| Product asks "what should I confirm?" | Confirmation contract is too process-heavy | Rewrite confirmation prompts to product conclusions |
| Product says output is too shallow | Requirement-unit granularity or Chapter 7 depth failed | Add anti-summary gate, tests, or examples |
| Product corrects scope, role, state, or boundary | Missing blocker or conflict surfaced late | Add earlier confirmation or source-sufficiency check |
| Product asks about file name or delivery target | Final identity contract is unclear | Tighten single-file formal naming rules |
| Agent resumes at wrong point | Recovery state is under-specified | Strengthen PRD-CONTROL precedence and state schema |
| Validator passes but product rejects readability | Quality validator is missing a presentation rule | Add a validator case from the trace |
| Product says rules were applied to the wrong resource, platform, role, or flow | Applicability boundary is missing | Add or tighten `applicability-matrix` |
| Product says permissions are mismatched | Permission types were collapsed | Add or tighten `permission-ledger` |
| Product says the PRD structure is wrong | Reading structure was chosen by the agent, not confirmed | Add or tighten `structure-decision-record` |
| Product says accepted detail disappeared after merging | Structural migration compressed accepted content | Add or tighten `migration-preservation-check` |
| Product says function IDs are too broad or too noisy | Coding policy is unclear | Add or tighten `function-code-policy` |

Maintain a `trace-issue-taxonomy` when a trace reveals multiple failures:

| Issue ID | Trace source | User-visible symptom | Root control failure | Required artifact/rule | Regression check | Status |
| --- | --- | --- | --- | --- | --- | --- |

### 17.2 Convert trace issues into regression artifacts

For each recurring failure:

1. Record the user-visible symptom and the exact output boundary that failed.
2. Identify the controlled variable: confirmation clarity, requirement depth,
   chapter structure, index traceability, file identity, recovery, or validation.
3. Decide whether the fix belongs in `SKILL.md`, `references/`, or `scripts/`.
4. Add or update one deterministic validation case when the failure can be
   mechanically detected.
5. Keep subjective writing guidance in references; keep fragile structural
   checks in scripts.

Do not add every trace complaint to `SKILL.md`. The main Skill should contain
only high-level invariants and workflow. Detailed chapter/readability rules live
in `references/full-prd-chapter-rules.md`; deterministic checks live in
`scripts/validate_prd_quality.py`.

### 17.3 Iteration convenience check

Before shipping a revised Skill after trace feedback, verify:

```text
main invariants still fit in SKILL.md
new detailed rules are placed in the right reference file
new validator cases pass
at least one previous good PRD still passes quality validation
at least one known bad trace output now fails or is explicitly accepted
```

This keeps the Skill learnable for product managers while allowing the internal
control system to become stricter over time.

## 18. Engineering Lifecycle Hook

`scripts/prd_lifecycle_hook.py` is the default deterministic lifecycle hook for
single-document and multi-material full PRD generation when local code execution
is available.

It controls:

```text
init-workspace
validate-function-coverage
complete-task
validate-release-ready
```

Command responsibilities:

| Command | When | Responsibility | Must not do |
| --- | --- | --- | --- |
| `init-workspace` | After target identity is known | Create recoverable workspace, control file, source inventory, function ledger and coverage matrix | Interpret source requirements |
| `validate-function-coverage` | After `function-inventory-ledger` and Function 总览检查表 exist | Ensure every included candidate appears in overview and every pending/excluded candidate has explicit disposition | Decide product scope |
| `complete-task` | After one leaf function has been read, enriched and written by the model | Mark the task `To Check`; in authorized confirmation mode, mark it `已生成` and advance to the next `To Generate` | Generate PRD prose |
| `validate-release-ready` | Before formal assembly/release | Block release when any function remains `To Generate` / `To Check` or coverage no longer passes | Approve business ambiguity |

Hard stops:

```text
没有通过 coverage gate，不得进入 leaf loop
没有清空 To Generate / To Check，不得发布
工程 Hook 负责阻断
```

The model remains responsible for reading original source evidence, enriching
details, writing chapter blocks, and recording pending items. Product remains
responsible for business decisions. Hook 不生成 PRD 正文, does not infer missing
requirements, and does not replace product confirmation.
