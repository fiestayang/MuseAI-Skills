# artifacts/presentation：逐页 HTML 的演示文稿流水线

[返回技能目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

逐页 HTML 的演示文稿流水线。入口：[SKILL.md](../../../../opt/hatch/skills/artifacts/presentation/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `artifacts/presentation` |
| frontmatter name | `artifact_presentation` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Build or revise a slide deck (pptx by default; pdf or html on request). Use whenever a build task's artifact kind is presentation, or the user asks for a deck, slides, or a presentation. Covers per-slide HTML authoring, the StylePlan theme system, font embedding, deck assembly, render gates, and the PPTX export.

<a id="flow"></a>
## 执行流程与输入输出

先编译 StylePlan，生成共享 deck.css、deck.json 和稳定 slide IDs；每页写独立 HTML；嵌入字体、组装并执行 gate；新鲜渲染所有页图；由已验证图片导出 PPTX。修订时读取原主题和源页，保留不受影响的页与 ID。

<a id="design"></a>
## 实现思路、异常与限制

把内容、主题、页面源和导出拆开，使重建可重复。PPTX 主要由栅格页图组成，标题进入讲者备注是有限无障碍补充，不能等同于原生可编辑文本。

hatch-slide-style 是现存 ELF，但 embed_deck_fonts、assemble_deck、render_audit、build_pptx 源脚本缺失。Google Slides 导入后文字不可编辑需要提前说明。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../../opt/hatch/skills/artifacts/presentation/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/authoring.md](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md) | 从叙事结构到每页论点，再到布局、图像和图表；文本溢出要调整布局而非无限缩小字体。各式布局属于作者规则，不证明运行时自动完成设计。 |
| [references/design-system.md](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md) | 定义 theme tokens、画布、内容布局、封面和 closing 的 CSS 结构。作为作者模板，需与实际 StylePlan 输出一致，不能另造一套主题。 |
| [references/editing.md](../../../../opt/hatch/skills/artifacts/presentation/references/editing.md) | 先读原 deck 源与主题，按用户意图只改目标页；保持 slide ID，再组装、验证和导出。旧截图不构成新版本验收证据。 |
| [references/image-directive.md](../../../../opt/hatch/skills/artifacts/presentation/references/image-directive.md) | 约束每页生成图像的目的、构图和使用时机；图片用于叙事而非填空装饰。依赖外部图像生成能力，本文只提供指令契约。 |
| [references/theme.md](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md) | 分 ui 与 visual 字段定义主题，生成后交 hatch-slide-style 编译并应用。schema 是生产者与作者之间的接口，字体不可下载的处理与布局 gate 分开。 |
| [references/visual.md](../../../../opt/hatch/skills/artifacts/presentation/references/visual.md) | 给出演示文稿排版和视觉限制；这些属于该产品审美约束，迁移时可替换品牌规范，但应保留可读性和溢出检查。 |
| [references/workflow.md](../../../../opt/hatch/skills/artifacts/presentation/references/workflow.md) | 完整新 deck 的源目录、manifest、主题、字体、组装、截图及 PPTX 导出流程。机器 gate 和逐页目视验收都必须完成；导出的图片页有可编辑性限制。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时先决定可编辑性要求：若要编辑对象，应选择原生 PPTX 作者路径；若允许图片幻灯片，可以复用 HTML 渲染链，但必须保留源与稳定页 ID。

最小验收建议：验证中间删页后其他 IDs 不变、组装拒绝越界样式、导出页数与 manifest 一致，并明确图片页的限制。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Slide-deck artifacts](../../../../opt/hatch/skills/artifacts/presentation/SKILL.md#L7) | 7 |
| [Scripts](../../../../opt/hatch/skills/artifacts/presentation/SKILL.md#L29) | 29 |
| [Verification](../../../../opt/hatch/skills/artifacts/presentation/SKILL.md#L39) | 39 |

### references/authoring.md

| 源章节 | 起始行 |
|---|---|
| [Slide authoring rulebook](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L5) | 5 |
| [Content strategy](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L17) | 17 |
| [Simplicity and restraint](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L34) | 34 |
| [Layout and composition](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L44) | 44 |
| [Typography and color](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L70) | 70 |
| [Images](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L130) | 130 |
| [Charts and diagrams](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L176) | 176 |
| [Overflow and card sizing](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L183) | 183 |
| [Layouts and lockups](../../../../opt/hatch/skills/artifacts/presentation/references/authoring.md#L206) | 206 |

### references/design-system.md

| 源章节 | 起始行 |
|---|---|
| [Slide design system](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L5) | 5 |
| [Theme tokens (`:root`)](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L14) | 14 |
| [Canvas](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L62) | 62 |
| [Content layout classes](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L84) | 84 |
| [Cover hero scaffolds](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L105) | 105 |
| [Lockups (text + image on a content slide)](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L187) | 187 |
| [Closing](../../../../opt/hatch/skills/artifacts/presentation/references/design-system.md#L199) | 199 |

### references/editing.md

| 源章节 | 起始行 |
|---|---|
| [Slide deck editing](../../../../opt/hatch/skills/artifacts/presentation/references/editing.md#L5) | 5 |
| [Load first (always)](../../../../opt/hatch/skills/artifacts/presentation/references/editing.md#L12) | 12 |
| [Apply the change by intent](../../../../opt/hatch/skills/artifacts/presentation/references/editing.md#L45) | 45 |
| [Keep the theme unless asked](../../../../opt/hatch/skills/artifacts/presentation/references/editing.md#L89) | 89 |
| [Re-assemble, re-validate and re-export](../../../../opt/hatch/skills/artifacts/presentation/references/editing.md#L95) | 95 |

### references/image-directive.md

| 源章节 | 起始行 |
|---|---|
| [Image generation directive](../../../../opt/hatch/skills/artifacts/presentation/references/image-directive.md#L5) | 5 |
| [Examples](../../../../opt/hatch/skills/artifacts/presentation/references/image-directive.md#L64) | 64 |
| [When to generate](../../../../opt/hatch/skills/artifacts/presentation/references/image-directive.md#L76) | 76 |

### references/theme.md

| 源章节 | 起始行 |
|---|---|
| [Theme schema and generation](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md#L5) | 5 |
| [Theme file schema](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md#L11) | 11 |
| [`ui` block fields](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md#L34) | 34 |
| [`visual` block fields](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md#L47) | 47 |
| [Generating a theme](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md#L60) | 60 |
| [Applying a theme (builder side)](../../../../opt/hatch/skills/artifacts/presentation/references/theme.md#L69) | 69 |

### references/visual.md

| 源章节 | 起始行 |
|---|---|
| [Presentation Visual Guidance](../../../../opt/hatch/skills/artifacts/presentation/references/visual.md#L5) | 5 |

### references/workflow.md

| 源章节 | 起始行 |
|---|---|
| [Slide deck build workflow](../../../../opt/hatch/skills/artifacts/presentation/references/workflow.md#L5) | 5 |
| [Steps](../../../../opt/hatch/skills/artifacts/presentation/references/workflow.md#L24) | 24 |
| [Quality gate](../../../../opt/hatch/skills/artifacts/presentation/references/workflow.md#L404) | 404 |
