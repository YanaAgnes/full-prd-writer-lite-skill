# PRD Discovery Workflow

Use this workflow before generating a formal full PRD from multiple, incomplete, conflicting, or versioned source materials.

The goal is not to confirm every sentence. The goal is to establish a product baseline that is current, bounded, internally connected, and safe for downstream use.

## Four Phases

```text
Material baseline
-> Product skeleton
-> Scenarios and detailed requirements
-> Generation gate and verification
```

Product normally participates in three confirmation rounds:

```text
Round 1: material precedence, target scope, conflicts
Round 2: functional tree, roles/permissions, flow/state, external boundaries
Round 3: core scenarios, blocking gaps, permission to generate
```

Rounds may be merged when source quality is high. Do not turn every phase or chapter into a separate meeting.

## Phase 1: Material Baseline

### 1. Establish the Target

Clarify:

```text
product/system
baseline version or baseline date
document scope
excluded scope
whether future plans are included
```

If the user does not provide a semantic version, use a concrete baseline date or a descriptive baseline name. Do not invent a release number.

### 2. Build the Material Index

| ID | Material | Type | Time/Version | Applicable Scope | Disposition | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Allowed dispositions:

```text
current baseline
supplemental
superseded
reference-only
pending confirmation
```

Do not assign one universal credibility score to an entire document. A source may be current for one module and obsolete for another. Record its applicable scope and disposition.

### 3. Summarize Only When Needed

Create a material extract card only for long documents, screenshots/prototypes, conflict-heavy sources, or sources that cannot be read as a whole.

```text
Source:
Applicable scope:
Visible/explicit facts:
Possible inference:
Conflict with:
Usable PRD information:
Questions:
```

For screenshots and prototypes:

- Treat visible fields, labels, controls, states, and navigation as evidence of visible UI only.
- Do not infer hidden permissions, validation, state rules, data sources, or backend behavior.
- When visual evidence conflicts with current written decisions, raise a conflict rather than choosing one silently.

### 4. Resolve Version and Source Relations

Use this as an initial ordering signal:

```text
current-session product decision
explicitly identified current/latest product document
explicit product decision record
applicable iteration document
meeting notes or chat record
prototype or screenshot
historical document
model inference
```

This order is not permission to silently decide substantive conflicts.

The following conflicts always require product confirmation:

```text
scope
role or permission
business flow or state transition
data meaning or ownership
business rule or acceptance outcome
external-system responsibility
failure or compensation behavior
```

### 5. Build the Conflict List

| ID | Type | Topic | Source A | Source B | Impact | Suggested Options | Level | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Conflict types:

```text
version
scope
flow/state
permission
data/rule
external boundary
acceptance
```

Levels:

```text
阻断
非阻断
后续
```

Never reconcile incompatible requirements using vague language such as `原则上`, `特殊情况下`, or `视情况而定` unless the source explicitly defines that rule.

### 6. Produce the Product Baseline Summary

Before detailed scenario or function writing, summarize:

```text
product positioning
target users and core roles
first-level covered scope
excluded scope
key business objects
main business flow
external systems and responsibility boundary
current source baseline
blocking conflicts
```

Round 1 confirmation asks product to approve or revise this summary and the material dispositions.

## Phase 2: Product Skeleton

### 1. Functional Tree

Build:

```text
functional domain
-> business object / business matter / process stage / capability group
-> page / list / form / operation unit
-> rule block
```

Confirm at least the first and second levels before expanding Chapter 7.

### 2. Roles and Permissions

Identify:

```text
role description
menu permission
button/action permission
data permission
```

Do not include external-system roles in this system's role table.

### 3. Main Flow and States

Identify:

```text
main business flow
necessary core subflows
key state names
state triggers
allowed rollback/withdraw/reject/resubmit behavior
state outcomes and visible product behavior
```

Only create function-level flows where multiple roles, steps, states, approvals, callbacks, synchronization, or important branches make a diagram useful.

### 4. External Boundaries

For each external system, establish:

```text
product collaboration scenario
this system's trigger and responsibility
external system's responsibility
data direction and ownership
user-visible result
failure and compensation behavior
```

Round 2 confirmation covers the functional tree, core roles/permissions, main flow/state, and external boundaries.

## Phase 3: Scenarios and Detailed Requirements

### 1. Discover the Scenario Set

Extract signals from roles, flows, functions, UI materials, external collaboration, and unresolved gaps.

Candidate card:

```text
SC-CAND-001 Scenario name
Role:
Goal:
Possible entry:
Related flow:
Related function:
Source:
Current gap:
Suggested classification:
Suggested action:
```

Allowed actions:

```text
keep
delete
merge
split
move to external collaboration
move to confirmation items
move out of scope
```

Batch 5-10 candidate cards at a time.

### 2. Classify Scenario Detail

Use distinct labels for scenario detail and confirmation severity:

| Classification | Treatment |
| --- | --- |
| Core scenario | Fully describe premise, main path, system response, outcome, key branches, related functions, and acceptance |
| Key scenario | Describe main path, important exception, result, related functions, and acceptance |
| Supporting scenario | Summarize role, goal, path, and result |
| Out of scope | Do not enter Chapter 6; record destination when needed |

Aim for scenario coverage, not identical detail for every scenario.

### 3. Final Story Format

```text
US-001 Scenario name

- Classification:
- Role:
- Business premise:
- User goal:
- Entry:
- Main path:
- System response:
- Completion result:
- Important exception/branch:
- Related function:
- Acceptance points:
```

Omit fields that add no value for supporting scenarios. Do not repeat Chapter 7's complete field, component, or rule specification.

### 4. Expand Requirements

Use the confirmed skeleton and scenarios to expand:

- Chapter 7: this system's functional requirements;
- Chapter 8: product-side external collaboration requirements;
- Chapter 9: unresolved product decisions.

Keep product-visible constraints with their relevant function or collaboration scenario:

```text
response expectation
file type/size limit
batch limit
permission isolation
audit trace
compatibility
user-facing error
retry or manual compensation
```

Round 3 confirmation covers core scenarios, blocking gaps, and final-generation permission.

## Question Batching

Each batch should contain:

- 5-10 selectable decisions;
- at most 1-3 open questions;
- source and conflict context;
- affected chapters/functions;
- what happens if unanswered.

Ask in this order:

```text
target and material precedence
-> blocking conflicts
-> functional tree and roles
-> flow/state and external boundary
-> core scenarios and acceptance gaps
```

Do not ask about ordinary wording, formatting, standard table organization, or other low-risk editorial completion.

## Final Generation Gate

A formal baseline may be generated when:

```text
target baseline and scope confirmed
material precedence sufficiently clear
first/second-level functional tree confirmed
core roles and permission boundaries confirmed
main flow and key states confirmed
core scenarios confirmed
external responsibility boundaries confirmed
blocking conflicts resolved
remaining items do not invalidate the body
product explicitly approves generation
```

If the user explicitly skips confirmation, generate only an unconfirmed draft and retain all blockers and risks.

## Cross-Chapter Chain Check

| Chain | Pass Condition |
| --- | --- |
| Role -> Permission | Every core role has menu/action/data boundaries |
| Scenario -> Requirement | Every retained scenario maps to Chapter 7 or 8 |
| Flow -> State | Every key transition has a trigger, permission, and outcome |
| Function -> Acceptance | Every core function has testable acceptance points |
| External collaboration -> Product behavior | Every collaboration has trigger, display/result, and failure handling |
| Critical data -> Operation | Critical data has source, visibility, edit, validation, or transition rules as applicable |
| Confirmation item -> Body | Unresolved decisions are not written elsewhere as definitive facts |
