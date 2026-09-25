# outlook-mail：Outlook 邮件读取与可恢复删除

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Outlook 邮件读取与可恢复删除。入口：[SKILL.md](../../../opt/hatch/skills/outlook-mail/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `outlook-mail` |
| frontmatter name | `outlook_mail` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Read, search, send, reply to, and delete messages in the user's Outlook Mail.

<a id="flow"></a>
## 执行流程与输入输出

list/search 取候选，get 按需读全文；send 前确认收件人、主题和正文；reply 明确是否 reply-all；delete 移入 Deleted Items；后续使用删除结果返回的新 message_id。

<a id="design"></a>
## 实现思路、异常与限制

移动邮件导致 Graph ID 改变，是与简单“ID 永久不变”假设不同的关键点。message_received_at 是运输时间；邮箱总结默认过滤明显垃圾与无关促销并说明范围。

删除不是永久销毁，不能这样汇报。新旧消息 ID 混用会导致后续定位失败；回复全部需要明确要求。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/outlook-mail/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/outlook-mail/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### outlook-mail/manifest.yaml

来源：[opt/hatch/skills/outlook-mail/manifest.yaml](../../../opt/hatch/skills/outlook-mail/manifest.yaml)；connector：`outlook_mail`。

请求配额声明：`mode` = `enforce`；`workers` = `['outlook-mail']`；`queries_per_minute` = `600`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `messages.list` | `allow` | 否 | ; guard=verification_codes | Search messages |
| `read` | `messages.get` | `allow` | 否 | ; guard=verification_codes | Access messages |
| `write` | `messages.send` | `ask` | 否 | — | Send emails |
| `write` | `messages.mark_read` | `allow` | 是 | — | Mark as read or unread |
| `write` | `messages.delete` | `allow` | 是 | — | Delete emails |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时 mutation result 返回新的实体定位句柄，不假设所有 provider 操作保留 ID；把正文事件时间与收信时间分开。

最小验收建议：删除后再读取应使用新 ID；含多个收件人的回复默认不扩展为 reply-all。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Outlook Mail](../../../opt/hatch/skills/outlook-mail/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/outlook-mail/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/outlook-mail/SKILL.md#L13) | 13 |
| [Auth](../../../opt/hatch/skills/outlook-mail/SKILL.md#L45) | 45 |
| [Operating Rules](../../../opt/hatch/skills/outlook-mail/SKILL.md#L53) | 53 |
