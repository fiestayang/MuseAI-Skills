# voice-selector：静态声音目录的占位入口

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

静态声音目录的占位入口。入口：[SKILL.md](../../../opt/hatch/skills/voice-selector/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `voice-selector` |
| frontmatter name | `voice_selector` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Provides the static system voice catalog used by Jarvis. It does not define a user-facing workflow.

<a id="flow"></a>
## 执行流程与输入输出

该 SKILL 仅说明目录用于提供 voice_source.json；用户请求选声音时转 muse.voice_options 或 voice-design；生成 TTS 时由相应技能读取静态目录。

<a id="design"></a>
## 实现思路、异常与限制

这不是执行工作流。metadata.voiceOnly 与 includeInPrompt=false 是元数据声明，voice-calls 别名也不能改变它的职责。

voice_source.json 在本快照缺失；不能列出已验证完整声库，更不能从 voice-calls 名称推断代理打电话能力。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/voice-selector/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把只读资源与可调用技能分开建模，目录入口明确标记无动作，避免路由器把每个 SKILL 都当执行器。

最小验收建议：请求代打电话不能路由到这个静态目录；目录缺失时需明确失败而非编造声音 ID。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Voice Catalog Data](../../../opt/hatch/skills/voice-selector/SKILL.md#L7) | 7 |
