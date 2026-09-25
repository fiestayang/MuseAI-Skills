# tessie：车辆状态与明确物理动作

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

车辆状态与明确物理动作。入口：[SKILL.md](../../../opt/hatch/skills/tessie/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `tessie` |
| frontmatter name | `tessie` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Monitor a Tesla vehicle, inspect live state, and run explicit Tessie command endpoints.

<a id="flow"></a>
## 执行流程与输入输出

连接状态未知时 verify；vehicles 得到 VIN，多车时选择；影响性操作前读 status/state；command 使用明确命令名和可选等待；泛用 request 按实际方法受授权控制。

<a id="design"></a>
## 实现思路、异常与限制

车辆 ID、当前状态和动作授权共同决定调用。manifest 对鸣笛、闪灯等列方法默认，其余车辆命令走审批；不能以 read/write 二分代替物理风险判断。

不推断用户未要求的动作；不能因为收到 command accepted 就断言执行完成。set-token 是特定 CLI 流程，不应把 token 放普通文件或报告。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/tessie/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/tessie/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### tessie/manifest.yaml

来源：[opt/hatch/skills/tessie/manifest.yaml](../../../opt/hatch/skills/tessie/manifest.yaml)；connector：`tessie`。

请求配额声明：`mode` = `enforce`；`workers` = `['tessie-api']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `vehicles.list` | `allow` | 否 | — | View vehicle status and location |
| `read` | `api.read` | `allow` | 否 | — | View other vehicle data through Tessie API |
| `write` | `vehicle.command.other` | `ask` | 否 | — | Control your vehicle |
| `write` | `vehicle.honk` | `allow` | 是 | — | Honk the horn |
| `write` | `vehicle.flash_lights` | `allow` | 是 | — | Flash the lights |
| `write` | `vehicle.boombox` | `allow` | 是 | — | Play Boombox audio |
| `write` | `vehicle.software_update` | `allow` | 是 | — | Schedule or cancel a software update |
| `write` | `telemetry.configure` | `allow` | 是 | — | Configure vehicle telemetry |
| `write` | `api.write.other` | `ask` | 否 | — | Make other changes through Tessie API |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时按动作定义风险和前置状态，返回 accepted/in_progress/completed；重试策略依据实际幂等性。

最小验收建议：多车同名、车辆睡眠及命令接受但未完成场景，确认不选错车、不虚报实际动作完成。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Tessie (Tesla Vehicle Control)](../../../opt/hatch/skills/tessie/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/tessie/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/tessie/SKILL.md#L13) | 13 |
| [Auth](../../../opt/hatch/skills/tessie/SKILL.md#L39) | 39 |
| [Operating Rules](../../../opt/hatch/skills/tessie/SKILL.md#L50) | 50 |
