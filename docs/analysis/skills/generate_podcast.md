# generate_podcast：脚本、合成、目录与可选发布

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

脚本、合成、目录与可选发布。入口：[SKILL.md](../../../opt/hatch/skills/generate_podcast/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `generate_podcast` |
| frontmatter name | `generate_podcast` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Compose and deliver audio content: a podcast episode, briefing, or narrated summary, with one or more voices, as an MP3. For reading supplied text aloud verbatim, use tts.

<a id="flow"></a>
## 执行流程与输入输出

先定主题、说话人和实际 voice IDs；写适合朗读的完整对白与 topics 去重摘要；podcast-helper 生成音频和封面；交付可播放 MP3；只有明确授权才公开 RSS 发布或保存到个人 Spotify；周期节目先生成首集再安排后续。

<a id="design"></a>
## 实现思路、异常与限制

音频生成、节目目录、公开 feed 和个人 Spotify 保存是四个不同阶段。series ID 控制共享封面，topics 防止连续节目重复；公开发布受内容审查。

podcast-helper 与 voice_source.json 缺失，只有相关 CLI 和说明不足以跑全流程。分块失败不能交付残缺节目；重试保持同一声音，不更换后端绕过。公开 feed 与私人保存的可见性不同。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/generate_podcast/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/save-to-spotify.md](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md) | 优先 podcast-helper 上传并更新本地目录，避免只调用原始 CLI 导致目录失联；区别个人 Spotify 保存、公开 feed 和删除管理，并尊重已有节目 ID。 |
| [save-to-spotify/manifest.yaml](../../../opt/hatch/skills/generate_podcast/save-to-spotify/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |
| [save-to-spotify/vendor/save-to-spotify/README.md](../../../opt/hatch/skills/generate_podcast/save-to-spotify/vendor/save-to-spotify/README.md) | 描述二进制 release pin 与 SOURCE.toml 更新流程，正文提及的源码和 pin 文件未完整附带。不能把说明文件视为 CLI 源码。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### save-to-spotify/manifest.yaml

来源：[opt/hatch/skills/generate_podcast/save-to-spotify/manifest.yaml](../../../opt/hatch/skills/generate_podcast/save-to-spotify/manifest.yaml)；connector：`save-to-spotify`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `content_read` | `shows.read` | `allow` | 否 | — | List shows and show details |
| `content_read` | `episodes.read` | `allow` | 否 | — | List episodes and check episode status |
| `content_read` | `timeline.read` | `allow` | 否 | — | Read episode timeline items |
| `content_write` | `shows.write` | `ask` | 否 | — | Create a show |
| `content_write` | `episodes.write` | `ask` | 否 | — | Upload and publish an episode |
| `content_write` | `timeline.write` | `ask` | 否 | — | Set episode timeline items |
| `content_delete` | `shows.delete` | `allow` | 否 | — | Delete a show and its episodes |
| `content_delete` | `episodes.delete` | `allow` | 否 | — | Delete an episode |
| `content_delete` | `timeline.delete` | `allow` | 否 | — | Delete episode timeline items |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `upload` | `episodes.write` |
| `shows create` | `shows.write` |
| `shows delete` | `shows.delete` |
| `shows get` | `shows.read` |
| `shows` | `shows.read` |
| `episodes create` | `episodes.write` |
| `episodes delete` | `episodes.delete` |
| `episodes status` | `episodes.read` |
| `episodes` | `episodes.read` |
| `timeline set` | `timeline.write` |
| `timeline get` | `timeline.read` |
| `timeline delete` | `timeline.delete` |
| `list` | `shows.read` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时先实现本地生成及清晰 manifest，再在有需求时增加发布 adapter。episode 状态保存 generated、published 和 saved 的独立结果。

最小验收建议：一块合成失败不产生完整成功状态；公开发布 blocked 时保留本地音频但禁止替代路径发布。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Generate Podcast](../../../opt/hatch/skills/generate_podcast/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/generate_podcast/SKILL.md#L9) | 9 |
| [Workflow](../../../opt/hatch/skills/generate_podcast/SKILL.md#L12) | 12 |
| [1. Plan](../../../opt/hatch/skills/generate_podcast/SKILL.md#L14) | 14 |
| [2. Write the script](../../../opt/hatch/skills/generate_podcast/SKILL.md#L21) | 21 |
| [3. Generate](../../../opt/hatch/skills/generate_podcast/SKILL.md#L50) | 50 |
| [4. Deliver to chat](../../../opt/hatch/skills/generate_podcast/SKILL.md#L110) | 110 |
| [5. Publish (if not done in step 3)](../../../opt/hatch/skills/generate_podcast/SKILL.md#L125) | 125 |
| [6. Subscribe (after publishing)](../../../opt/hatch/skills/generate_podcast/SKILL.md#L149) | 149 |
| [Feed Organization](../../../opt/hatch/skills/generate_podcast/SKILL.md#L171) | 171 |
| [Add to your Spotify (personal, optional)](../../../opt/hatch/skills/generate_podcast/SKILL.md#L179) | 179 |
| [Cover Art](../../../opt/hatch/skills/generate_podcast/SKILL.md#L227) | 227 |
| [Scheduling](../../../opt/hatch/skills/generate_podcast/SKILL.md#L251) | 251 |
| [Utility Commands](../../../opt/hatch/skills/generate_podcast/SKILL.md#L280) | 280 |
| [Listening to Existing Episodes](../../../opt/hatch/skills/generate_podcast/SKILL.md#L289) | 289 |
| [Operating Rules](../../../opt/hatch/skills/generate_podcast/SKILL.md#L296) | 296 |

### references/save-to-spotify.md

| 源章节 | 起始行 |
|---|---|
| [Add a generated episode to the user's Spotify](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L1) | 1 |
| [Prefer `podcast-helper save-to-spotify` for the upload](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L8) | 8 |
| [Tooling](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L16) | 16 |
| [Auth (shared Spotify connection — connect in Settings)](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L40) | 40 |
| [Upload flow](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L50) | 50 |
| [Deletion flow](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L65) | 65 |
| [Rules](../../../opt/hatch/skills/generate_podcast/references/save-to-spotify.md#L96) | 96 |

### save-to-spotify/vendor/save-to-spotify/README.md

| 源章节 | 起始行 |
|---|---|
| [save-to-spotify CLI release pin](../../../opt/hatch/skills/generate_podcast/save-to-spotify/vendor/save-to-spotify/README.md#L1) | 1 |
| [SOURCE.toml fields](../../../opt/hatch/skills/generate_podcast/save-to-spotify/vendor/save-to-spotify/README.md#L14) | 14 |
| [Update flow](../../../opt/hatch/skills/generate_podcast/save-to-spotify/vendor/save-to-spotify/README.md#L23) | 23 |
| [Operational note](../../../opt/hatch/skills/generate_podcast/save-to-spotify/vendor/save-to-spotify/README.md#L41) | 41 |
