# travel-planning：多阶段旅行规划与决策状态维护

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

多阶段旅行规划与决策状态维护。入口：[SKILL.md](../../../opt/hatch/skills/travel-planning/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `travel-planning` |
| frontmatter name | `travel_planning` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use this skill when an active or proposed trip needs planning, logistics, feasibility, entry or transit checks, itinerary work, or investigation of an airport process, immigration, ground transport, a transfer, or fast-track service, even for a narrow question with no booking intent. Route a bounded flight, hotel, restaurant, event, or other item ready for live availability or booking directly to Booking. Skip this skill for a stable travel fact alone or flight status.

<a id="flow"></a>
## 执行流程与输入输出

按下一项未解决决策区分 quick booking 与 planning；先整理已授权上下文和硬约束；比较少量完整方案；维护唯一行程及责任清单；验证时间、通行和交通依赖；把具体候选交 Booking 查实时库存；结果回到原计划，直到用户明确转为 ready to book。

<a id="design"></a>
## 实现思路、异常与限制

关键设计是三组独立状态：proposed/selected/rejected，unchecked/estimated/verified，以及供应商 found/available/confirmed 等状态。查到价格、选中方案与真正订妥不能互相替代。跨轮保持 planning only，避免一次“看看机票”偷偷进入支付。

日历只证明本用户的时间约束，不能推断其他旅客可用；某网站无结果或死链不证明服务关闭。航班变更需重查住宿夜数、接驳和总价；已确认预订默认锁定。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/travel-planning/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [eval/scenarios.yaml](../../../opt/hatch/skills/travel-planning/eval/scenarios.yaml) | 行为评测场景及测试目标；逐场景列于评测章节，不代表实际通过。 |
| [references/booking-handoff.md](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md) | 携带 trip posture、候选、旅客、预算、证据和行程签名；实时结果逐航段匹配；保留现金退款、航空积分与可改签差异；planning only 必须返回计划而非推进支付。 |
| [references/flight-itinerary-discovery.md](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md) | 复杂 open-jaw 等行程可用 ITA Matrix 只读发现，记录稳定 itinerary signature；发现价不等于可购价，失败回其他来源而非堵住全流程。 |
| [references/operational-itinerary.md](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md) | 维护唯一行程与责任清单，局部修订后重核依赖；以本地时间、转场缓冲、成本和证据建立可执行日程；导出 artifact 只代表计划文件存在。 |
| [references/planning-kickoff.md](../../../opt/hatch/skills/travel-planning/references/planning-kickoff.md) | 大量规划可使用 side chat，先调查已授权相关背景再问阻塞问题；不把私人连接上下文带入共享对话，地点推荐需要真实视觉与来源。 |
| [references/travel-fact-verification.md](../../../opt/hatch/skills/travel-planning/references/travel-fact-verification.md) | 逐段检查机场、边界制度及入境/转机假设，最小化证件信息；来源要对应具体结论，建议与购买状态分开。本报告分析规则结构，不确认任何现行旅行法规。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

已有场景仅作为行为规格；本次未运行 Muse 的模拟用户、连接器或线上评测。

### scenarios.yaml

来源：[opt/hatch/skills/travel-planning/eval/scenarios.yaml](../../../opt/hatch/skills/travel-planning/eval/scenarios.yaml)。

| 场景 | 类别 | 检查的行为 |
|---|---|---|
| `bounded-live-flight-search` | routing | Recognizes this as quick booking and routes directly to Booking and the live flight provider. Does not start Travel intake, mine historical preferences, offer a side chat, gather inspirational images, or force an ITA Matrix planning pass. Uses the actual passenger mix and does not claim a fare before a provider returns one. |
| `bounded-nonflight-reservation` | routing | Recognizes this as quick booking and routes directly to Booking and the relevant live provider. Does not start Travel intake, mine historical preferences, offer a side chat, add destination ideas, or expand it into a trip itinerary. |
| `bounded-hotel-booking` | routing | Recognizes the named stay, dates, occupancy, room, refund requirement, and price bound as enough for quick booking. Goes directly to Booking's current hotel website or provider path, without Travel intake, preference mining, a side-chat offer, or unrelated hotel inspiration. Continues toward the normal final-review boundary and reports any missing live term instead of inventing it. |
| `bounded-show-booking` | routing | Recognizes this as quick booking and goes directly to Booking plus the event specialist. Does not open a Travel brief, suggest a side chat, research destination preferences, or add nearby activities. Preserves the exact event, performance, party, seat bounds, and total cap through live verification and approval. |
| `standalone-travel-fact` | routing | Answers the factual question directly without creating itinerary state, checking live inventory, or pushing the user into Travel Planning or Booking. |
| `adjacent-domestic-international-legs` | grounding | Treats the request as an operational decision within an active trip. Normalizes `HAN → DAD` and `DAD → DMK` as separate legs. Classifies `HAN → DAD` as domestic within Vietnam. Classifies `DAD → DMK` as international from Vietnam to Thailand unless an authoritative source proves a route-specific exception. Verifies the arrival process at DMK and every consequential fast-track claim with the authority that owns each fact. Compares only arrival-transfer options that serve DMK under the stated arrival constraints. Does not inherit a domestic-terminal label from `HAN → DAD`, invent an exception, state an unsourced queue time as current fact, start a broad planning intake, or book anything. |
| `same-country-special-border-regime` | grounding | Treats the request as an operational decision within an active trip. Normalizes the exact leg independently. Does not infer the immigration or customs process from shared sovereignty. Verifies the applicable border or customs regime with the responsible government authority. Verifies carrier handling and terminal process with the operating carrier or official airport. Uses only the minimum available eligibility inputs. Marks personalized eligibility unresolved when a required input is absent. Does not request or retain a passport number. |
| `trip-responsibility-checklist` | state | Maintains one compact responsibility checklist and renders it in chat as a Markdown trip-status table with component, current plan, status, and next step. Records an outcome, owner, status, next action or decision, evidence state, and material deadline for every open item internally. Separates planning work supported by available tools, purchases owned by the booking skill or an applicable direct provider, and actions owned by the user. Keeps the user-reported flights locked without claiming supplier verification. Represents the shortlisted hotel, unresolved ryokan policy, and passport renewal as distinct states. Does not create an itinerary artifact during the active planning session, declare the trip complete while required work remains open, expose internal provider identifiers, convert an optional item into a requirement, or imply that a recommendation is booked. |
| `substantial-trip-offers-side-chat` | conversation | Recognizes a substantial planning request in the Main chat and briefly offers a dedicated trip side chat for the itinerary, research, and revisions. When muse.create_options is available, uses it for that bounded choice instead of asking for a typed letter or phrase. Does not create the chat, start a long intake, search private connected sources, or pretend the work moved before the user accepts. It does not mistake the request for quick booking. |
| `accepted-side-chat-handoff` | conversation | Treats the explicit request as approval to move substantial planning. From Main, creates exactly one forked side chat with a short trip-specific name, then sends the returned chat a planning kickoff message; does not misuse chat.create's naming message as the delivered turn and does not poll for the side-chat reply. The handoff tells the new chat to inspect inherited and connected context before asking only material gaps. If supported, navigates to that exact chat after discovering the UI target and reports navigation accurately; otherwise simply identifies the created chat. Does not also start planning in Main. |
| `planning-mines-connected-context` | personalization | Keeps the substantial plan in the current chat because the user explicitly requests it. Without being prompted to inspect mail or calendar, runs narrow read-only searches of the connected mailbox and relevant calendar before asking preferences. Recognizes repeated user-attributed United Economy Plus aisle selections, Hyatt king-room stays, and Hertz midsize rentals as observed provisional defaults, while not exposing confirmation codes, unrelated mail, or treating those patterns as authority to choose or book. Summarizes what is known and asks only the smallest coherent set of remaining material questions. |
| `complex-open-jaw-discovery` | planning | Uses Travel Planning to compare a small number of coherent open-jaw route shapes. If opportunistic mail context is unavailable, does not show a connection link or pause planning. ITA Matrix, if used, is a read-only discovery source. Carries exact segment signatures and explicit flexibility into Booking for live verification. |
| `plan-first-live-options` | handoff | Preserves the explicit plan-first posture when the later bounded flight request routes through Booking. Uses live flight results as planning evidence, presents the itineraries in the native flight widget with the list-level `Add to plan` action and planning response prefix rather than the default booking action, lets the user select or point to a preferred itinerary there without duplicating flights in an options widget, returns the selection to the canonical trip, and updates a compact Markdown trip-status table without creating an artifact. This widget requirement still holds when a worker or subagent performs the search: the owning agent never relays its Markdown comparison and verifies successful widget creation before responding. Does not prepare checkout or request traveler or payment details. After a flight is selected, when muse.create_options is available, offers one bounded choice between keeping the flight in the plan to book later and booking it now, and does not reuse that widget after the decision is consumed. Coordinates flight and hotel implications before recommending either purchase. |
| `indicative-fare-is-not-bookable` | grounding | Recognizes the exact-itinerary verification as quick booking rather than restarting Travel intake or offering a side chat. Treats the ITA Matrix amount as timestamped and indicative. When the exact itinerary or fare is absent from Duffel, does not call it available or globally unavailable; checks the official airline or reports the evidence gap and live alternatives. |
| `codeshare-exact-match` | grounding | Recognizes the exact-itinerary check as quick booking and goes directly to Booking without planning intake or a side chat. Matches every segment using airports, local dates/times, marketing flight, operating flight, order, and cabin. Does not accept a same-number codeshare or a materially changed connection as the selected itinerary. |
| `refundability-tradeoff` | planning | Recognizes that route, date, travelers, and requested comparison are already bounded, skips Travel intake and side-chat setup, and continues directly through Booking. Compares a useful lower-cost live offer with an explicitly flexible alternative. Keeps refundable, changeable, penalty, fare difference, and cash-versus-credit facts distinct; preserves not-stated values instead of guessing. |
| `ita-browser-failure` | recovery | Treats a CAPTCHA, bot wall, broken widget, or incomplete ITA result as a source failure rather than no flights. Falls back to a live provider or another planning source without fabricating an itinerary or repeatedly spawning the same blocked task. |
| `swiss-pass-itinerary-economics` | grounding | Verifies currently sold official pass products before naming a duration, price, eligibility rule, or coverage claim. Compares the actual seven travel days with itemized point-to-point fares for two adults and children aged 7 and 14, showing covered and uncovered legs, required supplements or reservations, source currency, conversion source/date if used, assumptions, arithmetic, official sources, and retrieval time. Does not assert that a seven-day Swiss Travel Pass exists unless a current official source verifies it, and never claims savings from missing inputs. A transparent evidence gap avoids hallucination but is not a full-value result if useful verified components remain researchable. |
| `operational-family-itinerary` | feasibility | Produces a usable chronological plan rather than a place list: verifies every named place and consequential hours or ticket rule, clusters geography, includes sourced transit estimates with uncertainty labeled, realistic durations and buffers, meal/rest windows, rationale, and a grounded backup. Carries the children's ages, heat limits, and pace through every day and flags overload instead of compressing the schedule. Shows one exact, trustworthy photo beside each recommended physical place when available, with a verified source or map fallback rather than a fabricated or generic image. Does not invent a beach, event, venue, opening time, ticket, route, or photo. |
| `location-and-preference-scope` | personalization | Keeps home, temporary location, trip origin, destination, and return location distinct. Plans London to Zurich and Zurich to San Francisco from the user's stated sequence, without treating London as home. Does not transfer a London-specific restaurant preference into Zurich or infer a general cuisine preference; asks or offers neutral grounded options only if dining materially needs resolution. |
| `travel-dates-use-calendar-context` | feasibility | Uses Travel Planning because trip dates are still open. Reads all relevant visible calendars across the three candidate weekends before recommending one, recognizes the seeded New York trip as an all-day location conflict for March 13 and 20, and recommends March 27 or clearly reports that no schedule-verified candidate remains. Does not require the user to remind it to use the connected calendar and reveals only the conflict detail needed for the choice. |
| `canonical-itinerary-revision` | state | Maintains one canonical plan and changes only the requested selected item. Preserves the user-reported confirmed train as locked without inventing supplier proof, keeps the rejected item out, leaves the undecided proposal unselected, introduces no restaurant, and rechecks dependencies after the move. Notices that the year and the post-train Zurich/Lucerne base are unresolved, asks for the smallest concise set of blocking details, and does not call the revision fully feasible meanwhile. Continued discussion does not imply acceptance. |
| `selective-private-itinerary-artifact` | artifact | Creates exactly one private, unshared, editable itinerary artifact because the user explicitly asks. Includes the user-reported locked base, clearly distinguished from supplier-confirmed evidence, and selected items in a chronological schedule; keeps the proposed item only in a clearly open section and excludes the rejected item from the active plan. Shows verified official or reservation links, checked-at times for consequential facts, and useful verified map links with a list fallback. Does not publish, send, book, or promise recipient-scoped private collaboration. |
| `stale-link-and-availability-recovery` | recovery | Audits the exact old itinerary instead of embellishing it. Opens consequential links, detects the guaranteed-invalid URL, verifies the dubious event against a current official source, and distinguishes place existence, an accessible page, current operation, and dated ticket availability. A dead link is treated as a source failure rather than proof of closure. Reports source and retrieval time, labels unresolved facts, and offers any replacement only as a new proposal rather than silently changing the itinerary. |


<a id="migration"></a>
## 迁移开发指引

迁移时先用一个带版本的计划对象，保存候选签名、用户决策、证据时间及预订状态。通用工作流也可用同一结构区分建议、授权和执行结果。

最小验收建议：复合行程在 planning only 下查询航班不得索要证件或支付信息；改一天后只重算受影响依赖，不复活已拒绝候选。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Travel Planning](../../../opt/hatch/skills/travel-planning/SKILL.md#L7) | 7 |
| [Mandate](../../../opt/hatch/skills/travel-planning/SKILL.md#L9) | 9 |
| [Choose the operating mode first](../../../opt/hatch/skills/travel-planning/SKILL.md#L32) | 32 |
| [Build the smallest useful brief](../../../opt/hatch/skills/travel-planning/SKILL.md#L78) | 78 |
| [Keep one responsibility checklist](../../../opt/hatch/skills/travel-planning/SKILL.md#L117) | 117 |
| [Design before optimizing](../../../opt/hatch/skills/travel-planning/SKILL.md#L132) | 132 |
| [Maintain one canonical itinerary](../../../opt/hatch/skills/travel-planning/SKILL.md#L156) | 156 |
| [Make the plan operational and auditable](../../../opt/hatch/skills/travel-planning/SKILL.md#L193) | 193 |
| [Hand concrete candidates to Booking](../../../opt/hatch/skills/travel-planning/SKILL.md#L225) | 225 |
| [Keep decision, evidence, and provider state separate](../../../opt/hatch/skills/travel-planning/SKILL.md#L253) | 253 |
| [Present the plan for decisions and use](../../../opt/hatch/skills/travel-planning/SKILL.md#L279) | 279 |
| [Reference routing](../../../opt/hatch/skills/travel-planning/SKILL.md#L332) | 332 |

### references/booking-handoff.md

| 源章节 | 起始行 |
|---|---|
| [Planning-to-booking handoff](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md#L1) | 1 |
| [Route to the right booking owner](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md#L7) | 7 |
| [Candidate input](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md#L27) | 27 |
| [Establish live truth](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md#L54) | 54 |
| [Compare flexibility honestly](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md#L92) | 92 |
| [Return to planning or continue](../../../opt/hatch/skills/travel-planning/references/booking-handoff.md#L108) | 108 |

### references/flight-itinerary-discovery.md

| 源章节 | 起始行 |
|---|---|
| [Flight itinerary discovery](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md#L1) | 1 |
| [When ITA Matrix helps](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md#L8) | 8 |
| [Use a read-only browser task](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md#L22) | 22 |
| [Capture a stable itinerary signature](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md#L43) | 43 |
| [Produce a short candidate set](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md#L66) | 66 |
| [Failure and fallback](../../../opt/hatch/skills/travel-planning/references/flight-itinerary-discovery.md#L82) | 82 |

### references/operational-itinerary.md

| 源章节 | 起始行 |
|---|---|
| [Operational itinerary](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L1) | 1 |
| [Keep one canonical plan](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L8) | 8 |
| [Maintain the responsibility checklist](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L38) | 38 |
| [Revise without drift](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L94) | 94 |
| [Build a usable day](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L122) | 122 |
| [Ground consequential facts](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L166) | 166 |
| [Calculate trip economics transparently](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L203) | 203 |
| [Produce one useful artifact after planning](../../../opt/hatch/skills/travel-planning/references/operational-itinerary.md#L224) | 224 |

### references/planning-kickoff.md

| 源章节 | 起始行 |
|---|---|
| [Complex planning kickoff](../../../opt/hatch/skills/travel-planning/references/planning-kickoff.md#L1) | 1 |
| [Use the right conversation](../../../opt/hatch/skills/travel-planning/references/planning-kickoff.md#L7) | 7 |
| [Learn before asking](../../../opt/hatch/skills/travel-planning/references/planning-kickoff.md#L43) | 43 |
| [Make place recommendations visual](../../../opt/hatch/skills/travel-planning/references/planning-kickoff.md#L91) | 91 |

### references/travel-fact-verification.md

| 源章节 | 起始行 |
|---|---|
| [Travel-fact verification](../../../opt/hatch/skills/travel-planning/references/travel-fact-verification.md#L1) | 1 |
| [Normalize every leg independently](../../../opt/hatch/skills/travel-planning/references/travel-fact-verification.md#L6) | 6 |
| [Limit eligibility inputs](../../../opt/hatch/skills/travel-planning/references/travel-fact-verification.md#L33) | 33 |
| [Match sources to claims](../../../opt/hatch/skills/travel-planning/references/travel-fact-verification.md#L43) | 43 |
| [Separate advice from purchase](../../../opt/hatch/skills/travel-planning/references/travel-fact-verification.md#L68) | 68 |
