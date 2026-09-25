# self-awareness：以当前状态回答 Agent 自身问题

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

以当前状态回答 Agent 自身问题。入口：[SKILL.md](../../../opt/hatch/skills/self-awareness/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `self-awareness` |
| frontmatter name | `self_awareness` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Ground self-referential answers in the agent's actual filesystem. Use when the user asks who the agent is, what it can do, what it knows, what it remembers, what it has built, what services are connected, or what rules it follows.

<a id="flow"></a>
## 执行流程与输入输出

根据问题选择身份、规则、用户知识、记忆、连接状态或已构建内容的文件；每次重新读取；按 question_types 指定路径展开；缺失或过时信息明确说明。extensions 只有在用户明确要连接建议或仪表板时加载。

<a id="design"></a>
## 实现思路、异常与限制

它将“能力解释”视为有来源的查询任务。文件存在、连接可用和作品已交付是不同事实；不能仅凭 skill 目录声称服务已连接。optional dashboard 被刻意放到按需引用中。

示例 cat/ls 忽略缺失文件，不代表缺失状态可以隐去。对连接的回答仍需要产品工具确认；本快照没有实际用户记忆文件。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/self-awareness/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/extensions.md](../../../opt/hatch/skills/self-awareness/references/extensions.md) | 可选连接推荐和仪表板必须有明确请求；把扩展建议与事实回答分开，防止调查范围无端膨胀。 |
| [references/question_types.md](../../../opt/hatch/skills/self-awareness/references/question_types.md) | 按能力、连接、身份、知识、记忆、产物和规则选择实际读取路径；避免一问自我介绍就遍历所有私人文件。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时让自我描述读取当前 capability registry 与状态，不维护第二份容易过时的能力清单。回答携带观察时间和证据来源。

最小验收建议：删除一个身份文件、保留一个未连接技能；回答必须区分文件缺失与服务不可用。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Self-Awareness](../../../opt/hatch/skills/self-awareness/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/self-awareness/SKILL.md#L9) | 9 |
| [Tooling](../../../opt/hatch/skills/self-awareness/SKILL.md#L12) | 12 |
| [Operating Rules](../../../opt/hatch/skills/self-awareness/SKILL.md#L29) | 29 |

### references/extensions.md

| 源章节 | 起始行 |
|---|---|
| [Optional Self-Awareness Extensions](../../../opt/hatch/skills/self-awareness/references/extensions.md#L1) | 1 |
| [Connection recommendations](../../../opt/hatch/skills/self-awareness/references/extensions.md#L5) | 5 |
| [Optional dashboard](../../../opt/hatch/skills/self-awareness/references/extensions.md#L16) | 16 |

### references/question_types.md

| 源章节 | 起始行 |
|---|---|
| [Self-Awareness Question Types](../../../opt/hatch/skills/self-awareness/references/question_types.md#L1) | 1 |
| [Shared framing](../../../opt/hatch/skills/self-awareness/references/question_types.md#L5) | 5 |
| [1. Capabilities](../../../opt/hatch/skills/self-awareness/references/question_types.md#L11) | 11 |
| [2. Connection discovery](../../../opt/hatch/skills/self-awareness/references/question_types.md#L25) | 25 |
| [3. Identity](../../../opt/hatch/skills/self-awareness/references/question_types.md#L37) | 37 |
| [4. User knowledge](../../../opt/hatch/skills/self-awareness/references/question_types.md#L48) | 48 |
| [5. Memory](../../../opt/hatch/skills/self-awareness/references/question_types.md#L60) | 60 |
| [6. Built items](../../../opt/hatch/skills/self-awareness/references/question_types.md#L71) | 71 |
| [7. Rules](../../../opt/hatch/skills/self-awareness/references/question_types.md#L82) | 82 |
