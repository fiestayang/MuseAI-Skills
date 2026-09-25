# google-docs：有格式内容发布到 Google Docs

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

有格式内容发布到 Google Docs。入口：[SKILL.md](../../../opt/hatch/skills/google-docs/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `google-docs` |
| frontmatter name | `google_docs` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read, create, and edit the user's Google Docs.

<a id="flow"></a>
## 执行流程与输入输出

先读取已有文档；整篇新建或重写先由 document artifact 生成带样式 docx，再创建空 Google Doc，通过 Drive files.update 上传转换；回读确认样式。局部结构修改使用 documents.batchUpdate；普通纯文本追加才使用 +write。

<a id="design"></a>
## 实现思路、异常与限制

本地 artifact 是整篇作者工作副本，Google Doc 是发布目标。正文开头展示通用 API 示例，但后面的 Composing 章节限制其适用范围，不能把 insertText 示例当整篇创作路径。

重新上传替换全文，会覆盖云端用户新改动，因此先回读、检测变化并取得同意。上传必须是 home 下绝对路径；共享文档编辑还有外发边界。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/google-docs/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/google-docs/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### google-docs/manifest.yaml

来源：[opt/hatch/skills/google-docs/manifest.yaml](../../../opt/hatch/skills/google-docs/manifest.yaml)；connector：`google_docs`。

CLI 绑定：`binary=hatch_gws_cli`, `skill=google_docs`, `service=docs`。

请求配额声明：`mode` = `enforce`；`workers` = `['hatch-gws-cli-fully-isolated']`；`queries_per_minute` = `60`；`burst` = `20`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `documents.get` | `allow` | 否 | — | Access documents |
| `write` | `documents.create` | `allow` | 是 | — | Create documents |
| `write` | `documents.batch_update.private` | `allow` | 是 | — | Edit private documents |
| `write` | `documents.batch_update.shared` | `ask` | 否 | — | Edit shared documents |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `+write --dry-run` | `documents.get` |
| `+write` | `documents.batch_update.private` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时分清发布同步与局部编辑，记录远端 revision 或内容摘要；若已漂移，先协调冲突，不能盲目覆盖。

最小验收建议：在两次发布间修改云端文档，确认第二次上传被拦截等待处理；检查标题与列表样式成功转换。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Google Docs](../../../opt/hatch/skills/google-docs/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/google-docs/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/google-docs/SKILL.md#L13) | 13 |
| [Connection management](../../../opt/hatch/skills/google-docs/SKILL.md#L20) | 20 |
| [Docs operations](../../../opt/hatch/skills/google-docs/SKILL.md#L27) | 27 |
| [Composing document content](../../../opt/hatch/skills/google-docs/SKILL.md#L48) | 48 |
| [Auth](../../../opt/hatch/skills/google-docs/SKILL.md#L57) | 57 |
| [First-use setup flow](../../../opt/hatch/skills/google-docs/SKILL.md#L60) | 60 |
| [Operating Rules](../../../opt/hatch/skills/google-docs/SKILL.md#L66) | 66 |
