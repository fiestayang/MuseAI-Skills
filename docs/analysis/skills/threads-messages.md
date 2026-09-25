# threads-messages：Threads 私信读取与不可重试发送

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Threads 私信读取与不可重试发送。入口：[SKILL.md](../../../opt/hatch/skills/threads-messages/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `threads-messages` |
| frontmatter name | `threads_messages` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use this to interact with the user's Threads messages: read inboxes and message threads, and send messages through `threads-messages-cli`.

<a id="flow"></a>
## 执行流程与输入输出

从 threads-cli accounts 得到本人账户 ID；Messages 单独完成连接；inbox 定位 thread，thread 分页读取；send 只能选一个既有 thread 或 1–11 个唯一正十进制 recipient FBIDs，并绑定正文或帖子及目标。

<a id="design"></a>
## 实现思路、异常与限制

基础 Threads 与 Messages 授权分离。发送检查 write correlation、账户 consent、授权和 quota；读 cursor 与写 message_id 是不透明句柄，不可把消息 ID 解析为 FBID。

发送禁用 retries；超时不说明未发送。禁止批量历史导出和持久频繁轮询；未成年过滤结果不能被重建绕过。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/threads-messages/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/threads-messages/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### threads-messages/manifest.yaml

来源：[opt/hatch/skills/threads-messages/manifest.yaml](../../../opt/hatch/skills/threads-messages/manifest.yaml)；connector：`threads_messages`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `messages.read` | `allow` | 否 | ; guard=verification_codes | Access messages |
| `write` | `messages.send` | `ask` | 否 | — | Send messages |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时在 runtime schema 中直接表达目标互斥、ID 格式和数量限制；把写关联标识保留在审计层。

最小验收建议：拒绝前导零、重复 recipient、12 人、thread 与 recipient 同时提供，以及缺 Messages consent 的发送。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Threads Messages CLI](../../../opt/hatch/skills/threads-messages/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/threads-messages/SKILL.md#L10) | 10 |
| [Message Export Safety](../../../opt/hatch/skills/threads-messages/SKILL.md#L17) | 17 |
| [Auth](../../../opt/hatch/skills/threads-messages/SKILL.md#L21) | 21 |
| [Tooling](../../../opt/hatch/skills/threads-messages/SKILL.md#L36) | 36 |
| [Global options](../../../opt/hatch/skills/threads-messages/SKILL.md#L49) | 49 |
| [Commands](../../../opt/hatch/skills/threads-messages/SKILL.md#L57) | 57 |
| [Connect URL](../../../opt/hatch/skills/threads-messages/SKILL.md#L59) | 59 |
| [Inbox](../../../opt/hatch/skills/threads-messages/SKILL.md#L65) | 65 |
| [Thread + Messages](../../../opt/hatch/skills/threads-messages/SKILL.md#L75) | 75 |
| [Send message](../../../opt/hatch/skills/threads-messages/SKILL.md#L85) | 85 |
| [Operating rules](../../../opt/hatch/skills/threads-messages/SKILL.md#L145) | 145 |
| [Output](../../../opt/hatch/skills/threads-messages/SKILL.md#L159) | 159 |
