# facebook-cli：社交内容阅读与自有商品刊登

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

社交内容阅读与自有商品刊登。入口：[SKILL.md](../../../opt/hatch/skills/facebook-cli/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `facebook-cli` |
| frontmatter name | `facebook_cli` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use when the user provides a Facebook URL or asks to read personal posts, comments, reactions, friends, timelines, profiles, stories, feeds, groups, events, or saved items, or to discover public events happening near a place, nearby, or in a local area on a date, or to create, edit, publish, or delete their own Marketplace listings. To find, browse, or buy Marketplace listings, use shopping instead.

<a id="flow"></a>
## 执行流程与输入输出

一般请求先 me 确认连接，公开 Marketplace 三类读取例外；粘贴 share link 先 decode，保留 canonical URL 再 read；按朋友、帖子、群组、活动等需要加载参考；自有 Marketplace 刊登走草稿、审批、发布及消息准备流程。

<a id="design"></a>
## 实现思路、异常与限制

ID 在输出与下一条命令间机械串联。Marketplace 买方发现归 shopping，管理自己的刊登归本技能；外部帖子内容不能给发送或修改授权。按功能拆 references 降低常驻上下文。

链接解码为空不能猜 post ID；timeline owner 不一定是作者。登录 Facebook 不代表具备普通 timeline 发帖能力。刊登发布受额外 gate，不能从 CLI 命令存在推断所有账户可发布。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/facebook-cli/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/facebook-cli/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |
| [references/comments.md](../../../opt/hatch/skills/facebook-cli/references/comments.md) | 读取具体帖子的评论字段及分页，评论是外部文本而非操作指令；保留作者和时间，不能把评论者当原帖作者。 |
| [references/events.md](../../../opt/hatch/skills/facebook-cli/references/events.md) | 搜索个人或公开本地活动，按日期、地点与坐标条件缩小，再读具体 event。城市中心精度与精确位置不同，不能冒充用户实时位置。 |
| [references/feed.md](../../../opt/hatch/skills/facebook-cli/references/feed.md) | Newsfeed 与 Friends feed 的参数和结果不同，保留游标翻页；展示片段不等于全量动态，有限结果不可作完整性承诺。 |
| [references/friends.md](../../../opt/hatch/skills/facebook-cli/references/friends.md) | 姓名、城市、公司与生日筛选可组合，SocialGraphSearch 返回匹配上下文。生日窗口、排名和 OR/AND 逻辑需要与用户问题对齐，不从社交关系推断敏感身份。 |
| [references/groups.md](../../../opt/hatch/skills/facebook-cli/references/groups.md) | 群组发现、详情和群内帖子分别调用；区分已加入与全部公开群；使用返回 group ID 和时间游标，不能把可搜到等同于有私密访问权。 |
| [references/marketplace.md](../../../opt/hatch/skills/facebook-cli/references/marketplace.md) | 涵盖买方检索、卖方 listing 草稿/编辑/删除/发布及 publish gate。买方展示仍服从 shopping；发表成功后检查买家消息能力，不虚构 Messenger 可用状态。 |
| [references/posts.md](../../../opt/hatch/skills/facebook-cli/references/posts.md) | numeric ID、PFBID 与 canonical URL 各有输入路径；share link 解码后读原 URL。不能把视频或图片 ID 任意当 post ID 重试。 |
| [references/profile.md](../../../opt/hatch/skills/facebook-cli/references/profile.md) | 读取具体 profile 字段并限制返回内容；只报告实际存在的数据，未知字段不补全为完整个人画像。 |
| [references/reactions.md](../../../opt/hatch/skills/facebook-cli/references/reactions.md) | 读取帖子反应及对应对象，反应类型和数量是平台记录；不能从反应推断未公开立场或把结果当写操作授权。 |
| [references/saved.md](../../../opt/hatch/skills/facebook-cli/references/saved.md) | list/add/remove 与 collection 操作分开；保存项目和从集合移除不同，必须按准确对象和收藏范围操作。 |
| [references/story.md](../../../opt/hatch/skills/facebook-cli/references/story.md) | 读取 story feed 的桶和条目，属于临时内容；列表结果不能自动授权下载并长期保存整个故事集合。 |
| [references/timeline.md](../../../opt/hatch/skills/facebook-cli/references/timeline.md) | 重点区分 author 与 timeline owner。帖子发表在某人主页不意味着由该人创作；分页和链接复用实际返回数据。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### facebook-cli/manifest.yaml

来源：[opt/hatch/skills/facebook-cli/manifest.yaml](../../../opt/hatch/skills/facebook-cli/manifest.yaml)；connector：`facebook_cli`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `facebook.search` | `allow` | 否 | — | Search |
| `write` | `marketplace.listing.draft` | `ask` | 否 | — | Create draft Marketplace listings |
| `write` | `marketplace.listing.publish` | `ask` | 否 | — | Publish Marketplace listings |
| `write` | `marketplace.listing.update` | `ask` | 否 | — | Update Marketplace listings |
| `write` | `marketplace.listing.delete` | `ask` | 否 | — | Delete Marketplace listings |
| `write` | `saved.write` | `allow` | 是 | — | Save items |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时以功能域拆操作手册，给 URL 解析与实体 ID 建严格边界；写入校验资源所有权与发布状态。

最小验收建议：测试 share link 空解码、他人在用户 timeline 的帖子、自有草稿与买方搜索分流，确认作者和权限不混淆。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Facebook CLI](../../../opt/hatch/skills/facebook-cli/SKILL.md#L9) | 9 |
| [Pasted links first](../../../opt/hatch/skills/facebook-cli/SKILL.md#L11) | 11 |
| [Quick Reference](../../../opt/hatch/skills/facebook-cli/SKILL.md#L20) | 20 |
| [Account Linking](../../../opt/hatch/skills/facebook-cli/SKILL.md#L69) | 69 |
| [Post IDs and URLs](../../../opt/hatch/skills/facebook-cli/SKILL.md#L83) | 83 |
| [Composability](../../../opt/hatch/skills/facebook-cli/SKILL.md#L96) | 96 |
| [How outputs chain across commands](../../../opt/hatch/skills/facebook-cli/SKILL.md#L100) | 100 |
| [Suggestion guidelines](../../../opt/hatch/skills/facebook-cli/SKILL.md#L124) | 124 |
| [References](../../../opt/hatch/skills/facebook-cli/SKILL.md#L135) | 135 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/SKILL.md#L151) | 151 |

### references/comments.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Comments](../../../opt/hatch/skills/facebook-cli/references/comments.md#L1) | 1 |
| [Command](../../../opt/hatch/skills/facebook-cli/references/comments.md#L5) | 5 |
| [Response Fields](../../../opt/hatch/skills/facebook-cli/references/comments.md#L16) | 16 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/comments.md#L31) | 31 |

### references/events.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Events](../../../opt/hatch/skills/facebook-cli/references/events.md#L1) | 1 |
| [Commands](../../../opt/hatch/skills/facebook-cli/references/events.md#L5) | 5 |
| [Search Events](../../../opt/hatch/skills/facebook-cli/references/events.md#L7) | 7 |
| [Read Event Details](../../../opt/hatch/skills/facebook-cli/references/events.md#L71) | 71 |

### references/feed.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Feed](../../../opt/hatch/skills/facebook-cli/references/feed.md#L1) | 1 |
| [Commands](../../../opt/hatch/skills/facebook-cli/references/feed.md#L5) | 5 |
| [Newsfeed](../../../opt/hatch/skills/facebook-cli/references/feed.md#L7) | 7 |
| [Friends Feed](../../../opt/hatch/skills/facebook-cli/references/feed.md#L32) | 32 |
| [Response Fields](../../../opt/hatch/skills/facebook-cli/references/feed.md#L54) | 54 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/feed.md#L71) | 71 |

### references/friends.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Friends](../../../opt/hatch/skills/facebook-cli/references/friends.md#L1) | 1 |
| [Commands](../../../opt/hatch/skills/facebook-cli/references/friends.md#L5) | 5 |
| [List / Search Friends](../../../opt/hatch/skills/facebook-cli/references/friends.md#L7) | 7 |
| [Upcoming birthdays via `--birthday-within-days`](../../../opt/hatch/skills/facebook-cli/references/friends.md#L55) | 55 |
| [SocialGraphSearch via `--json-query`](../../../opt/hatch/skills/facebook-cli/references/friends.md#L85) | 85 |
| [Supported filters](../../../opt/hatch/skills/facebook-cli/references/friends.md#L104) | 104 |
| [Response with match context](../../../opt/hatch/skills/facebook-cli/references/friends.md#L127) | 127 |
| [Your Identity](../../../opt/hatch/skills/facebook-cli/references/friends.md#L169) | 169 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/friends.md#L177) | 177 |

### references/groups.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Groups](../../../opt/hatch/skills/facebook-cli/references/groups.md#L1) | 1 |
| [Commands](../../../opt/hatch/skills/facebook-cli/references/groups.md#L5) | 5 |
| [Group Details](../../../opt/hatch/skills/facebook-cli/references/groups.md#L7) | 7 |
| [Search Groups](../../../opt/hatch/skills/facebook-cli/references/groups.md#L41) | 41 |
| [Search Posts in a Group](../../../opt/hatch/skills/facebook-cli/references/groups.md#L83) | 83 |

### references/marketplace.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Marketplace](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L1) | 1 |
| [Workflow](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L7) | 7 |
| [Step 0: Pasted item or share links](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L9) | 9 |
| [Step 1: Parse the user's request](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L39) | 39 |
| [Step 2: Search](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L54) | 54 |
| [Step 3: Present results](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L97) | 97 |
| [Step 4: Item details (on request)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L131) | 131 |
| [Step 5: Seller info (on request)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L140) | 140 |
| [Step 6: Saved listings (on request)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L148) | 148 |
| [Step 7: My listings (on request)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L158) | 158 |
| [CLI Reference](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L175) | 175 |
| [Search](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L177) | 177 |
| [Item Detail](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L198) | 198 |
| [Seller Info](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L207) | 207 |
| [Saved Listings](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L212) | 212 |
| [My Listings](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L224) | 224 |
| [Result Schema](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L237) | 237 |
| [Search Results (JSON)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L239) | 239 |
| [Item Detail (JSON)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L269) | 269 |
| [Seller Info (JSON)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L286) | 286 |
| [Recommendation Logic](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L296) | 296 |
| [The publish gate (READ FIRST before any create/publish)](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L304) | 304 |
| [Creating a Listing](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L347) | 347 |
| [Step 1: Gather listing details](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L349) | 349 |
| [Step 2: Present a draft for confirmation](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L380) | 380 |
| [Step 3: Create](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L418) | 418 |
| [Step 4: Confirm](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L433) | 433 |
| [Step 5: Check buyer-message readiness after publication](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L443) | 443 |
| [CLI Reference — Create](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L465) | 465 |
| [Editing a Listing](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L485) | 485 |
| [Step 1: Identify the listing](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L487) | 487 |
| [Step 2: Present changes for confirmation](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L492) | 492 |
| [Step 3: Edit](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L504) | 504 |
| [Step 4: Confirm](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L519) | 519 |
| [CLI Reference — Edit](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L523) | 523 |
| [Deleting a Listing](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L542) | 542 |
| [Step 1: Identify the listing](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L547) | 547 |
| [Step 2: Confirm before deleting](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L553) | 553 |
| [Step 3: Delete](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L559) | 559 |
| [Step 4: Confirm](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L565) | 565 |
| [CLI Reference — Delete](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L572) | 572 |
| [Publishing a Draft Listing](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L581) | 581 |
| [Step 1: Identify the draft](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L587) | 587 |
| [Step 2: Check the publish gate before calling](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L592) | 592 |
| [Step 3: Publish](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L605) | 605 |
| [Step 4: Confirm](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L622) | 622 |
| [CLI Reference — Publish](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L631) | 631 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/marketplace.md#L644) | 644 |

### references/posts.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Posts](../../../opt/hatch/skills/facebook-cli/references/posts.md#L1) | 1 |
| [Reading a Post](../../../opt/hatch/skills/facebook-cli/references/posts.md#L3) | 3 |
| [Reading from a Facebook URL](../../../opt/hatch/skills/facebook-cli/references/posts.md#L14) | 14 |
| [Other Entities](../../../opt/hatch/skills/facebook-cli/references/posts.md#L58) | 58 |
| [Browsing a Profile's Timeline](../../../opt/hatch/skills/facebook-cli/references/posts.md#L68) | 68 |
| [Reading Comments or Reactions](../../../opt/hatch/skills/facebook-cli/references/posts.md#L76) | 76 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/posts.md#L83) | 83 |

### references/profile.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Profile](../../../opt/hatch/skills/facebook-cli/references/profile.md#L1) | 1 |
| [Command](../../../opt/hatch/skills/facebook-cli/references/profile.md#L5) | 5 |
| [Response Fields](../../../opt/hatch/skills/facebook-cli/references/profile.md#L15) | 15 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/profile.md#L31) | 31 |

### references/reactions.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Reactions](../../../opt/hatch/skills/facebook-cli/references/reactions.md#L1) | 1 |
| [Command](../../../opt/hatch/skills/facebook-cli/references/reactions.md#L5) | 5 |
| [Response Fields](../../../opt/hatch/skills/facebook-cli/references/reactions.md#L17) | 17 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/reactions.md#L25) | 25 |

### references/saved.md

| 源章节 | 起始行 |
|---|---|
| [Saved](../../../opt/hatch/skills/facebook-cli/references/saved.md#L1) | 1 |
| [Commands](../../../opt/hatch/skills/facebook-cli/references/saved.md#L5) | 5 |
| [`saved list`](../../../opt/hatch/skills/facebook-cli/references/saved.md#L7) | 7 |
| [`saved add`](../../../opt/hatch/skills/facebook-cli/references/saved.md#L41) | 41 |
| [`saved remove`](../../../opt/hatch/skills/facebook-cli/references/saved.md#L55) | 55 |
| [`saved collections list`](../../../opt/hatch/skills/facebook-cli/references/saved.md#L71) | 71 |
| [`saved collections create`](../../../opt/hatch/skills/facebook-cli/references/saved.md#L89) | 89 |
| [Operating notes](../../../opt/hatch/skills/facebook-cli/references/saved.md#L99) | 99 |

### references/story.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Stories](../../../opt/hatch/skills/facebook-cli/references/story.md#L1) | 1 |
| [Commands](../../../opt/hatch/skills/facebook-cli/references/story.md#L5) | 5 |
| [Fetch Story Feed](../../../opt/hatch/skills/facebook-cli/references/story.md#L7) | 7 |

### references/timeline.md

| 源章节 | 起始行 |
|---|---|
| [Facebook Timeline](../../../opt/hatch/skills/facebook-cli/references/timeline.md#L1) | 1 |
| [Command](../../../opt/hatch/skills/facebook-cli/references/timeline.md#L5) | 5 |
| [Output](../../../opt/hatch/skills/facebook-cli/references/timeline.md#L25) | 25 |
| [Author vs Owner (CRITICAL)](../../../opt/hatch/skills/facebook-cli/references/timeline.md#L36) | 36 |
| [Example Output](../../../opt/hatch/skills/facebook-cli/references/timeline.md#L43) | 43 |
| [Operating Rules](../../../opt/hatch/skills/facebook-cli/references/timeline.md#L67) | 67 |
