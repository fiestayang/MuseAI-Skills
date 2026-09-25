# google-health-connect：Android Health Connect 同步数据

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Android Health Connect 同步数据。入口：[SKILL.md](../../../opt/hatch/skills/google-health-connect/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `google-health-connect` |
| frontmatter name | `google_health_connect` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> The user's synced Google Health Connect data from their Android device: daily metrics (steps, distance, calories, heart rate, HRV, VO2max), sleep sessions (stages, quality, efficiency), and workouts.

<a id="flow"></a>
## 执行流程与输入输出

先验证 Android 平台；health-cli 显式 provider=healthconnect；metrics 做分桶汇总，sessions 读睡眠或运动，samples 读高密度原始记录；status 检查范围与缺口；必要时执行设备 backfill 后重查。

<a id="design"></a>
## 实现思路、异常与限制

复用健康统一查询模型，但连接、断开和同步来源属于 Android。按类型选择查询避免把整夜睡眠和全天累计当同一种数据。

无法通过 CLI 断开，应在 Android 权限界面处理。delete 删除 Muse 已存记录，不表示删除手机上原始 Health Connect 数据；明确时间重叠语义和审批范围。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/google-health-connect/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/google-health-connect/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### google-health-connect/manifest.yaml

来源：[opt/hatch/skills/google-health-connect/manifest.yaml](../../../opt/hatch/skills/google-health-connect/manifest.yaml)；connector：`google_health_connect`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `healthconnect` | `healthconnect.query` | `allow` | 否 | — | Read daily metrics, sleep, and workouts from Health Connect |
| `healthconnect` | `healthconnect.status` | `allow` | 否 | — | Check Health Connect sync status |
| `delete` | `healthconnect.delete` | `ask` | 否 | — | Delete matching Health Connect records |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时将共享聚合层与平台授权 adapter 分开；删除参数 schema 要表达 all 与过滤条件互斥。

最小验收建议：聚合区间边界跨午夜、缺失样本和 provider 错误时验证，确保不混算、不声称撤销手机权限。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Health Connect](../../../opt/hatch/skills/google-health-connect/SKILL.md#L8) | 8 |
| [When to Use](../../../opt/hatch/skills/google-health-connect/SKILL.md#L17) | 17 |
| [Tooling](../../../opt/hatch/skills/google-health-connect/SKILL.md#L25) | 25 |
| [query metrics — all-day metric rollups](../../../opt/hatch/skills/google-health-connect/SKILL.md#L43) | 43 |
| [query sessions — discrete sessions](../../../opt/hatch/skills/google-health-connect/SKILL.md#L62) | 62 |
| [query samples — raw, unbucketed data points](../../../opt/hatch/skills/google-health-connect/SKILL.md#L87) | 87 |
| [status — data-sync status](../../../opt/hatch/skills/google-health-connect/SKILL.md#L103) | 103 |
| [auth connect](../../../opt/hatch/skills/google-health-connect/SKILL.md#L113) | 113 |
| [auth disconnect](../../../opt/hatch/skills/google-health-connect/SKILL.md#L121) | 121 |
| [delete — erase stored Health Connect records](../../../opt/hatch/skills/google-health-connect/SKILL.md#L131) | 131 |
| [Auth](../../../opt/hatch/skills/google-health-connect/SKILL.md#L160) | 160 |
| [Operating Rules](../../../opt/hatch/skills/google-health-connect/SKILL.md#L167) | 167 |
