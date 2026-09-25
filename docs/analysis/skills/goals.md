# goals：持久目标的创建与持续跟进

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

持久目标的创建与持续跟进。入口：[SKILL.md](../../../opt/hatch/skills/goals/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `goals` |
| frontmatter name | `goals` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Guidance for helping users create and accomplish goals. Read it before you create a goal for the user when no goal-creation contract is in context, and whenever you help with an existing goal. A Goals-tab creation turn already carries that contract and does not need this skill.

<a id="flow"></a>
## 执行流程与输入输出

先区分 Goals 页创建、普通对话创建和已有目标跟进。Goals 页已注入本类别完整契约时不重复读取；类别改变才加载另一份 creation。普通创建先读所属类别 creation；已有目标通过 user_goal.get 确认类别，仅加载 guides 下的 scaffold，再记录承诺、进展和调整。

<a id="design"></a>
## 实现思路、异常与限制

将首次 intake 与长期支持拆为不同资源，避免每次跟进重新盘问。七个类别分别约束数据来源、支持方式和领域风险。目标事实保存在 user_goal 产品工具中，指导文件只是行为模板。

无类别的旧目标只使用共享规则。目标期限结束不自动等于完成；需要判断结束、延长或回顾。Goals 页注入逻辑仅为文档契约，注入代码缺失。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/goals/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [creation/career.md](../../../opt/hatch/skills/goals/creation/career.md) | 首次创建指南：围绕职业方向、能力与行动机会；避免把招聘保证或替用户联系当作目标创建的默认步骤。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [creation/health.md](../../../opt/hatch/skills/goals/creation/health.md) | 首次创建指南：围绕健康目标、可用记录、可持续行为与安全边界；不将缺失数据变成诊断。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [creation/interests.md](../../../opt/hatch/skills/goals/creation/interests.md) | 首次创建指南：围绕兴趣、学习动机、已有水平与探索偏好；避免一开始就强加课程结构。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [creation/money.md](../../../opt/hatch/skills/goals/creation/money.md) | 首次创建指南：围绕财务目标、估算和信息来源；不把目标支持扩大为个性化交易或专业税法建议。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [creation/productivity.md](../../../opt/hatch/skills/goals/creation/productivity.md) | 首次创建指南：围绕时间、优先级、工作负荷与容量；先识别问题再决定是否需要工具和提醒。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [creation/relationships.md](../../../opt/hatch/skills/goals/creation/relationships.md) | 首次创建指南：围绕关系性质、边界及用户选择；使用消息、照片和通话记录前遵守额外许可。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [creation/something_else.md](../../../opt/hatch/skills/goals/creation/something_else.md) | 首次创建指南：围绕不适合既有领域的自定义目标；按用户明确的结果和隐私范围组织支持。该文件包含初次理解、创建工作流、可用数据源及安全规则；创建前读取，Goals 页已注入相同契约时不重复加载。 |
| [guides/career/scaffold.md](../../../opt/hatch/skills/goals/guides/career/scaffold.md) | 长期跟进指南：围绕职业方向、能力与行动机会；避免把招聘保证或替用户联系当作目标创建的默认步骤。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |
| [guides/health/scaffold.md](../../../opt/hatch/skills/goals/guides/health/scaffold.md) | 长期跟进指南：围绕健康目标、可用记录、可持续行为与安全边界；不将缺失数据变成诊断。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |
| [guides/interests/scaffold.md](../../../opt/hatch/skills/goals/guides/interests/scaffold.md) | 长期跟进指南：围绕兴趣、学习动机、已有水平与探索偏好；避免一开始就强加课程结构。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |
| [guides/money/scaffold.md](../../../opt/hatch/skills/goals/guides/money/scaffold.md) | 长期跟进指南：围绕财务目标、估算和信息来源；不把目标支持扩大为个性化交易或专业税法建议。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |
| [guides/productivity/scaffold.md](../../../opt/hatch/skills/goals/guides/productivity/scaffold.md) | 长期跟进指南：围绕时间、优先级、工作负荷与容量；先识别问题再决定是否需要工具和提醒。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |
| [guides/relationships/scaffold.md](../../../opt/hatch/skills/goals/guides/relationships/scaffold.md) | 长期跟进指南：围绕关系性质、边界及用户选择；使用消息、照片和通话记录前遵守额外许可。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |
| [guides/something_else/scaffold.md](../../../opt/hatch/skills/goals/guides/something_else/scaffold.md) | 长期跟进指南：围绕不适合既有领域的自定义目标；按用户明确的结果和隐私范围组织支持。已有目标先确认类别，再记录进展与承诺，不重跑创建问卷；这是持续支持策略而非 scheduler 实现。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时使用 create 与 follow-up 两种明确入口，目标记录保存 category、状态与进展事件。上下文中注明已加载的创建契约，禁止隐式重复 intake。

最小验收建议：同一目标创建后再跟进，应读取 scaffold 而非 creation；类别缺失时不能拼出不存在的路径。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Goals guidance assets](../../../opt/hatch/skills/goals/SKILL.md#L7) | 7 |

### creation/career.md

| 源章节 | 起始行 |
|---|---|
| [Creating a career goal](../../../opt/hatch/skills/goals/creation/career.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/career.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/career.md#L14) | 14 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/career.md#L81) | 81 |
| [Safety](../../../opt/hatch/skills/goals/creation/career.md#L91) | 91 |

### creation/health.md

| 源章节 | 起始行 |
|---|---|
| [Creating a health goal](../../../opt/hatch/skills/goals/creation/health.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/health.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/health.md#L9) | 9 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/health.md#L75) | 75 |
| [Safety](../../../opt/hatch/skills/goals/creation/health.md#L100) | 100 |

### creation/interests.md

| 源章节 | 起始行 |
|---|---|
| [Creating an interest goal](../../../opt/hatch/skills/goals/creation/interests.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/interests.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/interests.md#L15) | 15 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/interests.md#L82) | 82 |
| [Safety](../../../opt/hatch/skills/goals/creation/interests.md#L87) | 87 |

### creation/money.md

| 源章节 | 起始行 |
|---|---|
| [Creating a money goal](../../../opt/hatch/skills/goals/creation/money.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/money.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/money.md#L15) | 15 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/money.md#L82) | 82 |
| [Safety](../../../opt/hatch/skills/goals/creation/money.md#L89) | 89 |

### creation/productivity.md

| 源章节 | 起始行 |
|---|---|
| [Creating a productivity goal](../../../opt/hatch/skills/goals/creation/productivity.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/productivity.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/productivity.md#L14) | 14 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/productivity.md#L81) | 81 |
| [Safety](../../../opt/hatch/skills/goals/creation/productivity.md#L87) | 87 |

### creation/relationships.md

| 源章节 | 起始行 |
|---|---|
| [Creating a relationship goal](../../../opt/hatch/skills/goals/creation/relationships.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/relationships.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/relationships.md#L15) | 15 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/relationships.md#L82) | 82 |
| [Safety](../../../opt/hatch/skills/goals/creation/relationships.md#L94) | 94 |

### creation/something_else.md

| 源章节 | 起始行 |
|---|---|
| [Creating a goal for something else](../../../opt/hatch/skills/goals/creation/something_else.md#L1) | 1 |
| [Understanding the goal](../../../opt/hatch/skills/goals/creation/something_else.md#L3) | 3 |
| [The creation workflow](../../../opt/hatch/skills/goals/creation/something_else.md#L15) | 15 |
| [Data Sources](../../../opt/hatch/skills/goals/creation/something_else.md#L82) | 82 |
| [Safety](../../../opt/hatch/skills/goals/creation/something_else.md#L87) | 87 |

### guides/career/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Career goals](../../../opt/hatch/skills/goals/guides/career/scaffold.md#L1) | 1 |

### guides/health/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Health goals](../../../opt/hatch/skills/goals/guides/health/scaffold.md#L1) | 1 |

### guides/interests/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Interest goals](../../../opt/hatch/skills/goals/guides/interests/scaffold.md#L1) | 1 |

### guides/money/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Money goals](../../../opt/hatch/skills/goals/guides/money/scaffold.md#L1) | 1 |

### guides/productivity/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Productivity goals](../../../opt/hatch/skills/goals/guides/productivity/scaffold.md#L1) | 1 |

### guides/relationships/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Relationship goals](../../../opt/hatch/skills/goals/guides/relationships/scaffold.md#L1) | 1 |

### guides/something_else/scaffold.md

| 源章节 | 起始行 |
|---|---|
| [Custom goals](../../../opt/hatch/skills/goals/guides/something_else/scaffold.md#L1) | 1 |
