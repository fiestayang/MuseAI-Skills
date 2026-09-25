# 技能分析目录

[返回总目录](../README.md)

覆盖 68 个独立技能；4 个别名只记录实际指向，不重复当成独立能力。每篇包含流程、逐文件职责、权限展开、已有场景和迁移验收建议。

| 技能 | name | 常驻元数据声明 | 分析重点 |
|---|---|---|---|
| [apple-healthkit](apple-healthkit.md) | `apple_healthkit` | `true` | Apple Health 同步数据的统一查询 |
| [artifacts/document](artifacts/document.md) | `artifact_document` | `false` | Word 文档生成与编辑 |
| [artifacts/markdown](artifacts/markdown.md) | `artifact_markdown` | `false` | 纯 Markdown 文档交付 |
| [artifacts/pdf](artifacts/pdf.md) | `artifact_pdf` | `false` | 以 HTML 源生成固定版式 PDF |
| [artifacts/presentation](artifacts/presentation.md) | `artifact_presentation` | `false` | 逐页 HTML 的演示文稿流水线 |
| [artifacts/spreadsheet](artifacts/spreadsheet.md) | `artifact_spreadsheet` | `false` | 可重算工作簿与局部修改 |
| [artifacts/testing](artifacts/testing.md) | `artifact_testing` | `false` | 产物的统一验收入口 |
| [booking](booking.md) | `booking` | `true` | 交易入口和供应商路由 |
| [calendly](calendly.md) | `calendly` | `false` | 用户范围内的预约数据访问 |
| [device-data](device-data.md) | `device_data` | `true` | 设备同步缓存的读取和定界删除 |
| [duffel](duffel.md) | `duffel` | `false` | 航班报价、验证、购票与票价跟踪 |
| [facebook-cli](facebook-cli.md) | `facebook_cli` | `true` | 社交内容阅读与自有商品刊登 |
| [flightaware](flightaware.md) | `flightaware` | `true` | 精确日期航班状态与运行监控 |
| [forget](forget.md) | `forget` | `true` | 跨记忆及衍生状态的遗忘事务 |
| [function-health](function-health.md) | `function_health` | `false` | 有来源的检验指标与临床备注读取 |
| [generate_podcast](generate_podcast.md) | `generate_podcast` | `true` | 脚本、合成、目录与可选发布 |
| [gmail](gmail.md) | `gmail` | `true` | 邮件检索、组织与精确发送 |
| [goals](goals.md) | `goals` | `true` | 持久目标的创建与持续跟进 |
| [google-calendar](google-calendar.md) | `google_calendar` | `true` | 日历读取与通知敏感写入 |
| [google-contacts](google-contacts.md) | `google_contacts` | `false` | 联系人定位与字段保留更新 |
| [google-docs](google-docs.md) | `google_docs` | `false` | 有格式内容发布到 Google Docs |
| [google-drive](google-drive.md) | `google_drive` | `false` | 文件身份、内容和共享管理 |
| [google-forms](google-forms.md) | `google_forms` | `false` | 表单结构与回答的对应读取 |
| [google-health-connect](google-health-connect.md) | `google_health_connect` | `true` | Android Health Connect 同步数据 |
| [google-sheets](google-sheets.md) | `google_sheets` | `false` | 在线表格局部写入和格式验证 |
| [google-slides](google-slides.md) | `google_slides` | `false` | 演示文稿生成后转换发布 |
| [google-tasks](google-tasks.md) | `google_tasks` | `false` | 日期型任务与列表管理 |
| [granola](granola.md) | `granola` | `false` | 动态 MCP 会议知识检索 |
| [healthex](healthex.md) | `healthex` | `false` | 动态 MCP 医疗记录检索 |
| [image-search](image-search.md) | `image_search` | `true` | 公共图片搜索与来源保留 |
| [instagram-messages](instagram-messages.md) | `instagram_messages` | `false` | 独立私信连接与精确消息发送 |
| [instagram](instagram.md) | `instagram` | `true` | 账户绑定的内容读取、理解与发布 |
| [magic-moment](magic-moment.md) | `magic-moment` | `false` | 有事实约束的竖屏故事视频流水线 |
| [media-library](media-library.md) | `media_library` | `true` | 已上传图库与设备图库的分层检索 |
| [messenger](messenger.md) | `messenger_read` | `true` | 本地同步消息、联系人与安全写入 |
| [muse-early-access](muse-early-access.md) | `muse_early_access` | `true` | 通用抢先体验的申请与状态 |
| [muse-feedback](muse-feedback.md) | `muse-feedback` | `true` | 经授权的反馈提交与去重 |
| [muse-mail](muse-mail.md) | `muse_mail` | `true` | Agent 专用邮箱与来源授权 |
| [muse_db](muse_db.md) | `muse_db` | `false` | 受限数据库诊断入口 |
| [notion](notion.md) | `notion` | `false` | 动态 MCP 文档操作 |
| [opentable](opentable.md) | `opentable` | `false` | 餐厅身份、实时桌位与锁定预订 |
| [outlook-calendar](outlook-calendar.md) | `outlook_calendar` | `false` | Outlook 事件与邀请效果控制 |
| [outlook-contacts](outlook-contacts.md) | `outlook_contacts` | `false` | Outlook 联系人检索与局部更新 |
| [outlook-mail](outlook-mail.md) | `outlook_mail` | `false` | Outlook 邮件读取与可恢复删除 |
| [peloton](peloton.md) | `peloton` | `false` | 课程发现与训练预约 |
| [philips-hue](philips-hue.md) | `philips_hue` | `false` | OAuth 与 Bridge 就绪后的灯光控制 |
| [places-search](places-search.md) | `places_search` | `false` | 地点检索、详情和地图呈现 |
| [plaid](plaid.md) | `plaid` | `true` | 跨金融机构的只读账户数据 |
| [printify](printify.md) | `printify` | `false` | 按店铺隔离的按需印刷管理 |
| [self-awareness](self-awareness.md) | `self_awareness` | `false` | 以当前状态回答 Agent 自身问题 |
| [share-ideas](share-ideas.md) | `share_ideas` | `true` | 显式发布可复用原生 Idea |
| [shopping](shopping.md) | `shopping` | `true` | 多来源商品发现与受控购买 |
| [skill-creator](skill-creator.md) | `skill_creator` | `true` | 技能作者工作流与资源拆分 |
| [spotify](spotify.md) | `spotify` | `true` | 音乐、播客、播放列表与播放路由 |
| [subscription-status](subscription-status.md) | `subscription_status` | `true` | 实时套餐与额度查询 |
| [tailscale](tailscale.md) | `tailscale` | `false` | 私有网络的受限 TCP 访问 |
| [tessie](tessie.md) | `tessie` | `false` | 车辆状态与明确物理动作 |
| [threads-messages](threads-messages.md) | `threads_messages` | `false` | Threads 私信读取与不可重试发送 |
| [threads](threads.md) | `threads` | `true` | Threads 内容查询、分析与发布 |
| [ticketmaster](ticketmaster.md) | `ticketmaster` | `false` | 活动定位和带价格的座位推荐 |
| [travel-planning](travel-planning.md) | `travel_planning` | `true` | 多阶段旅行规划与决策状态维护 |
| [tts](tts.md) | `tts` | `true` | 输入文本的单人或多人语音合成 |
| [voice-design](voice-design.md) | `voice_design` | `false` | 语音选择与异步定制 |
| [voice-selector](voice-selector.md) | `voice_selector` | `false` | 静态声音目录的占位入口 |
| [wearable-device-skills](wearable-device-skills.md) | `wearable_device_skills` | `true` | 设备实时能力注册表的发现与调用 |
| [wearables-comms](wearables-comms.md) | `wearables_comms` | `true` | 穿戴来源的通话与短信 |
| [wide-research](wide-research.md) | `wide_research` | `false` | 同构多对象研究协调 |
| [withings](withings.md) | `withings` | `false` | 带单位字段与明确聚合规则的健康读取 |

## 别名

| 入口 | 实际指向 | 说明 |
|---|---|---|
| `facebook` | [facebook-cli](facebook-cli.md) | 复用正文；不新增实现 |
| `meta-threads` | [threads](threads.md) | 复用正文；不新增实现 |
| `podcast` | [generate_podcast](generate_podcast.md) | 复用正文；不新增实现 |
| `voice-calls` | [voice-selector](voice-selector.md) | 静态语音目录，不是打电话能力 |

## 无顶层技能入口的共享资源

[Artifacts 共享参考与 Spaces 模板](../appendices/shared-resources.md)。Spaces 不额外计为一个 skill。

## 完整技能源目录树

含配套参考、manifest、eval、别名及无独立入口的共享目录；用于与上面的分析篇目对照。

```text
opt/hatch/skills/
├── apple-healthkit/
│   ├── SKILL.md
│   └── manifest.yaml
├── artifacts/
│   ├── document/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── editing.md
│   │       └── visual.md
│   ├── markdown/
│   │   └── SKILL.md
│   ├── pdf/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── existing-pdfs.md
│   │       ├── visual.md
│   │       └── workflow.md
│   ├── presentation/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── authoring.md
│   │       ├── design-system.md
│   │       ├── editing.md
│   │       ├── image-directive.md
│   │       ├── theme.md
│   │       ├── visual.md
│   │       └── workflow.md
│   ├── references/
│   │   ├── charts.md
│   │   ├── live-data.md
│   │   ├── maps.md
│   │   ├── markdown.md
│   │   ├── prose.md
│   │   └── social-embeds.md
│   ├── spreadsheet/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── formulas.md
│   │       └── visual.md
│   └── testing/
│       └── SKILL.md
├── booking/
│   ├── SKILL.md
│   ├── assets/
│   │   └── airline-logos/
│   │       ├── NOTICE.md
│   │       └── UPSTREAM.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── references/
│       ├── browser-booking.md
│       ├── flights.md
│       ├── hotels.md
│       ├── presentation.md
│       ├── restaurants.md
│       └── tickets.md
├── calendly/
│   ├── SKILL.md
│   └── manifest.yaml
├── device-data/
│   └── SKILL.md
├── duffel/
│   ├── SKILL.md
│   ├── eval/
│   │   └── tracked-flight-scenarios.yaml
│   └── manifest.yaml
├── facebook/
│   ├── SKILL.md -> ../facebook-cli/SKILL.md
│   └── manifest.yaml -> ../facebook-cli/manifest.yaml
├── facebook-cli/
│   ├── SKILL.md
│   ├── manifest.yaml
│   └── references/
│       ├── comments.md
│       ├── events.md
│       ├── feed.md
│       ├── friends.md
│       ├── groups.md
│       ├── marketplace.md
│       ├── posts.md
│       ├── profile.md
│       ├── reactions.md
│       ├── saved.md
│       ├── story.md
│       └── timeline.md
├── flightaware/
│   ├── SKILL.md
│   ├── eval/
│   │   ├── findings.md
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── forget/
│   ├── SKILL.md
│   └── references/
│       └── artifact-inventory.md
├── function-health/
│   ├── SKILL.md
│   └── manifest.yaml
├── generate_podcast/
│   ├── SKILL.md
│   ├── references/
│   │   └── save-to-spotify.md
│   └── save-to-spotify/
│       ├── manifest.yaml
│       └── vendor/
│           └── save-to-spotify/
│               └── README.md
├── gmail/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── goals/
│   ├── SKILL.md
│   ├── creation/
│   │   ├── career.md
│   │   ├── health.md
│   │   ├── interests.md
│   │   ├── money.md
│   │   ├── productivity.md
│   │   ├── relationships.md
│   │   └── something_else.md
│   └── guides/
│       ├── career/
│       │   └── scaffold.md
│       ├── health/
│       │   └── scaffold.md
│       ├── interests/
│       │   └── scaffold.md
│       ├── money/
│       │   └── scaffold.md
│       ├── productivity/
│       │   └── scaffold.md
│       ├── relationships/
│       │   └── scaffold.md
│       └── something_else/
│           └── scaffold.md
├── google-calendar/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── google-contacts/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── google-docs/
│   ├── SKILL.md
│   └── manifest.yaml
├── google-drive/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── google-forms/
│   ├── SKILL.md
│   └── manifest.yaml
├── google-health-connect/
│   ├── SKILL.md
│   └── manifest.yaml
├── google-sheets/
│   ├── SKILL.md
│   └── manifest.yaml
├── google-slides/
│   ├── SKILL.md
│   └── manifest.yaml
├── google-tasks/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── granola/
│   ├── SKILL.md
│   └── manifest.yaml
├── healthex/
│   ├── SKILL.md
│   └── manifest.yaml
├── image-search/
│   └── SKILL.md
├── instagram/
│   ├── SKILL.md
│   ├── manifest.yaml
│   └── references/
│       └── content-questions.md
├── instagram-messages/
│   ├── SKILL.md
│   └── manifest.yaml
├── magic-moment/
│   ├── INSTALL.md
│   ├── SKILL.md
│   ├── guide/
│   │   ├── conversation_shape.md
│   │   ├── screenplay.md
│   │   ├── screenplay_review.md
│   │   ├── story_and_canon.md
│   │   ├── timeline.md
│   │   └── visuals.md
│   └── reference/
│       ├── card-spec.md
│       ├── design-system/
│       │   ├── muse-moments-kit.html
│       │   └── story-compositions.html
│       ├── design.md
│       ├── overlay-spec.md
│       └── visual-storytelling.md
├── media-library/
│   └── SKILL.md
├── messenger/
│   ├── SKILL.md
│   └── manifest.yaml
├── meta-threads/
│   ├── SKILL.md -> ../threads/SKILL.md
│   └── manifest.yaml -> ../threads/manifest.yaml
├── muse-early-access/
│   └── SKILL.md
├── muse-feedback/
│   └── SKILL.md
├── muse-mail/
│   ├── SKILL.md
│   └── references/
│       └── advanced.md
├── muse_db/
│   ├── SKILL.md
│   └── references/
│       └── schema.md
├── notion/
│   ├── SKILL.md
│   └── manifest.yaml
├── opentable/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── outlook-calendar/
│   ├── SKILL.md
│   └── manifest.yaml
├── outlook-contacts/
│   ├── SKILL.md
│   └── manifest.yaml
├── outlook-mail/
│   ├── SKILL.md
│   └── manifest.yaml
├── peloton/
│   ├── SKILL.md
│   └── manifest.yaml
├── philips-hue/
│   ├── SKILL.md
│   └── manifest.yaml
├── places-search/
│   ├── SKILL.md
│   └── eval/
│       └── scenarios.yaml
├── plaid/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── manifest.yaml
├── podcast/
│   └── SKILL.md -> ../generate_podcast/SKILL.md
├── printify/
│   ├── SKILL.md
│   └── manifest.yaml
├── self-awareness/
│   ├── SKILL.md
│   └── references/
│       ├── extensions.md
│       └── question_types.md
├── share-ideas/
│   └── SKILL.md
├── shopping/
│   ├── SKILL.md
│   └── references/
│       ├── backends.md
│       ├── browser-checkout.md
│       └── shopify-ucp.md
├── skill-creator/
│   ├── SKILL.md
│   └── references/
│       └── authoring_guide.md
├── spaces/
│   ├── templates/
│   │   ├── space-static/
│   │   │   └── workspace_agents.md
│   │   └── space-ts/
│   │       └── workspace_agents.md
│   └── ts-runtime/
│       ├── README.md
│       └── docs/
│           └── vertical-tool-schemas.md
├── spotify/
│   ├── SKILL.md
│   └── manifest.yaml
├── subscription-status/
│   └── SKILL.md
├── tailscale/
│   └── SKILL.md
├── tessie/
│   ├── SKILL.md
│   └── manifest.yaml
├── threads/
│   ├── SKILL.md
│   └── manifest.yaml
├── threads-messages/
│   ├── SKILL.md
│   └── manifest.yaml
├── ticketmaster/
│   ├── SKILL.md
│   └── manifest.yaml
├── travel-planning/
│   ├── SKILL.md
│   ├── eval/
│   │   └── scenarios.yaml
│   └── references/
│       ├── booking-handoff.md
│       ├── flight-itinerary-discovery.md
│       ├── operational-itinerary.md
│       ├── planning-kickoff.md
│       └── travel-fact-verification.md
├── tts/
│   ├── SKILL.md
│   └── manifest.yaml
├── voice-calls/
│   └── SKILL.md -> ../voice-selector/SKILL.md
├── voice-design/
│   └── SKILL.md
├── voice-selector/
│   └── SKILL.md
├── wearable-device-skills/
│   └── SKILL.md
├── wearables-comms/
│   └── SKILL.md
├── wide-research/
│   └── SKILL.md
└── withings/
    ├── SKILL.md
    ├── manifest.yaml
    └── references/
        └── commands.md
```
