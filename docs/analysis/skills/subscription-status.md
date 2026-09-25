# subscription-status：实时套餐与额度查询

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

实时套餐与额度查询。入口：[SKILL.md](../../../opt/hatch/skills/subscription-status/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `subscription-status` |
| frontmatter name | `subscription_status` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Answer questions about the user's Muse subscription, account or plan, current tier, usage, credits, remaining balance, quota, usage or rate limits, billing, reset timing, available subscription tiers, plan prices and costs, upgrades, or the subscription product catalog.

<a id="flow"></a>
## 执行流程与输入输出

仅直接询问订阅、价格、用量或重置时触发；只问当前状态调用 status，只问方案调用 plans，兼问两者调用 overview；单次返回安全事实简报后自然回答。

<a id="design"></a>
## 实现思路、异常与限制

将易变业务事实封装为一个权威查询，避免多次调用取到不一致状态。它是查询接口，不是升级、扣费或购买入口。

不能从历史回答或模型知识推断价格；额度耗尽不应自行推销升级。没有返回的计费原因和 reset 时间不能补猜。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/subscription-status/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时提供面向回答的最小 DTO，保留数据时点、币种和时区；业务变更另设明确授权命令。

最小验收建议：混合问题应只调用 overview 一次；缺失 reset 时刻应明确未知。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Subscription Status](../../../opt/hatch/skills/subscription-status/SKILL.md#L7) | 7 |
