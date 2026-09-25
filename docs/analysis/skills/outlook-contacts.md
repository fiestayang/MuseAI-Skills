# outlook-contacts：Outlook 联系人检索与局部更新

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

Outlook 联系人检索与局部更新。入口：[SKILL.md](../../../opt/hatch/skills/outlook-contacts/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `outlook-contacts` |
| frontmatter name | `outlook_contacts` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> List, search, create, update, and delete contacts in the user's Outlook account.

<a id="flow"></a>
## 执行流程与输入输出

--status 管理连接；search 定位或 list 分页；get 读取完整条目；create/update/delete 使用返回的 resource_name；只指定需要更改的字段。

<a id="design"></a>
## 实现思路、异常与限制

CLI 对外统一 contact 展示字段，底层 Graph ID 保持不透明。与 Google 集合替换规则不同，正文承诺未指定字段保持不变，应由 adapter 实现这一语义。

重名不能猜测目标。分页不全不能宣称通讯录无结果；认证失败回 status，不能尝试共享 helper 或手写 token 文件。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/outlook-contacts/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/outlook-contacts/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### outlook-contacts/manifest.yaml

来源：[opt/hatch/skills/outlook-contacts/manifest.yaml](../../../opt/hatch/skills/outlook-contacts/manifest.yaml)；connector：`outlook_contacts`。

请求配额声明：`mode` = `enforce`；`workers` = `['outlook-contacts']`；`queries_per_minute` = `600`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `contacts.list` | `allow` | 否 | — | Access contacts |
| `write` | `contacts.create` | `allow` | 否 | — | Create contacts |
| `write` | `contacts.update` | `allow` | 否 | — | Edit contacts |
| `write` | `contacts.delete` | `allow` | 否 | — | Delete contacts |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时在 provider adapter 内实现 patch 语义，并对每种 provider 的集合更新行为单独验证。

最小验收建议：只改一个电话后其他邮箱、组织和姓名必须保留；同名结果不能直接删除。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Outlook Contacts](../../../opt/hatch/skills/outlook-contacts/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/outlook-contacts/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/outlook-contacts/SKILL.md#L13) | 13 |
| [Auth](../../../opt/hatch/skills/outlook-contacts/SKILL.md#L41) | 41 |
| [Operating Rules](../../../opt/hatch/skills/outlook-contacts/SKILL.md#L56) | 56 |
