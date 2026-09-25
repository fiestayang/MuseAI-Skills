# notion：动态 MCP 文档操作

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

动态 MCP 文档操作。入口：[SKILL.md](../../../opt/hatch/skills/notion/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `notion` |
| frontmatter name | `notion` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Search, read, create, and update Notion pages via the Notion MCP.

<a id="flow"></a>
## 执行流程与输入输出

status 与 authorize-url 完成连接；list-tools 发现工具名和 input_schema；call-tool 传 JSON object；读取页面或数据库内容后再形成变更；修改前确认具体意图。

<a id="design"></a>
## 实现思路、异常与限制

认证通过 DCR 与 PKCE 的 authd 路径承接，模型只处理连接 URL 和业务参数。文档提到 token 路径但禁止手工编辑，不等于模型需要访问该文件。

动态工具名不应猜测；401 自动刷新后仍失败才回连接流程。日期属性与创建/编辑瞬时字段语义不同。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/notion/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/notion/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### notion/manifest.yaml

来源：[opt/hatch/skills/notion/manifest.yaml](../../../opt/hatch/skills/notion/manifest.yaml)；connector：`notion`。

请求配额声明：`mode` = `enforce`；`workers` = `['notion-cli']`；`queries_per_minute` = `180`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `pages.read` | `allow` | 否 | — | Access content |
| `read` | `search.read` | `allow` | 否 | — | Search content |
| `read` | `workspace.read` | `allow` | 否 | — | Access workspace info |
| `write` | `pages.write` | `ask` | 否 | — | Create and edit content |
| `write` | `comments.write` | `ask` | 否 | — | Add comments |
| `write` | `databases.write` | `ask` | 否 | — | Create and edit databases |
| `write` | `views.write` | `ask` | 否 | — | Change database views |
| `write` | `attachments.write` | `ask` | 否 | — | Upload files |
| `write` | `skills.write` | `ask` | 否 | — | Publish skills |
| `write` | `agents.write` | `ask` | 否 | — | Run custom agents |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时让 MCP adapter 负责 schema 校验、认证与刷新；应用层只接收可用工具契约和标准错误。

最小验收建议：拒绝数组型 arguments-json；模拟工具目录变更，确认旧工具名失效时重新发现而非重试猜名。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Notion](../../../opt/hatch/skills/notion/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/notion/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/notion/SKILL.md#L14) | 14 |
| [Connection management](../../../opt/hatch/skills/notion/SKILL.md#L21) | 21 |
| [MCP operations](../../../opt/hatch/skills/notion/SKILL.md#L31) | 31 |
| [Auth](../../../opt/hatch/skills/notion/SKILL.md#L42) | 42 |
| [First-use setup flow](../../../opt/hatch/skills/notion/SKILL.md#L47) | 47 |
| [Operating Rules](../../../opt/hatch/skills/notion/SKILL.md#L63) | 63 |
