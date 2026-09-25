# outlook-calendar：Outlook 事件与邀请效果控制

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Outlook 事件与邀请效果控制。入口：[SKILL.md](../../../opt/hatch/skills/outlook-calendar/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `outlook-calendar` |
| frontmatter name | `outlook_calendar` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> View, create, update, and delete events in the user's Outlook Calendar.

<a id="flow"></a>
## 执行流程与输入输出

--status 确認连接；list 用 time-min/time-max 和 page-size；get 获取具体事件；create/update 指定 RFC3339 与 IANA 时区；根据是否发送邀请或更新通知区分审批；删除复用精确 Graph ID。

<a id="design"></a>
## 实现思路、异常与限制

与 Google 走不同 CLI，但保留同一核心不变量：时间、目标身份和外发效果必须明确。helper 在更新前读取事件，用参会人及组织者信息判断通知影响。

当前 update 不支持修改 attendees，不能臆造参数。全天日期不应时区平移；分页 token 与 change key 不应泄露到面向用户结果。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/outlook-calendar/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/outlook-calendar/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### outlook-calendar/manifest.yaml

来源：[opt/hatch/skills/outlook-calendar/manifest.yaml](../../../opt/hatch/skills/outlook-calendar/manifest.yaml)；connector：`outlook_calendar`。

请求配额声明：`mode` = `enforce`；`workers` = `['outlook-calendar']`；`queries_per_minute` = `600`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `events.list` | `allow` | 否 | — | Show events |
| `read` | `events.get` | `allow` | 否 | — | Access events |
| `write` | `events.create` | `allow` | 是 | — | Create events |
| `write` | `events.create_with_invitations` | `ask` | 否 | — | Create events with invitations |
| `write` | `events.update` | `allow` | 是 | — | Edit events |
| `write` | `events.update_with_notifications` | `ask` | 否 | — | Update events and notify guests |
| `write` | `events.delete` | `allow` | 是 | — | Delete events |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时跨 provider 共享领域语义，不强求相同 flags；用能力表暴露“不支持修改来宾”这一实际差异。

最小验收建议：有参会人的会议时间变更应走通知审批；私人事件与全天日期保持正确时间语义。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Outlook Calendar](../../../opt/hatch/skills/outlook-calendar/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/outlook-calendar/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/outlook-calendar/SKILL.md#L13) | 13 |
| [Auth](../../../opt/hatch/skills/outlook-calendar/SKILL.md#L39) | 39 |
| [Operating Rules](../../../opt/hatch/skills/outlook-calendar/SKILL.md#L50) | 50 |
