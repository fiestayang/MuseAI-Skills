# skill-creator：技能作者工作流与资源拆分

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

技能作者工作流与资源拆分。入口：[SKILL.md](../../../opt/hatch/skills/skill-creator/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `skill-creator` |
| frontmatter name | `skill_creator` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Create or update a workspace skill: its description, structure, instructions, and supporting files.

<a id="flow"></a>
## 执行流程与输入输出

先明确窄职责和触发短语，再选择 workspace/skills 路径；主文件仅保留操作核心；长文放 references，交付资产放 assets，协议与认证逻辑交给 helper；编写 name/description 后校验真实命令和路径。自定义连接器先由 credentials.request_api_access 建立连接，再调用脚手架生成认证段。

<a id="design"></a>
## 实现思路、异常与限制

工具型技能按 Purpose、Tooling、Auth、Operating Rules 组织；纯工作流按 Workflow、Output Contract 组织。description 是触发面，正文是操作面，参考资料是按需上下文。

文中 scaffold-connector-skill 在快照中缺失；不能声称复制文档即可创建可运行连接器。401/403 要先检查凭据是否附加，不能一律归因于 token 失效。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/skill-creator/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/authoring_guide.md](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md) | 约束命名与 frontmatter，提供工具型和流程型模板，说明哪些资料应移出主文件；可直接迁移为轻量静态检查清单，无需新增框架。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时使用一个目录约定加静态校验即可。认证 helper 应由平台维护，模型只填业务逻辑；无需先建立复杂插件市场。

最小验收建议：用误导性的 description、缺失 helper 和不存在的引用各做一个负例，确保检查报告明确指出触发不清和交付缺项。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Skill Creator](../../../opt/hatch/skills/skill-creator/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/skill-creator/SKILL.md#L9) | 9 |
| [Workflow](../../../opt/hatch/skills/skill-creator/SKILL.md#L12) | 12 |
| [Connector Credentials](../../../opt/hatch/skills/skill-creator/SKILL.md#L31) | 31 |
| [Operating Rules](../../../opt/hatch/skills/skill-creator/SKILL.md#L44) | 44 |
| [Reference Guide](../../../opt/hatch/skills/skill-creator/SKILL.md#L52) | 52 |

### references/authoring_guide.md

| 源章节 | 起始行 |
|---|---|
| [Skill Authoring Guide](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L1) | 1 |
| [Naming](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L5) | 5 |
| [Resource Split](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L11) | 11 |
| [Frontmatter Template](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L19) | 19 |
| [Body Templates](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L31) | 31 |
| [Tool-backed skill](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L33) | 33 |
| [Workflow-only skill](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L50) | 50 |
| [What to Move Out of `SKILL.md`](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L67) | 67 |
| [Review Checklist](../../../opt/hatch/skills/skill-creator/references/authoring_guide.md#L76) | 76 |
