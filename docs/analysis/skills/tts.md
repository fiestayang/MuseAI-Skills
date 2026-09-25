# tts：输入文本的单人或多人语音合成

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

输入文本的单人或多人语音合成。入口：[SKILL.md](../../../opt/hatch/skills/tts/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `tts` |
| frontmatter name | `tts` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Turn supplied text into spoken audio, single or multi-speaker. For composed audio content (a podcast, briefing, or narrated summary), use podcast.

<a id="flow"></a>
## 执行流程与输入输出

从系统目录或 user/voices.json 取精确 voice ID；短文本 speak，长文本或多人 synthesize-script；为所有说话人建立映射；按句子分块且每块最多两人；串行合成后拼接，返回路径、时长及内部 artifact handle。

<a id="design"></a>
## 实现思路、异常与限制

文本作为原样朗读输入，语言须与 --language 一致。saved_voice_id、profile_id 与可用于合成的 voice_id 不同。多说话人支持来自分块安排，并非底层单次 API 支持无限人。

系统语音目录缺失；失败可能已耗尽内部重试，后续只能有限退避且保持原命令。voice 缓存调试建议与用户要求逐字朗读可能冲突，不应擅改交付文本。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/tts/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/tts/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### tts/manifest.yaml

来源：[opt/hatch/skills/tts/manifest.yaml](../../../opt/hatch/skills/tts/manifest.yaml)；connector：`tts`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时明确输入保真要求，标准化 voice ID 类型与分块映射；保留片段状态便于恢复，但只有完整合成才能标记完成。

最小验收建议：未映射说话人、三人交错和非英语文本测试，确认每块符合约束、语言正确、最终音频完整。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [TTS](../../../opt/hatch/skills/tts/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/tts/SKILL.md#L9) | 9 |
| [Voice Sources](../../../opt/hatch/skills/tts/SKILL.md#L12) | 12 |
| [Prefer the Meta AI voices by default](../../../opt/hatch/skills/tts/SKILL.md#L27) | 27 |
| [Language](../../../opt/hatch/skills/tts/SKILL.md#L39) | 39 |
| [Tooling](../../../opt/hatch/skills/tts/SKILL.md#L58) | 58 |
| [`tts speak` — Single-shot synthesis](../../../opt/hatch/skills/tts/SKILL.md#L60) | 60 |
| [Core flags](../../../opt/hatch/skills/tts/SKILL.md#L78) | 78 |
| [`tts synthesize-script` — Multi-speaker script synthesis](../../../opt/hatch/skills/tts/SKILL.md#L91) | 91 |
| [Script file format](../../../opt/hatch/skills/tts/SKILL.md#L114) | 114 |
| [What it does automatically](../../../opt/hatch/skills/tts/SKILL.md#L124) | 124 |
| [Core flags](../../../opt/hatch/skills/tts/SKILL.md#L132) | 132 |
| [Output Contract](../../../opt/hatch/skills/tts/SKILL.md#L143) | 143 |
| [Handling Failures](../../../opt/hatch/skills/tts/SKILL.md#L163) | 163 |
| [Operating Rules](../../../opt/hatch/skills/tts/SKILL.md#L200) | 200 |
