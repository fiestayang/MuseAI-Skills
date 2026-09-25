# wide-research：同构多对象研究协调

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

同构多对象研究协调。入口：[SKILL.md](../../../opt/hatch/skills/wide-research/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `wide-research` |
| frontmatter name | `wide_research` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use when the user needs broad parallel research across many independent inputs with a shared output schema.

<a id="flow"></a>
## 执行流程与输入输出

把可独立处理的对象先归一化、去重；定义统一字段、worker 提示词与完成格式；只创建一个 manager，由它逐对象派发 worker；合并 results 与 failures；可行时仅对失败项重试一次；最终同时报告结果和覆盖率。

<a id="design"></a>
## 实现思路、异常与限制

实现核心是输入与输出契约，不是并行 API 本身。operation_brief、inputs、output_schema、worker_prompt_template、completion_format 把协调职责显式交给 manager；total、success_count、failure_count 防止把部分结果包装成全部完成。includeInPrompt=false 不代表禁止使用。

单对象或存在先后依赖的任务不适用。后台任务启动后需要及时反馈；worker 成功数必须能对应去重后的输入。并发上限、取消传播、manager 持久化均没有可读实现。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/wide-research/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时先用一个协调函数和有界并发，不必复制多层 Agent。保留输入 ID、统一 schema、失败清单及一次局部重试。只有子任务需要独立推理上下文时才引入 worker Agent。

最小验收建议：构造三项输入，其中一项固定失败；确认分母仍为三、失败项不被丢弃、重试不重复执行成功项。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Wide Research](../../../opt/hatch/skills/wide-research/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/wide-research/SKILL.md#L9) | 9 |
| [When to Use](../../../opt/hatch/skills/wide-research/SKILL.md#L12) | 12 |
| [Tooling](../../../opt/hatch/skills/wide-research/SKILL.md#L19) | 19 |
| [Operating Rules](../../../opt/hatch/skills/wide-research/SKILL.md#L37) | 37 |
