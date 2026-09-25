# muse_db：受限数据库诊断入口

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

受限数据库诊断入口。入口：[SKILL.md](../../../opt/hatch/skills/muse_db/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `muse_db` |
| frontmatter name | `muse_db` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Inspect database-backed Muse records for diagnosis and cross-table tracing when purpose-built product tools do not expose the needed state.

<a id="flow"></a>
## 执行流程与输入输出

普通产品操作先用所属工具；只有跨表诊断和历史追踪才读 schema.md、编写一个有界 SELECT；使用 schema-qualified 表名与允许函数；连接时给列独立别名；结果截断后缩小时间窗或条件。

<a id="design"></a>
## 实现思路、异常与限制

查询表面通过函数和 cast 白名单、结果行数/字节/时间限制，以及对私有推理的脱敏投影控制数据范围。单条 SELECT 本身不是充分安全条件，文档明确 PostgreSQL 函数也可能有副作用。

凭据、系统目录、Sentinel 审批库和每个 artifact 的 app.db 均不在范围。被隐藏的列报错与被过滤的行缺失含义不同，不能都解释为记录丢失。执行器源码未提供。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/muse_db/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/schema.md](../../../opt/hatch/skills/muse_db/references/schema.md) | 生成式数据库契约，列出允许 SQL、软引用解析、schema/table/column、关系和脱敏限制。逐表导航与字段数量见数据库附录；这些是可查询投影的描述，不是 migrations 或真实数据库数据。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时优先有限诊断 API；确需 SQL 时结合只读数据库角色、语法限制、函数白名单和独立脱敏 view。不要让可观测入口成为任意数据库代理。

最小验收建议：验证重复列名、递归 CTE、不允许的函数及越权表均被拒绝；正常跨表查询保留唯一列名并说明截断范围。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Database inspection with `muse.db`](../../../opt/hatch/skills/muse_db/SKILL.md#L7) | 7 |

数据库 schema 的逐表解读见 [数据库附录](../appendices/database-schema.md)。
