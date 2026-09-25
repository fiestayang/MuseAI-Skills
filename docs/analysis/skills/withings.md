# withings：带单位字段与明确聚合规则的健康读取

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

带单位字段与明确聚合规则的健康读取。入口：[SKILL.md](../../../opt/hatch/skills/withings/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `withings` |
| frontmatter name | `withings` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use when linking Withings or reading Withings body measurements, activity, sleep, workout, heart, and intraday data.

<a id="flow"></a>
## 执行流程与输入输出

status 完成连接；list-fields 发现 category 的字段；query 选择 daily-metrics、sleep 或 workout 及日期区间；按需 hourly/daily/weekly；只有新表面缺少指标时才使用 legacy endpoint。

<a id="design"></a>
## 实现思路、异常与限制

计数累加、平均心率取平均、最高心率取最大、体重等取桶内最后值，不能用统一 sum。字段名包含单位，native 名称需显式映射。

commands.md 内有重复章节及认证描述差异；以主 SKILL 的当前连接契约为分析主线，并列出冲突。API 空数组不能解释为测量值零。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/withings/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/withings/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |
| [references/commands.md](../../../opt/hatch/skills/withings/references/commands.md) | 新 query 接口与 legacy passthrough 的映射、聚合、单位和游标。该文件重复两个大章节且 auth 描述不完全相同，需清理后才作为单一维护源。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### withings/manifest.yaml

来源：[opt/hatch/skills/withings/manifest.yaml](../../../opt/hatch/skills/withings/manifest.yaml)；connector：`withings`。

请求配额声明：`mode` = `enforce`；`workers` = `['withings']`；`queries_per_minute` = `90`；`burst` = `20`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `measures.read` | `allow` | 否 | — | Read measurements and heart data |
| `read` | `activity.read` | `allow` | 否 | — | Read activity, sleep and workouts |
| `read` | `device.read` | `allow` | 否 | — | Read devices |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把每个指标的聚合算子写入元数据，provider 转换在 adapter 内完成；避免调用者自行记数字 meas-type。

最小验收建议：同桶多次体重测量与多段步数应分别取最后值和求和；未知字段必须先 discover 而非猜别名。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Withings](../../../opt/hatch/skills/withings/SKILL.md#L8) | 8 |
| [When to Use](../../../opt/hatch/skills/withings/SKILL.md#L12) | 12 |
| [Tooling](../../../opt/hatch/skills/withings/SKILL.md#L20) | 20 |
| [Categories](../../../opt/hatch/skills/withings/SKILL.md#L30) | 30 |
| [Output](../../../opt/hatch/skills/withings/SKILL.md#L38) | 38 |
| [Examples](../../../opt/hatch/skills/withings/SKILL.md#L42) | 42 |
| [Auth](../../../opt/hatch/skills/withings/SKILL.md#L55) | 55 |
| [Operating Rules](../../../opt/hatch/skills/withings/SKILL.md#L66) | 66 |
| [Legacy / Advanced Commands](../../../opt/hatch/skills/withings/SKILL.md#L75) | 75 |

### references/commands.md

| 源章节 | 起始行 |
|---|---|
| [Withings CLI Commands](../../../opt/hatch/skills/withings/references/commands.md#L1) | 1 |
| [Recommended path — healthkit-shape surface](../../../opt/hatch/skills/withings/references/commands.md#L7) | 7 |
| [`withings status`](../../../opt/hatch/skills/withings/references/commands.md#L11) | 11 |
| [`withings list-fields --category CATEGORY`](../../../opt/hatch/skills/withings/references/commands.md#L30) | 30 |
| [`withings query --category CATEGORY --start-date YYYY-MM-DD [...]`](../../../opt/hatch/skills/withings/references/commands.md#L34) | 34 |
| [Output contract (new surface)](../../../opt/hatch/skills/withings/references/commands.md#L48) | 48 |
| [Daily-metrics aggregation rules](../../../opt/hatch/skills/withings/references/commands.md#L56) | 56 |
| [Withings → Muse field name mapping (new surface)](../../../opt/hatch/skills/withings/references/commands.md#L65) | 65 |
| [Legacy / Advanced commands](../../../opt/hatch/skills/withings/references/commands.md#L110) | 110 |
| [Auth](../../../opt/hatch/skills/withings/references/commands.md#L117) | 117 |
| [Data reads (raw passthrough)](../../../opt/hatch/skills/withings/references/commands.md#L123) | 123 |
| [Measurement Type IDs (`--meas-types` for legacy `measures` command)](../../../opt/hatch/skills/withings/references/commands.md#L135) | 135 |
| [Legacy output contract](../../../opt/hatch/skills/withings/references/commands.md#L177) | 177 |
| [Pagination](../../../opt/hatch/skills/withings/references/commands.md#L184) | 184 |
| [Withings CLI Commands](../../../opt/hatch/skills/withings/references/commands.md#L188) | 188 |
| [Recommended path — healthkit-shape surface](../../../opt/hatch/skills/withings/references/commands.md#L194) | 194 |
| [`withings status`](../../../opt/hatch/skills/withings/references/commands.md#L198) | 198 |
| [`withings list-fields --category CATEGORY`](../../../opt/hatch/skills/withings/references/commands.md#L224) | 224 |
| [`withings query --category CATEGORY --start-date YYYY-MM-DD [...]`](../../../opt/hatch/skills/withings/references/commands.md#L228) | 228 |
| [Output contract (new surface)](../../../opt/hatch/skills/withings/references/commands.md#L242) | 242 |
| [Daily-metrics aggregation rules](../../../opt/hatch/skills/withings/references/commands.md#L250) | 250 |
| [Withings → Muse field name mapping (new surface)](../../../opt/hatch/skills/withings/references/commands.md#L259) | 259 |
| [Legacy / Advanced commands](../../../opt/hatch/skills/withings/references/commands.md#L304) | 304 |
| [Auth (Account Center-managed)](../../../opt/hatch/skills/withings/references/commands.md#L311) | 311 |
| [Data reads (raw passthrough)](../../../opt/hatch/skills/withings/references/commands.md#L317) | 317 |
| [Measurement Type IDs (`--meas-types` for legacy `measures` command)](../../../opt/hatch/skills/withings/references/commands.md#L329) | 329 |
| [Legacy output contract](../../../opt/hatch/skills/withings/references/commands.md#L371) | 371 |
| [Pagination](../../../opt/hatch/skills/withings/references/commands.md#L378) | 378 |
