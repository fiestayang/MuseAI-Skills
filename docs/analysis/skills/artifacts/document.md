# artifacts/document：Word 文档生成与编辑

[返回技能目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Word 文档生成与编辑。入口：[SKILL.md](../../../../opt/hatch/skills/artifacts/document/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `artifacts/document` |
| frontmatter name | `artifact_document` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Create, read, edit, or manipulate Word documents (.docx) and Word templates (.dotx). Use whenever a build task's artifact kind is document with the default docx output, or the task mentions a Word doc, .docx, or .dotx, extracts or reorganizes content from one, inserts or replaces images, does find-and-replace in one, or works with tracked changes (redlines) or comments. Covers python-docx generation, raw OOXML editing of existing files, document structure and formatting, and render verification. Not for PDFs, spreadsheets, or Google Docs.

<a id="flow"></a>
## 执行流程与输入输出

按新建或已有文档分流，读取视觉、文本或 OOXML 编辑参考；保持真实标题样式、列表编号和核心 title；现有文档按原有结构做最小修改；LibreOffice 转 PDF、逐页栅格化并检查后交付。

<a id="design"></a>
## 实现思路、异常与限制

将可编辑文档结构与视觉外观同时纳入契约。editing 说明解包、定位 run、修改 XML、打包的过程，并覆盖修订和评论；文本跨多个 run 时不能简单字符串替换。

伪列表、用表格模拟横线、run 内塞多段文本都会破坏可编辑性。渲染环境、字体和 OOXML 辅助资源并非随本 skill 完整交付。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../../opt/hatch/skills/artifacts/document/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/editing.md](../../../../opt/hatch/skills/artifacts/document/references/editing.md) | 先识别原文件与修订要求，解包后在原 XML 上定位段落/run，再重打包与渲染。跨 run 文本、插入删除标记和评论范围各有独立语义，适合迁移为文档 adapter 的验收约束。 |
| [references/visual.md](../../../../opt/hatch/skills/artifacts/document/references/visual.md) | 约束页面、字体、层级和段落的可读性。它指导生成外观，不能代替真实编号和标题样式；迁移时映射到现有模板样式。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时保留原文档作为基线，修改业务需要的节点，另外生成页图验收。只有需要保留修订语义时才使用底层 OOXML。

最小验收建议：用跨 run 的待替换词及带编号列表文档验证，重新打开并渲染，确认编号、修订和分页不丢失。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Word-document artifacts](../../../../opt/hatch/skills/artifacts/document/SKILL.md#L7) | 7 |
| [Verification](../../../../opt/hatch/skills/artifacts/document/SKILL.md#L26) | 26 |

### references/editing.md

| 源章节 | 起始行 |
|---|---|
| [Editing existing Word documents](../../../../opt/hatch/skills/artifacts/document/references/editing.md#L1) | 1 |
| [The raw-XML round trip](../../../../opt/hatch/skills/artifacts/document/references/editing.md#L14) | 14 |
| [Run fragmentation](../../../../opt/hatch/skills/artifacts/document/references/editing.md#L35) | 35 |
| [Tracked changes (redlining)](../../../../opt/hatch/skills/artifacts/document/references/editing.md#L47) | 47 |
| [Comments](../../../../opt/hatch/skills/artifacts/document/references/editing.md#L82) | 82 |
| [Verify](../../../../opt/hatch/skills/artifacts/document/references/editing.md#L106) | 106 |

### references/visual.md

| 源章节 | 起始行 |
|---|---|
| [Document Visual Guidance](../../../../opt/hatch/skills/artifacts/document/references/visual.md#L5) | 5 |
