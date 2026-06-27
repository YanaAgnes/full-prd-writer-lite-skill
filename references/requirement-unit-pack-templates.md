# Requirement-Unit Pack Templates

Use this reference when a requirement unit matches a Gold Slice gate or
otherwise carries obvious compression risk. The goal is not to force one prose
style. The goal is to keep the local fidelity loop visible enough that the
model cannot skip from "I broadly understand it" to "I already wrote Chapter 7".

## 1. When to load this file

Load this file before drafting any of the following for a high-risk unit:

- `source-evidence.md`
- `local-anchor-contract.md`
- `chapter-block.md`
- `consumption-map.md`

Default scaffolding command:

```bash
python3 scripts/init_requirement_unit_pack.py \
  --root prd-workspace \
  --unit <requirement-unit> \
  --gate <form-detail|workflow-permission-message|object-lifecycle|derived-list-time-rule>
```

The script only creates the skeleton. It does not decide scope, infer missing
requirements, or fill the contract on your behalf.

## 2. Minimal file contract

Each high-risk requirement-unit pack should contain:

| File | Must preserve | Why |
| --- | --- | --- |
| `source-evidence.md` | 原文保真证据、来源 ID、定位 | 避免把字段/按钮/规则先压成摘要 |
| `source-extract.md` | 工作分组 | 允许重排，但不能替代证据真源 |
| `local-anchor-contract.md` | 局部锚点合同 | 把“必须写出来的点”固定下来 |
| `chapter-block.md` | 局部正文候选 | 只写当前需求单元，不偷用全局摘要 |
| `consumption-map.md` | 证据到正文的消费映射 | 证明正文真的消费了证据和 ledger |
| `local-gate-report.md` | 本地 gate 结果 | 把失败原因落下来，阻止静默放行 |

## 3. File templates

### 3.1 `source-evidence.md`

Use a table first, prose second.

```markdown
| evidence_id | source_id | location | evidence_type | content |
| --- | --- | --- | --- | --- |
| E-001 | SRC-V12 | 7.3.1 待处理需求 | text/table | 原文或表格保真内容 |
```

Rules:

- `content` 优先保留原文或表格原貌。
- 一个 evidence row 只承载一个稳定语义簇。
- 表格材料可以拆多行，但不要把字段列名和规则先合成摘要句。

### 3.2 `local-anchor-contract.md`

This file is the local fidelity contract, not a note pad.

Machine-readable table:

```markdown
| anchor_id | anchor | required_terms | weak_terms |
| --- | --- | --- | --- |
| AUD-001 | 审核入口与按钮 | 待处理需求 / 审核 | 支持相关操作 / 查看详情 |
```

Rules:

- `required_terms` 使用 `/` 表示必须同时出现的子锚点。
- 同一子锚点可用 ` or ` 表示别名。
- 只把有证据支撑的锚点写为 required。
- 固定 profile 中命中但证据不足的锚点，要转 `PEND-` 或在正文显式写 `不涉及`。

### 3.3 `chapter-block.md`

This is local prose for one unit, not a mini full PRD.

Recommended shape:

```markdown
## 元信息
- gate: `workflow-permission-message gate`
- target chapter section: 7.3 需求审核

## 局部保真检查清单
- [ ] 流程节点按钮
- [ ] 消息通知

## 正文草稿
### 7.3.1 待处理需求
...
```

Rules:

- 优先把字段、按钮、状态、权限、消息和异常写成清晰列表或表格。
- 不用 `支持相关操作`、`查询条件保持一致`、`按权限控制` 这类弱句替代锚点。
- 当前需求单元如果跨第 6、7、8、9 章，也只写它自己的跨章表达，不替别人代写。

### 3.4 `consumption-map.md`

Machine-readable table:

```markdown
| anchor_id | chapter_section | evidence_refs | ledger_refs |
| --- | --- | --- | --- |
| AUD-001 | 7.3.1 待处理需求 | E-001 / E-003 | permission-ledger:PERM-01 |
```

Rules:

- 每个 `anchor_id` 至少出现一次。
- `evidence_refs` 和 `ledger_refs` 二者至少填一个，最好都填。
- 没有被消费的证据可以留在 `source-evidence`，但没有被消费的 required anchor 不能冻结。

## 4. Gate profile seeds

`local-anchor-contract` 不是自由归纳出来的。先用固定 gate seed 扫证据，再形成 required rows。

### 4.1 form-detail gate

- 入口
- 按钮
- 嵌套表单
- 字段
- 展示规则
- 填写规则
- 校验规则
- 状态变化
- 验收

### 4.2 workflow-permission-message gate

- 流程节点按钮
- 菜单权限
- 页面/列表按钮权限
- 数据权限
- 外部平台控制权限
- 详情操作
- 状态变化
- 消息通知
- 外部跳转
- 日志/审批记录

### 4.3 object-lifecycle gate

- 业务对象状态
- 资源/对象类型
- 关联规则
- 撤销/取消规则
- 外部状态一致性
- 详情区块
- 异常分支
- 验收

### 4.4 derived-list-time-rule gate

- 列表生成规则
- 时间阈值
- 计算口径
- 任务 ID
- 提醒/催办
- 反馈记录
- 防重处理
- 验收

## 5. Fill order

For high-risk units, always fill in this order:

```text
source-evidence
-> source-extract
-> local-anchor-contract
-> chapter-block
-> consumption-map
-> local-gate-report
```

If the unit still reads like a summary after this sequence, the problem is
usually one of three things:

1. `source-evidence` already compressed the original material.
2. `local-anchor-contract` is missing gate seeds that had source support.
3. `chapter-block` used weak prose instead of enumerating the real rules.
