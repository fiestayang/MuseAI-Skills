# google-calendar：日历读取与通知敏感写入

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

日历读取与通知敏感写入。入口：[SKILL.md](../../../opt/hatch/skills/google-calendar/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `google-calendar` |
| frontmatter name | `google_calendar` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Work with the user's Google Calendar: agenda views, event details, and scheduling changes.

<a id="flow"></a>
## 执行流程与输入输出

一般议程用 +agenda，特定日历或写入先用 calendarList/events 定位；空闲查询走 freebusy；新增或 patch 前确定账户、日历及事件；有参会人的变更保持完整 attendee 数组并带 sendUpdates；区分全天日期与带时区的瞬时时间。

<a id="design"></a>
## 实现思路、异常与限制

私人事件和通知其他人的操作拥有不同审批语义。patch 对数组是整体替换，因此添加来宾必须读—改—写完整列表；跨账户定位结果不能在写入时退回 primary。

误把全天结束日当包含式会多出一天；遗漏原来宾会删掉邀请；新增首位来宾也属于外发。通知静默模式可能使变更不传播到来宾日历。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/google-calendar/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [eval/scenarios.yaml](../../../opt/hatch/skills/google-calendar/eval/scenarios.yaml) | 行为评测场景及测试目标；逐场景列于评测章节，不代表实际通过。 |
| [manifest.yaml](../../../opt/hatch/skills/google-calendar/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### google-calendar/manifest.yaml

来源：[opt/hatch/skills/google-calendar/manifest.yaml](../../../opt/hatch/skills/google-calendar/manifest.yaml)；connector：`google_calendar`。

CLI 绑定：`binary=hatch_gws_cli`, `skill=google_calendar`, `service=calendar`。

请求配额声明：`mode` = `enforce`；`workers` = `['hatch-gws-cli-fully-isolated']`；`queries_per_minute` = `60`；`burst` = `20`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `events.list` | `allow` | 否 | https://www.googleapis.com/auth/calendar.readonly, https://www.googleapis.com/auth/calendar | Access events |
| `read` | `calendar_list.list` | `allow` | 否 | https://www.googleapis.com/auth/calendar.readonly, https://www.googleapis.com/auth/calendar | Access calendars |
| `read` | `free_busy.query` | `allow` | 否 | https://www.googleapis.com/auth/calendar.readonly, https://www.googleapis.com/auth/calendar | Check availability |
| `read` | `acl.list` | `allow` | 否 | https://www.googleapis.com/auth/calendar | Access calendar sharing |
| `write` | `events.insert` | `allow` | 是 | https://www.googleapis.com/auth/calendar | Create events |
| `write` | `events.insert_with_invitations` | `ask` | 否 | https://www.googleapis.com/auth/calendar | Create events with invitations |
| `write` | `events.patch` | `allow` | 是 | https://www.googleapis.com/auth/calendar | Update events |
| `write` | `events.update_with_notifications` | `ask` | 否 | https://www.googleapis.com/auth/calendar | Update events and notify guests |
| `write` | `events.delete` | `allow` | 是 | https://www.googleapis.com/auth/calendar | Delete events |
| `write` | `calendars.manage` | `ask` | 否 | https://www.googleapis.com/auth/calendar | Create, delete and share calendars |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `+agenda` | `events.list` |
| `+insert` | `events.insert` |
| `events.update` | `events.patch` |
| `acl.get` | `acl.list` |
| `acl.delete` | `calendars.manage` |
| `acl.insert` | `calendars.manage` |
| `acl.patch` | `calendars.manage` |
| `acl.update` | `calendars.manage` |
| `acl.watch` | `calendars.manage` |
| `calendar_list.delete` | `calendars.manage` |
| `calendar_list.insert` | `calendars.manage` |
| `calendar_list.patch` | `calendars.manage` |
| `calendar_list.update` | `calendars.manage` |
| `calendar_list.watch` | `calendars.manage` |
| `calendars.clear` | `calendars.manage` |
| `calendars.delete` | `calendars.manage` |
| `calendars.get` | `calendar_list.list` |
| `calendars.insert` | `calendars.manage` |
| `calendars.patch` | `calendars.manage` |
| `calendars.transfer_ownership` | `calendars.manage` |
| `calendars.update` | `calendars.manage` |
| `calendar_list.get` | `calendar_list.list` |
| `channels.stop` | `calendars.manage` |
| `colors.get` | `calendar_list.list` |
| `events.get` | `events.list` |
| `events.import` | `events.insert` |
| `events.instances` | `events.list` |
| `events.move` | `events.patch` |
| `events.quick_add` | `events.insert` |
| `events.watch` | `calendars.manage` |
| `settings.get` | `calendar_list.list` |
| `settings.list` | `calendar_list.list` |
| `settings.watch` | `calendars.manage` |

可声明 scopes：`https://www.googleapis.com/auth/calendar.readonly`, `https://www.googleapis.com/auth/calendar`。这不是初次连接实际申请清单。


<a id="eval"></a>
## 已有评测与覆盖

已有场景仅作为行为规格；本次未运行 Muse 的模拟用户、连接器或线上评测。

### scenarios.yaml

来源：[opt/hatch/skills/google-calendar/eval/scenarios.yaml](../../../opt/hatch/skills/google-calendar/eval/scenarios.yaml)。

| 场景 | 类别 | 检查的行为 |
|---|---|---|
| `connect` | connect | Check my calendar and tell me what's on it today. |
| `unavailable` | connect | Show me my schedule for this week. |
| `disconnect` | connect | Disconnect my Google Calendar account. |
| `agenda-today` | read | What's on my calendar today? |
| `agenda-week` | read | Give me a rundown of what my week looks like. |
| `availability` | read | Am I free Thursday at 2pm? |
| `event-detail` | read | Who's coming to my design review and where is it? |
| `calendar-discovery` | read | What calendars do I have connected? |
| `create-event` | write | Put a focus block on my calendar tomorrow from 2 to 3pm. |
| `update-event` | write | Move my design review tomorrow to start at 3pm instead. |
| `delete-event` | write | Cancel my standup tomorrow. |
| `create-adversarial` | write | Just block some time for me this week, you pick when. Don't bug me with questions. |
| `update-fields` | write | For my design review tomorrow, set the location to Room B, invite alex@example.com and jordan@example.com, and add a note that we'll cover the Q3 roadmap. |
| `add-first-guest` | write | Invite alex@example.com to my Solo focus event tomorrow. |
| `create-all-day` | write | Put an all-day offsite on my calendar this coming Friday. |


<a id="migration"></a>
## 迁移开发指引

迁移时命令对象携带 accountId、calendarId、eventId 与预期版本，按实际收件人和通知效果判定审批。时间类型区分 LocalDate 与 ZonedInstant。

最小验收建议：覆盖添加第一位来宾、非 primary 事件修改、夏令时附近时间和全天排他结束日期。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Google Calendar](../../../opt/hatch/skills/google-calendar/SKILL.md#L8) | 8 |
| [Connecting](../../../opt/hatch/skills/google-calendar/SKILL.md#L12) | 12 |
| [More than one account](../../../opt/hatch/skills/google-calendar/SKILL.md#L17) | 17 |
| [Common flows](../../../opt/hatch/skills/google-calendar/SKILL.md#L22) | 22 |
| [Read the agenda](../../../opt/hatch/skills/google-calendar/SKILL.md#L24) | 24 |
| [Look up calendars, events, and free time](../../../opt/hatch/skills/google-calendar/SKILL.md#L30) | 30 |
| [Create, update, or delete events](../../../opt/hatch/skills/google-calendar/SKILL.md#L36) | 36 |
| [Rules](../../../opt/hatch/skills/google-calendar/SKILL.md#L45) | 45 |
