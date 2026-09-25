# artifacts/markdown：纯 Markdown 文档交付

[返回技能目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

纯 Markdown 文档交付。入口：[SKILL.md](../../../../opt/hatch/skills/artifacts/markdown/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `artifacts/markdown` |
| frontmatter name | `artifact_markdown` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Build or revise a plain markdown file (md) deliverable such as notes, a README, meeting minutes, documentation, or text the user will edit or paste elsewhere. Use whenever a build task's artifact kind is markdown. Covers markdown formatting conventions and read-back verification.

<a id="flow"></a>
## 执行流程与输入输出

直接写 Markdown 文件，以小段追加和局部编辑维护；参考共享格式约定；按内容选择真实标题、列表和表格；完成后全文回读并扫描未清理的草稿标记。

<a id="design"></a>
## 实现思路、异常与限制

没有编译环节，文件本身就是交付物。质量来自内容结构和回读，避免把构建脚手架、HTML 或聊天说明混入用户文件。

工具写入成功不证明链接、表格或结构正确。它的默认项目根路径是 Muse 产物上下文约定，不应原样替换其他仓库的文档组织。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../../opt/hatch/skills/artifacts/markdown/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时使用已有文件工具和 Markdown 即可；为多文档报告补相对链接检查、目录索引和覆盖清单。

最小验收建议：回读全部正文并检查本地链接目标，确保没有留存占位文本或表格列错位。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Markdown artifacts](../../../../opt/hatch/skills/artifacts/markdown/SKILL.md#L7) | 7 |
| [Verification](../../../../opt/hatch/skills/artifacts/markdown/SKILL.md#L23) | 23 |
