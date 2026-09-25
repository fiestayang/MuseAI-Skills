# magic-moment：有事实约束的竖屏故事视频流水线

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

有事实约束的竖屏故事视频流水线。入口：[SKILL.md](../../../opt/hatch/skills/magic-moment/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `magic-moment` |
| frontmatter name | `magic-moment` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Make a "magic moment" video — turn a creator's talking-head recording into a vertical video preserving the source narration where their Muse story replays through artifacts and brief exchanges synced to their voiceover — bubbles, typing, emoji reactions, real widgets and pages, message sounds, closing Muse lockup finisher. Use whenever a user with talking-head or selfie footage wants it turned into a shareable clip of their Muse story — "make a magic moment", "turn this video of me into...", "add the chat over my video", "retell what Muse did for me" — even if they never say the words "magic moment".

<a id="flow"></a>
## 执行流程与输入输出

按顺序执行 story_and_canon、conversation_shape、visuals、screenplay/timeline 和 screenplay_review；保留源视频与 ASR，修正另列来源；实际产物提供证明画面；validate 生成规范化 screenplay 和 fingerprint；逐 beat 审核后绑定 review 再渲染。

<a id="design"></a>
## 实现思路、异常与限制

设计资源只决定样式，真实对话和产物决定事实。用户气泡、审批、结果不能因为“故事好看”而虚构。审阅绑定精确构建指纹，避免改稿后沿用旧批准。

mm、cmm 实现与安装所指 bundle 不在快照；HTML kit 是可读设计资产而非完整 renderer。修正文稿没有自动词级时间戳，不能沿用旧 ASR 对齐而不核对。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [INSTALL.md](../../../opt/hatch/skills/magic-moment/INSTALL.md) | 描述在 Muse VM 安装 bundle 并验证 mm 的流程，依赖外部程序与目录。本报告不执行安装；现有资源不足以证明可直接渲染。 |
| [SKILL.md](../../../opt/hatch/skills/magic-moment/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [guide/conversation_shape.md](../../../opt/hatch/skills/magic-moment/guide/conversation_shape.md) | 只展示真实请求和决策，精确引用与忠实转述分开；持续帮助不需要虚构每轮新授权，以产物呈现替代无意义对话气泡。 |
| [guide/screenplay.md](../../../opt/hatch/skills/magic-moment/guide/screenplay.md) | 把事实组织为双边互动和视觉 beat；数据结构由缺失的 cmm/script.py 定义，不能从示例推断完整解析器行为。 |
| [guide/screenplay_review.md](../../../opt/hatch/skills/magic-moment/guide/screenplay_review.md) | validate 后审阅 resolved_screenplay，逐内容 beat 检查出处、说话人、时态和画面，review 绑定 fingerprint；任何改稿应使旧审阅失效。 |
| [guide/story_and_canon.md](../../../opt/hatch/skills/magic-moment/guide/story_and_canon.md) | 保留源旁白、ASR 与用户修正来源，建立事实表；未获授权不删减叙述，不把其他作品或样例作为本片事实。 |
| [guide/timeline.md](../../../opt/hatch/skills/magic-moment/guide/timeline.md) | 保持转录源摘要、时长和词时间；不同视频使用新 run，修正文本单独记录；所有 beat 对齐旁白，尾部 finisher 属于确定的结束阶段。 |
| [guide/visuals.md](../../../opt/hatch/skills/magic-moment/guide/visuals.md) | 从事实和真实产物选择组件，先预览再进入时间线；使用实际截图，不以 kit 样例伪装已完成工作。 |
| [reference/card-spec.md](../../../opt/hatch/skills/magic-moment/reference/card-spec.md) | 区分作者可用卡片和 renderer 内部机制，优先真实产物全块裁切；不得把维护说明当模型应自行实现的渲染步骤。 |
| [reference/design-system/muse-moments-kit.html](../../../opt/hatch/skills/magic-moment/reference/design-system/muse-moments-kit.html) | 1320 行静态 HTML/CSS 组件展示，含 artifact、媒体、浏览器、信任、通信、自动化等分区；没有 script 或外部 src/href。可作为 markup/CSS 样板，样例数据不是业务实现。CSS 的 @font-face 仍引用缺失的本地字体，不能误解为无资源依赖。 |
| [reference/design-system/story-compositions.html](../../../opt/hatch/skills/magic-moment/reference/design-system/story-compositions.html) | 43 行静态构图参考，演示无日期周期、抽象路线与连接机制；无 JavaScript；CSS 同样引用本地字体。特别避免给抽象路径赋予真实地理和给连接图编造成功状态。 |
| [reference/design.md](../../../opt/hatch/skills/magic-moment/reference/design.md) | 以 Muse Moments Kit 为视觉源，约束字体、缩放、卡片、留白、运动和结束画面；组件外观可迁移，产品品牌与真实内容必须替换。 |
| [reference/overlay-spec.md](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md) | 规定固定画布、气泡堆叠和 avatar/browser session 的渲染契约；动态物理和素材管理实现未附带，文档只提供规格。 |
| [reference/visual-storytelling.md](../../../opt/hatch/skills/magic-moment/reference/visual-storytelling.md) | 让图像承担证据与故事推进功能，避免整片仅重复字幕；选择具体产物而非抽象装饰，并保持事实时间顺序。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

## 两份 HTML 的实现解读

### muse-moments-kit.html

这是一份自包含的 markup/CSS 展示页，配合缺失的本地字体资源。全局 @font-face、背景、排版和局部 inline style 组成样式；各 section 用 flex 排列组件。图形主要由内联 SVG、纯色块和 CSS 画成，没有 JavaScript 业务层、事件处理器、网络查询或真实付款。

| 源码区域 | 组件与实现 | 使用边界 |
|---|---|---|
| Foundations，19 行 | 色板、字体层级、圆角与视觉规则 | 这是作者设计约束；占位块必须换成真实内容 |
| Thread chrome，57 行 | 左右气泡与 CSS dotpulse | 标明 renderer 绘制，仅作外观参考 |
| Artifacts & documents，75 行 | 应用图标卡、完整应用表面、文件/PPT 卡、上传 chip、外链卡 | 要根据真实应用或文档重建，不可把样板标题当用户成品 |
| Media，253 行 | 生成媒体、选图与 quote-reply 选择动画 | mobile 选择外观与 web 不同；动画不代表真实用户选择 |
| Browser & shopping，338 行 | 浏览器 journey、工具状态 chip、商品卡、review 浮层 | 真浏览器工作才显示 browser；connector 调用用 tool chip，不能伪造浏览器过程 |
| Trust & security，477 行 | 连接披露、凭据保存、审批卡等 | CSS 可以演出 Connected/Approved，但没有真实 OAuth 或授权状态 |
| Communication，627 行 | 消息 thread、Gmail compose、发送提示、音频气泡 | send/checkmark 是演示动画，不能作为消息送达证据 |
| Automation & ambient，755 行 | Bot Status、带按钮文本、选项、Letter、Ideas 与 Feed | 用真实任务/内容替换样例；卡片外观不是调度实现 |
| Personal intelligence，935 行 | 目标及个人信息相关展示、勾选和 confetti | 仅呈现已证实状态；不能从画面生成新的用户事实 |
| Work & analysis，1104 行 | 工作和分析成果的排版组件 | 数值、文件和进度必须回到真实任务来源 |
| Meta-capabilities，1183 行 | 钱包、付款审批、章节标题等 | 金额和 Approved 文案必须对应真实批准，模板没有支付能力 |

源定位：[完整 HTML](../../../opt/hatch/skills/magic-moment/reference/design-system/muse-moments-kit.html)。CSS keyframes 用延时、opacity、transform、颜色和 SVG stroke 等模拟一次动作并保持结尾，另有 loading 点等循环效果。定时动画说明如何拍演示画面，不构成状态机或用户点击反馈。

`data-ph` 标记截图、图片等占位资源。文件里的条纹块故意提示替换需求；视频 validator 是否拒绝残留占位属于外部工具契约。当前快照不能运行该完整 gate。移植时可取需要的单个组件并换品牌及真实数据，不必把 1,320 行样例整体加入产品。

### story-compositions.html

[43 行源文件](../../../opt/hatch/skills/magic-moment/reference/design-system/story-compositions.html) 提供三类构图：无日期的重复节奏、明确不作地理承诺的抽象路线、连接关系。页面卡片按 1240px 画布和局部样式组织，适合截取单块；slotReveal 等 CSS keyframes 负责逐步出现，SVG path 承担抽象路径表现。

标签和数值必须来自当前任务。没有日期就不画日历日期；抽象线不是地图或已验证交通路线；连接画面也不等于外部账号已授权。该文件无运行时数据源、真实调度器或连接器，只提供构图与动画规则。

<a id="migration"></a>
## 迁移开发指引

迁移时保留源摘要、事实清单、逐 beat 出处、时间锚点和构建指纹；先做一个可验证单片流水线，再扩展模板。

最小验收建议：稿件审阅后变更一句审批气泡，fingerprint 应失配；画面只能使用真实存在产物，不能把 kit 样例当用户成果。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### INSTALL.md

| 源章节 | 起始行 |
|---|---|
| [Installing magic-moment on a Muse VM](../../../opt/hatch/skills/magic-moment/INSTALL.md#L1) | 1 |
| [Verify](../../../opt/hatch/skills/magic-moment/INSTALL.md#L16) | 16 |
| [Updating](../../../opt/hatch/skills/magic-moment/INSTALL.md#L42) | 42 |

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Magic Moment](../../../opt/hatch/skills/magic-moment/SKILL.md#L7) | 7 |
| [Component index](../../../opt/hatch/skills/magic-moment/SKILL.md#L31) | 31 |

### guide/conversation_shape.md

| 源章节 | 起始行 |
|---|---|
| [Conversation and pacing](../../../opt/hatch/skills/magic-moment/guide/conversation_shape.md#L1) | 1 |

### guide/screenplay.md

| 源章节 | 起始行 |
|---|---|
| [Screenplay: Dramatize the Interaction, Don't Caption the Narration](../../../opt/hatch/skills/magic-moment/guide/screenplay.md#L1) | 1 |

### guide/screenplay_review.md

| 源章节 | 起始行 |
|---|---|
| [Review the exact build](../../../opt/hatch/skills/magic-moment/guide/screenplay_review.md#L1) | 1 |

### guide/story_and_canon.md

| 源章节 | 起始行 |
|---|---|
| [Preserve the source story](../../../opt/hatch/skills/magic-moment/guide/story_and_canon.md#L1) | 1 |

### guide/timeline.md

| 源章节 | 起始行 |
|---|---|
| [Source and timing](../../../opt/hatch/skills/magic-moment/guide/timeline.md#L1) | 1 |

### guide/visuals.md

| 源章节 | 起始行 |
|---|---|
| [Choose visuals from the evidence](../../../opt/hatch/skills/magic-moment/guide/visuals.md#L1) | 1 |

### reference/card-spec.md

| 源章节 | 起始行 |
|---|---|
| [Card Spec — proof artifact cards + the web-artifact process](../../../opt/hatch/skills/magic-moment/reference/card-spec.md#L1) | 1 |
| [Internals (maintainer reference — NOT an agent recipe)](../../../opt/hatch/skills/magic-moment/reference/card-spec.md#L7) | 7 |
| [What is locked, and why](../../../opt/hatch/skills/magic-moment/reference/card-spec.md#L18) | 18 |
| [Web-artifact process — specificity by full-block crop](../../../opt/hatch/skills/magic-moment/reference/card-spec.md#L43) | 43 |
| [Card shapes to reach for](../../../opt/hatch/skills/magic-moment/reference/card-spec.md#L85) | 85 |
| [Verification](../../../opt/hatch/skills/magic-moment/reference/card-spec.md#L99) | 99 |

### reference/design.md

| 源章节 | 起始行 |
|---|---|
| [Design Spec — the Muse Moments Kit is the design system](../../../opt/hatch/skills/magic-moment/reference/design.md#L1) | 1 |
| [The look is the Muse product's own](../../../opt/hatch/skills/magic-moment/reference/design.md#L13) | 13 |
| [Fonts: one face, three narrow exceptions](../../../opt/hatch/skills/magic-moment/reference/design.md#L44) | 44 |
| [Artifact cards are portraits, not templates](../../../opt/hatch/skills/magic-moment/reference/design.md#L73) | 73 |
| [Product-parity components copy the product exactly](../../../opt/hatch/skills/magic-moment/reference/design.md#L96) | 96 |
| [Shipping widget replicas outrank composed cards](../../../opt/hatch/skills/magic-moment/reference/design.md#L131) | 131 |
| [Placeholders never ship](../../../opt/hatch/skills/magic-moment/reference/design.md#L205) | 205 |
| [Scale kit markup to the 1240px canvas](../../../opt/hatch/skills/magic-moment/reference/design.md#L225) | 225 |
| [One card per component, flat inside, nothing bare on the video](../../../opt/hatch/skills/magic-moment/reference/design.md#L235) | 235 |
| [Breathing room](../../../opt/hatch/skills/magic-moment/reference/design.md#L264) | 264 |
| [Card motion](../../../opt/hatch/skills/magic-moment/reference/design.md#L272) | 272 |
| [Browser cards rebuild the real page](../../../opt/hatch/skills/magic-moment/reference/design.md#L280) | 280 |
| [The full-screen Muse finisher](../../../opt/hatch/skills/magic-moment/reference/design.md#L403) | 403 |
| [Mechanics (machine-enforced, unchanged by the kit)](../../../opt/hatch/skills/magic-moment/reference/design.md#L407) | 407 |

### reference/overlay-spec.md

| 源章节 | 起始行 |
|---|---|
| [Overlay Spec — deterministic bubble renderer](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L1) | 1 |
| [Internals (maintainer reference — NOT an agent recipe)](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L10) | 10 |
| [Canvas scale](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L18) | 18 |
| [What is locked, and why](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L27) | 27 |
| [Thread-stack physics](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L74) | 74 |
| [The browser session](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L83) | 83 |
| [The avatar](../../../opt/hatch/skills/magic-moment/reference/overlay-spec.md#L101) | 101 |

### reference/visual-storytelling.md

| 源章节 | 起始行 |
|---|---|
| [Compose the story visually](../../../opt/hatch/skills/magic-moment/reference/visual-storytelling.md#L1) | 1 |
