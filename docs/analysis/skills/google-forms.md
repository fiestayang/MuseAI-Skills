# google-forms：表单结构与回答的对应读取

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

表单结构与回答的对应读取。入口：[SKILL.md](../../../opt/hatch/skills/google-forms/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `google-forms` |
| frontmatter name | `google_forms` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read, create, and update the user's Google Forms, and read responses.

<a id="flow"></a>
## 执行流程与输入输出

status 后使用 forms.get 获取题目结构；创建或 batchUpdate 修改表单；读取 responses.list/get；用户要全部回答时分页到无 nextPageToken；把 question IDs 转为题目标题再展示。

<a id="design"></a>
## 实现思路、异常与限制

答案解析依赖表单版本与问题映射，不能孤立展示回答记录。未发布的私人表单与已共享/发布表单编辑适用不同权限。

只读第一页会漏报；题目重排或删除会让 ID 与当前标题对应不完整。工具成功不等于表单已经发布或用户收到邀请。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/google-forms/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/google-forms/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### google-forms/manifest.yaml

来源：[opt/hatch/skills/google-forms/manifest.yaml](../../../opt/hatch/skills/google-forms/manifest.yaml)；connector：`google_forms`。

CLI 绑定：`binary=hatch_gws_cli`, `skill=google_forms`, `service=forms`。

请求配额声明：`mode` = `enforce`；`workers` = `['hatch-gws-cli-fully-isolated']`；`queries_per_minute` = `60`；`burst` = `20`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `forms.get` | `allow` | 否 | — | Access forms |
| `read` | `forms.responses.list` | `allow` | 否 | — | Access form responses |
| `write` | `forms.create` | `allow` | 是 | — | Create forms |
| `write` | `forms.batch_update.private` | `allow` | 是 | — | Edit private and unpublished forms |
| `write` | `forms.batch_update.shared` | `ask` | 否 | — | Edit shared or published forms |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `forms.responses.get` | `forms.responses.list` |
| `forms.set_publish_settings` | `forms.batch_update.private` |
| `forms.watches.create` | `forms.create` |
| `forms.watches.delete` | `forms.create` |
| `forms.watches.list` | `forms.get` |
| `forms.watches.renew` | `forms.create` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时将表单 schema 与 response 一起采集，记录版本/读取时间，对未知题目 ID 保留未映射状态。

最小验收建议：多页回答与一个已删除问题的回答应全部保留，并明确无法映射部分，不能猜题目。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Google Forms](../../../opt/hatch/skills/google-forms/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/google-forms/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/google-forms/SKILL.md#L13) | 13 |
| [Connection management](../../../opt/hatch/skills/google-forms/SKILL.md#L20) | 20 |
| [Forms operations](../../../opt/hatch/skills/google-forms/SKILL.md#L27) | 27 |
| [Auth](../../../opt/hatch/skills/google-forms/SKILL.md#L49) | 49 |
| [First-use setup flow](../../../opt/hatch/skills/google-forms/SKILL.md#L52) | 52 |
| [Operating Rules](../../../opt/hatch/skills/google-forms/SKILL.md#L58) | 58 |
