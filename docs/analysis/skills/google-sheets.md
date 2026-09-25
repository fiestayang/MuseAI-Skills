# google-sheets：在线表格局部写入和格式验证

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

在线表格局部写入和格式验证。入口：[SKILL.md](../../../opt/hatch/skills/google-sheets/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `google-sheets` |
| frontmatter name | `google_sheets` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read, write, and manage the user's Google Sheets.

<a id="flow"></a>
## 执行流程与输入输出

读取 sheet 与 range；通过 values.update/append 写值，选择 USER_ENTERED；用 spreadsheets.batchUpdate 批量设置格式、冻结行和列宽；回读时显式 fields/ranges 读取 formattedValue 与 effectiveFormat；下载需求另建本地 workbook artifact。

<a id="design"></a>
## 实现思路、异常与限制

在线协作表格坚持 API 局部编辑，不用文件覆盖。spreadsheets.get 默认不含单元格数据，因此回读必须有字段投影，避免把空响应当作验证成功。

禁止 Drive 上传 xlsx 覆盖现有表格，因为会替换所有标签页。共享表格需要外发审批。USER_ENTERED 会解析公式与日期，不能对不可信字符串不加区分地应用。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/google-sheets/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/google-sheets/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### google-sheets/manifest.yaml

来源：[opt/hatch/skills/google-sheets/manifest.yaml](../../../opt/hatch/skills/google-sheets/manifest.yaml)；connector：`google_sheets`。

CLI 绑定：`binary=hatch_gws_cli`, `skill=google_sheets`, `service=sheets`。

请求配额声明：`mode` = `enforce`；`workers` = `['hatch-gws-cli-fully-isolated']`；`queries_per_minute` = `60`；`burst` = `20`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `spreadsheets.get` | `allow` | 否 | — | Access spreadsheets |
| `write` | `spreadsheets.create` | `allow` | 是 | — | Create spreadsheets |
| `write` | `spreadsheets.values.update.private` | `allow` | 是 | — | Update private spreadsheet values |
| `write` | `spreadsheets.values.update.shared` | `ask` | 否 | — | Update shared spreadsheet values |
| `write` | `spreadsheets.batch_update.private` | `allow` | 是 | — | Edit private spreadsheets |
| `write` | `spreadsheets.batch_update.shared` | `ask` | 否 | — | Edit shared spreadsheets |
| `write` | `spreadsheets.values.clear` | `allow` | 是 | — | Clear cell values |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `+read` | `spreadsheets.get` |
| `+append` | `spreadsheets.values.update.private` |
| `spreadsheets.developer_metadata.get` | `spreadsheets.get` |
| `spreadsheets.developer_metadata.search` | `spreadsheets.get` |
| `spreadsheets.get_by_data_filter` | `spreadsheets.get` |
| `spreadsheets.sheets.copy_to` | `spreadsheets.batch_update.shared` |
| `spreadsheets.values.batch_clear` | `spreadsheets.values.clear` |
| `spreadsheets.values.batch_clear_by_data_filter` | `spreadsheets.values.clear` |
| `spreadsheets.values.batch_get` | `spreadsheets.get` |
| `spreadsheets.values.batch_get_by_data_filter` | `spreadsheets.get` |
| `spreadsheets.values.batch_update` | `spreadsheets.values.update.private` |
| `spreadsheets.values.batch_update_by_data_filter` | `spreadsheets.values.update.private` |
| `spreadsheets.values.get` | `spreadsheets.get` |
| `spreadsheets.values.update` | `spreadsheets.values.update.private` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时区分 literal 输入与用户明确要解析的公式；写入范围尽量小，核对 tab ID、A1 范围和受影响单元格。

最小验收建议：包含额外用户标签页的表格修改后必须完整保留；验证日期、币种、公式和字符串的实际有效值。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Google Sheets](../../../opt/hatch/skills/google-sheets/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/google-sheets/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/google-sheets/SKILL.md#L13) | 13 |
| [Connection management](../../../opt/hatch/skills/google-sheets/SKILL.md#L20) | 20 |
| [Sheets operations](../../../opt/hatch/skills/google-sheets/SKILL.md#L27) | 27 |
| [Formatting spreadsheet content](../../../opt/hatch/skills/google-sheets/SKILL.md#L53) | 53 |
| [Auth](../../../opt/hatch/skills/google-sheets/SKILL.md#L62) | 62 |
| [First-use setup flow](../../../opt/hatch/skills/google-sheets/SKILL.md#L65) | 65 |
| [Operating Rules](../../../opt/hatch/skills/google-sheets/SKILL.md#L71) | 71 |
