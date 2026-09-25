# function-health：有来源的检验指标与临床备注读取

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

有来源的检验指标与临床备注读取。入口：[SKILL.md](../../../opt/hatch/skills/function-health/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `function-health` |
| frontmatter name | `function_health` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Retrieve lab biomarker results and clinician notes from Function Health.

<a id="flow"></a>
## 执行流程与输入输出

status 检查 OAuth；完成 authorize-url 后再次验证；按 observations 或 documents 读取 FHIR 数据；必要时按 LOINC 对齐指标；保留日期、单位、参考范围和临床备注的原始来源。

<a id="design"></a>
## 实现思路、异常与限制

最重要的输出约束是具体医学事实必须来自已完成返回值。工具任务句柄、空结果、遗漏附件都不是临床证据；interpretation 标签不等于独立诊断。

内联附件可能被省略并仅返回 omitted_reason/size_bytes，不能猜附件内容。服务失败不得用常见指标数值补答案。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/function-health/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/function-health/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### function-health/manifest.yaml

来源：[opt/hatch/skills/function-health/manifest.yaml](../../../opt/hatch/skills/function-health/manifest.yaml)；connector：`function_health`。

请求配额声明：`mode` = `enforce`；`workers` = `['function-health']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `observations.read` | `allow` | 否 | — | Access lab biomarker observations |
| `read` | `documents.read` | `allow` | 否 | — | Access clinician notes |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `authorize-url` | `null`（不映射方法；不等于任意放行） |
| `exchange-code` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `observations` | `observations.read` |
| `documents` | `documents.read` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时让查询结果区分 completed、running、empty、omitted 和 failed；医学事实输出保留记录 ID 与来源字段，但面向用户隐藏内部句柄。

最小验收建议：返回 running 和缺失附件时应报告未获得数据；单位不一致的同 LOINC 记录不得直接合并趋势。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Function Health](../../../opt/hatch/skills/function-health/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/function-health/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/function-health/SKILL.md#L13) | 13 |
| [Output](../../../opt/hatch/skills/function-health/SKILL.md#L25) | 25 |
| [No Real Data → Never Fabricate (highest-priority safety rule)](../../../opt/hatch/skills/function-health/SKILL.md#L32) | 32 |
| [Auth](../../../opt/hatch/skills/function-health/SKILL.md#L45) | 45 |
| [Operating Rules](../../../opt/hatch/skills/function-health/SKILL.md#L58) | 58 |
