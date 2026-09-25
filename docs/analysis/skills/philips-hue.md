# philips-hue：OAuth 与 Bridge 就绪后的灯光控制

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

OAuth 与 Bridge 就绪后的灯光控制。入口：[SKILL.md](../../../opt/hatch/skills/philips-hue/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `philips-hue` |
| frontmatter name | `philips_hue` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Control Philips Hue smart lights, rooms, scenes, and devices via the Hue Remote API v2.

<a id="flow"></a>
## 执行流程与输入输出

status 检查 ready；未连接先授权；已连接但无 application key 时 link-bridge，再复查；list-lights/rooms/scenes 发现真实 ID；light/group/scene 执行用户指定控制。

<a id="design"></a>
## 实现思路、异常与限制

把 OAuth 连接与 Bridge 配对就绪分开，避免“connected”被当作立即可控。控制作用域分单灯、组和场景；凭据与应用 key 均由 CLI 管理。

不能猜灯 ID、房间或 scene；远程 Bridge 自动配对是文档特定契约，不能推广为所有智能硬件均不需实体操作。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/philips-hue/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/philips-hue/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### philips-hue/manifest.yaml

来源：[opt/hatch/skills/philips-hue/manifest.yaml](../../../opt/hatch/skills/philips-hue/manifest.yaml)；connector：`philips_hue`。

请求配额声明：`mode` = `enforce`；`workers` = `['philips-hue']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `lights.list` | `allow` | 否 | — | Access lights, rooms, zones, and scenes |
| `read` | `devices.list` | `allow` | 否 | — | Access devices, sensors, buttons, and device state |
| `write` | `light.control` | `allow` | 否 | — | Control lights and groups |
| `write` | `scene.activate` | `allow` | 否 | — | Activate scenes |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时返回 connected、bridgeLinked、ready 的明确状态；硬件效果参数保留范围验证和设备能力校验。

最小验收建议：connected=true 但无 key 时先链接，不能控制；亮度越界及未知场景应拒绝。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Philips Hue (Smart Lighting)](../../../opt/hatch/skills/philips-hue/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/philips-hue/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/philips-hue/SKILL.md#L13) | 13 |
| [Authentication subcommands](../../../opt/hatch/skills/philips-hue/SKILL.md#L20) | 20 |
| [Setup subcommands](../../../opt/hatch/skills/philips-hue/SKILL.md#L25) | 25 |
| [Discovery subcommands](../../../opt/hatch/skills/philips-hue/SKILL.md#L28) | 28 |
| [Control subcommands](../../../opt/hatch/skills/philips-hue/SKILL.md#L37) | 37 |
| [User Onboarding](../../../opt/hatch/skills/philips-hue/SKILL.md#L46) | 46 |
| [Step 1 — Check Status](../../../opt/hatch/skills/philips-hue/SKILL.md#L50) | 50 |
| [Step 2 — Connect Philips Hue](../../../opt/hatch/skills/philips-hue/SKILL.md#L53) | 53 |
| [Step 3 — Bridge Linking](../../../opt/hatch/skills/philips-hue/SKILL.md#L60) | 60 |
| [Step 4 — Welcome & Discovery](../../../opt/hatch/skills/philips-hue/SKILL.md#L65) | 65 |
| [Credential Safety](../../../opt/hatch/skills/philips-hue/SKILL.md#L68) | 68 |
| [Disconnect](../../../opt/hatch/skills/philips-hue/SKILL.md#L73) | 73 |
