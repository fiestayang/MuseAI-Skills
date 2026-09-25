# google-slides：演示文稿生成后转换发布

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

演示文稿生成后转换发布。入口：[SKILL.md](../../../opt/hatch/skills/google-slides/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `google-slides` |
| frontmatter name | `google_slides` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read, create, and edit the user's Google Slides presentations.

<a id="flow"></a>
## 执行流程与输入输出

新建整套内容先由 presentation artifact 生成 PPTX；创建空 presentation，再以 Drive files.update 上传原 ID；回读页面数；修订仍修改 artifact 再上传，先检查线上是否发生编辑。

<a id="design"></a>
## 实现思路、异常与限制

Google Slides 在这里承担发布与展示，作者源在本地。presentation 的图片式导出意味着 Slides 中的文字不能原生编辑，流程明确要求告知用户。

API 提供 batchUpdate 不代表推荐用它从零拼整套内容。全量上传会替换所有页并丢弃线上改动；共享目标还需审批。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/google-slides/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/google-slides/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### google-slides/manifest.yaml

来源：[opt/hatch/skills/google-slides/manifest.yaml](../../../opt/hatch/skills/google-slides/manifest.yaml)；connector：`google_slides`。

CLI 绑定：`binary=hatch_gws_cli`, `skill=google_slides`, `service=slides`。

请求配额声明：`mode` = `enforce`；`workers` = `['hatch-gws-cli-fully-isolated']`；`queries_per_minute` = `60`；`burst` = `20`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `presentations.get` | `allow` | 否 | — | Access presentations |
| `write` | `presentations.create` | `allow` | 是 | — | Create presentations |
| `write` | `presentations.batch_update.private` | `allow` | 是 | — | Edit private presentations |
| `write` | `presentations.batch_update.shared` | `ask` | 否 | — | Edit shared presentations |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `presentations.pages.get` | `presentations.get` |
| `presentations.pages.get_thumbnail` | `presentations.get` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时先确认编辑性要求，再选择图片式或原生对象式导出；为全量发布保留远端变更检测。

最小验收建议：确认转换页数与源 deck 一致，在报告中明确图片页；线上插入一页后再次上传应先识别冲突。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Google Slides](../../../opt/hatch/skills/google-slides/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/google-slides/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/google-slides/SKILL.md#L13) | 13 |
| [Connection management](../../../opt/hatch/skills/google-slides/SKILL.md#L20) | 20 |
| [Slides operations](../../../opt/hatch/skills/google-slides/SKILL.md#L27) | 27 |
| [Composing presentation content](../../../opt/hatch/skills/google-slides/SKILL.md#L45) | 45 |
| [Auth](../../../opt/hatch/skills/google-slides/SKILL.md#L54) | 54 |
| [First-use setup flow](../../../opt/hatch/skills/google-slides/SKILL.md#L57) | 57 |
| [Operating Rules](../../../opt/hatch/skills/google-slides/SKILL.md#L63) | 63 |
