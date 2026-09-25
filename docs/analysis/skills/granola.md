# granola：动态 MCP 会议知识检索

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

动态 MCP 会议知识检索。入口：[SKILL.md](../../../opt/hatch/skills/granola/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `granola` |
| frontmatter name | `granola` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Search and read Granola meeting notes and transcripts through Granola's OAuth-backed MCP server.

<a id="flow"></a>
## 执行流程与输入输出

status 检查，未连接时 authorize-url 完成 OAuth；list-tools 获取实时输入 schema；问题检索优先 query_granola_meetings，元数据用 list_meetings，已知 ID 用 get_meetings，确需原文才取 transcript；保留引用链接。

<a id="design"></a>
## 实现思路、异常与限制

封装动态 MCP 而非写死所有参数。get_account_info 的访问 scopes 和默认最近 30 天窗口影响空结果含义，必须先排除范围限制。

只允许 JSON object 参数；零会议结果不能立刻断言无记录。持续 unauthorized 才显式 refresh/re-authorize；不能把会议笔记工具用来排未来日程。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/granola/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/granola/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### granola/manifest.yaml

来源：[opt/hatch/skills/granola/manifest.yaml](../../../opt/hatch/skills/granola/manifest.yaml)；connector：`granola`。

请求配额声明：`mode` = `enforce`；`workers` = `['granola-cli']`；`queries_per_minute` = `100`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `query_granola_meetings` | `allow` | 否 | ; guard=verification_codes | Search meeting notes |
| `read` | `list_meetings` | `allow` | 否 | ; guard=verification_codes | List meetings |
| `read` | `list_meeting_folders` | `allow` | 否 | ; guard=verification_codes | List meeting folders |
| `read` | `get_meetings` | `allow` | 否 | ; guard=verification_codes | Access meeting notes |
| `read` | `get_meeting_transcript` | `allow` | 否 | ; guard=verification_codes | Access meeting transcripts |
| `read` | `get_account_info` | `allow` | 否 | ; guard=verification_codes | Check account access |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时缓存工具 schema 但明确失效条件，同时保存检索窗口和访问范围。先取摘要与元数据，降低全文成本。

最小验收建议：默认窗口空、扩展历史有数据，以及 public-only workspace 看不到私人笔记时，回答应正确说明范围。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Granola](../../../opt/hatch/skills/granola/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/granola/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/granola/SKILL.md#L14) | 14 |
| [Connection management](../../../opt/hatch/skills/granola/SKILL.md#L21) | 21 |
| [MCP operations](../../../opt/hatch/skills/granola/SKILL.md#L31) | 31 |
| [Auth](../../../opt/hatch/skills/granola/SKILL.md#L42) | 42 |
| [First-use setup flow](../../../opt/hatch/skills/granola/SKILL.md#L46) | 46 |
| [Operating Rules](../../../opt/hatch/skills/granola/SKILL.md#L62) | 62 |
