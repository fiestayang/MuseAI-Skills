# artifacts/pdf：以 HTML 源生成固定版式 PDF

[返回技能目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

以 HTML 源生成固定版式 PDF。入口：[SKILL.md](../../../../opt/hatch/skills/artifacts/pdf/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `artifacts/pdf` |
| frontmatter name | `artifact_pdf` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Build, revise, or manipulate a fixed-layout PDF (report, guide, one-pager, printable document). Use whenever a build task's artifact kind is pdf, a document build's output format is pdf, or the task reads, merges, splits, crops, or fills an existing PDF, including fillable AcroForms. Covers authoring the print-CSS HTML source, rendering, the geometry and validation gates, existing-PDF manipulation and form filling, and delivery under workspace/your_files.

<a id="flow"></a>
## 执行流程与输入输出

新建或重排时保留 .src 下的 HTML 与 print CSS，按 workflow 编排，运行 render_audit 产出 PDF 和页图，再通过 validate_pdf 检查完整性并逐页观察。已有 PDF 的拆并、提取、表单处理由 existing-pdfs 分支指导。

<a id="design"></a>
## 实现思路、异常与限制

生成型 PDF 把源文件作为可编辑真相，二进制由源重新生成；这不应误读成禁止对外来 PDF 做 pypdf 操作。几何 gate 和视觉检查分别覆盖溢出与实际可读性。

render_audit.mjs 和 validate_pdf.sh 未随快照交付。表单处理需要保持既有字段、appearance 与加密约束；语法合法不证明字段在所有阅读器可见。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../../opt/hatch/skills/artifacts/pdf/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/existing-pdfs.md](../../../../opt/hatch/skills/artifacts/pdf/references/existing-pdfs.md) | 区分读/拆并/裁剪与 AcroForm 填写，说明加密损坏输入和 appearance 验证。保留未修改字段的 NeedAppearances 行为，填完需重新渲染，不能只检查字段字典。 |
| [references/visual.md](../../../../opt/hatch/skills/artifacts/pdf/references/visual.md) | 固定页面的留白、层级与内容密度规范。布局来源是 print CSS，设计是否合格最终依靠每页图像而不是 CSS 参数。 |
| [references/workflow.md](../../../../opt/hatch/skills/artifacts/pdf/references/workflow.md) | 给出 project_dir、可编辑源、渲染报告、几何 gate 和迭代步骤。目标内产物不一定存 your_files；必须使用任务给定项目路径；辅助脚本在快照缺失。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时采用现有 PDF 引擎，明确源与产物关系，并保留每页渲染图。只有用户任务要求编辑原 PDF 时使用对应编辑分支。

最小验收建议：用跨页表格和已有填写值的 AcroForm 验证，检查页数、文字截断和未修改字段的显示。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [PDF artifacts](../../../../opt/hatch/skills/artifacts/pdf/SKILL.md#L7) | 7 |
| [Scripts](../../../../opt/hatch/skills/artifacts/pdf/SKILL.md#L22) | 22 |
| [Verification](../../../../opt/hatch/skills/artifacts/pdf/SKILL.md#L29) | 29 |

### references/existing-pdfs.md

| 源章节 | 起始行 |
|---|---|
| [Working with existing PDFs](../../../../opt/hatch/skills/artifacts/pdf/references/existing-pdfs.md#L1) | 1 |
| [Filling forms](../../../../opt/hatch/skills/artifacts/pdf/references/existing-pdfs.md#L23) | 23 |
| [Encrypted or damaged inputs](../../../../opt/hatch/skills/artifacts/pdf/references/existing-pdfs.md#L141) | 141 |
| [Verify](../../../../opt/hatch/skills/artifacts/pdf/references/existing-pdfs.md#L148) | 148 |

### references/visual.md

| 源章节 | 起始行 |
|---|---|
| [PDF Visual Guidance](../../../../opt/hatch/skills/artifacts/pdf/references/visual.md#L5) | 5 |

### references/workflow.md

| 源章节 | 起始行 |
|---|---|
| [PDF artifacts](../../../../opt/hatch/skills/artifacts/pdf/references/workflow.md#L5) | 5 |
| [Content checks by artifact type](../../../../opt/hatch/skills/artifacts/pdf/references/workflow.md#L171) | 171 |
