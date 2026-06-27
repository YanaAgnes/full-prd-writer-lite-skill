# PRD 半结构化装配式 Skill 优化设计

## 1. 背景与问题

`full-prd-writer-lite` 的目标是从多份历史 PRD、迭代说明、原型和碎片材料中恢复一份可评审、可研发、可测试的完整 PRD。当前多轮优化后，skill 已经加入了 source inventory、applicability matrix、permission ledger、cross-cutting rule ledger、Gold Slice Regression Gates 等控制，但真实生成结果仍然出现严重压缩。

以 `数据需求审批 / 需求审核` 为例，gold slice 已经保留待处理列表、已处理列表、审核详情、同意/驳回按钮、节点权限、消息通知、异常审批流刷新等细节；新生成的完整 PRD 第 7.3 节却只保留了概要句。全文级回归检查仍然通过，因为权限、消息、日志等关键词散落在其他章节，不能证明需求审核本地正文完整。

这说明问题不是单纯“提示词不够强调不要压缩”，而是 skill 的执行结构仍然允许模型在最终正文阶段重新概括。下一轮优化应从“让模型写完整 PRD”转为“让模型按需求单元消费证据并装配正文”。

## 2. 目标

本次设计目标是把 skill 改造成半结构化装配器：

1. 每个高风险需求单元必须先形成结构化证据包，再生成正文。
2. 第 7 章正文必须逐项消费证据包中的字段、按钮、状态、权限、消息、异常和验收锚点。
3. 回归检查从全文级改为需求单元级，避免全文关键词假阳性。
4. 横切规则可以有全局章节，但必须回填到受影响的本地功能正文。
5. 如果局部正文未覆盖对应证据，不允许标记为正式基线，只能输出待补齐草案或失败报告。

非目标：

- 不做完整数据库、Schema、Jinja 模板或复杂编译器。
- 不要求所有功能统一成僵硬表格模板。
- 不把 gold slice 原文逐字复制进正式 PRD。
- 不追求一次性修复全系统所有历史质量问题；先解决高风险需求单元压缩。

## 3. 推荐方案

采用“半结构化装配器”方案。

### 3.1 与其他方案比较

| 方案 | 说明 | 优点 | 风险 | 结论 |
| --- | --- | --- | --- | --- |
| A. 轻量强化 Prompt | 继续增加“不要压缩”“更详细”的规则，并增强最终检查 | 改动小 | 仍会被模型摘要倾向吞掉；全文检查容易假通过 | 不推荐 |
| B. 半结构化装配器 | 每个需求单元先生成证据包，再由证据包驱动正文，并做局部 gate | 能明显降低压缩；复杂度可控 | 需要新增执行流程和局部检查脚本 | 推荐 |
| C. 强约束证据编译器 | 正文必须逐项引用 source extract / ledger，缺证据即报错 | 保真最高 | 过重，写作弹性低，维护成本高 | 暂不采用 |

推荐 B，因为它能把“证据保真”和“PRD 可读性”同时保住。

## 4. 新执行架构

### 4.1 需求单元证据包

对命中 gold gate 或高风险模式的功能，建立 `requirement-unit-pack`。每个 pack 至少包含：

| 文件 | 职责 |
| --- | --- |
| `source-extract.md` | 从原始材料摘出该需求单元相关原文、表格、OCR、迭代变更，不做摘要替代 |
| `applicability-matrix.md` | 记录每条规则适用的角色、页面、状态、资源类型、操作和外部系统 |
| `permission-ledger.md` | 拆分菜单权限、页面/列表按钮权限、流程节点按钮权限、数据权限、外部平台控制权限 |
| `cross-cutting-rule-ledger.md` | 记录消息、附件、红点、评价、外部跳转、防重复提交等横切规则及本地回填点 |
| `specialized-ledger.md` | 根据 gate 选择 form-detail、message-notification、object-lifecycle 或 derived-list-time-rule ledger |
| `local-anchor-contract.md` | 本需求单元最终正文必须覆盖的局部锚点清单 |
| `chapter-block.md` | 该需求单元准备写入第 6、7、8、9 章的正文块 |
| `local-gate-report.md` | 局部 gate 校验结果和缺失项 |

### 4.2 Local Anchor Contract

`local-anchor-contract.md` 是本次优化的关键。它不是普通备忘录，而是正文生成和校验的合同。

对于 workflow-permission-message 类型需求单元，合同至少包含：

```text
列表 / 页面入口
筛选条件
列表展示字段和展示规则
详情页区域和字段
流程节点按钮
按钮填写规则
状态变更
权限分层
消息触发矩阵
消息接收对象
变量字典
跳转链接
异常与补偿
防重复提交
验收口径
```

正文生成时必须逐项消费这些锚点。某项无来源时必须写明“不涉及”或形成待确认项，不能静默省略。

### 4.3 正文生成规则

第 7 章不再允许直接从材料自由写作。高风险需求单元正文生成顺序改为：

```text
source-extract
-> ledgers
-> local-anchor-contract
-> chapter-block
-> local-gate-report
-> chapters/
-> final assembly
```

正文块可以用自然语言、列表或表格表达，但必须能从 `local-anchor-contract` 逐项追踪。对于表单、列表、审批、派生清单、生命周期功能，优先使用表格表达字段、按钮、状态和验收，避免段落把规则吞掉。

### 4.4 横切规则回填

消息通知、小红点、无审批人、异常订单、防重复提交、外部跳转等可以保留全局功能章节，但每个受影响功能必须写本地效果。

例如 `需求审核` 中：

- 消息通知全局章节可定义模板、日志和开关。
- `7.3 需求审核` 本地必须写待审批、审核即将超期、审核超期、审核已通过、审核已驳回的触发、接收对象、跳转和变量。
- 异常订单可以在系统管理章节展开，但 `需求审核` 或关联需求提交功能必须写审批流异常对审核状态和入口的影响。

## 5. 局部 Gate 设计

新增 `validate_requirement_unit_gate.py`，用于检查单个需求单元正文，而不是整篇 PRD。

输入：

```text
--contract <local-anchor-contract.md>
--block <chapter-block.md 或最终 PRD 中抽出的局部章节>
--profile workflow-permission-message
```

输出：

```text
pass / fail
missing anchors
weak anchors
global-only anchors
suggested local destinations
```

检查规则：

1. 合同中的 required anchor 必须在局部正文中出现。
2. 如果 anchor 只出现在全局章节，不算通过，标记为 `global-only`。
3. 如果只出现模糊词，例如“支持相关操作”“查询条件保持一致”“按权限控制”，标记为 `weak anchor`。
4. 失败时不阻断继续分析，但阻断正式基线标记。

## 6. 数据流

```text
原始 PRD / 迭代材料
  -> source-inventory
  -> requirement-unit selection
  -> source-extract
  -> ledgers
  -> local-anchor-contract
  -> chapter-block draft
  -> local gate
  -> product confirmation
  -> frozen chapter fragment
  -> final assembly
  -> full PRD quality checks
```

关键变化是：第 7 章正文不再是一次性生成，而是由多个通过局部 gate 的正文块组成。

## 7. 错误处理

| 场景 | 处理 |
| --- | --- |
| 原始材料缺少某锚点 | 在合同中标记为 `source-missing`，正文写入待确认项 |
| ledger 有锚点但正文缺失 | local gate 失败，返回缺失项，禁止冻结该正文块 |
| 锚点只在全局章节出现 | 标记为 `global-only`，要求回填本地功能正文 |
| 正文使用概括词替代细节 | 标记为 `weak anchor`，要求展开字段、按钮、状态或消息规则 |
| 用户授权默认确认 | 只减少等待，不跳过证据包、合同和 local gate |
| 需求单元过大 | 拆成多个连续子单元，但必须保持同一业务对象或流程的追踪关系 |

## 8. 测试策略

### 8.1 单元测试

新增测试覆盖：

- `local-anchor-contract` 中 required anchor 缺失时失败。
- anchor 只在全文其他章节出现时失败。
- “查询条件保持一致”“按权限控制”等弱表达被识别。
- `data-demand-approval` 的完整 slice 能通过 workflow-permission-message local gate。
- 新生成稿第 7.3 的压缩版应失败，并输出缺失项。

### 8.2 回归样本

首批使用现有 gold slices：

| Slice | Profile | 目的 |
| --- | --- | --- |
| `manual-data-demand-create` | form-detail | 表单、字段、嵌套页面、保存提交 |
| `data-demand-approval` | workflow-permission-message | 审批、权限、消息、异常刷新 |
| `supply-responsibility-review-notice` | workflow-permission-message | 责任审核、协商、消息通知 |
| `data-resource-association-lifecycle` | object-lifecycle | 资源生命周期 |
| `supervise-timeout-reminder` | derived-list-time-rule | 派生清单和时间规则 |

### 8.3 验收标准

下一版 skill 跑完整 PRD 后，至少满足：

1. `需求审核` 第 7 章局部正文通过 `data-demand-approval` local gate。
2. 全文级检查不再作为唯一保真结论。
3. 任一 gold-like 功能缺失本地锚点时，最终报告必须明确指出，不能宣称正式基线通过。
4. 生成稿第 7 章局部正文可被研发按页面、字段、按钮、状态、权限和消息还原功能蓝图。

## 9. 实施边界

第一阶段只改 skill 规则、参考文档、检查脚本和 gold slice 回归，不重写整个 PRD 生成器。

建议实施顺序：

1. 在 skill 文档中加入“半结构化装配器”执行模式。
2. 在 discovery workflow 中加入 `local-anchor-contract` 和 requirement-unit local gate。
3. 新增 `validate_requirement_unit_gate.py`。
4. 为 `data-demand-approval` 建立 contract，并用压缩生成稿作为失败样本。
5. 更新 formal baseline gate：所有 gold-like 需求单元 local gate 通过后，才能进入正式基线。

## 10. 设计结论

本次优化不再把压缩问题视为 prompt 问题，而视为生成架构问题。skill 必须把“证据包”和“局部正文”绑定起来，强制模型逐项消费证据，再用需求单元级 gate 验证。这样才能从根上降低第 7 章功能描述被压缩的概率。

