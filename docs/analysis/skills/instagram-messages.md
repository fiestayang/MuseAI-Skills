# instagram-messages：独立私信连接与精确消息发送

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

独立私信连接与精确消息发送。入口：[SKILL.md](../../../opt/hatch/skills/instagram-messages/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `instagram-messages` |
| frontmatter name | `instagram_messages` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use this to interact with the user's Instagram messages. Read inboxes, threads, top recipients, filtered inbox views, DM search results, and send messages through `instagram-messages-cli`.

<a id="flow"></a>
## 执行流程与输入输出

accounts 检查每个账号 connected；未授权先 connect-url；按 inbox/thread 或关键词、联系人、时间搜索缩小范围；发送选择现有 thread 或收件人 FBIDs 其中一种，确定精确正文及回复对象后执行。

<a id="design"></a>
## 实现思路、异常与限制

Instagram 内容连接与 Messages 连接是不同状态。filtered-inbox 只供 professional account；top-recipients 是互动推断，不是 Close Friends 名单。

不批量镜像消息历史，不还原被过滤内容；不从名字推导 FBID。发送产生外部副作用，不能把重试读取的机制不加区分地用于发送。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/instagram-messages/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/instagram-messages/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### instagram-messages/manifest.yaml

来源：[opt/hatch/skills/instagram-messages/manifest.yaml](../../../opt/hatch/skills/instagram-messages/manifest.yaml)；connector：`instagram_messages`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `messages.read` | `allow` | 否 | — | Access messages |
| `write` | `messages.send` | `ask` | 否 | — | Send messages |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时消息 adapter 独立保存授权状态；目标 union 区分 thread 和 recipient list，禁止同时传两种。持久化范围与用户查询范围一致。

最小验收建议：基础 Instagram 已连接而 Messages 未连接应阻止读取；歧义收件人或缺正文不应发送。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Instagram Messages CLI](../../../opt/hatch/skills/instagram-messages/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/instagram-messages/SKILL.md#L10) | 10 |
| [Message Export Safety](../../../opt/hatch/skills/instagram-messages/SKILL.md#L15) | 15 |
| [Auth](../../../opt/hatch/skills/instagram-messages/SKILL.md#L19) | 19 |
| [Operating rules](../../../opt/hatch/skills/instagram-messages/SKILL.md#L36) | 36 |
| [Tooling](../../../opt/hatch/skills/instagram-messages/SKILL.md#L46) | 46 |
| [Global options](../../../opt/hatch/skills/instagram-messages/SKILL.md#L68) | 68 |
| [Commands](../../../opt/hatch/skills/instagram-messages/SKILL.md#L73) | 73 |
| [Connect URL](../../../opt/hatch/skills/instagram-messages/SKILL.md#L75) | 75 |
| [Accounts](../../../opt/hatch/skills/instagram-messages/SKILL.md#L81) | 81 |
| [Inbox](../../../opt/hatch/skills/instagram-messages/SKILL.md#L88) | 88 |
| [Thread + Messages](../../../opt/hatch/skills/instagram-messages/SKILL.md#L102) | 102 |
| [React to message](../../../opt/hatch/skills/instagram-messages/SKILL.md#L111) | 111 |
| [Send message](../../../opt/hatch/skills/instagram-messages/SKILL.md#L120) | 120 |
| [Top recipients](../../../opt/hatch/skills/instagram-messages/SKILL.md#L147) | 147 |
| [Keyword search](../../../opt/hatch/skills/instagram-messages/SKILL.md#L155) | 155 |
| [Contact search](../../../opt/hatch/skills/instagram-messages/SKILL.md#L163) | 163 |
| [Temporal search](../../../opt/hatch/skills/instagram-messages/SKILL.md#L171) | 171 |
| [Filtered inbox](../../../opt/hatch/skills/instagram-messages/SKILL.md#L179) | 179 |
| [Output](../../../opt/hatch/skills/instagram-messages/SKILL.md#L198) | 198 |
