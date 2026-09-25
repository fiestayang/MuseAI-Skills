# threads：Threads 内容查询、分析与发布

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Threads 内容查询、分析与发布。入口：[SKILL.md](../../../opt/hatch/skills/threads/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `threads` |
| frontmatter name | `threads` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read and manage the user's Threads account: profile, posts, feed, saved posts, activity, insights, social graph, search, trends, and a specific post by URL or ID. Can tune feed ranking and publish posts on request.

<a id="flow"></a>
## 执行流程与输入输出

accounts 选择本人 ID；URL 优先原样传 post；按 profile/feed/search/insights 读取；公开搜索与账户内容按规则分流；publish-post 在一次可信确认中绑定正文、回复权限、媒体顺序和封面；dear-algo-whisper 根据明确要求调节偏好。

<a id="design"></a>
## 实现思路、异常与限制

发布是一条隐藏写命令，没有可供模型拼装的公开 draft handle。读操作可配置有限重试，publish 与算法变更不可用传输重试，以免重复 mutation。

正文列出 search 命令，Operating rules 又限制一般发现的使用，报告将其视为路由范围约束而非“完全不支持搜索”。账户绑定失败不应绕过 typed insights 到内部接口。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/threads/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/threads/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### threads/manifest.yaml

来源：[opt/hatch/skills/threads/manifest.yaml](../../../opt/hatch/skills/threads/manifest.yaml)；connector：`threads`。

请求配额声明：`mode` = `shadow`；`workers` = `['threads-cli', 'threads-messages-cli']`；`queries_per_minute` = `600`；`burst` = `100`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `content.read` | `allow` | 否 | — | Access content |
| `read` | `interactions.read` | `allow` | 否 | — | Access interactions |
| `read` | `algorithm.read` | `allow` | 否 | — | Access your algorithm |
| `write` | `algorithm.update` | `allow` | 是 | — | Edit your algorithm |
| `write` | `content.post` | `ask` | 否 | — | Post content |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时输出 schema 与写入策略一起版本化；发布前摘要需覆盖全部媒体与账号，失败后重新调用视为新审批动作。

最小验收建议：模拟发布超时和账号失配，确认不自动重发；检查空白、Unicode 与媒体次序在审批后保持不变。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Threads CLI](../../../opt/hatch/skills/threads/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/threads/SKILL.md#L10) | 10 |
| [Account Linking](../../../opt/hatch/skills/threads/SKILL.md#L17) | 17 |
| [Tooling](../../../opt/hatch/skills/threads/SKILL.md#L31) | 31 |
| [Post output](../../../opt/hatch/skills/threads/SKILL.md#L64) | 64 |
| [Global options](../../../opt/hatch/skills/threads/SKILL.md#L71) | 71 |
| [Commands](../../../opt/hatch/skills/threads/SKILL.md#L77) | 77 |
| [Accounts](../../../opt/hatch/skills/threads/SKILL.md#L79) | 79 |
| [Profile](../../../opt/hatch/skills/threads/SKILL.md#L86) | 86 |
| [Activity Feed](../../../opt/hatch/skills/threads/SKILL.md#L93) | 93 |
| [Liked Media](../../../opt/hatch/skills/threads/SKILL.md#L105) | 105 |
| [Saved Posts](../../../opt/hatch/skills/threads/SKILL.md#L117) | 117 |
| [Insights Overview](../../../opt/hatch/skills/threads/SKILL.md#L128) | 128 |
| [Post-Level Insights](../../../opt/hatch/skills/threads/SKILL.md#L142) | 142 |
| [Top Posts](../../../opt/hatch/skills/threads/SKILL.md#L149) | 149 |
| [Other User's Profile](../../../opt/hatch/skills/threads/SKILL.md#L158) | 158 |
| [Profile Threads](../../../opt/hatch/skills/threads/SKILL.md#L166) | 166 |
| [Profile Replies](../../../opt/hatch/skills/threads/SKILL.md#L175) | 175 |
| [Profile Media](../../../opt/hatch/skills/threads/SKILL.md#L183) | 183 |
| [Followers](../../../opt/hatch/skills/threads/SKILL.md#L191) | 191 |
| [Following](../../../opt/hatch/skills/threads/SKILL.md#L199) | 199 |
| [Post by URL or ID](../../../opt/hatch/skills/threads/SKILL.md#L207) | 207 |
| [Fetch Post Comments](../../../opt/hatch/skills/threads/SKILL.md#L227) | 227 |
| [Fetch Post Likers](../../../opt/hatch/skills/threads/SKILL.md#L238) | 238 |
| [Feedback Hub Overview](../../../opt/hatch/skills/threads/SKILL.md#L249) | 249 |
| [Feedback Hub Tab](../../../opt/hatch/skills/threads/SKILL.md#L256) | 256 |
| [Trends](../../../opt/hatch/skills/threads/SKILL.md#L265) | 265 |
| [Search](../../../opt/hatch/skills/threads/SKILL.md#L273) | 273 |
| [Feed](../../../opt/hatch/skills/threads/SKILL.md#L285) | 285 |
| [Publish a post](../../../opt/hatch/skills/threads/SKILL.md#L304) | 304 |
| [Post write safety](../../../opt/hatch/skills/threads/SKILL.md#L372) | 372 |
| [Dear Algo Whisper](../../../opt/hatch/skills/threads/SKILL.md#L398) | 398 |
| [Operating rules](../../../opt/hatch/skills/threads/SKILL.md#L405) | 405 |
| [Output](../../../opt/hatch/skills/threads/SKILL.md#L418) | 418 |
