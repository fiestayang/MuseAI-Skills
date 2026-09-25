# MuseAI-Skills 详细分析报告

分析基线：`61121abf5c4da12fe32ef970a861108b16a0731b`。分析日期：2026-09-25。来源：[win4r/MuseAI-Skills](https://github.com/win4r/MuseAI-Skills)。以当前本地 checkout 的文件为准。

这是一份技能与运行环境快照。主要可复用资产是工作流约束、工具契约、权限声明和 Linux 生命周期脚本；核心 Agent、CLI、授权与调度执行器没有完整源码。报告分析其可见实现，不将二进制接口或文档声明写成已验证内部算法。

## 目录

| 阅读顺序 | 文档 | 回答的问题 |
|---|---|---|
| 1 | [仓库总览](01-repository-overview.md) | 来源、规模、模块职责、能分析到哪里 |
| 2 | [完整目录导览](02-directory-guide.md) | 文件如何组织、从哪里进入 |
| 3 | [技能选择与加载](03-skill-selection-and-loading.md) | 可见、发现、选择、按需加载、执行的分层 |
| 4 | [工具与权限](04-tooling-and-permissions.md) | CLI、MCP、manifest、OAuth、审批与配额 |
| 5 | [运行与隔离](05-runtime-and-isolation.md) | 启动、网络、凭据、rootfs、停机和恢复 |
| 6 | [状态与后台工作](06-state-and-background-work.md) | 记忆、目标、调度、执行和交付记录 |
| 7 | [评测与缺项](07-evaluation-and-gaps.md) | 行为场景覆盖、矛盾、风险及未知 |
| 8 | [迁移开发指引](08-development-guide.md) | 为其他仓库开发类似模块的最小方案 |
| 9 | [实际验证记录](09-validation.md) | 本次运行了什么、证明什么、没有证明什么 |

逐对象深入阅读：

- [68 个独立技能与 4 个别名](skills/README.md)：每篇包含触发、流程、实现思路、逐文件分析、权限、评测及迁移建议。
- [27 个运行时文本文件](runtime/README.md)：22 个 runtime-cell 文件及 5 个镜像侧文本文件。
- [产品说明与用户配置](appendices/product-docs.md)：逐文件解释产品表面与行为约束。
- [Artifacts 共享参考与 Spaces](appendices/shared-resources.md)：不归单个 SKILL 的共享资源。
- [数据库逐表导航](appendices/database-schema.md)：每个已声明关系的字段、键和关联说明。
- [技能—工具映射](appendices/skill-tool-matrix.md)：已出现的本地工具依赖与权限材料。
- [二进制接口清单](appendices/binaries.md)：格式、大小、内容重复与文本调用证据。
- [第三方组件](appendices/third-party-components.md)：npm 源码流程、依赖包、许可与分析边界。
- [全部 2,658 个基线路径覆盖清单](appendices/file-coverage.md)：文件类型、分析归属和深度。
- [证据与未知项](appendices/evidence-and-unknowns.md)：结论分级及不应推断的内部行为。

## 如何使用

理解系统先读 1–6，再从技能目录选择相近业务。为其他仓库实现模块时，先读开发指引，再对照对应技能的异常路径和最小验收建议。排查具体文件直接查覆盖清单。

文中四种证据口径：

| 标签 | 含义 |
|---|---|
| 代码事实 | 可见脚本、HTML 或配置直接证明的结构与分支 |
| 文档声明 | SKILL、产品说明、schema 或脚本注释描述的约定 |
| 推断 | 从多个文件组合推导，但缺乏完整执行器验证 |
| 开发建议 | 为其他项目提出的实现选择，不是本仓库已有功能 |

引用使用相对路径和基线行号。GitHub 可定位 `#L`；本地阅读器若不支持，按标明标题或符号定位。源码不随本报告修改。旧 [PROJECT_ANALYSIS.md](../../PROJECT_ANALYSIS.md) 保留为历史分析材料，不作为当前验证结果。

## 覆盖与限制

全部独立 SKILL 有独立文章。配套参考、manifest 和 eval 在所属文章逐项说明；共享资源另列。第三方 npm 的 2,269 个路径全量入索引，正文按包与功能分析，未逐函数审计所有第三方依赖。二进制逐项记录接口证据，未反编译。

报告中的命令示例和 Agent 指令都是研究对象，不是要求在当前电脑执行的操作。没有启动 Muse、容器、钱包、邮箱或其他外部连接器；没有把 YAML 场景视为已通过测试。
