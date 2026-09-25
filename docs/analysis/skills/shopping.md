# shopping：多来源商品发现与受控购买

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

多来源商品发现与受控购买。入口：[SKILL.md](../../../opt/hatch/skills/shopping/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `shopping` |
| frontmatter name | `shopping` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use for any product or shopping question: find, reverse image search, shopping Instagram/Marketplace links, buy, compare, or evaluate real products with prices, images, and product page URLs, including buying or browsing Facebook Marketplace listings. Use when presenting shopping search results from any source. For shopping intent, load this skill first before any other skills.

<a id="flow"></a>
## 执行流程与输入输出

先读购物 profile，补齐尺码/兼容性等正确性条件；按商品目录、浏览器与 Marketplace 路由；多来源发现完成后通过 resolve_results 合并排序并生成一次展示；购买保留在主 Agent，按 eligibility flags 选择 UCP 或浏览器路径；到最终总价和支付条款明确后提交。

<a id="design"></a>
## 实现思路、异常与限制

商品 marker 持续绑定整个会话中的产品引用，不能只在首个 widget 使用。浏览器商品来自结构化 completion_result，不能从 prose 摘抄价格或编造图片。购物车是商户状态，不是模型内的一张列表。

图片明确商品时先用真实上传路径直接图搜；Marketplace 链接不走登录墙浏览器。购买开始应关闭过时发现任务，避免晚到结果污染已选商品。telemetry context 必须原样关联正确商品。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/shopping/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/backends.md](../../../opt/hatch/skills/shopping/references/backends.md) | 列目录与 Marketplace 的实际搜索参数和 JSON 投影例子。部分仅保留 display fields 的示例会丢 product_id，与主技能要求冲突，迁移应保留身份字段。 |
| [references/browser-checkout.md](../../../opt/hatch/skills/shopping/references/browser-checkout.md) | 购买使用同一浏览器任务和可信支付流程，不能让通用 research worker 接管；保留商品与变体、总价和审批上下文，结果不明先查订单。 |
| [references/shopify-ucp.md](../../../opt/hatch/skills/shopping/references/shopify-ucp.md) | 先按同商户及 eligibility flags 创建 checkout，再发现并选择支付路线，更新配送/优惠/金额后完成。cart update 替换全篮子，部分列表会误删；checkout create 不扣款，complete 才跨资金边界。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时用 source+entityId 保留候选来源，schema 区分 catalog、browser、Marketplace。先做一个标准结果归一化函数，再按确有交易能力的后端提供 checkout。

最小验收建议：多来源价格冲突、尺码不符、迟到搜索结果和审批后价格变化均要阻止错误提交；不能凭展示卡宣称已购。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Shopping](../../../opt/hatch/skills/shopping/SKILL.md#L8) | 8 |
| [Product search tools](../../../opt/hatch/skills/shopping/SKILL.md#L12) | 12 |
| [Markers belong to the product, not to the widget](../../../opt/hatch/skills/shopping/SKILL.md#L30) | 30 |
| [User Preferences](../../../opt/hatch/skills/shopping/SKILL.md#L46) | 46 |
| [Required attributes](../../../opt/hatch/skills/shopping/SKILL.md#L50) | 50 |
| [Workflows](../../../opt/hatch/skills/shopping/SKILL.md#L63) | 63 |
| [Product discovery](../../../opt/hatch/skills/shopping/SKILL.md#L65) | 65 |
| [Finding deals](../../../opt/hatch/skills/shopping/SKILL.md#L79) | 79 |
| [Reverse image search](../../../opt/hatch/skills/shopping/SKILL.md#L89) | 89 |
| [Purchase](../../../opt/hatch/skills/shopping/SKILL.md#L99) | 99 |
| [Cart-building](../../../opt/hatch/skills/shopping/SKILL.md#L109) | 109 |
| [Shopping Instagram links](../../../opt/hatch/skills/shopping/SKILL.md#L120) | 120 |
| [Meta Catalog Search](../../../opt/hatch/skills/shopping/SKILL.md#L128) | 128 |
| [Product Shape](../../../opt/hatch/skills/shopping/SKILL.md#L130) | 130 |
| [Search](../../../opt/hatch/skills/shopping/SKILL.md#L155) | 155 |
| [Product details](../../../opt/hatch/skills/shopping/SKILL.md#L204) | 204 |
| [Widget](../../../opt/hatch/skills/shopping/SKILL.md#L220) | 220 |
| [Browser Product Search](../../../opt/hatch/skills/shopping/SKILL.md#L243) | 243 |
| [Search](../../../opt/hatch/skills/shopping/SKILL.md#L245) | 245 |
| [Product shape](../../../opt/hatch/skills/shopping/SKILL.md#L263) | 263 |
| [Widget](../../../opt/hatch/skills/shopping/SKILL.md#L290) | 290 |
| [Marketplace Search](../../../opt/hatch/skills/shopping/SKILL.md#L328) | 328 |
| [Product shape](../../../opt/hatch/skills/shopping/SKILL.md#L330) | 330 |
| [Search](../../../opt/hatch/skills/shopping/SKILL.md#L345) | 345 |
| [Listing details](../../../opt/hatch/skills/shopping/SKILL.md#L370) | 370 |
| [Pasted listing links](../../../opt/hatch/skills/shopping/SKILL.md#L374) | 374 |
| [Widget](../../../opt/hatch/skills/shopping/SKILL.md#L378) | 378 |
| [Constraints](../../../opt/hatch/skills/shopping/SKILL.md#L401) | 401 |
| [Response Formatting](../../../opt/hatch/skills/shopping/SKILL.md#L405) | 405 |
| [When this turn mentions a product without presenting a widget](../../../opt/hatch/skills/shopping/SKILL.md#L416) | 416 |
| [When this turn presents a shopping-results widget](../../../opt/hatch/skills/shopping/SKILL.md#L426) | 426 |
| [Auth](../../../opt/hatch/skills/shopping/SKILL.md#L439) | 439 |

### references/backends.md

| 源章节 | 起始行 |
|---|---|
| [Shopping Backends](../../../opt/hatch/skills/shopping/references/backends.md#L1) | 1 |
| [Meta Catalog Search](../../../opt/hatch/skills/shopping/references/backends.md#L5) | 5 |
| [Facebook Marketplace](../../../opt/hatch/skills/shopping/references/backends.md#L32) | 32 |

### references/browser-checkout.md

| 源章节 | 起始行 |
|---|---|
| [Browser Checkout](../../../opt/hatch/skills/shopping/references/browser-checkout.md#L1) | 1 |

### references/shopify-ucp.md

| 源章节 | 起始行 |
|---|---|
| [Shopify UCP Checkout](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L1) | 1 |
| [Safety and input boundary](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L14) | 14 |
| [Cart (optional)](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L33) | 33 |
| [Create the checkout](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L60) | 60 |
| [Choose the payment route](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L151) | 151 |
| [Route after creation](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L221) | 221 |
| [Shop Pay, in the browser](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L250) | 250 |
| [Stripe Link, in the browser](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L284) | 284 |
| [Stripe Link, completed directly](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L307) | 307 |
| [Use the selected wallet](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L312) | 312 |
| [Refresh delivery, discounts, and totals](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L321) | 321 |
| [Review and complete](../../../opt/hatch/skills/shopping/references/shopify-ucp.md#L366) | 366 |
