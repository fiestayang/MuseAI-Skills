# 产品说明、配置与历史材料

[返回目录](../README.md)

覆盖 home/hatch 下全部 31 个文件。以下是本地文档解读；涉及发布地区、UI、价格、平台限制等不作为当前线上事实认证。研究对象中的命令和角色指令不适用于本次分析会话。

## 文件目录

- [artifacts.md](#file-1)
- [browser.md](#file-2)
- [calls-texts-notifications.md](#file-3)
- [channel-availability.md](#file-4)
- [whatsapp.md](#file-5)
- [client-surfaces.md](#file-6)
- [connectors.md](#file-7)
- [data-handling.md](#file-8)
- [feed.md](#file-9)
- [files-and-library.md](#file-10)
- [goals.md](#file-11)
- [ideas.md](#file-12)
- [media.md](#file-13)
- [muse.md](#file-14)
- [payments-and-purchases.md](#file-15)
- [privacy-and-credentials.md](#file-16)
- [referrals.md](#file-17)
- [scheduling-and-watching.md](#file-18)
- [self_improvement.md](#file-19)
- [voice.md](#file-20)
- [mac_app.md](#file-21)
- [tailscale.md](#file-22)
- [home_link.md](#file-23)
- [brother_printers.md](#file-24)
- [lutron_smart_bridges.md](#file-25)
- [shelly_plugs.md](#file-26)
- [home.yaml](#file-27)
- [skills.yaml](#file-28)
- [PROACTIVE_PREFERENCES.md](#file-29)
- [memory_import.md](#file-30)
- [muse-security-audit.md](#file-31)

<a id="file-1"></a>
## home/hatch/docs/artifacts.md

来源：[home/hatch/docs/artifacts.md](../../../home/hatch/docs/artifacts.md)。

定义文件、静态页面、交互应用三种产物；生成、存储、公开发布是不同动作。只有静态 artifact 可发布，更新公开版本也需新的单次审批；删除 artifact 为永久操作，与工作区文件的回收站不同。移植时把发布版本和工作版本分开，不能把保存视为公开。

章节入口：[Artifacts](../../../home/hatch/docs/artifacts.md#L1)；[Location](../../../home/hatch/docs/artifacts.md#L21)；[Sharing & Publishing](../../../home/hatch/docs/artifacts.md#L29)；[Deletion](../../../home/hatch/docs/artifacts.md#L52)。

<a id="file-2"></a>
## home/hatch/docs/browser.md

来源：[home/hatch/docs/browser.md](../../../home/hatch/docs/browser.md)。

描述服务端浏览器的导航、提取、交互、下载和阻塞状态。connector 登录不继承到浏览器；用户设备 cookies 也不自动转移。网络、上传、下载、填凭据和提交有各自权限；CAPTCHA 和 checkout 有独立约束。浏览器不能自行锁票价或库存，下载成功后还需交付文件。

章节入口：[Browser](../../../home/hatch/docs/browser.md#L1)；[Limitations](../../../home/hatch/docs/browser.md#L8)；[Browser permissions](../../../home/hatch/docs/browser.md#L21)；[Sessions and sign-in](../../../home/hatch/docs/browser.md#L33)；[No holds, locks, or reservations](../../../home/hatch/docs/browser.md#L41)；[Downloads](../../../home/hatch/docs/browser.md#L45)；[Live browser watching](../../../home/hatch/docs/browser.md#L49)；[Purchases and refunds](../../../home/hatch/docs/browser.md#L53)。

<a id="file-3"></a>
## home/hatch/docs/calls-texts-notifications.md

来源：[home/hatch/docs/calls-texts-notifications.md](../../../home/hatch/docs/calls-texts-notifications.md)。

拆开代打商业电话、配对设备发短信、应用 push 和 proactive editions。电话开始使用 phone.begin_call，再准备本次 brief；人类/AI caller 选择按本次发现与用户回答。iPhone message.draft 不等于发送；Android 能力依设置变化。无通用原始 push 发送或送达验证接口，不能以审批已产生证明手机收到。

章节入口：[Calls, Texts, and Notifications](../../../home/hatch/docs/calls-texts-notifications.md#L1)；[Phone calls](../../../home/hatch/docs/calls-texts-notifications.md#L3)；[Texting](../../../home/hatch/docs/calls-texts-notifications.md#L53)；[Notifications](../../../home/hatch/docs/calls-texts-notifications.md#L91)；[Proactive editions](../../../home/hatch/docs/calls-texts-notifications.md#L122)；[Voice and audio](../../../home/hatch/docs/calls-texts-notifications.md#L144)；[Messaging channels](../../../home/hatch/docs/calls-texts-notifications.md#L157)。

<a id="file-4"></a>
## home/hatch/docs/channel-availability.md

来源：[home/hatch/docs/channel-availability.md](../../../home/hatch/docs/channel-availability.md)。

将文档目录、channel.status 和实时 delivery route 分开。linked 只说明已关联，不证明交付正常。每个 provider 会话对应独立 side chat，回复和定时任务按来源会话路由；主会话不能随意向渠道推送。unknown provider 表示本环境不可用，不是全产品没有该渠道。

章节入口：[Channel availability and routing](../../../home/hatch/docs/channel-availability.md#L1)；[Available channels](../../../home/hatch/docs/channel-availability.md#L4)；[Connection and disconnection](../../../home/hatch/docs/channel-availability.md#L32)；[Linked conversation behavior](../../../home/hatch/docs/channel-availability.md#L44)；[Message routing](../../../home/hatch/docs/channel-availability.md#L52)。

<a id="file-5"></a>
## home/hatch/docs/channels/whatsapp.md

来源：[home/hatch/docs/channels/whatsapp.md](../../../home/hatch/docs/channels/whatsapp.md)。

给出 WhatsApp 专用内容格式、关联会话与媒体规则。它是用户与自有 Agent 的渠道，不提供用户个人 WhatsApp 历史或向任意联系人代发。渠道指南只描述相应表面的能力，不能把 App 页面控件说成 WhatsApp 内按钮。

章节入口：[WhatsApp Channel](../../../home/hatch/docs/channels/whatsapp.md#L14)；[How it works](../../../home/hatch/docs/channels/whatsapp.md#L25)；[Supported media and attachments](../../../home/hatch/docs/channels/whatsapp.md#L40)；[Connecting](../../../home/hatch/docs/channels/whatsapp.md#L52)；[`channel.status` / `channel.disable` Tools](../../../home/hatch/docs/channels/whatsapp.md#L64)；[`status`](../../../home/hatch/docs/channels/whatsapp.md#L78)；[`disable`](../../../home/hatch/docs/channels/whatsapp.md#L100)；[Runtime behavior](../../../home/hatch/docs/channels/whatsapp.md#L105)。

<a id="file-6"></a>
## home/hatch/docs/client-surfaces.md

来源：[home/hatch/docs/client-surfaces.md](../../../home/hatch/docs/client-surfaces.md)。

逐平台描述 web、iOS、Android、Mac 的导航、设置、状态面板、文件与配对功能。入口和按钮差异是产品支持知识，不是前端组件源码。没有 Skills tab；连接器在 Settings。迁移支持 Agent 时需要按平台检索对应段落，防止把某平台功能泛化给所有设备。

章节入口：[Where users access Muse](../../../home/hatch/docs/client-surfaces.md#L1)；[Mac app](../../../home/hatch/docs/client-surfaces.md#L13)；[iOS, Android, and web](../../../home/hatch/docs/client-surfaces.md#L51)；[Tabs (variations per platform below)](../../../home/hatch/docs/client-surfaces.md#L53)；[Side chats](../../../home/hatch/docs/client-surfaces.md#L74)；[Gestures on mobile](../../../home/hatch/docs/client-surfaces.md#L83)；[Deleting a sent message](../../../home/hatch/docs/client-surfaces.md#L112)；[Chat search](../../../home/hatch/docs/client-surfaces.md#L120)；[Status screen (tap your avatar)](../../../home/hatch/docs/client-surfaces.md#L142)；[Approval requests from the user's agent](../../../home/hatch/docs/client-surfaces.md#L151)；[Settings](../../../home/hatch/docs/client-surfaces.md#L155)；[iOS app only](../../../home/hatch/docs/client-surfaces.md#L183)；[Tabs](../../../home/hatch/docs/client-surfaces.md#L185)；[Settings](../../../home/hatch/docs/client-surfaces.md#L189)；[Paired devices](../../../home/hatch/docs/client-surfaces.md#L211)；[Sharing](../../../home/hatch/docs/client-surfaces.md#L215)；[Home Screen widget](../../../home/hatch/docs/client-surfaces.md#L219)；[Android app only](../../../home/hatch/docs/client-surfaces.md#L227)；[Tabs](../../../home/hatch/docs/client-surfaces.md#L229)；[Settings](../../../home/hatch/docs/client-surfaces.md#L233)；[Paired devices](../../../home/hatch/docs/client-surfaces.md#L272)；[Sharing](../../../home/hatch/docs/client-surfaces.md#L276)；[Web app only](../../../home/hatch/docs/client-surfaces.md#L282)；[Tabs](../../../home/hatch/docs/client-surfaces.md#L284)；[Status screen](../../../home/hatch/docs/client-surfaces.md#L310)；[Settings](../../../home/hatch/docs/client-surfaces.md#L325)；[Paired devices](../../../home/hatch/docs/client-surfaces.md#L430)；[Sharing](../../../home/hatch/docs/client-surfaces.md#L434)；[What pairing a phone does not let me do](../../../home/hatch/docs/client-surfaces.md#L438)；[iOS, Android, and web rules](../../../home/hatch/docs/client-surfaces.md#L446)。

<a id="file-7"></a>
## home/hatch/docs/connectors.md

来源：[home/hatch/docs/connectors.md](../../../home/hatch/docs/connectors.md)。

解释连接器授权、读写操作与账户连接管理。已连接不等于浏览器已登录，也不等于默认批准所有动作。连接器目录和权限状态应由实际工具读取；本地 skills.yaml 不是在线登录凭据或实时可用性证明。

章节入口：[Connectors and what they do](../../../home/hatch/docs/connectors.md#L1)；[The core rule](../../../home/hatch/docs/connectors.md#L6)；[Connection state: verify this turn](../../../home/hatch/docs/connectors.md#L41)；[Region availability](../../../home/hatch/docs/connectors.md#L75)；[Action permissions](../../../home/hatch/docs/connectors.md#L89)；[Additional OAuth access](../../../home/hatch/docs/connectors.md#L106)；[The skill file is the source of truth](../../../home/hatch/docs/connectors.md#L121)；[Provider limits](../../../home/hatch/docs/connectors.md#L131)；[Invented connect flows](../../../home/hatch/docs/connectors.md#L146)；[Mail and verification codes](../../../home/hatch/docs/connectors.md#L152)。

<a id="file-8"></a>
## home/hatch/docs/data-handling.md

来源：[home/hatch/docs/data-handling.md](../../../home/hatch/docs/data-handling.md)。

处理用户数据用途、控制入口和可说明的范围；属于隐私产品说明，不是数据处理 pipeline 源码或法律合规证书。引用时保留产品声明来源，不能由本快照验证线上保留期限或实际训练排除状态。

章节入口：[How the user's information is handled](../../../home/hatch/docs/data-handling.md#L9)；[What you know, and who else can see it](../../../home/hatch/docs/data-handling.md#L15)；[What the user can control, and where](../../../home/hatch/docs/data-handling.md#L31)。

<a id="file-9"></a>
## home/hatch/docs/feed.md

来源：[home/hatch/docs/feed.md](../../../home/hatch/docs/feed.md)。

定义定时编辑的个人 Feed 及 feed prompt。新用户 Getting started 内容是随包介绍，不源自私人背景；不能把启动样例描述为已分析用户。Feed 内容偏好与 Chat 主动通知偏好是不同表面，配置变更要定位实际对象。

章节入口：[The Feed](../../../home/hatch/docs/feed.md#L1)；[The default posts a new reader starts with](../../../home/hatch/docs/feed.md#L11)；[How posts get written](../../../home/hatch/docs/feed.md#L36)；[Steering coverage](../../../home/hatch/docs/feed.md#L61)；[Generation and schedule](../../../home/hatch/docs/feed.md#L67)；[On, off, and notifications](../../../home/hatch/docs/feed.md#L77)；[Per-post actions](../../../home/hatch/docs/feed.md#L89)。

<a id="file-10"></a>
## home/hatch/docs/files-and-library.md

来源：[home/hatch/docs/files-and-library.md](../../../home/hatch/docs/files-and-library.md)。

区分 Agent 文件系统、上传 workspace/user、交付 workspace/your_files、Library 索引和应用展示注释。上传不自动成为 Library 项目；About this file 为展示层附加，不在文件字节中。普通聊天文件链接带登录约束，公开临时下载与 artifact publish 又是另一条路径。

章节入口：[Files and the Library](../../../home/hatch/docs/files-and-library.md#L1)；[Your computer and workspace](../../../home/hatch/docs/files-and-library.md#L5)；[Where uploads land](../../../home/hatch/docs/files-and-library.md#L15)；[Deliverables and the Library](../../../home/hatch/docs/files-and-library.md#L23)；[Managing Library items](../../../home/hatch/docs/files-and-library.md#L30)；[Downloading and sharing](../../../home/hatch/docs/files-and-library.md#L48)；[Durability](../../../home/hatch/docs/files-and-library.md#L54)。

<a id="file-11"></a>
## home/hatch/docs/goals.md

来源：[home/hatch/docs/goals.md](../../../home/hatch/docs/goals.md)。

描述 Goals 页、目标和持续支持行为。目标记录不等于新建 cron；创建、进展更新、完成和删除有各自对象语义。具体领域编排放在 goals skill 的 creation 与 guides 下，本文件承担产品表面说明。

章节入口：[Goals](../../../home/hatch/docs/goals.md#L1)；[Creating and managing goals](../../../home/hatch/docs/goals.md#L7)；[Active and completed states](../../../home/hatch/docs/goals.md#L17)；[App controls](../../../home/hatch/docs/goals.md#L24)；[Goal briefings](../../../home/hatch/docs/goals.md#L32)；[Background work](../../../home/hatch/docs/goals.md#L42)。

<a id="file-12"></a>
## home/hatch/docs/ideas.md

来源：[home/hatch/docs/ideas.md](../../../home/hatch/docs/ideas.md)。

解释主动产生的 Ideas 卡片、选择执行及管理流程。建议出现、用户选择和实际构建产物是三个阶段；不能因卡片存在就称应用已生成。详情与原因应追踪真实记录，而非从最后标题反向编故事。

章节入口：[Ideas](../../../home/hatch/docs/ideas.md#L1)；[Running an idea](../../../home/hatch/docs/ideas.md#L7)；[Dismissing and expiry](../../../home/hatch/docs/ideas.md#L17)。

<a id="file-13"></a>
## home/hatch/docs/media.md

来源：[home/hatch/docs/media.md](../../../home/hatch/docs/media.md)。

列视频、图像和音频的能力、限制与相关工具路径。它是能力说明，不含模型生成实现；工具失败、时长/格式限制和保密环境差异需要按实际响应处理。生成结果应交付真实产物，不能把提示词或排队状态称为成品。

章节入口：[Media generation](../../../home/hatch/docs/media.md#L1)；[Images](../../../home/hatch/docs/media.md#L7)；[Video](../../../home/hatch/docs/media.md#L11)；[Audio, TTS, and podcasts](../../../home/hatch/docs/media.md#L19)；[Environment gates: no preflight signal](../../../home/hatch/docs/media.md#L27)；[Video playback](../../../home/hatch/docs/media.md#L31)；[Attributing generated media](../../../home/hatch/docs/media.md#L35)。

<a id="file-14"></a>
## home/hatch/docs/muse.md

来源：[home/hatch/docs/muse.md](../../../home/hatch/docs/muse.md)。

产品总入口，链接其他说明并规定能力问答的信息来源。包含公司、模型、发布时间与可用地区等本地声明；本报告不将其认证为线上事实。订阅/额度需 subscription-status 实际查询，内部服务标识不等于用户所用模型。

章节入口：[Muse](../../../home/hatch/docs/muse.md#L1)；[Quick Facts](../../../home/hatch/docs/muse.md#L10)；[Answering Product Questions](../../../home/hatch/docs/muse.md#L62)。

<a id="file-15"></a>
## home/hatch/docs/payments-and-purchases.md

来源：[home/hatch/docs/payments-and-purchases.md](../../../home/hatch/docs/payments-and-purchases.md)。

区分订阅与购买钱包、购物流程、交易审批及额度。购买审批绑定具体交易，不应从通用任务授权扩大为任意金额支付。Shop Pay、Stripe Link 与商户浏览器路径分别处理；退款由商户决定，不是 Agent 可以保证撤销的本地操作。

章节入口：[Purchases and payments](../../../home/hatch/docs/payments-and-purchases.md#L1)；[Purchase Flow](../../../home/hatch/docs/payments-and-purchases.md#L5)；[Purchase Approval](../../../home/hatch/docs/payments-and-purchases.md#L13)；[Connecting a Wallet](../../../home/hatch/docs/payments-and-purchases.md#L21)；[Shop Pay](../../../home/hatch/docs/payments-and-purchases.md#L27)；[Stripe Link](../../../home/hatch/docs/payments-and-purchases.md#L36)；[Shared wallet rules](../../../home/hatch/docs/payments-and-purchases.md#L43)；[Limits](../../../home/hatch/docs/payments-and-purchases.md#L53)；[Stripe Link purchase protections](../../../home/hatch/docs/payments-and-purchases.md#L62)；[Canceling, refunds, subscriptions](../../../home/hatch/docs/payments-and-purchases.md#L76)；[Paying with a merchant-saved card](../../../home/hatch/docs/payments-and-purchases.md#L82)；[Special cases](../../../home/hatch/docs/payments-and-purchases.md#L86)。

<a id="file-16"></a>
## home/hatch/docs/privacy-and-credentials.md

来源：[home/hatch/docs/privacy-and-credentials.md](../../../home/hatch/docs/privacy-and-credentials.md)。

将密码、OAuth、保存登录与 Agent 可读内容隔离；还描述导出、删除和账户级数据控制。安全存储可供授权填充不意味着明文可由 Agent 查询。实际凭据 vault/authd 不在源码内，迁移必须自己保留可信边界。

章节入口：[Privacy and credentials](../../../home/hatch/docs/privacy-and-credentials.md#L1)；[Sign-in secrets](../../../home/hatch/docs/privacy-and-credentials.md#L3)；[Saved logins](../../../home/hatch/docs/privacy-and-credentials.md#L58)；[Data retention and the user's controls](../../../home/hatch/docs/privacy-and-credentials.md#L81)；[Permissions](../../../home/hatch/docs/privacy-and-credentials.md#L110)；[Who can see the user's data](../../../home/hatch/docs/privacy-and-credentials.md#L149)。

<a id="file-17"></a>
## home/hatch/docs/referrals.md

来源：[home/hatch/docs/referrals.md](../../../home/hatch/docs/referrals.md)。

邀请/推荐机制与聊天共享不同。使用有效链接或代码、遵守产品 offer 条件和查询路径；不能把 invite 当成加入现有私人会话。优惠和资格受服务状态影响，本报告只分析规则组织，不确认当前额度和活动。

章节入口：[Referrals and invite codes](../../../home/hatch/docs/referrals.md#L1)；[Sharing an invitation](../../../home/hatch/docs/referrals.md#L8)；[Redeeming a code](../../../home/hatch/docs/referrals.md#L19)；[Offer terms and outcomes](../../../home/hatch/docs/referrals.md#L36)；[Missing options or failed lookups](../../../home/hatch/docs/referrals.md#L53)。

<a id="file-18"></a>
## home/hatch/docs/scheduling-and-watching.md

来源：[home/hatch/docs/scheduling-and-watching.md](../../../home/hatch/docs/scheduling-and-watching.md)。

明确观察由轮询完成，事件可能在两次检查间发生并消失；任务时间有分钟级偏移。告警不能阻止源系统事件，交付默认到用户聊天；对别人发消息是独立 connector send。cron.runs 才是执行证据，计划存在不是已运行。条件写入任务逻辑，不能假装调度器提供未支持的起止日期和 fire-only-when。

章节入口：[Scheduled work and watching](../../../home/hatch/docs/scheduling-and-watching.md#L1)；[How it works: polling, not watching](../../../home/hatch/docs/scheduling-and-watching.md#L7)；[Watches alert; they don't stop things](../../../home/hatch/docs/scheduling-and-watching.md#L24)；[Background work runs reliably](../../../home/hatch/docs/scheduling-and-watching.md#L33)；[Messages go to the user only](../../../home/hatch/docs/scheduling-and-watching.md#L39)；[Check the run history, not the schedule](../../../home/hatch/docs/scheduling-and-watching.md#L49)；[What you can do with jobs](../../../home/hatch/docs/scheduling-and-watching.md#L55)。

<a id="file-19"></a>
## home/hatch/docs/self_improvement.md

来源：[home/hatch/docs/self_improvement.md](../../../home/hatch/docs/self_improvement.md)。

描述记忆维护、关系整理、Ideas、目标学习、dreaming、skill review 与 quiet-moment 的后台工作和声明频率。用户不应自己创建这些内部任务。查询来源理由和交付链时使用 muse.db，再追踪文件；记录可能缺失或过期，accepted/handoff 不等于 delivered。

章节入口：[How You Evolve](../../../home/hatch/docs/self_improvement.md#L1)；[Explaining a suggestion or update](../../../home/hatch/docs/self_improvement.md#L31)；[Tracing what happened to the work](../../../home/hatch/docs/self_improvement.md#L46)。

<a id="file-20"></a>
## home/hatch/docs/voice.md

来源：[home/hatch/docs/voice.md](../../../home/hatch/docs/voice.md)。

拆开输入听写、语音消息转录、生成语音和实时通话等能力。客户端麦克风是否存在要按客户端事实判断，不把 mobile 功能泛化到 web。与 tts、voice-selector 的内容生成路径不同，单有声线列表无法实现打电话。

章节入口：[Voice](../../../home/hatch/docs/voice.md#L1)。

<a id="file-21"></a>
## home/hatch/docs/devices/mac_app.md

来源：[home/hatch/docs/devices/mac_app.md](../../../home/hatch/docs/devices/mac_app.md)。

Mac 客户端同时是聊天表面与设备配对入口。先 device.describe 获取当前命令，再考虑 AppleScript、消息等操作与系统授权。关闭窗口与退出应用不同；可见界面、全磁盘权限和消息发送不能由“已安装 Mac app”推导。

章节入口：[Mac App](../../../home/hatch/docs/devices/mac_app.md#L1)；[Choosing the Mac](../../../home/hatch/docs/devices/mac_app.md#L11)；[Mac Capabilities](../../../home/hatch/docs/devices/mac_app.md#L23)；[Apps and Browser](../../../home/hatch/docs/devices/mac_app.md#L44)；[Files and Capture](../../../home/hatch/docs/devices/mac_app.md#L59)；[Local App Data](../../../home/hatch/docs/devices/mac_app.md#L69)；[Local App Permissions](../../../home/hatch/docs/devices/mac_app.md#L82)；[User-Facing Language](../../../home/hatch/docs/devices/mac_app.md#L95)。

<a id="file-22"></a>
## home/hatch/docs/devices/tailscale.md

来源：[home/hatch/docs/devices/tailscale.md](../../../home/hatch/docs/devices/tailscale.md)。

解释把私有设备网络接入 Agent 的路径、连接前提与账户边界。配对设备能力与网络可达性不同；连入 tailnet 不等于获得任意服务登录权限。结合 tailscale skill 的状态、发现和故障诊断使用。

章节入口：[Tailscale](../../../home/hatch/docs/devices/tailscale.md#L11)；[Connecting](../../../home/hatch/docs/devices/tailscale.md#L26)；[Reaching Machines](../../../home/hatch/docs/devices/tailscale.md#L61)；[Inspecting](../../../home/hatch/docs/devices/tailscale.md#L88)；[User-Facing Language](../../../home/hatch/docs/devices/tailscale.md#L105)。

<a id="file-23"></a>
## home/hatch/docs/devices/home_link.md

来源：[home/hatch/docs/devices/home_link.md](../../../home/hatch/docs/devices/home_link.md)。

通过 Home Link 发现家庭网络设备并经 CONNECT proxy 访问。先取新发现结果，识别设备和协议，再按对应集成指南控制；地址、端口与品牌不能靠猜。凭据及控制授权仍独立，发现一个网络主机不是扫描或修改所有设备的理由。

章节入口：[Muse Home Link](../../../home/hatch/docs/devices/home_link.md#L1)；[Quick Facts](../../../home/hatch/docs/devices/home_link.md#L10)；[Link Commands](../../../home/hatch/docs/devices/home_link.md#L18)；[`device.health`](../../../home/hatch/docs/devices/home_link.md#L29)；[`device.ota`](../../../home/hatch/docs/devices/home_link.md#L34)；[`device.discover`](../../../home/hatch/docs/devices/home_link.md#L39)；[Finding a new device or a specific manufacturer](../../../home/hatch/docs/devices/home_link.md#L45)；[Presenting discovery results](../../../home/hatch/docs/devices/home_link.md#L70)；[Integration Guides](../../../home/hatch/docs/devices/home_link.md#L90)；[Catalog](../../../home/hatch/docs/devices/home_link.md#L102)；[Controlling Local Devices](../../../home/hatch/docs/devices/home_link.md#L117)；[HTTP APIs](../../../home/hatch/docs/devices/home_link.md#L149)；[Troubleshooting](../../../home/hatch/docs/devices/home_link.md#L176)；[User-Facing Language](../../../home/hatch/docs/devices/home_link.md#L190)。

<a id="file-24"></a>
## home/hatch/docs/devices/home_link/integrations/brother_printers.md

来源：[home/hatch/docs/devices/home_link/integrations/brother_printers.md](../../../home/hatch/docs/devices/home_link/integrations/brother_printers.md)。

实测指南以具体 Brother 型号为范围。读 IPP capabilities，支持时优先 PWG Raster，经 CUPS 转换并按纸张/分辨率缩放，再 Print-Job；结果不明先查 job 状态避免重复打印。不能把该型号测试当成全品牌兼容性保证。

章节入口：[Brother Printers: IPP Printing](../../../home/hatch/docs/devices/home_link/integrations/brother_printers.md#L1)；[Recommended Path](../../../home/hatch/docs/devices/home_link/integrations/brother_printers.md#L8)。

<a id="file-25"></a>
## home/hatch/docs/devices/home_link/integrations/lutron_smart_bridges.md

来源：[home/hatch/docs/devices/home_link/integrations/lutron_smart_bridges.md](../../../home/hatch/docs/devices/home_link/integrations/lutron_smart_bridges.md)。

指定 HomeKit/HAP 路线而非假设 telnet。ff=1 时选择 PairSetupWithAuth，整个配对保持同一代理 TCP 连接；使用八位 setup code，持久配对材料进入批准存储，文件型存储 mode 0600。控制前枚举真实 accessory/service/characteristic，避免硬编码 ID。

章节入口：[Lutron Smart Bridges: Light and Shade Control](../../../home/hatch/docs/devices/home_link/integrations/lutron_smart_bridges.md#L1)；[Recommended Path](../../../home/hatch/docs/devices/home_link/integrations/lutron_smart_bridges.md#L8)。

<a id="file-26"></a>
## home/hatch/docs/devices/home_link/integrations/shelly_plugs.md

来源：[home/hatch/docs/devices/home_link/integrations/shelly_plugs.md](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md)。

用 mDNS 和设备响应确认型号、代际；MAC 前缀只作旁证。Gen 2+ RPC 与 Gen 1 relay API 不兼容。通过 Home Link 访问实际发现端点，再读开关和功耗或执行开关；不要把设备名称、网络可达或零值功耗单独当完整状态。

章节入口：[Shelly Plugs (Gen 4): Switching and Power Metering](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L1)；[Identifying the Plug](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L9)；[Check the Generation First](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L29)；[Recommended Path](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L37)；[Endpoints](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L60)；[Auth](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L73)；[Other Capabilities](../../../home/hatch/docs/devices/home_link/integrations/shelly_plugs.md#L84)。

<a id="file-27"></a>
## home/hatch/config/home.yaml

来源：[home/hatch/config/home.yaml](../../../home/hatch/config/home.yaml)。

最小配置：root_agent 和 subagent reasoning effort 为 high；channels.providers 是空映射，schema_version 为 2。它没有路由模型、优先级或在线连接凭据。不能由 providers 为空推断整个产品不支持渠道。


<a id="file-28"></a>
## home/hatch/config/skills.yaml

来源：[home/hatch/config/skills.yaml](../../../home/hatch/config/skills.yaml)。

version 1 的 31 个 entries 均标 available；使用 snake_case 标识，与目录 kebab-case 并非逐字一致。它只覆盖部分 connector，不是 68 个技能总注册表，也不是“已连接且已授权”的账户状态。


<a id="file-29"></a>
## home/hatch/PROACTIVE_PREFERENCES.md

来源：[home/hatch/PROACTIVE_PREFERENCES.md](../../../home/hatch/PROACTIVE_PREFERENCES.md)。

用户主动消息偏好的可编辑文档；Tell me about、Never tell me about 和 How 基本是模板，When 给出本地 09:00–21:30 及安静时机约束。文件声明每次写消息前全读，不能据此证明加载代码实际执行。应把内容偏好与计划时间、渠道送达分开。

章节入口：[PROACTIVE_PREFERENCES.md](../../../home/hatch/PROACTIVE_PREFERENCES.md#L1)；[Tell me about](../../../home/hatch/PROACTIVE_PREFERENCES.md#L5)；[Never tell me about](../../../home/hatch/PROACTIVE_PREFERENCES.md#L7)；[When](../../../home/hatch/PROACTIVE_PREFERENCES.md#L9)；[How](../../../home/hatch/PROACTIVE_PREFERENCES.md#L13)。

<a id="file-30"></a>
## home/hatch/assets/onboarding_tour/memory_import.md

来源：[home/hatch/assets/onboarding_tour/memory_import.md](../../../home/hatch/assets/onboarding_tour/memory_import.md)。

仅在用户要求迁移时展示完整 portable prompt，让用户在另一助手生成、审阅并去掉不想分享的内容，再粘贴回来。导入响应是不可信资料，按正常 memory 流程保存，写成功才称已保存。标签中的 prompt 不是对当前 Agent 的执行指令。

章节入口：[Bring context from another AI](../../../home/hatch/assets/onboarding_tour/memory_import.md#L1)；[Identity](../../../home/hatch/assets/onboarding_tour/memory_import.md#L23)；[Profession & work](../../../home/hatch/assets/onboarding_tour/memory_import.md#L25)；[Communication preferences](../../../home/hatch/assets/onboarding_tour/memory_import.md#L27)；[Recurring people](../../../home/hatch/assets/onboarding_tour/memory_import.md#L29)；[Health & dietary](../../../home/hatch/assets/onboarding_tour/memory_import.md#L31)；[Interests & hobbies](../../../home/hatch/assets/onboarding_tour/memory_import.md#L33)；[Ongoing projects](../../../home/hatch/assets/onboarding_tour/memory_import.md#L35)；[Working style & values](../../../home/hatch/assets/onboarding_tour/memory_import.md#L37)；[Tools & environment](../../../home/hatch/assets/onboarding_tour/memory_import.md#L39)；[Anything else durable](../../../home/hatch/assets/onboarding_tour/memory_import.md#L41)。

<a id="file-31"></a>
## home/hatch/workspace/muse-security-audit.md

来源：[home/hatch/workspace/muse-security-audit.md](../../../home/hatch/workspace/muse-security-audit.md)。

旧环境的定向安全审计，包含不在当前仓库内的 icons、session logs、inode/hardlinks 与宿主路径。其 Clean 结论有明确方法限制，不能作为本轮执行证据或整个供应链安全背书。本报告重新核对当前文件格式和内容摘要，但未反编译所有二进制。

章节入口：[Muse security audit](../../../home/hatch/workspace/muse-security-audit.md#L1)；[Method](../../../home/hatch/workspace/muse-security-audit.md#L9)；[Files scanned](../../../home/hatch/workspace/muse-security-audit.md#L24)；[Filename hits (11)](../../../home/hatch/workspace/muse-security-audit.md#L26)；[Content hits under `/home/hatch`](../../../home/hatch/workspace/muse-security-audit.md#L46)；[Persistence](../../../home/hatch/workspace/muse-security-audit.md#L67)；[Findings per file](../../../home/hatch/workspace/muse-security-audit.md#L79)；[`/home/hatch/docs/muse.md` — clean](../../../home/hatch/workspace/muse-security-audit.md#L81)；[Museum icons and `muse-lockup-1x1.mp4` — clean](../../../home/hatch/workspace/muse-security-audit.md#L85)；[`muse-moments-kit.html` — clean](../../../home/hatch/workspace/muse-security-audit.md#L89)；[`muse-early-access/SKILL.md` — clean](../../../home/hatch/workspace/muse-security-audit.md#L93)；[`muse-feedback/SKILL.md` — clean](../../../home/hatch/workspace/muse-security-audit.md#L97)；[`muse-mail/SKILL.md` and `references/advanced.md` — clean](../../../home/hatch/workspace/muse-security-audit.md#L101)；[`muse_db/SKILL.md` and `references/schema.md` — clean](../../../home/hatch/workspace/muse-security-audit.md#L112)；[`/opt/hatch/bin/muse-mail` — clean product CLI in a shared binary](../../../home/hatch/workspace/muse-security-audit.md#L118)；[Session transcripts — clean on indicator scan](../../../home/hatch/workspace/muse-security-audit.md#L147)；[Hash manifest — clean](../../../home/hatch/workspace/muse-security-audit.md#L151)；[Overall verdict](../../../home/hatch/workspace/muse-security-audit.md#L162)。
