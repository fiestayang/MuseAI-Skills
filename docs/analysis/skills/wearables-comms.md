# wearables-comms：穿戴来源的通话与短信

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

穿戴来源的通话与短信。入口：[SKILL.md](../../../opt/hatch/skills/wearables-comms/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `wearables-comms` |
| frontmatter name | `wearables_comms` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> >- Required for every call or text-message request originating on a wearable: resolve named recipients from synced device contacts and invoke the originating wearable, not a paired phone.

<a id="flow"></a>
## 执行流程与输入输出

list/describe 固定来源穿戴设备；完整号码直接用，否则先从该设备同步缓存查联系人；检查所有候选和号码标签；歧义时保留原短信正文并给可辨识选项；使用实时公布的通话或短信命令 invoke。

<a id="design"></a>
## 实现思路、异常与限制

明确把“用户自己通话”与“Agent 代谈”分开。联系人匹配、号码选择和动作执行是三步；发信内容不能为歧义收件人提供授权。

不能因手机也能打电话而改用手机；同音名需要拼读或号码后缀。超时或中断不能盲目重拨/重发。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/wearables-comms/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时为语音澄清设计稳定候选序号与可读标签，暂存待发正文但不执行，目标确认后恢复同一操作。

最小验收建议：同音联系人和多线路测试，确认澄清期间正文不变；设备超时后状态应为未知而非失败后自动重试。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Wearables Calls and Messages](../../../opt/hatch/skills/wearables-comms/SKILL.md#L11) | 11 |
| [Purpose](../../../opt/hatch/skills/wearables-comms/SKILL.md#L13) | 13 |
| [Select the device](../../../opt/hatch/skills/wearables-comms/SKILL.md#L24) | 24 |
| [Resolve a recipient](../../../opt/hatch/skills/wearables-comms/SKILL.md#L38) | 38 |
| [Ask for clarification](../../../opt/hatch/skills/wearables-comms/SKILL.md#L76) | 76 |
| [Place a call](../../../opt/hatch/skills/wearables-comms/SKILL.md#L116) | 116 |
| [Send a message](../../../opt/hatch/skills/wearables-comms/SKILL.md#L124) | 124 |
| [Report the result](../../../opt/hatch/skills/wearables-comms/SKILL.md#L142) | 142 |
