# share-ideas：显式发布可复用原生 Idea

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

显式发布可复用原生 Idea。入口：[SKILL.md](../../../opt/hatch/skills/share-ideas/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `share-ideas` |
| frontmatter name | `share_ideas` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Publish a reusable native Muse Idea with idea.share when the user explicitly asks to share or publish an Idea or asks for a muse.ai/ideas link. Never offer it unprompted. Not for pages or write-ups, sending a result to someone, social posts, or sharing an artifact.

<a id="flow"></a>
## 执行流程与输入输出

仅用户明确要发布 Idea 或特定 ideas 链接时触发；已有 Idea 先 search/list 再 get；内容齐全时 share 仅传 idea_id；需要形成可复用指导时确保标题、摘要、How it works 与 instructions 各自完整并去除个人信息。

<a id="design"></a>
## 实现思路、异常与限制

分享对象是可复用指令及说明，受众是持链接的已认证 Muse 用户；它不同于 artifact 网页分享、社交发布或发送结果给某个人。

不能主动推荐发布；不能把私人上下文、具体账号或原始附件隐含带入模板。拿到任意页面链接不表示已经发布原生 Idea。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/share-ideas/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时把 reusable recipe 与 execution instance 分开，发布前扫描实例数据泄漏，使用单独 publish 命令。

最小验收建议：用户只说“发给朋友这份报告”不应触发 Idea 发布；已保存完整 Idea 不应被无理由重写。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Share ideas](../../../opt/hatch/skills/share-ideas/SKILL.md#L8) | 8 |
