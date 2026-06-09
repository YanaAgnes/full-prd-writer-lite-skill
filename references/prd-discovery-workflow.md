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

Also keep `<prd-workspace>/FULL-PRD.md` as the canonical baseline. The
product-named file is a delivery export, not the source for future incremental
upgrades.

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
│   ├── material-index.md
│   ├── requirement-ledger.md
│   ├── migration-ledger.md
│   ├── current-system-map.md
│   ├── coverage-matrix.md
│   └── extracts/
├── function-packs/
├── global-packs/
├── chapters/
│   ├── 00-05-global.md
│   ├── 06-user-stories/
│   ├── 07-functions/
│   ├── 08-collaboration/
│   ├── 09-pending.md
│   └── 10-appendix.md
├── ASSEMBLY-MANIFEST.md
└── FULL-PRD.md
```

### 3.1 Required artifacts by mode

| Mode | Required | Conditional |
| --- | --- | --- |
| 多材料基线重建 | material index, requirement ledger, current system map, coverage matrix, needed requirement-unit packs, chapter fragments, assembly manifest | source extracts, migration ledger |
| 单文档重构 | migration ledger, current system map, coverage matrix, chapter fragments, assembly manifest | requirement ledger, extracts, requirement-unit packs for rewritten/completed content and synthesized story/function/collaboration coverage |
| 基线增量升级 | baseline registration, change set, impact analysis, target-version working copy, chapter fragments, assembly manifest | affected requirement-unit packs, local ledger, version diff |

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

### 3.3 Material index

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

### 3.4 Requirement ledger

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

### 3.5 Migration ledger

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

### 3.6 Coverage matrix

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

It does not replace the 0-10 impact index.

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
candidate chapter blocks
pending product questions
confirmation record
```

Minimum closure rule:

```text
one current leaf function or explicitly related small batch
-> one function pack or recorded direct-migration disposition
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
The assembled `FULL-PRD.md` must not contain these markers.

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
-> product closes behavior-changing blockers
-> generate complete cross-chapter candidate blocks
-> product reviews the complete requirement unit
-> copy confirmed text unchanged into chapter fragments
-> verify text/SHA-256
-> freeze blocks
-> update control compass, ledgers, coverage, and impact index
```

Start with structure and behavior-changing decisions. Ask finer field, interaction, exception, and acceptance questions only for the current unit.

Do not ask product to approve every sentence or ordinary editorial normalization. Do not postpone behavior-changing questions until after detailed writing.

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
- The final `FULL-PRD.md` contains only clean product prose; `PRD-BLOCK` comments remain in `chapters/` for source verification and are stripped from formal output.

### 14.2 Formal assembly

Run:

```bash
python3 <skill-dir>/scripts/assemble_prd.py \
  --workspace <prd-workspace> \
  --manifest <prd-workspace>/ASSEMBLY-MANIFEST.md \
  --output <prd-workspace>/FULL-PRD.md
```

Manual model concatenation is an unverified draft, not a formal baseline.
If a copy outside the workspace is needed, first assemble and verify `<prd-workspace>/FULL-PRD.md`, then copy that verified file separately.

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

## 15. Quality Validation

Run quality validation before marking a formal baseline:

```bash
python3 <skill-dir>/scripts/validate_prd_quality.py \
  --final <prd-workspace>/FULL-PRD.md \
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

### 16.8 Assembly completeness

The deterministic assembler must return success. Any illegal state, outside source, duplicate ID/order, missing marker, hash mismatch, order mismatch, or unregistered body blocks formal delivery.

### 16.9 Assembly and quality completeness

- The deterministic assembler returns success.
- The quality validator returns success.
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
| Product asks about file name or delivery target | Final identity contract is unclear | Tighten canonical/delivery naming rules |
| Agent resumes at wrong point | Recovery state is under-specified | Strengthen PRD-CONTROL precedence and state schema |
| Validator passes but product rejects readability | Quality validator is missing a presentation rule | Add a validator case from the trace |

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
