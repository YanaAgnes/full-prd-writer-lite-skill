---
name: full-prd-writer-lite
description: Use when a product manager needs to generate, consolidate, rewrite, or baseline a complete PRD from historical PRDs, iteration documents, meeting notes, chat records, screenshots, prototypes, or scattered product descriptions.
---

# Full PRD Writer Lite

Turn mixed product materials into a current, bounded, product-confirmed PRD baseline. Optimize for content quality and product closure, not one-shot document length.

This is a lightweight skill. Do not create structured JSON, Schema/Jinja pipelines, lifecycle routing, multi-agent workflows, or database-style traceability unless the user explicitly requests an engineering system.

## Default Behavior

Use staged discovery and confirmation by default.

- A request such as `生成完整 PRD` or `用这个 Skill 生成 PRD` is not permission to skip confirmation.
- Do not generate the formal final PRD until product explicitly confirms that it may be generated.
- Batch questions and confirm only decisions that affect the product baseline.
- Merge confirmation rounds when the source materials are already clear.

For a new multi-source task, the first substantive response should contain the material index, product baseline summary, explicit conflicts/gaps, and the first confirmation batch. Do not replace visible confirmation with an unreported internal analysis.

Only skip confirmation when the user explicitly says something equivalent to:

```text
跳过确认，直接生成
不要提问，直接输出
基于现有材料直接生成最终文档
```

In that case, output an `未确认版完整 PRD 草案`, not a formal product baseline. Include a risk summary, preserve conflicts as unresolved, and never present unsupported product decisions as confirmed facts.

## Core Workflow

Load `references/prd-discovery-workflow.md` before processing multiple source materials.

### 1. Establish the Material Baseline

- Identify the target product/system, target baseline version or date, and intended scope.
- Build a material index with source, time/version, applicable scope, and disposition.
- Mark materials as current baseline, supplemental, superseded, reference-only, or pending confirmation.
- Extract explicit conflicts and missing product decisions.
- Ask the first confirmation batch: material precedence, target scope, and boundary conflicts.

### 2. Establish the Product Skeleton

- Produce the first/second-level functional tree.
- Summarize roles and menu/button/data permissions.
- Identify the main business flow and key state transitions.
- Separate this system's functions from external-system responsibilities.
- Ask the second confirmation batch: functional tree, roles, flow/state, and external boundaries.

### 3. Establish Scenarios and Requirements

- Discover the complete scenario set, then classify scenarios as core, key, supporting, or out of scope.
- Fully expand core scenarios; expand key scenarios only to the detail needed for implementation and testing; summarize supporting scenarios.
- Expand Chapter 7 and Chapter 8 requirements from the confirmed skeleton and scenarios.
- Ask the third confirmation batch: core scenarios, high-risk product gaps, and permission to generate the final PRD.

### 4. Generate and Verify

- Check the final generation gate.
- Write the PRD using `references/full-prd-template.md`.
- Apply the chapter boundaries in `references/full-prd-chapter-rules.md`.
- Run cross-chapter chain checks before delivery.

## Information Classes

Keep these classes distinct during discovery:

| Class | Meaning | Treatment |
| --- | --- | --- |
| Confirmed decision | Product explicitly confirmed it | May be written as definitive |
| Supported fact | A current applicable source states it without conflict | May be written with source retained in working notes |
| Low-risk editorial completion | Naming, formatting, ordinary wording that does not change behavior | May be standardized without asking |
| Product inference | Plausible but not stated product behavior | Must be confirmed or moved to Chapter 9 |
| Conflict | Applicable sources disagree | Must not be silently merged |

Never infer scope, permissions, state transitions, data meaning, business rules, external responsibility, failure behavior, or acceptance outcomes.

## Confirmation Rules

- Prefer 5-10 selectable decisions plus at most 1-3 open questions per batch.
- State the source, reason for confirmation, affected chapters/functions, and default handling if unanswered.
- Ask blockers first. Do not ask the user to review every sentence or every low-risk detail.
- Do not create a separate confirmation workflow for every chapter.

Use these confirmation levels:

```text
阻断：must be resolved before a formal baseline is generated
非阻断：may remain in Chapter 9 if the body is still valid
后续：outside the current baseline; move to future scope or remove
```

## Final Generation Gate

Generate a formal full PRD only when:

- target baseline and document scope are confirmed;
- material precedence is clear enough to avoid mixing old and current requirements;
- first/second-level functional tree is confirmed;
- core roles and permission boundaries are confirmed;
- main flow and key states are confirmed;
- core scenarios are confirmed;
- external-system responsibility boundaries are confirmed;
- blocking conflicts are resolved;
- remaining confirmation items do not invalidate the body;
- product explicitly confirms final generation.

If a blocker affects the main flow, permissions, state, data meaning, external boundary, or acceptance outcome, do not hide it in Chapter 9 and call the result final.

## Cross-Chapter Verification

Before delivery, verify:

```text
role -> permission
scenario -> Chapter 7 or Chapter 8 requirement
flow -> state trigger and outcome
function -> testable acceptance point
external collaboration -> product entry/display/failure handling
critical data -> source/display/edit/validation/transition rule
pending item -> no conflicting definitive statement in the body
```

## Reference Loading

- Load `references/prd-discovery-workflow.md` for multi-source discovery, conflict handling, confirmation, scenario classification, and generation gates.
- Load `references/full-prd-chapter-rules.md` before drafting or revising chapter content.
- Load `references/full-prd-template.md` only when preparing the final PRD or an explicitly requested unconfirmed draft.

## Content Boundaries

- Chapter 7 is the main requirements body. Keep short tables and rules there.
- Chapter 8 contains product-side external collaboration requirements, not API documentation.
- Chapter 9 contains source gaps or unresolved product decisions that product must close.
- Chapter 10 is optional and only contains confirmed, body-referenced material that is too long for Chapter 7.
- Exclude one-time deployment, environment, middleware, technical refactoring, and engineering delivery tasks.
- Retain product-visible and testable constraints such as response expectations, file limits, batch limits, permission isolation, audit traces, compatibility, user-facing errors, and failure compensation in Chapter 7 or 8.

## Direct-Generation Degradation

When the user explicitly skips confirmation:

1. Label the output `未确认版完整 PRD 草案`.
2. Add a short risk summary before Chapter 0.
3. Mark unsupported statements as inferred or pending.
4. Keep substantive conflicts unresolved.
5. Put blocking and non-blocking product questions in Chapter 9.
6. State that the draft is for product review and is not yet a development/test baseline.
