# media-library：已上传图库与设备图库的分层检索

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

已上传图库与设备图库的分层检索。入口：[SKILL.md](../../../opt/hatch/skills/media-library/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `media-library` |
| frontmatter name | `media_library` |
| includeInPrompt | `true` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Search and inspect the user's photo library, including connected device galleries. Use for photo requests and whenever a photo could ground or personalize a response; lookups of uploaded photos are cheap, so check opportunistically and move on if nothing fits.

<a id="flow"></a>
## 执行流程与输入输出

已上传照片先 stats，再 search/recent，候选 scan 与 get，描述不足才读图；个人照片需求在上传库不足时发现设备并 describe photos.search；选中设备照片后按实际能力上传为可用素材。

<a id="design"></a>
## 实现思路、异常与限制

元数据检索和实际像素获取分开。FTS/BM25 依赖已生成描述，未描述照片应通过日期或 recent 寻找，而不能得出不存在结论。

设备搜索结果本身不是可供模型读图的文件；权限拒绝和分页不全要反映到覆盖范围。不能从个人图像任意推断敏感属性。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/media-library/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时为照片保留上传状态、描述状态与设备来源；先小范围候选再传大图，避免无谓同步整个相册。

最小验收建议：图库有照片但描述 pending 时文字检索空，应转 recent；设备仅返回 metadata 时不能声称看过画面。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Media Library](../../../opt/hatch/skills/media-library/SKILL.md#L7) | 7 |
| [Purpose](../../../opt/hatch/skills/media-library/SKILL.md#L9) | 9 |
| [Device Photos](../../../opt/hatch/skills/media-library/SKILL.md#L12) | 12 |
| [Tooling](../../../opt/hatch/skills/media-library/SKILL.md#L21) | 21 |
| [Operating Rules](../../../opt/hatch/skills/media-library/SKILL.md#L40) | 40 |
