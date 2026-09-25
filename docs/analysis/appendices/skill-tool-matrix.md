# 技能与工具对应关系

[返回目录](../README.md) · [权限解释](../04-tooling-and-permissions.md)

矩阵按 68 个独立技能列出本目录文本实际出现的本地 CLI 名称、manifest 及 eval 情况。匹配使用完整名称边界，属于文本证据；不等于所有出现的名字都会在每次执行中调用。未出现不代表没有原生工具、远程 MCP 或间接依赖。跨技能引用见各篇流程。

原生工具的重要类别包括 device、cron、goals、artifact、browser、muse.db、phone、channel 与模型媒体能力。其执行器没有以同名可读源文件全部给出；不能强制映射到 ELF 才算能力。

| 技能 | 本地 CLI 名称的文本线索 | 独立 manifest | YAML 场景数 | 分析 |
|---|---|---|---|---|
| `apple-healthkit` | `health-cli`, `share` | 是 | 0 | [详解](../skills/apple-healthkit.md) |
| `artifacts/document` | `edits`, `hatch` | 否 | 0 | [详解](../skills/artifacts/document.md) |
| `artifacts/markdown` | `hatch` | 否 | 0 | [详解](../skills/artifacts/markdown.md) |
| `artifacts/pdf` | `hatch`, `places`, `share` | 否 | 0 | [详解](../skills/artifacts/pdf.md) |
| `artifacts/presentation` | `edits`, `hatch`, `hatch-slide-style`, `image-search`, `share` | 否 | 0 | [详解](../skills/artifacts/presentation.md) |
| `artifacts/spreadsheet` | `edits`, `hatch` | 否 | 0 | [详解](../skills/artifacts/spreadsheet.md) |
| `artifacts/testing` | `hatch` | 否 | 0 | [详解](../skills/artifacts/testing.md) |
| `booking` | `duffel`, `hatch`, `opentable`, `shopping`, `ticketmaster` | 否 | 16 | [详解](../skills/booking.md) |
| `calendly` | `calendly`, `share` | 是 | 0 | [详解](../skills/calendly.md) |
| `device-data` | `device-data` | 否 | 0 | [详解](../skills/device-data.md) |
| `duffel` | `duffel`, `hatch`, `places`, `stripe-link` | 是 | 19 | [详解](../skills/duffel.md) |
| `facebook-cli` | `facebook-cli`, `geocode`, `hatch_messenger_cli`, `share`, `shopping` | 是 | 0 | [详解](../skills/facebook-cli.md) |
| `flightaware` | `duffel`, `edits`, `flightaware`, `hatch`, `opentable` | 是 | 13 | [详解](../skills/flightaware.md) |
| `forget` | `places`, `shopping` | 否 | 0 | [详解](../skills/forget.md) |
| `function-health` | `function-health`, `share` | 是 | 0 | [详解](../skills/function-health.md) |
| `generate_podcast` | `hatch`, `media-generation`, `save-to-spotify`, `share`, `spotify-api`, `tts` | 否 | 0 | [详解](../skills/generate_podcast.md) |
| `gmail` | `calendly`, `hatch`, `hatch_gws_cli` | 是 | 20 | [详解](../skills/gmail.md) |
| `goals` | `hatch`, `share` | 否 | 0 | [详解](../skills/goals.md) |
| `google-calendar` | `hatch_gws_cli`, `share` | 是 | 15 | [详解](../skills/google-calendar.md) |
| `google-contacts` | `edits`, `hatch_gws_cli`, `share` | 是 | 11 | [详解](../skills/google-contacts.md) |
| `google-docs` | `edits`, `hatch_gws_cli`, `share` | 是 | 0 | [详解](../skills/google-docs.md) |
| `google-drive` | `hatch`, `hatch_gws_cli`, `share` | 是 | 17 | [详解](../skills/google-drive.md) |
| `google-forms` | `hatch_gws_cli`, `share` | 是 | 0 | [详解](../skills/google-forms.md) |
| `google-health-connect` | `health-cli` | 是 | 0 | [详解](../skills/google-health-connect.md) |
| `google-sheets` | `hatch_gws_cli`, `share` | 是 | 0 | [详解](../skills/google-sheets.md) |
| `google-slides` | `edits`, `hatch_gws_cli`, `share` | 是 | 0 | [详解](../skills/google-slides.md) |
| `google-tasks` | `edits`, `hatch_gws_cli`, `share` | 是 | 16 | [详解](../skills/google-tasks.md) |
| `granola` | `granola-cli`, `share` | 是 | 0 | [详解](../skills/granola.md) |
| `healthex` | `healthex`, `share` | 是 | 0 | [详解](../skills/healthex.md) |
| `image-search` | `hatch`, `image-search`, `share` | 否 | 0 | [详解](../skills/image-search.md) |
| `instagram` | `hatch-zeitgeist`, `instagram-cli`, `instagram-messages-cli`, `shopping` | 是 | 0 | [详解](../skills/instagram.md) |
| `instagram-messages` | `instagram-cli`, `instagram-messages-cli`, `share` | 是 | 0 | [详解](../skills/instagram-messages.md) |
| `magic-moment` | `hatch`, `share`, `shopping` | 否 | 0 | [详解](../skills/magic-moment.md) |
| `media-library` | `geocode`, `hatch`, `media-library` | 否 | 0 | [详解](../skills/media-library.md) |
| `messenger` | `edits`, `hatch_messenger_cli`, `share` | 是 | 0 | [详解](../skills/messenger.md) |
| `muse-early-access` | `feature-request`, `hatch` | 否 | 0 | [详解](../skills/muse-early-access.md) |
| `muse-feedback` | `feature-request`, `hatch`, `share` | 否 | 0 | [详解](../skills/muse-feedback.md) |
| `muse-mail` | `hatch`, `muse-mail` | 否 | 0 | [详解](../skills/muse-mail.md) |
| `muse_db` | `share`, `stripe-link` | 否 | 0 | [详解](../skills/muse_db.md) |
| `notion` | `notion-cli`, `share` | 是 | 0 | [详解](../skills/notion.md) |
| `opentable` | `hatch`, `opentable` | 是 | 19 | [详解](../skills/opentable.md) |
| `outlook-calendar` | `outlook-calendar`, `share` | 是 | 0 | [详解](../skills/outlook-calendar.md) |
| `outlook-contacts` | `outlook-contacts`, `share` | 是 | 0 | [详解](../skills/outlook-contacts.md) |
| `outlook-mail` | `outlook-mail`, `share` | 是 | 0 | [详解](../skills/outlook-mail.md) |
| `peloton` | `peloton`, `share` | 是 | 0 | [详解](../skills/peloton.md) |
| `philips-hue` | `philips-hue`, `share` | 是 | 0 | [详解](../skills/philips-hue.md) |
| `places-search` | `geocode`, `local-search`, `places`, `share` | 否 | 9 | [详解](../skills/places-search.md) |
| `plaid` | `plaid`, `share` | 是 | 8 | [详解](../skills/plaid.md) |
| `printify` | `printify`, `share` | 是 | 0 | [详解](../skills/printify.md) |
| `self-awareness` | `hatch` | 否 | 0 | [详解](../skills/self-awareness.md) |
| `share-ideas` | `share` | 否 | 0 | [详解](../skills/share-ideas.md) |
| `shopping` | `facebook-cli`, `hatch`, `instagram-cli`, `meta-catalog-search`, `places`, `share`, `shopify-ucp-cli`, `shopping`, `stripe-link` | 否 | 0 | [详解](../skills/shopping.md) |
| `skill-creator` | `hatch`, `outlook-calendar`, `places` | 否 | 0 | [详解](../skills/skill-creator.md) |
| `spotify` | `save-to-spotify`, `share`, `spotify-api` | 是 | 0 | [详解](../skills/spotify.md) |
| `subscription-status` | `subscription-status` | 否 | 0 | [详解](../skills/subscription-status.md) |
| `tailscale` | `hatch`, `tailscale` | 否 | 0 | [详解](../skills/tailscale.md) |
| `tessie` | `share`, `tessie-api` | 是 | 0 | [详解](../skills/tessie.md) |
| `threads` | `instagram-cli`, `share`, `threads-cli`, `threads-messages-cli` | 是 | 0 | [详解](../skills/threads.md) |
| `threads-messages` | `share`, `threads-cli`, `threads-messages-cli` | 是 | 0 | [详解](../skills/threads-messages.md) |
| `ticketmaster` | `hatch`, `ticketmaster` | 是 | 0 | [详解](../skills/ticketmaster.md) |
| `travel-planning` | `duffel`, `hatch`, `opentable`, `places`, `share`, `ticketmaster` | 否 | 24 | [详解](../skills/travel-planning.md) |
| `tts` | `hatch`, `remote-storage`, `tts` | 是 | 0 | [详解](../skills/tts.md) |
| `voice-design` | 无本地 CLI 名称匹配；核对原生/远程工具契约 | 否 | 0 | [详解](../skills/voice-design.md) |
| `voice-selector` | 无本地 CLI 名称匹配；核对原生/远程工具契约 | 否 | 0 | [详解](../skills/voice-selector.md) |
| `wearable-device-skills` | 无本地 CLI 名称匹配；核对原生/远程工具契约 | 否 | 0 | [详解](../skills/wearable-device-skills.md) |
| `wearables-comms` | `device-data` | 否 | 0 | [详解](../skills/wearables-comms.md) |
| `wide-research` | 无本地 CLI 名称匹配；核对原生/远程工具契约 | 否 | 0 | [详解](../skills/wide-research.md) |
| `withings` | `hatch`, `share`, `withings` | 是 | 0 | [详解](../skills/withings.md) |

## 分流示例

| 任务链 | 组合 | 交接数据 |
|---|---|---|
| 旅行计划到航班预订 | travel-planning → booking → duffel/官网 | 精确行程、人数、候选签名、planning posture、金额与退改 |
| 生成后上传 Google 文件 | artifacts/document 或 presentation → google-docs/slides → google-drive | 可编辑源、导出路径、目标 ID、远端漂移检查 |
| 设备健康问题 | wearable-device-skills/device-data → 平台 HealthKit 或 Health Connect | device.describe 结果、数据类别、单位、时间区间、数据缺口 |
| 社交发现到购物 | facebook-cli Marketplace → shopping | 商品/变体/商户 ID、真实 URL、资格与当前总价 |
| 语音产物 | tts 或 generate_podcast → voice-selector/voice-design | 原文与新稿区分、声线 ID、发音、音频文件与发布状态 |
| 进度解释 | 产品状态问题 → muse_db | 准确 request/run/message/delivery ID，受限只读查询 |

这些是文本指导的工作流组合，不是程序中注册的固定 DAG。实际会话应只加载必要分支，且以工具返回的实时能力为准。
