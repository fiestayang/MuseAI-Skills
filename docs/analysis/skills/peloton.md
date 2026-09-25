# peloton：课程发现与训练预约

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

课程发现与训练预约。入口：[SKILL.md](../../../opt/hatch/skills/peloton/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `peloton` |
| frontmatter name | `peloton` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Connect to Peloton to browse fitness classes, check schedules, and book workouts.

<a id="flow"></a>
## 执行流程与输入输出

普通读取直接调用，不额外 status；自然语言优先 search-class；结构化筛选才走 ride-archived/live，并用 metadata-mappings 获取真实筛选 IDs；结果按规范列表呈现；schedule/reschedule/delete 操作绑定课程或 join token。

<a id="design"></a>
## 实现思路、异常与限制

将前置连接检查限制在认证错误或管理连接时，减少无必要请求。搜索参数与筛选 ID 来源明确；预约直播和点播是不同契约。

连接存储持久 token 的流程需要明确知情；不能从课程分数推断医学适用性。排课 epoch 与展示本地时间需要一致。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/peloton/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/peloton/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### peloton/manifest.yaml

来源：[opt/hatch/skills/peloton/manifest.yaml](../../../opt/hatch/skills/peloton/manifest.yaml)；connector：`peloton`。

请求配额声明：`mode` = `enforce`；`workers` = `['peloton']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `classes.read` | `allow` | 否 | — | Browse classes and schedules |
| `write` | `connection.disconnect` | `allow` | 否 | — | Disconnect Peloton account |
| `write` | `schedule.write` | `allow` | 否 | — | Manage workout schedule |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `authorize-url` | `null`（不映射方法；不等于任意放行） |
| `exchange-code` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `connection.disconnect` |
| `refresh` | `null`（不映射方法；不等于任意放行） |
| `ride-archived` | `classes.read` |
| `ride-live` | `classes.read` |
| `search-class` | `classes.read` |
| `search-class-widget` | `classes.read` |
| `deeplink` | `null`（不映射方法；不等于任意放行） |
| `metadata-mappings` | `classes.read` |
| `schedule-event` | `schedule.write` |
| `delete-scheduled-event` | `schedule.write` |
| `reschedule-event` | `schedule.write` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时允许不同连接器各自决定是否 preflight，不机械套用统一 status；以课程能力驱动预约参数。

最小验收建议：普通读取只发一次数据请求；遇 not_connected 才进入连接流程；无效 instructor ID 不应硬编码重试。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Peloton](../../../opt/hatch/skills/peloton/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/peloton/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/peloton/SKILL.md#L13) | 13 |
| [Class Browsing](../../../opt/hatch/skills/peloton/SKILL.md#L21) | 21 |
| [Filter IDs](../../../opt/hatch/skills/peloton/SKILL.md#L33) | 33 |
| [Scheduling](../../../opt/hatch/skills/peloton/SKILL.md#L36) | 36 |
| [Deeplinks](../../../opt/hatch/skills/peloton/SKILL.md#L42) | 42 |
| [Auth](../../../opt/hatch/skills/peloton/SKILL.md#L45) | 45 |
| [Operating Rules](../../../opt/hatch/skills/peloton/SKILL.md#L62) | 62 |
