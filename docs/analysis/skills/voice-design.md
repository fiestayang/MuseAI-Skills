# voice-design：语音选择与异步定制

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

语音选择与异步定制。入口：[SKILL.md](../../../opt/hatch/skills/voice-design/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `voice-design` |
| frontmatter name | `voice_design` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Choose or design a new speaking voice when the user asks for a new, different, custom, invented, or generated voice.

<a id="flow"></a>
## 执行流程与输入输出

用户没有方向时只问一次；有方向后 muse.voice_options 调一次，按许可决定 allow_create_new_voices；默认单结果直接选择，明确要二或三项时仅返回选项；定制由一个后台 worker 完成。

<a id="design"></a>
## 实现思路、异常与限制

允许创建并不意味着一定创建，运行时可以选择已有最佳声音。返回 options、选中、保存和 live_switch_completed 是不同结果，尤其通话中需要确认实际切换完成。

后台生成不得轮询或再开第二个设计；多个新声音请求当前只能逐个处理。通话已结束时不能说正在通话的声音已更换。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/voice-design/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时用显式结果 union 表达 options、pending、selected 和 switched，UI 根据结果而非模型措辞更新。

最小验收建议：candidate_count=3 不应自动选择；生成完成但通话已结束时应只报告保存结果。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Voice design](../../../opt/hatch/skills/voice-design/SKILL.md#L7) | 7 |
| [Start naturally](../../../opt/hatch/skills/voice-design/SKILL.md#L13) | 13 |
| [Choose the path](../../../opt/hatch/skills/voice-design/SKILL.md#L27) | 27 |
| [Report the result](../../../opt/hatch/skills/voice-design/SKILL.md#L60) | 60 |
