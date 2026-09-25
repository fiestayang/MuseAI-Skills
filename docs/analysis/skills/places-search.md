# places-search：地点检索、详情和地图呈现

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

地点检索、详情和地图呈现。入口：[SKILL.md](../../../opt/hatch/skills/places-search/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `places-search` |
| frontmatter name | `places_search` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Find, compare, and share details on physical places near the user or in a specified area, including restaurants, cafes, bars, hotels, parks, attractions, shops, and businesses with local services. Not for itineraries, choosing a city or region, dated events or showtimes, or directions.

<a id="flow"></a>
## 执行流程与输入输出

browser.search 承接地点发现与名字地址解析；有全数字 place_id 才调用 places details；详情提供同一地点坐标后创建一个 local_map；图片加 GPS 的地点识别走 places detect；无详情时保留带来源的文字回答。

<a id="design"></a>
## 实现思路、异常与限制

发现和详情分层，数字 ID 及坐标必须来自同一已返回记录。多地区分别搜索；地图覆盖相关结果并将文字推荐放前；相同可比评分可用于排序但不直接显示。

没有 numeric ID 时只精确重查一次，不造 ID 或自行 geocode；widget 失败回文字不无限重建。此技能不提供路线或估计交通时间。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/places-search/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [eval/scenarios.yaml](../../../opt/hatch/skills/places-search/eval/scenarios.yaml) | 行为评测场景及测试目标；逐场景列于评测章节，不代表实际通过。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

已有场景仅作为行为规格；本次未运行 Muse 的模拟用户、连接器或线上评测。

### scenarios.yaml

来源：[opt/hatch/skills/places-search/eval/scenarios.yaml](../../../opt/hatch/skills/places-search/eval/scenarios.yaml)。

| 场景 | 类别 | 检查的行为 |
|---|---|---|
| `basic-nearby-discovery` | read | Uses local-search for the nearby set. If any final result has a grounded numeric place ID and coordinates, creates exactly one local_map with rich_place elements and includes its embed token; the user need not ask for a map. |
| `non-food-recreation` | read | Treats paintball as place discovery, uses the requested radius, and creates one grounded local_map when eligible results are returned. Does not fall back to a text-only web list. |
| `place-based-program` | read | Researches age fit when needed, grounds the final camp venues with local-search, and creates one local_map for eligible final results. Does not treat a camp as out of scope merely because it is a program. |
| `subjective-place-constraint` | read | Uses web research for the crowding claim, then grounds the final beaches with local-search and creates one local_map when place IDs and coordinates are available. |
| `dynamic-place-constraint` | read | Uses current sources for hours and wait-time evidence, grounds the final urgent-care clinics with local-search, and creates one local_map for eligible clinics. Clearly qualifies unavailable wait-time data instead of inventing it. |
| `single-known-place-details` | read | Uses known-place search for the intended Apple Store, answers the hours question, and creates one local_map when that single result has a grounded place ID and coordinates. A map does not require multiple recommendations. |
| `neighborhood-comparison` | read | Uses web research for qualitative safety and family-fit claims, grounds final named neighborhoods with local-search, and maps eligible results. Does not confuse choosing neighborhoods within a city with choosing between destination cities. |
| `local-school-quality` | read | Uses current school-quality sources, grounds the final named schools with local-search, and creates one local_map when eligible results are available. Does not answer only with generic neighborhood statistics or omit major nearby schools without explanation. |
| `directions-boundary` | read | Uses the navigation capability for route, travel-time, or turn-by-turn needs rather than forcing Places. Does not create a local_map solely because the destination is a real place. |


<a id="migration"></a>
## 迁移开发指引

迁移时保留地点实体 ID 与证据坐标，UI 降级不改变事实来源。区分 venue discovery、dated event 和 navigation 路由。

最小验收建议：搜索只有名称无 ID 时仍能给有来源文字但不伪造地图；两座同名餐厅应按地区消歧。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Places](../../../opt/hatch/skills/places-search/SKILL.md#L8) | 8 |
| [Common flows](../../../opt/hatch/skills/places-search/SKILL.md#L17) | 17 |
| [Find places](../../../opt/hatch/skills/places-search/SKILL.md#L19) | 19 |
| [Get richer details](../../../opt/hatch/skills/places-search/SKILL.md#L49) | 49 |
| [Show places on a map](../../../opt/hatch/skills/places-search/SKILL.md#L66) | 66 |
| [Identify a place from a photo](../../../opt/hatch/skills/places-search/SKILL.md#L100) | 100 |
| [Response formatting](../../../opt/hatch/skills/places-search/SKILL.md#L108) | 108 |
| [Limits](../../../opt/hatch/skills/places-search/SKILL.md#L134) | 134 |
