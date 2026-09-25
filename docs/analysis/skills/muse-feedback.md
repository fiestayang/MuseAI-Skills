# muse-feedback：经授权的反馈提交与去重

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

经授权的反馈提交与去重。入口：[SKILL.md](../../../opt/hatch/skills/muse-feedback/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `muse-feedback` |
| frontmatter name | `muse-feedback` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use for feedback and feature requests to the Muse team. Whenever your response tells the user you can't do a specific thing they wanted, or accepts them giving up on one, offer once to file feedback in that response. This covers missing integrations you can't do yourself, capabilities you lack, and tasks that keep failing at a specific point. File only on their go-ahead. Also use when asked to send, view, check, or withdraw feedback.

<a id="flow"></a>
## 执行流程与输入输出

遇能力缺口可提议一次；用户同意后按 kind、subject 和摘要草拟/提交；个人情况只放本地 context；同一 gap 使用原报告与原审批；查看、撤回先读 CLI 对应 help；官方发布消息才触发进展汇报。

<a id="design"></a>
## 实现思路、异常与限制

外发 summary 与本地 context 分开，避免把个人敏感背景发送团队。kind+subject 对应稳定反馈对象，重复表达不能变成重复票数。

草稿不等于已提交；重复报告流程要求后续回合，不能同一轮假称保存。反馈无工单答复和修复时间承诺。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/muse-feedback/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时外发 payload 与本地上下文用不同 schema 存储，去重键与审批摘要固定，结果区分 drafted 与 delivered。

最小验收建议：同一问题补充个人信息时不应改写原外发摘要或重复计票；首次草稿未发送不能报告完成。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Muse feedback](../../../opt/hatch/skills/muse-feedback/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/muse-feedback/SKILL.md#L10) | 10 |
| [When to offer feedback](../../../opt/hatch/skills/muse-feedback/SKILL.md#L23) | 23 |
| [Positive feedback](../../../opt/hatch/skills/muse-feedback/SKILL.md#L66) | 66 |
| [Filing](../../../opt/hatch/skills/muse-feedback/SKILL.md#L75) | 75 |
| [One report per gap](../../../opt/hatch/skills/muse-feedback/SKILL.md#L164) | 164 |
| [Viewing and withdrawing reports](../../../opt/hatch/skills/muse-feedback/SKILL.md#L192) | 192 |
| [Announcing a shipped request](../../../opt/hatch/skills/muse-feedback/SKILL.md#L201) | 201 |
| [Promises](../../../opt/hatch/skills/muse-feedback/SKILL.md#L206) | 206 |
