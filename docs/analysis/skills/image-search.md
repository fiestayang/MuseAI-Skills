# image-search：公共图片搜索与来源保留

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

公共图片搜索与来源保留。入口：[SKILL.md](../../../opt/hatch/skills/image-search/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `image-search` |
| frontmatter name | `image_search` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Search the web by text query for image URLs and source pages for feeds, artifacts, and visual references. Does not identify a supplied image or person.

<a id="flow"></a>
## 执行流程与输入输出

按文字查询 image-search；优先 media_url，缺失时用 thumbnail_cdn_url；保留 page_url 来源；交付引用图片前按用途检查可获取性与相关性。

<a id="design"></a>
## 实现思路、异常与限制

图片字节 URL、来源页面 URL 和内部 media handle 是不同类型。CDN 预览适合展示但不应成为持久 artifact 唯一副本。

不做上传图片或人物身份识别；不能将 candidate_ref 当图片 URL。搜索返回不保证许可、永久可用或内容与查询完全一致。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/image-search/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时将 assetUrl、previewUrl、sourcePage 和 opaqueHandle 分开，保存素材时保留来源与获取时间。

最小验收建议：仅缩略图结果及失效原图测试，确认正确降级并不把内部 handle 发给渲染器。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Image Search](../../../opt/hatch/skills/image-search/SKILL.md#L7) | 7 |
