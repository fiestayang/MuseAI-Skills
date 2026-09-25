# device-data：设备同步缓存的读取和定界删除

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

设备同步缓存的读取和定界删除。入口：[SKILL.md](../../../opt/hatch/skills/device-data/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `device-data` |
| frontmatter name | `device_data` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read cached contacts and calendar events from Muse storage. Delete Muse's local copy of either source without modifying paired devices.

<a id="flow"></a>
## 执行流程与输入输出

离线或设备无 live search 时用 device-data 读取缓存联系人/日历；按设备与查询缩小范围；联系人支持 literal、token、nickname、phonetic 和受限 fuzzy；读取 selection_evidence 与 phone_selection；明确删除请求仅清 Muse 本地副本。

<a id="design"></a>
## 实现思路、异常与限制

缓存读取不接触设备。名称近似匹配产生候选而非授权；日历 all-day end_date 是包含式，与 Google Calendar 排他式不同，需要 adapter 转换。

缓存新鲜度不能当设备实时状态；一次 fuzzy 唯一结果也可能需要澄清。删除缓存不代表设备数据或权限被删除。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/device-data/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时将匹配证据和可操作性分开返回，保留来源设备、同步时间与日期语义。

最小验收建议：同音名、多号码及单日全天事件测试；删除缓存后设备原始数据不应被声称已删除。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Device Data](../../../opt/hatch/skills/device-data/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/device-data/SKILL.md#L10) | 10 |
| [Commands](../../../opt/hatch/skills/device-data/SKILL.md#L18) | 18 |
| [Operating Rules](../../../opt/hatch/skills/device-data/SKILL.md#L101) | 101 |
