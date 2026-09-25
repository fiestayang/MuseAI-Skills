# plaid：跨金融机构的只读账户数据

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

跨金融机构的只读账户数据。入口：[SKILL.md](../../../opt/hatch/skills/plaid/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `plaid` |
| frontmatter name | `plaid` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use to connect Plaid and read linked financial accounts: metadata, balances, transactions, recurring transactions, liabilities, and investments.

<a id="flow"></a>
## 执行流程与输入输出

status 连接后 accounts 读取账户与余额；多机构通过 credential-id 与 account-id 联合定位；交易用 transactions-sync 及每机构 cursor map 持续读取；recurring、liabilities 与 investments 按问题选用；无 investment account 时不空跑持仓读取。

<a id="design"></a>
## 实现思路、异常与限制

只读财务连接器，资金移动不在能力范围。不同接口分页协议不同：交易增量 cursor、投资交易 offset/count。余额汇总必须说明账户范围，避免把 available、current 与 limit 混加。

机构未全部覆盖不能称总资产；无持仓账户不等于用户现实中没有投资。连接状态、数据时间与币种均需要保留，不能将未知金额记为零。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/plaid/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [eval/scenarios.yaml](../../../opt/hatch/skills/plaid/eval/scenarios.yaml) | 行为评测场景及测试目标；逐场景列于评测章节，不代表实际通过。 |
| [manifest.yaml](../../../opt/hatch/skills/plaid/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### plaid/manifest.yaml

来源：[opt/hatch/skills/plaid/manifest.yaml](../../../opt/hatch/skills/plaid/manifest.yaml)；connector：`plaid`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `accounts.read` | `allow` | 是 | — | View account details |
| `read` | `transactions.read` | `allow` | 否 | — | View transactions and recurring activity |
| `read` | `investments.read` | `allow` | 否 | — | View investments and investment activity |
| `read` | `liabilities.read` | `allow` | 否 | — | View loans and liabilities |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `authorize-url` | `null`（不映射方法；不等于任意放行） |
| `exchange-code` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `accounts` | `accounts.read` |
| `transactions-sync` | `transactions.read` |
| `investments-holdings` | `investments.read` |
| `investments-transactions` | `investments.read` |
| `liabilities` | `liabilities.read` |
| `transactions-recurring` | `transactions.read` |


<a id="eval"></a>
## 已有评测与覆盖

已有场景仅作为行为规格；本次未运行 Muse 的模拟用户、连接器或线上评测。

### scenarios.yaml

来源：[opt/hatch/skills/plaid/eval/scenarios.yaml](../../../opt/hatch/skills/plaid/eval/scenarios.yaml)。

| 场景 | 类别 | 检查的行为 |
|---|---|---|
| `connect` | connect | Disconnected start: agent runs status, gets not_connected, and posts the exact returned connect_url as `[Connect Plaid](<url>)` - no fabricated URL, no Settings redirect, no bank-credential ask, no fabricated balances. Grade on the link; the post-consent continuation is not spawn-testable (a synthetic user cannot complete the Account Center consent). |
| `disconnect` | connect | Runs `plaid disconnect` and posts the returned disconnect_url as `[Disconnect Plaid](<url>)`; no Settings redirect. If status still shows connected right after, the agent must NOT loop on `plaid status` or stand up a background check / goal / cron to watch for disconnection - it posts the link and stops. Grade on the link + absence of a watcher. |
| `balances` | read | Runs `plaid accounts` (balances come from its per-account `balances` field; there is no separate balances command); reports current balances and a correct combined total across accounts; plain language only - no command, flag, JSON, field name, raw account id, or credential id. A masked suffix is allowed only to disambiguate similar accounts. |
| `spending` | read | Reads transactions (transactions-sync); surfaces recent card spending and correctly identifies the genuine duplicate charge without fabricating one or flagging the legitimate duplicate-looking decoys; no jargon. |
| `recurring` | read | Runs transactions-recurring; lists recurring bills/subscriptions (inflow and outflow) in plain language and states it can't cancel them (read-only). Uses the catalog persona because recurring streams cannot be world-seeded. |
| `liabilities` | read | Runs liabilities; reports the credit-card balance, limit, statement amount, and due date correctly, in plain language. Uses the catalog persona because liabilities cannot be world-seeded. |
| `investments` | read | Runs investments-holdings; reports the brokerage positions and their value from the seeded holdings, with no fabricated tickers or amounts; no jargon. |
| `total-across-accounts` | read | Aggregates balances across every account into one combined figure with a correct sum; names accounts in words and does NOT leak account ids or credential ids while distinguishing them. |


<a id="migration"></a>
## 迁移开发指引

迁移时建立明确金额币种及账户类型字段，增量同步保留 added/modified/removed 的语义；不复用到交易执行模块。

最小验收建议：两个机构有相同局部 account ID、不同币种和待入账交易，确认不会错账户、跨币种相加或重复计数。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Plaid](../../../opt/hatch/skills/plaid/SKILL.md#L9) | 9 |
| [Connecting](../../../opt/hatch/skills/plaid/SKILL.md#L15) | 15 |
| [Common flows](../../../opt/hatch/skills/plaid/SKILL.md#L22) | 22 |
| [Accounts and balances](../../../opt/hatch/skills/plaid/SKILL.md#L24) | 24 |
| [Spending and transactions](../../../opt/hatch/skills/plaid/SKILL.md#L27) | 27 |
| [Recurring bills and subscriptions](../../../opt/hatch/skills/plaid/SKILL.md#L30) | 30 |
| [Loans and credit](../../../opt/hatch/skills/plaid/SKILL.md#L33) | 33 |
| [Investments](../../../opt/hatch/skills/plaid/SKILL.md#L36) | 36 |
| [Rules](../../../opt/hatch/skills/plaid/SKILL.md#L39) | 39 |
| [Limits](../../../opt/hatch/skills/plaid/SKILL.md#L50) | 50 |
