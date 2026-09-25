# calendly：用户范围内的预约数据访问

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

用户范围内的预约数据访问。入口：[SKILL.md](../../../opt/hatch/skills/calendly/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `calendly` |
| frontmatter name | `calendly` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> View Calendly events and event types, and manage scheduling data using the Calendly CLI.

<a id="flow"></a>
## 执行流程与输入输出

status 后连接，me 确定 user URI 与 organization URI；list-events 或 event-types 按用户、时间和状态读取；用返回 page token 分页；高级 request 仅在已知契约内使用。

<a id="design"></a>
## 实现思路、异常与限制

身份发现先于用户范围查询，避免把组织或用户 URI 混用。CLI 负责 token 刷新；高层技能不保存认证状态文件。

泛用 request 也可能产生取消预约或删除订阅的副作用，不能因为命令名字通用就绕开审批。按 user_local 展示预约时间。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/calendly/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/calendly/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### calendly/manifest.yaml

来源：[opt/hatch/skills/calendly/manifest.yaml](../../../opt/hatch/skills/calendly/manifest.yaml)；connector：`calendly`。

请求配额声明：`mode` = `enforce`；`workers` = `['calendly']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `access.read` | `allow` | 否 | — | Read access |
| `write` | `api.write` | `ask` | 否 | — | Manage scheduling or account data |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时让 raw request 仍经过方法级授权，不给通用 HTTP 入口高于专用命令的权限。

最小验收建议：多页活动与组织/用户 URI 不一致时核验范围；POST/DELETE request 应进入对应审批。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Calendly](../../../opt/hatch/skills/calendly/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/calendly/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/calendly/SKILL.md#L13) | 13 |
| [Auth](../../../opt/hatch/skills/calendly/SKILL.md#L32) | 32 |
| [Operating Rules](../../../opt/hatch/skills/calendly/SKILL.md#L46) | 46 |
