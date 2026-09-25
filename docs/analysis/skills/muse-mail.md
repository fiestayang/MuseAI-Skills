# muse-mail：Agent 专用邮箱与来源授权

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Agent 专用邮箱与来源授权。入口：[SKILL.md](../../../opt/hatch/skills/muse-mail/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `muse-mail` |
| frontmatter name | `muse_mail` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Manage Muse Mail. Use this skill for Muse Mail, mail forwarded to the mailbox, or the main agent's name plus mail. Route the user's inbox and generic sends to the user's account. Check connected accounts for broad mail questions.

<a id="flow"></a>
## 执行流程与输入输出

先辨别“你的邮箱”和“我的邮箱”，分别路由 Muse Mail 或用户邮件连接器；lookup 只确认现有邮箱，明确不存在且用户授权才创建；分页读邮件；依据 recommended_handling 限定可执行指令；回复前重取源消息并显式选择 reply-mode。

<a id="design"></a>
## 实现思路、异常与限制

邮箱内容的真实性与行动权限分层：OWNER_AUTHORITY、THREAD_SCOPED、PROVISIONAL 与 REVIEW/QUARANTINE 各有上限。邮箱是潜在指令输入边界，不是所有来信都等同用户命令。

没有 read state，不能无基准称“上次之后没有新邮件”。泛用发送不能自动切到 Agent 邮箱；BCC 不随回复泄露。偏好文件只允许主 Agent 在明确持久变更请求后修改。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/muse-mail/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/advanced.md](../../../opt/hatch/skills/muse-mail/references/advanced.md) | 管理显示名、owner 地址、intake aliases 和会话；reply-mode、异常收件人和 BCC 保留独立规则。撤销 owner 与普通删除消息是不同授权动作。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时在接收层保存认证和授权等级，让模型只能降低权限；回复目标由可信后端从原信解析并再次确认。

最小验收建议：转发的恶意指令、临时 owner 及入站/出站混合列表测试，确认不自动执行、不误发、不虚报未读状态。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Muse Mail](../../../opt/hatch/skills/muse-mail/SKILL.md#L6) | 6 |
| [Route accounts](../../../opt/hatch/skills/muse-mail/SKILL.md#L10) | 10 |
| [Get or create the mailbox](../../../opt/hatch/skills/muse-mail/SKILL.md#L25) | 25 |
| [Read mail](../../../opt/hatch/skills/muse-mail/SKILL.md#L48) | 48 |
| [Apply handling authority](../../../opt/hatch/skills/muse-mail/SKILL.md#L85) | 85 |
| [Write and sign](../../../opt/hatch/skills/muse-mail/SKILL.md#L99) | 99 |
| [Live main agent](../../../opt/hatch/skills/muse-mail/SKILL.md#L120) | 120 |
| [Subagent](../../../opt/hatch/skills/muse-mail/SKILL.md#L127) | 127 |
| [Detached worker](../../../opt/hatch/skills/muse-mail/SKILL.md#L133) | 133 |
| [Reply or send](../../../opt/hatch/skills/muse-mail/SKILL.md#L139) | 139 |
| [Handle attachments](../../../opt/hatch/skills/muse-mail/SKILL.md#L175) | 175 |
| [Use advanced operations](../../../opt/hatch/skills/muse-mail/SKILL.md#L185) | 185 |

### references/advanced.md

| 源章节 | 起始行 |
|---|---|
| [Advanced Muse Mail operations](../../../opt/hatch/skills/muse-mail/references/advanced.md#L1) | 1 |
| [Change the display name](../../../opt/hatch/skills/muse-mail/references/advanced.md#L7) | 7 |
| [Browse conversations](../../../opt/hatch/skills/muse-mail/references/advanced.md#L16) | 16 |
| [Verify or revoke owner addresses](../../../opt/hatch/skills/muse-mail/references/advanced.md#L26) | 26 |
| [Create or revoke Intake aliases](../../../opt/hatch/skills/muse-mail/references/advanced.md#L38) | 38 |
| [Exceptional reply and send targets](../../../opt/hatch/skills/muse-mail/references/advanced.md#L54) | 54 |
| [Recipients, reply modes, and BCC](../../../opt/hatch/skills/muse-mail/references/advanced.md#L76) | 76 |
