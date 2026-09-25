# artifacts/testing：产物的统一验收入口

[返回技能目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

产物的统一验收入口。入口：[SKILL.md](../../../../opt/hatch/skills/artifacts/testing/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `artifacts/testing` |
| frontmatter name | `artifact_testing` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Verify an artifact before delivering it - file deliverables (pdf, pptx, docx, xlsx, csv) and web artifacts alike. Use whenever a build is about to return a link, or a build task asks for validation, QA, or a visual check. Covers the per-kind gate scripts, render-and-look verification, and leftover-placeholder scanning.

<a id="flow"></a>
## 执行流程与输入输出

按 PDF、presentation、docx、xlsx、csv/md 或 web 类型选择 gate；结构验证后读取新生成页图；检查溢出、遮挡、对比度和草稿标记；三次修复失败后报告具体问题并停止无界循环。

<a id="design"></a>
## 实现思路、异常与限制

把生成成功与用户可用分开。共享的验收准则适用于所有产物，但各格式保留自己的机械检查，不用单一截图替代公式或文件完整性检查。

web_artifacts 的工具实现及多个文件 gate 不在快照。规则要求逐页检查，不能根据代码或旧截图证明当前结果。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../../opt/hatch/skills/artifacts/testing/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时为每种交付格式保留最小机械检查，再按需要增加视觉验收；记录构建版本或摘要，防止检查旧产物。

最小验收建议：改动源后保留旧截图，验收流程应要求重新生成；故意制造溢出与残留草稿词，确认均能发现。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Artifact verification](../../../../opt/hatch/skills/artifacts/testing/SKILL.md#L7) | 7 |
| [File kinds: gates, then eyes](../../../../opt/hatch/skills/artifacts/testing/SKILL.md#L15) | 15 |
| [Web artifacts](../../../../opt/hatch/skills/artifacts/testing/SKILL.md#L39) | 39 |
