# spotify：音乐、播客、播放列表与播放路由

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

音乐、播客、播放列表与播放路由。入口：[SKILL.md](../../../opt/hatch/skills/spotify/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `spotify` |
| frontmatter name | `spotify` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Discover, search, and manage Spotify music, podcasts, and playlists, including deleting shows or episodes you created with Save to Spotify.

<a id="flow"></a>
## 执行流程与输入输出

status 后按 search/library/experience 读取，next-page 复用返回链接；保存及 playlist create/add/update 使用真实 URI；播放前验证设备；穿戴入口用 wearable-play 解析，再将 node_command/params 交设备执行；生成节目管理另走 save-to-spotify。

<a id="design"></a>
## 实现思路、异常与限制

搜索类型与库过滤类型并不相同。播放目标和内容 URI 分开；wearable-play 只解析，不代表已经开始播放。Save to Spotify 自建节目与普通 Spotify 库对象有不同删除接口。

不支持的 home、recommendations、history 等能力不能靠重连获得。精确歌曲缺失要按 fallback 报告，不用翻唱冒充。后续页面 URL 不能自行拼。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/spotify/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/spotify/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### spotify/manifest.yaml

来源：[opt/hatch/skills/spotify/manifest.yaml](../../../opt/hatch/skills/spotify/manifest.yaml)；connector：`spotify`。

请求配额声明：`mode` = `enforce`；`workers` = `['spotify-api']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `access.read` | `allow` | 否 | — | Read access |
| `write` | `library.manage` | `allow` | 是 | — | Manage library |
| `write` | `playback.control` | `allow` | 是 | — | Manage playback |
| `write` | `content.manage` | `ask` | 否 | — | Publish and manage content |

命令到方法的完整映射：

| 命令键 | 权限方法 |
|---|---|
| `status` | `null`（不映射方法；不等于任意放行） |
| `disconnect` | `null`（不映射方法；不等于任意放行） |
| `authorize-url` | `null`（不映射方法；不等于任意放行） |
| `exchange-code` | `null`（不映射方法；不等于任意放行） |
| `experience` | `access.read` |
| `next-page` | `access.read` |
| `library` | `access.read` |
| `search` | `access.read` |
| `wearable-play` | `access.read` |
| `now-playing` | `access.read` |
| `devices` | `access.read` |
| `get-queue` | `access.read` |
| `save` | `library.manage` |
| `create-collection` | `library.manage` |
| `add-to-collection` | `library.manage` |
| `update-collection` | `library.manage` |
| `play` | `playback.control` |
| `pause` | `playback.control` |
| `resume` | `playback.control` |
| `skip` | `playback.control` |
| `previous` | `playback.control` |
| `seek` | `playback.control` |
| `set-volume` | `playback.control` |
| `transfer` | `playback.control` |
| `add-to-queue` | `playback.control` |
| `upload` | `content.manage` |
| `shows create` | `content.manage` |
| `shows delete` | `content.manage` |
| `shows get` | `access.read` |
| `shows` | `access.read` |
| `episodes create` | `content.manage` |
| `episodes delete` | `content.manage` |
| `episodes status` | `access.read` |
| `episodes` | `access.read` |
| `timeline set` | `content.manage` |
| `timeline get` | `access.read` |
| `timeline delete` | `content.manage` |
| `list` | `access.read` |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把 content resolver 与 playback adapter 分开，返回 resolved 与 played 两种状态；集合操作携带 revision 防止并发漂移。

最小验收建议：歌曲同名翻唱、多设备、wearable 仅解析成功和节目管理 unavailable 时都应给准确结果。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Spotify](../../../opt/hatch/skills/spotify/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/spotify/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/spotify/SKILL.md#L13) | 13 |
| [Connection](../../../opt/hatch/skills/spotify/SKILL.md#L16) | 16 |
| [Browse & Discover](../../../opt/hatch/skills/spotify/SKILL.md#L21) | 21 |
| [Search](../../../opt/hatch/skills/spotify/SKILL.md#L25) | 25 |
| [Filter values](../../../opt/hatch/skills/spotify/SKILL.md#L29) | 29 |
| [Library](../../../opt/hatch/skills/spotify/SKILL.md#L34) | 34 |
| [Delete Save to Spotify shows or episodes](../../../opt/hatch/skills/spotify/SKILL.md#L38) | 38 |
| [Collections (Playlists)](../../../opt/hatch/skills/spotify/SKILL.md#L49) | 49 |
| [Playback Control](../../../opt/hatch/skills/spotify/SKILL.md#L54) | 54 |
| [Wearable (glasses) playback](../../../opt/hatch/skills/spotify/SKILL.md#L68) | 68 |
| [Known unavailable or conditional commands](../../../opt/hatch/skills/spotify/SKILL.md#L72) | 72 |
| [Auth](../../../opt/hatch/skills/spotify/SKILL.md#L77) | 77 |
| [Operating Rules](../../../opt/hatch/skills/spotify/SKILL.md#L87) | 87 |
