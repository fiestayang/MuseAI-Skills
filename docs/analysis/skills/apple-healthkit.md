# apple-healthkit：Apple Health 同步数据的统一查询

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Apple Health 同步数据的统一查询。入口：[SKILL.md](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `apple-healthkit` |
| frontmatter name | `apple_healthkit` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> The user's synced Apple Health (HealthKit) data: daily metrics (steps, distance, calories, heart rate, HRV, VO2max), sleep sessions (stages, quality, efficiency), and workouts.

<a id="flow"></a>
## 执行流程与输入输出

device.list 确定 iPhone 平台；所有 health-cli 命令显式 provider=healthkit；按数据形态选择 metrics 聚合、sessions 的 sleep/workout 或 samples 原始点；先发现用户实际存在字段；读取 coverage，不完整时按 warning 请求 backfill 并复查。

<a id="design"></a>
## 实现思路、异常与限制

统一 schema 在字段中编码单位，区分字段已知与 observed。Apple Health 是汇聚渠道，不代表每条数据由 iPhone 本身测量。删除走专门审计入口，仅删除指定 provider 的存储记录。

缺数据不等于零。samples 的 fields 表示样本类型而非列投影；不能从 GPS 推断地点名称。断开连接与删除记录不同，CLI 不提供直接断开流程。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/apple-healthkit/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/apple-healthkit/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### apple-healthkit/manifest.yaml

来源：[opt/hatch/skills/apple-healthkit/manifest.yaml](../../../opt/hatch/skills/apple-healthkit/manifest.yaml)；connector：`apple_healthkit`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `healthkit` | `healthkit.query` | `allow` | 否 | — | Read daily metrics, sleep, and workouts from Apple Health |
| `healthkit` | `healthkit.status` | `allow` | 否 | — | Check Apple Health sync status |
| `delete` | `healthkit.delete` | `ask` | 否 | — | Delete matching Apple Health records |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时返回 records 与 coverage 一起的结果，字段目录来自实际数据；provider、设备、时间和单位参与校验。

最小验收建议：两台来源设备、缺失同步日期和 observed=false 指标用例，确保不补零、不误称完整，不跨 provider 删除。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Apple Health](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L8) | 8 |
| [Data Source](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L17) | 17 |
| [When to Use](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L21) | 21 |
| [Tooling](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L28) | 28 |
| [query metrics — all-day metric rollups](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L46) | 46 |
| [query sessions — discrete sessions](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L65) | 65 |
| [query samples — raw, unbucketed data points](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L90) | 90 |
| [status — data-sync status](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L106) | 106 |
| [auth connect](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L116) | 116 |
| [auth disconnect](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L124) | 124 |
| [delete — erase stored Apple Health (HealthKit) records](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L134) | 134 |
| [Auth](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L163) | 163 |
| [Operating Rules](../../../opt/hatch/skills/apple-healthkit/SKILL.md#L170) | 170 |
