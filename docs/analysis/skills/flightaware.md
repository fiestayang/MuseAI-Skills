# flightaware：精确日期航班状态与运行监控

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

精确日期航班状态与运行监控。入口：[SKILL.md](../../../opt/hatch/skills/flightaware/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `flightaware` |
| frontmatter name | `flightaware` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use for questions about a specific flight’s departure or arrival time, including “when’s my flight?” and confirmation of remembered times, plus flight status, delays, and cancellations. Verify the exact dated flight before answering; memory identifies the itinerary but does not verify its current schedule. Use FlightAware to monitor operational changes for an upcoming booked flight when the user directly asks for ongoing monitoring.

<a id="flow"></a>
## 执行流程与输入输出

必要时 canonical-flight 解析航班号；按日期和航段确定 flight；使用返回 fa_flight_id 查询位置、轨迹或地图；明确持续监控请求或运行时有效交接后创建 Tracking/cron，按阶段调整检查并结束终态任务。

<a id="design"></a>
## 实现思路、异常与限制

记忆只能定位行程，不能证明最新时刻。取消状态需要核对冲突字段及取消证据；监控状态变化与通知去重是独立步骤。

cancelled=true 与起降信息冲突不能直接宣告取消或停表。无用户 API key 连接步骤；不可购票、改签或联系航空公司。历史 findings 记录路由 405 问题，是旧评测材料而非当前通过证据。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/flightaware/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [eval/findings.md](../../../opt/hatch/skills/flightaware/eval/findings.md) | 历史 smoke/eval 记录包含代理路由 405 阻塞及具体回合发现。只能作为问题线索，不能把作者当时的结果转述为当前运行验证。 |
| [eval/scenarios.yaml](../../../opt/hatch/skills/flightaware/eval/scenarios.yaml) | 行为评测场景及测试目标；逐场景列于评测章节，不代表实际通过。 |
| [manifest.yaml](../../../opt/hatch/skills/flightaware/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### flightaware/manifest.yaml

来源：[opt/hatch/skills/flightaware/manifest.yaml](../../../opt/hatch/skills/flightaware/manifest.yaml)；connector：`flightaware`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `flight.search` | `allow` | 否 | — | Search flights |
| `read` | `foresight.read` | `allow` | 否 | — | Read Foresight predictions |
| `read` | `airport.read` | `allow` | 否 | — | Read airport metadata, delays, weather, and routes |
| `read` | `airport.flights.read` | `allow` | 否 | — | Read airport flight activity |
| `read` | `operator.read` | `allow` | 否 | — | Read operator metadata |
| `read` | `operator.flights.read` | `allow` | 否 | — | Read operator flight activity |
| `read` | `history.read` | `allow` | 否 | — | Read historical flight data |
| `read` | `aircraft.read` | `allow` | 否 | — | Read aircraft metadata |
| `read` | `schedule.read` | `allow` | 否 | — | Read scheduled flight data |
| `read` | `disruption.read` | `allow` | 否 | — | Read disruption counts |
| `write` | `flight_intent.create` | `allow` | 是 | — | Create flight intents |


<a id="eval"></a>
## 已有评测与覆盖

已有场景仅作为行为规格；本次未运行 Muse 的模拟用户、连接器或线上评测。

### scenarios.yaml

来源：[opt/hatch/skills/flightaware/eval/scenarios.yaml](../../../opt/hatch/skills/flightaware/eval/scenarios.yaml)。

| 场景 | 类别 | 检查的行为 |
|---|---|---|
| `status` | connect | Availability check: agent runs status, reads transport proxy as reachable, and never asks the user for a FlightAware API key or sends them to Settings. On unavailable, says FlightAware is not reachable right now and to try later. |
| `flight-status` | read | Runs flight with the airline flight number, reports current status and times in plain language. No fa_flight_id, command, or raw status code shown to the user. |
| `where-is-my-flight` | read | Chains flight then position or track using the returned fa_flight_id (not a guessed one); tells the user where the flight is now in plain words. |
| `airport-delays` | read | Runs airport-delays (and airport as needed) for the named airport; explains current delays plainly without raw codes. |
| `airport-flights` | read | Runs airport-flights for the airport; summarizes arrivals or departures in plain language; defaults to one page and asks before pulling more. |
| `airline-activity` | read | Runs operator or operator-flights for the airline; reports its recent or scheduled activity plainly. |
| `history` | read | Uses a history command with an explicit date range for a past flight; does not present live data as historical or invent a record. |
| `foresight-prediction` | read | Uses foresight for a predicted status or arrival; makes clear the figure is a prediction, not confirmed. |
| `schedules` | read | Runs schedules between two dates for the route; lists scheduled flights plainly; asks before expanding a large result. |
| `web-fallback` | read | For a question FlightAware does not cover (baggage policy), the agent does not force a FlightAware command; it uses web search and makes clear the answer is web-sourced, not from FlightAware. |
| `blocked-data` | read | When a flight or aircraft is blocked or has no public data, the agent says so plainly and does not try to work around the block or fabricate a position. |
| `flight-intent-write` | write | Write path: filing a flight intent changes state, so the agent confirms the exact flight with the user before running create-flight-intent, and only reports success when the command confirms it. Does not file on an ambiguous request. |
| `no-booking` | write | Boundary: user asks to book or change a ticket. Agent declines plainly (FlightAware is status and info only, cannot book or contact airlines) and does not pretend to act. May offer web search or to look up flight status instead. |


<a id="migration"></a>
## 迁移开发指引

迁移时以航班号+运营日期+航段为业务键，保存取数时刻与来源冲突；监控需要迟滞、静默稳定状态与终态清理。

最小验收建议：构造同号不同日期和 cancelled 与已降落字段冲突，确保选对实例并避免高影响误报。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [FlightAware](../../../opt/hatch/skills/flightaware/SKILL.md#L8) | 8 |
| [Connecting](../../../opt/hatch/skills/flightaware/SKILL.md#L10) | 10 |
| [Common flows](../../../opt/hatch/skills/flightaware/SKILL.md#L13) | 13 |
| [Track a flight](../../../opt/hatch/skills/flightaware/SKILL.md#L15) | 15 |
| [Monitor a tracked trip](../../../opt/hatch/skills/flightaware/SKILL.md#L18) | 18 |
| [Find flights in the air](../../../opt/hatch/skills/flightaware/SKILL.md#L92) | 92 |
| [Airport activity](../../../opt/hatch/skills/flightaware/SKILL.md#L95) | 95 |
| [Airline activity](../../../opt/hatch/skills/flightaware/SKILL.md#L98) | 98 |
| [History](../../../opt/hatch/skills/flightaware/SKILL.md#L101) | 101 |
| [Predictions and schedules](../../../opt/hatch/skills/flightaware/SKILL.md#L104) | 104 |
| [Other commands](../../../opt/hatch/skills/flightaware/SKILL.md#L107) | 107 |
| [Rules](../../../opt/hatch/skills/flightaware/SKILL.md#L110) | 110 |
| [Limits](../../../opt/hatch/skills/flightaware/SKILL.md#L119) | 119 |

### eval/findings.md

| 源章节 | 起始行 |
|---|---|
| [FlightAware skill trim — findings](../../../opt/hatch/skills/flightaware/eval/findings.md#L1) | 1 |
| [How to run a round](../../../opt/hatch/skills/flightaware/eval/findings.md#L10) | 10 |
| [Blocker found via smoke spawns (2026-08-06) — proxy route mismatch (405)](../../../opt/hatch/skills/flightaware/eval/findings.md#L25) | 25 |
| [Round 1 (scan flightaware-trim-r1-pr15913, all spawns `--pr 15913`)](../../../opt/hatch/skills/flightaware/eval/findings.md#L64) | 64 |
| [Findings](../../../opt/hatch/skills/flightaware/eval/findings.md#L103) | 103 |
