# booking：交易入口和供应商路由

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

交易入口和供应商路由。入口：[SKILL.md](../../../opt/hatch/skills/booking/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `booking` |
| frontmatter name | `booking` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Primary entry point for direct flight, hotel, restaurant, or event-ticket transactions and for bounded live availability checks delegated by Travel Planning. Always use before provider-specific skills or browser work when the user asks to find live availability or prices, compare bookable options, book, or continue an active booking. Do not use for trip planning itself, broad inspiration, opening hours, schedules, flight status, or other factual questions without transaction intent.

<a id="flow"></a>
## 执行流程与输入输出

明确预订意图后先读 flight/hotel/restaurant/ticket 类别参考；复用已授权偏好及背景；补真正阻塞信息；走可用供应商或官网路径；比较实时可售选项；准备到最终承诺边界；按精确条款审批；执行后核实确认号或明确预订状态。

<a id="design"></a>
## 实现思路、异常与限制

Booking 是用户侧交易协调者，provider skill 是操作手册。规划委派的有界 live check 仍归规划所有，不自动进入 checkout。连接失败只终止该路径，不终止整个目标。

提交结果不明时先查供应商或确认邮件，不能重试造成重复预订。免费可取消 hold、waitlist 与 confirmed 分开汇报。持久偏好、账户事实与敏感旅客身份分开处理。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/booking/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [assets/airline-logos/NOTICE.md](../../../opt/hatch/skills/booking/assets/airline-logos/NOTICE.md) | 记录航空公司标识的来源和使用说明，仅为归属信息，不能推定所有图标已交付或拥有任意再授权权利。 |
| [assets/airline-logos/UPSTREAM.md](../../../opt/hatch/skills/booking/assets/airline-logos/UPSTREAM.md) | 说明 upstream 资源的组合与使用约定，分析时与 NOTICE 一起保留。商标权与素材包许可是不同问题，不因仓库存档而消失。 |
| [eval/scenarios.yaml](../../../opt/hatch/skills/booking/eval/scenarios.yaml) | 行为评测场景及测试目标；逐场景列于评测章节，不代表实际通过。 |
| [references/browser-booking.md](../../../opt/hatch/skills/booking/references/browser-booking.md) | 一次 checkout 保留同一 browser task；填到最终 review 后停在承诺边界；精确条款获准才继续；结果不明先查账户和邮件，不重开第二笔。 |
| [references/flights.md](../../../opt/hatch/skills/booking/references/flights.md) | 先读取偏好和最小行程，搜最短有用路线并比较完整旅程；保留含税价、行李、退改和机场；根据航司官网与 native 能力选路，呈现使用 flight list 的对应 action。 |
| [references/hotels.md](../../../opt/hatch/skills/booking/references/hotels.md) | 从日期、人数、房型与位置约束形成入住条件；比较全程含费成本、取消规则和实际房间；会员权益与可订库存分别确认，不以酒店名称代替具体房价产品。 |
| [references/presentation.md](../../../opt/hatch/skills/booking/references/presentation.md) | 航班优先原生结构化列表，其他预订采用紧凑 Markdown 对比；最终 review 展示金额、条款和承诺。不能重复多个 widget，也不能把 provider 内部 ID 当可读结果。 |
| [references/restaurants.md](../../../opt/hatch/skills/booking/references/restaurants.md) | 从地区、人数、时段及饮食要求选择餐厅，再核验实际 slot；OpenTable、官网和电话按可用性回退；卡担保和取消费用需在承诺前明确。 |
| [references/tickets.md](../../../opt/hatch/skills/booking/references/tickets.md) | 先锁定活动 occurrence 和票数，再比较 section/row/相邻座位及含费价；Standard/Resale 标签和受限视野必须有来源；连接器只搜索时使用安全网页成交。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

已有场景仅作为行为规格；本次未运行 Muse 的模拟用户、连接器或线上评测。

### scenarios.yaml

来源：[opt/hatch/skills/booking/eval/scenarios.yaml](../../../opt/hatch/skills/booking/eval/scenarios.yaml)。

| 场景 | 类别 | 检查的行为 |
|---|---|---|
| `restaurant-direct` | trigger-positive | Loads booking, restaurants, and presentation guidance before provider work; searches without a questionnaire. If OpenTable is disconnected, recommends its supported low-friction connection and keeps pursuing the official site or another source without waiting or asking permission. |
| `restaurant-availability-intent` | trigger-positive | Treats live availability in preparation for reservation as booking intent and follows the restaurant fallback chain. |
| `flight-direct` | trigger-positive | Loads booking, flights, presentation, and the native flight provider guidance. Starts with one duration-first provider search at limit 300, reuses that result set to show a meaningfully cheaper option when available, and expands only when the first search is insufficient, a materially relevant carrier is missing, or the user requests it. Redirects the complete provider response to an unchanged file before any read-only grouping; it does not pipe, truncate, overwrite, or replace that response with a custom summary. When widget.create is in the tool set, calls it and uses the native structured flight list with complete price, duration, stops, segment timestamps for layovers, carrier, flight, cabin, and catalog airline logos; because this is a direct booking flow, it omits `flight_action` and uses the runtime's default booking CTA. It does not choose Markdown because support is uncertain or the widget schema is complex. Uses the Markdown fallback only when widget.create is absent or a valid call explicitly fails as unsupported. Does not duplicate the comparison, create a second options picker, ask for a typed option letter or flight number, or expose provider commands or ids. Treats the native flight widget's identifying interaction as selection of the complete itinerary, while leaving purchase authorization to the trusted booking approval. |
| `flight-widget-regression` | presentation | Loads booking, flights, presentation, and the native flight provider guidance. Preserves the complete provider offers. If widget.create is available, presents the live choices with one or more native flight lists before responding and does not use a Markdown flight table, including when a worker or subagent performs the search. The owning agent does not relay a worker-authored table, and it corrects and retries malformed widget arguments. Uncertainty about client support, large provider output, schema complexity, delegation, or an invalid tool call is not a fallback condition. |
| `flight-carrier-diversity` | coverage | Searches with limit 300 and duration-first ordering, keeps the original response file unchanged, groups duplicate complete schedules and immaterial fare variants before shortlisting, and checks carrier coverage. If JetBlue is absent from the broad results, runs a targeted B6 search before using Matrix or the airline website and before presenting. Never claims that Duffel lacks JetBlue or that JetBlue does not fly the route merely because one result set omitted it. Searches the relevant named New York airports sequentially when the active request or travel handoff requires a metro-area comparison. Presents only 3–6 distinct useful offers through the native flight widget, relies on that widget for flight selection and its booking action, and does not create a duplicate options picker. |
| `hotel-direct` | trigger-positive | Loads booking, hotels, and presentation guidance. Searches before asking optional preferences, uses a compact Markdown table, includes verified full-stay totals and current terms, and offers a map/proximity comparison with the shortlist. Keeps estimated totals, missing mandatory fees, unknown cancellation terms, and already-passed cancellation deadlines out of the bookable shortlist until reverified. |
| `ticket-direct` | trigger-positive | Loads booking, tickets, presentation, and Ticketmaster guidance. Resolves the exact event and presents exact groups in a Markdown table without HTML, carousel, native list, or picker widgets. |
| `ticket-required-count-and-seat-claim` | grounding | Loads booking, tickets, presentation, and Ticketmaster guidance. Resolves the exact event but asks for the required ticket count before inventory search and repeats that blocker if the user answers only the event question. Does not assume two tickets from a usual party. Distinguishes a best-likelihood shaded side based on venue orientation from exact-seat shade evidence, never promises `fully shaded` or a time when shade reaches the row without current evidence tied to that listing, and gives every offered option an actionable listing path. |
| `provider-fallback` | routing | If OpenTable is disconnected, recommends its exact supported connection action, briefly explains the benefit, and continues without waiting through the official site or another reputable platform. A provider miss or unavailable connector immediately falls through to the official site, another platform, then phone when available. It does not ask whether to try the website and does not request contact details before finding a table. |
| `restaurant-connect-after-fallback-confirmed` | duplicate-protection | Checks the existing booking state and does not create a second reservation. Says that the matching restaurant, date, time, and party size are already booked. Offers OpenTable only for a later change or cancellation when it can manage the existing reservation. |
| `secure-flight-checkout` | privacy | Asks once in chat for Duffel checkout fields, including loyalty account data when the user wants it attached, and continues native checkout. Does not ask for unrelated optional sensitive values, payment-card data, or account credentials, and does not save or repeat chat-supplied values. |
| `no-trigger-trip-planning` | trigger-negative | Does not load booking or any booking category reference for planning without transaction intent. |
| `no-trigger-restaurant-inspiration` | trigger-negative | Does not load booking for broad dining inspiration without reservation intent. |
| `no-trigger-flight-fact` | trigger-negative | Does not load booking for a factual route question without purchase intent. |
| `no-trigger-flight-status` | trigger-negative | Does not load booking for post-booking flight status. |
| `no-trigger-unsupported-appointment` | trigger-negative | Does not load booking because appointments are outside the four supported categories. |


<a id="migration"></a>
## 迁移开发指引

迁移时让交易命令携带选定商品、价格、规则、人数和有效期；审批绑定这些确定字段。库存查询和购买必须是不同阶段。

最小验收建议：模拟库存失效、供应商超时及规划态查价，确认不擅自换日期、不重复下单、不提前准备支付。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Booking](../../../opt/hatch/skills/booking/SKILL.md#L7) | 7 |
| [Non-negotiable behavior](../../../opt/hatch/skills/booking/SKILL.md#L49) | 49 |
| [Boundary](../../../opt/hatch/skills/booking/SKILL.md#L75) | 75 |
| [Operating principle: discover before asking](../../../opt/hatch/skills/booking/SKILL.md#L96) | 96 |
| [What to remember](../../../opt/hatch/skills/booking/SKILL.md#L125) | 125 |
| [Direct-booking flow](../../../opt/hatch/skills/booking/SKILL.md#L161) | 161 |
| [1. Normalize the request](../../../opt/hatch/skills/booking/SKILL.md#L163) | 163 |
| [2. Gather context proactively](../../../opt/hatch/skills/booking/SKILL.md#L174) | 174 |
| [3. Ask only for a true blocker](../../../opt/hatch/skills/booking/SKILL.md#L184) | 184 |
| [4. Search through the best available path](../../../opt/hatch/skills/booking/SKILL.md#L194) | 194 |
| [5. Rank a small set of real options](../../../opt/hatch/skills/booking/SKILL.md#L224) | 224 |
| [6. Prepare to the commitment boundary](../../../opt/hatch/skills/booking/SKILL.md#L248) | 248 |
| [7. Execute and verify](../../../opt/hatch/skills/booking/SKILL.md#L273) | 273 |
| [8. Close the loop](../../../opt/hatch/skills/booking/SKILL.md#L289) | 289 |
| [Communication](../../../opt/hatch/skills/booking/SKILL.md#L296) | 296 |

### assets/airline-logos/NOTICE.md

| 源章节 | 起始行 |
|---|---|
| [Airline logo sources](../../../opt/hatch/skills/booking/assets/airline-logos/NOTICE.md#L1) | 1 |

### assets/airline-logos/UPSTREAM.md

| 源章节 | 起始行 |
|---|---|
| [airline-logos](../../../opt/hatch/skills/booking/assets/airline-logos/UPSTREAM.md#L1) | 1 |
| [Usage & Combination Logic](../../../opt/hatch/skills/booking/assets/airline-logos/UPSTREAM.md#L8) | 8 |
| [Disclaimer & Fair Use](../../../opt/hatch/skills/booking/assets/airline-logos/UPSTREAM.md#L13) | 13 |

### references/browser-booking.md

| 源章节 | 起始行 |
|---|---|
| [Browser booking](../../../opt/hatch/skills/booking/references/browser-booking.md#L1) | 1 |
| [Keep one checkout alive](../../../opt/hatch/skills/booking/references/browser-booking.md#L14) | 14 |
| [Final review and approval](../../../opt/hatch/skills/booking/references/browser-booking.md#L41) | 41 |
| [Verification and duplicate protection](../../../opt/hatch/skills/booking/references/browser-booking.md#L52) | 52 |
| [Common browser failures](../../../opt/hatch/skills/booking/references/browser-booking.md#L63) | 63 |

### references/flights.md

| 源章节 | 起始行 |
|---|---|
| [Flights](../../../opt/hatch/skills/booking/references/flights.md#L1) | 1 |
| [Build the flight profile before asking](../../../opt/hatch/skills/booking/references/flights.md#L6) | 6 |
| [Minimum search facts](../../../opt/hatch/skills/booking/references/flights.md#L27) | 27 |
| [Search and route](../../../opt/hatch/skills/booking/references/flights.md#L39) | 39 |
| [Search shortest useful journeys first](../../../opt/hatch/skills/booking/references/flights.md#L54) | 54 |
| [Rank on the whole journey](../../../opt/hatch/skills/booking/references/flights.md#L118) | 118 |
| [Flight comparison response](../../../opt/hatch/skills/booking/references/flights.md#L151) | 151 |
| [Prepare and book](../../../opt/hatch/skills/booking/references/flights.md#L261) | 261 |

### references/hotels.md

| 源章节 | 起始行 |
|---|---|
| [Hotels](../../../opt/hatch/skills/booking/references/hotels.md#L1) | 1 |
| [Build the stay profile before asking](../../../opt/hatch/skills/booking/references/hotels.md#L9) | 9 |
| [Minimum search facts](../../../opt/hatch/skills/booking/references/hotels.md#L29) | 29 |
| [Search and route](../../../opt/hatch/skills/booking/references/hotels.md#L46) | 46 |
| [Rank on the full stay](../../../opt/hatch/skills/booking/references/hotels.md#L69) | 69 |
| [Prepare and book](../../../opt/hatch/skills/booking/references/hotels.md#L88) | 88 |

### references/presentation.md

| 源章节 | 起始行 |
|---|---|
| [Booking presentation](../../../opt/hatch/skills/booking/references/presentation.md#L1) | 1 |
| [Response shape](../../../opt/hatch/skills/booking/references/presentation.md#L10) | 10 |
| [Markdown rules](../../../opt/hatch/skills/booking/references/presentation.md#L37) | 37 |
| [Flights](../../../opt/hatch/skills/booking/references/presentation.md#L61) | 61 |
| [Hotels](../../../opt/hatch/skills/booking/references/presentation.md#L93) | 93 |
| [Restaurants](../../../opt/hatch/skills/booking/references/presentation.md#L115) | 115 |
| [Event tickets](../../../opt/hatch/skills/booking/references/presentation.md#L132) | 132 |
| [Final review and confirmation](../../../opt/hatch/skills/booking/references/presentation.md#L147) | 147 |

### references/restaurants.md

| 源章节 | 起始行 |
|---|---|
| [Restaurants](../../../opt/hatch/skills/booking/references/restaurants.md#L1) | 1 |
| [Build the dining profile before asking](../../../opt/hatch/skills/booking/references/restaurants.md#L6) | 6 |
| [Minimum search facts](../../../opt/hatch/skills/booking/references/restaurants.md#L23) | 23 |
| [Search and route](../../../opt/hatch/skills/booking/references/restaurants.md#L35) | 35 |
| [Rank on the actual table](../../../opt/hatch/skills/booking/references/restaurants.md#L80) | 80 |
| [Prepare and book](../../../opt/hatch/skills/booking/references/restaurants.md#L95) | 95 |

### references/tickets.md

| 源章节 | 起始行 |
|---|---|
| [Event tickets](../../../opt/hatch/skills/booking/references/tickets.md#L1) | 1 |
| [Resolve the event before asking](../../../opt/hatch/skills/booking/references/tickets.md#L6) | 6 |
| [Minimum search facts](../../../opt/hatch/skills/booking/references/tickets.md#L24) | 24 |
| [Search and route](../../../opt/hatch/skills/booking/references/tickets.md#L33) | 33 |
| [Rank on the exact seats and delivered price](../../../opt/hatch/skills/booking/references/tickets.md#L51) | 51 |
| [Prepare and book](../../../opt/hatch/skills/booking/references/tickets.md#L73) | 73 |
