# printify：按店铺隔离的按需印刷管理

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

按店铺隔离的按需印刷管理。入口：[SKILL.md](../../../opt/hatch/skills/printify/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `printify` |
| frontmatter name | `printify` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Use Printify to browse catalog data, manage shops and products, and review or create orders.

<a id="flow"></a>
## 执行流程与输入输出

status/verify 完成连接；shops 定位 shop_id；catalog 从 blueprints 到 print-providers 再到 variants；上传素材后创建或更新商品；publish 和 create-order 分别按明确审批执行。

<a id="design"></a>
## 实现思路、异常与限制

将商品定义、公开发布与订单区分，避免创建商品直接被理解为已售卖。token 通过 stdin 交 CLI，业务层不写认证文件。

create-order 可能产生费用；高级 request 写入也需审批。产品删除的默认与创建/发布不同，应看方法级策略而不是统一给所有 write 一个行为。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/printify/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |
| [manifest.yaml](../../../opt/hatch/skills/printify/manifest.yaml) | 声明权限组、方法默认、连接器与可选命令映射；完整解析见权限契约。声明不能替代执行器。 |

<a id="permissions"></a>
## 工具与权限契约

以下从 manifest 解析。有效默认取方法的 `default`，缺省时继承 action group；它不是当前用户的实际设置或 OAuth 授权状态。

### printify/manifest.yaml

来源：[opt/hatch/skills/printify/manifest.yaml](../../../opt/hatch/skills/printify/manifest.yaml)；connector：`printify`。

请求配额声明：`mode` = `enforce`；`workers` = `['printify']`；`queries_per_minute` = `300`；`burst` = `50`。

| 权限组 | 方法 | 有效默认 | 方法覆盖 | Scope / 响应保护 | 含义 |
|---|---|---|---|---|---|
| `read` | `shops.list` | `allow` | 否 | — | Access shops |
| `read` | `orders.list` | `allow` | 否 | — | Access orders |
| `read` | `api.read` | `allow` | 否 | — | Access via raw API request |
| `write` | `products.create` | `ask` | 否 | — | Create or edit products |
| `write` | `orders.create` | `ask` | 否 | — | Create orders |
| `write` | `api.write` | `ask` | 否 | — | Write or delete via raw API request |
| `write` | `products.delete` | `allow` | 是 | — | Delete products |


<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时实体引用同时携带 shopId、productId 和 variantId，价格与生产供应商绑定；订单保留精确版本。

最小验收建议：跨店铺同名商品和不可用 variant 场景应拒绝误操作；订单审批必须包含具体商品与费用。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Printify (Print on Demand)](../../../opt/hatch/skills/printify/SKILL.md#L8) | 8 |
| [Purpose](../../../opt/hatch/skills/printify/SKILL.md#L10) | 10 |
| [Tooling](../../../opt/hatch/skills/printify/SKILL.md#L13) | 13 |
| [Auth](../../../opt/hatch/skills/printify/SKILL.md#L54) | 54 |
| [Operating Rules](../../../opt/hatch/skills/printify/SKILL.md#L64) | 64 |
