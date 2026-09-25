# muse-early-access：通用抢先体验的申请与状态

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

通用抢先体验的申请与状态。入口：[SKILL.md](../../../opt/hatch/skills/muse-early-access/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `muse-early-access` |
| frontmatter name | `muse_early_access` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use for questions about Muse's general early access program, requests to join it, checking or withdrawing a join request, and admission updates.

<a id="flow"></a>
## 执行流程与输入输出

只有明确申请通用计划才进入；show 固定 kind=missing-capability、subject=early-access-group；已有确认或撤回状态不重报；明确申请后按工具流程提交；查询 admission，只有 addressed 表示已加入。

<a id="design"></a>
## 实现思路、异常与限制

借用 feature-request 存储机制但保持不同业务语义。想测试一个功能或愿意帮忙不是通用加入授权；撤回申请也不等于立即退出成员资格。

不能承诺优先测试、功能访问或时间。未知送达与已加入不可混淆；撤回后再次加入需要新请求。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/muse-early-access/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把 submitted、delivered、addressed、withdrawn 建成独立状态，不从消息自然语言推导成员权限。

最小验收建议：单功能体验咨询不能创建通用申请；撤回成功后的回答不能声称成员身份已被移除。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Muse early access](../../../opt/hatch/skills/muse-early-access/SKILL.md#L8) | 8 |
| [Joining](../../../opt/hatch/skills/muse-early-access/SKILL.md#L13) | 13 |
| [Status and withdrawal](../../../opt/hatch/skills/muse-early-access/SKILL.md#L43) | 43 |
