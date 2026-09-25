# forget：跨记忆及衍生状态的遗忘事务

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

跨记忆及衍生状态的遗忘事务。入口：[SKILL.md](../../../opt/hatch/skills/forget/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `forget` |
| frontmatter name | `forget` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Remove a personal fact, preference, relationship detail, topic, or prior event from Muse's active memory and stop existing copies or automations from bringing it back. Use for explicit requests such as 'forget that', 'don't remember this about me', or 'remove that from your memory'. Do not use when 'forget it' merely means cancel the current task.

<a id="flow"></a>
## 执行流程与输入输出

forget.plan 以空参数启动只读规划，继承对话识别对象；清点原始记忆、衍生内容和未来生产者；展示范围和不可逆动作并取得后续明确确认；forget.confirm 启动新执行者重新核实，先停止获准的后台生产者，再按所属产品工具清理；写 pending.json 的 claim IDs 与引用定位；运行时撤回 claim 并刷新检索后才汇报。

<a id="design"></a>
## 实现思路、异常与限制

规划与执行分离，且不在工具参数、文件名或报告中再次复制要遗忘的内容。闭环不只是删除文件，还包含停止回写来源和更新检索投影。pending.json 即使两个列表为空也要写，表明执行者完成了交接。

工具失败不得改用临时手工删除。引用刷新失败或子工作未结束时只能报告未完成。混合内容文件需要局部编辑；外部邮件、其他人副本和共享发布物没有被一次遗忘请求自动授权删除。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/forget/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [references/artifact-inventory.md](../../../opt/hatch/skills/forget/references/artifact-inventory.md) | 逐层检查会话/源文件/检索投影/后台产物/未来生产者/分享/外部缓存/保留副本，记录 owner、定位、前置条件、可逆性和验证。清单不是全域删除授权。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把删除范围快照、审批、执行、索引撤回和验证做成显式状态机。最小实现也必须能证明不存在仍会回写的生产者，不能把数据库删除成功当作整体完成。

最小验收建议：注入一个仍排队的记忆生产任务和一次检索刷新失败；验收应阻止完成声明，并保持未授权数据不变。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Forget](../../../opt/hatch/skills/forget/SKILL.md#L7) | 7 |
| [Make a plan](../../../opt/hatch/skills/forget/SKILL.md#L21) | 21 |
| [Ask, then execute](../../../opt/hatch/skills/forget/SKILL.md#L47) | 47 |
| [Report honestly](../../../opt/hatch/skills/forget/SKILL.md#L102) | 102 |

### references/artifact-inventory.md

| 源章节 | 起始行 |
|---|---|
| [Forget artifact inventory](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L1) | 1 |
| [1. Conversation and live execution](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L8) | 8 |
| [2. Source files and standing context](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L27) | 27 |
| [3. Memory retrieval and derived projections](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L68) | 68 |
| [4. Self-improvement outputs](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L100) | 100 |
| [5. Goals, schedules, and future producers](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L137) | 137 |
| [6. Artifacts and sharing](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L174) | 174 |
| [7. Connected and cached sources](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L190) | 190 |
| [8. Operational and retained copies](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L204) | 204 |
| [9. Verification closure](../../../opt/hatch/skills/forget/references/artifact-inventory.md#L216) | 216 |
