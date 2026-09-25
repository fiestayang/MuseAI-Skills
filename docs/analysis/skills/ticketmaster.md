# ticketmaster：活动定位和带价格的座位推荐

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

活动定位和带价格的座位推荐。入口：[SKILL.md](../../../opt/hatch/skills/ticketmaster/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `ticketmaster` |
| frontmatter name | `ticketmaster` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Search Ticketmaster events and seats with pricing. Returns Buy-now links to Ticketmaster checkout; it cannot complete a purchase itself.

<a id="flow"></a>
## 执行流程与输入输出

先通过 Booking 明确场次及票数；search-events 得到活动 ID，event-details 确认日期地点；top-picks 按价格或质量排序；返回真实 checkout 链接及验证过的座位图片；交易由供应商网页继续。

<a id="design"></a>
## 实现思路、异常与限制

CLI 返回 Ticketmaster 原始 payload，不统一包 ok；读 _embedded 和 page 才能正确分页。先广搜实际 section 名再筛选，不能把 section 编号自行解释为楼层或视野。

连接器不能完成购买；只拿到购票链接不等于出票。用户说“三个选项”不等于买三张票。存在 seat-view-carousel 命令但当前 Booking 流程明确不用它。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/ticketmaster/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/ticketmaster/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### ticketmaster/manifest.yaml

来源：[opt/hatch/skills/ticketmaster/manifest.yaml](../../../opt/hatch/skills/ticketmaster/manifest.yaml)；connector：`ticketmaster`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `events.read` | `allow` | 否 | — | Access event details |
| `read` | `tickets.read` | `allow` | 否 | — | Access ticket listings |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时分别建场次 ID、票数、座位属性来源和到手总价字段；把能力列表与当前流程允许使用的呈现形式分开。

最小验收建议：同一演出多日期、Standard/Resale 混合票与未知遮挡属性测试，不得猜场次或座位质量。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Ticketmaster](../../../opt/hatch/skills/ticketmaster/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/ticketmaster/SKILL.md#L9) | 9 |
| [Tooling](../../../opt/hatch/skills/ticketmaster/SKILL.md#L22) | 22 |
| [search-events](../../../opt/hatch/skills/ticketmaster/SKILL.md#L28) | 28 |
| [event-details](../../../opt/hatch/skills/ticketmaster/SKILL.md#L36) | 36 |
| [top-picks](../../../opt/hatch/skills/ticketmaster/SKILL.md#L43) | 43 |
| [seat-view-carousel](../../../opt/hatch/skills/ticketmaster/SKILL.md#L54) | 54 |
| [Output](../../../opt/hatch/skills/ticketmaster/SKILL.md#L61) | 61 |
| [Auth](../../../opt/hatch/skills/ticketmaster/SKILL.md#L129) | 129 |
| [Operating Rules](../../../opt/hatch/skills/ticketmaster/SKILL.md#L132) | 132 |
