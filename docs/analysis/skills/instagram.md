# instagram：账户绑定的内容读取、理解与发布

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

账户绑定的内容读取、理解与发布。入口：[SKILL.md](../../../opt/hatch/skills/instagram/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `instagram` |
| frontmatter name | `instagram` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Answer questions about Instagram posts and reels, including links the user shares, using post context, media descriptions, and visual inspection when needed. Read profiles, followers, posts, comments, likes, stories, feed, saved content, and insights. Manage feed interests and profile details, and publish stories, reels, posts, or carousels when requested.

<a id="flow"></a>
## 执行流程与输入输出

accounts 取得本人 user_fbid；非消息读取走 profile/posts/feed 等；用户给具体 post/reel 时读 content-questions，先上下文与媒体描述再视需要目视检查；写入仅在明确请求下进行，媒体先放 workspace，Story 用 draft 预览再发布。

<a id="design"></a>
## 实现思路、异常与限制

内容与私信拆成独立技能和授权。post 结果统一为紧凑集合，缺失字段按需 hydrate；账号 ID 与目标用户 ID 分开。公开发现交 social.search，私有账户操作由 CLI 承担。

following/favorites feed 与 ranked home 的支持不同，不能猜省略 variant；部分响应 provider_error 不能称完整。发布视频需要匹配 cover，carousel 顺序必须保留。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/instagram/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/instagram/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |
| [references/content-questions.md](../../../opt/hatch/skills/instagram/references/content-questions.md) | 先读帖子语境和描述，未解决的视觉细节才取图观察，再交相关任务技能完成目标；事实、猜测和未检查部分需要明确区分。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### instagram/manifest.yaml

来源：[opt/hatch/skills/instagram/manifest.yaml](../../../opt/hatch/skills/instagram/manifest.yaml)；connector：`instagram`。

请求配额声明：`mode` = `shadow`；`workers` = `['instagram-cli', 'instagram-messages-cli']`；`queries_per_minute` = `600`；`burst` = `100`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `content.read` | `allow` | 否 | — | Access content |
| `read` | `interactions.read` | `allow` | 否 | — | Access followers, comments, likes, and insights |
| `read` | `analytics.read` | `allow` | 否 | — | Access analytics |
| `read` | `algorithm.read` | `allow` | 否 | — | Access your algorithm |
| `write` | `profile.edit` | `ask` | 否 | — | Edit your profile |
| `write` | `algorithm.update` | `allow` | 是 | — | Edit your algorithm |
| `write` | `content.post` | `ask` | 否 | — | Post content |
| `write` | `saved.write` | `allow` | 是 | — | Manage saved posts |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时让 preview 与 publish 绑定同一媒体顺序、正文和账号；媒体理解结论标明来自文字描述还是实际图像。

最小验收建议：多账户选择、缺 URL 的 feed 条目、Story draft 未发布、混合 carousel 顺序都应有独立验收。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Instagram CLI](../../../opt/hatch/skills/instagram/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/instagram/SKILL.md#L10) | 10 |
| [Questions about a post or reel](../../../opt/hatch/skills/instagram/SKILL.md#L15) | 15 |
| [Account Linking](../../../opt/hatch/skills/instagram/SKILL.md#L19) | 19 |
| [Operating rules](../../../opt/hatch/skills/instagram/SKILL.md#L33) | 33 |
| [Tooling](../../../opt/hatch/skills/instagram/SKILL.md#L45) | 45 |
| [Post output](../../../opt/hatch/skills/instagram/SKILL.md#L93) | 93 |
| [Global options](../../../opt/hatch/skills/instagram/SKILL.md#L127) | 127 |
| [Commands](../../../opt/hatch/skills/instagram/SKILL.md#L132) | 132 |
| [Accounts](../../../opt/hatch/skills/instagram/SKILL.md#L134) | 134 |
| [Profile](../../../opt/hatch/skills/instagram/SKILL.md#L141) | 141 |
| [Update bio](../../../opt/hatch/skills/instagram/SKILL.md#L150) | 150 |
| [Current interests](../../../opt/hatch/skills/instagram/SKILL.md#L158) | 158 |
| [Update interests](../../../opt/hatch/skills/instagram/SKILL.md#L164) | 164 |
| [Posts](../../../opt/hatch/skills/instagram/SKILL.md#L172) | 172 |
| [Followers](../../../opt/hatch/skills/instagram/SKILL.md#L187) | 187 |
| [Following](../../../opt/hatch/skills/instagram/SKILL.md#L197) | 197 |
| [Close friends](../../../opt/hatch/skills/instagram/SKILL.md#L207) | 207 |
| [Feed](../../../opt/hatch/skills/instagram/SKILL.md#L216) | 216 |
| [Activity notifications](../../../opt/hatch/skills/instagram/SKILL.md#L235) | 235 |
| [Other user's profile](../../../opt/hatch/skills/instagram/SKILL.md#L243) | 243 |
| [Tagged posts](../../../opt/hatch/skills/instagram/SKILL.md#L252) | 252 |
| [Post by ID or URL](../../../opt/hatch/skills/instagram/SKILL.md#L263) | 263 |
| [Post comments](../../../opt/hatch/skills/instagram/SKILL.md#L274) | 274 |
| [Post likers](../../../opt/hatch/skills/instagram/SKILL.md#L284) | 284 |
| [Saved posts](../../../opt/hatch/skills/instagram/SKILL.md#L294) | 294 |
| [Saved collections](../../../opt/hatch/skills/instagram/SKILL.md#L305) | 305 |
| [Manage saved posts and collections](../../../opt/hatch/skills/instagram/SKILL.md#L313) | 313 |
| [Own stories](../../../opt/hatch/skills/instagram/SKILL.md#L328) | 328 |
| [Stories archive](../../../opt/hatch/skills/instagram/SKILL.md#L335) | 335 |
| [Stories tray](../../../opt/hatch/skills/instagram/SKILL.md#L343) | 343 |
| [Story media](../../../opt/hatch/skills/instagram/SKILL.md#L353) | 353 |
| [Location search](../../../opt/hatch/skills/instagram/SKILL.md#L361) | 361 |
| [Publish story](../../../opt/hatch/skills/instagram/SKILL.md#L375) | 375 |
| [Publish feed post](../../../opt/hatch/skills/instagram/SKILL.md#L416) | 416 |
| [Set profile picture](../../../opt/hatch/skills/instagram/SKILL.md#L467) | 467 |
| [Media understanding](../../../opt/hatch/skills/instagram/SKILL.md#L476) | 476 |
| [Recently liked posts](../../../opt/hatch/skills/instagram/SKILL.md#L484) | 484 |
| [Recently commented posts](../../../opt/hatch/skills/instagram/SKILL.md#L494) | 494 |
| [Analytics workflows](../../../opt/hatch/skills/instagram/SKILL.md#L504) | 504 |
| [Output](../../../opt/hatch/skills/instagram/SKILL.md#L515) | 515 |

### references/content-questions.md

| 源章节 | 起始行 |
|---|---|
| [Instagram content questions](../../../opt/hatch/skills/instagram/references/content-questions.md#L1) | 1 |
| [Read the available evidence](../../../opt/hatch/skills/instagram/references/content-questions.md#L5) | 5 |
| [Inspect unresolved visual details](../../../opt/hatch/skills/instagram/references/content-questions.md#L23) | 23 |
| [Finish the user's task](../../../opt/hatch/skills/instagram/references/content-questions.md#L31) | 31 |
