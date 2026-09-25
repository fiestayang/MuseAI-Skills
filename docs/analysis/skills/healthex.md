# healthex：动态 MCP 医疗记录检索

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

动态 MCP 医疗记录检索。入口：[SKILL.md](../../../opt/hatch/skills/healthex/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `healthex` |
| frontmatter name | `healthex` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use to connect HealthEx and ask questions about your medications, lab results, and other health records.

<a id="flow"></a>
## 执行流程与输入输出

Connection Guard 说明服务与只读授权；按问题先取 conditions、medications、labs 等相关类别；需要深查时 mcp-list 获取 schema；总体摘要仅作可选辅助；后台调用等完成才读真实 stdout；分页按响应窗口继续追踪历史。

<a id="design"></a>
## 实现思路、异常与限制

从分类记录建立可追溯上下文，避免慢速 get_health_summary 成为唯一依赖。分页的“本窗口完整”不是“全部历史结束”。临床模式是文档中的启发式建议，不是经过本仓库验证的诊疗规则。

缺失记录不证明未接受治疗；不得把旧时间窗或聚合摘要当全病史。文中的健康建议不在本次代码分析中作医学有效性背书。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/healthex/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/healthex/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### healthex/manifest.yaml

来源：[opt/hatch/skills/healthex/manifest.yaml](../../../opt/hatch/skills/healthex/manifest.yaml)；connector：`healthex`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `tools.list` | `allow` | 否 | — | List available HealthEx tools |
| `read` | `records.read` | `allow` | 否 | — | Access patient health records |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `setup` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `authorize-url` | `null`（不映射方法；不等于任意放行） |
| `refresh` | `null`（不映射方法；不等于任意放行） |
| `exchange-code` | `null`（不映射方法；不等于任意放行） |
| `mcp-list` | `tools.list` |
| `get-medications` | `records.read` |
| `get-conditions` | `records.read` |
| `get-allergies` | `records.read` |
| `get-immunizations` | `records.read` |
| `get-vitals` | `records.read` |
| `get-labs` | `records.read` |
| `get-procedures` | `records.read` |
| `get-visits` | `records.read` |
| `get-clinical-notes` | `records.read` |
| `get-health-summary` | `records.read` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时保存时间窗覆盖与字段来源，先输出事实再给经过独立验证的解释。医疗规则应由专业评审与更新机制维护，不能直接复制固定阈值。

最小验收建议：分类调用成功但总摘要超时仍能报告有依据部分；分页窗口完整但更早还有记录时不得提前宣称已遍历历史。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [HealthEx (OAuth + MCP Health Records)](../../../opt/hatch/skills/healthex/SKILL.md#L9) | 9 |
| [Purpose](../../../opt/hatch/skills/healthex/SKILL.md#L11) | 11 |
| [Tooling](../../../opt/hatch/skills/healthex/SKILL.md#L18) | 18 |
| [Connection Guard](../../../opt/hatch/skills/healthex/SKILL.md#L33) | 33 |
| [Data Retrieval Strategy](../../../opt/hatch/skills/healthex/SKILL.md#L44) | 44 |
| [Clinical Insight Patterns](../../../opt/hatch/skills/healthex/SKILL.md#L66) | 66 |
| [1. Care Gap Detection](../../../opt/hatch/skills/healthex/SKILL.md#L70) | 70 |
| [2. Condition-Medication-Lab Cross-Reference](../../../opt/hatch/skills/healthex/SKILL.md#L77) | 77 |
| [3. Contextual Health Guidance](../../../opt/hatch/skills/healthex/SKILL.md#L84) | 84 |
| [4. Risk Factor Aggregation](../../../opt/hatch/skills/healthex/SKILL.md#L90) | 90 |
| [Handling Slow or Backgrounded Calls](../../../opt/hatch/skills/healthex/SKILL.md#L95) | 95 |
| [No Real Data → Never Fabricate (highest-priority safety rule)](../../../opt/hatch/skills/healthex/SKILL.md#L108) | 108 |
| [Pagination](../../../opt/hatch/skills/healthex/SKILL.md#L123) | 123 |
| [Operating Rules](../../../opt/hatch/skills/healthex/SKILL.md#L140) | 140 |
