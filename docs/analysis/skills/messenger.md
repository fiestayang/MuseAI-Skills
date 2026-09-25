# messenger：本地同步消息、联系人与安全写入

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

本地同步消息、联系人与安全写入。入口：[SKILL.md](../../../opt/hatch/skills/messenger/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `messenger` |
| frontmatter name | `messenger_read` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Work with the user's Messenger account: read call history; read and search contacts; read, search, and summarize conversations; send, react to, unsend, or edit messages; and message Marketplace listing threads.

<a id="flow"></a>
## 执行流程与输入输出

先区分 Messenger Channel 与 Companion；check 验证 Companion，sync 刷新后查询 retained threads/messages；通过缓存 gap 与 oldest_cached_ts 判断覆盖；定位具体会话和收件人；精确预览后用 --text-stdin 保留正文；edit/unsend 先验证本人消息与支持范围。

<a id="design"></a>
## 实现思路、异常与限制

将同步范围、检索窗口和缓存完整性分开。repair 只重解保留密文，不拉历史；群聊与私聊不能凭同名替代。Marketplace initiate 的 created=false 表示仅拿到既有会话，并没有发送。

Marketplace 不支持 unsend；消息解密失败只说明该行不可读。sync 扩大缓存不等于 search 的日期过滤。正文无 --text 参数，错误拼接 shell 会改变内容。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/messenger/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/messenger/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### messenger/manifest.yaml

来源：[opt/hatch/skills/messenger/manifest.yaml](../../../opt/hatch/skills/messenger/manifest.yaml)；connector：`messenger_read`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `calls.read` | `allow` | 否 | — | Access call history |
| `read` | `messages.read` | `allow` | 否 | — | Access messages |
| `read` | `contacts.read` | `allow` | 否 | — | Access contacts |
| `write` | `messages.compose` | `ask` | 否 | — | Send messages |
| `write` | `messages.edit` | `ask` | 否 | — | Edit or remove messages |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把 sync/read/write 分层，消息正文通过 stdin 或结构化参数传递。写入绑定当前会话类型、参与人和已预览内容。

最小验收建议：测试个人聊天请求只有同名群聊、缓存缺口、created=false 及正文特殊字符；确认不误群发、不虚报已发送。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Messenger](../../../opt/hatch/skills/messenger/SKILL.md#L10) | 10 |
| [Routing and Safety](../../../opt/hatch/skills/messenger/SKILL.md#L14) | 14 |
| [Tooling](../../../opt/hatch/skills/messenger/SKILL.md#L48) | 48 |
| [User-facing output](../../../opt/hatch/skills/messenger/SKILL.md#L73) | 73 |
| [Connect or Disconnect Companion](../../../opt/hatch/skills/messenger/SKILL.md#L87) | 87 |
| [Sync Threads and Messages](../../../opt/hatch/skills/messenger/SKILL.md#L108) | 108 |
| [Resolve Contacts](../../../opt/hatch/skills/messenger/SKILL.md#L127) | 127 |
| [Contact profile links](../../../opt/hatch/skills/messenger/SKILL.md#L144) | 144 |
| [Read Messenger Call History](../../../opt/hatch/skills/messenger/SKILL.md#L157) | 157 |
| [Read Threads and Messages](../../../opt/hatch/skills/messenger/SKILL.md#L171) | 171 |
| [Return URLs from messages](../../../opt/hatch/skills/messenger/SKILL.md#L198) | 198 |
| [Count total messages](../../../opt/hatch/skills/messenger/SKILL.md#L206) | 206 |
| [Link to a specific conversation](../../../opt/hatch/skills/messenger/SKILL.md#L218) | 218 |
| [Search Messages](../../../opt/hatch/skills/messenger/SKILL.md#L240) | 240 |
| [Message Text Input](../../../opt/hatch/skills/messenger/SKILL.md#L259) | 259 |
| [Send a Message](../../../opt/hatch/skills/messenger/SKILL.md#L274) | 274 |
| [Resolve the recipient](../../../opt/hatch/skills/messenger/SKILL.md#L278) | 278 |
| [Preview and execute](../../../opt/hatch/skills/messenger/SKILL.md#L294) | 294 |
| [Automatic replies](../../../opt/hatch/skills/messenger/SKILL.md#L324) | 324 |
| [Initiate a Marketplace conversation](../../../opt/hatch/skills/messenger/SKILL.md#L337) | 337 |
| [React to a Message](../../../opt/hatch/skills/messenger/SKILL.md#L364) | 364 |
| [Edit or Unsend an Existing Message](../../../opt/hatch/skills/messenger/SKILL.md#L408) | 408 |
| [Unsend](../../../opt/hatch/skills/messenger/SKILL.md#L436) | 436 |
| [Edit](../../../opt/hatch/skills/messenger/SKILL.md#L449) | 449 |
| [Repair Unreadable Messages](../../../opt/hatch/skills/messenger/SKILL.md#L468) | 468 |
