# artifacts/spreadsheet：可重算工作簿与局部修改

[返回技能目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

可重算工作簿与局部修改。入口：[SKILL.md](../../../../opt/hatch/skills/artifacts/spreadsheet/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `artifacts/spreadsheet` |
| frontmatter name | `artifact_spreadsheet` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Create, read, edit, fix, or clean spreadsheet files (.xlsx, .xlsm, .csv, .tsv). Use whenever a build task's artifact kind is spreadsheet, or the task names a spreadsheet file and wants something done to it or produced from it, including restructuring messy tabular data into a proper workbook. Covers openpyxl generation, formulas and recalculation, editing existing workbooks, and the validation gates. Not for tasks whose deliverable is a document, report, or web page that merely contains a table.

<a id="flow"></a>
## 执行流程与输入输出

用 openpyxl 和保留的生成脚本创建工作簿；读取已有文件时分别加载公式与缓存值；写公式而非预计算常量；含公式时经 LibreOffice 重算并解析 JSON 结果，再跑 validate_xlsx；抽查关键公式的业务含义。

<a id="design"></a>
## 实现思路、异常与限制

将“公式能求值”和“公式算对目标”分开。recalc_xlsx 的 errors_found 可能仍退出 0，因此不能仅看进程退出码。CSV 用标准库回读即可。

辅助重算与验证脚本缺失。data_only 读取不保留可编辑公式；已有工作簿的未涉及 sheet、图表和用户数据不能在重建时丢弃。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../../opt/hatch/skills/artifacts/spreadsheet/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/formulas.md](../../../../opt/hatch/skills/artifacts/spreadsheet/references/formulas.md) | 公式与缓存值双重读取、LibreOffice 重算以及已有工作簿局部编辑；讨论兼容公式和 openpyxl 限制。检查错误值并不替代业务公式抽查。 |
| [references/visual.md](../../../../opt/hatch/skills/artifacts/spreadsheet/references/visual.md) | 表头、冻结行、格式和财务模型约定；包含按任务 project_dir 生成的验证例子。迁移时应保留用户原 tab/column 名称而非套模板覆盖。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时保留双模式读取、公式错误列表与少量业务抽查。仅在复杂清洗确有需要时引入 pandas。

最小验收建议：用含公式错误及跨 sheet 引用的工作簿，确认退出 0 但存在 errors_found 时仍拒绝交付。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Spreadsheet artifacts](../../../../opt/hatch/skills/artifacts/spreadsheet/SKILL.md#L7) | 7 |
| [Scripts](../../../../opt/hatch/skills/artifacts/spreadsheet/SKILL.md#L44) | 44 |
| [Verification](../../../../opt/hatch/skills/artifacts/spreadsheet/SKILL.md#L51) | 51 |

### references/formulas.md

| 源章节 | 起始行 |
|---|---|
| [Formulas, recalculation, and editing existing workbooks](../../../../opt/hatch/skills/artifacts/spreadsheet/references/formulas.md#L1) | 1 |
| [Why recalculation is mandatory](../../../../opt/hatch/skills/artifacts/spreadsheet/references/formulas.md#L3) | 3 |
| [Choosing formulas that survive](../../../../opt/hatch/skills/artifacts/spreadsheet/references/formulas.md#L25) | 25 |
| [openpyxl gotchas](../../../../opt/hatch/skills/artifacts/spreadsheet/references/formulas.md#L48) | 48 |
| [Editing an existing workbook](../../../../opt/hatch/skills/artifacts/spreadsheet/references/formulas.md#L62) | 62 |

### references/visual.md

| 源章节 | 起始行 |
|---|---|
| [Spreadsheet Visual Guidance](../../../../opt/hatch/skills/artifacts/spreadsheet/references/visual.md#L5) | 5 |
| [Validation](../../../../opt/hatch/skills/artifacts/spreadsheet/references/visual.md#L20) | 20 |
| [Financial-model conventions](../../../../opt/hatch/skills/artifacts/spreadsheet/references/visual.md#L41) | 41 |
